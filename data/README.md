# Dataset

Thư mục này chứa dữ liệu đầu vào và dữ liệu đã chuẩn bị cho các thí nghiệm. Các tệp dữ liệu được tạo khi chạy script và được Git bỏ qua; script cùng hướng dẫn tái tạo được lưu trong repository.

## Chuẩn bị dữ liệu stationary

Từ thư mục gốc repository, chạy:

```bash
python scripts/prepare_dataset.py
```

Script tải hai bộ dữ liệu `Annthyroid.csv` và `Mammography.csv` từ [repository Online Isolation Forest của tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/main/datasets/stationary/ifor), sau đó lưu bản gốc trong `data/raw/` và bản đã chuẩn bị trong `data/processed/`.

Lần tải đầu tiên, script kiểm tra SHA-256 của từng tệp so với checksum đã khai báo trước khi lưu. Những lần chạy sau, script dùng lại bản gốc đã lưu và kiểm tra checksum lại. Nếu tải nhầm Git LFS pointer, checksum sai, cấu trúc cột thay đổi hoặc dữ liệu không hợp lệ, script dừng với lỗi thay vì âm thầm tiếp tục.

Mỗi CSV nguồn cần có đúng các cột theo thứ tự `id,x0,x1,x2,x3,x4,x5,y`. Bản đầu ra bỏ `id`, giữ nguyên giá trị đặc trưng và thứ tự dòng, rồi đổi tên `y` thành `label`. Các giá trị được chuyển sang số; script từ chối dữ liệu thiếu/vô hạn và yêu cầu nhãn có đúng hai giá trị `0` và `1`.

Không chuẩn hóa (scaling), xáo trộn, chia tập hay loại bỏ dòng trùng lặp. Số dòng trùng được ghi nhận trong báo cáo nhưng vẫn được giữ lại.

## Kết quả được tạo

```text
data/
├── raw/
│   ├── Annthyroid.csv
│   └── Mammography.csv
└── processed/
    ├── annthyroid.csv
    ├── mammography.csv
    └── stationary-summary.json
```

`stationary-summary.json` ghi nguồn tải, checksum, số mẫu, số đặc trưng, số nhãn bình thường/bất thường, tỷ lệ bất thường, số giá trị thiếu, số dòng trùng và các bước xử lý.

Các thư mục `raw/` và `processed/` đã được Git bỏ qua. Cần cài các phụ thuộc của dự án (bao gồm NumPy và pandas) trước khi chạy script.

## Dữ liệu cho thí nghiệm khác

Script hiện chỉ chuẩn bị hai bộ dữ liệu stationary nêu trên. Với INSECTS hoặc dữ liệu dùng cho thí nghiệm drift, cần giữ đúng thứ tự thời gian và ghi rõ nguồn, phiên bản, nhãn/lớp được chọn cùng cách xử lý trước khi bổ sung pipeline tương ứng.
