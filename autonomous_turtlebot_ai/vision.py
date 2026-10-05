"""Small spatial encoder with temporal GRU; smoke uses one frame, violence eight."""
import numpy as np
import cv2
import torch
from torch import nn

class EventNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(nn.Conv2d(3,16,3,padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16,32,3,padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d((4,4)))
        self.temporal = nn.GRU(32*4*4,32,batch_first=True)
        self.head = nn.Linear(32,1)
    def forward(self, clips):
        batch,frames,channels,height,width = clips.shape
        features = self.encoder(clips.reshape(batch*frames,channels,height,width)).flatten(1)
        _, state = self.temporal(features.reshape(batch,frames,-1))
        return self.head(state[-1]).squeeze(-1)

def frame_tensor(rgb):
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError('Expected RGB HWC image')
    array = cv2.resize(rgb,(64,64)).astype(np.float32)/255.
    return torch.from_numpy(array.transpose(2,0,1).copy())

class Predictor:
    def __init__(self, path, task):
        torch.set_num_threads(2)
        checkpoint = torch.load(path,map_location='cpu',weights_only=True)
        if checkpoint.get('task') != task or checkpoint.get('schema') != 1:
            raise ValueError('Checkpoint task/schema mismatch')
        self.frames = 1 if task == 'smoke' else 8
        self.model = EventNet().eval()
        self.model.load_state_dict(checkpoint['state_dict'])
        self.provenance = checkpoint.get('provenance',{})
    def score(self, rgb_frames):
        if len(rgb_frames) != self.frames:
            raise ValueError(f'Require {self.frames} frames')
        clip = torch.stack([frame_tensor(x) for x in rgb_frames]).unsqueeze(0)
        with torch.inference_mode():
            return float(torch.sigmoid(self.model(clip)).item())


def image_rgb(data, width, height, step, encoding):
    """Decode ROS RGB/BGR8 buffers including row padding, without cv_bridge ABI coupling."""
    if encoding not in {'rgb8','bgr8'} or width < 1 or height < 1 or step < width*3 or len(data) < height*step:
        raise ValueError('Require complete RGB8/BGR8 image with a valid row stride')
    image = np.ndarray((height,width,3),dtype=np.uint8,buffer=data,strides=(step,3,1))
    return image.copy() if encoding == 'rgb8' else image[:,:,::-1].copy()
