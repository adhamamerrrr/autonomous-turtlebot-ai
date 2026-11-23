New model replacement completed

This package uses the NEW YOLO model only.
Old integration model was replaced at:
  integration_bridge/best.pt

New dataset class names from data.yaml:
  0: cigarette
  1: vape

The ML bridge now treats both classes as a pending smoking detection trigger:
  --target-classes cigarette,vape

The robot/app flow is still the same:
  YOLO detects cigarette/vape -> creates smoke_detections pending review -> security guard confirms or rejects -> confirmed violation appears for the manually entered student ID.

Firebase private key is NOT included. Copy your own serviceAccountKey.json into integration_bridge before running Python scripts.
