# Bản nháp slide của Phúc — phương pháp và dữ liệu ổn định (3.2, 3.3, 5.1, 6.1, 7.1)

Mỗi slide gồm nội dung trên slide, hình minh họa, speaker notes và nguồn IEEE ở chân slide (đánh số
riêng trong từng slide; khi ghép deck sẽ đổi sang số chung). Ký hiệu thống nhất toàn deck: `h` là khối
lượng (`mass` trong code), `k` là độ sâu, `R` là miền bao, `τ` là số cây, `ω` là cỡ cửa sổ. Kết quả
stationary nằm ở [`results/stationary.md`](../results/stationary.md) và
[`results/stationary-summary.csv`](../results/stationary-summary.csv); W&B chưa bật cho các lần chạy này.

---

## Slide 3.2 — Online-iTree: histogram phân cấp thích nghi

**Nội dung trên slide**

- Một Online-iTree là histogram đa chiều, được biểu diễn bằng cây nhị phân; mỗi node ứng với một ô không gian.
- Node lưu `h` (số mẫu đi qua) và miền bao `R = [lower, upper]`; node trong lưu thêm chiều chia `q`, ngưỡng `p` và hai node con.
- Rừng Online-iForest gồm `τ` cây; cửa sổ trượt giữ tối đa `ω` mẫu mới nhất.
- Các ô có thể tách khi học thêm dữ liệu và gộp khi quên dữ liệu cũ.

**Hình minh họa / Biểu đồ**

Một hình chữ nhật 2D được chia thành vài ô; ô có nhiều điểm hơn tô đậm hơn. Một ô đã chia được nối với
node cha tương ứng trong sơ đồ cây, node ghi `h`, `R`, `q`, `p`. Chú thích: “mỗi cây = một histogram;
rừng = `τ` cây”.

**Speaker notes**

Online-iTree mô hình hóa không gian đặc trưng bằng cách chia đệ quy thành các ô. Node `N = (h, R)` trong
bài báo lưu chiều cao ô `h`, tức số điểm đi qua node, và miền bao `R`; trong code nhóm, đại lượng này có
tên `mass`, còn miền bao được lưu bằng `lower` và `upper` (`src/oif/tree.py`). `k` là độ sâu của node,
khác với `h`. Node trong còn giữ chiều chia và ngưỡng để định tuyến điểm xuống một trong hai con: nếu
`x_q < p` thì sang trái, ngược lại sang phải. Node không lưu danh sách mẫu thật, nên bộ nhớ của một cây
chỉ phụ thuộc số node, không phụ thuộc độ dài luồng.

Tập hợp `τ` Online-iTree tạo thành Online-iForest. Cửa sổ FIFO thuộc bộ quản lý rừng: khi cửa sổ đầy,
mẫu cũ nhất được đưa vào thủ tục quên của mọi cây. Hai thủ tục học và quên được trình bày ở các slide
tiếp theo; slide này chỉ mô tả trạng thái mà hai thủ tục đó thay đổi [1].

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.

---

## Slide 3.3 — Khởi tạo cây và điều kiện dừng

**Nội dung trên slide**

- Cây bắt đầu là một lá gốc rỗng: `h = 0`, `k = 0`, `R` rỗng; mẫu đầu tiên đặt `R` bằng chính điểm đó
- Tham số: `τ = 32` cây, `ω = 2048`, `η = 32`; cây nhị phân, chia song song trục
- Lá chỉ tách khi đủ cả hai điều kiện: `h ≥ ĥ(k) = η·2^k` **và** `k < δ`
- `δ = C(n_eff, η)` tăng dần khi cửa sổ đang đầy lên; bằng 3 khi `n_eff = ω`

`C(m, η) = 0` nếu `m ≤ η`, ngược lại `ln(m/η) / ln 4`

| Độ sâu `k` | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Ngưỡng tách `ĥ(k)` | 32 | 64 | 128 | 256 |
| Được tách khi cửa sổ đầy (`δ = 3`) | có | có | có | không |

| `n_eff` | 32 | 128 | 512 | 2048 |
|---|---:|---:|---:|---:|
| `δ = C(n_eff, 32)` | 0 | 1 | 2 | 3 |

*`h`: khối lượng ô; `k`: độ sâu; `R`: miền bao; `η`: số mẫu cơ sở; `ĥ(k)`: ngưỡng tách ở độ sâu `k`;
`δ`: giới hạn độ sâu (số thực); `n_eff`: số mẫu đang giữ trong cửa sổ, tối đa `ω`.*

**Hình minh họa / Biểu đồ**

Ba trạng thái của một cây trong giai đoạn khởi động: `n_eff = 32` (chỉ có gốc, `δ = 0`), `n_eff = 128`
(gốc đã tách, `δ = 1`), `n_eff = 2048` (cây sâu tối đa 3 tầng). Mỗi tầng ghi ngưỡng `ĥ(k)` tương ứng.

**Speaker notes**

Online-iTree không được dựng sẵn từ một tập dữ liệu như Isolation Forest truyền thống. Cây bắt đầu từ một
lá gốc rỗng, khối lượng bằng 0 và chưa có miền bao. Mẫu đầu tiên đặt miền bao bằng chính điểm đó; các
mẫu sau nới dần miền bao. Cấu trúc cây chỉ hình thành qua thủ tục học, nên “khởi tạo” ở đây gồm trạng
thái ban đầu, các tham số và điều kiện quyết định khi nào một lá được tách [1].

Có ba tham số chính. `τ` là số cây; nhiều cây giúp giảm phụ thuộc vào một chuỗi phép chia ngẫu nhiên.
`ω` là số mẫu gần nhất mà rừng ghi nhớ. `η` là số mẫu cơ sở: một lá ở độ sâu `k` phải có ít nhất
`η·2^k` mẫu mới được tách. Ngưỡng gấp đôi sau mỗi tầng vì, nếu dữ liệu chia đều, mỗi con chỉ nhận khoảng
một nửa số mẫu của cha; điều kiện này ngăn cây chia quá mịn ở vùng ít dữ liệu và là cơ sở cho phân tích
độ phức tạp ở slide 3.8.

Điều kiện thứ hai là giới hạn độ sâu `δ`. Bài báo ghi `δ = log₂(ω/η)`, bằng 6 với cấu hình trên; code
tác giả dùng `log₄(ω/η)` cho cây nhị phân, bằng 3 [2]. Nhóm theo code tác giả, và tính `δ` từ số mẫu
đang giữ `n_eff` thay vì từ `ω`. Vì vậy trong giai đoạn khởi động, `δ` tăng dần: với 32 mẫu chưa lá nào
được tách, với 128 mẫu chỉ gốc được tách, khi cửa sổ đầy cây có tối đa ba tầng chia. `δ` giữ kiểu số
thực, không làm tròn, và điều kiện tách là `k < δ`.

Bảng trên slide cho thấy hai điều kiện cùng giới hạn kích thước cây: ngưỡng khối lượng quyết định vùng
nào đủ dữ liệu, còn `δ` chặn độ sâu tối đa. Khi đã thỏa cả hai, lá được tách bằng mẫu ảo đều trong miền
bao như slide 3.4 mô tả. Một khác biệt triển khai cần nêu: giả mã bài báo sinh `ĥ` mẫu ảo, còn code nhóm
sinh đúng `h` mẫu ảo, để tổng khối lượng hai con bằng khối lượng cha khi lá đã vượt ngưỡng từ trước do
`δ` tăng dần. Đây là lựa chọn của nhóm, không gán cho bài báo.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest

---

## Slide 5.1 — Dữ liệu ổn định: Annthyroid và Mammography

**Nội dung trên slide**

| Bộ dữ liệu | Số dòng (nhóm) | Số dòng (bài báo) | Đặc trưng | Bất thường (nhóm) | Bất thường (bài báo) |
|---|---:|---:|---:|---:|---:|
| Annthyroid | 7.200 | 6.832 | 6 | 534 (7,42%) | 7,00% |
| Mammography | 11.183 | 11.183 | 6 | TODO | 2,00% |

- Tệp lấy từ thư mục `datasets/stationary/ifor` trong repo tác giả [1]; chỉ bỏ cột ID, giữ mọi dòng
- Annthyroid lệch 368 dòng so với bài báo [2], [3]: sai khác phiên bản/tiền xử lý chưa được giải thích
- Phạm vi: 2 bộ dữ liệu ổn định; 30 seed (0–29); ROC-AUC, AP và thời gian

**Hình minh họa / Biểu đồ**

Bảng là trọng tâm; không dùng hình riêng.

**Speaker notes**

Tệp Annthyroid nhóm dùng có 7.200 dòng, gồm 6.666 bình thường và 534 bất thường (7,42%). UCI ghi bộ ANN
có 3.772 dòng train và 3.428 dòng test; các nguồn ODDS và OpenML cũng phổ biến bản 7.200 dòng [4]. Bảng
Isolation Forest 2008 ghi 6.832 dòng và 7%; bài báo Online Isolation Forest lặp lại cặp số đó [2], [3].
Một đối chiếu độc lập cho biết họ không khôi phục được đúng phiên bản 6.832: bản trên web có 7.200 dòng,
còn bài báo không dẫn bước tiền xử lý để giải thích chênh lệch [5]. Nghiên cứu đó cũng dùng bản 7.200
nhưng báo tỷ lệ outlier 2%, nên cách chọn nhãn có thể khác giữa các bản. Vì vậy, nhóm gọi đây là sai
khác phiên bản hoặc tiền xử lý chưa được giải thích; chưa đủ căn cứ kết luận tệp nhóm sai hay 6.832 là
lỗi gõ.

Script nhóm kiểm tra SHA-256, chỉ bỏ cột ID và giữ mọi dòng. Có 138 dòng trùng theo đặc trưng và nhãn,
không đủ để giải thích 368 dòng chênh lệch, và nhóm không tự xóa dòng để khớp bài báo khi chưa có quy tắc
lọc được xác nhận. Mammography có cùng số dòng và số đặc trưng với bài báo. Hai bộ này là dữ liệu ổn
định, tức không có mốc thay đổi phân phối, nên được dùng để kiểm tra chất lượng và thời gian của bản
triển khai trước khi chuyển sang luồng có drift.

[1] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[2] F. T. Liu, K. M. Ting, and Z.-H. Zhou, "Isolation Forest," in *Proc. 8th IEEE Int. Conf. Data
Mining (ICDM)*, 2008, pp. 413–422, doi: 10.1109/ICDM.2008.17.
[3] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[4] OpenML, "Annthyroid," dataset 40886. [Online]. Available:
https://www.openml.org/search?id=40886&sort=runs&type=data
[5] A. Azzari and M. Bicego, "An empirical characterization of the stability of Isolation Forest
results," in *Proc. Joint IAPR Int. Workshops S+SSPR*, 2024, pp. 166–176,
doi: 10.1007/978-3-031-80507-3_17.

---

## Slide 6.1 — Giao thức đánh giá dữ liệu ổn định

**Nội dung trên slide**

- Mỗi seed xáo trộn dữ liệu một lần; OIF và baseline dùng cùng thứ tự
- 30% đầu làm warm-up; phần còn lại đánh giá theo lô 100
- OIF chấm điểm mỗi lô rồi mới học lô đó; baseline Isolation Forest (scikit-learn) học trên warm-up rồi giữ cố định
- Cấu hình OIF: 32 cây, `ω = 2048`, `η = 32`; 30 seed (0–29); nhãn chỉ dùng để tính chỉ số

**Hình minh họa / Biểu đồ**

Sơ đồ quy trình: dữ liệu → xáo trộn theo seed → 30% warm-up → các lô 100 (chấm điểm → ghi điểm → học).
Nhánh baseline: học một lần trên warm-up → chấm mọi lô. Nhánh nhãn chỉ đi vào khối “ROC-AUC/AP”.

**Speaker notes**

Nhãn chỉ dùng để tính chỉ số, không được đưa vào cập nhật mô hình. Baseline là `IsolationForest` của
scikit-learn [2], học một lần trên phần warm-up rồi giữ cố định. Với dữ liệu ổn định, thứ tự mẫu
không mang thông tin thời gian, nên nhóm xáo trộn theo seed để mỗi lần chạy thấy một luồng khác nhau;
OIF và baseline trong cùng seed dùng chung thứ tự để so sánh có kiểm soát. Điều này khác INSECTS, nơi
thứ tự gốc được giữ nguyên.

Warm-up 30% và baseline cố định là lựa chọn của nhóm, không phải protocol nguyên bản trong bài báo. Bài
báo báo cáo 30 lần chạy và lô 100, nhưng đánh giá oIFOR trên luồng theo cách khác và so với các phương
pháp trực tuyến khác qua thư viện PySAD [1]. Vì vậy kết quả nhóm dùng để phân tích bản triển khai theo
protocol đã nêu, không phải tái tạo trực tiếp Bảng 4. Thứ tự chấm điểm rồi mới học bảo đảm điểm của một
mẫu không dùng thông tin của chính mẫu đó; thứ tự này giống thí nghiệm INSECTS của nhóm.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Machine Learning
Research*, vol. 12, pp. 2825–2830, 2011.

---

## Slide 7.1 — Kết quả dữ liệu ổn định

**Nội dung trên slide**

| Bộ dữ liệu | Phương pháp | ROC-AUC bài báo (oIFOR) | ROC-AUC nhóm | Độ lệch tương đối | AP nhóm | Thời gian nhóm (s) |
|---|---|---:|---:|---:|---:|---:|
| Annthyroid | OIF | 0,685 | 0,725 [0,664; 0,743] | +5,8% | 0,236 | 17,6 |
| Annthyroid | Isolation Forest (scikit-learn) | — | 0,819 [0,804; 0,834] | — | 0,308 | 0,4 |
| Mammography | OIF | 0,854 | 0,870 [0,862; 0,889] | +1,9% | 0,199 | 39,8 |
| Mammography | Isolation Forest (scikit-learn) | — | 0,863 [0,852; 0,870] | — | 0,192 | 0,7 |

*ROC-AUC nhóm: trung vị [Q1; Q3] qua 30 seed; bài báo: trung vị Bảng 4 [1]. Độ lệch tương đối =
(nhóm − bài báo) / bài báo. W&B: chưa có run (lượt chạy tắt W&B).*

- Protocol và số dòng Annthyroid khác bài báo → độ lệch không phải sai số tái tạo thuần túy

**Hình minh họa / Biểu đồ**

Hai biểu đồ nhóm tự tạo: [`stationary-auc.png`](../figures/stationary-auc.png) (ROC-AUC theo seed) và
[`stationary-time.png`](../figures/stationary-time.png) (thời gian).

**Speaker notes**

Với protocol của nhóm, OIF thấp hơn baseline scikit-learn trên Annthyroid (0,725 so với 0,819) và cao
hơn nhẹ trên Mammography (0,870 so với 0,863). So với mốc ROC-AUC trong bài báo, OIF của nhóm cao hơn
0,040 trên Annthyroid (+5,8%) và 0,016 trên Mammography (+1,9%). Không diễn giải các chênh lệch này là
sai lệch tái tạo thuần túy vì ba lý do: protocol khác (warm-up 30% và chấm điểm rồi mới học), tệp
Annthyroid có 7.200 dòng thay vì 6.832, và bài báo chạy qua PySAD còn nhóm dùng bản tự cài đặt.

Thời gian OIF lớn hơn vì OIF cập nhật 32 cây theo từng mẫu bằng Python thuần, còn baseline được huấn
luyện một lần trên warm-up rồi giữ cố định và chấm điểm bằng scikit-learn [2]. Đây không phải so sánh tốc
độ giữa hai thuật toán trực tuyến tương đương, nên không đối chiếu với Bảng 4b của bài báo.

Code hiện tại tạo `h` mẫu ảo đều trong miền bao khi tách lá, rồi dùng chúng để khởi tạo khối lượng và
miền bao cho hai node con (`src/oif/learning.py`); mỗi run lưu hash của `learning.py` và `forest.py` để
truy lại phiên bản. Giả mã bài báo lấy số mẫu theo ngưỡng `ĥ`; nhóm dùng `h` để bảo toàn tổng khối
lượng hai con.

Hạn chế cần nêu: lượt stationary truyền seed trực tiếp cho rừng, và `forest.py` gán seed `seed + i` cho
cây thứ `i`. Hai seed liền nhau vì vậy dùng chung 31/32 cây, nên 30 lần chạy không độc lập và khoảng
Q1–Q3 có thể hẹp hơn thực tế. Thí nghiệm INSECTS đã tránh lỗi này bằng seed rừng `seed × 32`. Lượt
chạy cũng chưa có W&B, nên số liệu chỉ truy được qua tệp kết quả trong repo.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Machine Learning
Research*, vol. 12, pp. 2825–2830, 2011.
