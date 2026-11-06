"""Install complete skills into Codex or DeepSeek Harness scan roots."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,tempfile,uuid,sys
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
NAME='mmhs-cryptographic-function-design'
def digest(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}
def contained(path,root):
    if not path.resolve().is_relative_to(root.resolve()):raise ValueError('destination escaped installation root')
def install(source,root,name,upgrade=False,dry=False):
    source=source.resolve();root=root.resolve();dest=root/name;contained(dest,root)
    if not (source/'SKILL.md').is_file():raise ValueError('source lacks SKILL.md: '+str(source))
    if any(p.is_symlink() for p in source.rglob('*')):raise ValueError('source contains symlinks; review and use a plain directory')
    if dest.is_symlink():raise ValueError('destination is a symlink; refusing implicit overwrite')
    if dest.exists() and digest(source)==digest(dest):return {'skill':name,'status':'already_installed','destination':str(dest)}
    if dest.exists() and not upgrade:raise ValueError('different version exists; review then use --upgrade (a backup is kept)')
    if dry:return {'skill':name,'status':'dry_run','destination':str(dest),'would_backup':dest.exists()}
    root.mkdir(parents=True,exist_ok=True)
    stage=root/('.tmp-'+uuid.uuid4().hex[:8]);contained(stage,root);stage.mkdir()
    copied=stage/name
    shutil.copytree(source,copied,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
    backup=None
    if dest.exists():
        stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup=root/'.backups'/stamp/name;contained(backup,root);backup.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(dest),str(backup))
    os.replace(copied,dest);stage.rmdir()
    return {'skill':name,'status':'installed','destination':str(dest),'backup':str(backup) if backup else None}
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--host',choices=['codex','deepseek'],required=True)
    ap.add_argument('--scope',choices=['user','project'],default='user')
    ap.add_argument('--project',type=Path);ap.add_argument('--root',type=Path,help='explicit scan-root override, useful for isolated testing')
    ap.add_argument('--cangjie-source',type=Path,help='complete extracted upstream cangjie-skill directory')
    ap.add_argument('--upgrade',action='store_true');ap.add_argument('--dry-run',action='store_true')
    a=ap.parse_args();repo=Path(__file__).resolve().parents[1]
    try:
        if a.root:root=a.root
        elif a.scope=='project':
            if a.project is None:raise ValueError('--project is required for project scope')
            root=a.project/('.agents' if a.host=='codex' else '.dsh')/'skills'
        else:root=(Path.home()/'.agents' if a.host=='codex' else Path(os.environ.get('DSH_HOME',str(Path.home()/'.dsh'))))/'skills'
        sources=[]
        if a.cangjie_source:
            for required in ['SKILL.md','scripts/cangjie.py','methodology']:
                if not (a.cangjie_source/required).exists():raise ValueError('incomplete Cangjie directory: missing '+required)
            sources.append((a.cangjie_source,'cangjie-skill'))
        sources.append((repo/'skills'/NAME,NAME))
        # Preflight all sources before mutating either installation.
        for source,name in sources:install(source,root,name,a.upgrade,True)
        results=[install(source,root,name,a.upgrade,a.dry_run) for source,name in sources]
        print(json.dumps({'host':a.host,'scope':a.scope,'results':results,'note':'Filesystem installation is not a live host/model acceptance test.'},ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError) as e:
        print(json.dumps({'status':'error','error':str(e)},ensure_ascii=False));return 2
if __name__=='__main__':raise SystemExit(main())
