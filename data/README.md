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

## Chuẩn bị dữ liệu không dừng INSECTS

Từ thư mục gốc repository, chạy:

```bash
python scripts/prepare_insects.py
```

Script chỉ dùng thư viện chuẩn và NumPy (không cần pandas).

### Nguồn và phiên bản

- Tệp: `insects_ae-aegypti-female_cx-quinq-male_ae-albopictus-male.csv` trong `datasets/non-stationary/kqt/` của [repository tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/e528c86b77219791d026d732f618efb0c7bde3c1/datasets/non-stationary/kqt), cố định commit `e528c86b77219791d026d732f618efb0c7bde3c1`, tải qua `media.githubusercontent.com` (tệp lưu bằng Git LFS).
- Kích thước 64.138.813 byte; SHA-256 `c38d9b89fb6b133db5b9fe4249621b056f18f177f5832cc8b1d66a840e4eb5d3`. Script kiểm tra checksum ở lần tải đầu và mỗi lần chạy lại; từ chối Git LFS pointer.
- Dữ liệu gốc là INSECTS của Souza và cộng sự (2020). Bài báo (Mục 5.1) và tệp nguồn **không ghi biến thể** (abrupt/incremental/gradual, balanced/imbalanced) đã dùng; tệp cũng không còn tên lớp, nhiệt độ hay timestamp nên không xác định được biến thể từ dữ liệu. TODO: đối chiếu với bộ dữ liệu gốc của Souza và cộng sự nếu nhóm cần ghi rõ.

### Gán nhãn

Tệp nguồn đã được tác giả lọc sẵn ba lớp và chỉ còn cột `y` (0/1):

| `label` | Lớp (theo tên tệp và Mục 5.1) |
|---|---|
| 0 (bình thường) | `ae-aegypti-female`, `cx-quinq-male` |
| 1 (bất thường) | `ae-albopictus-male` |

Vì không còn tên lớp, script không thể tự lọc theo tên; việc lọc được kiểm chứng gián tiếp qua số mẫu và tỷ lệ bất thường so với bài báo (bảng dưới).

### Xử lý

- Kiểm tra cột đúng thứ tự `id,x0,...,x32,y` và `id` đúng bằng `0..n-1` (xác nhận thứ tự dòng gốc).
- Bỏ `id`, đổi `y` thành `label`; giữ nguyên giá trị đặc trưng và thứ tự dòng (thứ tự thời gian).
- Từ chối dữ liệu thiếu/vô hạn; yêu cầu nhãn có đúng hai giá trị `0` và `1`.
- Không chuẩn hóa, xáo trộn, chia tập hay loại bỏ dòng trùng. Theo C5, không chia tập ngẫu nhiên cho INSECTS; đánh giá tuần tự theo thứ tự này.
- Script dừng với lỗi nếu số mẫu, số đặc trưng hoặc tỷ lệ bất thường lệch Mục 5.1.

### Thống kê kiểm chứng

| Đại lượng | Bài báo (Mục 5.1) | Thực tế |
|---|---|---|
| Số mẫu `n` | 212514 | 212514 |
| Số đặc trưng `d` | 33 | 33 |
| Bình thường / bất thường | — | 200813 / 11701 |
| Tỷ lệ bất thường | 5.50% | 5.506% (bài báo nhiều khả năng cắt bớt chữ số; script chấp nhận sai lệch < 0.01 điểm %) |
| Giá trị thiếu / dòng trùng (bỏ `id`) | — | 0 / 0 |

### Mốc thay đổi phân phối

Bài báo nêu INSECTS có 5 thay đổi thực do nhiệt độ (vạch đỏ ở Hình 7) nhưng không liệt kê chỉ số dòng. Năm mốc lấy từ biến `change_points` trong [`experiments/scripts/plot/plot_results_sliding_window.py`](https://github.com/ineveLoppiliF/Online-Isolation-Forest/blob/e528c86b77219791d026d732f618efb0c7bde3c1/experiments/scripts/plot/plot_results_sliding_window.py) của tác giả (cùng commit; phần tử cuối `212514` là cuối luồng, không phải mốc). Script đó vẽ mốc trên trục "# samples" của chính tệp này, nên chỉ số trùng với `row_index` (đếm từ 0, sau khi lọc lớp, C5): mỗi mốc là dòng đầu tiên của đoạn mới.

| Đoạn | `row_index` | Số mẫu | Tỷ lệ bất thường |
|---|---|---:|---:|
| 1 | 0 – 51254 | 51255 | 4.67% |
| 2 | 51255 – 74380 | 23126 | 3.71% |
| 3 | 74381 – 100943 | 26563 | 8.62% |
| 4 | 100944 – 142290 | 41347 | 2.19% |
| 5 | 142291 – 152206 | 9916 | 30.57% |
| 6 | 152207 – 212513 | 60307 | 3.69% |

Kiểm tra độc lập trên dữ liệu: chuẩn hóa từng đặc trưng, so trung bình 3000 dòng trước và sau mỗi mốc. Khoảng cách Euclid tại 5 mốc là 1.78, 3.08, 1.78, 2.62, 1.38, trong khi trung vị tại 200 điểm ngẫu nhiên là 0.17. Đây chỉ là kiểm tra tính hợp lý, không thay cho nguồn của tác giả.

Lưu ý: script thí nghiệm của tác giả (`experiments/scripts/test/test_kqt_datasets.py`) chỉ dùng 10 đặc trưng đầu (`data[:, :10]`), khác với `d = 33` ở Mục 5.1. Tệp này vẫn giữ đủ 33 đặc trưng; số đặc trưng dùng khi chạy do script thí nghiệm quyết định và ghi vào `config.json`.

### Kết quả được tạo

```text
data/
├── raw/
│   └── insects_ae-aegypti-female_cx-quinq-male_ae-albopictus-male.csv
└── processed/
    ├── insects.csv            # x0..x32, label
    └── insects-summary.json   # nguồn, checksum, thống kê, ánh xạ nhãn, các bước xử lý
```
