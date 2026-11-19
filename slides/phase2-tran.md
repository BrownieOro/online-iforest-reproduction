# Nội dung slide — Trân (6.3, 8.1, 8.2)

Bản nháp để ghép vào deck; INSECTS đã chạy lại 5 seed trên commit `6ac25e3`; bảng và 10 link run tại [kết quả drift](../results/drift-fixed-10.md). Không dùng số stationary OIF cũ: chúng được tạo trước khi sửa khởi tạo node con.

## 6.3 — Mô hình hoàn chỉnh và cách đánh giá

**Trên slide**

- Luồng dữ liệu → chấm điểm bằng rừng hiện tại → học lô mới → quên mẫu FIFO vượt cửa sổ.
- 32 cây; cửa sổ học 2.048 mẫu; η = 32; mỗi cây có seed riêng. Điểm lớn hơn thể hiện mức độ bất thường cao hơn.
- INSECTS: 10 đặc trưng đầu, giữ thứ tự dòng; lô 100; lô đầu khởi động; nhãn chỉ dùng để đánh giá.
- Đo ROC-AUC, average precision và thời gian; đường ROC-AUC theo cửa sổ đánh giá 5.000 mẫu, bước 1.000. Cửa sổ đánh giá khác cửa sổ học.
- Đối chứng: Isolation Forest của sklearn được huấn luyện lại theo cửa sổ; không phải cùng cài đặt PySAD của tác giả.

**Hình tự vẽ**: lô t → chấm điểm → ghi điểm → học → loại mẫu cũ; bên cạnh là nhánh tính ROC-AUC/AP từ nhãn, tách khỏi đường học.

**Speaker notes**: Forest cập nhật mỗi cây, duy trì hàng đợi và lấy trung bình độ sâu hiệu chỉnh để tính điểm. Với thí nghiệm nhóm, điểm của cả lô được tính trước khi lô đó được học; lô đầu tiên chỉ dùng khởi động. Code tác giả học trước rồi chấm cùng lô nên đây là khác biệt protocol quan trọng. Kiểm thử nhánh tích hợp: 55 passed ngày 19/11 sau khi sửa giới hạn độ sâu giai đoạn khởi động. Đọc cấu hình, metrics và dự đoán trong artifact của từng run để kiểm tra. [1]

## 8.1 — Khả năng thích nghi khi dữ liệu thay đổi

**Trên slide**

- So sánh ROC-AUC trước và sau các mốc thay đổi; đường cong được tính từ điểm dự đoán trong cửa sổ 5.000 mẫu.
- Cửa sổ học giữ 2.048 mẫu gần nhất: học mới và quên cũ giúp mô hình thay đổi theo dòng, nhưng không đảm bảo phục hồi ngay.
- Định nghĩa phục hồi và đo số mẫu sau mốc chỉ khi có đường cong đủ dữ liệu; nếu không chạm ngưỡng trước mốc kế tiếp, ghi “chưa quan sát được”.
- Phân bố điểm theo nhãn trước/sau mốc là mô tả, không phải bằng chứng nhân quả; so sánh cùng protocol và thang điểm.

**Speaker notes**: Sau mốc đầu, trung vị AUC cửa sổ giảm 0,870 xuống 0,731; 0/5 seed đạt lại ngưỡng trước mốc kế tiếp. Sau mốc 74.381, 5/5 seed đạt ngưỡng, trung vị 9.719 mẫu tính tới cuối cửa sổ; xem results/drift-fixed-10.md. Quy tắc phục hồi được dùng: ngưỡng bằng ROC-AUC cửa sổ ngay trước mốc, tìm cửa sổ hoàn chỉnh đầu tiên sau mốc đạt lại ngưỡng và đo tới cuối cửa sổ trước mốc thay đổi kế tiếp. Cửa sổ đánh giá chồng lấn và làm mượt chuyển tiếp nên độ trễ đo được là gần đúng; nếu dữ liệu một cửa sổ thiếu một lớp thì ROC-AUC không xác định. Không suy ra tách/gộp là nguyên nhân duy nhất của biến đổi chất lượng. [1]

## 8.2 — Tổng kết thực nghiệm

**Trên slide**

| Bằng chứng | Kết luận có thể rút ra | Giới hạn |
|---|---|---|
| INSECTS, 10 đặc trưng | 5 seed: OIF ROC-AUC trung vị 0,728; baseline 0,786 ([các run](../results/drift-fixed-10.md)) | Protocol khác code tác giả; 5 seed so với 30 lần của tác giả |
| Stationary | Chờ Phúc chạy lại sau sửa code | Kết quả OIF cũ không còn hợp lệ cho phiên bản mới |
| Baseline offline đã log | Annthyroid ROC-AUC 0,821; Mammography 0,862, seed 42 | Holdout ngẫu nhiên; không so trực tiếp với protocol streaming |

Repo: https://github.com/BrownieOro/online-iforest-reproduction  
Nhánh đang tích hợp: `feat/tran-insects` (tách từ `origin/feat/thi-learning-tests`; nhánh tích hợp đã đẩy lên GitHub).  
W&B project: https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif  
Annthyroid offline: https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/z86dyqji  
Mammography offline: https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/judihdbh

**Speaker notes**: Đây là các kết quả có thể truy vết, không phải toàn bộ tái lập paper. Trên INSECTS, cùng 10 đặc trưng nhưng nhóm chấm trước học còn tác giả học trước chấm; baseline cũng khác cài đặt. Paper báo 33 đặc trưng trong mô tả dataset trong khi script dùng 10 cột đầu. Đối với stationary, tệp Annthyroid của tác giả có 7.200 dòng so với 6.832 dòng trong paper; cần Phúc xác minh và chạy lại. Không dùng chênh lệch phần trăm như thước đo tái tạo chính xác nếu dữ liệu hoặc protocol khác. [1]

[1] F. Leveni et al., “Online Isolation Forest,” Proc. 41st Int. Conf. Machine Learning, PMLR vol. 235, pp. 27288–27298, 2024. https://proceedings.mlr.press/v235/leveni24a.html

Giới hạn độ sâu: Table 3 paper ghi log₂(ω/η); code tác giả và code nhóm dùng log₄(ω/η) với cây nhị phân. Đây là khác biệt cần trình bày, không suy đoán nguyên nhân.
