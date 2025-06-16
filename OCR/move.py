# import os
# import shutil

# # Thư mục chứa label và ảnh
# label_dir = "OCR/labels/val/"
# image_dir = "OCR/images/val/"
# output_label_dir = "corrected/labels/"
# output_image_dir = "corrected/images/"

# # Tạo thư mục đầu ra nếu chưa có
# os.makedirs(output_label_dir, exist_ok=True)
# os.makedirs(output_image_dir, exist_ok=True)

# # Duyệt từng file label
# for filename in os.listdir(label_dir):
#     if not filename.endswith(".txt"):
#         continue

#     label_path = os.path.join(label_dir, filename)
#     with open(label_path, "r") as f:
#         lines = [line.strip() for line in f.readlines() if line.strip()]

#     if len(lines) == 9:
#         # Di chuyển label
#         shutil.move(label_path, os.path.join(output_label_dir, filename))

#         # Di chuyển ảnh tương ứng
#         base_name = os.path.splitext(filename)[0]
#         moved = False
#         for ext in [".jpg", ".jpeg", ".png"]:
#             image_path = os.path.join(image_dir, base_name + ext)
#             if os.path.exists(image_path):
#                 shutil.move(image_path, os.path.join(output_image_dir, base_name + ext))
#                 moved = True
#                 break

#         if moved:
#             print(f"✔ Di chuyển: {filename}")
#         else:
#             print(f"⚠ Không tìm thấy ảnh cho {filename}")

import os
import shutil

# Thư mục gốc
label_dir = "OCR/labels/val/"
image_dir = "OCR/images/val/"
output_label_dir = "corrected/labels/"
output_image_dir = "corrected/images/"

# Tạo thư mục đích nếu chưa tồn tại
os.makedirs(output_label_dir, exist_ok=True)
os.makedirs(output_image_dir, exist_ok=True)

# Duyệt từng file label
for filename in os.listdir(label_dir):
    if not filename.endswith(".txt"):
        continue

    label_path = os.path.join(label_dir, filename)

    # Tìm file ảnh tương ứng
    base_name = os.path.splitext(filename)[0]
    found_image = False
    for ext in [".jpg", ".jpeg", ".png"]:
        image_path = os.path.join(image_dir, base_name + ext)
        if os.path.exists(image_path):
            # Di chuyển label và ảnh
            shutil.move(label_path, os.path.join(output_label_dir, filename))
            shutil.move(image_path, os.path.join(output_image_dir, base_name + ext))
            print(f"✔ Đã di chuyển: {filename} và {base_name + ext}")
            found_image = True
            break

    if not found_image:
        print(f"⚠ Bỏ qua {filename}: không tìm thấy ảnh")
