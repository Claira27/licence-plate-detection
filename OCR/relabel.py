import os
import shutil

# Bảng ánh xạ class_id cần chỉnh
id_mapping = {
    20: 22,
    29: 23,
    23: 28,
    18: 20,
    28: 34,
    21: 24,
    24: 29,
    25: 30,
    17: 19,
    22: 27,
    19: 21,
    27: 33,
    26: 32,
}

# Thư mục chứa label và ảnh
label_dir = "OCR/labels/val/"
image_dir = "OCR/images/val/"
output_label_dir = "corrected/labels/"
output_image_dir = "corrected/images/"

# Tạo thư mục đầu ra nếu chưa có
os.makedirs(output_label_dir, exist_ok=True)
os.makedirs(output_image_dir, exist_ok=True)

# Xử lý từng file trong thư mục label
for filename in os.listdir(label_dir):
    if filename.endswith(".txt"):
        label_path = os.path.join(label_dir, filename)
        with open(label_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        changed = False

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            class_id = int(parts[0])
            if class_id in id_mapping:
                parts[0] = str(id_mapping[class_id])
                changed = True
            new_lines.append(" ".join(parts))

        if changed:
            # Ghi lại label đã sửa
            output_label_path = os.path.join(output_label_dir, filename)
            with open(output_label_path, "w") as f:
                f.write("\n".join(new_lines) + "\n")
            os.remove(label_path)
            # Di chuyển ảnh tương ứng
            base_name = os.path.splitext(filename)[0]
            for ext in [".jpg", ".png", ".jpeg"]:
                image_path = os.path.join(image_dir, base_name + ext)
                if os.path.exists(image_path):
                    shutil.move(image_path, os.path.join(output_image_dir, base_name + ext))
                    break
