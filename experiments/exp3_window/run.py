"""Reproduce the group's four-window INSECTS diagnostic without changing protocol."""
import argparse,subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'results/raw/window-sweep-f4-10')
    p.add_argument('--windows',nargs='+',type=int,default=[256,512,2048,8192])
    args=p.parse_args()
    env={**os.environ,'PYTHONPATH':str(ROOT/'src')}
    for window in args.windows:
        subprocess.run([sys.executable,str(ROOT/'experiments/exp2_drift/run.py'),'--models','oif','--seeds','0','--n-features','10','--window-size',str(window),'--output',str(args.output/f'omega-{window}')],env=env,check=True)
if __name__=='__main__': main()
