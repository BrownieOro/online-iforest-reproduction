# Nhận và upload kết quả đã chạy

Phần Trân phụ trách. Không cần chạy lại mô hình chỉ để đưa raw lên W&B.
Trạng thái mốc21/11: stationary-f4 chưa có link; drift33 và sweep chưa có link;
drift10 đã có10link trong [danh mục](wandb-runs.md). Chỉ cập nhật trạng thái
sau khi upload thật và đọc lại đúng run/artifact.

## 1. Nhận đúng bộ kết quả

| Bộ | Cấu trúc dự kiến | Số run |
|---|---|---:|
| Stationary | stationary-f4/dataset/model/seed-n/ | 120 |
| Drift33 | thư mục bản cuối, bên trong oif_seed0..4/asdifor_seed0..4 | 10 |
| Sweep10 | window-sweep-10/omega-size/oif_seed0/ | 4 |

Mỗi run phải có config.json, metrics.json, predictions.csv. Stationary thêm
runs.csv ở gốc. Sweep gồm window256/512/2048/8192, seed0, d=10.
Drift33 có tên raw khác nhau giữa hai báo cáo; yêu cầu Thi xác nhận bản cuối
khớp bảng trước khi upload. Giữ ZIP gốc và config/metrics nguyên trạng.

Kiểm tra dataset, model, seed, số đặc trưng, window_size, commit, protocol và
thứ tự học/chấm trong config. Kiểm số dòng dự đoán, ROC-AUC/AP và thống kê theo
seed với bảng báo cáo. Thiếu file hoặc sai bộ thì giữ trạng thái chờ, không
dùng một run tương tự thay thế.

## 2. Thiết lập trên máy người upload

Từ thư mục repo, cài gói:

```bash
python -m pip install -e ".[wandb]"
wandb login
```

Dùng tài khoản và cấu hình project chung đang có. Trong .env đã được Git bỏ qua,
đặt WANDB_MODE=online, WANDB_PROJECT=intro-ml-oif và WANDB_ENTITY đúng workspace
của nhóm; không suy tên entity từ tên người đăng nhập. Giữ nguyên cấu hình host
nếu môi trường hiện tại đã dùng host riêng. Không gửi API key trong ZIP/repo/chat.

## 3. Stationary: dùng uploader Phúc đã có

```bash
python experiments/exp1_stationary/log_runs.py --runs-dir results/raw/stationary-f4
```

Uploader đọc .env, kiểm ba file, lưu URL sau mỗi run vào
results/stationary-wandb-links.csv và cập nhật trạng thái trong báo cáo/nháp slide
Phúc. Dùng lại manifest khi tiếp tục cùng bộ run để tránh upload trùng.
Không dùng manifest của một lượt cũ cho lượt mới có cùng dataset/model/seed.

Sau đó bổ sung bảng link stationary vào docs/wandb-runs.md và phần Trân.
Uploader hiện không tự thêm biểu đồ tổng hợp vào artifact; cần log/đính kèm hình
stationary-auc.png và stationary-time.png phù hợp sau khi kiểm raw.

## 4. Drift33: dùng uploader drift

Script drift hiện đọc biến môi trường trực tiếp, không tự load .env. Có thể
nạp .env rồi chạy bằng lệnh dưới; thay raw path theo thư mục Thi xác nhận:

```bash
python -c "import sys,runpy; from dotenv import load_dotenv; load_dotenv(); sys.argv=['upload_runs.py','results/raw/drift-v2','--manifest','results/drift33-wandb-links.json']; runpy.run_path('experiments/exp2_drift/upload_runs.py',run_name='__main__')"
```

Script gửi scalars, đường ROC-AUC trượt và ba file vào artifact. Manifest lưu
theo tên oif_seedN/asdifor_seedN, nên drift33 phải có manifest riêng với drift10.
Không dùng cùng manifest cho dataset/số cột/window khác.

## 5. Sweep: một manifest cho mỗi window

Dùng cùng lệnh drift, nhưng thay run_dir và manifest cho từng cấu hình:

| run_dir | manifest |
|---|---|
| results/raw/window-sweep-10/omega-256 | results/window-256-wandb-links.json |
| results/raw/window-sweep-10/omega-512 | results/window-512-wandb-links.json |
| results/raw/window-sweep-10/omega-2048 | results/window-2048-wandb-links.json |
| results/raw/window-sweep-10/omega-8192 | results/window-8192-wandb-links.json |

Không dùng một manifest chung: cả bốn thư mục đều có thể mang tên oif_seed0,
uploader sẽ coi các cấu hình sau là đã upload rồi và bỏ qua.

## 6. Xác nhận và gắn link

Mở từng URL, kiểm dataset/model/seed/d/window/protocol, scalars và ba file
artifact. Các biểu đồ/số liệu trên slide phải truy được tới đúng các run tạo ra
chúng. Bảng median30seed nên dẫn tới manifest đủ30run của hàng đó, không chỉ
một run đại diện.

Không dùng các link holdout seed42 làm link stationary30seed. Không dùng run
drift sơ bộ dqkrvfhm cho số cuối, hoặc link drift10 cho drift33/sweep.
Giữ manifest trong repo; không cần commit toàn bộ raw hay dataset.

Trước khi nhận ZIP, tài liệu này chỉ chuẩn bị thao tác; không chứng minh đã
upload hoặc đã xác minh raw. Xem [bàn giao Trân](ban-giao-tran.md) để chốt việc còn chờ.
