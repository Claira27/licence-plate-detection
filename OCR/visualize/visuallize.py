import os
import cv2
import numpy as np
from pathlib import Path
import random

CLASSES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", 
    "T", "U", "V", "W", "X", "Y", "Z",
]

def generate_colors(num_classes):
    random.seed(42)
    colors = []
    for _ in range(num_classes):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(color)
    return colors

def read_yolo_label(label_path, img_width, img_height):
    bboxes = []
    if not os.path.exists(label_path):
        return bboxes

    with open(label_path, 'r') as f:
        for line in f:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            class_id = int(class_id)

            x_min = int((x_center - width / 2) * img_width)
            x_max = int((x_center + width / 2) * img_width)
            y_min = int((y_center - height / 2) * img_height)
            y_max = int((y_center + height / 2) * img_height)

            bboxes.append((class_id, x_min, y_min, x_max, y_max))

    return bboxes

def draw_bboxes(image, bboxes, classes, colors):
    label_positions = set()  # Để tránh vẽ label trùng vị trí

    for class_id, x_min, y_min, x_max, y_max in bboxes:
        if class_id >= len(classes):
            continue

        color = colors[class_id]
        class_name = classes[class_id]

        # Vẽ bounding box
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

        # Label ngắn gọn
        label = f"{class_name} ({class_id})"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        thickness = 1

        # Tính kích thước label
        (label_width, label_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
        label_x = x_min
        label_y = y_min - label_height - 4

        # Nếu label_y quá cao thì vẽ xuống dưới
        if label_y < 0:
            label_y = y_min + label_height + 4

        # Dời label nếu bị trùng vị trí
        while (label_x, label_y) in label_positions:
            label_y += label_height + 2
        label_positions.add((label_x, label_y))

        # Vẽ background label
        cv2.rectangle(image, 
                      (label_x, label_y - label_height - 2), 
                      (label_x + label_width + 4, label_y + baseline), 
                      color, 
                      thickness=cv2.FILLED)

        # Vẽ text
        cv2.putText(image, 
                    label, 
                    (label_x + 2, label_y), 
                    font, 
                    font_scale, 
                    (255, 255, 255), 
                    thickness)

    return image

def visualize_yolo_results(images_dir, labels_dir, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    colors = generate_colors(len(CLASSES))
    labels_dir = Path(labels_dir)
    images_dir = Path(images_dir)

    for label_file in labels_dir.glob("*.txt"):
        image_name = label_file.stem + ".jpg"
        image_path = images_dir / image_name
        if not image_path.exists():
            print(f"Không tìm thấy ảnh: {image_path}")
            continue

        image = cv2.imread(str(image_path))
        if image is None:
            print(f"Không thể đọc ảnh: {image_path}")
            continue

        img_height, img_width = image.shape[:2]
        bboxes = read_yolo_label(label_file, img_width, img_height)
        image_with_bboxes = draw_bboxes(image, bboxes, CLASSES, colors)

        output_path = output_dir / f"{label_file.stem}_bbox.jpg"
        cv2.imwrite(str(output_path), image_with_bboxes)

if __name__ == "__main__":
    IMAGES_DIR = "need_relabel/images"
    LABELS_DIR = "need_relabel/labels"
    OUTPUT_DIR = "drawbb"

    visualize_yolo_results(IMAGES_DIR, LABELS_DIR, OUTPUT_DIR)
