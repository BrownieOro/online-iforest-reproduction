# So sánh trên luồng dữ liệu ổn định

Thí nghiệm so sánh `OnlineIsolationForest` của nhóm với mô hình
`IsolationForest` ngoại tuyến của scikit-learn trên Annthyroid và Mammography.
Mỗi seed tạo một thứ tự dữ liệu xáo trộn dùng chung cho cả hai phương pháp.

## Cách chạy

- Chạy 30 lần với seed từ 0 đến 29; mỗi seed tạo một thứ tự xáo trộn riêng.
- Dùng 30% dòng đầu làm phần khởi động cho cả hai phương pháp.
- Chấm các dòng còn lại theo lô 100. OIF chấm từng lô rồi mới học lô đó; cửa
  sổ có kích thước 2048, gồm 32 cây với `eta=32`.
- Huấn luyện Isolation Forest của scikit-learn một lần trên phần khởi động,
  dùng 100 cây và cùng seed, sau đó giữ mô hình cố định.
- Báo cáo ROC-AUC, average precision (AP), thời gian huấn luyện/cập nhật/chấm
  điểm và trung vị qua 30 lần chạy. Mô hình chỉ nhận các cột đặc trưng đã chuẩn
  bị; không nhận nhãn.

Đây là protocol theo luồng do nhóm thiết kế, không phải tái tạo nguyên trạng
protocol stationary trong bài báo. Bài báo xáo trộn và xử lý toàn bộ luồng theo
lô 100, đồng thời so sánh năm phương pháp trực tuyến. Nhóm dùng phần khởi động
30% và baseline ngoại tuyến cố định để so sánh hai cách làm hiện có. Khi bàn về
Bảng 4 của bài báo, cần nêu rõ khác biệt này.

## Chạy thí nghiệm

Từ thư mục gốc của repo:

```powershell
python scripts/prepare_dataset.py
python experiments/exp1_stationary/run.py
```

Mỗi bộ dữ liệu và seed có một thư mục trong `results/raw/stationary/`, gồm
`config.json`, `metrics.json` và `predictions.csv`. Script cũng tạo `runs.csv`
và `results/stationary-summary.csv`. Git bỏ qua dữ liệu đã chuẩn bị và kết quả
thô; giữ lại thư mục này khi cần kiểm tra các lần chạy.

## Tải các lần chạy lên W&B

W&B là tùy chọn khi chạy cục bộ. Để tải các kết quả đã có lên mà không chạy lại
mô hình, cần cài phần phụ thuộc W&B, đăng nhập và cấu hình project/entity trong
`.env`; sau đó đặt `WANDB_MODE=online` và chạy:

```powershell
python experiments/exp1_stationary/log_runs.py
```

Mỗi lần chạy sẽ thành một W&B run riêng, có tag `reproduction` và `stationary`.
Không đưa khóa API vào Git. Hiện môi trường chưa có cấu hình W&B nên chưa tạo
được đường dẫn run trực tuyến.

## Mốc tham khảo từ bài báo

Bài báo báo cáo ROC-AUC trung vị của oIFOR là 0,854 trên Mammography và 0,685
trên Annthyroid (Bảng 4). Đây là số tham khảo, không so trực tiếp được với
protocol của nhóm hoặc baseline scikit-learn. Xem
[`results/stationary.md`](../../results/stationary.md) để biết kết quả và các
giới hạn khi diễn giải.
