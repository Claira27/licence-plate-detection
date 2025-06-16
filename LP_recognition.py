from PIL import Image, ImageOps
import cv2
import torch
import math 
import function.utils_rotate as utils_rotate
from IPython.display import display
import os
import function.helper as helper
import pathlib
import torch

# Fix lỗi PosixPath khi load mô hình YOLOv5 trên Windows
pathlib.PosixPath = pathlib.WindowsPath

# load yolo model for detect and character detection stage
# please download yolov5 from our link on github
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/lp_detection.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/letter_detection.pt', force_reload=True, source='local')

# set model confidence threshold 
# yolo_LP_detect.conf = 0.6
yolo_license_plate.conf = 0.60

#enter image path here
#image_file = "test/8.jpg"
img_file = "test/CarLongPlate135.jpg"
img = cv2.imread(img_file)
plates = yolo_LP_detect(img, size=640)

list_plates = plates.pandas().xyxy[0].values.tolist()
list_read_plates = set()

count = 0
if len(list_plates) == 0:
    lp = helper.read_plate(yolo_license_plate,img)
    if lp != "unknown":
        list_read_plates.add(lp)
else:
    for plate in list_plates:
        flag = 0
        x = int(plate[0]) # xmin
        y = int(plate[1]) # ymin
        w = int(plate[2] - plate[0]) # xmax - xmin
        h = int(plate[3] - plate[1]) # ymax - ymin  
        crop_img = img[y:y+h, x:x+w]
        cv2.rectangle(img, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)
        cv2.imwrite("crop.jpg", crop_img)
        rc_image = cv2.imread("crop.jpg")
        lp = ""
        count+=1
        for cc in range(0,2):
            for ct in range(0,2):
                lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                if lp != "unknown":
                    list_read_plates.add(lp)
                    flag = 1
                    break
            if flag == 1:
                break
print("Danh sách biển số phát hiện:", list_read_plates)
img = Image.open(img_file)
basewidth = 500
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
display(img)


###################################

# from PIL import Image, ImageOps
# import cv2
# import torch
# import pathlib
# import function.helper as helper
# import function.utils_rotate as utils_rotate
# from IPython.display import display

# # Fix lỗi PosixPath khi load mô hình YOLOv5 trên Windows
# pathlib.PosixPath = pathlib.WindowsPath

# # load yolo model for detect and character detection stage
# yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/lp_detection.pt', force_reload=True, source='local')
# yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/letter_detection.pt', force_reload=True, source='local')

# # set model confidence threshold
# yolo_license_plate.conf = 0.60

# #enter image path here
# img_file = "test/CarLongPlate70.jpg"
# img = cv2.imread(img_file)
# plates = yolo_LP_detect(img, size=640)

# list_plates = plates.pandas().xyxy[0].values.tolist()
# list_read_plates = set()

# count = 0
# if len(list_plates) == 0:
#     lp = helper.read_plate(yolo_license_plate, img)
#     if lp != "unknown":
#         list_read_plates.add(lp)
# else:
#     for plate in list_plates:
#         flag = 0
#         x = int(plate[0])  # xmin
#         y = int(plate[1])  # ymin
#         w = int(plate[2] - plate[0])  # xmax - xmin
#         h = int(plate[3] - plate[1])  # ymax - ymin  
#         crop_img = img[y:y+h, x:x+w]
        
#         # Vẽ bounding box lên ảnh
#         cv2.rectangle(img, (int(plate[0]), int(plate[1])), (int(plate[2]), int(plate[3])), color=(0, 0, 225), thickness=2)
        
#         # Ghi kết quả lên ảnh (biển số)
#         lp = helper.read_plate(yolo_license_plate, crop_img)
#         if lp != "unknown":
#             list_read_plates.add(lp)
#             cv2.putText(img, lp, (int(plate[0]), int(plate[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

#         count += 1

# # Lưu ảnh đã chỉnh sửa
# output_img_file = "output_image.jpg"
# cv2.imwrite(output_img_file, img)

# # Hiển thị ảnh
# img_pil = Image.open(img_file)
# basewidth = 500
# wpercent = (basewidth / float(img_pil.size[0]))
# hsize = int((float(img_pil.size[1]) * float(wpercent)))
# img_pil = img_pil.resize((basewidth, hsize), Image.Resampling.LANCZOS)
# display(img_pil)

# # In kết quả
# print("Danh sách biển số phát hiện:", list_read_plates)