"""Synthetic AVI round trip for the temporal training path; no violence evidence."""
import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import cv2
import numpy as np
from autonomous_turtlebot_ai.vision import Predictor

with tempfile.TemporaryDirectory() as folder:
    root=Path(folder); rows=[]; rng=np.random.default_rng(42)
    for split,count in [('train',4),('val',2),('test',2)]:
        for label in (0,1):
            for i in range(count):
                name=f'{split}_{label}_{i}.avi'
                writer=cv2.VideoWriter(str(root/name),cv2.VideoWriter_fourcc(*'MJPG'),5,(64,64))
                assert writer.isOpened(), 'AVI encoder unavailable'
                for frame in range(8):
                    image=rng.integers(0,30,(64,64,3),dtype=np.uint8)
                    image[:,:,label]=180+frame
                    writer.write(image)
                writer.release()
                rows.append({'path':name,'label':label,'split':split,'group':name})
    with (root/'manifest.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','label','split','group']); w.writeheader(); w.writerows(rows)
    subprocess.run([sys.executable,'-m','autonomous_turtlebot_ai.train','--task','violence',
        '--manifest',str(root/'manifest.csv'),'--data-root',str(root),'--output',str(root/'models'),
        '--epochs','1','--source','synthetic-AVI-software-fixture'],check=True)
    predictor=Predictor(root/'models'/'violence.pt','violence')
    assert 0 <= predictor.score([np.zeros((64,64,3),dtype=np.uint8)]*8) <= 1
print('Synthetic temporal data decoding, training, save, load and inference passed; no real violence model trained')
