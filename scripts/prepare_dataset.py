from pathlib import Path
from urllib.request import urlopen
import hashlib
import json

import numpy as np
import pandas as pd


# Tính đường dẫn từ vị trí script
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

BASE_URL = (
    "https://media.githubusercontent.com/media/"
    "ineveLoppiliF/Online-Isolation-Forest/main/"
    "datasets/stationary/ifor"
)

# SHA-256 lấy từ các tệp Git LFS của tác giả đã kiểm tra.
DATASETS = {
    "annthyroid": {
        "filename": "Annthyroid.csv",
        "sha256": (
            "8a890d0e7bef159585385774909a7390d4"
            "7e15c7742dde25d6cf0d2ec944bc98"
        ),
    },
    "mammography": {
        "filename": "Mammography.csv",
        "sha256": (
            "66fcdb2f70fccd8e31553d49bc5240411"
            "b0442882c6ada44163f69437fd1b156"
        ),
    },
}


def prepare_dataset(name, info):
    url = f"{BASE_URL}/{info['filename']}"
    raw_path = RAW_DIR / info["filename"]

    # Tải lần đầu; các lần chạy sau đọc bản gốc đã lưu.
    if not raw_path.exists():
        print(f"Downloading {info['filename']}...")
        with urlopen(url, timeout=120) as response:
            content = response.read()

        if content.startswith(b"version https://git-lfs.github.com"):
            raise ValueError("Đã tải nhầm tệp trỏ Git LFS.")

        if hashlib.sha256(content).hexdigest() != info["sha256"]:
            raise ValueError(
                "Nội dung nguồn khác bản đã xác minh. "
                "Cần kiểm tra phiên bản trước khi tiếp tục."
            )

        raw_path.write_bytes(content)

    content = raw_path.read_bytes()
    source_hash = hashlib.sha256(content).hexdigest()
    if source_hash != info["sha256"]:
        raise ValueError(f"Bản gốc {raw_path.name} không đúng checksum.")

    df = pd.read_csv(raw_path)

    features = [f"x{i}" for i in range(6)]
    expected_columns = ["id", *features, "y"]
    if list(df.columns) != expected_columns:
        raise ValueError(f"Cấu trúc cột không đúng: {list(df.columns)}")

    # Chỉ lấy đặc trưng và nhãn; bỏ ID.
    output = df[features + ["y"]].copy()
    output = output.rename(columns={"y": "label"})

    # Chuyển sang số; báo lỗi nếu gặp nội dung không hợp lệ.
    output = output.apply(pd.to_numeric, errors="raise")

    if not np.isfinite(output.to_numpy(dtype=float)).all():
        raise ValueError(f"{name}: có dữ liệu thiếu hoặc vô hạn.")

    if set(output["label"].unique()) != {0, 1}:
        raise ValueError(f"{name}: nhãn phải có hai giá trị 0 và 1.")

    output["label"] = output["label"].astype(int)

    output_path = PROCESSED_DIR / f"{name}.csv"
    output.to_csv(output_path, index=False)

    n = len(output)
    n_anomaly = int(output["label"].sum())

    return {
        "dataset": name,
        "source_url": url,
        "source_sha256": source_hash,
        "n_samples": n,
        "n_features": len(features),
        "n_normal": n - n_anomaly,
        "n_anomaly": n_anomaly,
        "anomaly_ratio": n_anomaly / n,
        "missing_values": int(output.isna().sum().sum()),
        # Chỉ đếm để báo cáo, không xóa dòng trùng.
        "duplicate_rows_without_id": int(output.duplicated().sum()),
        "processing": [
            "Drop id",
            "Rename y to label",
            "Preserve feature values and row order",
            "No scaling, shuffling, splitting or deduplication",
        ],
    }


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    summaries = []
    for name, info in DATASETS.items():
        summary = prepare_dataset(name, info)
        summaries.append(summary)
        print(
            f"{name}: {summary['n_samples']} samples, "
            f"{summary['n_features']} features, "
            f"{summary['n_anomaly']} anomalies "
            f"({summary['anomaly_ratio']:.2%})"
        )

    summary_path = PROCESSED_DIR / "stationary-summary.json"
    summary_path.write_text(
        json.dumps(summaries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print("Dataset preparation complete.")


if __name__ == "__main__":
    main()
