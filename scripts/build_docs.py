from pathlib import Path
import os,shutil,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    engine=shutil.which('xelatex')
    if not engine:raise SystemExit('XeLaTeX not found; install TeX Live/MiKTeX with ctex and Fandol fonts')
    out=ROOT/'.build/tex';out.mkdir(parents=True,exist_ok=True);reports=[]
    for name in ['tutorial-codex-v1','tutorial-deepseek-v1']:
        for step in range(2):
            p=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory='+str(out),name+'.tex'],cwd=ROOT/'docs',capture_output=True)
            (out/f'{name}-pass{step+1}.txt').write_bytes(p.stdout+p.stderr)
            if p.returncode:raise SystemExit('XeLaTeX failed; see '+str(out/f'{name}-pass{step+1}.txt'))
        log=(out/(name+'.log')).read_text(encoding='utf-8',errors='replace')
        problems=[line for line in log.splitlines() if any(s in line for s in ['Overfull \\hbox','Missing character:','LaTeX Error:','undefined references','undefined citations'])]
        if problems:raise SystemExit('\n'.join(problems))
        shutil.copyfile(out/(name+'.pdf'),ROOT/'docs'/(name+'.pdf'))
        reports.append({'document':name,'compiled_passes':2,'blocking_log_findings':problems})
    print(json.dumps(reports,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
