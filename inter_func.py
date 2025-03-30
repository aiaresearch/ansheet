import cv2
import numpy as np
# import inter_class as it
import tkinter as tk
import os
import requests
import base64
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from classificate import process_data
import json

PROJECT_PATH="."
IMG_NAME="img2.jpg"
#change the access token to yours
access_token="24.2c19f62013baddbeb646c9d2546154f4.2592000.1744906016.282335-48885010"

def img_preprocess(img):

    img=cv2.copyMakeBorder(img,10,10,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
    h, w = img.shape[0], img.shape[1]
    img=img[:,20:w-20]
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,img_binary=cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    #cv2.imwrite('a.jpg',img_binary)
    size=int((h+w)/3000)
    kernel=np.ones((size,size),np.uint8)
    #img_open=cv2.morphologyEx(img_binary,cv2.MORPH_OPEN,kernel)
    img_open=(cv2.dilate(img_binary,kernel,iterations=5))
    img_open=(cv2.erode(img_open,kernel,iterations=5))

    return img,img_open,h,w

def find_contours(img_open,height,width):
    contours,hierarchy=cv2.findContours(img_open,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    #img_open=cv2.bitwise_not(img_open)
    xx=[]
    yy=[]
    locations=[]
    ww=[]

    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        # cv2.rectangle(img_open, (x, y), (x + w, y + h), (0, 0, 255), 1)
        if w > (width/90) and w < width/30 and h < height/12:
            cv2.rectangle(img_open, (x, y), (x + w, y + h), (0, 0, 255), 1)
            locations.append((x, y))
            xx.append(x)
            yy.append(y)
            ww.append(w)
    # cv2.pyrDown(img_open)
    # cv2.imshow("img", img_open)
    # cv2.waitKey(0)
    return xx,yy,locations,ww,h

def transform1(locations, img_open, img):
    leftup = (float('inf'), (-1, -1))
    rightdown = (0, (-1, -1))
    leftdown = (float('inf'), (-1, -1))
    height, _ = img_open.shape

    for loc in locations:
        distance_squared = loc[0] ** 2 + loc[1] ** 2
        if distance_squared < leftup[0]:
            leftup = (distance_squared, loc)
        if distance_squared > rightdown[0]:
            rightdown = (distance_squared, loc)
        distance_squared = loc[0] ** 2 + (loc[1] - height) ** 2
        if distance_squared < leftdown[0]:
            leftdown = (distance_squared, loc)

    leftup_point = leftup[1]
    rightdown_point = rightdown[1]
    leftdown_point = leftdown[1]
    rightup_point = (
    rightdown_point[0] - leftdown_point[0] + leftup_point[0], rightdown_point[1] - leftdown_point[1] + leftup_point[1])

    hh = int(pow((leftup_point[0] - leftdown_point[0]) ** 2 + (leftup_point[1] - leftdown_point[1]) ** 2, 0.5))
    ww = int(pow((leftdown_point[0] - rightdown_point[0]) ** 2 + (leftdown_point[1] - rightdown_point[1]) ** 2, 0.5))

    docCnt = [leftup_point, leftdown_point, rightdown_point, rightup_point]

    points = []
    for peak in docCnt:
        cv2.circle(img_open, peak, 10, (0, 0, 255), 2)
        points.append(peak)

    # cv2.imshow("a", img_open)
    # cv2.waitKey(0)
    cv2.imwrite(os.path.join(PROJECT_PATH,"image/img_enrode.jpg"), img_open)

    src = np.array([points[0], points[1], points[2], points[3]], dtype=np.float32)
    dst = np.array([[0, 0], [0, hh], [ww, hh], [ww, 0]], dtype=np.float32)

    m = cv2.getPerspectiveTransform(src, dst)
    img_finish = cv2.warpPerspective(img_open, m, (ww, hh))
    cv2.imwrite("image/img_finish.jpg", img_finish)
    img2 = cv2.warpPerspective(img, m, (ww, hh))
    cv2.imwrite("img.jpg", img2)
    return img2, img_finish, dst

def transform2(locations,rect,dstlist,img_open):
    x_begin,y_begin,x_end,y_end=rect
    dst=np.array(dstlist, dtype=np.float32)
    leftup = (float('inf'), (-1, -1))
    rightdown = (0, (-1, -1))
    leftdown = (float('inf'), (-1, -1))
    height,_ = img_open.shape

    for loc in locations:
        distance_squared = loc[0] ** 2 + loc[1] ** 2
        if distance_squared < leftup[0]:
            leftup = (distance_squared, loc)
        if distance_squared > rightdown[0]:
            rightdown = (distance_squared, loc)
        distance_squared = loc[0] ** 2 + (loc[1] - height) ** 2
        if distance_squared < leftdown[0]:
            leftdown = (distance_squared, loc)

    leftup_point = leftup[1]
    rightdown_point = rightdown[1]
    leftdown_point = leftdown[1]
    docCnt = [leftup_point, leftdown_point, rightdown_point]

    points = []
    for peak in docCnt:
        cv2.circle(img_open, peak, 10, (0, 0, 255), 2)
        points.append(peak)

    # cv2.imshow("a", img_open)
    # cv2.waitKey(0)
    cv2.imwrite("img_enrode.jpg", img_open)

    src = np.array([points[0], points[1], points[2] ], dtype=np.float32)

    m = cv2.getAffineTransform(src, dst)
    locations=np.array(locations,dtype=np.float32)

    print(locations)

    locations=cv2.transform(locations.reshape(1, -1, 2),m)

    locations=locations.tolist()[0]
    print(locations)
    locations=[location for location in locations if (y_begin<location[1]<y_end and x_begin<location[0]<x_end)]
    #
    img_open = cv2.warpAffine(img_open, m,tuple(map(int,tuple(dstlist[2]))))
    img_finish=img_open[y_begin:y_end,x_begin:x_end]
    cv2.imwrite("img_finish.jpg", img_finish)
    return locations
# path='./ansheet/image/img2.jpg'
def baidu_ocr(image_path, access_token,recognize_granularity="small"):

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {
        "access_token": access_token,
        "recognize_granularity": recognize_granularity,
    }
    with open(image_path, "rb") as file:
        image_data = file.read()
    image_base64 = base64.b64encode(image_data).decode()
    data = {"image": image_base64}

    # Send OCR request
    response = requests.post(url, headers=headers, params=params, data=data)
    return response

def write_json(dst,b,c,number_top,xx,rect,ww):
    dst=dst.tolist()
    dst.pop(3)
    config_dict ={
        'b':b,
        'c':c,
        'number_top': number_top,
        'column_location': xx,
        'dst': dst,
        'rect':rect,
        'w':ww[-1]
    }
    with open('config.json','w') as f:
        json.dump(config_dict,f)
def read_json():
    with open('config.json','r') as f:
        config= json.load(f)
    f.close()
    b=config['b']
    c=config['c']
    number_top=config['number_top']
    column_location=config['column_location']
    dstlist=config['dst']
    dst=np.array(dstlist, dtype=np.float32)
    rect=config['rect']
    W=config['w']
    return b,c,number_top,column_location,dstlist,dst,rect,W

def function_a():
    global height,width,img_per,img_cnt_per
    img=cv2.imread(os.path.join("./ansheet/image",IMG_NAME))
    img,img_open,height,width=img_preprocess(img)

    # cv2.imshow("img", img_open)
    cv2.waitKey(0)
    _,_,locations, _, _ = find_contours(img_open,height, width)

    img_per, img_cnt_per, dst = transform1(locations, img_open, img)
    # cv2.imshow("img_per", img_per)
    # cv2.imshow("img_cnt_per", img_cnt_per)
    cv2.waitKey(0)

    path="./ansheet/image/img_per.jpg"
    cv2.imwrite(path, img_per)


    return path,dst

def function_b(data,dst):
    global height,width,img_per,img_cnt_per
    num_digits=data['num_digits']
    b,c=data['class_range'][0],data['class_range'][1]
    x_begin,y_begin,x_end,y_end=rect=data['rectangles'][0]
    img_cut=img_per[y_begin:y_end,x_begin:x_end]
    img_cnt_cut=img_cnt_per[y_begin:y_end,x_begin:x_end]
    cv2.imwrite("./ansheet/image/img_cut.jpg", img_cut)
    xx, yy, locations, ww, h = find_contours(img_cnt_cut, height, width)
    xx = list(set(xx))
    xx.sort()
    result=baidu_ocr("./ansheet/image/img_cut.jpg",access_token)
    dict1=result.json()
    print(dict1)
    number_left_list,number_top_list=process_data(dict1,num_digits)
    # close()
    write_json(dst,b,c,number_left_list,number_top_list,rect,ww)



# def function_b(data):
#     # 示例：显示收集到的数据
#     print("传递给函数b的数据：")
#     print(f"准考证位数：{data['num_digits']}")
#     print(f"班级信息段：{data['class_range'][0]}-{data['class_range'][1]}")
#     print("框选区域坐标：")
#     for i, rect in enumerate(data['rectangles']):
#         print(f"区域{i + 1}: {rect}")


# if __name__=='__main__':
#     global img_per, img_cnt_per
#     root = tk.Tk()
#     app = it.MainApp(root)
#     root.mainloop()
if __name__ == '__main__':
    _,dst=function_a()
    function_b({'rectangles': [(987, 385, 2578, 1317)], 'num_digits': 8, 'class_range': (5, 6)},dst)