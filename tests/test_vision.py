import numpy as np
import torch
import pytest
from autonomous_turtlebot_ai.vision import EventNet, Predictor, frame_tensor

def test_both_task_shapes_and_backward():
    torch.set_num_threads(2)
    model=EventNet()
    for frames in (1,8):
        x=torch.zeros(2,frames,3,64,64)
        out=model(x)
        assert out.shape==(2,) and torch.isfinite(out).all()
        out.sum().backward()

def test_checkpoint_roundtrip(tmp_path):
    path=tmp_path/'model.pt'
    torch.save({'schema':1,'task':'smoke','state_dict':EventNet().state_dict()},path)
    predictor=Predictor(path,'smoke')
    assert 0 <= predictor.score([np.zeros((32,32,3),dtype=np.uint8)]) <= 1
    with pytest.raises(ValueError): Predictor(path,'violence')
    with pytest.raises(ValueError): frame_tensor(np.zeros((32,32)))

def test_rgb_buffer_stride_and_bgr():
    from autonomous_turtlebot_ai.vision import image_rgb
    buffer=bytes([1,2,3,0,4,5,6,0])
    image=image_rgb(buffer,1,2,4,'rgb8')
    assert image.tolist()==[[[1,2,3]],[[4,5,6]]]
    assert image_rgb(buffer,1,2,4,'bgr8')[0,0].tolist()==[3,2,1]
    with pytest.raises(ValueError): image_rgb(buffer,1,2,4,'mono8')
