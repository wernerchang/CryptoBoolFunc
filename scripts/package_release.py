"""Create immutable versioned host archives and public upload manifest."""
from pathlib import Path
import hashlib,json,zipfile,re
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def public_files():
    roots=['skills','scripts','tests','docs','examples','evidence','.github','releases']
    names=['README.md','VERSION','CHANGELOG.md','RELEASE_NOTES.md','CONTRIBUTORS.md','CONTRIBUTING.md','RELEASE_PROCESS.md','AGENTS.md','.gitignore','THIRD_PARTY_NOTICES.md']
    files=[ROOT/n for n in names if (ROOT/n).is_file()]
    for name in roots:
        for p in (ROOT/name).rglob('*'):
            if p.is_file() and p.name!='prepare_public.py' and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.aux','.log','.toc','.out','.fls','.fdb_latexmk'] and p.name not in ['upload-receipt.json','public-manifest.json','SHA256SUMS']:files.append(p)
    return sorted(set(files))
def main():
    version=(ROOT/'VERSION').read_text().strip();release=ROOT/'releases'/('v'+version);release.mkdir(parents=True,exist_ok=True)
    for host in ['codex','deepseek']:
        archive=release/f'CryptoBoolFunc-v{version}-{host}.zip'
        paths=list((ROOT/'skills').rglob('*.md'))+list((ROOT/'skills').rglob('*.py'))
        paths += [ROOT/'scripts/install.py',ROOT/'scripts/verify_downloads.py',ROOT/'VERSION',ROOT/'README.md',ROOT/'THIRD_PARTY_NOTICES.md']+list((ROOT/'examples').glob('*.json'))
        guide=ROOT/'docs'/f'tutorial-{host}-v1.pdf';paths.append(guide)
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(set(paths)):z.write(p,p.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    files=public_files()
    forbidden=[]
    for p in files:
        if p.suffix in ['.md','.py','.tex','.json','.yml','.txt']:
            s=p.read_text(encoding='utf-8')
            if re.search(r'[A-Za-z]:[\\/]+Users[\\/]+[^\s\\/]+',s):forbidden.append(p.relative_to(ROOT).as_posix())
    assert not forbidden,forbidden
    manifest={'version':version,'edition':'第一版','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files],'raw_pdf_distributed':False,'codex_credit':'CONTRIBUTORS.md'}
    (release/'public-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    checks=[p for p in files if p.suffix in ['.pdf','.zip']]
    (release/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in checks),encoding='utf-8')
    print(json.dumps({'version':version,'public_files':len(files)+2,'assets':len(checks),'total_bytes':sum(p.stat().st_size for p in files)},ensure_ascii=False))
if __name__=='__main__':main()
