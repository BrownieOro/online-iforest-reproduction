"""Upload completed local drift runs and their rolling-AUC chart to W&B."""
import argparse
import json
import os
from pathlib import Path

import wandb


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir', type=Path)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    links = json.loads(args.manifest.read_text(encoding='utf-8')) if args.manifest.exists() else {}
    paths = sorted(args.run_dir.glob('*_seed*/metrics.json'))
    for path in paths:
        folder = path.parent
        if folder.name in links:
            continue
        config = json.loads((folder / 'config.json').read_text(encoding='utf-8'))
        metrics = json.loads(path.read_text(encoding='utf-8'))
        with wandb.init(project=os.environ.get('WANDB_PROJECT', 'intro-ml-oif'),
                        entity=os.environ.get('WANDB_ENTITY'), job_type='drift_prequential',
                        tags=config.get('tags', []), config=config) as run:
            scalars = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
            window = metrics['sliding_window']
            rows = [[start + window['size'] / 2, auc] for start, auc in
                    zip(window['row_start'], window['roc_auc']) if auc is not None]
            table = wandb.Table(columns=['stream_position', 'roc_auc'], data=rows)
            scalars['rolling_roc_auc'] = wandb.plot.line(table, 'stream_position', 'roc_auc',
                                                       title='Rolling ROC-AUC')
            run.log(scalars)
            artifact = wandb.Artifact(f'drift-prequential-{run.id}', type='evaluation')
            for name in ('config.json', 'metrics.json', 'predictions.csv'):
                artifact.add_file(str(folder / name))
            run.log_artifact(artifact)
            url = run.url
        links[folder.name] = url
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(links, indent=2), encoding='utf-8')
        print(folder.name, url, flush=True)


if __name__ == '__main__':
    main()
