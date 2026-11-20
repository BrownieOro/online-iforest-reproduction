# Kết quả thí nghiệm dữ liệu ổn định

**Thực hiện:** 2 bộ dữ liệu × 2 phương pháp × 30 seed (0–29) = 120 run. Mỗi run có
`config.json`, `metrics.json` và `predictions.csv`; tổng cộng 120 tệp của mỗi loại
được lưu tại [`results/raw/stationary-seedblock/`](raw/stationary-seedblock/).
Thư mục kết quả thô được Git bỏ qua. Bảng tổng hợp có tại
[`stationary-summary.csv`](stationary-summary.csv); số liệu từng seed nằm trong
`results/raw/stationary-seedblock/runs.csv`.

<!-- W&B status begin -->
**W&B:** 0/120 run được tải lên. Lúc hoàn tất các lượt chạy, chưa có tài khoản/API
key W&B để xác thực. Các tệp kết quả vẫn được lưu cục bộ.
<!-- W&B status end -->

Các `config.json` ghi Git commit `32d594f47fb7ada4b0cf478ec6b6b783dff9ef7d`,
chứa L1 (`ceeaed8`) và F1 (`6ac25e3`), cùng `git_worktree_dirty=true`. Seed cây
OIF cho run seed `s` nằm trong khoảng `32 × s` đến `32 × s + 31`; các khoảng
seed của 30 run không giao nhau.

## Giao thức

Mỗi seed tạo một hoán vị mẫu dùng chung cho Online Isolation Forest (OIF) và
Isolation Forest của scikit-learn. 30% đầu làm warm-up; phần còn lại được chấm
theo lô 100 mẫu. OIF chấm điểm trước rồi cập nhật từng lô, dùng 32 cây, cửa sổ
`ω=2048` và `η=32`. Seed rừng OIF là `32 × seed`; cây thứ `i` dùng seed
`32 × seed + i`. Baseline scikit-learn dùng 100 cây, fit một lần trên warm-up
và giữ cố định. Nhãn chỉ được dùng để tính ROC-AUC và average precision (AP).

| Bộ dữ liệu | Tổng dòng | Warm-up | Dòng được chấm mỗi seed | Seed |
|---|---:|---:|---:|---:|
| Annthyroid | 7.200 | 2.160 | 5.040 | 30 |
| Mammography | 11.183 | 3.354 | 7.829 | 30 |

## Kết quả tổng hợp

Các giá trị là trung vị qua 30 seed; ROC-AUC có kèm Q1 và Q3. Thời gian là tổng
fit/cập nhật và chấm điểm, đơn vị giây.

| Bộ dữ liệu | Phương pháp | Run | ROC-AUC median [Q1; Q3] | AP median | Tổng thời gian median (s) | W&B (đã tải/tổng) |
|---|---|---:|---:|---:|---:|---:|
| Annthyroid | OIF | 30 | 0,7468 [0,7117; 0,7928] | 0,2757 | 15,0283 | 0/30 |
| Annthyroid | Isolation Forest (scikit-learn) | 30 | 0,8187 [0,8044; 0,8338] | 0,3077 | 0,4776 | 0/30 |
| Mammography | OIF | 30 | 0,8805 [0,8675; 0,8913] | 0,2344 | 34,4144 | 0/30 |
| Mammography | Isolation Forest (scikit-learn) | 30 | 0,8633 [0,8517; 0,8698] | 0,1920 | 0,5987 | 0/30 |

## Chênh lệch giữa hai phương pháp

- **Annthyroid:** ROC-AUC OIF thấp hơn 0,0719 (0,7468 so với 0,8187); AP thấp hơn
  0,0320 (0,2757 so với 0,3077). Tổng thời gian trung vị là 15,0283 giây với OIF
  và 0,4776 giây với baseline.
- **Mammography:** ROC-AUC OIF cao hơn 0,0173 (0,8805 so với 0,8633); AP cao hơn
  0,0424 (0,2344 so với 0,1920). Tổng thời gian trung vị là 34,4144 giây với OIF
  và 0,5987 giây với baseline.

OIF cập nhật 32 cây xuyên suốt phần đánh giá; baseline chỉ fit trên warm-up rồi
giữ cố định. Các thời gian trên đo hai quy trình này.

## Đối chiếu Bảng 4 của bài báo

Bảng 4 báo ROC-AUC oIFOR là 0,685 trên Annthyroid và 0,854 trên Mammography.
ROC-AUC OIF của nhóm lần lượt là 0,7468 và 0,8805, tương ứng chênh +0,0618
(+9,02%) và +0,0265 (+3,10%) so với các mốc đó. Protocol nhóm dùng warm-up 30%
và baseline ngoại tuyến cố định; bài báo đánh giá trên toàn luồng và so sánh năm
phương pháp trực tuyến. Tệp Annthyroid nhóm dùng có 7.200 dòng, trong khi Bảng 4
báo 6.832 dòng.

## Thống kê bộ dữ liệu

| Bộ dữ liệu | Tệp nhóm | Nhãn bất thường trong tệp nhóm | Bài báo |
|---|---:|---:|---:|
| Annthyroid | 7.200 dòng, 6 đặc trưng | 534/7.200 (7,42%) | 6.832 dòng, 7% |
| Mammography | 11.183 dòng, 6 đặc trưng | 260/11.183 (2,32%) | 11.183 dòng, 2% |

Tệp Annthyroid lấy từ kho dữ liệu Online Isolation Forest [6]. Script xác minh
SHA-256, bỏ cột ID và giữ 7.200 dòng. Trong tệp có 138 dòng trùng theo đặc trưng
và nhãn. UCI ghi bộ ANN gồm 3.772 dòng train và 3.428 dòng test, tổng 7.200 [3];
OpenML cũng ghi tổng 7.200 [4]. Liu et al. (2008) và Leveni et al. (2024) ghi số
6.832 và tỷ lệ 7% [1], [2]. Azzari và Bicego (2024) ghi họ không khôi phục được
phiên bản 6.832; bản web có 7.200 dòng và nghiên cứu của họ báo tỷ lệ outlier 2%
trên bản này [5]. Tệp Mammography của nhóm có 260 nhãn bất thường, tương ứng
2,32%.

## Chi tiết triển khai

Giới hạn độ sâu tính theo số mẫu hiệu dụng `n_eff` trong cửa sổ: `δ=0` khi
`n_eff≤η`; còn lại `δ=ln(n_eff/η)/ln(4)`. Khi cửa sổ đầy (`n_eff=ω=2048`), `δ=3`.
Khi tách lá, code nhóm lấy `node.mass` mẫu ảo đều trong miền bao và dùng chúng
để khởi tạo mass hai node con. Phần 4.1 của bài báo ghi `h`, còn chú thích Hình 2
ghi `ĥ`; code nhóm dùng `h`.

Hai biểu đồ thể hiện trung vị và Q1–Q3 qua 30 seed:
[ROC-AUC](../figures/stationary-auc.png) ·
[thời gian xử lý](../figures/stationary-time.png).

## Nguồn

1. F. Leveni, G. Weigert Cassales, B. Pfahringer, A. Bifet, and G. Boracchi,
   “Online Isolation Forest,” *Proc. 41st Int. Conf. Machine Learning*, PMLR 235,
   pp. 27288–27298, 2024, [PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/leveni24a/leveni24a.pdf).
2. F. T. Liu, K. M. Ting, and Z.-H. Zhou, “Isolation Forest,” *Proc. 8th IEEE Int.
   Conf. Data Mining*, pp. 413–422, 2008,
   [DOI](https://doi.org/10.1109/ICDM.2008.17).
3. UCI Machine Learning Repository, [Thyroid Disease, dataset 102](https://archive.ics.uci.edu/dataset/102/thyroid%2Bdisease).
4. OpenML, [Annthyroid, dataset 40886](https://www.openml.org/search?id=40886&sort=runs&type=data).
5. A. Azzari and M. Bicego, “An Empirical Characterization of the Stability of
   Isolation Forest Results,” *Proc. Joint IAPR Int. Workshops S+SSPR*, pp. 166–176,
   2024, [DOI](https://doi.org/10.1007/978-3-031-80507-3_17).
6. F. Leveni, [Online-Isolation-Forest source code](https://github.com/ineveLoppiliF/Online-Isolation-Forest/blob/main/OnlineIForest/onlineitree.py).
