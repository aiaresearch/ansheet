import json
import numpy as np
import cv2
# f=open('config.txt','r')
# lines=f.readlines()
# b=lines[0]
# c=lines[1]
# number_top=lines[2]
# column_location=lines[3]
# dst=lines[4:7]
# f.close()
# print(dst)
with open('config.json','r') as f:
    config= json.load(f)
f.close()
b=config['b']
c=config['c']
number_top=config['number_top']
column_location=config['column_location']
dstlist=config['dst']
dst=np.array(dstlist, dtype=np.float32)
top=config['top']



img=cv2.imread('img.jpg')
img=cv2.pyrDown(img)
#img=cv2.pyrDown(img)
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_binary=img_thre=cv2.adaptiveThreshold(img_gray,100,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,31,30)
kernel=np.ones((3,3),np.uint8)
#img_open=cv2.morphologyEx(img_binary,cv2.MORPH_OPEN,kernel)
img_open=(cv2.dilate(img_binary,kernel,iterations=3))
img_open=(cv2.erode(img_open,kernel,iterations=3))

contours,hierarchy=cv2.findContours(img_open,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
#img_open=cv2.bitwise_not(img_open)
xx=[]
yy=[]
locations=[]

for contour in contours:
    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    if w > h and w > 10 and w < 150 and h < 150:
        #cv2.rectangle(img_open, (x, y), (x + w, y + h), (0, 0, 255), 1)
        locations.append((x, y))
        xx.append(x)
        yy.append(y)

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

src = np.array([points[0], points[1], points[2], ], dtype=np.float32)

m = cv2.getAffineTransform(src, dst)
locations=np.array(locations,dtype=np.float32)

print(locations)

locations=cv2.transform(locations.reshape(1, -1, 2),m)

locations=locations.tolist()[0]
print(locations)
locations=[location for location in locations if location[1]<top]
#
img_open = cv2.warpAffine(img_open, m,tuple(map(int,tuple(dstlist[2]))))
img_finish=img_open[0:top]
cv2.imwrite("img_finish.jpg", img_finish)
#



