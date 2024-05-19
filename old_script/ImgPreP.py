import cv2
import numpy as np

def img_preprocess(img):
    img=cv2.pyrDown(img)
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_binary=img_thre=cv2.adaptiveThreshold(img_gray,100,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,31,30)


    kernel=np.ones((3,3),np.uint8)
    #img_open=cv2.morphologyEx(img_binary,cv2.MORPH_OPEN,kernel)
    img_open=(cv2.dilate(img_binary,kernel,iterations=3))
    img_open=(cv2.erode(img_open,kernel,iterations=3))
    cv2.imwrite('image/img_open.jpg',img_open)
    return img,img_open

if __name__ =="__main__":
    img_preprocess('image/img.jpg')