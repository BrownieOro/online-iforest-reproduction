# Bản nháp slide của Thi — Giai đoạn 1 (2.1, 2.2, 3.4, 3.5, 3.9a, 3.9b)

Sáu slide để ghép vào deck chung. Mỗi slide gồm: nội dung trên slide (khung ý, công thức, chú thích
biến, bảng), hình minh họa hoặc biểu đồ, speaker notes và nguồn IEEE ở chân slide. Ký hiệu thống nhất với mục 3.1 và 3.6–3.8: `h` là khối lượng của ô, `k` là độ sâu,
`R` là miền bao. Mọi hình do nhóm tự vẽ. Số trong ví dụ 3.9a–3.9b là số minh họa, không phải kết quả
thực nghiệm.

---

## Slide 2.1 — Isolation Forest truyền thống

**Nội dung trên slide**

Chú thích hình: *Điểm lẻ bị cô lập sau ít phép chia → đường đi ngắn → điểm cao.*

`s(x, n) = 2^(−h̄(x) / c(n))`  với  `c(n) = 2H(n−1) − 2(n−1)/n`,  `H(i) ≈ ln i + 0,5772`

*`x`: mẫu; `n`: cỡ mẫu con mỗi cây; `h̄(x)`: độ dài đường đi trung bình qua các cây (có hiệu chỉnh ở
lá); `c(n)`: độ dài đường đi trung bình kỳ vọng của cây `n` mẫu; `H(i)`: số điều hòa, 0,5772 là hằng
số Euler; `s ∈ (0, 1]`, càng gần 1 càng đáng nghi.*

Giới hạn trên luồng:

- Xây một lần trên tập hữu hạn, không có bước học/quên tăng dần
- Phân phối thay đổi → mô hình cũ lệch khỏi hành vi bình thường hiện tại
- Huấn luyện lại định kỳ được, nhưng tốn chi phí và có độ trễ thích nghi

**Hình minh họa / Biểu đồ**

Khung 1: mặt phẳng 2D, một điểm cam ở xa bị đóng khung sau 2 đường cắt; một điểm xanh trong cụm cần
khoảng 6 đường cắt. Khung 2: cây tương ứng, nhánh điểm cam dừng ở độ sâu 2, nhánh điểm xanh xuống độ
sâu 6.

**Speaker notes**

Isolation Forest, gọi tắt là IF, tiếp cận phát hiện bất thường bằng cách cô lập. Mỗi cây được dựng
bằng phép chia ngẫu nhiên: chọn một đặc trưng, rồi chọn một ngưỡng nằm giữa giá trị nhỏ nhất và lớn
nhất của dữ liệu tại nút đó. Quá trình lặp lại cho đến khi mỗi điểm nằm riêng ở một lá, hoặc cây chạm
giới hạn độ sâu. Hình minh họa thể hiện trực giác: điểm bất thường vừa hiếm vừa khác biệt nên thường
bị tách ra sau ít phép chia, còn điểm trong cụm đông cần nhiều phép chia hơn. Vì một cây phụ thuộc
nhiều vào lựa chọn ngẫu nhiên, IF lấy trung bình độ dài đường đi trên nhiều cây.

Công thức đổi độ dài đường đi trung bình thành điểm. Mẫu số `c(n)` là độ dài đường đi trung bình kỳ
vọng của cây nhị phân dựng trên `n` mẫu, nên điểm của các cây có kích thước khác nhau so sánh được với
nhau. Khi `h̄(x)` nhỏ so với `c(n)`, điểm tiến về 1. Điểm này dùng để xếp hạng mức độ đáng nghi; muốn
có nhãn cảnh báo vẫn phải chọn ngưỡng riêng cho từng ứng dụng.

Khi đưa IF vào luồng dữ liệu, có ba giới hạn chính. Thứ nhất, rừng được xây từ một tập hữu hạn và
không có thủ tục học thêm mẫu mới hay quên mẫu cũ. Thứ hai, khi phân phối thay đổi theo thời gian, mô
hình cũ có thể không còn mô tả đúng hành vi bình thường hiện tại, dẫn tới báo động sai hoặc bỏ sót kiểu
bất thường mới. Thứ ba, như mục 1.3 đã nêu, có thể xây lại rừng định kỳ trên cửa sổ dữ liệu gần đây.
Cách này vẫn dùng được, nhưng mỗi lần xây lại tốn chi phí tính toán, và mô hình chỉ phản ánh thay đổi
sau lần làm mới kế tiếp. Làm mới thưa thì thích nghi chậm, làm mới dày thì tốn tài nguyên. Đây là bối
cảnh để xét các phương pháp trực tuyến ở slide sau và cách Online Isolation Forest cập nhật dần cấu
trúc cây.

[1] F. T. Liu, K. M. Ting, and Z.-H. Zhou, "Isolation Forest," in *Proc. 8th IEEE Int. Conf. Data
Mining (ICDM)*, 2008, pp. 413–422, doi: 10.1109/ICDM.2008.17.
[2] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288-27298, 2024.

---

## Slide 2.2 — Các phương pháp phát hiện bất thường trực tuyến trước OIF

**Nội dung trên slide**

| | Cập nhật | Phân hoạch | Bộ nhớ | Điểm nghẽn chính |
|---|---|---|---|---|
| asdIFOR [2] | Huấn luyện lại định kỳ trên cửa sổ | Cây ngẫu nhiên trên mẫu con | Cửa sổ + một rừng | Thích nghi trễ giữa hai lần làm mới |
| RRCF [3] | Thêm/bớt từng điểm, sửa cây | Lát cắt ngẫu nhiên theo dữ liệu | Cây giữ các điểm mẫu | Sửa cấu trúc cây tốn tài nguyên |
| LODA [4] | Cập nhật histogram 1D | Chiếu ngẫu nhiên 1D, số ô cố định | Số phép chiếu × số ô | Khó mô tả dữ liệu đa đỉnh |
| HST [5] | Làm mới khối lượng định kỳ | Chia đôi tại trung điểm, dựng trước | Số nút cố định, cả vùng trống | Tốn ô cho vùng trống |
| **OIF** [1] | Học từng mẫu, quên mẫu cũ nhất | Tách vùng đông, gộp vùng thưa | `τ` cây + `ω` mẫu cửa sổ | Phải giữ `ω` mẫu; chọn `ω` là đánh đổi |

Bảng 4 của [1] (PySAD, `τ = 32`): oIFOR có tổng thời gian thấp nhất; nhóm kiểm chứng lại ở phần
thực nghiệm.

**Hình minh họa / Biểu đồ**

Không dùng hình riêng; bảng là nội dung chính của slide.

**Speaker notes**

Bài báo so sánh OIF với bốn phương pháp trực tuyến tiêu biểu, chia làm hai hướng. Hướng thứ nhất mở
rộng Isolation Forest. asdIFOR là cách trực tiếp nhất: giữ một cửa sổ dữ liệu gần đây và định kỳ huấn
luyện lại một rừng mới từ đầu, bỏ rừng cũ. Cách này đơn giản, nhưng mô hình chỉ thay đổi sau mỗi lần
huấn luyện lại; làm mới càng dày thì càng tốn thời gian. RRCF quản lý cây động, thêm và bớt từng điểm
bằng cách sửa cấu trúc cây, và dùng điểm số dựa trên mức thay đổi độ phức tạp của cây khi bỏ một điểm.
Theo nhóm tác giả OIF, các thao tác sửa cây này tốn tài nguyên hơn so với việc tách hoặc gộp ô.

Hướng thứ hai dùng histogram. LODA chiếu dữ liệu ngẫu nhiên xuống nhiều trục một chiều rồi dựng
histogram trên từng trục. Cách này nhẹ, nhưng số ô cố định nên khó mô tả dữ liệu có nhiều cụm hoặc
cấu trúc phức tạp. HST dùng cây nhị phân đầy đủ, chia đôi không gian tại trung điểm của một chiều chọn
ngẫu nhiên, trước khi thấy dữ liệu. Vì vậy HST có thể dành nhiều ô cho vùng trống, và cũng phải làm
mới định kỳ như asdIFOR.

OIF kết hợp hai hướng: mỗi cây là một histogram mà độ phân giải thay đổi theo dữ liệu. Vùng đông được
tách nhỏ khi học mẫu mới, vùng thưa được gộp lại khi quên mẫu cũ, và mỗi mẫu được xử lý ngay khi đến.
OIF cũng có giới hạn: rừng phải giữ `ω`
mẫu trong cửa sổ để biết cần quên mẫu nào, và việc chọn `ω` là đánh đổi giữa tốc độ thích nghi và độ
chính xác mô hình hóa, như Mục 4.3 của bài báo phân tích.

Về tốc độ, Bảng 4 của bài báo cho thấy oIFOR có tổng thời gian thấp nhất trong năm phương pháp, khi
tất cả cùng dùng 32 cây và chạy qua thư viện PySAD. Đây là kết quả trong thiết lập của tác giả. Phần
thực nghiệm của nhóm sẽ đo lại thời gian trên cài đặt của nhóm trước khi rút ra kết luận.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288-27298, 2024.
[2] Z. Ding and M. Fei, "An anomaly detection approach based on isolation forest algorithm for
streaming data using sliding window," *IFAC Proc. Volumes*, vol. 46, no. 20, pp. 12–17, 2013.
[3] S. Guha, N. Mishra, G. Roy, and O. Schrijvers, "Robust random cut forest based anomaly detection
on streams," in *Proc. 33rd Int. Conf. Machine Learning*, PMLR, vol. 48, pp. 2712–2721, 2016.
[4] T. Pevný, "Loda: Lightweight on-line detector of anomalies," *Machine Learning*, vol. 102, no. 2,
pp. 275–304, 2016.
[5] S. C. Tan, K. M. Ting, and T. F. Liu, "Fast anomaly detection for streaming data," in *Proc. 22nd
Int. Joint Conf. Artificial Intelligence (IJCAI)*, 2011, pp. 1511–1516.

---

## Slide 3.4 — Học dữ liệu mới và tách ô

**Nội dung trên slide**

- Duyệt gốc → lá theo `x_q < p`; mỗi nút: `h ← h + 1`, nới `R` chứa `x`
- Tách lá khi `h ≥ ĥ` và `k < δ`; ngưỡng gấp đôi mỗi tầng
- `δ`: bài báo `log₂(ω/η)` = 6; code tác giả và nhóm `log₄(ω/η)` = 3

`ĥ(k) = η · 2^k`  ·  mẫu ảo `X ~ U_R`

*`x`: mẫu mới; `x_q`: giá trị ở chiều `q`; `q, p`: chiều và ngưỡng chia; `h`: khối lượng ô; `R`: miền
bao; `k`: độ sâu; `η = 32`: số mẫu cơ sở; `ĥ`: ngưỡng tách; `δ`: giới hạn độ sâu; `ω`: cỡ cửa sổ;
`U_R`: phân phối đều trong `R`.*

Nhãn 4 ô sơ đồ: *Chọn `q`, `p`* → *Sinh mẫu ảo đều trong `R`* → *Chia theo `x_q < p`* → *Khởi tạo 2
con*

**Hình minh họa / Biểu đồ**

Bốn ô vuông nhỏ: (1) hình chữ nhật `R` với một đường cắt nét đứt tại `p`; (2) thêm các chấm xám là mẫu
ảo; (3) chấm có `x_q < p` tô xanh, chấm còn lại tô cam; (4) hai hộp con vừa khít các chấm, mỗi hộp ghi `h_l`,
`h_r`.

**Speaker notes**

Khi một mẫu mới đến, Thuật toán 1 đưa mẫu vào cửa sổ và cho mọi cây học mẫu đó. Thủ tục học của một
cây là Thuật toán 2. Mẫu đi từ gốc xuống lá theo các phép chia đã có: nếu giá trị ở chiều chia nhỏ hơn
ngưỡng thì rẽ trái, ngược lại rẽ phải. Tại mọi nút trên đường đi, khối lượng `h` tăng thêm 1 và miền
bao `R` được nới ra để chứa mẫu. Như vậy mỗi nút chỉ lưu thống kê của ô, không lưu danh sách mẫu.

Khi tới lá ở độ sâu `k`, cây kiểm tra hai điều kiện. Khối lượng phải đạt ngưỡng `η · 2^k`, và độ sâu
phải nhỏ hơn giới hạn `δ`. Ngưỡng tăng gấp đôi sau mỗi tầng: 32 mẫu ở gốc, 64 ở tầng 1, 128 ở tầng 2.
Nhờ đó vùng thưa không bị chia quá sâu, còn vùng đông được chia mịn hơn, và kích thước cây được kiểm
soát. Về `δ`, bài báo ghi `log₂(ω/η)`, còn code tác giả dùng `log₄(ω/η)` cho cây nhị phân. Nhóm theo
code tác giả và tính `δ` từ số mẫu đang có trong cửa sổ, nên `δ` tăng dần khi cửa sổ chưa đầy. Khác
biệt này được ghi lại để không gán lựa chọn của nhóm cho bài báo.

Sơ đồ minh họa thể hiện cách tách ô. Vì không giữ mẫu thật, cây không thể chia lại dữ liệu cũ. Cây
chọn ngẫu nhiên chiều `q` và ngưỡng `p` trong khoảng của chiều đó, sinh `ĥ` mẫu ảo phân phối đều trong
`R`, rồi chia các mẫu ảo theo `x_q < p`. Số mẫu ảo ở mỗi phía cho khối lượng ban đầu của hai nút con,
và hộp bao của chúng cho miền bao ban đầu. Cách làm này dựa trên giả định dữ liệu trong một ô gần đều.
Bản nhóm sinh `h` mẫu ảo thay vì `ĥ` để tổng khối lượng hai con bằng khối lượng cha; chi tiết nằm ở
mục 3.3 và 6.2.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288-27298, 2024.
[2] F. Leveni, "Online-Isolation-Forest," GitHub repository, commit e528c86, 2024. [Online].
Available: https://github.com/ineveLoppiliF/Online-Isolation-Forest

---

## Slide 3.5 — Quên dữ liệu cũ và gộp ô

**Nội dung trên slide**

- Cửa sổ FIFO vượt `ω` → loại mẫu cũ nhất `x_{t−ω}`; mọi cây quên mẫu này
- Duyệt giảm `h ← h − 1`; nút trong có `h < η·2^k` → gộp và dừng
- Drift: vùng cũ mất mẫu → lá nông → điểm tăng; không bảo đảm phục hồi ngay

`R ← BoundingBox(R_l ∪ R_r)`: `l_i ← min(l_i^(l), l_i^(r))`, `r_i ← max(r_i^(l), r_i^(r))`; xóa `q, p`,
`N_l, N_r`

*`ω`: cỡ cửa sổ; `x_{t−ω}`: mẫu vào từ `ω` bước trước; `h`: khối lượng sau khi trừ; `k`: độ sâu;
`R_l, R_r`: miền bao hai con; `l_i, r_i`: cận dưới/trên ở chiều `i`; `q, p`: phép chia;
`N_l, N_r`: hai nút con.*

**Hình minh họa / Biểu đồ**

Trước: nút `N` ở `k = 1`, `h = 64`, hai hộp `R_l`, `R_r` tách bởi một đường cắt. Mũi tên chuyển trạng thái ghi "quên:
`h` 64 → 63 < 64". Sau: đường cắt và hai con biến mất, `N` thành lá với một hộp bao trùm hai hộp cũ.

**Speaker notes**

Thủ tục quên giữ cho mô hình chỉ phản ánh dữ liệu gần đây. Rừng giữ một cửa sổ trượt tối đa `ω` mẫu
theo nguyên tắc vào trước ra trước. Khi một mẫu mới làm cửa sổ vượt `ω`, mẫu cũ nhất bị lấy ra và mọi
cây được yêu cầu quên mẫu đó, theo dòng 8 đến 11 của Thuật toán 1. Vì cần biết mẫu nào bị quên, rừng
phải lưu `ω` mẫu này; đây là phần `+ ω` trong độ phức tạp bộ nhớ ở mục 3.8.

Thủ tục quên của một cây là Thuật toán 3. Mẫu cũ đi từ gốc xuống theo các phép chia hiện có, và khối
lượng `h` giảm 1 tại mỗi nút đi qua. Ở một nút trong độ sâu `k`, sau khi giảm, cây so `h` với ngưỡng
`η · 2^k`. Nếu `h` đã thấp hơn ngưỡng, vùng này không còn đủ dữ liệu để giữ phép chia. Cây gộp hai con:
miền bao của nút được thay bằng hộp nhỏ nhất bao cả hai miền bao con, chiều chia, ngưỡng chia và hai
nhánh con bị xóa, nút trở lại thành lá, và thủ tục dừng tại đó. Nếu `h` vẫn đạt ngưỡng, mẫu đi tiếp
xuống nhánh tương ứng; khi tới lá thì chỉ giảm khối lượng. Như vậy, học có thể làm cây sâu thêm, còn
quên có thể làm cây nông lại.

Cơ chế này hỗ trợ thích nghi khi phân phối thay đổi. Nếu một vùng từng đông nhưng không còn nhận mẫu
mới, các mẫu cũ của vùng đó lần lượt bị quên, khối lượng giảm dưới ngưỡng và các ô được gộp thành lá
nông hơn. Một mẫu mới rơi vào vùng này sẽ có đường đi ngắn hơn, nên điểm bất thường cao hơn so với mẫu
ở vùng còn đông. Ngược lại, vùng đang nhận nhiều mẫu mới được tách mịn hơn qua thủ tục học. Tốc độ
của quá trình này phụ thuộc vào `ω`: cần khoảng `ω` mẫu mới để thay toàn bộ cửa sổ. Thủ tục quên không
bảo đảm mô hình phục hồi ngay sau mỗi thay đổi; phần thực nghiệm trên INSECTS sẽ đo điều này.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288-27298, 2024.

---

## Slide 3.9a — Ví dụ minh họa (1/2): học mẫu mới và quên mẫu cũ

**Nội dung trên slide**

Khung tham số: `ω = 2048` (cửa sổ đầy) · `η = 32` · `k = 1 ⇒ ĥ = 64` · `δ = 3` (nhóm; bài báo 6)

- **Bước 1 — Học `x_t`:** lá trái `h` 63 → 64 ≥ 64 → tách thành 2 lá ở `k = 2`
- **Bước 2 — Quên `x_{t−ω}`:** nút phải `h` 64 → 63 < 64 → gộp về lá ở `k = 1`

*`ω`: cỡ cửa sổ; `η`: số mẫu cơ sở; `k`: độ sâu; `h`: khối lượng; `ĥ = η·2^k`: ngưỡng tách/gộp; `δ`:
giới hạn độ sâu; `x_t`: mẫu mới; `x_{t−ω}`: mẫu cũ nhất.*

**Hình minh họa / Biểu đồ**

Ba cây nhỏ nối tiếp nhau. Trạng thái 1: gốc chia hai; con trái là lá `h = 63`, con phải là nút trong
`h = 64` có hai lá. Trạng thái 2: con trái `h = 64` nở thành hai lá xanh. Trạng thái 3: con phải
`h = 63`, hai lá con biến mất, còn một lá cam.

**Speaker notes**

Ví dụ này ghép thủ tục học và thủ tục quên vào một lần cập nhật của một cây. Cửa sổ đã đầy 2048 mẫu
và `η = 32`, nên ở độ sâu 1 ngưỡng tách và ngưỡng gộp đều bằng `32 · 2 = 64`. Giới hạn độ sâu theo quy
ước của nhóm là 3 khi cửa sổ đầy, theo công thức của bài báo là 6; cả hai đều lớn hơn 1, nên điều kiện
độ sâu không cản trở bước tách. Theo Thuật toán 1 của bài báo, thứ tự là học mẫu mới, quên mẫu cũ, rồi
mới tính điểm. Phần thực nghiệm của nhóm chấm điểm trước khi học để không dùng chính mẫu đang được đánh
giá; khác biệt này được nêu lại ở phần thực nghiệm.

Ở trạng thái ban đầu, gốc đã được chia làm hai. Con trái là một lá đang có 63 mẫu, ngay dưới ngưỡng.
Con phải là một nút trong có đúng 64 mẫu và hai lá con.

Bước 1: mẫu mới đi vào nhánh trái. Khối lượng của lá trái tăng từ 63 lên 64, bằng ngưỡng, nên lá được
tách thành hai lá ở độ sâu 2 bằng mẫu ảo như slide 3.4. Vùng này đang nhận dữ liệu nên độ phân giải
tăng.

Bước 2: vì cửa sổ vượt 2048 mẫu, mẫu cũ nhất bị lấy ra và cây quên mẫu đó. Mẫu cũ đi vào nhánh phải.
Khối lượng của nút trong bên phải giảm từ 64 xuống 63, thấp hơn ngưỡng, nên hai con bị gộp, miền bao
được thay bằng hộp bao chung, và nút trở thành một lá ở độ sâu 1. Vùng này đang mất dữ liệu nên độ
phân giải giảm.

Gốc học một mẫu rồi quên một mẫu, nên khối lượng của gốc không đổi và gốc vẫn giữ phép chia. Sau một
lần cập nhật, cây dời độ phân giải từ vùng đang mất dữ liệu sang vùng đang nhận dữ liệu, trong khi số
mẫu mô hình phản ánh vẫn giữ đúng bằng kích thước cửa sổ.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288-27298, 2024.

---

## Slide 3.9b — Ví dụ minh họa (2/2): tính điểm bất thường sau cập nhật

**Nội dung trên slide**

`D_i(x) = k_i(x) + C(h_i(x), η)` · `D̄(x) = (1/τ) Σ_i D_i(x)` · `s(x) = 2^(−D̄(x)/c)`
`C(h, η) = 0` nếu `h ≤ η`, ngược lại `log₄(h/η)`

*`k_i(x)`, `h_i(x)`: độ sâu và khối lượng của lá chứa `x` ở cây `i`; `C`: hiệu chỉnh lá; `η = 32`;
`τ = 3` cây; `c = 4`: mẫu số minh họa (bản nhóm: 3).*

| | Mẫu A (vùng đông) | Mẫu B (vùng thưa đã gộp) |
|---|---|---|
| Lá trên 3 cây `(k, h)` | (3, 64) · (3, 128) · (3, 256) | (1, 20) · (1, 20) · (1, 20) |
| `D_i(x)` | 3,5 · 4,0 · 4,5 | 1,0 · 1,0 · 1,0 |
| `D̄(x)` → `s(x)` | 4,0 → 0,50 | 1,0 → 0,84 |

Lưu ý: B được xếp đáng nghi hơn A; `s` không phải xác suất, 0,50 không phải ngưỡng.

**Hình minh họa / Biểu đồ**

Ba cây nhỏ. Đường xanh (mẫu A) đi xuống lá ở tầng 3 trong cả ba cây; đường đỏ (mẫu B)
dừng ở lá tầng 1. Ghi `(k, h)` cạnh mỗi lá được chạm tới.

**Speaker notes**

Sau khi cây đã cập nhật, rừng tính điểm cho một mẫu theo ba bước, giống mục 3.6–3.7. Trước hết, ở mỗi
cây, mẫu đi từ gốc xuống lá và lấy độ sâu `k` của lá đó. Vì một lá có thể còn chứa nhiều khối lượng,
độ sâu được cộng thêm phần hiệu chỉnh `C(h, η)`. Phần này bằng 0 khi lá có không quá `η` mẫu, và bằng
`log₄(h/η)` khi lá lớn hơn. Sau đó rừng lấy trung bình độ sâu đã hiệu chỉnh qua các cây, rồi mới đổi
trung bình đó thành điểm bằng hàm mũ. Thứ tự này quan trọng: tính điểm từng cây rồi lấy trung bình sẽ
cho kết quả khác.

Ví dụ dùng rừng 3 cây. Mẫu A nằm ở vùng đông đã được tách mịn, nên ở cả ba cây nó rơi vào lá ở độ sâu
3. Ba lá có khối lượng 64, 128 và 256, nên phần hiệu chỉnh lần lượt là 0,5, 1 và 1,5, cho độ sâu 3,5,
4,0 và 4,5. Lá có 256 mẫu đạt ngưỡng tách ở tầng 3, nhưng tầng 3 đã bằng giới hạn độ sâu của nhóm
khi cửa sổ đầy, nên lá không tách tiếp. Mẫu B nằm ở vùng thưa đã được gộp về một lá ở độ sâu 1, như
bước 2 của slide trước. Vùng này tiếp tục mất mẫu cho tới khi lá chỉ còn 20 mẫu. Vì 20 không vượt quá
`η = 32`, phần hiệu chỉnh bằng 0 và độ sâu ở cả ba cây đúng bằng 1.

Mẫu số `c = 4` được chọn cho dễ tính, giống ví dụ ở mục 3.6. Với mẫu A, độ sâu trung bình 4 cho điểm
0,50; với mẫu B, độ sâu trung bình 1 cho điểm khoảng 0,84. Nếu dùng `c = 3` theo quy ước của nhóm khi
cửa sổ đầy, điểm đổi thành khoảng 0,40 và 0,79 nhưng thứ hạng giữ nguyên. Kết luận đúng là B được xếp
đáng nghi hơn A. Điểm không phải xác suất, và 0,50 không tự động là ngưỡng phân loại. Muốn gắn nhãn
cảnh báo phải chọn ngưỡng riêng, còn ROC-AUC và AP dùng trực tiếp điểm liên tục.

[1] F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi, "Online Isolation
Forest," in *Proc. 41st Int. Conf. Machine Learning*, PMLR, vol. 235, pp. 27288-27298, 2024.
