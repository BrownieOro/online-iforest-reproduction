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
- Seed rừng OIF bằng seed thí nghiệm. Cây thứ `i` nhận seed
  `seed_rừng × n_trees + i`; cấu hình từng lượt lưu seed xáo trộn, seed
  baseline, seed rừng và seed của từng cây.

Đây là protocol theo luồng do nhóm thiết kế, không phải tái tạo nguyên trạng
protocol stationary trong bài báo. Bài báo xáo trộn và xử lý toàn bộ luồng theo
lô 100, đồng thời so sánh năm phương pháp trực tuyến. Nhóm dùng phần khởi động
30% và baseline ngoại tuyến cố định để so sánh hai cách làm hiện có. Khi bàn về
Bảng 4 của bài báo, cần nêu rõ khác biệt này.

## Chạy thí nghiệm

Từ thư mục gốc của repo:

```powershell
python scripts/prepare_dataset.py
python experiments/exp1_stationary/run.py --output results/raw/stationary-seedsequence
python experiments/exp1_stationary/plot_summary.py --runs results/raw/stationary-seedsequence/runs.csv
```

`--output` phải trỏ tới thư mục chưa chứa các run đó; dùng một thư mục tên mới
khi chạy lại để không ghi đè artifacts cũ.

Mỗi bộ dữ liệu, mô hình và seed có thư mục riêng dưới đường dẫn `--output`, ví dụ
`results/raw/stationary-seedsequence/<dataset>/<model>/seed-<n>/`. Mỗi thư mục chứa
`config.json`, `metrics.json` và `predictions.csv` với các cột
`row_index, stream_index, anomaly_score, label`. Cấu hình ghi commit Git, trạng
thái worktree, tham số, phiên bản thư viện, tiền xử lý, thứ tự đánh giá và cách
đo thời gian; metrics dùng đơn vị giây cho thời gian. Script cũng tạo `runs.csv`
và `results/stationary-summary.csv` để tổng hợp hai phương pháp theo seed (có thể
đổi bằng `--summary-output`).
`plot_summary.py` tạo hai biểu đồ median kèm khoảng tứ phân vị Q1–Q3 từ `runs.csv`;
biểu đồ thời gian dùng trục log để thể hiện rõ cả hai phương pháp. Git bỏ qua dữ
liệu đã chuẩn bị và kết quả thô; giữ lại thư mục này khi cần kiểm tra các lần chạy.

## Tải các lần chạy lên W&B

Các kết quả cục bộ có thể tải lên mà không chạy lại mô hình. Cài phần phụ thuộc,
sao chép `.env.example` thành `.env`, đặt `WANDB_MODE=online` và project cần dùng;
nếu project thuộc team, đặt thêm `WANDB_ENTITY`. Sau đó đăng nhập cục bộ bằng
`wandb login` (hoặc lưu `WANDB_API_KEY` trong `.env`, được Git bỏ qua):

```powershell
python -m pip install -e ".[wandb]"
wandb login
python experiments/exp1_stationary/log_runs.py --runs-dir results/raw/stationary-seedsequence
```

Mỗi bộ `(dataset, model, seed)` trở thành một W&B run riêng, có tag
`reproduction` và `stationary`. Script không chạy lại mô hình; sau mỗi lần tải
thành công, lưu URL vào `results/stationary-wandb-links.csv` và cập nhật số run,
link project và manifest trong `results/stationary.md` cùng `slides/phase2-phuc.md`.
Nếu chạy tiếp sau khi bị gián đoạn, các bộ đã có trong manifest sẽ được bỏ qua.
Không đưa khóa API vào Git.

## Mốc tham khảo từ bài báo

Bài báo báo cáo ROC-AUC trung vị của oIFOR là 0,854 trên Mammography và 0,685
trên Annthyroid (Bảng 4). Đây là số tham khảo, không so trực tiếp được với
protocol của nhóm hoặc baseline scikit-learn. Xem
[`results/stationary.md`](../../results/stationary.md) để biết kết quả và các
giới hạn khi diễn giải.
