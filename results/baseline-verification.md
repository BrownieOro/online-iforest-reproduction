# Kết quả kiểm tra baseline — 2026-11-01

Môi trường thực chạy: Python 3.11.9, numpy 2.4.6, pandas 3.0.3, sklearn 1.9.0.
Khai báo hỗ trợ Python >=3.9; chưa chạy trực tiếp trên Python 3.9 hoặc Linux.

- `python -m pytest -q --basetemp results/raw/pytest-verified-01`: 6 passed.
- Lệnh pytest mặc định ban đầu lỗi quyền ở thư mục temp Windows, trước khi chạy test.
  Có thể dùng `--basetemp results/raw/pytest-<ten-moi>` khi gặp lỗi này;
  luôn chọn thư mục mới vì pytest có thể dọn nội dung basetemp.
- Synthetic: `python scripts/run_baseline.py --output results/raw/verified-smoke-42`.
- CSV: `python -m oif.baseline --data results/raw/verified-input.csv --label-column label --output results/raw/verified-csv-42`.
  CSV kiểm tra được sinh bằng RNG seed 7: 180 normal Gaussian, 20 anomaly uniform [6,9], 3 chiều.
- W&B disabled và offline contract được test bằng mock; chưa chạy SDK offline thật/online upload.
- Không commit/push; không xóa file hiện hữu. Repo sạch trước khi bắt đầu.

| Run | Train/test | ROC-AUC | AP | Precision | Recall | F1 | Fit (s) | Score + predict (s) |
|---|---|---|---|---|---|---|---|---|
| verified-smoke-42 | 700/300 | 1.0000 | 1.0000 | 1.0000 | 0.9667 | 0.9831 | 0.2060 | 0.0220 |
| verified-csv-42 | 140/60 | 1.0000 | 1.0000 | 0.8571 | 1.0000 | 0.9231 | 0.1493 | 0.0183 |

Đây là dữ liệu synthetic dễ phân biệt, chỉ xác nhận pipeline hoạt động. Không phải kết quả dataset paper/OIF. File local nằm trong results/raw (gitignored).

## Kiểm tra W&B bằng SDK thật

- W&B 0.31.0, chạy bằng Python trong `.venv`.
- Đã chạy baseline ở chế độ offline, run ID `gzpddfj5`.
- Đã ghi config, 9 metrics và artifact chứa config.json, metrics.json, predictions.csv.
- Kết quả local: `results/raw/wandb-offline-verified-01/`.
- Log W&B: `wandb/offline-run-20261101_173226-gzpddfj5/`.
- Chưa đồng bộ online vì máy chưa có xác thực W&B.
- `.env` local đã đặt WANDB_MODE=offline; không đưa vào Git.
