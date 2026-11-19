# Bản nháp slide của Phúc — phương pháp và stationary

Mục 3.2–3.3 dưới đây được soạn theo phần phương pháp của bài Online Isolation Forest;
đối chiếu lại tên mục với outline chung khi ghép deck. Các mục 5.1, 6.1 và 7.1 đã
được cập nhật theo lần chạy mới sau khi nhóm bổ sung cách khởi tạo node con bằng mẫu
ảo đều trong miền bao. Kết quả nằm ở
[`results/stationary.md`](../results/stationary.md) và
[`results/stationary-summary.csv`](../results/stationary-summary.csv). W&B chưa được
bật cho các lần chạy này nên chưa có URL run.

## Slide 3.2 — Online-iTree: histogram phân cấp thích nghi

**Nội dung trên slide**

- Một Online-iTree là histogram đa chiều, được biểu diễn bằng cây nhị phân; mỗi node ứng với một ô không gian.
- Node lưu `mass` (số mẫu đi qua) và miền bao `R = [lower, upper]`; node trong lưu thêm chiều chia `q`, ngưỡng `p` và hai node con.
- Rừng Online-iForest gồm `τ` cây; cửa sổ trượt giữ tối đa `ω` mẫu mới nhất [5].
- Các ô có thể tách khi học thêm dữ liệu và gộp khi quên dữ liệu cũ.

**Hình minh họa (tự vẽ)**

Vẽ một hình chữ nhật 2D được chia thành vài ô; tô đậm ô có nhiều điểm hơn. Nối một ô đã chia với node cha tương ứng trong sơ đồ cây, ghi `mass`, `R`, `q`, `p` lên node. Bên cạnh ghi “mỗi cây = một histogram; rừng = τ cây”.

**Speaker notes**

Online-iTree mô hình hóa không gian đặc trưng bằng cách chia đệ quy thành các ô. Node `N = (h, R)` trong bài báo lưu chiều cao ô `h` — số điểm đi qua node — và miền bao `R`; trong code nhóm, đại lượng này có tên `mass`, còn miền bao được lưu bằng `lower` và `upper` ([`tree.py`](../src/oif/tree.py)). `k` là độ sâu của node, khác với `h`/`mass`. Node trong còn giữ chiều chia và ngưỡng để định tuyến điểm xuống một trong hai con. Tập hợp `τ` Online-iTree tạo thành Online-iForest. Cửa sổ FIFO thuộc bộ quản lý rừng: khi cửa sổ đầy, mẫu cũ được đưa vào thủ tục quên; chi tiết học/quên theo thời gian nằm ở phần 6.2 của Thi [5].

## Slide 3.3 — Học điểm mới và tách ô

**Nội dung trên slide**

- Điểm mới đi từ gốc tới lá: tăng `mass` và nới miền bao trên đường đi.
- Tách lá khi `mass ≥ ĥ(k) = η·2^k` và `k < δ`.
- Chọn chiều `q` đều ngẫu nhiên, chọn ngưỡng `p` đều trong khoảng của chiều đó.
- Sinh mẫu ảo đều trong miền bao, chia theo `x_q < p`; dùng mass và miền bao của hai nhóm mẫu để khởi tạo hai node con [5].
- **Trong code nhóm:** lấy `node.mass` mẫu ảo; giả mã paper dùng số mẫu theo ngưỡng `ĥ`.

**Hình minh họa (tự vẽ)**

Vẽ tuần tự 3 bước: (1) ô `R` chứa điểm mới; (2) chọn chiều `q` và đường cắt `p`; (3) các mẫu ảo ở hai phía tạo hai node con với `mass` và miền bao riêng. Thêm nhãn ngưỡng `η·2^k` và điều kiện độ sâu `k < δ`.

**Speaker notes**

Khi học một mẫu, code nhóm đi từ root đến lá, tăng `mass` và mở rộng hộp bao để chứa điểm. Nếu lá đạt `η·2^k` và chưa chạm giới hạn độ sâu `δ`, code chọn ngẫu nhiên một chiều rồi một điểm cắt trong khoảng giá trị của chiều ấy. Vì cây chỉ lưu thống kê thay vì giữ toàn bộ mẫu ở từng lá, thuật toán sinh mẫu ảo đều trong miền bao để ước lượng mass và miền bao ban đầu của hai con. Đây là bước khởi tạo, không phải chia lại toàn bộ dữ liệu thật.

Có một khác biệt triển khai cần nêu rõ: giả mã trong paper lấy số mẫu ảo theo ngưỡng `ĥ`, còn `_split` trong code nhóm lấy `node.mass`. Lựa chọn này giữ tổng mass của hai node con bằng mass node cha nếu node đã vượt ngưỡng. Code nhóm cũng chuyển sang chiều rộng lớn nhất khi chiều ngẫu nhiên bị suy biến, bỏ tách nếu mọi chiều đều có độ rộng 0, và dùng trung điểm nếu ngưỡng cắt rơi đúng biên ([`learning.py`](../src/oif/learning.py)). Đây là xử lý của nhóm; không gán các trường hợp biên này cho paper [5].

Phúc đã chạy lại OIF 30 seed cho Annthyroid và Mammography với cách lấy `node.mass`; kết quả hiện tại và các tệp để dò nằm trong [`results/stationary.md`](../results/stationary.md). Không cần chạy lại chỉ để hoàn thiện slide này. Nếu nhóm đổi sang lấy đúng `ĥ` như giả mã, cần chạy lại OIF trên cả hai bộ (30 seed mỗi bộ), rồi cập nhật bảng tổng hợp và hai biểu đồ; baseline scikit-learn không phụ thuộc thay đổi này. Hướng dẫn lệnh chạy ở [`experiments/exp1_stationary/README.md`](../experiments/exp1_stationary/README.md).

## Phần 5.1 — Bộ dữ liệu và phạm vi

**Nội dung trên slide**

- Annthyroid: 7.200 dòng, 6 đặc trưng; paper ghi 6.832 dòng trong bảng benchmark [4], [5].
  Tệp nhóm lấy từ repo Online-Isolation-Forest [1].
- Mammography: 11.183 dòng, 6 đặc trưng [1].
- Chạy 30 seed (0–29); báo cáo ROC-AUC, average precision (AP) và thời gian.
- Nêu rõ đây là hai bộ dữ liệu stationary trong phạm vi tái tạo của nhóm.

**Speaker notes**

Tệp Annthyroid nhóm dùng có 7.200 dòng, gồm 6.666 bình thường và 534 bất thường
(7,42%). OpenML ghi bộ gốc gồm 3.772 dòng train và 3.428 dòng test; một công bố
khác cũng ghi 7.200 dòng, 6 đặc trưng và tỷ lệ bất thường xấp xỉ 7% [2], [3].
Bảng benchmark Isolation Forest 2008 ghi 6.832 dòng và 7%; paper Online Isolation
Forest lặp lại cặp số đó [4], [5]. Đối chiếu hiện có cho thấy nhiều khả năng số
6.832 là lỗi số mẫu trong bảng benchmark được lặp lại, chứ không phải do code xử
lý của nhóm. Cách chuẩn bị dữ liệu của nhóm chỉ bỏ cột ID và giữ nguyên mọi dòng;
có 138 dòng trùng theo đặc trưng và nhãn, nên loại trùng cũng không tạo ra 6.832.
Nhóm giữ nguyên bộ dữ liệu 7.200 dòng và báo rõ sai khác này.

## Phần 6.1 — Cách đánh giá

**Nội dung trên slide**

- Mỗi seed dùng cùng thứ tự xáo trộn cho OIF và baseline.
- 30% đầu làm warm-up; phần còn lại được đánh giá theo lô 100.
- OIF chấm điểm mỗi lô rồi mới học lô đó; baseline Isolation Forest của scikit-learn
  được huấn luyện trên warm-up và giữ cố định.
- Cấu hình OIF: 32 cây, `window_size=2048`, `eta=32`; 30 seed (0–29).

**Speaker notes**

Nhãn chỉ dùng để tính chỉ số, không được đưa vào cập nhật mô hình. Warm-up 30% và
baseline cố định là lựa chọn của nhóm để so sánh có kiểm soát; đây không phải
protocol nguyên bản trong paper. Paper báo cáo 30 lần chạy và lô 100, nhưng đánh
giá oIFOR trên luồng theo cách khác và so với các phương pháp trực tuyến. Vì vậy
kết quả nhóm dùng để phân tích triển khai theo protocol đã nêu, không phải tái tạo
trực tiếp Bảng 4 [5].

## Phần 7.1 — Kết quả và sai khác

**Nội dung trên slide**

ROC-AUC là trung vị [Q1; Q3] qua 30 seed. Kết quả paper là ROC-AUC trung vị của
oIFOR trong Bảng 4 [5].

| Bộ dữ liệu | Phương pháp nhóm | ROC-AUC nhóm | AP nhóm | Thời gian nhóm (giây) | oIFOR trong paper |
|---|---|---:|---:|---:|---:|
| Annthyroid | OIF | 0,725 [0,664; 0,743] | 0,236 | 17,619 | 0,685 |
| Annthyroid | Isolation Forest (scikit-learn) | 0,819 [0,804; 0,834] | 0,308 | 0,418 | — |
| Mammography | OIF | 0,870 [0,862; 0,889] | 0,199 | 39,826 | 0,854 |
| Mammography | Isolation Forest (scikit-learn) | 0,863 [0,852; 0,870] | 0,192 | 0,683 | — |

Dùng hai hình tự vẽ: [`stationary-auc.png`](../figures/stationary-auc.png) và
[`stationary-time.png`](../figures/stationary-time.png). Chèn URL W&B khi có; hiện
các run stationary chưa được tải lên.

**Speaker notes**

Với protocol của nhóm, OIF thấp hơn baseline scikit-learn trên Annthyroid
(0,725 so với 0,819) và cao hơn nhẹ trên Mammography (0,870 so với 0,863). So với
mốc ROC-AUC trong paper, kết quả OIF của nhóm cao hơn 0,040 trên Annthyroid và
0,016 trên Mammography; không diễn giải đây là sai lệch tái tạo thuần túy vì
protocol khác nhau và Annthyroid có số dòng khác nhau. Thời gian OIF lớn hơn vì
OIF cập nhật 32 cây theo luồng, còn baseline được huấn luyện một lần trên warm-up
rồi giữ cố định; đây không phải so sánh tốc độ giữa hai thuật toán trực tuyến
tương đương.

Code hiện tại của nhóm tạo `node.mass` mẫu ảo đều trong miền bao khi tách lá, rồi
dùng chúng để khởi tạo mass và miền bao cho hai node con
([`learning.py`](../src/oif/learning.py)). So với lần chạy trước khi có thay đổi
này, ROC-AUC OIF giảm 0,022 trên Annthyroid và tăng 0,008 trên Mammography. Dùng
bảng và hình mới trong slide; cấu hình mỗi run lưu hash của `learning.py` và
`forest.py` để truy lại phiên bản triển khai. Giả mã paper lấy số mẫu theo ngưỡng
tách `h_hat`; code nhóm dùng `node.mass` để bảo toàn tổng mass hai con nếu node
đã vượt ngưỡng. Đây là lựa chọn triển khai của nhóm cần nêu rõ, không khẳng định
khớp nguyên xi giả mã. W&B chưa được bật nên chưa có URL run.

## Tài liệu trích dẫn

[1] Online-Isolation-Forest, “Stationary datasets: ifor,” GitHub repository. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/main/datasets/stationary/ifor.

[2] OpenML, “Annthyroid,” dataset 40886. [Online]. Available:
https://www.openml.org/search?id=40886&sort=runs&type=data.

[3] K. M. Ting, G.-T. Zhou, F. T. Liu, and S. C. Tan, “Mass estimation,” *Machine
Learning*, vol. 90, pp. 127–160, 2013, doi: 10.1007/s10994-012-5303-x.

[4] F. T. Liu, K. M. Ting, and Z.-H. Zhou, “Isolation Forest,” in *Proc. IEEE Int.
Conf. Data Mining*, 2008. [Online]. Available:
https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf.

[5] L. Leveni et al., “Online Isolation Forest,” *Proceedings of Machine Learning
Research*, vol. 235, pp. 27288–27298, 2024, Table 4. [Online]. Available:
https://proceedings.mlr.press/v235/leveni24a.html.
