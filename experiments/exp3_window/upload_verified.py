"""Upload audited group results; persistent unique IDs prevent accidental duplicates."""
import os,json,hashlib,argparse
from pathlib import Path
import wandb
HOST='https://api.forge.coreweave.com'
ENTITY='24122055-university-of-science-viet-nam-national-univer'
PROJECT='intro-ml-oif'
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True); p.add_argument('--kind',choices=['drift33','window'],required=True); args=p.parse_args()
os.environ['WANDB_BASE_URL']=HOST
if not wandb.Api(overrides={'base_url':HOST}).api_key:
    raise SystemExit('W&B login required. No credentials found; no runs created.')
manifest=HERE/(args.kind+'-wandb-links.json')
links=json.loads(manifest.read_text()) if manifest.exists() else {}
paths=sorted(args.root.rglob('metrics.json'))
expected=10 if args.kind=='drift33' else 4
if len(paths)!=expected: raise ValueError(f'Expected {expected} runs; found {len(paths)}')
for path in paths:
    folder=path.parent
    c=json.loads((folder/'config.json').read_text()); m=json.loads(path.read_text())
    fingerprint=hashlib.sha256(b''.join((folder/n).read_bytes() for n in ['config.json','metrics.json','predictions.csv'])).hexdigest()
    key=f"{args.kind}/{folder.relative_to(args.root).as_posix()}"
    if key in links:
        if links[key]['sha256']!=fingerprint: raise ValueError('Artifacts changed after upload')
        continue
    w=c['params']['window_size']
    run_id=hashlib.sha256((key+fingerprint).encode()).hexdigest()[:16]
    with wandb.init(entity=ENTITY,project=PROJECT,id=run_id,resume='allow',name=f"{args.kind}-{c['model']}-w{w}-seed{c['seed']}",config=c,tags=[*c.get('tags',[]),args.kind,'after-bootstrap','after-F4'],job_type='completed-result-upload',mode='online',settings=wandb.Settings(init_timeout=120)) as run:
        scalars={k:v for k,v in m.items() if isinstance(v,(int,float))}
        win=m['sliding_window']
        data=[[a+win['size']/2,b] for a,b in zip(win['row_start'],win['roc_auc']) if b is not None]
        table=wandb.Table(columns=['stream_position','roc_auc'],data=data)
        scalars['rolling_roc_auc']=wandb.plot.line(table,'stream_position','roc_auc',title='Rolling ROC-AUC')
        run.log(scalars)
        run.summary.update({k:v for k,v in m.items() if isinstance(v,(int,float))})
        art=wandb.Artifact(f'{args.kind}-{run_id}',type='evaluation',metadata={'source_files_sha256':fingerprint})
        for name in ['config.json','metrics.json','predictions.csv']: art.add_file(str(folder/name))
        run.log_artifact(art).wait()
        url=run.url
    # Fetch completed run back: only record URL if server has accepted artifacts.
    remote=wandb.Api(overrides={'base_url':HOST}).run(f'{ENTITY}/{PROJECT}/{run_id}')
    history=remote.history(samples=10,pandas=False)
    measured=remote.summary.get('roc_auc')
    if measured is None:
        measured=next((row['roc_auc'] for row in reversed(history) if 'roc_auc' in row),None)
    if measured is None or abs(measured-m['roc_auc'])>1e-12: raise RuntimeError('Readback metric mismatch')
    if not list(remote.logged_artifacts()): raise RuntimeError('No logged artifacts on server')
    links[key]=dict(url=url,sha256=fingerprint,model=c['model'],seed=c['seed'],window_size=w,roc_auc=m['roc_auc'],average_precision=m['average_precision'])
    tmp=manifest.with_suffix('.tmp'); tmp.write_text(json.dumps(links,indent=2)); tmp.replace(manifest)
    print(key,url,flush=True)
