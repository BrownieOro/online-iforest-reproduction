# Đối chiếu stationary: paper và nhóm

Số liệu paper lấy từ Bảng 4a/4b; số liệu nhóm là một lần chạy seed 42 trên bản dữ liệu đã chuẩn bị. Thời gian không so sánh tuyệt đối vì protocol paper đo toàn luồng còn nhóm đo fit + score trên holdout.

| Dataset | Paper ROC-AUC (oIFOR) | Nhóm ROC-AUC | Độ lệch tương đối | Thời gian nhóm (s) | W&B |
|---|---:|---:|---:|---:|---|
| Annthyroid | 0.685 | 0.8212 | +19.89% | 0.347 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/z86dyqji) |
| Mammography | 0.854 | 0.8624 | +0.99% | 0.236 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/judihdbh) |

## Giải thích sai lệch

- Nhóm dùng sklearn IsolationForest làm baseline offline holdout, không phải code oIF tác giả; paper báo oIFOR trên protocol streaming và tổng hợp nhiều lần chạy.
- Khác biệt về cách chia train/test, contamination, số lần chạy, phiên bản thư viện và thời gian đo có thể làm ROC-AUC/thời gian khác paper.
- Bảng này là baseline đối chiếu, chưa phải tuyên bố tái lập OIF. Khi runner OIF hoàn chỉnh, bổ sung dòng OIF nhóm với cùng protocol streaming.
