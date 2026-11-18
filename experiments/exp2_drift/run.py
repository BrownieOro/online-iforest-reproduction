"""Thí nghiệm concept drift trên INSECTS (Mục 5.2, Hình 7): đánh giá prequential theo thứ tự gốc.

Luồng giữ nguyên thứ tự `row_index` của `data/processed/insects.csv`, không xáo trộn, không chia
tập ngẫu nhiên. Mỗi lô `batch_size` mẫu được chấm điểm trước rồi mới cho mô hình học (test-then-
train), nên điểm của một mẫu không dùng thông tin của chính nó hay tương lai. Lô đầu tiên chỉ dùng
để khởi động (mô hình rỗng chưa chấm được) và không được đánh giá.

Mỗi lần chạy `(model, seed)` ghi `config.json`, `metrics.json`, `predictions.csv` vào
`<output>/<model>_seed<seed>/` (Contract C5).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import sklearn
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score, roc_auc_score

from oif.forest import OnlineIsolationForest
from oif.tracking import log_run


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "insects.csv"
N_FEATURES = 33
# Dòng đầu tiên của mỗi đoạn mới (row_index); nguồn: data/README.md, mục "Mốc thay đổi phân phối".
CHANGE_POINTS = (51255, 74381, 100944, 142291, 152207)
MODELS = ("oif", "asdifor")


def load_insects(path, n_samples=None, n_features=N_FEATURES):
    """Đọc `n_samples` dòng đầu (None = toàn bộ) và `n_features` đặc trưng đầu, giữ thứ tự dòng."""
    with path.open(encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != [*(f"x{i}" for i in range(N_FEATURES)), "label"]:
        raise ValueError(f"Unexpected columns in {path.name}; run scripts/prepare_insects.py")
    data = np.loadtxt(path, delimiter=",", skiprows=1, dtype=float, ndmin=2, max_rows=n_samples)
    X, y = data[:, :n_features], data[:, -1].astype(int)
    if not np.isfinite(X).all() or not np.isin(y, [0, 1]).all():
        raise ValueError(f"{path.name} contains invalid feature values or labels")
    return X, y


class SlidingIForest:
    """Baseline kiểu asdIFOR do nhóm tự dựng trên `sklearn.ensemble.IsolationForest`.

    Giữ `window_size` mẫu gần nhất. Khi chưa đủ một cửa sổ, huấn luyện lại trên mọi mẫu đã thấy
    sau mỗi lô; sau đó huấn luyện lại trên `window_size` mẫu gần nhất mỗi khi đã thấy thêm ít nhất
    `window_size` mẫu kể từ lần huấn luyện trước (cửa sổ rời, không chồng lấn). Giữa hai lần huấn
    luyện, mô hình được giữ cố định. Đây không phải mã của pysad mà tác giả dùng.
    """

    def __init__(self, window_size, n_estimators, max_samples, seed):
        self.window_size = window_size
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.rng = np.random.default_rng(seed)
        self.buffer = np.empty((0, 0))
        self.n_seen = 0
        self.last_fit = 0
        self.n_fits = 0
        self.model = None

    def learn_batch(self, X):
        """Đưa lô vào bộ đệm cửa sổ; huấn luyện lại theo quy tắc ở docstring lớp."""
        self.buffer = X.copy() if self.n_seen == 0 else np.vstack([self.buffer, X])
        self.buffer = self.buffer[-self.window_size:]
        self.n_seen += len(X)
        if self.n_seen <= self.window_size or self.n_seen - self.last_fit >= self.window_size:
            self.model = IsolationForest(
                n_estimators=self.n_estimators,
                max_samples=min(self.max_samples, len(self.buffer)),
                random_state=int(self.rng.integers(2**31 - 1)), n_jobs=1,
            ).fit(self.buffer)
            self.last_fit = self.n_seen
            self.n_fits += 1
        return self

    def score_samples(self, X):
        """Điểm bất thường trong (0, 1], cao = bất thường (đổi dấu `score_samples` của sklearn)."""
        return -self.model.score_samples(X)


def make_model(name, seed, args):
    """Khởi tạo mô hình và trả kèm tham số để ghi vào config.

    `forest.py` gán seed `seed + i` cho cây thứ i, nên hai seed liền nhau dùng chung n_trees - 1
    cây. Vì vậy truyền `seed * n_trees` để các seed không có cây trùng nhau.
    """
    if name == "oif":
        forest_seed = seed * args.n_trees
        params = {"n_trees": args.n_trees, "window_size": args.window_size, "eta": args.eta,
                  "forest_seed": forest_seed, "tree_seeds": f"forest_seed + i, i < {args.n_trees}"}
        return OnlineIsolationForest(args.n_trees, args.window_size, args.eta, forest_seed), params
    params = {"implementation": "group SlidingIForest over sklearn.ensemble.IsolationForest",
              "n_estimators": args.n_trees, "window_size": args.window_size,
              "max_samples": args.asd_max_samples, "seed": seed}
    return SlidingIForest(args.window_size, args.n_trees, args.asd_max_samples, seed), params


def _auc_ap(y, scores):
    """ROC-AUC và AP; None nếu đoạn chỉ có một lớp (không định nghĩa được)."""
    if len(y) == 0 or len(np.unique(y)) < 2:
        return None, None
    return float(roc_auc_score(y, scores)), float(average_precision_score(y, scores))


def segment_ids(n):
    """Số thứ tự đoạn (1..6) của từng dòng 0..n-1 theo CHANGE_POINTS."""
    return np.searchsorted(np.asarray(CHANGE_POINTS), np.arange(n), side="right") + 1


def evaluate(y, scores, warmup, batch_seconds, batch_starts, window, step):
    """Chỉ số toàn luồng, theo từng đoạn và theo cửa sổ trượt (chỉ trên các dòng đã chấm điểm)."""
    n = len(y)
    seg = segment_ids(n)
    rows = np.arange(warmup, n)
    roc_auc, ap = _auc_ap(y[rows], scores[rows])
    segments = []
    bounds = [0, *CHANGE_POINTS, max(n, CHANGE_POINTS[-1] + 1)]
    for k, (a, b) in enumerate(zip(bounds[:-1], bounds[1:]), start=1):
        mask = rows[(seg[rows] == k)]
        if len(mask) == 0:
            continue
        s_auc, s_ap = _auc_ap(y[mask], scores[mask])
        in_seg = (batch_starts >= a) & (batch_starts < b)
        segments.append({"segment": k, "row_start": a, "row_stop": min(b, n),
                         "n_evaluated": int(len(mask)), "n_anomaly": int(y[mask].sum()),
                         "roc_auc": s_auc, "average_precision": s_ap,
                         "seconds": float(batch_seconds[in_seg].sum())})
    starts = list(range(warmup, n - window + 1, step))
    sliding = [_auc_ap(y[s:s + window], scores[s:s + window]) for s in starts]
    return {
        "n_evaluated": int(len(rows)), "n_anomaly_evaluated": int(y[rows].sum()),
        "roc_auc": roc_auc, "average_precision": ap, "segments": segments,
        "sliding_window": {"size": window, "step": step, "row_start": starts,
                           "roc_auc": [a for a, _ in sliding],
                           "average_precision": [p for _, p in sliding]},
    }


def _git(*args):
    """Chạy lệnh git chỉ đọc tại gốc repo và trả stdout."""
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout.strip()


def run_once(name, seed, X, y, args, output, data_sha256):
    """Chạy prequential một mô hình với một seed và ghi 3 tệp theo C5."""
    model, params = make_model(name, seed, args)
    n, bs = len(X), args.batch_size
    scores = np.full(n, np.nan)
    batch_starts = np.arange(0, n, bs)
    batch_seconds = np.zeros(len(batch_starts))
    learn_seconds = score_seconds = 0.0
    for b, start in enumerate(batch_starts):
        batch = X[start:start + bs]
        t0 = time.perf_counter()
        if start > 0:
            scores[start:start + bs] = model.score_samples(batch)
        t1 = time.perf_counter()
        model.learn_batch(batch)
        t2 = time.perf_counter()
        score_seconds += t1 - t0
        learn_seconds += t2 - t1
        batch_seconds[b] = t2 - t0
    warmup = min(bs, n)
    if not np.isfinite(scores[warmup:]).all():
        raise ValueError(f"{name} seed {seed}: non-finite scores")

    metrics = evaluate(y, scores, warmup, batch_seconds, batch_starts, args.eval_window,
                       args.eval_step)
    metrics = {"model": name, "seed": seed, "n_samples": n, "n_features": int(X.shape[1]),
               "n_warmup": warmup, **metrics, "learn_seconds": learn_seconds,
               "score_seconds": score_seconds, "total_seconds": learn_seconds + score_seconds}
    if name == "asdifor":
        metrics["n_refits"] = model.n_fits

    config = {
        "experiment": "drift_prequential", "tags": ["reproduction", "drift", name],
        "git_commit": _git("rev-parse", "HEAD"),
        "git_worktree_dirty": bool(_git("status", "--porcelain")),
        "dataset": "insects", "dataset_path": "data/processed/insects.csv",
        "dataset_sha256": data_sha256, "n_samples": n, "n_features": int(X.shape[1]),
        "change_points": list(CHANGE_POINTS),
        "protocol": ("original row order, no shuffle/split; batches of batch_size; score each batch "
                     "before learning it; first batch is warm-up only and not evaluated"),
        "preprocessing": ("none: prepared CSV used as is (no scaling, imputation, shuffling or "
                          f"deduplication); first {int(X.shape[1])} of 33 features"),
        "timing": ("time.perf_counter wall-clock seconds, measured separately for scoring and "
                   "learning of each batch; data loading and file writing excluded"),
        "model": name, "seed": seed, "params": params, "batch_size": bs,
        "eval_window": args.eval_window, "eval_step": args.eval_step,
        "python": platform.python_version(), "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "known_deviation": ("Author script learns each batch before scoring it, uses only the first "
                            "10 features and pysad IForestASD; this run scores before learning."),
    }
    output.mkdir(parents=True, exist_ok=False)
    seg = segment_ids(n)
    with (output / "predictions.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["row_index", "segment", "label", "anomaly_score"])
        for i in range(warmup, n):
            writer.writerow([i, int(seg[i]), int(y[i]), repr(float(scores[i]))])
    for fname, value in (("config", config), ("metrics", metrics)):
        (output / f"{fname}.json").write_text(json.dumps(value, indent=2, allow_nan=False),
                                              encoding="utf-8")
    log_run(config, metrics, output)
    return metrics


def main():
    """Đọc tham số dòng lệnh và chạy mọi cặp (model, seed)."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", nargs="+", choices=MODELS, default=list(MODELS))
    parser.add_argument("--seeds", nargs="+", type=int, default=[0])
    parser.add_argument("--n-samples", type=int, default=None, help="chỉ dùng n dòng đầu (smoke test)")
    parser.add_argument("--n-features", type=int, default=N_FEATURES)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--n-trees", type=int, default=32)
    parser.add_argument("--window-size", type=int, default=2048)
    parser.add_argument("--eta", type=float, default=32.0)
    parser.add_argument("--asd-max-samples", type=int, default=256)
    parser.add_argument("--eval-window", type=int, default=5000)
    parser.add_argument("--eval-step", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "raw" / "drift")
    args = parser.parse_args()
    if args.batch_size < 1 or not 1 <= args.n_features <= N_FEATURES or args.eval_window < 2:
        parser.error("batch-size >= 1, 1 <= n-features <= 33, eval-window >= 2")
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Missing {DATA_PATH}. Run: python scripts/prepare_insects.py")

    data_sha256 = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()
    X, y = load_insects(DATA_PATH, args.n_samples, args.n_features)
    for name in args.models:
        for seed in args.seeds:
            m = run_once(name, seed, X, y, args, args.output / f"{name}_seed{seed}", data_sha256)
            print(json.dumps({k: m[k] for k in ("model", "seed", "n_evaluated", "roc_auc",
                                                "average_precision", "total_seconds")}), flush=True)


if __name__ == "__main__":
    main()
