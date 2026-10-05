"""Reproducible binary image/clip training with explicit supplied split manifests."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import random
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import classification_report, confusion_matrix
from .vision import EventNet, frame_tensor


def read_manifest(path, root):
    rows = list(csv.DictReader(Path(path).open()))
    if not rows or not {'path','label','split','group'} <= rows[0].keys():
        raise ValueError('Manifest needs path,label,split,group columns')
    groups, hashes = {}, {}
    for row in rows:
        row['label'] = int(row['label'])
        if row['label'] not in (0,1) or row['split'] not in {'train','val','test'} or not row['group']:
            raise ValueError('Invalid label, split or source group')
        file = (Path(root)/row['path']).resolve()
        if not file.is_relative_to(Path(root).resolve()) or not file.is_file():
            raise ValueError('Path missing or outside data root')
        row['resolved'] = str(file)
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        row['sha256'] = digest
        if row['group'] in groups and groups[row['group']] != row['split']:
            raise ValueError('Source group leakage across splits')
        if digest in hashes:
            raise ValueError('Duplicate media bytes in manifest')
        groups[row['group']], hashes[digest] = row['split'], row['split']
    for split in ('train','val','test'):
        if {r['label'] for r in rows if r['split']==split} != {0,1}:
            raise ValueError(f'{split} must contain both classes')
    return rows


def read_clip(path, task):
    if task == 'smoke':
        image = cv2.imread(str(path))
        if image is None:
            raise ValueError(f'Unreadable image: {Path(path).name}')
        return torch.stack([frame_tensor(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))])
    cap = cv2.VideoCapture(str(path))
    try:
        count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if count < 8:
            raise ValueError('Video needs at least eight readable frames')
        frames = []
        for position in np.linspace(0,count-1,8).astype(int):
            cap.set(cv2.CAP_PROP_POS_FRAMES,int(position))
            ok,frame = cap.read()
            if not ok:
                raise ValueError(f'Unreadable video frame: {Path(path).name}')
            frames.append(frame_tensor(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)))
        return torch.stack(frames)
    finally:
        cap.release()

class MediaDataset(Dataset):
    def __init__(self, rows, task):
        self.samples = [(read_clip(r['resolved'],task),float(r['label'])) for r in rows]
    def __len__(self):
        return len(self.samples)
    def __getitem__(self, index):
        return self.samples[index]


def evaluate(model, loader):
    actual, predicted, scores = [], [], []
    model.eval()
    with torch.inference_mode():
        for x,y in loader:
            probabilities = torch.sigmoid(model(x))
            actual.extend(y.int().tolist())
            scores.extend(probabilities.tolist())
            predicted.extend((probabilities >= .5).int().tolist())
    return {'classification_report':classification_report(actual,predicted,labels=[0,1],
                target_names=['negative','event'],output_dict=True,zero_division=0),
            'confusion_matrix':confusion_matrix(actual,predicted,labels=[0,1]).tolist(),
            'labels':actual,'scores':scores}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', choices=['smoke','violence'],required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--data-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--epochs',type=int,default=15)
    parser.add_argument('--source',required=True,help='Public dataset source URL')
    args = parser.parse_args()
    if args.epochs < 1:
        parser.error('epochs must be positive')
    random.seed(42); np.random.seed(42); torch.manual_seed(42)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    rows = read_manifest(args.manifest,args.data_root)
    loaders = {split:DataLoader(MediaDataset([r for r in rows if r['split']==split],args.task),
               batch_size=32,shuffle=split=='train',generator=torch.Generator().manual_seed(42)) for split in ('train','val','test')}
    model = EventNet()
    optimizer = torch.optim.Adam(model.parameters(),lr=.001)
    criterion = torch.nn.BCEWithLogitsLoss()
    history, best, weights = [], -1., None
    for epoch in range(args.epochs):
        model.train()
        loss_sum = 0.
        for x,y in loaders['train']:
            optimizer.zero_grad()
            loss = criterion(model(x),y.float())
            loss.backward(); optimizer.step()
            loss_sum += float(loss.item())*len(y)
        val = evaluate(model,loaders['val'])
        f1 = val['classification_report']['macro avg']['f1-score']
        history.append({'epoch':epoch+1,'train_loss':loss_sum/len(loaders['train'].dataset),'val_macro_f1':f1})
        if f1 > best:
            best = f1
            weights = {k:v.detach().clone() for k,v in model.state_dict().items()}
    model.load_state_dict(weights)
    result = {'task':args.task,'seed':42,'source':args.source,'epochs':args.epochs,'selected_val_macro_f1':best,
              'manifest_sha256':hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
              'split_counts':{s:len(l.dataset) for s,l in loaders.items()},'history':history,
              'test':evaluate(model,loaders['test']), 'torch_version':str(torch.__version__),
              'limitations':'Small baseline; dataset-specific scores do not validate surveillance or robot safety.'}
    args.output.mkdir(parents=True,exist_ok=True)
    torch.save({'schema':1,'task':args.task,'state_dict':weights,'provenance':{'source':args.source,
        'manifest_sha256':result['manifest_sha256'],'seed':42}}, args.output/(args.task+'.pt'))
    (args.output/(args.task+'_results.json')).write_text(json.dumps(result,indent=2))
    (args.output/'media_hashes.json').write_text(json.dumps([{k:v for k,v in r.items() if k!='resolved'} for r in rows],indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in {'test','history'}},indent=2))

if __name__=='__main__':
    main()
