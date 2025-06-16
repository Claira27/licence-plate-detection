import math

# license plate type classification helper function
def linear_equation(x1, y1, x2, y2):
    b = y1 - (y2 - y1) * x1 / (x2 - x1)
    a = (y1 - b) / x1
    return a, b

def check_point_linear(x, y, x1, y1, x2, y2):
    a, b = linear_equation(x1, y1, x2, y2)
    y_pred = a * x + b
    return math.isclose(y_pred, y, abs_tol=3)

def read_plate(yolo_license_plate, im):
    results = yolo_license_plate(im)
    detections = results.pandas().xyxy[0].copy()

    # Cộng thêm 1 vào class ID
    detections['class'] = detections['class'] + 1

    # Map class ID thành ký tự biển số
    class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                   'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z']
    
    detections['char'] = detections['class'].apply(lambda x: class_names[int(x)] if int(x) < len(class_names) else '?')

    # Nếu không đủ ký tự hoặc quá nhiều, trả về unknown
    if len(detections) < 7 or len(detections) > 10:
        return "unknown"

    center_list = []
    y_sum = 0
    for _, row in detections.iterrows():
        x_c = (row['xmin'] + row['xmax']) / 2
        y_c = (row['ymin'] + row['ymax']) / 2
        y_sum += y_c
        center_list.append([x_c, y_c, row['char']])

    y_mean = int(y_sum / len(center_list))

    # Tìm điểm trái nhất và phải nhất
    l_point = min(center_list, key=lambda x: x[0])
    r_point = max(center_list, key=lambda x: x[0])

    # Xác định loại biển số: 1 dòng hay 2 dòng
    LP_type = "1"
    for ct in center_list:
        if l_point[0] != r_point[0] and not check_point_linear(ct[0], ct[1], l_point[0], l_point[1], r_point[0], r_point[1]):
            LP_type = "2"
            break

    line_1 = []
    line_2 = []
    license_plate = ""

    if LP_type == "2":
        for c in center_list:
            if int(c[1]) > y_mean:
                line_2.append(c)
            else:
                line_1.append(c)
        for l1 in sorted(line_1, key=lambda x: x[0]):
            license_plate += str(l1[2])
        license_plate += "-"
        for l2 in sorted(line_2, key=lambda x: x[0]):
            license_plate += str(l2[2])
    else:
        for l in sorted(center_list, key=lambda x: x[0]):
            license_plate += str(l[2])

    return license_plate
