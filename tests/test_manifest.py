import csv
import pytest
from autonomous_turtlebot_ai.train import read_manifest

def write(tmp_path, duplicate=False, group_leak=False):
    rows=[]
    for split in ('train','val','test'):
        for label in (0,1):
            name=f'{split}{label}.jpg'
            (tmp_path/name).write_bytes(b'same' if duplicate else name.encode())
            rows.append({'path':name,'label':label,'split':split,'group':'same' if group_leak else name})
    with (tmp_path/'m.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','label','split','group']);w.writeheader();w.writerows(rows)
    return tmp_path/'m.csv'

def test_valid_split(tmp_path):
    assert len(read_manifest(write(tmp_path),tmp_path))==6

def test_duplicate_rejected(tmp_path):
    with pytest.raises(ValueError,match='Duplicate'):
        read_manifest(write(tmp_path,duplicate=True),tmp_path)

def test_group_leakage_rejected(tmp_path):
    with pytest.raises(ValueError,match='group leakage'):
        read_manifest(write(tmp_path,group_leak=True),tmp_path)
