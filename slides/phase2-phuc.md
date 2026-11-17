# Bản nháp slide của Phúc — thí nghiệm dữ liệu ổn định

Nội dung và lời ghi chú dưới đây dành cho ba phần 5.1, 6.1 và 7.1. Cần bổ sung
đường dẫn W&B sau khi tải các lần chạy lên project của nhóm. Khi rà soát, nhóm
đã thấy cách khởi tạo nhánh sau khi tách cây trong code hiện tại khác mã tác giả;
cần sửa phần học và chạy lại trước khi chốt số liệu OIF.

## Phần 5.1 — Bộ dữ liệu và phạm vi

**Nội dung trên slide:** Annthyroid (7.200 dòng trong tệp nhóm; bài báo ghi
6.832) và Mammography (11.183 dòng), mỗi bộ có 6 đặc trưng. Chạy 30 seed, báo
cáo ROC-AUC và thời gian xử lý. Trích dẫn Bảng 2–4 của bài báo bằng `[1]` ở
cuối slide.

**Ghi chú:** Bài báo xáo trộn từng bộ dữ liệu rồi xử lý luồng theo lô 100 điểm.
oIFOR có ROC-AUC trung vị được báo cáo là 0,685 trên Annthyroid và 0,854 trên
Mammography. Nhóm tập trung vào hai bộ dữ liệu này, so sánh phần triển khai OIF
của nhóm với Isolation Forest của scikit-learn. Tệp Annthyroid lấy từ kho của
tác giả có 7.200 dòng, trong khi Bảng 2 ghi 6.832. Nhóm giữ nguyên dữ liệu đã
kiểm tra và nêu rõ chênh lệch này, không tự ý xóa dòng.

## Phần 6.1 — Cách đánh giá

**Nội dung trên slide:** Cùng thứ tự xáo trộn theo từng seed → 30% đầu làm phần
khởi động → chấm phần còn lại theo lô 100 → OIF chấm rồi mới học; Isolation
Forest của scikit-learn giữ cố định. Cấu hình: `window=2048`, `trees=32`,
`eta=32`, seed 0–29.

**Ghi chú:** Hai phương pháp nhận cùng phần dữ liệu khởi động và cùng thứ tự các
điểm tiếp theo. Nhãn chỉ dùng để tính chỉ số. Phần khởi động 30% là lựa chọn của
nhóm để huấn luyện baseline ngoại tuyến; đây không phải protocol nguyên bản của
bài báo. OIF chấm từng lô trước khi học lô đó. Vì vậy, đây là phép so sánh có
kiểm soát giữa hai phương pháp theo cách nhóm triển khai, không phải tái tạo
trực tiếp Bảng 4.

## Phần 7.1 — Kết quả và khác biệt

**Nội dung trên slide:** Dùng `figures/stationary-auc.png` và
`figures/stationary-time.png`. ROC-AUC trung vị của nhóm: Annthyroid — OIF
0,747, scikit-learn 0,819; Mammography — OIF 0,862, scikit-learn 0,863. Mốc
oIFOR trong bài báo: 0,685 và 0,854. Chèn link W&B tương ứng sau khi tải lên.

**Ghi chú:** Các số liệu nhóm là trung vị của 30 seed. OIF thấp hơn baseline
scikit-learn trên Annthyroid và gần bằng trên Mammography. Thời gian trung vị
của OIF là 8,83 giây và 12,92 giây; baseline là khoảng 0,24 giây trên cả hai
bộ dữ liệu. So sánh thời gian không ngang điều kiện vì baseline không được cập
nhật trong luồng. Bài báo dùng toàn bộ luồng và so sánh với năm phương pháp
trực tuyến, nên kết quả nhóm không phải tái tạo trực tiếp. Annthyroid của nhóm
có 7.200 dòng so với 6.832 dòng trong Bảng 2. Cần nêu các khác biệt này cạnh
bảng so sánh. Đối chiếu mã tác giả cho thấy hệ số hiệu chỉnh độ sâu của cây nhị
phân khớp với code nhóm, nhưng code nhóm hiện tạo node con rỗng khi tách cây; mã
tác giả khởi tạo nhánh từ các điểm lấy mẫu trong miền bao. Vì khác biệt này có
thể làm thay đổi kết quả, cần sửa phần học, chạy lại thí nghiệm và cập nhật
bảng cùng biểu đồ trước khi chốt. Link W&B hiện chưa có vì môi trường chạy chưa
được cấu hình tài khoản/project.

## Tài liệu trích dẫn

[1] L. Leveni, D. Carrera và G. B. Giacobello, “Online Isolation Forest,”
ICML, 2024, Mục 5.1–5.3, Bảng 3 và Bảng 4.
