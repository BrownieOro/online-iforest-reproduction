"""Summarize five-seed INSECTS runs without mixing models or protocol versions."""
import json
import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / 'results/raw/tran-fixed-10'


def main():
    links = json.loads((RUNS / 'wandb-links.json').read_text(encoding='utf-8'))
    rows = []
    for model in ('oif', 'asdifor'):
        for seed in range(5):
            name = f'{model}_seed{seed}'
            config = json.loads((RUNS / name / 'config.json').read_text(encoding='utf-8'))
            m = json.loads((RUNS / name / 'metrics.json').read_text(encoding='utf-8'))
            if config['n_features'] != 10 or not config['git_commit'].startswith('6ac25e3'):
                raise ValueError(f'Unexpected configuration: {name}')
            rows.append((name, m, links[name]))
    lines = ['# INSECTS — 10 đặc trưng, năm seed sau sửa warm-up', '',
             '212.514 dòng theo thứ tự gốc; 100 dòng đầu khởi động, 212.414 dòng chấm trước học. '
             '32 cây, cửa sổ học 2.048, η=32, lô 100; ROC-AUC trượt 5.000, bước 1.000. '
             'Hai phương pháp cùng dữ liệu, nhưng baseline là sklearn dựng lại theo cửa sổ, '
             'không phải PySAD của tác giả.', '',
             '| Run | ROC-AUC | Average precision | W&B |', '|---|---:|---:|---|']
    for name, m, url in rows:
        lines.append(f'| {name} | {m["roc_auc"]:.6f} | {m["average_precision"]:.6f} | [run]({url}) |')
    lines += ['', '## Tổng hợp', '']
    for model in ('oif', 'asdifor'):
        metrics = [m for name, m, _ in rows if name.startswith(model + '_')]
        auc = np.array([m['roc_auc'] for m in metrics])
        ap = np.array([m['average_precision'] for m in metrics])
        lines.append(f'- {model}: ROC-AUC trung vị {np.median(auc):.6f}, '
                     f'Q1–Q3 [{np.quantile(auc,.25):.6f}; {np.quantile(auc,.75):.6f}]; '
                     f'AP trung vị {np.median(ap):.6f}.')
    with (ROOT / 'results/recovery-fixed-10.csv').open(encoding='utf-8', newline='') as f:
        recovery = list(csv.DictReader(f))
    lines += ['', '## Phục hồi OIF', '',
              'Ngưỡng là AUC cửa sổ hoàn chỉnh cuối trước mốc; phục hồi là cửa sổ hoàn chỉnh '
              'sau mốc đầu tiên đạt lại ngưỡng trước mốc tiếp theo. Độ trễ tính đến cuối cửa '
              'sổ, bao gồm tích lũy 5.000 mẫu; không phải độ trễ thích nghi tức thời.', '',
              '| Mốc | AUC trước, trung vị | AUC cửa sổ đầu sau, trung vị | Số seed phục hồi | Độ trễ trung vị khi phục hồi |',
              '|---:|---:|---:|---:|---:|']
    for cp in (51255, 74381, 100944, 142291, 152207):
        group = [r for r in recovery if r['model'] == 'oif' and int(r['change']) == cp]
        before = np.median([float(r['baseline_auc']) for r in group])
        after = np.median([float(r['first_post_auc']) for r in group])
        delays = [int(r['delay_samples']) for r in group if r['delay_samples']]
        delay = f'{np.median(delays):,.0f}' if delays else 'chưa quan sát'
        lines.append(f'| {cp:,} | {before:.3f} | {after:.3f} | {len(delays)}/5 | {delay} |')
    lines += ['', '![ROC-AUC theo năm seed](../figures/drift-recovery-fixed-10.png)',
              '', 'Phân bố điểm trước/sau mốc đầu theo từng nhãn: '
              '[hình seed 0](../figures/drift-score-distribution-fixed-10.png); '
              'mỗi lớp chuẩn hóa riêng, không thể hiện tỷ lệ lớp.']
    lines += ['', 'Không so thời gian giữa các phương pháp vì các run OIF được chạy đồng thời. '
              'Paper Hình 7 báo trung vị 30 lần và dùng cửa sổ 5.000 mẫu; script tác giả '
              'học trước khi chấm, còn nhóm chấm trước học. Mô tả paper ghi 33 đặc trưng '
              'nhưng script tác giả dùng 10 cột đầu. Không so trực tiếp chênh lệch phần trăm.',
              '', 'Giới hạn độ sâu: Table 3 paper ghi log₂(ω/η), code tác giả và code nhóm '
              'dùng log₄(ω/η) cho cây nhị phân. Xem [phân tích phương pháp](drift-analysis-10.md).', '']
    (ROOT / 'results/drift-fixed-10.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
