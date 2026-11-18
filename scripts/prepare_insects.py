"""Chuẩn bị bộ dữ liệu không dừng INSECTS từ repository của tác giả (Contract C1).

Nguồn là tệp CSV tác giả đã lọc sẵn 3 lớp: `ae-aegypti-female`, `cx-quinq-male`
(nhãn 0) và `ae-albopictus-male` (nhãn 1). Tệp nguồn chỉ còn cột `y` (0/1), không còn
tên lớp, nên script kiểm chứng việc lọc lớp qua số mẫu và tỷ lệ bất thường ở Mục 5.1
của bài báo. Giữ nguyên thứ tự dòng (thứ tự thời gian); không chuẩn hóa, xáo trộn,
chia tập hay xóa dòng trùng.
"""
from pathlib import Path
from urllib.request import urlopen
import csv
import hashlib
import json

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

COMMIT = "e528c86b77219791d026d732f618efb0c7bde3c1"
FILENAME = "insects_ae-aegypti-female_cx-quinq-male_ae-albopictus-male.csv"
URL = (
    "https://media.githubusercontent.com/media/ineveLoppiliF/Online-Isolation-Forest/"
    f"{COMMIT}/datasets/non-stationary/kqt/{FILENAME}"
)
SHA256 = "c38d9b89fb6b133db5b9fe4249621b056f18f177f5832cc8b1d66a840e4eb5d3"

N_FEATURES = 33
FEATURES = [f"x{i}" for i in range(N_FEATURES)]
EXPECTED_COLUMNS = ["id", *FEATURES, "y"]

# Mục 5.1 của bài báo: n = 212514 điểm, d = 33, 5.50% bất thường.
PAPER_N_SAMPLES = 212514
PAPER_ANOMALY_PERCENT = 5.50


def sha256_of(path):
    """Tính SHA-256 của tệp theo từng khối để không nạp cả tệp vào bộ nhớ."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def download_raw(raw_path):
    """Tải tệp nguồn nếu chưa có; từ chối Git LFS pointer và checksum sai."""
    if raw_path.exists():
        return
    print(f"Downloading {FILENAME}...")
    with urlopen(URL, timeout=600) as response:
        content = response.read()
    if content.startswith(b"version https://git-lfs.github.com"):
        raise ValueError("Downloaded a Git LFS pointer instead of the data file.")
    if hashlib.sha256(content).hexdigest() != SHA256:
        raise ValueError("Downloaded content does not match the verified SHA-256.")
    raw_path.write_bytes(content)


def load_raw(raw_path):
    """Đọc CSV nguồn; kiểm tra cột, thứ tự id, giá trị hữu hạn và nhãn 0/1.

    Trả về X (n, 33) kiểu float và y (n,) kiểu int, giữ nguyên thứ tự dòng.
    """
    with raw_path.open(encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != EXPECTED_COLUMNS:
        raise ValueError(f"Unexpected columns: {header[:3]} ... {header[-3:]}")

    try:
        data = np.loadtxt(raw_path, delimiter=",", skiprows=1, dtype=float, ndmin=2)
    except ValueError as error:
        raise ValueError(f"Non-numeric or missing value in source: {error}") from error
    if data.shape[1] != len(EXPECTED_COLUMNS):
        raise ValueError(f"Unexpected number of columns: {data.shape[1]}")
    if not np.isfinite(data).all():
        raise ValueError("Source contains NaN or infinite values.")

    ids = data[:, 0]
    if not np.array_equal(ids, np.arange(len(data))):
        raise ValueError("Column id is not 0..n-1 in order; row order cannot be verified.")

    labels = data[:, -1]
    if not np.isin(labels, [0.0, 1.0]).all() or set(np.unique(labels)) != {0.0, 1.0}:
        raise ValueError("Labels must contain exactly the values 0 and 1.")
    return data[:, 1:-1], labels.astype(int)


def check_against_paper(X, y):
    """Dừng nếu số mẫu, số đặc trưng hoặc tỷ lệ bất thường lệch Mục 5.1.

    Bài báo ghi tỷ lệ với 2 chữ số thập phân (5.50%); tệp nguồn cho 11701/212514 = 5.506%,
    khớp nếu bài báo cắt bớt chữ số. Vì vậy chấp nhận sai lệch dưới 0.01 điểm phần trăm.
    """
    percent = 100.0 * y.mean()
    if len(X) != PAPER_N_SAMPLES or X.shape[1] != N_FEATURES:
        raise ValueError(f"Shape {X.shape} differs from paper ({PAPER_N_SAMPLES}, {N_FEATURES}).")
    if abs(percent - PAPER_ANOMALY_PERCENT) >= 0.01:
        raise ValueError(f"Anomaly rate {percent:.4f}% differs from paper {PAPER_ANOMALY_PERCENT}%.")


def write_processed(X, y, out_path):
    """Ghi 33 cột đặc trưng + cột label ở cuối, theo đúng thứ tự dòng nguồn."""
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([*FEATURES, "label"])
        for features, label in zip(X.tolist(), y.tolist()):
            writer.writerow([*features, label])


def main():
    """Tải, kiểm chứng, ghi `data/processed/insects.csv` và `insects-summary.json`."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / FILENAME

    download_raw(raw_path)
    source_hash = sha256_of(raw_path)
    if source_hash != SHA256:
        raise ValueError(f"Raw file {raw_path.name} does not match the verified SHA-256.")

    X, y = load_raw(raw_path)
    check_against_paper(X, y)

    out_path = PROCESSED_DIR / "insects.csv"
    write_processed(X, y, out_path)

    n, n_anomaly = len(y), int(y.sum())
    rows = np.column_stack([X, y])
    summary = {
        "dataset": "insects",
        "source_url": URL,
        "source_commit": COMMIT,
        "source_sha256": source_hash,
        "n_samples": n,
        "n_features": X.shape[1],
        "n_normal": n - n_anomaly,
        "n_anomaly": n_anomaly,
        "anomaly_ratio": n_anomaly / n,
        "label_mapping": {
            "0": ["ae-aegypti-female", "cx-quinq-male"],
            "1": ["ae-albopictus-male"],
            "note": "Applied by the source file; it contains only y in {0, 1}, no class names.",
        },
        "first_anomaly_row": int(np.argmax(y == 1)),
        "missing_values": 0,
        # Chỉ đếm để báo cáo, không xóa dòng trùng.
        "duplicate_rows_without_id": int(n - len(np.unique(rows, axis=0))),
        "processing": [
            "Verify columns id,x0..x32,y and id == 0..n-1 (source row order)",
            "Drop id",
            "Rename y to label",
            "Preserve feature values and row order",
            "No scaling, shuffling, splitting or deduplication",
        ],
    }
    (PROCESSED_DIR / "insects-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        f"insects: {n} samples, {X.shape[1]} features, "
        f"{n_anomaly} anomalies ({n_anomaly / n:.2%})"
    )
    print("Dataset preparation complete.")


if __name__ == "__main__":
    main()
