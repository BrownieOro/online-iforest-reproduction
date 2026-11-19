# Phân tích bổ sung - Kích thước cửa sổ

Đây là thí nghiệm bổ sung của nhóm, không phải tái tạo nguyên xi bài báo. Chỉ đổi
`window_size` của OIF; các tham số khác giữ nguyên. Dùng 10 đặc trưng đầu INSECTS,
đúng như script thực nghiệm của nhóm gốc. Bảng dữ liệu trong bài báo mô tả 33 đặc
trưng, nên đây là đối chiếu theo script, không phải theo mô tả bảng dữ liệu.

## Protocol

- Đủ 212.514 dòng INSECTS, giữ nguyên thứ tự thời gian, không xáo trộn.
- Prequential theo lô 100: chấm điểm trước khi học lô; lô đầu làm warm-up.
- 32 cây, `eta=32`, một seed (`seed=0`); lần lượt thử cửa sổ 256, 512, 2048,
  8192. Dùng ROC-AUC/AP toàn luồng và các cửa sổ đánh giá 5.000 mẫu, bước 1.000.
- Đây là sweep ban đầu một seed; chưa đủ để chọn cửa sổ tốt nhất.

## Chạy lại

Từ thư mục gốc repo trong PowerShell:

```powershell
$env:PYTHONPATH = 'src'
$env:WANDB_MODE = 'disabled'
foreach ($omega in @(256, 512, 2048, 8192)) {
  python experiments/exp2_drift/run.py --models oif --seeds 0 --n-features 10 `
    --window-size $omega --output ("results/raw/window-sweep-10/omega-" + $omega)
}
```

Mỗi cấu hình lưu `config.json`, `metrics.json`, `predictions.csv` tại
`results/raw/window-sweep-10/omega-<size>/oif_seed0/`. W&B được tắt; chưa có URL
W&B.

## Kết quả

Mỗi dòng là seed 0, 10 đặc trưng đầu, 212.414 mẫu được chấm. Thời gian là tổng
chấm điểm và cập nhật OIF trên môi trường này.

| `window_size` | ROC-AUC | AP | Thời gian (giây) |
|---:|---:|---:|---:|
| 256 | 0,665 | 0,103 | 798,3 |
| 512 | 0,679 | 0,109 | 703,9 |
| 2048 | 0,691 | 0,109 | 987,4 |
| 8192 | 0,716 | 0,112 | 798,9 |

ROC-AUC tăng theo bốn mức trong seed này, nhưng một seed chưa đủ để chọn cấu hình
tốt nhất. Thời gian chạy cũng dao động theo mức cửa sổ và tải máy. Bảng CSV đầy
đủ ở [`results/window-sweep-10.csv`](../../results/window-sweep-10.csv). Tạo
biểu đồ bằng `python experiments/exp3_window/plot.py`:
[`figures/window-sweep-10.png`](../../figures/window-sweep-10.png).
