# Bản nháp slide của Thi — Giai đoạn 2 (5.2, 6.2a, 6.2b, 7.2a, 7.2b, 7.2c)

Sáu slide để ghép vào deck chung. Mỗi slide gồm: nội dung trên slide (khung ý, công thức, chú thích
biến, bảng), hình minh họa hoặc biểu đồ, speaker notes và nguồn IEEE ở chân slide. Ký hiệu thống nhất
với Giai đoạn 1: `h` là khối lượng của ô (trong code là `mass`), `k` là độ sâu, `R` là miền bao, `ω` là
kích thước cửa sổ (trong code là `window_size`). Số liệu lấy từ `results/drift.md`,
`results/drift-by-segment.csv`, `results/drift-fixed-10.md`, `docs/wandb-runs.md` và `data/README.md`
trên nhánh `feature/tree_data`. Lượt d = 33 chạy tại commit `fb35956`; lượt d = 10 chạy tại commit
`6ac25e3`; cả hai đều có bản sửa giới hạn độ sâu khi khởi động.

---

## Slide 5.2 — Dữ liệu thay đổi theo thời gian: INSECTS

**Nội dung trên slide**

- 212.514 mẫu × 33 đặc trưng · nhãn 0: `ae-aegypti-female`, `cx-quinq-male` · nhãn 1:
  `ae-albopictus-male` (5,506%)
- Tệp của repo tác giả (`e528c86`, kiểm SHA-256); giữ thứ tự thời gian, không chuẩn hóa, xáo trộn
  hay chia tập
- Biến thể gốc (abrupt/incremental) không được ghi trong bài báo lẫn script tác giả

| Đoạn | `row_index` | Số mẫu | Bất thường |
|---|---|---:|---:|
| 1 | 0–51254 | 51.255 | 4,67% |
| 2 | 51255–74380 | 23.126 | 3,71% |
| 3 | 74381–100943 | 26.563 | 8,62% |
| 4 | 100944–142290 | 41.347 | 2,19% |
| 5 | 142291–152206 | 9.916 | 30,57% |
| 6 | 152207–212513 | 60.307 | 3,69% |

**Hình minh họa / Biểu đồ**

Trục thời gian từ 0 đến 212.514 chia 6 đoạn màu nhạt xen kẽ, vạch đỏ đứt tại 5 mốc, mỗi đoạn ghi tỷ lệ
bất thường; đoạn 5 (30,57%) tô đậm hơn.

**Speaker notes**

INSECTS là bộ dữ liệu cảm biến ghi lại chuyển động cánh của côn trùng bay [3]. Phân phối thay đổi theo
thời gian vì nhiệt độ môi trường thay đổi, nên bộ này phù hợp để kiểm tra khả năng thích nghi của một
mô hình trực tuyến. Nhóm không tự lọc lớp từ bộ gốc mà dùng đúng tệp tác giả dùng trong thí nghiệm, là
`datasets/non-stationary/kqt/insects_ae-aegypti-female_cx-quinq-male_ae-albopictus-male.csv` trong
repository của tác giả [2], cố định commit `e528c86` và kiểm tra SHA-256. Tệp này đã được lọc sẵn ba
lớp và chỉ còn nhãn 0/1, không còn tên lớp hay nhiệt độ. Vì vậy việc lọc lớp được kiểm chứng gián tiếp:
số mẫu và số đặc trưng khớp Mục 5.1 của bài báo [1]. Tỷ lệ bất thường thực tế là 11.701/212.514 =
5,506%, bài báo ghi 5,50%; chênh lệch nằm ở chữ số thứ ba, nhiều khả năng do bài báo làm tròn xuống.

Năm mốc thay đổi 51.255, 74.381, 100.944, 142.291 và 152.207 không được liệt kê trong bài báo. Nhóm lấy
chúng từ biến `change_points` trong script vẽ Hình 7 của tác giả [2]. Script vẽ các mốc trên trục số
mẫu của chính tệp này, nên chỉ số trùng với `row_index` của nhóm: mỗi mốc là dòng đầu tiên của đoạn
mới. Nhóm kiểm tra thêm trên dữ liệu bằng cách chuẩn hóa từng đặc trưng và so trung bình 3.000 dòng
trước và sau mỗi mốc. Khoảng cách tại 5 mốc là 1,38 đến 3,08, trong khi trung vị tại 200 điểm ngẫu nhiên
chỉ là 0,17. Đây là kiểm tra tính hợp lý, không thay cho nguồn của tác giả.

Bảng cho thấy drift không chỉ làm đổi phân phối đặc trưng mà còn làm đổi tỷ lệ bất thường: đoạn 4 chỉ
có 2,19%, đoạn 5 lên tới 30,57%. Điều này ảnh hưởng trực tiếp tới AP ở phần kết quả, vì AP phụ thuộc tỷ
lệ lớp dương. Hạn chế cần nêu là không xác định được biến thể INSECTS mà tác giả dùng, vì bài báo, tệp
nguồn và script đều không ghi; nhóm không đoán biến thể. Script tạo lại dữ liệu là
`scripts/prepare_insects.py`, mọi chi tiết nằm trong `data/README.md`.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[3] V. M. A. Souza, D. M. dos Reis, A. G. Maletzke, and G. E. A. P. A. Batista, "Challenges in
benchmarking stream learning algorithms with real-world data," *Data Mining and Knowledge
Discovery*, vol. 34, no. 6, pp. 1805–1858, 2020.

---

## Slide 6.2a — Triển khai học/quên và cửa sổ trượt

**Nội dung trên slide**

- Nút lưu `mass` (`h`), `depth` (`k`), `lower/upper` (`R`) và phép chia; không lưu mẫu thật
- Tách khi `mass ≥ ĥ(k)`, `k < δ`; sinh `mass` mẫu ảo, giữ tổng mass hai con
- Forest: học → đẩy FIFO → vượt `window_size` (`ω`) thì mọi cây quên mẫu cũ nhất
- Ngoại lệ biên: chiều rộng 0, ngưỡng trùng biên, con `mass = 0` khi quên

`ĥ(k) = η · 2^k` · `δ = C(n_eff, η)`, với `C(m, η) = 0` nếu `m ≤ η`, ngược lại `ln(m/η) / ln 4`

*`mass`/`h`: khối lượng nút; `k`: độ sâu; `η = 32`; `n_eff`: số mẫu đang giữ trong cửa sổ, tối đa
`ω = 2048`; `δ`: giới hạn độ sâu kiểu số thực, bằng 3 khi cửa sổ đầy; rừng gồm 32 cây.*

**Hình minh họa / Biểu đồ**

Sơ đồ vòng đời một nút: "lá" → (`mass ≥ η·2^k` và `k < δ`) → "nút trong có 2 con" → (`mass < η·2^k`
khi quên) → "lá", kèm hàng đợi FIFO 2048 ô với mũi tên vào (học) và mũi tên ra (quên).

**Speaker notes**

Slide này nêu các quyết định cài đặt của nhóm. Phần học và quên nằm trong `src/oif/learning.py`, phần cửa sổ nằm trong `src/oif/forest.py`. Ký hiệu trong
code nối trực tiếp với lý thuyết: `mass` là khối lượng `h`, `depth` là độ sâu `k`, cặp `lower` và
`upper` là miền bao `R`, còn `window_size` là `ω`. Mỗi nút chỉ giữ các thống kê này cùng chiều chia và
ngưỡng chia, nên bộ nhớ của một cây không phụ thuộc độ dài luồng.

Giới hạn độ sâu được tính bằng cùng hàm `C` dùng để hiệu chỉnh độ sâu và chuẩn hóa điểm, theo code của
tác giả [2], và được giữ ở dạng số thực, không làm tròn. Trước khi học mỗi mẫu, Forest tính lại `δ` từ
số mẫu sẽ có trong cửa sổ sau khi thêm mẫu đó, giới hạn bởi `ω`. Vì vậy trong giai đoạn khởi động `δ`
tăng dần, còn khi cửa sổ đầy thì `δ = log₄(2048/32) = 3`.

Khi tách lá, bài báo sinh `ĥ` mẫu ảo đều trong miền bao [1]. Nhóm sinh đúng `mass` mẫu ảo, bằng số mẫu
lá đang có. Lý do là `δ` tăng dần, nên một lá có thể đã vượt ngưỡng từ trước khi được phép tách; lấy
`mass` mẫu ảo giữ được bất biến tổng mass hai con bằng mass của cha. Đây là lựa chọn triển khai cần
nêu rõ, không phải chi tiết của bài báo.

Thứ tự trong Forest theo Thuật toán 1: mọi cây học mẫu mới, mẫu được đưa vào hàng đợi, và nếu hàng đợi
vượt `ω` thì mẫu cũ nhất được lấy ra để mọi cây quên. Nhóm thêm ba quy tắc cho các trường hợp biên. Nếu
chiều được chọn có độ rộng bằng 0 thì đổi sang chiều rộng nhất, và nếu mọi chiều đều rộng 0 thì không
tách, để tránh phép chia vô nghĩa trên dữ liệu trùng. Nếu ngưỡng rơi đúng biên thì dùng trung điểm. Khi
quên, vì khối lượng con được khởi tạo từ mẫu ảo, mẫu thật có thể rơi vào con có `mass = 0`; khi đó phần
trừ được chuyển sang con còn lại để giữ bất biến về khối lượng.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest

---

## Slide 6.2b — Ví dụ chạy thật: tách rồi gộp một nút, và kết quả kiểm thử

**Nội dung trên slide**

Thiết lập: 2 đặc trưng `(x0, x1)`, `η = 4`, cố định `δ = 1`, cửa sổ 4 mẫu, seed 2; mẫu p1–p5 đến lần
lượt.

| Bước | Sự kiện | Gốc (`k = 0`, ngưỡng 4) | Con trái | Con phải |
|---|---|---|---|---|
| 1 | Học p1–p3 | Lá, mass 3 | — | — |
| 2 | Học p4 | Mass 4 → **tách** `x1 < 2,19` | Mass 2 | Mass 2 |
| 3 | Học p5 | Mass 5 | Mass 3, **nới hộp** | Mass 2 |
| 4 | Quên p1 | Mass 4 → **giữ** phép chia | Mass 2 | Mass 2 |
| 5 | Quên p2 | Mass 3 < 4 → **gộp** | — | — |

Kiểm thử: 23 unit test cho học/quên và cửa sổ (`test_learning.py` 15, `test_window.py` 8); toàn repo
**55 passed**.

**Hình minh họa / Biểu đồ**

Ba khung mặt phẳng `(x0, x1)`. Khung 1 (sau bước 2): 4 điểm thật, 4 mẫu ảo, đường `x1 = 2,19`, hộp con
trái `[1,56; 3,44]×[1,22; 1,37]` và hộp con phải `[1,82; 2,80]×[3,63; 3,91]`. Khung 2 (sau bước 3): hộp
trái nới tới `(3,50; 1,50)`. Khung 3 (sau bước 5): một hộp gộp `[1,56; 3,50]×[1,22; 3,91]`.

**Speaker notes**

Ví dụ được thu nhỏ để đếm bằng tay: `η = 4` thay vì 32, và cố định `δ = 1` để chỉ gốc được tách. Năm
mẫu đến lần lượt là p1 = (1; 1), p2 = (3; 2), p3 = (2; 5), p4 = (4; 4) và p5 = (3,5; 1,5). Mọi con số
trong bảng và trong hình là đầu ra thật của `learning.py` với seed 2.

Ba mẫu đầu chỉ làm gốc tăng mass và nới hộp tới `[1, 3]×[1, 5]`, vì mass 3 còn dưới ngưỡng
`4 · 2^0 = 4`. Mẫu thứ tư đưa mass lên 4 và hộp thành `[1, 4]×[1, 5]`. Gốc ở độ sâu 0, nhỏ hơn
`δ = 1`, nên được tách. Cây chọn chiều `x1` và ngưỡng 2,19 lấy đều trong `[1, 5]`, rồi sinh 4 mẫu ảo
đều trong hộp của gốc, không dùng lại 4 mẫu thật. Hai mẫu ảo có `x1` dưới 2,19 tạo con trái, hai mẫu
còn lại tạo con phải. Hộp của mỗi con là hộp bao các mẫu ảo của nó, nên nhỏ hơn và khác hộp các điểm
thật; đó là cái giá của việc không lưu dữ liệu.

Mẫu p5 có `x1 = 1,5 < 2,19` nên đi sang trái: con trái tăng mass lên 3 và nới hộp tới 3,50 theo `x0`.
Cửa sổ chỉ giữ 4 mẫu, nên p1 bị quên. Gốc giảm còn mass 4, vẫn bằng ngưỡng, nên phép chia được giữ và
con trái giảm về 2. Khi tiếp tục quên p2, gốc còn 3, dưới ngưỡng 4, nên hai con bị gộp và gốc thành lá
với hộp bằng hợp hai hộp con.

Bộ test kiểm tra các bất biến sau mỗi lần học và quên: mass không âm, hộp rỗng khi và chỉ khi mass bằng
0, tổng mass hai con bằng mass cha, mọi nút trong đều đủ ngưỡng và hộp con nằm trong hộp cha. Bộ test
cũng kiểm tra `δ` kiểu số thực, học rồi quên hết thì trở về lá rỗng, dữ liệu trùng không bị tách, cửa sổ giữ đúng các mẫu mới nhất theo thứ tự, mass gốc bằng độ dài cửa sổ, và
chấm điểm không làm thay đổi trạng thái rừng.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.

---

## Slide 7.2a — Giao thức và kết quả theo đoạn

**Nội dung trên slide**

- Chấm điểm rồi mới học, lô 100, đúng thứ tự gốc; đánh giá 212.414 mẫu
- OIF và asdIFOR tự dựng bằng scikit-learn: 32 cây, `ω = 2048`, `η = 32`; 5 seed, `d = 33`

| Đoạn | OIF ROC-AUC | asdIFOR ROC-AUC | OIF AP | asdIFOR AP |
|---|---:|---:|---:|---:|
| Toàn luồng | 0,706 [0,696; 0,744] | 0,718 [0,711; 0,718] | 0,104 | 0,097 |
| 1 | 0,774 [0,742; 0,813] | 0,794 [0,794; 0,797] | 0,116 | 0,110 |
| 2 | 0,607 [0,586; 0,608] | 0,600 [0,599; 0,604] | 0,046 | 0,045 |
| 3 | 0,741 [0,724; 0,789] | 0,744 [0,720; 0,755] | 0,198 | 0,169 |
| 4 | 0,659 [0,633; 0,682] | 0,658 [0,654; 0,659] | 0,034 | 0,032 |
| 5 | 0,665 [0,614; 0,716] | 0,664 [0,660; 0,680] | 0,420 | 0,391 |
| 6 | 0,760 [0,749; 0,791] | 0,754 [0,744; 0,756] | 0,080 | 0,076 |

*ROC-AUC: trung vị [Q1; Q3] qua 5 seed; AP: trung vị.* W&B: lượt d = 33 chờ tải lên; lượt d = 10 có
link ở slide 7.2c.

**Hình minh họa / Biểu đồ**

Bảng số liệu là trọng tâm của slide; không dùng hình riêng.

**Speaker notes**

Giao thức được chọn để điểm của mỗi mẫu không dùng thông tin của chính nó hay của tương lai. Mỗi lô 100
mẫu được chấm bằng mô hình đã học tới lô trước, rồi mới đưa vào học; lô đầu tiên chỉ dùng để khởi động.
Nhóm đã kiểm chứng bằng cách dựng lại mô hình từ đầu và chạy lại 5.000 mẫu đầu: điểm tính lại trùng
từng bit với tệp kết quả, còn thứ tự học trước rồi chấm cho điểm khác. Nhãn chỉ dùng để tính chỉ số.
Lượt d = 33 được chạy tại commit `fb35956`; ROC-AUC của cả 10 lần chạy trùng với một lượt chạy độc lập
khác của nhóm, sai lệch bằng 0, nên kết quả tái lập được.

Mã thí nghiệm của tác giả [2] học mỗi lô trước khi chấm, nên điểm của một mẫu đã chịu ảnh hưởng của
chính mẫu đó; nhóm cố ý không làm theo cách này. Baseline asdIFOR được dựng lại bằng Isolation Forest
của scikit-learn [3] theo ý tưởng cửa sổ rời của IForestASD: 32 cây, `max_samples = 256`, huấn luyện
lại trên 2048 mẫu gần nhất sau mỗi 2048 mẫu mới. Tác giả dùng bản trong thư viện PySAD, vì vậy hai
baseline cùng ý tưởng nhưng không cùng mã.

Trên toàn luồng, trung vị ROC-AUC của OIF là 0,706 và của asdIFOR là 0,718; AP lần lượt là 0,104 và
0,097. Theo đoạn, OIF có trung vị thấp hơn ở đoạn 1 và 3, cao hơn rất ít ở đoạn 2, 4, 5 và 6. Các
chênh lệch này đều nhỏ so với khoảng Q1–Q3 của OIF, nên không nên đọc bảng như một bảng xếp hạng.

AP thay đổi mạnh theo đoạn chủ yếu vì tỷ lệ bất thường thay đổi. Đoạn 5 có 30,57% bất thường nên AP
khoảng 0,4, còn đoạn 4 chỉ có 2,19% nên AP khoảng 0,03. Vì vậy so AP chỉ có ý nghĩa giữa hai mô hình
trong cùng một đoạn. Bài báo chạy 30 lần; nhóm chạy 5 seed vì giới hạn thời gian trên CPU laptop. Bảng
đầy đủ gồm min, max, thời gian học và thời gian chấm điểm nằm trong `results/drift-by-segment.csv`.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[3] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Machine Learning
Research*, vol. 12, pp. 2825–2830, 2011.

---

## Slide 7.2b — Chất lượng theo thời gian qua 5 mốc thay đổi

**Nội dung trên slide**

| Mốc | Đoạn | OIF | asdIFOR |
|---|---|---:|---:|
| 51255 | 1 → 2 | −0,167 | −0,194 |
| 74381 | 2 → 3 | +0,134 | +0,143 |
| 100944 | 3 → 4 | −0,082 | −0,085 |
| 142291 | 4 → 5 | +0,006 | +0,005 |
| 152207 | 5 → 6 | +0,095 | +0,090 |

*Thay đổi ROC-AUC trung vị (5 seed, d = 33) từ đoạn trước sang đoạn sau mỗi mốc.*

- Đổi cùng chiều ở 5/5 mốc; đáy tại tâm 70.600: OIF 0,551, asdIFOR 0,524
- 20.000 mẫu đầu: OIF 0,735 so với asdIFOR 0,795 (giả thuyết: `δ` tăng dần khi khởi động)

**Hình minh họa / Biểu đồ**

`figures/drift-quality.png` (nhóm tự tạo, 1800×828 px): ROC-AUC trên cửa sổ trượt 5.000 mẫu, bước
1.000; đường đậm là trung vị 5 seed, vùng nhạt là Q1–Q3, vạch đỏ đứt là 5 mốc. Không dùng Hình 7 của
bài báo.

**Speaker notes**

Biểu đồ trình bày theo cách của Hình 7 trong bài báo [1], nhưng bằng số liệu của nhóm. Mỗi điểm là
ROC-AUC tính trên 5.000 mẫu liên tiếp, đặt ở tâm cửa sổ như Mục 5.3 mô tả, bước 1.000 mẫu. Cửa sổ
đánh giá này khác cửa sổ học 2048 mẫu: cửa sổ học là phần mô hình nhớ, cửa sổ đánh giá chỉ dùng để làm
mượt đường cong.

Mốc đầu tiên tại 51.255 gây sụt lớn nhất: trung vị ROC-AUC theo đoạn giảm 0,167 với OIF và 0,194 với
asdIFOR. Đường cong chạm đáy tại 70.600, gần cuối đoạn 2, rồi bật lên sau mốc 74.381. Mốc 100.944 lại
kéo chất lượng xuống. Hai mốc cuối đưa chất lượng hồi dần: đoạn 6 có trung vị 0,760 với OIF, gần mức
0,774 của đoạn 1, và đỉnh của đường trung vị nằm trong đoạn 6 (OIF 0,911 tại 165.600; asdIFOR 0,927
tại 179.600).

Ở đầu luồng, OIF thấp hơn asdIFOR rõ rệt: với các cửa sổ có tâm đến 20.000, trung vị đường OIF là
0,735, của asdIFOR là 0,795. Phần còn lại của đoạn 1, sau 25.000, hai đường gần nhau với chênh trung vị
0,012. Giả thuyết chưa kiểm chứng: OIF bắt đầu từ cây rỗng và giới hạn độ sâu `δ` chỉ tăng dần theo số
mẫu trong cửa sổ, còn asdIFOR dựng lại cả rừng sau mỗi lô cho tới khi đủ 2048 mẫu.

Hai mô hình rất khác nhau về cơ chế: OIF cập nhật từng mẫu, còn asdIFOR dựng lại rừng sau mỗi 2048
mẫu. Dù vậy, chúng đổi cùng chiều ở cả 5 mốc với biên độ gần nhau, phù hợp với nhận xét của bài báo
rằng các phương pháp bị ảnh hưởng tương tự bởi thay đổi đột ngột. Một cách giải thích là cả hai chỉ nhớ
khoảng 2048 mẫu gần nhất, nên sau mỗi mốc cần cỡ một cửa sổ để thay hết mẫu cũ. Độ khó của bài toán
cũng có thể đổi theo đoạn, nên mức sụt không chỉ phản ánh tốc độ thích nghi; nhóm chưa tách riêng được
hai yếu tố này. Phân tích độ trễ phục hồi sau từng mốc trên lượt d = 10 nằm trong
`results/drift-fixed-10.md`.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.

---

## Slide 7.2c — Phương sai theo seed, d = 33 so với d = 10, và thời gian chạy

**Nội dung trên slide**

| Mô hình | d = 33: trung vị [Q1; Q3] | d = 33: min–max | d = 10: trung vị [Q1; Q3] | d = 10: min–max |
|---|---:|---:|---:|---:|
| OIF | 0,706 [0,696; 0,744] | 0,645–0,748 | 0,728 [0,722; 0,788] | 0,691–0,830 |
| asdIFOR | 0,718 [0,711; 0,718] | 0,706–0,718 | 0,786 [0,785; 0,786] | 0,785–0,798 |

- Theo seed (d = 33): OIF dao động rộng gấp ~9 lần asdIFOR; đoạn 5 rộng nhất (0,536–0,745)
- Thời gian d = 33: OIF 182,9 s, asdIFOR 10,2 s; chậm ~18× (Python thuần so với Cython)
- W&B d = 10 — OIF: [s0](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/lpprt64h)·[s1](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5nsp99kc)·[s2](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/bkkazl0o)·[s3](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zrvo8y72)·[s4](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/gq0qkj76) | asdIFOR: [s0](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/pqz5mwjq)·[s1](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/8w9ds7kg)·[s2](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/nijtz9s7)·[s3](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5b66rbfq)·[s4](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zkiiyp3g); d = 33: chờ tải lên

**Hình minh họa / Biểu đồ**

Biểu đồ cột thời gian toàn luồng d = 33 (trung vị 5 seed, cùng trục giây): OIF 182,9 s với nhãn "Python
thuần", asdIFOR 10,2 s với nhãn "scikit-learn (Cython)".

**Speaker notes**

Với d = 33, ROC-AUC toàn luồng của OIF dao động theo seed rộng hơn khoảng 9 lần so với asdIFOR, tính
theo khoảng min–max: 0,103 so với 0,012. Chênh lệch trung vị giữa hai mô hình chỉ là 0,012, nhỏ hơn
khoảng dao động của OIF, nên với 5 seed nhóm không kết luận mô hình nào tốt hơn trên INSECTS. Giả
thuyết chưa kiểm chứng: cây OIF phụ thuộc chuỗi phép tách ngẫu nhiên tích lũy suốt luồng, còn asdIFOR
dựng lại rừng định kỳ. Trong `forest.py`, cây
thứ `i` nhận seed `seed + i`, nên hai seed rừng liền nhau dùng chung 31/32 dòng ngẫu nhiên của cây. Thí
nghiệm này cấp seed rừng `seed × 32` để các seed không dùng chung cây nào.

Bài báo ghi d = 33, nhưng script thí nghiệm của tác giả [2] chỉ lấy 10 cột đầu. Hai cấu hình được chạy
với cùng `run.py`, cùng seed 0 đến 4 và cùng cách cấp seed rừng, chỉ khác số cột. Với asdIFOR, d = 10
cao hơn ở cả 5 seed và hai khoảng min–max tách rời. Với OIF, d = 10 cao hơn ở 4/5 seed, trung vị 0,728
so với 0,706, nhưng hai khoảng vẫn chồng lên nhau, và seed 0 lại ngược chiều với 0,691 so với 0,744.
Với 5 seed, đây là quan sát, chưa phải kiểm định; khi so với bài báo cần ghi rõ số đặc trưng. Lượt d = 10 không được so thời gian vì các run OIF chạy đồng thời.

Về thời gian, bài báo báo cáo oIFOR có thời gian thấp nhất [1], còn ở nhóm OIF chậm hơn khoảng 18 lần
với d = 33. Nguyên nhân chủ yếu là cách cài đặt. OIF của nhóm, như mã tác giả, viết bằng Python thuần và
lặp qua 32 cây cho từng mẫu. asdIFOR của
nhóm gọi scikit-learn [3], nơi phần dựng và duyệt cây viết bằng Cython, chỉ huấn luyện lại 120 lần trên
toàn luồng và chấm điểm theo lô. Tác giả chạy asdIFOR qua PySAD, vốn xử lý từng mẫu, nên hai bộ số thời
gian không so trực tiếp được. Thời gian đo bằng `time.perf_counter` trên CPU laptop một luồng.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288–27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest
[3] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Machine Learning
Research*, vol. 12, pp. 2825–2830, 2011.
