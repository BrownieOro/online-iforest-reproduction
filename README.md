# Online Isolation Forest

Repo đồ án Nhập môn Học máy, nghiên cứu bài **Online Isolation Forest (ICML 2024)**.

## Cấu trúc repo

```text
online-iforest-reproduction/
├── README.md                         Sơ đồ và hướng dẫn tìm file
├── .gitignore                        Bỏ qua môi trường, khóa và dữ liệu lớn
├── .gitattributes                    Quy định định dạng file trong Git
│
├── papers/                           Tài liệu bài báo
│   ├── leveni24a-original.pdf         Paper gốc tiếng Anh
│   ├── online-isolation-forest-vi.md  Bản dịch tiếng Việt
│   ├── CITATION.bib                   Thông tin trích dẫn
│   ├── NOTICE.md                      Nguồn và ghi công tài liệu
│   └── figures/                      Hình gốc để đọc đối chiếu
│
├── docs/                             Tài liệu học và yêu cầu môn
│   ├── bat-dau-o-day.md               Giải thích pipeline bằng tiếng Việt
│   ├── ghi-chu-doi-chieu.md           Chi tiết cần kiểm tra khi triển khai
│   ├── yeu-cau-do-an.md               Yêu cầu đồ án
│   ├── checklist-nop-bai.md           Danh sách kiểm tra trước khi nộp
│   ├── tai-nguyen.md                  Link tài liệu, code và dữ liệu tham khảo
│   └── requirements/                 Bản lưu các nguồn yêu cầu
│
├── model/                            Thuật toán chung do nhóm tự viết
├── data/                             Code và hướng dẫn chuẩn bị dữ liệu
├── experiments/                      Code chạy từng thí nghiệm
│   ├── exp1_stationary/              Thí nghiệm dữ liệu ổn định
│   ├── exp2_drift/                   Thí nghiệm dữ liệu thay đổi theo thời gian
│   └── exp3_window/                  Phân tích kích thước cửa sổ
├── results/                          Bảng kết quả nhóm tự chạy
├── figures/                          Biểu đồ và hình nhóm tự tạo
└── slides/                           Nội dung trình bày
    └── README.md                     Link outline trên Google Docs; nơi đặt PPTX cuối
```

Baseline sklearn đã chạy được trong `src/oif/`; OIF hiện chỉ có API scaffold, chưa triển khai thuật toán. `papers/figures/` chứa hình của tác giả; `figures/` dành cho hình nhóm tự tạo.

## Mở nhanh

- [Paper gốc](papers/leveni24a-original.pdf) · [Bản dịch tiếng Việt](papers/online-isolation-forest-vi.md)
- [Giải thích pipeline](docs/bat-dau-o-day.md) · [Yêu cầu đồ án](docs/yeu-cau-do-an.md)
- [Outline slide và deadline trên Google Docs](https://docs.google.com/document/d/1BXscOQX-TQZYzKy0HOXoMgYcpc5V_lgIFqZvYFJ9c1g/edit?tab=t.pdo9d2xfspft)
- [Kế hoạch và phân việc trên Google Docs](https://docs.google.com/document/d/1BXscOQX-TQZYzKy0HOXoMgYcpc5V_lgIFqZvYFJ9c1g/edit?tab=t.eimsvhhx7ipi)

Nguồn bài: [PMLR](https://proceedings.mlr.press/v235/leveni24a.html) · [Repo tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest). Xem [ghi công tài liệu](papers/NOTICE.md).

## Chạy baseline ngay (Python >=3.9)

Windows PowerShell, tại thư mục repo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -m pytest -q
python scripts/run_baseline.py --output results/raw/smoke-42
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cp .env.example .env
python -m pytest -q
python scripts/run_baseline.py --output results/raw/smoke-42
```

Không truyền `--data`: synthetic 1.000 dòng, 4 chiều, 10% bất thường dễ phân biệt,
seed 42; đây là smoke test pipeline, không phải tái lập kết quả paper.
Mỗi lần chạy dùng thư mục output mới; code từ chối ghi đè thư mục đã tồn tại.
Hai entry point tương đương: `python -m oif.baseline` và `oif-baseline`.

### Dataset và input/output

```bash
python scripts/run_baseline.py --data data/raw/dataset.csv --label-column label --seed 42 --contamination 0.1 --output results/raw/dataset-42
```

CSV có header; mỗi hàng một mẫu, các cột feature là số. Bỏ ID/timestamp/text trước
khi chạy. Nhãn tùy chọn: `0=normal, 1=anomaly`; bỏ `--label-column` nếu không có nhãn.
Nếu file có nhãn mà không khai báo, cột đó sẽ bị coi là feature: phải khai báo đúng.
NaN feature được điền median từ train; từ chối infinity, cột train toàn NaN và nhãn sai.
Random holdout 70/30 (stratify nếu nhãn có hai lớp); không dùng nhãn để fit mô hình
hoặc chọn contamination. Median + StandardScaler chỉ fit train. Seed điều khiển split và model.
Dataset quá ít mẫu mỗi lớp có thể không stratify được: cần bổ sung dữ liệu.

Output: `config.json` (tham số, features, SHA256 CSV, phiên bản thư viện),
`metrics.json` (ROC-AUC, average precision, precision/recall/F1, thời gian fit/score),
`predictions.csv` (row_index gốc tính từ 0, anomaly_score, prediction 0/1, label nếu có).
AUC/AP là null nếu thiếu nhãn hoặc test chỉ có một lớp; không bịa metric.
`anomaly_score=-sklearn.score_samples`: càng cao càng bất thường; prediction dùng
ngưỡng của model với contamination cố định từ CLI, không tune bằng test.
Nguồn quy ước sklearn: [IsolationForest API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html).
Baseline này là offline holdout; không dùng làm đánh giá stream/drift hoặc tuyên bố tái lập paper.

### W&B dùng ở đâu?

Mọi runner gọi chung `src/oif/tracking.py::log_run(config, metrics, output)` sau khi
đã lưu local. Mặc định `WANDB_MODE=disabled`: không cần W&B hay tài khoản.
Muốn thử offline: `python -m pip install -e ".[wandb]"`, sửa `.env` thành
`WANDB_MODE=offline`. Muốn upload: chọn `online`, cấu hình project/entity và
`WANDB_API_KEY` riêng trong `.env`. Không đưa khóa vào Git. Biến môi trường hiện có
ưu tiên hơn `.env`; chạy lệnh từ gốc repo. Offline lưu trong `wandb/`, có thể sync
bằng `wandb sync <thu-muc-run>` khi có tài khoản.
W&B nhận config, metric số và artifact chứa ba file output; không upload dataset gốc.
Lỗi W&B làm lệnh báo lỗi, nhưng file local vẫn được giữ. Chưa cần W&B để chạy baseline.

| Experiment | Script / API | Input → output | W&B |
|---|---|---|---|
| Synthetic smoke | `scripts/run_baseline.py` | synthetic → JSON + predictions CSV | job baseline, optional |
| Dataset baseline | cùng script + `--data --label-column` | CSV → holdout metrics + predictions | config/metrics/artifact |
