"""Portable exact small-parameter Boolean-function laboratory.

Usage: python math_tool.py COMMAND --input input.json [--output result.json]
Commands: inspect, mm, prefix, gmm, codes, ps, ds, d-array,
zero-transport, normality, sequence, corrector.
Integer x encodes input bit i at (x>>i)&1. No floating point arithmetic.
This implementation is a bounded research tool, not an asymptotic proof.
"""
import argparse,itertools,json,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

def require(condition,message):
    if not condition:raise ValueError(message)
def parity(x):return x.bit_count()&1
def integer(x):return isinstance(x,int) and not isinstance(x,bool)
def table(values):
    require(isinstance(values,list) and len(values)>=2 and len(values)&(len(values)-1)==0,'table length must be a power of two >=2')
    require(len(values)<=4096,'small-parameter limit: n<=12')
    require(all(integer(v) and v in (0,1) for v in values),'Boolean table entries must be integer 0 or 1')
    return values
def fwht(values):
    a=list(values);h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            for j in range(i,i+h):
                u,v=a[j],a[j+h];a[j],a[j+h]=u+v,u-v
        h*=2
    return a
def anf(values):
    a=list(values);h=1
    while h<len(a):
        for x in range(len(a)):
            if x&h:a[x]^=a[x^h]
        h*=2
    return [i for i,v in enumerate(a) if v]
def scalar(values):
    f=table(values);n=len(f).bit_length()-1;w=fwht([1-2*v for v in f]);terms=anf(f)
    sums=[sum(v for a,v in enumerate(w) if a.bit_count()==j) for j in range(n+1)]
    t=min(a.bit_count() for a,v in enumerate(w) if v)-1
    order=next(j-1 for j,v in enumerate(sums) if v)
    return {'n':n,'balanced':w[0]==0,'nonlinearity':(len(f)-max(map(abs,w)))//2,'resilience':t,'corrector_order':order,'degree':max((a.bit_count() for a in terms),default=0),'anf_masks':terms,'walsh':w,'weight_layer_sums':sums,'absolute_spectrum':dict(sorted(Counter(map(abs,w)).items())),'parseval':sum(v*v for v in w),'sac':[sum(f[x]^f[x^(1<<j)] for x in range(len(f)))==len(f)//2 for j in range(n)]}
def vector(values,m):
    require(integer(m) and 1<=m<=6,'vector m must be in 1..6')
    require(all(integer(v) and 0<=v<1<<m for v in values),'vector output out of range')
    table([parity(v) for v in values])
    comps={str(c):scalar([parity(c&v) for v in values]) for c in range(1,1<<m)}
    return {'n':len(values).bit_length()-1,'m':m,'component_count':len(comps),'balanced':all(v['balanced'] for v in comps.values()),'min_nonlinearity':min(v['nonlinearity'] for v in comps.values()),'min_degree':min(v['degree'] for v in comps.values()),'max_degree':max(v['degree'] for v in comps.values()),'resilience':min(v['resilience'] for v in comps.values()),'corrector_order':min(v['corrector_order'] for v in comps.values()),'output_counts':dict(sorted(Counter(values).items())),'components':comps}
def basis(vectors):
    piv={};chosen=[]
    for a in vectors:
        b=a
        for k,p in sorted(piv.items(),reverse=True):
            if b>>k&1:b^=p
        if b:piv[b.bit_length()-1]=b;chosen.append(a)
    return chosen
def span(rows):
    out=[0]
    for r in rows:out+=[x^r for x in out]
    return set(out)
def mul(a,b,k,poly):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a&(1<<k):a^=poly
    return r
def powers(k,poly):
    require(integer(k) and 1<=k<=10,'field dimension must be in 1..10')
    require(integer(poly) and poly.bit_length()==k+1 and poly&1,'polynomial must be monic degree k with constant term 1')
    a=1;out=[]
    for _ in range((1<<k)-1):out.append(a);a=mul(a,2,k,poly)
    require(a==1 and len(set(out))==(1<<k)-1 and 0 not in out,'x is not primitive in the specified quotient')
    return out
def inspect(d):
    f=d['table']
    if 'm' in d:return {'metrics':vector(f,d['m'])}
    return {'metrics':scalar(f)}
def mm(d):
    k=d['k'];phi=d['phi'];h=d.get('h',[0]*len(phi))
    require(integer(k) and 1<=k<=10,'k must be in 1..10')
    table([0]*len(phi));table(h)
    require(len(h)==len(phi) and len(phi)*(1<<k)<=4096,'selector length mismatch or n>12')
    require(all(integer(a) and 0<=a<1<<k for a in phi),'coefficient out of range')
    require(len(set(phi))==len(phi),'phi must be injective')
    if d.get('require_sac',False):require(all((a^((1<<k)-1)) in phi for a in phi),'SAC construction requires complementary image pairs')
    f=[parity(a&x)^h[y] for y,a in enumerate(phi) for x in range(1<<k)]
    return {'table':f,'metrics':scalar(f),'min_image_weight':min(a.bit_count() for a in phi),'complement_closed':all((a^((1<<k)-1)) in phi for a in phi)}
def prefix(d):
    n=d['n'];require(integer(n) and 2<=n<=12,'n must be in 2..12')
    layers=d['layers'];require(len({r['u'] for r in layers})==len(layers),'each u must occur once')
    cursor=0;out=[]
    for r in sorted(layers,key=lambda r:-r['u']):
        u,count=r['u'],r['count'];require(integer(u) and 1<=u<n and integer(count) and count>=0,'invalid layer size or count')
        for _ in range(count):
            require(cursor%(1<<u)==0 and cursor+(1<<u)<=1<<n,'dyadic capacity overflow')
            out.append({'u':u,'prefix':cursor>>u});cursor+=1<<u
    require(cursor==1<<n,'incomplete cover')
    return {'n':n,'blocks':out,'complete_disjoint_cover':True}
def gmm(d):
    n=d['n'];require(integer(n) and 2<=n<=12,'n must be in 2..12')
    blocks=d['blocks'];f=[None]*(1<<n);used={};dims=set()
    for r in blocks:
        u,p,a=r['u'],r['prefix'],r['coefficient'];b=r.get('constant',0)
        require(integer(u) and 1<=u<n and integer(p) and 0<=p<1<<(n-u),'invalid prefix block')
        require(integer(a) and 0<=a<1<<u and b in (0,1),'invalid coefficient or constant')
        require(a not in used.setdefault(u,set()),'coefficient collision within a layer')
        used[u].add(a);dims.add(u)
        for x in range(1<<u):
            at=(p<<u)|x;require(f[at] is None,'overlapping blocks');f[at]=parity(a&x)^b
    require(all(v is not None for v in f),'incomplete cover')
    t=d.get('t',0);require(integer(t) and t>=0,'t must be nonnegative')
    require(all(a.bit_count()>t for s in used.values() for a in s),'coefficient weight does not exceed t')
    return {'table':f,'metrics':scalar(f),'nonlinearity_lower_bound':(1<<(n-1))-sum(1<<(u-1) for u in dims),'complete_disjoint_cover':True}
def codes(d):
    k=d['k'];require(integer(k) and 1<=k<=4,'codes limit: k<=4')
    q=1<<k;powers(k,d['poly']);cs=[[a|(mul(a,z,k,d['poly'])<<k) for a in range(q)] for z in range(q)]+[[a<<k for a in range(q)]]
    for A,B in itertools.combinations(cs,2):require(set(A)&set(B)=={0},'nontrivial code intersection')
    return {'k':k,'code_count':len(cs),'codes':cs,'nonzero_coverage':len(set().union(*map(set,cs)))-1,'pairwise_intersection_zero':True,'minimum_distances':[min(v.bit_count() for v in C if v) for C in cs]}
def ps(d):
    mode=d.get('mode','recursive');m=d['m'];require(integer(m) and 1<=m<=6,'m must be in 1..6')
    if mode=='bent':
        k=d['k'];require(integer(k) and m<=k<=6,'require m<=k<=6');q=1<<k;poly=d['poly'];pw=powers(k,poly);inv={a:pw[-i%len(pw)] for i,a in enumerate(pw)}
        f=[0 if x==0 else mul(y,inv[x],k,poly)&((1<<m)-1) for x in range(q) for y in range(q)]
    else:
        require(mode=='recursive','mode must be bent or recursive');f=d['seed'];require(len(f)==1<<m and sorted(f)==list(range(1<<m)),'seed must be a permutation on m bits')
        sm=vector(f,m);threshold=(1<<(m-1))-(1<<(m//2 if m%2==0 else (m-1)//2))
        require(sm['min_nonlinearity']>=threshold,'seed does not meet construction 3.16 nonlinearity requirement')
        polys=d['polys'];require(len(polys)>0,'at least one recursive level required')
        for poly in polys:
            k=len(f).bit_length()-1;require(2*k<=12,'recursive output exceeds n=12');q=1<<k;pw=powers(k,poly);inv={a:pw[-i%len(pw)] for i,a in enumerate(pw)}
            f=[f[y] if x==0 else mul(y,inv[x],k,poly)&((1<<m)-1) for x in range(q) for y in range(q)]
    return {'table':f,'metrics':vector(f,m),'mode':mode}
def ds(d):
    require(not any(key in d for key in ['R','R_z','R_matrices']),'ds implements R_z=I only; custom R is outside the verified scope')
    k,s=d['k'],d['s'];require(integer(k) and integer(s) and k>=3 and k%2==1 and s>=k and 2*s+k<=12,'require odd k>=3, s>=k, 2s+k<=12')
    seed=d['seed'];require(len(seed)==1<<k and sorted(seed)==list(range(1<<k)),'AB seed must be a k-bit permutation')
    sm=vector(seed,k);require(all(set(v['walsh'])<=set([0,1<<((k+1)//2),-(1<<((k+1)//2))]) for v in sm['components'].values()),'seed is not AB')
    poly=d['poly'];powers(s,poly);f=[]
    for z in range(1<<s):
        rows=[mul(z,1<<i,s,poly) for i in range(k)]
        for x in range(1<<k):
            for y in range(1<<s):f.append(seed[x^sum(parity(y&r)<<i for i,r in enumerate(rows))])
    return {'table':f,'metrics':vector(f,k),'R':'identity','field_dimension':s}
def d_array(d):
    u,m,t=d['u'],d['m'],d['t'];require(integer(m) and 1<=m<=min(6,u) and integer(t) and t>=0,'invalid m or t');pw=powers(u,d['poly']);out=[]
    for j in range(len(pw)):
        row=[pw[(j+i)%len(pw)] for i in range(m)];weights=[]
        for c in range(1,1<<m):
            a=0
            for i,v in enumerate(row):
                if c>>i&1:a^=v
            weights.append(a.bit_count())
        if min(weights)>t:out.append({'index':j,'coefficients':row,'combination_weights':weights})
    return {'u':u,'m':m,'t':t,'poly':d['poly'],'basis':'1,alpha,...,alpha^(u-1); integer bit i is alpha^i','valid_count':len(out),'rows':out,'statement':'Capacity belongs to this representation and column selection; no mixed-GMM extremum is inferred.'}
def zero_transport(d):
    f=table(d['table']);n=len(f).bit_length()-1;w=fwht([1-2*v for v in f]);zeros=[a for a,v in enumerate(w) if not v]
    for delta in zeros:
        rows=basis([a^delta for a in zeros])
        if len(rows)==n:break
    else:return {'status':'no_full_basis','claim':'no such affine full zero basis found by exhaustive delta scan','zero_count':len(zeros)}
    g=[None]*len(f)
    for u in range(len(f)):
        x=sum(parity(u&r)<<i for i,r in enumerate(rows));g[x]=f[u]^parity(delta&u)
    return {'status':'constructed','delta':delta,'R_rows':rows,'table':g,'metrics':scalar(g),'claim':'guarantees at least first-order resilience, not arbitrary higher t'}
def normality(d):
    f=table(d['table']);n=len(f).bit_length()-1;require(n%2==0 and n<=6,'normality enumeration requires even n<=6')
    w=fwht([1-2*v for v in f]);require(all(abs(v)==1<<(n//2) for v in w),'normality pruning requires Bent input')
    k=n//2;spaces=set()
    for rows in itertools.combinations(range(1,len(f)),k):
        if len(basis(rows))==k:spaces.add(tuple(sorted(span(rows))))
    result=set();checked=0
    for C in spaces:
        cosets={tuple(sorted(x^c for c in C)) for x in range(len(f))}
        for S in sorted(cosets):
            checked+=1;wt=sum(f[x] for x in S)
            if wt in (0,len(S)):result.add(S)
            elif wt!=len(S)//2:break
    return {'linear_subspace_count':len(spaces),'checked_cosets':checked,'regular_cosets':sorted(result),'is_regular':bool(result),'enumeration':'unique spans; not a claim of an implemented GJB-specific enumerator'}
def sequence(d):
    require(not d.get('cyclic_shifts',False),'cyclic-shift correlation is outside this command')
    f,g=table(d['f']),table(d['g']);require(len(f)==len(g),'sequence table lengths differ');aa=d.get('a',[0]);bb=d.get('b',[0]);require(len(aa)*len(bb)<=4096,'at most 4096 selected label pairs')
    require(all(integer(a) and 0<=a<len(f) for a in aa+bb),'label out of range');h=[x^y for x,y in zip(f,g)];w=fwht([1-2*v for v in h]);pairs=[]
    for a in aa:
        for b in bb:
            corr=sum(1-2*(f[x]^g[x]^parity((a^b)&x)) for x in range(len(f)));require(corr==w[a^b],'internal correlation check failed');pairs.append({'a':a,'b':b,'correlation':corr})
    return {'pairs':pairs,'max_selected_absolute_correlation':max(abs(p['correlation']) for p in pairs),'max_all_labels_absolute_correlation':max(map(abs,w)),'cyclic_shifts_tested':False}
def corrector(d):
    require(d.get('model','iid_same_bias')=='iid_same_bias','corrector guarantee requires independent identical input bias')
    m=d['m'];c1,c2=d['basis1'],d['basis2'];u=d['u'];require(integer(m) and 2<=m<=6 and integer(u) and m<u and m+u<=12,'require 2<=m<u and m+u<=12')
    require(len(c1)==len(c2)==m and all(integer(x) and 0<=x<1<<u for x in c1+c2),'invalid bases')
    require(len(basis(c1))==len(basis(c2))==m,'bases must have full row rank');C,D=span(c1),span(c2);require(C&D=={0},'codes must intersect only in zero')
    weights={v.bit_count() for v in (C|D)-{0}};require(len(weights)==1,'both codes must have the same constant nonzero weight')
    pw=powers(m,d['poly']);f=[]
    def pi(a,rows):
        out=0
        for i,r in enumerate(rows):
            if a>>i&1:out^=r
        return out
    for y in range(1<<m):
        coeff=[pi(pw[(y+i)%len(pw)],c2 if y==0 else c1) for i in range(m)]
        for x in range(1<<u):f.append(sum((parity(a&x)^((y>>(m-1-i))&1))<<i for i,a in enumerate(coeff)))
    return {'table':f,'metrics':vector(f,m),'guaranteed_corrector_order':next(iter(weights)),'selector_bit_order':'[Y] is the integer y; yi=(y>>(m-1-i))&1; output i is bit i','model':'independent inputs with identical bias only'}
COMMANDS={'inspect':inspect,'mm':mm,'prefix':prefix,'gmm':gmm,'codes':codes,'ps':ps,'ds':ds,'d-array':d_array,'zero-transport':zero_transport,'normality':normality,'sequence':sequence,'corrector':corrector}
def run(command,data):return {'status':'ok','command':command,**COMMANDS[command](data)}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=COMMANDS);ap.add_argument('--input',required=True);ap.add_argument('--output');args=ap.parse_args()
    try:result=run(args.command,json.loads(Path(args.input).read_text(encoding='utf-8-sig')));code=0
    except (ValueError,KeyError,TypeError,IndexError) as e:result={'status':'error','command':args.command,'error':str(e)};code=2
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:Path(args.output).write_text(text+'\n',encoding='utf-8')
    else:print(text)
    return code
if __name__=='__main__':sys.exit(main())
