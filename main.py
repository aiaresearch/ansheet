import function, OCR, scan,ser
import argparse
import cv2
from sklearn.cluster import KMeans
import numpy as np
import requests
import base64
import json
import os
import ser
import time
import sane


def first(args):
    os.environ["OMP_NUM_THREADS"] = "1"
    dev = scan.init()
    scan.scan(dev)
    img = cv2.imread(args.path)
    img, img_open = function.img_preprocess(img)
    xx, yy, locations, _, _ = function.find_contours(img_open)
    img, img_finish, dst = function.transform1(locations, img_open, img)
    xx, yy, locations, ww, h = function.find_contours(img_finish)
    xx, ww, top = function.kmeans(xx, yy, locations, ww, h, img)
    xx = list(set(xx))
    xx.sort()
    result = OCR.baidu_ocr("image/example.jpg", recognize_granularity="small")
    dict1 = result.json()
    xx, number_top = function.classificate(dict1, xx, args.b, args.c, ww)
    # close()
    function.write_json(dst, args.b, args.c, number_top, xx, top, ww)
    # serial()
    dev.close()


def repair(args):
    dev = scan.init()
    

    b, c, number_top, column_location, dstlist, dst, top, W = function.read_json()
    class_ = []
    serial_ = []
    ser.set_motor(True)
    ser.reset_all_servo()
    # img = cv2.imread(args.path)
    # img_open = function.img_preprocess(img)
    # xx, yy, locations, _, _ = function.find_contours(img_open)
    # locations = function.transform2(locations, top, dstlist, img_open)
    # cls_nmb = function.compare(locations, column_location, W, number_top, b, c)
    # ser.write(98)
    # ser.write(101)

    for i in range(args.frequency):
        scan.scan(dev)
        img = cv2.imread(args.path)
        img,img_open = function.img_preprocess(img)
        xx, yy, locations, _, _ = function.find_contours(img_open)
        locations = function.transform2(locations, top, dstlist, img_open)
        print(locations)
        cls_nmb = function.compare(locations, column_location, W, number_top, b, c)
        if cls_nmb==1:
            try:
                # 发送字符'a'到串口
                ser.serial_write(1)
                #time.sleep(8)
                #ser.reset_all_servo()
            except Exception as e:
                print("Error:", e)
        elif cls_nmb==2:
            try:
                # 发送字符'a'到串口
                ser.serial_write(2)
                #time.sleep(8)
                #ser.reset_all_servo()
            except Exception as e:
                print("Error:", e)
        else:
            try:
                # 发送字符'a'到串口
                ser.serial_write(2)
                #time.sleep(8)
                #ser.reset_all_servo()
            except Exception as e:
                print("Error:", e)
        # if class_ == []:
        #     class_.append(cls_nmb)
        #     serial_.append(2)
        #     try:
        #         # 发送字符'a'到串口
        #         ser.serial_write(1)
        #         #time.sleep(8)
        #         ser.reset_all_servo()
        #     except Exception as e:
        #         print("Error:", e)
        # elif class_(cls_nmb) != -1:
        #     try:
        #         ser.serial_write(serial_[class_.index(cls_nmb)])
        #         print("Sent", serial_[class_.index(cls_nmb)], "over serial", sep="")
        #         #time.sleep(8)
        #         ser.reset_all_servo()
        #     except Exception as e:
        #         print("Error:", e)
        # else:

        #     class_.append(cls_nmb)
        #     serial_.append(serial_[-1] + 1)
        #     try:
        #         ser.serial_write(serial_[-1])
        #         print("Sent", input, "over serial", sep="")
        #         #time.sleep(8)
        #         ser.reset_all_servo()
        #     except Exception as e:
        #         print("Error:", e)
        time.sleep(3)
    time.sleep(5)
    ser.raise_all_servo()

    dev.close()
    ser.set_motor(False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="arguments")
    parser.add_argument(
        "-m",
        type=int,
        required=True,
        help="'1' for first mode,'2' for repair mode",
    )
    parser.add_argument("--path", type=str, default="image/img.jpg", help="image path")
    parser.add_argument(
        "--b", type=int, default=5, help="the sequence of class information"
    )
    parser.add_argument(
        "--c", type=int, default=6, help="the sequence of class information"
    )
    parser.add_argument("--port", type=str, help="serial port")
    parser.add_argument(
        "--frequency",
        "-f",
        type=int,
        default=5,
        help="the approximately number of ansheets to classificate",
    )
    args = parser.parse_args()

    # first
    if args.mode == 1:
        first(args)

    elif args.mode == 2:
        repair(args)

    else:
        print("Mode number out of range.Please input '1' or '2'.")
