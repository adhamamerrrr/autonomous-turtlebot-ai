"""Download author-linked D-Fire mirror and select a small reproducible subset."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import random
import urllib.request
import zipfile
import yaml
URL='https://www.kaggle.com/api/v1/datasets/download/sayedgamal99/smoke-fire-detection-yolo'
p=argparse.ArgumentParser()
p.add_argument('--archive',type=Path,default=Path('data/dfire.zip'))
p.add_argument('--output',type=Path,default=Path('data/dfire-small'))
p.add_argument('--train-per-class',type=int,default=200)
p.add_argument('--eval-per-class',type=int,default=50)
a=p.parse_args()
if min(a.train_per_class,a.eval_per_class)<1: p.error('Counts must be positive')
a.archive.parent.mkdir(parents=True,exist_ok=True)
if not a.archive.exists():
    with urllib.request.urlopen(URL,timeout=60) as response, a.archive.with_suffix('.part').open('wb') as out:
        while block:=response.read(1024*1024): out.write(block)
    a.archive.with_suffix('.part').replace(a.archive)
a.output.mkdir(parents=True,exist_ok=True)
rng=random.Random(42); rows=[]; used_hashes=set(); available={}
with zipfile.ZipFile(a.archive) as z:
    meta=yaml.safe_load(z.read('data.yaml'))
    if meta.get('names') != ['smoke','fire']: raise ValueError('Unexpected class ordering')
    names=set(z.namelist())
    for split in ('train','val','test'):
        candidates={0:[],1:[]}; prefix=f'data/{split}/images/'
        for name in sorted(n for n in names if n.startswith(prefix) and n.endswith('.jpg')):
            label_name=name.replace('/images/','/labels/').rsplit('.',1)[0]+'.txt'
            if label_name not in names: raise ValueError('Missing annotation')
            labels=z.read(label_name).decode().splitlines()
            smoke=any(line.split()[0]=='0' for line in labels if line.strip())
            candidates[int(smoke)].append(name)
        available[split]={str(label):len(items) for label,items in candidates.items()}
        count=a.train_per_class if split=='train' else a.eval_per_class
        for label,items in candidates.items():
            rng.shuffle(items); selected=0
            for name in items:
                contents=z.read(name); digest=hashlib.sha256(contents).hexdigest()
                if digest in used_hashes: continue
                relative=Path(name); dest=(a.output/relative).resolve()
                if not dest.is_relative_to(a.output.resolve()): raise ValueError('Unsafe archive path')
                dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(contents)
                used_hashes.add(digest)
                rows.append({'path':relative.as_posix(),'label':label,'split':split,'group':relative.as_posix()})
                selected+=1
                if selected==count: break
            if selected<count: raise ValueError('Insufficient unique images')
with (a.output/'manifest.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['path','label','split','group']); writer.writeheader(); writer.writerows(rows)
hash_object=hashlib.sha256()
with a.archive.open('rb') as f:
    while block:=f.read(1024*1024): hash_object.update(block)
provenance={'source':URL,'original_source':'https://github.com/gaia-solutions-on-demand/DFireDataset',
    'license':'Upstream D-Fire collection CC0 1.0; Kaggle mirror declares CC0',
    'archive_sha256':hash_object.hexdigest(),'seed':42,'selected_images':len(rows),'available_counts':available,
    'label_rule':'smoke if any YOLO class 0 box; fire-only is negative for smoke',
    'split':'preserve mirror train/val/test, sample equally by label, remove selected exact byte duplicates',
    'limitations':'Capture/source grouping unavailable. Filename groups do not guarantee scene-independent evaluation.'}
(a.output/'dataset.json').write_text(json.dumps(provenance,indent=2)); print(json.dumps(provenance,indent=2))
