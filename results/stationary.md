# Kết quả thí nghiệm dữ liệu ổn định

**Trạng thái:** Đã chạy lại 30 seed (0–29) mỗi bộ sau khi cập nhật khởi tạo node
con bằng mẫu đều trong miền bao. Kết quả mới nằm trong
[`results/raw/stationary-after-bootstrap/`](raw/stationary-after-bootstrap/);
bảng tổng hợp là [`stationary-summary.csv`](stationary-summary.csv). W&B đang tắt,
nên chưa có đường dẫn trực tuyến.

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
| Annthyroid | OIF | 0,725 [0,664; 0,743] | 0,236 | 17,619 | Chưa tải lên |
| Annthyroid | Isolation Forest (scikit-learn) | 0,819 [0,804; 0,834] | 0,308 | 0,418 | Chưa tải lên |
| Mammography | OIF | 0,870 [0,862; 0,889] | 0,199 | 39,826 | Chưa tải lên |
| Mammography | Isolation Forest (scikit-learn) | 0,863 [0,852; 0,870] | 0,192 | 0,683 | Chưa tải lên |

Bài báo báo cáo ROC-AUC trung vị của oIFOR là 0,685 trên Annthyroid và 0,854
trên Mammography (Bảng 4). Đây chỉ là mốc tham khảo: bài báo đánh giá trên toàn
bộ luồng và so sánh với các phương pháp trực tuyến, còn thí nghiệm của nhóm có
30% dữ liệu khởi động và dùng một baseline ngoại tuyến cố định.

Tệp Annthyroid nhóm dùng, tải từ kho dữ liệu Online Isolation Forest, có 7.200
dòng (6.666 nhãn bình thường, 534 bất thường). UCI/OpenML mô tả bản gốc gồm
3.772 dòng train và 3.428 dòng test; hai lớp bệnh được gộp thành bất thường,
tương ứng 534/7.200 = 7,42% [OpenML]. Bảng dữ liệu của Isolation Forest 2008 lại
ghi 6.832 dòng cùng lúc với “classes 1, 2 (7%)”; Online Isolation Forest 2024
lặp lại đúng cặp 6.832/7% [Liu et al., 2008; Leveni et al., 2024]. Một công bố
khác cũng ghi Annthyroid là 7.200 dòng, 6 chiều, 7% [*Mass estimation*, 2013].

Đối chiếu này cho thấy 6.832 nhiều khả năng là lỗi số mẫu trong bảng benchmark
Isolation Forest 2008 được lặp lại ở paper Online Isolation Forest, chứ không
phải khác biệt do code cây của nhóm. Cùng bộ dữ liệu Annthyroid được ghi là
7.200 dòng, 6 chiều, hai lớp bất thường và 7% trong công bố *Mass estimation*
(2013) của Ting, Zhou, Liu và Tan. Azzari và Bicego cũng đối chiếu bản web 7.200
với số 6.832 trong Isolation Forest 2008, đồng thời ghi nhận paper không nêu
tiền xử lý. 6.832 đúng bằng 7.200 − 368, nhưng nếu bỏ lớp 368 mẫu thì chỉ còn
166 bất thường trên 6.832 (2,43%), không khớp mức 7% và cách gộp hai lớp bất
thường được nêu trong nguồn. Code chuẩn bị dữ liệu của nhóm chỉ bỏ cột ID, giữ
mọi dòng; thay đổi cách khởi tạo node có thể làm đổi điểm số nhưng không thể
làm đổi số dòng đầu vào. Có 138 dòng trùng theo đặc trưng và nhãn, nên bỏ trùng
cũng không tạo ra 6.832. Tệp Mammography nhóm dùng có 11.183 dòng, trùng với số
trong bài.

Nguồn đối chiếu: UCI/OpenML, [Annthyroid](https://www.openml.org/search?id=40886&sort=runs&type=data); F. T. Liu, K. M. Ting, and Z.-H. Zhou, “Isolation Forest,” ICDM 2008, [PDF](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf); L. Leveni et al., “Online Isolation Forest,” ICML 2024, [PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/leveni24a/leveni24a.pdf); K. M. Ting, G.-T. Zhou, F. T. Liu, and S. C. Tan, “Mass estimation,” *Machine Learning*, 90, 127–160, 2013, [doi:10.1007/s10994-012-5303-x](https://doi.org/10.1007/s10994-012-5303-x); A. Azzari and M. Bicego, “An Empirical Characterization of the Stability of Isolation Forest Results,” SSPR 2024, pp. 166–176, [doi:10.1007/978-3-031-80507-3_17](https://doi.org/10.1007/978-3-031-80507-3_17).

## Nhận xét

Theo protocol này, ROC-AUC trung vị của OIF thấp hơn baseline scikit-learn trên
Annthyroid (0,725 so với 0,819) và cao hơn nhẹ trên Mammography (0,870 so với
0,863). Thời gian OIF cao hơn vì cập nhật 32 cây theo từng lô, còn baseline chỉ
được huấn luyện một lần rồi giữ cố định. Vì vậy, đây không phải phép so tốc độ
giữa hai phương pháp trực tuyến tương đương.

AP trung vị của OIF lần lượt là 0,236 và 0,199. Chỉ số này được báo cáo thêm vì
cả hai bộ dữ liệu đều mất cân bằng lớp. So với AUC trong bài báo, kết quả nhóm
cao hơn khoảng 5,8% trên Annthyroid và 1,9% trên Mammography; không nên xem đây
là sai lệch tái tạo thuần túy vì protocol, số dòng Annthyroid và nhóm phương
pháp đối chứng đều khác nhau.

Đối chiếu [code Online Isolation Forest gốc](https://github.com/ineveLoppiliF/Online-Isolation-Forest/blob/main/OnlineIForest/onlineitree.py),
hệ số hiệu chỉnh cho cây nhị phân được tính theo `log(ω/η) / log(4)`, khớp với
cách tính hiện tại trong code nhóm. Code học của nhóm hiện sinh `node.mass` mẫu
đều trong miền bao và dùng chúng để khởi tạo mass cùng miền bao cho hai node
con ([`learning.py`](../src/oif/learning.py)). Đây là một lựa chọn triển khai cần
nêu rõ: giả mã paper lấy số mẫu theo ngưỡng tách `h_hat`, còn code nhóm lấy theo
`node.mass` để giữ tổng mass hai con bằng mass cha nếu node đã vượt ngưỡng. Cần
chốt với nhóm việc giữ lựa chọn này hay đổi về đúng `h_hat`; nếu đổi thì phải chạy
lại. Với phiên bản đang đo, ROC-AUC OIF giảm 0,022 trên Annthyroid và tăng 0,008
trên Mammography so với lần chạy cũ; dùng bộ kết quả mới khi cập nhật slide. Hai
biểu đồ đã được tạo lại từ summary mới:
[ROC-AUC](../figures/stationary-auc.png) và
[thời gian xử lý](../figures/stationary-time.png).
