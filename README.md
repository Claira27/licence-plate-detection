# License Plate Detection and Recognition 
A complete deep learning pipeline using two YOLOv5 models to **detect license plates** and **recognize characters** from images. This project is designed to handle Vietnamese license plates with high accuracy.
## Project Overview

This project performs:

1. **License Plate Detection** using a YOLOv5 object detection model.
2. **Text Recognition (OCR)** by cropping the detected license plate and passing it to a character recognition model.

---

## Folder Structure

Licence-Plate-Detection/
├── function/
│ ├── helper.py # Utilities for reading character sequences
│ └── utils_rotate.py # Image rotation and preprocessing helpers
│
├── LP_recognition.py # 🔥 Main inference script (image → plate text)
│
├── model/
│ ├── plate_detection.pt # YOLOv5 model for detecting license plates
│ └── letter_detection.pt # YOLOv5 model for detecting characters
│
├── LP_detection/ # Dataset for license plate detection (YOLO format)
├── OCR/ # Dataset for letter (character) detection
│
├── plate_detection_train_result/ # Training logs/results for plate detection
├── letter_detection_train_result/ # Training logs/results for character detection
│
├── test/ # Folder with test images
├── yolov5/ # YOLOv5 repo (used for training/inference)


---

## Workflow

1. **Plate Detection**  
   The image is passed through a YOLOv5 model to detect license plates.

2. **Plate Cropping & Alignment**  
   Detected plates are cropped and rotated if necessary using helper functions.

3. **Character Detection**  
   Cropped plates are passed to a second YOLOv5 model to detect each character.

4. **Character Sorting & Reading**  
   Characters in multi-line plates are sorted from left to right, top to bottom and assembled into a string using logic from `helper.py`.

---

## Test with LP_recognition.py

You can test the full pipeline on any image using:

```bash
python LP_recognition.py 


