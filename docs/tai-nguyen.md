# Tài nguyên của nhóm

## Đọc theo thứ tự

1. [Giải thích tiếng Việt cho người mới](bat-dau-o-day.md).
2. [Bản dịch bài](../papers/online-isolation-forest-vi.md) và [PDF gốc](../papers/leveni24a-original.pdf).
3. [Trang xuất bản PMLR](https://proceedings.mlr.press/v235/leveni24a.html).
4. [README repo tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest#readme).
5. [Ví dụ nhỏ của tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest/blob/main/Online-iForest_demo.py).

## Code, dữ liệu và đối chiếu

| Nguồn | Dùng làm gì |
|---|---|
| [Thuật toán gốc](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/main/OnlineIForest) | Đọc và chạy đối chứng với bản nhóm tự viết |
| [Dữ liệu tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/main/datasets) | Tìm đúng phiên bản dữ liệu dùng trong bài |
| [Script thí nghiệm](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/main/experiments/scripts/test) | Kiểm tra cấu hình, thứ tự xử lý và cách đánh giá |
| [Script vẽ hình](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/main/experiments/scripts/plot) | Đối chiếu cách tổng hợp kết quả |
| [Kết quả gốc](https://github.com/ineveLoppiliF/Online-Isolation-Forest/tree/main/experiments/results) | Đối chiếu số liệu, không dùng làm kết quả nhóm |
| [Thư viện gốc yêu cầu](https://github.com/ineveLoppiliF/Online-Isolation-Forest/blob/main/requirements.txt) | Kiểm tra môi trường trước khi chạy |
| [PySAD](https://pysad.readthedocs.io/en/latest/) | Các phương pháp so sánh; kiểm tra phiên bản với repo gốc |
| [Git LFS](https://git-lfs.com/) | Repo gốc có dùng tệp lớn; đọc lưu ý README trước khi tải |

README tác giả lưu ý chỉnh wrapper PySAD của Isolation Forest-ASD để truyền số cây. Kiểm tra đúng phiên bản trước khi áp dụng thay đổi, không sửa mù theo tài liệu cũ.

## Kiến thức và công cụ hỗ trợ

- [Isolation Forest cơ bản](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html).
- [ROC AUC trong scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html).
- [Bắt đầu lưu kết quả W&B](https://github.com/wandb/wandb#quickstart).
- [Ví dụ phát hiện bất thường CapyMOA](https://capymoa.org/notebooks/anomaly_detection.html).
- [Online Isolation Forest trong CapyMOA](https://capymoa.org/api/modules/capymoa.anomaly.OnlineIsolationForest.html).

Các đường dẫn tham khảo được tổng hợp ngày 31/10/2026. Đây không phải danh sách thư viện nhóm đã cài hoặc đã kiểm chứng tương thích.
