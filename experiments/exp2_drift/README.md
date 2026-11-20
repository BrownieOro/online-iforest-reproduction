# Thí nghiệm chính 2 - Dữ liệu thay đổi theo thời gian

Đánh giá OIF trên INSECTS (Mục 5.1–5.2, Hình 7 của bài báo) theo thứ tự thời gian gốc, so với baseline kiểu asdIFOR. Phân biệt cửa sổ học (`window_size = 2048`, phần mô hình nhớ) với cửa sổ đánh giá (5000 mẫu, chỉ dùng để tính chỉ số).

## Protocol

- Dữ liệu: `data/processed/insects.csv` (tạo bằng `python scripts/prepare_insects.py`), giữ nguyên thứ tự dòng, không xáo trộn, không chia tập ngẫu nhiên.
- Prequential theo lô 100: chấm điểm lô trước, rồi mới cho mô hình học lô đó. Lô đầu chỉ để khởi động, không đánh giá.
- Mô hình:
  - `oif`: `OnlineIsolationForest` của nhóm, 32 cây, `window_size = 2048`, `eta = 32`. Truyền seed thí nghiệm vào forest; cây thứ `i` nhận seed `seed * n_trees + i`, nên các lượt dùng các dải seed không giao nhau.
  - `asdifor`: `IsolationForest` của scikit-learn (32 cây, `max_samples = 256`), huấn luyện lại trên 2048 mẫu gần nhất sau mỗi 2048 mẫu mới; trước khi đủ 2048 mẫu thì huấn luyện lại sau mỗi lô. Baseline do nhóm dựng, không phải `pysad.IForestASD` mà tác giả dùng.
- Chỉ số trong `metrics.json`:
  - ROC-AUC và AP trên toàn luồng;
  - ROC-AUC, AP và thời gian của từng đoạn, với các đoạn tách bởi 5 mốc thay đổi ở [`data/README.md`](../../data/README.md);
  - ROC-AUC và AP trên cửa sổ trượt 5000 mẫu, bước 1000;
  - thời gian học và thời gian chấm điểm.
- Mặc định dùng đủ 33 đặc trưng như Mục 5.1. Script của tác giả chỉ dùng 10 đặc trưng đầu; muốn so sát với cách đó thì chạy với `--n-features 10`.

## Chạy

Từ thư mục gốc repo:

```powershell
$env:PYTHONPATH = "src"
python experiments/exp2_drift/run.py --seeds 0 1 2 3 4
# Smoke test: python experiments/exp2_drift/run.py --n-samples 10000 --seeds 0 --output <thư mục tạm>
```

Mỗi cặp `(model, seed)` được ghi vào `results/raw/drift/<model>_seed<seed>/`, gồm `config.json`, `metrics.json` và `predictions.csv` (các cột `row_index, segment, label, anomaly_score`). Script không ghi đè thư mục đã có. Log W&B bật bằng `WANDB_MODE`, giống thí nghiệm 1.

## Khác với script của tác giả

`experiments/scripts/test/test_kqt_datasets.py` (commit `e528c86`) khác script này ở ba điểm:

- học mỗi lô trước khi chấm điểm lô đó;
- chỉ dùng 10 đặc trưng đầu;
- có thêm một tập holdout 10% chọn ngẫu nhiên.

Script này chấm điểm trước khi học, dùng đủ 33 đặc trưng và không có holdout ngẫu nhiên, theo quy định đánh giá tuần tự của nhóm.
