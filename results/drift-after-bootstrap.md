# INSECTS drift sau cập nhật khởi tạo node con

> Cập nhật21/11: ZIP drift33 sauF4 đã bàn giao và upload10run. Dùng [báo cáo/nguồn run mới](drift33-f4.md) và [manifest](drift33-wandb-links.json) cho trạng thái W&B và thời gian lượt mới; nội dung bên dưới giữ lịch sử lượt trước.

## Thiết lập

Đã chạy đủ 212.514 dòng theo thứ tự gốc, 33 đặc trưng, 5 seed (0–4), 32 cây,
`window_size=2048`, `eta=32`, lô 100. Lô đầu là warm-up; các lô sau được chấm
điểm trước rồi mới học. Các mẫu lỗi được giữ nguyên. INSECTS được tải từ nguồn đã
ghim phiên bản và xác minh checksum bằng
[`prepare_insects.py`](../scripts/prepare_insects.py).

Các lượt OIF dùng code đã bổ sung lấy mẫu đều trong miền bao để khởi tạo hai node
con. Kết quả thô và cấu hình từng seed ở
[`results/raw/drift-after-bootstrap/`](raw/drift-after-bootstrap/); bảng từng
seed ở [`drift-after-bootstrap.csv`](drift-after-bootstrap.csv). W&B đang tắt.

## Kết quả toàn luồng

| Mô hình | ROC-AUC trung vị [Q1, Q3] | AP trung vị [Q1, Q3] | Thời gian trung vị (giây) |
|---|---:|---:|---:|
| OIF của nhóm | 0,706 [0,696; 0,744] | 0,104 [0,093; 0,108] | 1049,8 |
| asdIFOR của nhóm | 0,718 [0,711; 0,718] | 0,097 [0,096; 0,098] | 61,2 |

asdIFOR trong phép so sánh này là baseline nhóm dựng trên scikit-learn, không
phải implementation trong `pysad` được dùng trong bài báo. Thời gian của hai
implementation vì vậy không phải so sánh tốc độ trực tiếp.

## Ảnh hưởng của các mốc đổi phân phối

Trung vị ROC-AUC theo sáu đoạn, từ seed 0–4:

| Đoạn | OIF | asdIFOR |
|---:|---:|---:|
| 1 | 0,774 | 0,794 |
| 2 | 0,607 | 0,600 |
| 3 | 0,741 | 0,744 |
| 4 | 0,659 | 0,658 |
| 5 | 0,665 | 0,664 |
| 6 | 0,760 | 0,754 |

Hai mô hình cùng giảm sau các mốc 51.255, 100.944 và tăng sau các mốc 74.381,
142.291, 152.207; đây là cùng chiều thay đổi tại cả năm mốc. Hình 7 trong bài
báo mô tả định tính rằng các thuật toán đều chịu ảnh hưởng tương tự khi phân
phối thay đổi đột ngột và không có một phương pháp luôn đứng đầu. Kết quả nhóm
phù hợp với nhận xét đó.

Không nên so các mức AUC trực tiếp với đường cong Hình 7: bài báo lấy trung vị
30 lần chạy, còn nhóm có 5 seed; protocol bài báo học lô trước khi chấm, còn
protocol này chấm trước khi học; script thực nghiệm nhóm gốc dùng 10 đặc trưng,
còn lượt drift chính này dùng 33 theo bảng dữ liệu của bài. Xem mô tả
[protocol và sai khác](../experiments/exp2_drift/README.md) và
[bản dịch bài báo](../papers/online-isolation-forest-vi.md).
