# Công thức OIF dùng trong bản nhóm

Tài liệu này chốt quy ước để `tree.py`, `scoring.py` và `forest.py` dùng cùng một cách tính.

## Ký hiệu và quy ước

- `eta`: ngưỡng khối lượng để một ô ở độ sâu `k` được tách, ngưỡng là `eta * 2**k`.
- `h`: khối lượng ô lá; `k`: độ sâu ô. Hai đại lượng này không thay thế nhau.
- `n_eff`: số mẫu đang nằm trong cửa sổ sau học/quên.
- `D_i(x)`: độ sâu đã hiệu chỉnh của mẫu `x` trong cây `i`.
- `tau`: số cây; `s(x)`: điểm bất thường, cao hơn nghĩa là bất thường hơn.

Bản nhóm dùng quy ước của code tác giả cho cây nhị phân:

```text
C(m, eta) = 0                         nếu m <= eta
C(m, eta) = ln(m / eta) / ln(4)       nếu m > eta
D_i(x) = k_i(x) + C(h_i(x), eta)
c = C(n_eff, eta)
s(x) = 2 ** (-mean_i(D_i(x)) / (c + eps))
```

`eps = np.finfo(float).eps` chỉ tránh chia cho 0. Khi `n_eff <= eta`, điểm thuộc giai đoạn khởi động; không diễn giải nó là xác suất.

Paper ghi `c(omega, eta) = log2(omega / eta)` ở phương trình (1), trong khi code tác giả dùng `ln(m/eta)/ln(4)` cho cây nhị phân. Bản nhóm bám code tham chiếu và ghi khác biệt này trong slide.

## Trường hợp biên

- Forest chưa học: `score_samples` báo `ValueError`.
- `m <= eta`: hiệu chỉnh bằng 0.
- `m < 0`, `eta <= 0`, độ sâu không hữu hạn hoặc đầu vào có NaN/infinity: báo lỗi.
- Chấm điểm chỉ đọc trạng thái, không học/quên và không đổi cửa sổ.

## Ví dụ kiểm tra tay

Với `eta=32`, `n_eff=2048`, `c=log4(64)=3`. Nếu ba cây trả độ sâu `[2,3,4]`, trung bình là `3` và điểm là `0.5`. Nếu trung bình là `2`, điểm là `2**(-2/3)`, cao hơn nên bất thường hơn.

Nguồn: Leveni et al., *Online Isolation Forest*, ICML 2024, phương trình (1), Thuật toán 4 và mục 4.2; code tác giả tại commit `e528c86b77219791d026d732f618efb0c7bde3c1`.
