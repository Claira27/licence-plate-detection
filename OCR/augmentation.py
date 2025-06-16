import cv2
import albumentations as A
import numpy as np
import os
import glob

def read_yolo_labels(label_path):
    labels = []
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:])
            labels.append({
                'class_id': class_id,
                'bbox': [x_center, y_center, width, height]
            })
    return labels

def write_yolo_labels(label_path, labels):
    with open(label_path, 'w') as f:
        for label in labels:
            class_id = label['class_id']
            x_center, y_center, width, height = label['bbox']
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def augment_images(image_dir, num_augmentations=5):
    # Định nghĩa pipeline augmentation
    transform = A.Compose([
        A.Rotate(limit=15, p=0.5),  # Xoay ±15 độ
        A.HorizontalFlip(p=0.5),  # Lật ngang
        A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=0, p=0.5),  # Dịch chuyển, phóng to/thu nhỏ
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),  # Độ sáng, tương phản
        A.GaussNoise(p=0.3),  # Nhiễu Gaussian
        A.Blur(blur_limit=3, p=0.2),  # Làm mờ
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_ids']))

    # Lấy tất cả file ảnh
    image_files = glob.glob(os.path.join(image_dir, "*.jpg"))
    
    for image_path in image_files:
        # Đọc ảnh
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Could not read image {image_path}")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Đọc nhãn
        label_path = os.path.splitext(image_path)[0] + '.txt'
        if not os.path.exists(label_path):
            print(f"Warning: Label file {label_path} not found")
            continue
        labels = read_yolo_labels(label_path)
        bboxes = [label['bbox'] for label in labels]
        class_ids = [label['class_id'] for label in labels]
        
        # Tạo nhiều ảnh tăng cường
        for i in range(num_augmentations):
            # Áp dụng augmentation
            augmented = transform(image=image, bboxes=bboxes, class_ids=class_ids)
            aug_image = augmented['image']
            aug_bboxes = augmented['bboxes']
            aug_class_ids = augmented['class_ids']
            
            # Lưu ảnh mới
            aug_image_path = os.path.splitext(image_path)[0] + f'_aug{i+1}.jpg'
            cv2.imwrite(aug_image_path, cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR))
            
            # Lưu nhãn mới
            aug_label_path = os.path.splitext(image_path)[0] + f'_aug{i+1}.txt'
            aug_labels = [{'class_id': cid, 'bbox': bbox} for cid, bbox in zip(aug_class_ids, aug_bboxes)]
            write_yolo_labels(aug_label_path, aug_labels)
            
            print(f"Generated {aug_image_path} and {aug_label_path}")

# Chạy augmentation
image_dir = r"need_relabel\images"
augment_images(image_dir, num_augmentations=5)