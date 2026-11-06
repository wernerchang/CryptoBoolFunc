from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1]
manifest=root/'releases/v1.0.0/SHA256SUMS'
if not manifest.exists():raise SystemExit('Run this verification in the complete repository checkout containing releases/v1.0.0/SHA256SUMS')
for line in manifest.read_text(encoding='utf-8').splitlines():
    expected,name=line.split(None,1);p=(root/name.strip()).resolve()
    if not p.is_relative_to(root.resolve()):raise SystemExit('Manifest path escaped repository')
    if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise SystemExit('SHA256 mismatch: '+name)
    print('PASS',name)
