"""Offline first-edition regression and isolated installer checks."""
from pathlib import Path
import importlib.util,json,subprocess,sys,tempfile,uuid
ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mt=load(ROOT/'skills/mmhs-cryptographic-function-design/resources/math_tool.py','mt')
checks=[]
def check(name,fn):
    fn();checks.append({'id':name,'passed':True})
def expect(value):assert value
def rejects(name,command,data):
    try:mt.run(command,data)
    except (ValueError,KeyError):checks.append({'id':name,'passed':True});return
    raise AssertionError(name+' accepted invalid input')
def main():
    seed=[0,1,3,4,5,6,7,2]
    check('mm',lambda:expect(mt.mm({'k':3,'phi':[3,4],'h':[1,0],'require_sac':True})['metrics']['nonlinearity']==4))
    check('prefix',lambda:expect(len(mt.prefix({'n':6,'layers':[{'u':3,'count':6},{'u':2,'count':4}]})['blocks'])==10))
    evidence=json.loads((ROOT/'evidence/v1/additional-verification-results.json').read_text(encoding='utf-8'))
    blocks=[{'u':x['free_variables'],'prefix':x['prefix'],'coefficient':x['coefficient']} for x in evidence['GMM_n10_t1']['blocks']]
    check('gmm',lambda:expect(mt.gmm({'n':10,'t':1,'blocks':blocks})['metrics']['nonlinearity']==484))
    check('codes',lambda:expect(mt.codes({'k':3,'poly':11})['nonzero_coverage']==63))
    check('ps-bent',lambda:expect(mt.ps({'mode':'bent','k':3,'m':3,'poly':11})['metrics']['min_nonlinearity']==28))
    check('ps-recursive',lambda:expect(mt.ps({'mode':'recursive','m':3,'seed':seed,'polys':[11,67]})['metrics']['min_nonlinearity']==2010))
    check('ds9',lambda:expect(mt.ds({'k':3,'s':3,'seed':seed,'poly':11})['metrics']['min_nonlinearity']==240))
    check('ds11',lambda:expect(mt.ds({'k':3,'s':4,'seed':seed,'poly':19})['metrics']['min_nonlinearity']==992))
    for poly,count in [(37,10),(47,11)]:check('d-array-'+str(poly),lambda p=poly,c=count:expect(mt.d_array({'u':5,'m':3,'t':1,'poly':p})['valid_count']==c))
    corrector=json.loads((ROOT/'examples/corrector.json').read_text(encoding='utf-8'))
    check('double-code',lambda:expect(mt.corrector(corrector)['metrics']['min_nonlinearity']==448))
    h=evidence['zero_transport_n8']['source_hex'];f=[int(c) for a in h for c in f'{int(a,16):04b}']
    check('zero-transport',lambda:expect(mt.zero_transport({'table':f})['metrics']['resilience']>=1))
    f4=[((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1)) for x in range(16)]
    check('normality',lambda:expect(len(mt.normality({'table':f4})['regular_cosets'])==15))
    check('sequence',lambda:expect(mt.sequence({'f':f4,'g':[0]*16,'a':list(range(16)),'b':list(range(16))})['max_selected_absolute_correlation']==4))
    check('all-components',lambda:expect(mt.vector(seed,3)['component_count']==7))
    rejects('duplicate-phi','mm',{'k':2,'phi':[1,1]})
    rejects('incomplete-partition','prefix',{'n':6,'layers':[{'u':3,'count':7}]})
    rejects('bad-field','codes',{'k':3,'poly':9})
    rejects('custom-R','ds',{'k':3,'s':3,'seed':seed,'poly':11,'R_z':'arbitrary'})
    rejects('bad-AB','ds',{'k':3,'s':3,'seed':list(range(8)),'poly':11})
    rejects('nonBent-pruning','normality',{'table':[0,1,1,0]})
    rejects('cyclic-overclaim','sequence',{'f':f4,'g':[0]*16,'cyclic_shifts':True})
    rejects('intersecting-codes','corrector',{**corrector,'basis2':corrector['basis1']})
    fc=[mt.parity(3&(x&7)) if x<8 else mt.parity(5&(x&7))^1 for x in range(16)]
    check('layer-vs-pointwise',lambda:expect(mt.scalar(fc)['corrector_order']==2 and mt.scalar(fc)['resilience']==1))
    build=ROOT/'.build/t';build.mkdir(parents=True,exist_ok=True)
    trial=(build/uuid.uuid4().hex[:6]).resolve();trial.mkdir();assert trial.is_relative_to(build.resolve())
    def cli(*args):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),*args],capture_output=True,text=True,encoding='utf-8');return p.returncode,json.loads(p.stdout)
    for host,sub in [('codex','.agents'),('deepseek','.dsh')]:
        project=trial/host;project.mkdir();args=['--host',host,'--scope','project','--project',str(project)]
        code,v=cli(*args,'--dry-run');assert code==0 and not (project/sub).exists()
        code,v=cli(*args);assert code==0 and v['results'][0]['status']=='installed',v
        installed=project/sub/'skills/mmhs-cryptographic-function-design';assert (installed/'references/capabilities/ds-semibent.md').exists()
        code,v=cli(*args);assert code==0 and v['results'][0]['status']=='already_installed'
        entry=installed/'SKILL.md';entry.write_text(entry.read_text(encoding='utf-8')+'\nlocal edit\n',encoding='utf-8')
        code,v=cli(*args);assert code==2
        code,v=cli(*args,'--upgrade');assert code==0 and Path(v['results'][0]['backup']).is_relative_to(project.resolve())
        checks.append({'id':'installer-'+host+'-dry-idempotent-refuse-backup','passed':True})
    assert len(list((ROOT/'skills/mmhs-cryptographic-function-design/references/capabilities').glob('*.md')))==15
    report={'version':(ROOT/'VERSION').read_text().strip(),'checks':checks,'passed':len(checks),'failed':0,'scope':'offline mathematics and isolated project directory installation; no live account/model session'}
    (ROOT/'.build/test-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'version':report['version'],'passed':len(checks),'failed':0,'scope':report['scope']},ensure_ascii=False))
if __name__=='__main__':main()
