# Bản nháp slide của Thi: dữ liệu thay đổi, học/quên và kết quả drift

Nội dung cho các mục 5.2, 6.2 và 7.2 (6 slide), để ghép vào deck chung. Mỗi slide gồm: nội dung
trình chiếu, hình tự vẽ, công thức (nếu có), speaker notes (dưới 500 từ) và nguồn IEEE đặt ở cuối
slide. Mọi số liệu lấy từ [`results/drift.md`](../results/drift.md),
[`results/drift-by-segment.csv`](../results/drift-by-segment.csv),
[`results/drift-fixed-10.md`](../results/drift-fixed-10.md),
[`docs/wandb-runs.md`](../docs/wandb-runs.md) và [`data/README.md`](../data/README.md). Số d = 33
là lượt chạy lại 5 seed tại commit `fb35956` (đã sửa F1); số d = 10 là 5 seed của Trân sau sửa F1.
Ví dụ số ở slide 6.2b là kết quả chạy thật của `src/oif/learning.py`, không phải số tự đặt.

Còn thiếu: link W&B của lượt d = 33 (chưa tải lên; lệnh tải ở cuối `results/drift.md`).

---

## Slide 5.2 — Dữ liệu thay đổi theo thời gian: INSECTS

**Nội dung trên slide**

- Nguồn: tệp `insects_ae-aegypti-female_cx-quinq-male_ae-albopictus-male.csv` trong
  `datasets/non-stationary/kqt/` của repository tác giả [2], cố định commit `e528c86`, kiểm tra
  SHA-256. Dữ liệu gốc: INSECTS [3].
- 212.514 mẫu × 33 đặc trưng; giữ 3 lớp:
  - nhãn 0 (bình thường): `ae-aegypti-female`, `cx-quinq-male`;
  - nhãn 1 (bất thường): `ae-albopictus-male`, chiếm 11.701 mẫu (5,506%).
- Giữ nguyên thứ tự thời gian; không chuẩn hóa, không xáo trộn, không chia tập.
- 5 mốc thay đổi `51255, 74381, 100944, 142291, 152207` chia luồng thành 6 đoạn.
- Biến thể gốc (abrupt/incremental, balanced/imbalanced) không được ghi trong bài báo, tệp nguồn
  hay script của tác giả.

| Đoạn | `row_index` | Số mẫu | Bất thường |
|---|---|---:|---:|
| 1 | 0–51254 | 51.255 | 4,67% |
| 2 | 51255–74380 | 23.126 | 3,71% |
| 3 | 74381–100943 | 26.563 | 8,62% |
| 4 | 100944–142290 | 41.347 | 2,19% |
| 5 | 142291–152206 | 9.916 | 30,57% |
| 6 | 152207–212513 | 60.307 | 3,69% |

**Hình minh họa (tự vẽ)**

Một trục thời gian nằm ngang từ 0 đến 212.514, chia 6 đoạn màu nhạt xen kẽ, vạch đỏ đứt tại 5 mốc.
Trên mỗi đoạn ghi tỷ lệ bất thường; đoạn 5 (30,57%) tô đậm hơn để thấy tỷ lệ bất thường thay đổi
mạnh giữa các đoạn.

**Speaker notes**

INSECTS là bộ dữ liệu cảm biến ghi lại chuyển động cánh của côn trùng bay. Phân phối thay đổi theo
thời gian vì nhiệt độ môi trường thay đổi, nên nó phù hợp để kiểm tra một mô hình trực tuyến có
thích nghi được hay không. Nhóm không tự lọc lớp từ bộ gốc mà lấy đúng tệp tác giả dùng trong thí
nghiệm. Tệp này đã được lọc sẵn ba lớp và chỉ còn nhãn 0/1, không còn tên lớp hay nhiệt độ. Vì vậy
việc lọc lớp được kiểm chứng gián tiếp: số mẫu (212.514) và số đặc trưng (33) khớp đúng Mục 5.1 của
bài báo [1]. Tỷ lệ bất thường thực tế là 11.701/212.514 = 5,506%, bài báo ghi 5,50%; chênh lệch nằm
ở chữ số thứ ba, nhiều khả năng do bài báo cắt bớt chữ số.

Năm mốc thay đổi không được liệt kê trong bài báo. Nhóm lấy chúng từ biến `change_points` trong
script vẽ Hình 7 của tác giả [2]. Script vẽ các mốc trên trục số mẫu của chính tệp này, nên chỉ số
trùng với `row_index` của nhóm: mỗi mốc là dòng đầu tiên của đoạn mới. Nhóm kiểm tra thêm trên dữ
liệu: chuẩn hóa từng đặc trưng, so trung bình 3.000 dòng trước và sau mỗi mốc. Khoảng cách tại 5 mốc
là 1,38 đến 3,08, trong khi trung vị tại 200 điểm ngẫu nhiên chỉ là 0,17. Đây là kiểm tra tính hợp
lý, không thay cho nguồn của tác giả.

Bảng cho thấy drift không chỉ làm đổi phân phối đặc trưng mà còn làm đổi tỷ lệ bất thường: đoạn 4
chỉ có 2,19% bất thường, đoạn 5 lên tới 30,57%. Điều này ảnh hưởng trực tiếp tới AP ở phần kết quả,
vì AP phụ thuộc tỷ lệ lớp dương. Hạn chế cần nêu trung thực: không xác định được biến thể INSECTS mà
tác giả dùng, vì cả bài báo, tệp nguồn và script đều không ghi. Nhóm không đoán biến thể. Script tạo
lại dữ liệu là `scripts/prepare_insects.py`; mọi chi tiết nằm trong `data/README.md`.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[3] V. M. A. Souza, D. M. dos Reis, A. G. Maletzke, and G. E. A. P. A. Batista, "Challenges in
benchmarking stream learning algorithms with real-world data," *Data Mining and Knowledge
Discovery*, vol. 34, no. 6, pp. 1805–1858, 2020.

---

## Slide 6.2a — Học/quên trên cây và cửa sổ trượt

**Nội dung trên slide**

- Mỗi nút chỉ lưu: `mass` (số mẫu đi qua), độ sâu `k`, miền bao `[lower, upper]`, phép chia. Không
  lưu mẫu thật.
- **Học** một mẫu: đi từ gốc xuống lá, tăng `mass` và nới miền bao trên đường đi.
- **Tách lá** khi `mass ≥ η·2^k` và `k < δ`: chọn chiều, chọn ngưỡng đều trong miền bao, sinh
  `mass` **mẫu ảo** đều trong miền bao để khởi tạo hai con.
- **Quên** một mẫu: đi lại đường cũ, giảm `mass`; nếu một nút trong có `mass < η·2^k` thì **gộp**
  hai con về nút đó.
- **Cửa sổ FIFO** (Forest): học mẫu mới → đưa vào hàng đợi → nếu vượt `window_size` thì mọi cây quên
  mẫu cũ nhất. Cấu hình: `η = 32`, `window_size = 2048`, 32 cây.

**Công thức**

- Ngưỡng tách/gộp: `ĥ(k) = η · 2^k`.
- Giới hạn độ sâu động: `δ = C(n_eff, η)`, với `C(m, η) = 0` nếu `m ≤ η`, ngược lại `ln(m/η)/ln 4`;
  giữ kiểu số thực. Khi cửa sổ đầy: `δ = ln(2048/32)/ln 4 = 3`.

**Hình minh họa (tự vẽ)**

Sơ đồ vòng đời một nút: "lá" → (mass chạm η·2^k và k < δ) → "nút trong có 2 con" → (mass tụt dưới
η·2^k khi quên) → "lá". Bên cạnh là hàng đợi FIFO 2048 ô: mũi tên vào ở đầu (học), mũi tên ra ở
cuối (quên).

**Speaker notes**

Điểm khác cốt lõi so với Isolation Forest gốc [2] là cây không được dựng lại từ dữ liệu lưu sẵn. Cây
chỉ giữ thống kê tóm tắt. Mỗi nút biết có bao nhiêu mẫu đã rơi vào vùng của nó (`mass`) và hộp nhỏ
nhất chứa các mẫu đó. Nhờ vậy bộ nhớ của một cây không phụ thuộc độ dài luồng.

Khi học, mẫu đi theo phép chia từ gốc xuống lá; mọi nút trên đường đi tăng `mass` và nới hộp để chứa
mẫu. Ngưỡng tách tăng gấp đôi theo mỗi tầng: gốc cần `η` mẫu, tầng 1 cần `2η`, tầng 2 cần `4η`. Như
vậy nút sâu phải có nhiều bằng chứng hơn mới được chia nhỏ tiếp. Giới hạn độ sâu `δ` tính từ số mẫu
đang giữ trong cửa sổ và được giữ là số thực, không làm tròn [1].

Khi tách, cây không có mẫu thật để chia. Theo bài báo, nó sinh các mẫu ảo phân bố đều trong hộp của
lá, chia chúng theo ngưỡng vừa chọn, rồi dùng số mẫu ảo và hộp bao của chúng để khởi tạo hai con.
Nhóm chọn sinh đúng `mass` mẫu ảo, để tổng mass hai con luôn bằng mass của cha. Bản cũ của nhóm tạo
hai con rỗng; đây là một trong năm lỗi đã sửa (L1–L5).

Khi quên, mẫu cũ đi lại đường cũ và giảm `mass`. Nếu một nút trong không còn đủ ngưỡng của tầng mình,
nó gộp hai con thành một lá có hộp bằng hợp hai hộp con. Trong luồng có drift, vùng dữ liệu cũ dần
mất mass nên các nhánh ở đó tự thu lại, còn vùng mới được chia nhỏ hơn. Đây là cơ chế thích nghi mà
thí nghiệm 7.2 đo.

Nhóm giữ ba ngoại lệ an toàn đã thống nhất: nếu chiều được chọn có độ rộng 0 thì đổi sang chiều rộng
nhất; nếu mọi chiều đều rộng 0 thì không tách; nếu ngưỡng rơi đúng biên thì dùng trung điểm. Khi
quên, nếu mẫu rơi vào con có mass 0 (do mẫu ảo phân bố khác mẫu thật) thì trừ vào con còn lại.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. T. Liu, K. M. Ting, and Z.-H. Zhou, "Isolation Forest," in *Proc. 8th IEEE Int. Conf. Data
Mining*, 2008, pp. 413–422. DOI: 10.1109/ICDM.2008.17.

---

## Slide 6.2b — Ví dụ số: tách rồi gộp một nút, và kết quả kiểm thử

**Nội dung trên slide**

Ví dụ thu nhỏ: 2 đặc trưng `(x0, x1)`, `η = 4`, cố định `δ = 1` (chỉ gốc được tách), cửa sổ 4 mẫu,
seed 2. Năm mẫu đến lần lượt: `p1=(1,1)`, `p2=(3,2)`, `p3=(2,5)`, `p4=(4,4)`, `p5=(3.5,1.5)`.

| Bước | Sự kiện | Gốc (k = 0, ngưỡng 4) | Con trái | Con phải |
|---|---|---|---|---|
| 1 | học p1–p3 | lá, mass 3 < 4, hộp `[1,3]×[1,5]` | — | — |
| 2 | học p4 | mass 4 ≥ 4 và 0 < δ, hộp `[1,4]×[1,5]` → **tách**: `x1 < 2,19` | mass 2, hộp `[1,56; 3,44]×[1,22; 1,37]` | mass 2, hộp `[1,82; 2,80]×[3,63; 3,91]` |
| 3 | học p5 (x1 = 1,5 < 2,19) | mass 5 | mass 3, hộp nới tới `(3,50; 1,50)` | mass 2 |
| 4 | quên p1 (FIFO) | mass 4 ≥ 4 → giữ phép chia | mass 2 | mass 2 |
| 5 | quên p2 | mass 3 < 4 → **gộp** | — | — |

Sau bước 5, gốc là lá, mass 3, hộp `[1,56; 3,50]×[1,22; 3,91]`, bằng hợp hai hộp con.

Kiểm thử: `tests/test_learning.py` (15 ca) và `tests/test_window.py` (8 ca); cả bộ test của repo:
**55 passed**.

**Hình minh họa (tự vẽ)**

Ba khung mặt phẳng `(x0, x1)` từ trái sang phải:

1. Sau bước 2: 4 điểm thật (chấm đen), 4 mẫu ảo (dấu x xám), đường ngang `x1 = 2,19`, hai hộp con
   màu xanh/cam.
2. Sau bước 3: hộp trái nới ra để chứa p5.
3. Sau bước 5: hai hộp hợp thành một hộp xám.

**Speaker notes**

Ví dụ được thu nhỏ để đếm bằng tay được: `η = 4` thay vì 32, và cố định `δ = 1` để chỉ gốc được
tách. Trong cấu hình thật, `δ` tính từ số mẫu trong cửa sổ. Mọi con số trong bảng là đầu ra thật
của `learning.py` với seed 2.

Ba mẫu đầu chỉ làm gốc tăng mass và nới hộp, vì mass 3 còn dưới ngưỡng `4·2^0 = 4`. Mẫu thứ tư đưa
mass lên 4. Gốc ở độ sâu 0, nhỏ hơn `δ = 1`, nên được tách. Cây chọn chiều `x1` và ngưỡng 2,19 lấy
đều trong khoảng `[1, 5]`. Sau đó cây sinh 4 mẫu ảo đều trong hộp `[1,4]×[1,5]`, không dùng lại 4
mẫu thật. Hai mẫu ảo có `x1` dưới 2,19 tạo con trái, hai mẫu còn lại tạo con phải. Hộp của mỗi con
là hộp bao các mẫu ảo của nó, nên nhỏ hơn và khác hộp các điểm thật. Đó là cái giá của việc không lưu
dữ liệu.

Mẫu p5 có `x1 = 1,5 < 2,19` nên đi sang trái: con trái tăng mass lên 3 và nới hộp tới 3,50 theo `x0`.
Cửa sổ chỉ giữ 4 mẫu, nên p1 bị quên. Gốc giảm còn mass 4, vẫn bằng ngưỡng, nên phép chia được giữ;
con trái giảm về 2. Khi tiếp tục quên p2, gốc còn 3, dưới ngưỡng 4. Hai con bị gộp, gốc thành lá với
hộp bằng hợp hai hộp con. Trong rừng thật, cửa sổ luôn đầy (2048 mẫu) nên gốc hiếm khi gộp. Việc gộp
chủ yếu xảy ra ở các nhánh sâu thuộc vùng mà luồng đã rời đi sau drift.

Bộ test kiểm tra các bất biến sau mỗi lần học/quên:

- mass không âm;
- hộp rỗng khi và chỉ khi mass bằng 0;
- tổng mass hai con bằng mass cha;
- nút trong luôn đủ ngưỡng;
- hộp con nằm trong hộp cha.

Bộ test cũng kiểm tra:

- `δ` kiểu số thực;
- học rồi quên hết thì trở về lá rỗng;
- cùng seed cho cùng cây;
- dữ liệu trùng không bị tách vô nghĩa;
- cửa sổ giữ đúng các mẫu mới nhất theo thứ tự;
- mass gốc bằng độ dài cửa sổ;
- chấm điểm không làm thay đổi trạng thái rừng.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.

---

## Slide 7.2a — Giao thức và kết quả theo đoạn

**Nội dung trên slide**

- Chấm điểm rồi mới học (score-then-learn), lô 100, đúng thứ tự gốc. Lô đầu chỉ để khởi động; đánh
  giá 212.414 mẫu.
- OIF: 32 cây, cửa sổ 2048, `η = 32`.
- asdIFOR (nhóm tự dựng): Isolation Forest của scikit-learn [3], 32 cây, `max_samples = 256`, huấn
  luyện lại trên 2048 mẫu gần nhất sau mỗi 2048 mẫu mới.
- 5 seed (0–4), d = 33. Bảng dưới là trung vị [Q1; Q3] của ROC-AUC qua 5 seed:

| Đoạn | OIF ROC-AUC | asdIFOR ROC-AUC | OIF AP | asdIFOR AP |
|---|---:|---:|---:|---:|
| Toàn luồng | 0,706 [0,696; 0,744] | 0,718 [0,711; 0,718] | 0,104 | 0,097 |
| 1 | 0,774 [0,742; 0,813] | 0,794 [0,794; 0,797] | 0,116 | 0,110 |
| 2 | 0,607 [0,586; 0,608] | 0,600 [0,599; 0,604] | 0,046 | 0,045 |
| 3 | 0,741 [0,724; 0,789] | 0,744 [0,720; 0,755] | 0,198 | 0,169 |
| 4 | 0,659 [0,633; 0,682] | 0,658 [0,654; 0,659] | 0,034 | 0,032 |
| 5 | 0,665 [0,614; 0,716] | 0,664 [0,660; 0,680] | 0,420 | 0,391 |
| 6 | 0,760 [0,749; 0,791] | 0,754 [0,744; 0,756] | 0,080 | 0,076 |

W&B: lượt d = 33 chưa tải lên (TODO); lượt d = 10 có link ở slide 7.2c.

**Hình minh họa (tự vẽ)**

Dùng bảng trên. Có thể thêm sơ đồ một lô: "lô t đến → chấm điểm bằng mô hình sau lô t−1 → ghi điểm
→ mô hình học lô t".

**Speaker notes**

Giao thức được chọn để điểm của mỗi mẫu không dùng thông tin của chính nó hay của tương lai. Mỗi lô
100 mẫu được chấm bằng mô hình đã học tới lô trước, rồi mới đưa vào học. Nhóm đã kiểm chứng bằng cách
dựng lại mô hình từ đầu và chạy lại 5.000 mẫu đầu: điểm tính lại trùng khớp từng bit với tệp kết quả,
còn thứ tự học-trước-chấm-sau cho điểm khác. Nhãn chỉ dùng để tính chỉ số. Lượt d = 33 trong bảng
được chạy lại trên code đã sửa F1 (commit `fb35956`); ROC-AUC của cả 10 lần chạy trùng với một
lượt chạy độc lập khác của nhóm (sai lệch bằng 0), nên kết quả tái lập được.

Mã thí nghiệm của tác giả [2] học mỗi lô trước khi chấm, nên điểm của một mẫu đã chịu ảnh hưởng của
chính mẫu đó. Nhóm cố ý không làm theo cách này. Baseline asdIFOR được dựng lại trên scikit-learn
theo ý tưởng cửa sổ rời của IForestASD; tác giả dùng bản trong thư viện pysad. Vì vậy hai baseline
cùng ý tưởng nhưng không cùng mã.

Trên toàn luồng, trung vị ROC-AUC của OIF là 0,706 và của asdIFOR là 0,718; AP lần lượt 0,104 và
0,097. Theo đoạn, OIF có trung vị thấp hơn ở đoạn 1 và 3, cao hơn rất ít ở đoạn 2, 4, 5 và 6. Các
chênh lệch này đều nhỏ so với khoảng Q1–Q3 của OIF, nên không nên đọc bảng như một bảng xếp hạng.

AP thay đổi mạnh theo đoạn chủ yếu vì tỷ lệ bất thường thay đổi. Đoạn 5 có 30,57% bất thường nên AP
khoảng 0,4; đoạn 4 chỉ có 2,19% nên AP khoảng 0,03. Vì vậy so AP chỉ có ý nghĩa giữa hai mô hình
trong cùng một đoạn.

Bài báo chạy 30 lần; nhóm chạy 5 seed vì giới hạn thời gian trên CPU laptop. Bảng đầy đủ (min, max,
thời gian học và chấm điểm) nằm trong `results/drift-by-segment.csv`.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[3] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Machine Learning
Research*, vol. 12, pp. 2825–2830, 2011.

---

## Slide 7.2b — Chất lượng theo thời gian: sụt giảm và phục hồi tại các mốc

**Nội dung trên slide**

- Hình: [`figures/drift-quality.png`](../figures/drift-quality.png) (nhóm tự tạo): ROC-AUC trên cửa
  sổ trượt 5.000 mẫu, bước 1.000; đường đậm là trung vị 5 seed, vùng nhạt là Q1–Q3, vạch đỏ đứt là 5
  mốc.
- Thay đổi ROC-AUC trung vị qua từng mốc:

| Mốc | Đoạn | OIF | asdIFOR |
|---|---|---:|---:|
| 51255 | 1 → 2 | −0,167 | −0,194 |
| 74381 | 2 → 3 | +0,134 | +0,143 |
| 100944 | 3 → 4 | −0,082 | −0,085 |
| 142291 | 4 → 5 | +0,006 | +0,005 |
| 152207 | 5 → 6 | +0,095 | +0,090 |

- Hai mô hình đổi cùng chiều ở 5/5 mốc. Đáy của cả hai nằm tại tâm cửa sổ 70.600: OIF 0,551,
  asdIFOR 0,524.

**Hình minh họa**

Chèn nguyên `figures/drift-quality.png` (1800×828 px). Không dùng Hình 7 của bài báo.

**Speaker notes**

Hình tái hiện cách trình bày của Hình 7 trong bài báo [1] bằng số liệu của nhóm. Mỗi điểm là
ROC-AUC tính trên 5.000 mẫu liên tiếp, đặt ở tâm cửa sổ như Mục 5.3 mô tả. Cửa sổ đánh giá này khác
cửa sổ học 2048 mẫu: cửa sổ học là thứ mô hình nhớ, cửa sổ đánh giá chỉ dùng để làm mượt đường cong.

Mốc đầu tiên tại 51.255 gây sụt mạnh nhất: trung vị ROC-AUC theo đoạn giảm 0,167 (OIF) và 0,194
(asdIFOR). Đường cong chạm đáy tại 70.600, gần cuối đoạn 2, rồi bật lên ngay sau mốc 74.381. Mốc
100.944 lại kéo chất lượng xuống. Hai mốc cuối đưa chất lượng hồi dần: đoạn 6 có trung vị 0,760
(OIF), gần mức 0,774 của đoạn 1, và đỉnh cao nhất của đường trung vị nằm trong đoạn 6 (OIF 0,911 tại
165.600; asdIFOR 0,927 tại 179.600).

Ở đầu luồng, OIF thấp hơn asdIFOR rõ rệt: với các cửa sổ có tâm đến 20.000, trung vị đường OIF là
0,735, của asdIFOR là 0,795. Phần còn lại của đoạn 1 (sau 25.000) hai đường gần nhau (chênh trung vị
0,012). Giả thuyết, chưa kiểm chứng: OIF bắt đầu từ cây rỗng và giới hạn độ sâu `δ` chỉ tăng dần theo
số mẫu trong cửa sổ, còn asdIFOR dựng lại cả rừng sau mỗi lô cho tới khi đủ 2048 mẫu.

Điều đáng chú ý là hai mô hình rất khác nhau về cơ chế: OIF cập nhật từng mẫu, còn asdIFOR dựng lại
rừng sau mỗi 2048 mẫu. Dù vậy, chúng đi cùng chiều ở cả 5 mốc với biên độ gần nhau. Điều này phù hợp
với nhận xét của bài báo rằng các phương pháp bị ảnh hưởng tương tự bởi thay đổi đột ngột, và không
phương pháp nào luôn giữ được chất lượng sau thay đổi.

Một cách giải thích: cả hai chỉ nhớ khoảng 2048 mẫu gần nhất, nên sau mỗi mốc cần cỡ một cửa sổ để
thay hết mẫu cũ. Ngoài ra, độ khó của bài toán cũng có thể đổi theo đoạn (giả thuyết), ví dụ khi lớp
bất thường và bình thường gần nhau hơn ở nhiệt độ mới. Mức sụt không chỉ phản ánh tốc độ thích nghi
của mô hình. Nhóm chưa tách riêng được hai yếu tố này. Phân tích độ trễ phục hồi sau từng mốc (lượt
d = 10, 5 seed) do Trân thực hiện, xem `results/drift-fixed-10.md`.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.

---

## Slide 7.2c — Phương sai theo seed, d = 33 so với d = 10, và thời gian chạy

**Nội dung trên slide**

- ROC-AUC toàn luồng qua 5 seed, d = 33:
  - OIF trong [0,645; 0,748], IQR 0,048;
  - asdIFOR trong [0,706; 0,718], IQR 0,007.
  - Đoạn dao động mạnh nhất của OIF là đoạn 5 (0,536–0,745).
- d = 33 so với d = 10 (5 seed mỗi cấu hình; script tác giả chỉ dùng 10 đặc trưng đầu):

| Mô hình | d = 33: trung vị [Q1; Q3] | d = 33: min–max | d = 10: trung vị [Q1; Q3] | d = 10: min–max |
|---|---:|---:|---:|---:|
| OIF | 0,706 [0,696; 0,744] | 0,645–0,748 | 0,728 [0,722; 0,788] | 0,691–0,830 |
| asdIFOR | 0,718 [0,711; 0,718] | 0,706–0,718 | 0,786 [0,785; 0,786] | 0,785–0,798 |

| Seed | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| OIF d = 33 | 0,744 | 0,696 | 0,645 | 0,706 | 0,748 |
| OIF d = 10 | 0,691 | 0,722 | 0,788 | 0,728 | 0,830 |
| asdIFOR d = 33 | 0,711 | 0,718 | 0,706 | 0,718 | 0,718 |
| asdIFOR d = 10 | 0,786 | 0,785 | 0,786 | 0,785 | 0,798 |

- Thời gian toàn luồng d = 33 (trung vị 5 seed, chạy tuần tự): OIF 182,9 s (~861 µs/mẫu; học
  131,5 s, chấm 51,4 s), asdIFOR 10,2 s, tức OIF chậm hơn khoảng 18 lần.
- W&B (d = 10): OIF seed [0](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/lpprt64h),
  [1](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5nsp99kc),
  [2](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/bkkazl0o),
  [3](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zrvo8y72),
  [4](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/gq0qkj76);
  asdIFOR seed [0](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/pqz5mwjq),
  [1](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/8w9ds7kg),
  [2](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/nijtz9s7),
  [3](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5b66rbfq),
  [4](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zkiiyp3g).
  d = 33: chưa tải lên (TODO).

**Hình minh họa (tự vẽ)**

Trái: biểu đồ chấm ROC-AUC toàn luồng của 5 seed cho mỗi mô hình, cho thấy độ trải rộng của OIF.
Phải: hai cột thời gian dùng cùng trục giây, kèm nhãn "Python thuần" cho OIF và "scikit-learn
(Cython)" cho asdIFOR.

**Speaker notes**

Với d = 33, ROC-AUC của OIF dao động theo seed rộng hơn khoảng 9 lần so với asdIFOR, tính theo
khoảng min–max (0,103 so với 0,012). Chênh lệch trung vị giữa hai mô hình chỉ là 0,012, nhỏ hơn
khoảng dao động của OIF. Vì vậy với 5 seed, nhóm không kết luận mô hình nào tốt hơn trên INSECTS. Giả thuyết, chưa kiểm
chứng: cấu trúc cây OIF phụ thuộc chuỗi phép tách ngẫu nhiên tích lũy suốt luồng (mỗi lần tách còn
sinh mẫu ảo), còn asdIFOR xóa và dựng lại rừng định kỳ. Nhóm cũng phát hiện `forest.py` gán seed
`seed + i` cho cây thứ i, nên hai seed liền nhau dùng chung 31/32 cây. Trong thí nghiệm này nhóm né
bằng seed rừng `seed × 32` (điểm F4, đã báo người phụ trách).

Bài báo ghi d = 33, nhưng script thí nghiệm của tác giả [2] chỉ lấy 10 cột đầu. Hai cấu hình được
chạy với cùng `run.py`, cùng seed 0–4 và cùng cách cấp seed rừng, chỉ khác số cột. Với asdIFOR,
d = 10 cao hơn ở cả 5 seed và hai khoảng min–max tách rời (0,785–0,798 so với 0,706–0,718). Với OIF,
d = 10 cao hơn ở 4/5 seed (trung vị 0,728 so với 0,706) nhưng hai khoảng vẫn chồng lên nhau, và
seed 0 lại ngược chiều (0,691 so với 0,744). Với 5 seed, đây là quan sát, chưa phải kiểm định thống
kê. Kết quả nhắc rằng so số với bài báo phải ghi rõ số đặc trưng. Các link W&B ở trên là của lượt
d = 10; lượt d = 10 không so thời gian vì các run OIF được chạy đồng thời.

Về thời gian, bài báo kết luận oIFOR là phương pháp nhanh nhất [1], còn ở nhóm OIF chậm hơn khoảng
18 lần (d = 33). Nguyên nhân chủ yếu là cách cài đặt chứ không phải độ phức tạp thuật toán:

- OIF của nhóm, cũng như mã tác giả, viết bằng Python thuần; mỗi mẫu đi qua vòng lặp Python trên 32
  cây để học, cộng thêm một lần quên.
- asdIFOR của nhóm gọi scikit-learn [3], nơi phần dựng và duyệt cây viết bằng Cython. Nó chỉ huấn
  luyện lại 120 lần trên toàn luồng và chấm điểm theo lô.
- Tác giả chạy asdIFOR qua pysad, vốn xử lý từng mẫu, nên thời gian trong bài báo và của nhóm không so
  trực tiếp được.

Thời gian đo bằng `time.perf_counter`, tách riêng phần chấm điểm và phần học của từng lô, trên CPU
laptop một luồng.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[3] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Machine Learning
Research*, vol. 12, pp. 2825–2830, 2011.
