# Bản nháp slide của Trân — Giai đoạn 2 (6.3, 8.1, 8.2)

Mỗi slide gồm nội dung trên slide, hình minh họa, speaker notes và nguồn IEEE ở chân slide (đánh số
riêng trong từng slide; khi ghép deck sẽ đổi sang số chung). INSECTS d = 10 chạy lại 5 seed trên commit
`6ac25e3`; bảng và 10 link run ở [kết quả drift d = 10](../results/drift-fixed-10.md). Lượt d = 33 ở
[`results/drift.md`](../results/drift.md); stationary ở [`results/stationary.md`](../results/stationary.md).

---

## Slide 6.3 — Mô hình hoàn chỉnh và giao thức đánh giá INSECTS

**Nội dung trên slide**

- Luồng dữ liệu → chấm điểm bằng rừng hiện tại → học lô mới → quên mẫu FIFO vượt cửa sổ.
- 32 cây; cửa sổ học `ω = 2.048`; `η = 32`; mỗi cây có seed riêng. Điểm lớn hơn thể hiện mức độ bất thường cao hơn.
- INSECTS giữ thứ tự dòng; d = 10 (như script tác giả) và d = 33 (như bài báo); lô 100; lô đầu khởi động; nhãn chỉ dùng để đánh giá.
- Đo ROC-AUC, AP và thời gian; ROC-AUC theo cửa sổ đánh giá 5.000 mẫu, bước 1.000. Cửa sổ đánh giá khác cửa sổ học.
- Đối chứng: asdIFOR do nhóm tự dựng bằng Isolation Forest của scikit-learn, huấn luyện lại theo cửa sổ; không phải bản PySAD của tác giả.

**Hình minh họa / Biểu đồ**

Lô t → chấm điểm → ghi điểm → học → loại mẫu cũ; nhánh nhãn chỉ đi vào khối tính ROC-AUC/AP, tách khỏi
đường học.

**Speaker notes**

Forest cập nhật mọi cây, duy trì hàng đợi FIFO và lấy trung bình độ sâu hiệu chỉnh để tính điểm. Với
thí nghiệm của nhóm, điểm của cả lô được tính trước khi lô đó được học; lô đầu tiên chỉ dùng khởi động.
Code tác giả học trước rồi chấm cùng lô [2], nên điểm một mẫu đã chịu ảnh hưởng của chính mẫu đó; đây là
khác biệt protocol quan trọng khi đối chiếu kết quả.

Bài báo ghi INSECTS có 33 đặc trưng [1], nhưng script thí nghiệm của tác giả chỉ lấy 10 cột đầu [2].
Nhóm chạy cả hai cấu hình với cùng code, cùng seed 0–4, chỉ khác số cột. Mỗi seed rừng được cấp
`seed × 32` để hai seed khác nhau không dùng chung cây nào.

Baseline asdIFOR dùng `IsolationForest` của scikit-learn [3] với 32 cây, huấn luyện lại trên 2.048 mẫu
gần nhất sau mỗi 2.048 mẫu mới, theo ý tưởng cửa sổ rời của IForestASD. Tác giả dùng bản trong PySAD,
nên hai baseline cùng ý tưởng nhưng không cùng mã.

Giới hạn độ sâu: bảng tham số của bài báo ghi `log₂(ω/η)`, còn code tác giả và code nhóm dùng
`log₄(ω/η)` với cây nhị phân; khác biệt được tổng hợp ở slide phụ lục. Kiểm thử nhánh tích hợp: 55
passed ngày 19/11 sau khi sửa giới hạn độ sâu trong giai đoạn khởi động. Cấu hình, metrics và dự đoán
của từng run lưu theo hợp đồng kết quả và trong artifact W&B của lượt d = 10.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[3] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Machine Learning
Research*, vol. 12, pp. 2825–2830, 2011.

---

## Slide 8.1 — Khả năng thích nghi sau các mốc thay đổi

**Nội dung trên slide**

| Mốc | ROC-AUC trước mốc | Cửa sổ đầu sau mốc | Seed phục hồi | Độ trễ trung vị (mẫu) |
|---:|---:|---:|---:|---:|
| 51.255 | 0,870 | 0,731 | 0/5 | chưa quan sát |
| 74.381 | 0,749 | 0,624 | 5/5 | 9.719 |
| 100.944 | 0,891 | 0,613 | 0/5 | chưa quan sát |
| 142.291 | 0,696 | 0,607 | 4/5 | 9.309 |
| 152.207 | 0,730 | 0,824 | 5/5 | 5.893 |

*OIF, INSECTS d = 10, trung vị 5 seed; ROC-AUC trên cửa sổ đánh giá 5.000 mẫu.*

- Cửa sổ học 2.048 mẫu: học mới và quên cũ giúp mô hình đổi theo luồng, nhưng không phục hồi ngay
- 2/5 mốc không phục hồi trước mốc kế tiếp; độ trễ đo được gồm cả thời gian tích lũy cửa sổ 5.000

**Hình minh họa / Biểu đồ**

[`drift-recovery-fixed-10.png`](../figures/drift-recovery-fixed-10.png): ROC-AUC theo cửa sổ của 5 seed,
vạch đứt tại các mốc. Hình phụ
[`drift-score-distribution-fixed-10.png`](../figures/drift-score-distribution-fixed-10.png): phân bố điểm
theo nhãn trước và sau mốc đầu (seed 0).

**Speaker notes**

Quy tắc phục hồi: ngưỡng là ROC-AUC của cửa sổ đánh giá hoàn chỉnh cuối cùng trước mốc. Nhóm tìm cửa sổ
hoàn chỉnh đầu tiên sau mốc đạt lại ngưỡng, trước mốc thay đổi kế tiếp, và đo độ trễ tới cuối cửa sổ đó.
Nếu không đạt trước mốc kế tiếp, kết quả ghi “chưa quan sát”, không có nghĩa là mô hình không bao giờ
phục hồi.

Sau mốc đầu, trung vị ROC-AUC giảm từ 0,870 xuống 0,731 và không seed nào đạt lại ngưỡng trong đoạn 2.
Mốc 100.944 cho kết quả tương tự. Sau mốc 74.381, cả 5 seed phục hồi với độ trễ trung vị 9.719 mẫu;
sau mốc 142.291, 4/5 seed phục hồi với trung vị 9.309 mẫu. Ở mốc 152.207, cửa sổ đầu sau mốc đã cao hơn
ngưỡng (0,824 so với 0,730), nên con số 5.893 chỉ phản ánh thời gian tích lũy cửa sổ, không phải một lần
sụt rồi hồi. Baseline asdIFOR có cùng mẫu hình: 0/5 seed ở mốc 51.255 và 100.944, phục hồi ở ba mốc còn
lại; tại mốc 74.381 nó phục hồi sau 5.719 mẫu so với 9.719 của OIF.

Cửa sổ đánh giá chồng lấn và làm mượt chuyển tiếp, nên độ trễ đo được là gần đúng; nếu một cửa sổ thiếu
một lớp thì ROC-AUC không xác định. Mốc có ngưỡng trước cao (0,870 và 0,891) cũng khó đạt lại hơn, nên
không phục hồi có thể do độ khó của đoạn mới thay vì tốc độ thích nghi. Phân bố điểm theo nhãn trước và
sau mốc là mô tả, mỗi lớp chuẩn hóa riêng nên không thể hiện tỷ lệ lớp; nó không phải bằng chứng nhân
quả. Nhóm không suy ra tách/gộp là nguyên nhân duy nhất của biến đổi chất lượng [1].

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.

---

## Slide 8.2 — Tổng kết thực nghiệm

**Nội dung trên slide**

| Bằng chứng | Kết quả của nhóm | Giới hạn |
|---|---|---|
| Ổn định, 30 seed | OIF 0,725 (Annthyroid), 0,870 (Mammography); bài báo 0,685 và 0,854 (+5,8%, +1,9%) | Protocol khác; Annthyroid 7.200 dòng; các seed dùng chung cây; chưa có W&B |
| INSECTS d = 10, 5 seed | OIF 0,728 [0,722; 0,788]; asdIFOR 0,786 ([các run](../results/drift-fixed-10.md)) | Chấm trước học; baseline không phải PySAD |
| INSECTS d = 33, 5 seed | OIF 0,706 [0,696; 0,744]; asdIFOR 0,718 | Chênh lệch nhỏ hơn dao động theo seed của OIF; chưa có W&B |
| Thời gian (d = 33) | OIF 182,9 s, asdIFOR 10,2 s | Python thuần so với Cython; bài báo đo qua PySAD |
| Cửa sổ `ω` (d = 10) | ROC-AUC 0,665 → 0,716 khi `ω` 256 → 8.192 | 1 seed; chưa có W&B |

Repo: [online-iforest-reproduction](https://github.com/BrownieOro/online-iforest-reproduction) · W&B:
[intro-ml-oif](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif)

**Hình minh họa / Biểu đồ**

Bảng là trọng tâm; không dùng hình riêng.

**Speaker notes**

Đây là các kết quả có thể truy vết, không phải toàn bộ tái lập bài báo. Kết luận chính có ba ý. Thứ
nhất, bản triển khai OIF của nhóm đạt chất lượng cùng mức với số của bài báo trên hai bộ dữ liệu ổn định,
nhưng thấp hơn baseline scikit-learn trên Annthyroid. Thứ hai, trên INSECTS với d = 33, OIF và asdIFOR đổi
chất lượng cùng chiều ở cả 5 mốc thay đổi, và chênh lệch trung vị nhỏ hơn dao động theo seed của OIF,
còn với d = 10, asdIFOR cao hơn. Thứ ba, bản OIF Python thuần của nhóm chậm hơn asdIFOR dùng
scikit-learn, trái với xếp hạng thời gian của bài báo; nguyên nhân chủ yếu là cách cài đặt, nên kết quả
này không bác bỏ nhận định về tốc độ của tác giả.

Các giới hạn chung: nhóm chấm điểm trước khi học, còn code tác giả học trước rồi chấm cùng lô; baseline
không phải bản PySAD; INSECTS chạy 5 seed so với 30 lần của bài báo; tệp Annthyroid có 7.200 dòng so với
6.832 dòng trong bài báo. Lượt stationary truyền seed trực tiếp nên các seed liền nhau dùng chung 31/32
cây. Vì dữ liệu hoặc protocol khác, không dùng chênh lệch phần trăm như thước đo tái tạo chính xác.

Baseline offline kiểm tra cài đặt (holdout ngẫu nhiên, seed 42: Annthyroid 0,821, Mammography 0,862; W&B
`z86dyqji`, `judihdbh`) không đưa vào bảng vì khác protocol luồng. Toàn bộ code, kết quả và link run nằm
trong repo nhóm; số liệu từng dòng lấy từ `results/stationary.md`, `results/drift-fixed-10.md`,
`results/drift.md` và `experiments/exp3_window/README.md` [1].

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
