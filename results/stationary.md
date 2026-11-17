# Kết quả thí nghiệm dữ liệu ổn định

**Trạng thái:** Đã chạy xong 30 lần trên mỗi bộ dữ liệu. Kết quả thô nằm trong
[`results/raw/stationary/`](raw/stationary/) và bảng tổng hợp ở
[`stationary-summary.csv`](stationary-summary.csv). Chưa có đường dẫn W&B trực
tuyến vì môi trường chạy chưa được cấu hình W&B. Trong lúc rà soát, phát hiện
một khác biệt quan trọng ở cách khởi tạo node con khi tách cây; vì vậy số liệu
OIF hiện tại chưa nên dùng như kết quả đã xác nhận và cần chạy lại sau khi nhóm
sửa, kiểm tra phần học.

## Cách đánh giá

Xem [mô tả thí nghiệm](../experiments/exp1_stationary/README.md). Mỗi bộ dữ liệu
được chạy với 30 seed (0–29) và cùng một thứ tự xáo trộn cho hai phương pháp.
30% dữ liệu đầu dùng làm phần khởi động; phần còn lại được chấm theo lô 100 điểm.
OIF chấm từng lô rồi mới học lô đó. Isolation Forest của scikit-learn được huấn
luyện một lần trên phần khởi động và giữ nguyên trong suốt quá trình đánh giá.
Nhãn chỉ dùng để tính chỉ số, không đưa vào quá trình cập nhật mô hình.

## Kết quả

| Bộ dữ liệu | Phương pháp | ROC-AUC trung vị [Q1, Q3] | AP trung vị | Thời gian trung vị (giây) | Đường dẫn W&B |
|---|---|---:|---:|---:|---|
| Annthyroid | OIF | 0,747 [0,721; 0,770] | 0,253 | 8,829 | Chưa tải lên |
| Annthyroid | Isolation Forest (scikit-learn) | 0,819 [0,804; 0,834] | 0,308 | 0,238 | Chưa tải lên |
| Mammography | OIF | 0,862 [0,848; 0,879] | 0,156 | 12,923 | Chưa tải lên |
| Mammography | Isolation Forest (scikit-learn) | 0,863 [0,852; 0,870] | 0,192 | 0,239 | Chưa tải lên |

Bài báo báo cáo ROC-AUC trung vị của oIFOR là 0,685 trên Annthyroid và 0,854
trên Mammography (Bảng 4). Đây chỉ là mốc tham khảo: bài báo đánh giá trên toàn
bộ luồng và so sánh với các phương pháp trực tuyến, còn thí nghiệm của nhóm có
30% dữ liệu khởi động và dùng một baseline ngoại tuyến cố định.

Tệp Annthyroid lấy từ kho của tác giả có 7.200 dòng, trong khi Bảng 2 của bài
báo ghi 6.832 dòng. Tệp Mammography có 11.183 dòng, trùng với số liệu trong bài.
Script chuẩn bị dữ liệu giữ nguyên các dòng nguồn, kể cả dòng trùng lặp; chênh
lệch của Annthyroid hiện chưa được giải quyết.

## Nhận xét

Theo protocol này, ROC-AUC trung vị của OIF thấp hơn baseline scikit-learn trên
Annthyroid (0,747 so với 0,819) và gần bằng trên Mammography (0,862 so với
0,863). Thời gian OIF cao hơn vì cập nhật 32 cây theo từng lô, còn baseline chỉ
được huấn luyện một lần rồi giữ cố định. Vì vậy, đây không phải phép so tốc độ
giữa hai phương pháp trực tuyến tương đương.

AP trung vị của OIF lần lượt là 0,253 và 0,156. Chỉ số này được báo cáo thêm vì
cả hai bộ dữ liệu đều mất cân bằng lớp. So với AUC trong bài báo, kết quả nhóm
cao hơn khoảng 9,0% trên Annthyroid và 0,9% trên Mammography; không nên xem đây
là sai lệch tái tạo thuần túy vì protocol, số dòng Annthyroid và nhóm phương
pháp đối chứng đều khác nhau.

Đối chiếu [mã nguồn của tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest/blob/main/OnlineIForest/onlineitree.py),
hệ số hiệu chỉnh cho cây nhị phân được tính theo `log(ω/η) / log(4)`, khớp với
cách tính hiện tại trong code nhóm. Tuy vậy, khi tách một node, code nhóm mới
tạo hai node con rỗng; mã tác giả lấy mẫu đều các điểm trong miền bao rồi dùng
các điểm đó để khởi tạo đệ quy hai nhánh. Khác biệt này ảnh hưởng độ sâu và số
đếm khi quên điểm, nên các chỉ số OIF ở trên chỉ mô tả lần chạy của phiên bản
hiện tại. Cần nhóm phụ trách phần học đối chiếu, sửa và chạy lại trước khi dùng
các số liệu OIF trên slide. Biểu đồ hiện tại cũng cần được tạo lại sau lần chạy
mới: [ROC-AUC](../figures/stationary-auc.png) và
[thời gian xử lý](../figures/stationary-time.png).
