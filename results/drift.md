# Kết quả thí nghiệm concept drift trên INSECTS

> Cập nhật21/11: ZIP drift33 sauF4 đã bàn giao và upload10run. Dùng [báo cáo/nguồn run mới](drift33-f4.md) và [manifest](drift33-wandb-links.json) cho trạng thái W&B và thời gian lượt mới; nội dung bên dưới giữ lịch sử lượt trước.

**Trạng thái:** d = 33 chạy 5 seed (0–4) tại commit `fb35956` (đã có bản sửa F1 `6ac25e3`); kết quả thô trong `results/raw/drift-v2/` (Git bỏ qua), chưa tải lên W&B. d = 10 lấy từ [`drift-fixed-10.md`](drift-fixed-10.md) (5 seed, cùng `run.py`, sau sửa F1), mỗi run có link W&B. Bảng đầy đủ ở [`drift-by-segment.csv`](drift-by-segment.csv). Số liệu sinh bởi [`experiments/exp2_drift/plot_summary.py`](../experiments/exp2_drift/plot_summary.py).

Đối chiếu: ROC-AUC toàn luồng của 10 lần chạy d = 33 khớp [`drift-after-bootstrap.csv`](drift-after-bootstrap.csv), sai lệch lớn nhất 0.0e+00.

## Giao thức

- Dữ liệu `data/processed/insects.csv` (212.514 mẫu), giữ nguyên thứ tự dòng; không xáo trộn, không chia tập. Năm mốc thay đổi `51255, 74381, 100944, 142291, 152207` lấy từ script vẽ Hình 7 của tác giả (xem [`data/README.md`](../data/README.md)), chia luồng thành 6 đoạn.
- Đánh giá tuần tự **chấm điểm rồi mới học** (score-then-learn), theo lô 100. Lô đầu chỉ để khởi động; 212.414 mẫu còn lại được đánh giá. Nhãn chỉ dùng để tính chỉ số.
- OIF: 32 cây, `window_size = 2048`, `eta = 32`, seed rừng `seed * 32` để các seed không dùng chung cây (điểm F4 của `forest.py`).
- asdIFOR (nhóm tự dựng): `sklearn.ensemble.IsolationForest` 32 cây, `max_samples = 256`, huấn luyện lại trên 2048 mẫu gần nhất sau mỗi 2048 mẫu mới, giống ý tưởng cửa sổ rời của `pysad.IForestASD` mà tác giả dùng nhưng không phải cùng mã.
- Chỉ số: ROC-AUC, AP trên toàn luồng và từng đoạn; ROC-AUC trên cửa sổ trượt 5.000 mẫu, bước 1.000 (208 cửa sổ); thời gian học và chấm điểm (giây, CPU laptop, 1 luồng, các lần chạy d = 33 chạy tuần tự).
- Tiền xử lý: không có. Dùng nguyên CSV đã chuẩn bị, không chuẩn hóa/scaling, không điền khuyết, không xáo trộn, không bỏ dòng trùng; lượt d = 10 chỉ lấy 10 cột đầu `x0..x9`.
- Đo thời gian: `time.perf_counter` (giây, thời gian thực), đo tách riêng phần chấm điểm và phần học của từng lô rồi cộng dồn; không tính thời gian đọc dữ liệu và ghi tệp (ghi trong trường `preprocessing` và `timing` của `config.json`).

## Kết quả theo đoạn (d = 33, trung vị [Q1; Q3] qua 5 seed)

| Đoạn | `row_index` | Số mẫu | Bất thường | OIF ROC-AUC | asdIFOR ROC-AUC | OIF AP | asdIFOR AP | OIF giây | asdIFOR giây |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Toàn luồng | 100–212513 | 212414 | 5,51% | 0,706 [0,696; 0,744] | 0,718 [0,711; 0,718] | 0,104 | 0,097 | 182,9 | 10,2 |
| 1 | 0–51254 | 51155 | 4,67% | 0,774 [0,742; 0,813] | 0,794 [0,794; 0,797] | 0,116 | 0,110 | 43,9 | 3,1 |
| 2 | 51255–74380 | 23126 | 3,71% | 0,607 [0,586; 0,608] | 0,600 [0,599; 0,604] | 0,046 | 0,045 | 19,3 | 1,0 |
| 3 | 74381–100943 | 26563 | 8,62% | 0,741 [0,724; 0,789] | 0,744 [0,720; 0,755] | 0,198 | 0,169 | 22,5 | 1,2 |
| 4 | 100944–142290 | 41347 | 2,19% | 0,659 [0,633; 0,682] | 0,658 [0,654; 0,659] | 0,034 | 0,032 | 34,8 | 1,8 |
| 5 | 142291–152206 | 9916 | 30,57% | 0,665 [0,614; 0,716] | 0,664 [0,660; 0,680] | 0,420 | 0,391 | 8,8 | 0,4 |
| 6 | 152207–212513 | 60307 | 3,69% | 0,760 [0,749; 0,791] | 0,754 [0,744; 0,756] | 0,080 | 0,076 | 51,1 | 2,7 |

Thời gian theo đoạn là tổng thời gian chấm điểm và học của các lô bắt đầu trong đoạn. Mỗi đoạn chỉ ghi tổng này; thời gian học và chấm điểm tách riêng chỉ có ở cấp toàn luồng (xem CSV).

## ROC-AUC theo cửa sổ trượt

![ROC-AUC theo cửa sổ trượt trên INSECTS](../figures/drift-quality.png)

Đường đậm là trung vị qua 5 seed, vùng nhạt là Q1–Q3; vạch đỏ đứt là 5 mốc thay đổi. Mỗi điểm đặt ở tâm cửa sổ (`row_start + 2500`), theo mô tả ở Mục 5.3 của bài báo. Đây là hình do nhóm tạo, không phải hình trích từ bài báo.

## Đối chiếu d = 33 và d = 10 (toàn luồng, 5 seed mỗi cấu hình)

Script của tác giả chỉ dùng 10 đặc trưng đầu (`data[:, :10]`). Số d = 10 lấy từ [`drift-fixed-10.md`](drift-fixed-10.md); hai cấu hình dùng cùng `run.py`, cùng seed 0–4 và cùng cách cấp seed rừng (`seed * 32`), chỉ khác số cột.

| Mô hình | d = 33: ROC-AUC trung vị [Q1; Q3] | d = 33: min–max | d = 10: ROC-AUC trung vị [Q1; Q3] | d = 10: min–max | AP trung vị d = 33 | AP trung vị d = 10 |
|---|---:|---:|---:|---:|---:|---:|
| OIF | 0,706 [0,696; 0,744] | 0,645–0,748 | 0,728 [0,722; 0,788] | 0,691–0,830 | 0,104 | 0,120 |
| asdIFOR | 0,718 [0,711; 0,718] | 0,706–0,718 | 0,786 [0,785; 0,786] | 0,785–0,798 | 0,097 | 0,163 |

Theo từng seed (ROC-AUC toàn luồng; link W&B của lượt d = 10):

| Seed | OIF d = 33 | OIF d = 10 | asdIFOR d = 33 | asdIFOR d = 10 | W&B d = 10 |
|---:|---:|---:|---:|---:|---|
| 0 | 0,744 | 0,691 | 0,711 | 0,786 | [OIF](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/lpprt64h), [asdIFOR](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/pqz5mwjq) |
| 1 | 0,696 | 0,722 | 0,718 | 0,785 | [OIF](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5nsp99kc), [asdIFOR](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/8w9ds7kg) |
| 2 | 0,645 | 0,788 | 0,706 | 0,786 | [OIF](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/bkkazl0o), [asdIFOR](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/nijtz9s7) |
| 3 | 0,706 | 0,728 | 0,718 | 0,785 | [OIF](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zrvo8y72), [asdIFOR](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5b66rbfq) |
| 4 | 0,748 | 0,830 | 0,718 | 0,798 | [OIF](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/gq0qkj76), [asdIFOR](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zkiiyp3g) |

OIF: d = 10 cao hơn d = 33 ở 4/5 seed, khoảng min–max hai cấu hình chồng lên nhau; asdIFOR: d = 10 cao hơn d = 33 ở 5/5 seed, khoảng min–max hai cấu hình tách rời. Khoảng tách rời nghĩa là chênh lệch lớn hơn dao động theo seed quan sát được; với 5 seed đây vẫn là quan sát, chưa phải kiểm định. Lượt d = 10 không ghi kết quả theo đoạn và không so thời gian (các run OIF chạy đồng thời); phân tích phục hồi sau từng mốc của d = 10 nằm ở [`drift-fixed-10.md`](drift-fixed-10.md).

## Nhận xét

**Sụt giảm và phục hồi qua các mốc.** Thay đổi ROC-AUC trung vị từ đoạn trước sang đoạn sau mỗi mốc (d = 33):

| Mốc | Đoạn | OIF | asdIFOR |
|---|---|---:|---:|
| 51255 | 1 → 2 | -0,167 | -0,194 |
| 74381 | 2 → 3 |  0,134 | 0,143 |
| 100944 | 3 → 4 | -0,082 | -0,085 |
| 142291 | 4 → 5 |  0,006 | 0,005 |
| 152207 | 5 → 6 |  0,095 | 0,090 |

Hai mô hình thay đổi cùng chiều ở 5/5 mốc, phù hợp với nhận định ở Mục 5.3 rằng các thuật toán bị ảnh hưởng tương tự bởi thay đổi đột ngột. Trên đường cửa sổ trượt, điểm thấp nhất của OIF là 0,551 (tâm cửa sổ 70600) và của asdIFOR là 0,524 (tâm 70600). Cả hai đều chỉ nhớ 2048 mẫu gần nhất, nên sau mỗi mốc cần khoảng một cửa sổ học để thay toàn bộ mẫu cũ; cửa sổ đánh giá 5.000 mẫu làm mượt thêm nên đường cong không đổi tức thời tại vạch đỏ.

**Phương sai theo seed.** ROC-AUC toàn luồng của OIF nằm trong [0,645; 0,748] (IQR 0,048), của asdIFOR trong [0,706; 0,718] (IQR 0,007). Đoạn dao động mạnh nhất của OIF là đoạn 5 (0,536–0,745), của asdIFOR là đoạn 6 (0,722–0,763). Giả thuyết (chưa kiểm chứng): OIF dao động lớn hơn vì cấu trúc cây phụ thuộc chuỗi phép tách ngẫu nhiên tích lũy suốt luồng (mỗi lần tách còn sinh mẫu ảo), trong khi asdIFOR dựng lại toàn bộ rừng sau mỗi 2048 mẫu. Với 5 seed, chênh lệch trung vị toàn luồng giữa hai mô hình (0,012) nhỏ hơn khoảng dao động của OIF (0,103), nên chưa đủ cơ sở để nói mô hình nào tốt hơn trên INSECTS.

**Thời gian: Python thuần so với Cython.** Trung vị tổng thời gian là 182,9 giây với OIF (~861 µs/mẫu; học 131,5 giây, chấm điểm 51,4 giây) và 10,2 giây với asdIFOR, tức OIF chậm hơn khoảng 18 lần. Kết quả này ngược với Mục 5.3 (oIFOR nhanh nhất) và chủ yếu do cách cài đặt, không phải do độ phức tạp thuật toán:
- OIF của nhóm viết bằng Python thuần: mỗi mẫu đi qua vòng lặp Python trên 32 cây để học, và thêm một lần quên khi cửa sổ đầy. Mã của tác giả cũng là Python thuần.
- asdIFOR của nhóm gọi scikit-learn, nơi phần dựng và duyệt cây viết bằng Cython, và chỉ huấn luyện lại 120 lần trên toàn luồng; chấm điểm được vector hóa theo lô 100.
- Tác giả chạy asdIFOR qua `pysad`, với giao diện xử lý từng mẫu, nên số thời gian trong bài báo không so trực tiếp được với baseline của nhóm.

## Khác biệt so với bài báo và mã tác giả

- Bài báo chạy 30 lần; nhóm chạy 5 seed cho mỗi cấu hình d = 33 và d = 10.
- Mã tác giả học mỗi lô trước khi chấm điểm lô đó, nên điểm của một mẫu đã dùng chính mẫu đó; nhóm chấm điểm trước khi học. Mã tác giả cũng có thêm holdout ngẫu nhiên 10%, nhóm không dùng.
- Mã tác giả chỉ dùng 10 đặc trưng; bài báo ghi d = 33. Bảng theo đoạn và hình ở đây dùng d = 33; kết quả d = 10 (có W&B) ở [`drift-fixed-10.md`](drift-fixed-10.md).
- Hình của nhóm dùng bước cửa sổ 1.000 và đặt điểm ở tâm cửa sổ; script vẽ của tác giả dùng bước 10 và co giãn chỉ số đầu cửa sổ theo độ dài luồng.
- Không chép số liệu bài báo; Hình 7 không có bảng số nên chỉ so được về hình dạng.

## Tệp kết quả

- `results/raw/drift-v2/<model>_seed<s>/` (d = 33): `config.json`, `metrics.json`, `predictions.csv` (cột `row_index, segment, label, anomaly_score`).
- [`drift-by-segment.csv`](drift-by-segment.csv): trung vị, Q1, Q3, min, max của ROC-AUC, AP, `learn_seconds`, `score_seconds`, `total_seconds` theo `n_features`, mô hình và phạm vi (`all`, `segment_1`…`segment_6`; d = 10 chỉ có `all`). Ô trống là chỉ số không được ghi cho phạm vi đó.
- [`../figures/drift-quality.png`](../figures/drift-quality.png).

## Tải kết quả d = 33 lên W&B

Lượt d = 10 đã có link W&B (xem [`docs/wandb-runs.md`](../docs/wandb-runs.md)). Lượt d = 33 chưa tải. Cần cài phần phụ thuộc W&B (`python -m pip install -e .[wandb]`), đăng nhập (`wandb login`) và đặt `WANDB_PROJECT`/`WANDB_ENTITY`; không đưa khóa API vào Git. Dùng script tải của nhóm, không chạy lại mô hình:

```powershell
python experiments/exp2_drift/upload_runs.py results/raw/drift-v2 --manifest results/raw/drift-v2/wandb-links.json
```

Script ghi URL từng run vào manifest; sau đó bổ sung các URL vào mục Trạng thái và `docs/wandb-runs.md`.
