"""Tổng hợp thí nghiệm drift INSECTS.

Đọc d = 33 từ `results/raw/drift-v2/` (`config.json`/`metrics.json` từng lần chạy) và d = 10 từ
bảng từng run trong `results/drift-fixed-10.md` (5 seed sau sửa F1, có link W&B). Tạo
`results/drift-by-segment.csv`, `figures/drift-quality.png` và `results/drift.md`; script không
chạy lại mô hình.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "raw"
RUN_DIR_33 = RAW / "drift-v2"
FIXED10_PATH = ROOT / "results" / "drift-fixed-10.md"
BOOTSTRAP_CSV = ROOT / "results" / "drift-after-bootstrap.csv"
F1_FIX = "6ac25e3"  # commit sửa giới hạn độ sâu khi khởi động (F1)
CSV_PATH = ROOT / "results" / "drift-by-segment.csv"
FIGURE_PATH = ROOT / "figures" / "drift-quality.png"
REPORT_PATH = ROOT / "results" / "drift.md"
CHANGE_POINTS = [51255, 74381, 100944, 142291, 152207]
MODELS = {"oif": "OIF", "asdifor": "asdIFOR"}
METRICS = ("roc_auc", "average_precision", "learn_seconds", "score_seconds", "total_seconds")
STATS = ("median", "q1", "q3", "min", "max")
# Bảng màu phân loại mặc định đã kiểm tra (slot 1 xanh, slot 2 cam); đỏ cho mốc thay đổi.
COLORS = {"oif": "#2a78d6", "asdifor": "#eb6834", "change": "#d03b3b",
          "text": "#52514e", "grid": "#e4e3df"}


def load_runs(directory):
    """Đọc mọi `<model>_seed<s>/` trong thư mục; trả {model: [(config, metrics), ...]} theo seed."""
    runs = {}
    for run_dir in sorted(directory.glob("*_seed*")):
        config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
        metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
        if config["change_points"] != CHANGE_POINTS:
            raise ValueError(f"{run_dir} uses different change points")
        if not (run_dir / "predictions.csv").is_file():
            raise FileNotFoundError(f"{run_dir} is missing predictions.csv")
        runs.setdefault(config["model"], []).append((config, metrics))
    for model in runs:
        runs[model].sort(key=lambda item: item[0]["seed"])
    return runs


def load_fixed10(path=FIXED10_PATH):
    """Đọc bảng từng run trong `drift-fixed-10.md`; trả {model: [(seed, auc, ap, url), ...]}."""
    pattern = re.compile(r"^\| (oif|asdifor)_seed(\d+) \| ([0-9.]+) \| ([0-9.]+) \| "
                         r"\[run\]\((\S+)\) \|")
    runs = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = pattern.match(line)
        if m:
            runs.setdefault(m[1], []).append((int(m[2]), float(m[3]), float(m[4]), m[5]))
    if set(runs) != set(MODELS):
        raise ValueError(f"{path} must list runs for {sorted(MODELS)}")
    for model in runs:
        runs[model].sort()
    return runs


def has_commit(ancestor, commit):
    """True nếu `ancestor` nằm trong lịch sử của `commit` (dùng `git merge-base`)."""
    result = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, commit], cwd=ROOT,
                            capture_output=True)
    return result.returncode == 0


def bootstrap_check(runs33, path=BOOTSTRAP_CSV):
    """So ROC-AUC từng seed d = 33 với `drift-after-bootstrap.csv`; trả (số cặp, sai lệch lớn nhất)."""
    if not path.is_file():
        return None
    with path.open(encoding="utf-8-sig", newline="") as f:
        ref = {(r["model"], int(r["seed"])): float(r["roc_auc"]) for r in csv.DictReader(f)
               if r["n_features"] == "33"}
    diffs = [abs(m["roc_auc"] - ref[(model, c["seed"])]) for model, v in runs33.items()
             for c, m in v if (model, c["seed"]) in ref]
    return (len(diffs), max(diffs)) if diffs else None


def describe(values):
    """Trung vị, Q1, Q3, min, max (bỏ None); None nếu không có giá trị."""
    v = np.array([x for x in values if x is not None], dtype=float)
    if len(v) == 0:
        return dict.fromkeys(STATS)
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    return {"median": float(med), "q1": float(q1), "q3": float(q3),
            "min": float(v.min()), "max": float(v.max())}


def scope_values(metrics_list, scope):
    """Lấy thông tin và giá trị chỉ số của một phạm vi (`all` hoặc số đoạn 1..6) qua các seed."""
    if scope == "all":
        m0 = metrics_list[0]
        info = {"row_start": m0["n_warmup"], "row_stop": m0["n_samples"],
                "n_evaluated": m0["n_evaluated"], "n_anomaly": m0["n_anomaly_evaluated"]}
        values = {k: [m[k] for m in metrics_list] for k in METRICS}
        return info, values
    segs = [next(s for s in m["segments"] if s["segment"] == scope) for m in metrics_list]
    info = {k: segs[0][k] for k in ("row_start", "row_stop", "n_evaluated", "n_anomaly")}
    # Mỗi đoạn chỉ ghi tổng thời gian (chấm điểm + học); không tách learn/score theo đoạn.
    values = {"roc_auc": [s["roc_auc"] for s in segs],
              "average_precision": [s["average_precision"] for s in segs],
              "learn_seconds": [None] * len(segs), "score_seconds": [None] * len(segs),
              "total_seconds": [s["seconds"] for s in segs]}
    return info, values


def _row(n_features, model, scope, info, seeds, values):
    """Một dòng bảng tổng hợp: khóa, thông tin phạm vi và thống kê của từng chỉ số."""
    row = {"n_features": n_features, "model": MODELS[model],
           "scope": "all" if scope == "all" else f"segment_{scope}", **info,
           "n_seeds": len(seeds), "seeds": " ".join(map(str, seeds))}
    for metric in METRICS:
        for stat, value in describe(values[metric]).items():
            row[f"{metric}_{stat}"] = value
    return row


def summarize(runs33, fixed10):
    """Tạo các dòng bảng: d = 33 cho toàn luồng và 6 đoạn; d = 10 chỉ toàn luồng.

    `drift-fixed-10.md` chỉ ghi ROC-AUC/AP toàn luồng và không so thời gian, nên các ô thời gian
    và các đoạn của d = 10 để trống. Thông tin dòng (`row_start`, số mẫu, số bất thường) lấy từ
    d = 33 vì hai cấu hình dùng cùng các dòng và nhãn.
    """
    rows = []
    for model in MODELS:
        metrics_list = [m for _, m in runs33[model]]
        seeds = [c["seed"] for c, _ in runs33[model]]
        for scope in ["all", *range(1, len(CHANGE_POINTS) + 2)]:
            info, values = scope_values(metrics_list, scope)
            rows.append(_row(33, model, scope, info, seeds, values))
    info_all, _ = scope_values([m for _, m in runs33["oif"]], "all")
    for model in MODELS:
        runs = fixed10[model]
        values = dict.fromkeys(METRICS, [None] * len(runs))
        values["roc_auc"] = [r[1] for r in runs]
        values["average_precision"] = [r[2] for r in runs]
        rows.append(_row(10, model, "all", info_all, [r[0] for r in runs], values))
    return rows


def write_csv(rows):
    """Ghi bảng tổng hợp; ô trống nghĩa là chỉ số không được ghi cho phạm vi đó."""
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if v is None else v for k, v in row.items()})


def sliding_median(runs, model):
    """Tâm cửa sổ và các phân vị 25/50/75 của ROC-AUC cửa sổ trượt qua các seed."""
    sw = [m["sliding_window"] for _, m in runs[model]]
    centers = np.asarray(sw[0]["row_start"]) + sw[0]["size"] / 2
    auc = np.array([[np.nan if a is None else a for a in s["roc_auc"]] for s in sw], dtype=float)
    q1, med, q3 = np.nanpercentile(auc, [25, 50, 75], axis=0)
    return centers, q1, med, q3, sw[0]


def plot(runs):
    """Vẽ ROC-AUC trung vị theo cửa sổ trượt (d = 33) và 5 mốc thay đổi, kiểu Hình 7."""
    fig, ax = plt.subplots(figsize=(10, 4.6), constrained_layout=True)
    n_seeds = len(runs["oif"])
    for model, name in MODELS.items():
        x, q1, med, q3, sw = sliding_median(runs, model)
        ax.fill_between(x, q1, q3, color=COLORS[model], alpha=0.15, linewidth=0)
        ax.plot(x, med, color=COLORS[model], linewidth=2,
                label=f"{name}: trung vị {n_seeds} seed (vùng nhạt: Q1–Q3)")
    for i, p in enumerate(CHANGE_POINTS):
        ax.axvline(p, color=COLORS["change"], linestyle="--", linewidth=1,
                   label="Mốc thay đổi phân phối" if i == 0 else None)
    ax.set_xlim(0, runs["oif"][0][1]["n_samples"])
    ax.set_ylim(0.4, 1.0)
    size, step = (f"{v:,}".replace(",", ".") for v in (sw["size"], sw["step"]))
    ax.set_xlabel(f"row_index (tâm cửa sổ {size} mẫu, bước {step})")
    ax.set_ylabel("ROC-AUC trên cửa sổ")
    ax.set_title("INSECTS, d = 33: ROC-AUC theo cửa sổ trượt (đánh giá chấm trước, học sau)")
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(colors=COLORS["text"])
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    fig.savefig(FIGURE_PATH, dpi=180)
    plt.close(fig)


def vn(x, digits=3):
    """Định dạng số kiểu Việt Nam (dấu phẩy thập phân); None thành 'không xác định'."""
    return "không xác định" if x is None else f"{x:.{digits}f}".replace(".", ",")


def pick(rows, n_features, model, scope):
    """Tìm dòng tổng hợp theo khóa."""
    return next(r for r in rows if r["n_features"] == n_features and r["model"] == model
                and r["scope"] == scope)


def report(rows, runs33, fixed10):
    """Viết `results/drift.md` từ bảng tổng hợp; nhận xét định lượng được tính từ số liệu."""
    n_seeds = len(runs33["oif"])
    commits = sorted({c["git_commit"][:7] for v in runs33.values() for c, _ in v})
    scopes = ["all", *[f"segment_{k}" for k in range(1, 7)]]
    label = {"all": "Toàn luồng", **{f"segment_{k}": str(k) for k in range(1, 7)}}
    L = []
    add = L.append
    add("# Kết quả thí nghiệm concept drift trên INSECTS\n")
    full = {c["git_commit"] for v in runs33.values() for c, _ in v}
    has_f1 = all(has_commit(F1_FIX, c) for c in full)
    add(f"**Trạng thái:** d = 33 chạy {n_seeds} seed (0–{n_seeds - 1}) tại commit "
        f"`{', '.join(commits)}` ("
        + ("đã có" if has_f1 else "**chưa có hoặc không xác định được**")
        + f" bản sửa F1 `{F1_FIX}`); kết quả thô trong "
        "`results/raw/drift-v2/` (Git bỏ qua), chưa tải lên W&B. d = 10 lấy từ "
        "[`drift-fixed-10.md`](drift-fixed-10.md) (5 seed, cùng `run.py`, sau sửa F1), mỗi run có "
        "link W&B. Bảng đầy đủ ở [`drift-by-segment.csv`](drift-by-segment.csv). Số liệu sinh bởi "
        "[`experiments/exp2_drift/plot_summary.py`](../experiments/exp2_drift/plot_summary.py).\n")
    check = bootstrap_check(runs33)
    if check:
        add(f"Đối chiếu: ROC-AUC toàn luồng của {check[0]} lần chạy d = 33 "
            + ("khớp" if check[1] < 1e-9 else "**không khớp**")
            + " [`drift-after-bootstrap.csv`](drift-after-bootstrap.csv), sai lệch lớn nhất "
            f"{check[1]:.1e}.\n")
    dirty = [f"{c['model']} seed {c['seed']}" for v in runs33.values() for c, _ in v
             if c["git_worktree_dirty"]]
    if dirty:
        add(f"Các lần chạy có `git_worktree_dirty = true` ({'; '.join(dirty)}): lúc chạy, working "
            "tree có thay đổi chưa commit; cần đối chiếu `git_commit` trong `config.json`.\n")

    add("## Giao thức\n")
    add("- Dữ liệu `data/processed/insects.csv` (212.514 mẫu), giữ nguyên thứ tự dòng; không xáo "
        "trộn, không chia tập. Năm mốc thay đổi `51255, 74381, 100944, 142291, 152207` lấy từ script "
        "vẽ Hình 7 của tác giả (xem [`data/README.md`](../data/README.md)), chia luồng thành 6 đoạn.")
    add("- Đánh giá tuần tự **chấm điểm rồi mới học** (score-then-learn), theo lô 100. Lô đầu chỉ "
        "để khởi động; 212.414 mẫu còn lại được đánh giá. Nhãn chỉ dùng để tính chỉ số.")
    add("- OIF: 32 cây, `window_size = 2048`, `eta = 32`, seed rừng `seed * 32` để các seed không "
        "dùng chung cây (điểm F4 của `forest.py`).")
    add("- asdIFOR (nhóm tự dựng): `sklearn.ensemble.IsolationForest` 32 cây, `max_samples = 256`, "
        "huấn luyện lại trên 2048 mẫu gần nhất sau mỗi 2048 mẫu mới, giống ý tưởng cửa sổ rời của "
        "`pysad.IForestASD` mà tác giả dùng nhưng không phải cùng mã.")
    add("- Chỉ số: ROC-AUC, AP trên toàn luồng và từng đoạn; ROC-AUC trên cửa sổ trượt 5.000 mẫu, "
        "bước 1.000 (208 cửa sổ); thời gian học và chấm điểm (giây, CPU laptop, 1 luồng, các "
        "lần chạy d = 33 chạy tuần tự).")
    add("- Tiền xử lý: không có. Dùng nguyên CSV đã chuẩn bị, không chuẩn hóa/scaling, không điền "
        "khuyết, không xáo trộn, không bỏ dòng trùng; lượt d = 10 chỉ lấy 10 cột đầu `x0..x9`.")
    add("- Đo thời gian: `time.perf_counter` (giây, thời gian thực), đo tách riêng phần chấm điểm "
        "và phần học của từng lô rồi cộng dồn; không tính thời gian đọc dữ liệu và ghi tệp (ghi "
        "trong trường `preprocessing` và `timing` của `config.json`).\n")

    add(f"## Kết quả theo đoạn (d = 33, trung vị [Q1; Q3] qua {n_seeds} seed)\n")
    add("| Đoạn | `row_index` | Số mẫu | Bất thường | OIF ROC-AUC | asdIFOR ROC-AUC | OIF AP | "
        "asdIFOR AP | OIF giây | asdIFOR giây |")
    add("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for scope in scopes:
        o, a = pick(rows, 33, "OIF", scope), pick(rows, 33, "asdIFOR", scope)
        add(f"| {label[scope]} | {o['row_start']}–{o['row_stop'] - 1} | {o['n_evaluated']} | "
            f"{vn(100 * o['n_anomaly'] / o['n_evaluated'], 2)}% | "
            f"{vn(o['roc_auc_median'])} [{vn(o['roc_auc_q1'])}; {vn(o['roc_auc_q3'])}] | "
            f"{vn(a['roc_auc_median'])} [{vn(a['roc_auc_q1'])}; {vn(a['roc_auc_q3'])}] | "
            f"{vn(o['average_precision_median'])} | {vn(a['average_precision_median'])} | "
            f"{vn(o['total_seconds_median'], 1)} | {vn(a['total_seconds_median'], 1)} |")
    add("\nThời gian theo đoạn là tổng thời gian chấm điểm và học của các lô bắt đầu trong đoạn. "
        "Mỗi đoạn chỉ ghi tổng này; thời gian học và chấm điểm tách riêng chỉ có ở cấp toàn luồng "
        "(xem CSV).\n")

    add("## ROC-AUC theo cửa sổ trượt\n")
    add("![ROC-AUC theo cửa sổ trượt trên INSECTS](../figures/drift-quality.png)\n")
    add(f"Đường đậm là trung vị qua {n_seeds} seed, vùng nhạt là Q1–Q3; vạch đỏ đứt là 5 mốc thay "
        "đổi. Mỗi điểm đặt ở tâm cửa sổ (`row_start + 2500`), theo mô tả ở Mục 5.3 của bài báo. Đây "
        "là hình do nhóm tạo, không phải hình trích từ bài báo.\n")

    add("## Đối chiếu d = 33 và d = 10 (toàn luồng, 5 seed mỗi cấu hình)\n")
    add("Script của tác giả chỉ dùng 10 đặc trưng đầu (`data[:, :10]`). Số d = 10 lấy từ "
        "[`drift-fixed-10.md`](drift-fixed-10.md); hai cấu hình dùng cùng `run.py`, cùng seed "
        "0–4 và cùng cách cấp seed rừng (`seed * 32`), chỉ khác số cột.\n")
    add("| Mô hình | d = 33: ROC-AUC trung vị [Q1; Q3] | d = 33: min–max | "
        "d = 10: ROC-AUC trung vị [Q1; Q3] | d = 10: min–max | AP trung vị d = 33 | "
        "AP trung vị d = 10 |")
    add("|---|---:|---:|---:|---:|---:|---:|")
    for name in MODELS.values():
        r33, r10 = pick(rows, 33, name, "all"), pick(rows, 10, name, "all")
        add(f"| {name} | " + " | ".join(
            f"{vn(r['roc_auc_median'])} [{vn(r['roc_auc_q1'])}; {vn(r['roc_auc_q3'])}] | "
            f"{vn(r['roc_auc_min'])}–{vn(r['roc_auc_max'])}" for r in (r33, r10))
            + f" | {vn(r33['average_precision_median'])} | "
            f"{vn(r10['average_precision_median'])} |")
    add("\nTheo từng seed (ROC-AUC toàn luồng; link W&B của lượt d = 10):\n")
    add("| Seed | OIF d = 33 | OIF d = 10 | asdIFOR d = 33 | asdIFOR d = 10 | W&B d = 10 |")
    add("|---:|---:|---:|---:|---:|---|")
    by_seed = {model: {c["seed"]: m["roc_auc"] for c, m in runs33[model]} for model in MODELS}
    ten = {model: {s: (auc, url) for s, auc, _, url in fixed10[model]} for model in MODELS}
    seeds = sorted(set(by_seed["oif"]) & set(ten["oif"]))
    for s in seeds:
        add(f"| {s} | {vn(by_seed['oif'][s])} | {vn(ten['oif'][s][0])} | "
            f"{vn(by_seed['asdifor'][s])} | {vn(ten['asdifor'][s][0])} | "
            f"[OIF]({ten['oif'][s][1]}), [asdIFOR]({ten['asdifor'][s][1]}) |")
    verdicts = []
    for model, name in MODELS.items():
        r33, r10 = pick(rows, 33, name, "all"), pick(rows, 10, name, "all")
        higher = sum(ten[model][s][0] > by_seed[model][s] for s in seeds)
        overlap = r10["roc_auc_min"] <= r33["roc_auc_max"] and r33["roc_auc_min"] <= r10["roc_auc_max"]
        verdicts.append(
            f"{name}: d = 10 cao hơn d = 33 ở {higher}/{len(seeds)} seed, khoảng min–max hai "
            "cấu hình " + ("chồng lên nhau" if overlap else "tách rời"))
    add("\n" + "; ".join(verdicts) + ". Khoảng tách rời nghĩa là chênh lệch lớn hơn dao động "
        "theo seed quan sát được; với 5 seed đây vẫn là quan sát, chưa phải kiểm định. Lượt d = 10 "
        "không ghi kết quả theo đoạn và không so thời gian (các run OIF chạy đồng thời); phân tích "
        "phục hồi sau từng mốc của d = 10 nằm ở [`drift-fixed-10.md`](drift-fixed-10.md).\n")

    add("## Nhận xét\n")
    add("**Sụt giảm và phục hồi qua các mốc.** Thay đổi ROC-AUC trung vị từ đoạn trước sang đoạn "
        "sau mỗi mốc (d = 33):\n")
    add("| Mốc | Đoạn | OIF | asdIFOR |")
    add("|---|---|---:|---:|")
    for k, p in enumerate(CHANGE_POINTS, start=1):
        delta = {}
        for name in MODELS.values():
            before = pick(rows, 33, name, f"segment_{k}")["roc_auc_median"]
            after = pick(rows, 33, name, f"segment_{k + 1}")["roc_auc_median"]
            delta[name] = after - before
        add(f"| {p} | {k} → {k + 1} | {vn(delta['OIF'], 3):>6} | {vn(delta['asdIFOR'], 3)} |")
    same_sign = sum(
        np.sign(pick(rows, 33, "OIF", f"segment_{k + 1}")["roc_auc_median"]
                - pick(rows, 33, "OIF", f"segment_{k}")["roc_auc_median"])
        == np.sign(pick(rows, 33, "asdIFOR", f"segment_{k + 1}")["roc_auc_median"]
                   - pick(rows, 33, "asdIFOR", f"segment_{k}")["roc_auc_median"])
        for k in range(1, len(CHANGE_POINTS) + 1))
    lows = {}
    for model, name in MODELS.items():
        x, _, med, _, _ = sliding_median(runs33, model)
        i = int(np.nanargmin(med))
        lows[name] = (vn(float(med[i])), int(x[i]))
    add(f"\nHai mô hình thay đổi cùng chiều ở {same_sign}/{len(CHANGE_POINTS)} mốc, phù hợp với "
        "nhận định ở Mục 5.3 rằng các thuật toán bị ảnh hưởng tương tự bởi thay đổi đột ngột. Trên "
        "đường cửa sổ trượt, "
        f"điểm thấp nhất của OIF là {lows['OIF'][0]} (tâm cửa sổ {lows['OIF'][1]}) và của asdIFOR "
        f"là {lows['asdIFOR'][0]} (tâm {lows['asdIFOR'][1]}). Cả hai đều chỉ nhớ 2048 mẫu gần "
        "nhất, nên sau mỗi mốc cần khoảng một cửa sổ học để thay toàn bộ mẫu cũ; cửa sổ đánh giá "
        "5.000 mẫu làm mượt thêm nên đường cong không đổi tức thời tại vạch đỏ.\n")

    o_all, a_all = pick(rows, 33, "OIF", "all"), pick(rows, 33, "asdIFOR", "all")
    spread = {}
    for name in MODELS.values():
        widest = max(scopes[1:], key=lambda s: pick(rows, 33, name, s)["roc_auc_max"]
                     - pick(rows, 33, name, s)["roc_auc_min"])
        r = pick(rows, 33, name, widest)
        spread[name] = (label[widest], vn(r["roc_auc_min"]), vn(r["roc_auc_max"]))
    add(f"**Phương sai theo seed.** ROC-AUC toàn luồng của OIF nằm trong "
        f"[{vn(o_all['roc_auc_min'])}; {vn(o_all['roc_auc_max'])}] (IQR "
        f"{vn(o_all['roc_auc_q3'] - o_all['roc_auc_q1'])}), của asdIFOR trong "
        f"[{vn(a_all['roc_auc_min'])}; {vn(a_all['roc_auc_max'])}] (IQR "
        f"{vn(a_all['roc_auc_q3'] - a_all['roc_auc_q1'])}). Đoạn dao động mạnh nhất của OIF là "
        f"đoạn {spread['OIF'][0]} ({spread['OIF'][1]}–{spread['OIF'][2]}), của asdIFOR là đoạn "
        f"{spread['asdIFOR'][0]} ({spread['asdIFOR'][1]}–{spread['asdIFOR'][2]}). Giả thuyết (chưa kiểm chứng): OIF "
        "dao động lớn hơn vì cấu trúc cây phụ thuộc chuỗi phép tách ngẫu nhiên tích lũy suốt luồng (mỗi lần tách "
        "còn sinh mẫu ảo), trong khi asdIFOR dựng lại toàn bộ rừng sau mỗi 2048 mẫu. "
        + (f"Với {n_seeds} seed, chênh lệch trung vị toàn luồng giữa hai mô hình "
           f"({vn(abs(o_all['roc_auc_median'] - a_all['roc_auc_median']))}) nhỏ hơn khoảng dao động "
           f"của OIF ({vn(o_all['roc_auc_max'] - o_all['roc_auc_min'])}), nên chưa đủ cơ sở để nói "
           "mô hình nào tốt hơn trên INSECTS.\n"
           if abs(o_all["roc_auc_median"] - a_all["roc_auc_median"])
           < o_all["roc_auc_max"] - o_all["roc_auc_min"] else
           "Chênh lệch trung vị toàn luồng lớn hơn khoảng dao động của OIF.\n"))

    n_eval = o_all["n_evaluated"]
    ratio = o_all["total_seconds_median"] / a_all["total_seconds_median"]
    add(f"**Thời gian: Python thuần so với Cython.** Trung vị tổng thời gian là "
        f"{vn(o_all['total_seconds_median'], 1)} giây với OIF "
        f"(~{vn(1e6 * o_all['total_seconds_median'] / n_eval, 0)} µs/mẫu; học "
        f"{vn(o_all['learn_seconds_median'], 1)} giây, chấm điểm "
        f"{vn(o_all['score_seconds_median'], 1)} giây) và {vn(a_all['total_seconds_median'], 1)} giây "
        f"với asdIFOR, tức OIF chậm hơn khoảng {vn(ratio, 0)} lần. Kết quả này ngược với Mục 5.3 "
        "(oIFOR nhanh nhất) và chủ yếu do cách cài đặt, không phải do độ phức tạp thuật toán:")
    add("- OIF của nhóm viết bằng Python thuần: mỗi mẫu đi qua vòng lặp Python trên 32 cây để học, "
        "và thêm một lần quên khi cửa sổ đầy. Mã của tác giả cũng là Python thuần.")
    refits = runs33["asdifor"][0][1]["n_refits"]
    add("- asdIFOR của nhóm gọi scikit-learn, nơi phần dựng và duyệt cây viết bằng Cython, và chỉ "
        f"huấn luyện lại {refits} lần trên toàn luồng; chấm điểm được vector hóa theo lô 100.")
    add("- Tác giả chạy asdIFOR qua `pysad`, với giao diện xử lý từng mẫu, nên số thời gian trong bài "
        "báo không so trực tiếp được với baseline của nhóm.\n")
    slow = []
    for model, name in MODELS.items():
        times = [(c["seed"], m["total_seconds"]) for c, m in runs33[model]]
        med = float(np.median([t for _, t in times]))
        slow += [f"{name} seed {s}: {vn(t, 1)} giây, gấp {vn(t / med, 0)} lần trung vị"
                 for s, t in times if t > 5 * med]
    if slow:
        add(f"**Thời gian bất thường:** {'; '.join(slow)}. Thời gian thực của lần chạy này bị gián "
            "đoạn (ví dụ máy vào chế độ ngủ); ROC-AUC/AP không bị ảnh hưởng, nhưng chỉ nên dùng "
            "trung vị thời gian, không dùng min/max trong CSV cho mô hình này.\n")

    add("## Khác biệt so với bài báo và mã tác giả\n")
    add("- Bài báo chạy 30 lần; nhóm chạy 5 seed cho mỗi cấu hình d = 33 và d = 10.")
    add("- Mã tác giả học mỗi lô trước khi chấm điểm lô đó, nên điểm của một mẫu đã dùng chính mẫu "
        "đó; nhóm chấm điểm trước khi học. Mã tác giả cũng có thêm holdout ngẫu nhiên 10%, nhóm "
        "không dùng.")
    add("- Mã tác giả chỉ dùng 10 đặc trưng; bài báo ghi d = 33. Bảng theo đoạn và hình ở đây "
        "dùng d = 33; kết quả d = 10 (có W&B) ở [`drift-fixed-10.md`](drift-fixed-10.md).")
    add("- Hình của nhóm dùng bước cửa sổ 1.000 và đặt điểm ở tâm cửa sổ; script vẽ của tác giả "
        "dùng bước 10 và co giãn chỉ số đầu cửa sổ theo độ dài luồng.")
    add("- Không chép số liệu bài báo; Hình 7 không có bảng số nên chỉ so được về hình dạng.\n")

    add("## Tệp kết quả\n")
    add("- `results/raw/drift-v2/<model>_seed<s>/` (d = 33): `config.json`, `metrics.json`, "
        "`predictions.csv` (cột `row_index, segment, label, anomaly_score`).")
    add("- [`drift-by-segment.csv`](drift-by-segment.csv): trung vị, Q1, Q3, min, max của ROC-AUC, "
        "AP, `learn_seconds`, `score_seconds`, `total_seconds` theo `n_features`, mô hình và phạm vi "
        "(`all`, `segment_1`…`segment_6`; d = 10 chỉ có `all`). Ô trống là chỉ số không được ghi "
        "cho phạm vi đó.")
    add("- [`../figures/drift-quality.png`](../figures/drift-quality.png).\n")

    add("## Tải kết quả d = 33 lên W&B\n")
    add("Lượt d = 10 đã có link W&B (xem [`docs/wandb-runs.md`](../docs/wandb-runs.md)). Lượt "
        "d = 33 chưa tải. Cần cài phần phụ thuộc W&B (`python -m pip install -e .[wandb]`), đăng "
        "nhập (`wandb login`) và đặt `WANDB_PROJECT`/`WANDB_ENTITY`; không đưa khóa API vào Git. "
        "Dùng script tải của nhóm, không chạy lại mô hình:\n")
    add("```powershell")
    add("python experiments/exp2_drift/upload_runs.py results/raw/drift-v2 "
        "--manifest results/raw/drift-v2/wandb-links.json")
    add("```\n")
    add("Script ghi URL từng run vào manifest; sau đó bổ sung các URL vào mục Trạng thái và "
        "`docs/wandb-runs.md`.")
    REPORT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    """Đọc kết quả thô và ghi bảng CSV, hình PNG, báo cáo Markdown."""
    runs33 = load_runs(RUN_DIR_33) if RUN_DIR_33.is_dir() else {}
    if set(runs33) != set(MODELS):
        raise FileNotFoundError("Run experiments/exp2_drift/run.py --output results/raw/drift-v2 first")
    if any(c["n_features"] != 33 for v in runs33.values() for c, _ in v):
        raise ValueError(f"{RUN_DIR_33} must contain d = 33 runs only")
    fixed10 = load_fixed10()
    rows = summarize(runs33, fixed10)
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_csv(rows)
    plot(runs33)
    report(rows, runs33, fixed10)
    for path in (CSV_PATH, FIGURE_PATH, REPORT_PATH):
        print(f"{path.relative_to(ROOT).as_posix()}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
