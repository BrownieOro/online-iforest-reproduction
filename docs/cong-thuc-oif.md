# Công thức OIF đang dùng trong bản nhóm

Tài liệu đối chiếu phần Trân phụ trách: độ sâu, điểm bất thường, ghép rừng và
các trường hợp biên. Mốc mã nguồn: nhánh tích hợp sau F4, commit `0ea32145`.
Tài liệu mô tả lựa chọn hiện có; không thay đổi thuật toán và không đưa các lượt
thử nghiệm riêng ngoài bộ số liệu nhóm đã chốt vào báo cáo.

## 1. Ký hiệu và trạng thái

| Ký hiệu | Ý nghĩa | Trong code |
|---|---|---|
| h | Khối lượng thống kê của node, không phải độ sâu | `Node.mass` |
| k | Độ sâu node; gốc bằng 0 | `Node.depth` |
| R | Miền bao của node theo từng chiều | `lower, upper` |
| η | Ngưỡng khối lượng cơ sở | `eta=32` |
| ω | Dung lượng cửa sổ học | `window_size=2048` |
| n_eff | Số mẫu đang giữ trong cửa sổ | `len(forest._window)` |
| τ | Số cây | `n_trees=32` |

Mass của các con có nguồn gốc từ mẫu ảo ở bước tách, nên không diễn giải chúng
là phép đếm chính xác mọi điểm thật hiện có trong từng vùng.

## 2. Độ sâu và điều kiện tách

Trong code nhóm, đặt

```text
c_group(m, η) = 0                         nếu m ≤ η
              ln(m / η) / ln(4)          nếu m > η

δ = c_group(n_eff, η)
ngưỡng tách/gộp ở node sâu k: ĥ(k) = η × 2^k
```

Khi học một điểm, Forest tính giới hạn từ `min(n_window+1, ω)` trước khi
đưa điểm vào cây. Lá được tách khi đồng thời `h ≥ η × 2^k` và `k < δ`.
Giữ δ dạng số thực, không làm tròn. Ví dụ:

| n_eff | 32 | 128 | 512 | 2048 |
|---|---:|---:|---:|---:|
| δ | 0 | 1 | 2 | 3 |
| k được phép tách | không có | 0 | 0–1 | 0–2 |

Khi n_eff=2048, lá có thể ở độ sâu 3; điều đó không có nghĩa mọi cây cân bằng
hoặc mọi lá đều sâu 3. Ngưỡng khối lượng vẫn phải thỏa mãn.

## 3. Độ sâu hiệu chỉnh và điểm

Với điểm x rơi vào lá của cây i:

```text
D_i(x) = k_i + c_group(h_i, η)
D_mean(x) = mean_i D_i(x)
s(x) = 2 ^ ( -D_mean(x) / (c_group(n_eff, η) + ε) )
ε = numpy.finfo(float).eps
```

- `tree.path_lengths(X)` trả vector độ sâu đã hiệu chỉnh, một giá trị mỗi mẫu.
- `anomaly_scores(depths, window_size, eta)` nhận ma trận (số cây, số mẫu).
  Tên đối số là `window_size`, nhưng Forest truyền **n_eff hiện tại**.
- `forest.score_samples(X)` chấm bằng trạng thái hiện tại; không học/quên và
  không thay trạng thái RNG.
- Điểm lớn hơn biểu thị mức bất thường cao hơn theo mô hình; không phải xác suất.
  Không tự gán `s=0.5` thành ngưỡng “an toàn”.

Ví dụ minh họa khi n_eff=2048 và η=32, mẫu số xấp xỉ 3:

| Tình huống minh họa | Độ sâu hiệu chỉnh trung bình | Điểm |
|---|---:|---:|
| Các cây đều cho k=3, h=128: c_group=1 | 4 | 2^(-4/3) ≈ 0,39685 |
| Các cây đều cho k=1, h=32: c_group=0 | 1 | 2^(-1/3) ≈ 0,79370 |

Ví dụ chỉ giải thích công thức và thứ tự điểm, không gán nhãn thật.

## 4. Biên và quy tắc xấp xỉ

- Forest chưa học thì chấm điểm báo lỗi rõ ràng.
- Khi m≤η, code chặn hệ số hiệu chỉnh về 0; ε tránh chia trực tiếp cho 0.
  Đây là quy ước triển khai, không phải công thức log áp dụng nguyên xi cho m=0.
- Đầu vào phải là ma trận hữu hạn, đúng số chiều. Code không dùng nhãn để học.
- Lá rỗng có mass=0 và miền bao None; hiệu chỉnh của nó bằng 0.
- Khi tách, nhóm lấy `node.mass` mẫu đều trong R, chia theo q,p rồi khởi tạo
  mass/miền bao hai con; tổng mass con bằng mass cha. Không tạo mặc định hai con rỗng.
- Nếu chiều chọn có độ rộng 0, nhóm dùng chiều rộng nhất; mọi chiều hằng thì
  không tách. Ngưỡng rơi đúng biên được thay bằng trung điểm.
- Khi quên vào con mass=0, nhóm trừ sang con còn lại để tránh mass âm. Đây là
  xử lý xấp xỉ bổ sung ngoài giả mã; không gọi là định tuyến đúng điểm thật.
- Gộp khi mass của node trong xuống dưới η×2^k: lấy miền bao các con không
  rỗng, xóa phép chia và con. Không lưu kho điểm thật ở từng node.

## 5. Paper, code tác giả và lựa chọn nhóm

| Nội dung | Paper | Code nhóm |
|---|---|---|
| Giới hạn δ | log₂(ω/η), mục 4.1 và Table 3 | log₄(n_eff/η), chặn 0 khi nhỏ |
| c ở công thức điểm | log₂(m/η), công thức (1) và Algorithm 4 | c_group như trên |
| Cập nhật/chấm | Algorithm 1: học → quên → chấm | Runner hiện tại: chấm lô → học/quên |
| Tách | Chọn q,p; sinh mẫu đều; khởi tạo con | Cùng cơ chế chính, thêm các xử lý biên |

Hàm `OnlineITree.get_random_path_length` trong code tác giả dùng mẫu số
`log(2 × branching_factor)`; cây nhị phân cho log₄. Nhóm theo lựa chọn này
cho hệ số/giới hạn, không nói nó trùng công thức in trong paper.

Mục 4.2 của paper suy ra độ sâu trung bình cây cân bằng
`floor(0.5 × log₂(ω/η) + 1)`. Đây là đại lượng phân tích dưới giả thiết cây
cân bằng; không tự đồng nhất nó với giới hạn độ sâu hay hệ số đã cài đặt.

Script tác giả xử lý cả lô trước khi quên phần dư; nhóm học/quên từng điểm bên
trong lô. Không gọi mọi khác biệt với code tác giả là lỗi so với giả mã paper.

## 6. Seed và phạm vi đánh giá đang chốt

Sau F4, run seed s được truyền trực tiếp vào Forest:
`tree_seed_i = s × n_trees + i`. Các runner lịch sử từng nhân s×32 bên ngoài
khi Forest còn dùng `seed+i`; sau F4 không được nhân thêm lần nữa.
Không đổi config của một run lịch sử để làm như nó đã chạy code mới.

- Stationary Phúc: warm-up 30%, chấm 70% còn lại trước khi học lô, 30 seed.
  Baseline sklearn 100 cây fit một lần trên warm-up rồi giữ cố định.
- Drift: 100 dòng đầu khởi động, 212.414 dòng được chấm trước học; 5 seed.
  d=10 và d=33 phải ghi rõ, không trộn các hàng.
- Cửa sổ học 2.048 khác cửa sổ đánh giá ROC-AUC 5.000, bước 1.000.
- Baseline cửa sổ của nhóm là sklearn tự bọc; nhãn lịch sử `asdifor` không
  xác nhận đó là implementation PySAD trong paper.

## Nguồn để rà và ghép slide

1. F. Leveni et al., “Online Isolation Forest,” ICML, PMLR 235, 2024,
   pp. 27288–27298: Algorithm 1–4, mục 4.1–4.2, Table 3.
   [Paper](https://proceedings.mlr.press/v235/leveni24a.html).
2. [Code tác giả, commit e528c86](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/e528c86b77219791d026d732f618efb0c7bde3c1).
3. Code nhóm: [forest.py](../src/oif/forest.py), [tree.py](../src/oif/tree.py),
   [scoring.py](../src/oif/scoring.py), [learning.py](../src/oif/learning.py).
4. [Stationary](../results/stationary.md), [drift d=33](../results/drift.md),
   [drift d=10](../results/drift-fixed-10.md).
