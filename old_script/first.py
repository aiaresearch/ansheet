import cv2
from sklearn.cluster import KMeans
import numpy as np
import requests
import base64
import json
import os
os.environ["OMP_NUM_THREADS"] = '1'


b,c=map(int,input('准考证号的第几位是班级？（两位之间用空格连接）').split())
img=cv2.imread('image/bigscan.png')
img=cv2.pyrDown(img)
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
rightup_point = (rightdown_point[0] - leftdown_point[0] + leftup_point[0], rightdown_point[1] - leftdown_point[1] + leftup_point[1])

hh=int(pow((leftup_point[0]-leftdown_point[0])**2+(leftup_point[1]-leftdown_point[1])**2,0.5))
ww=int(pow((leftdown_point[0]-rightdown_point[0])**2+(leftdown_point[1]-rightdown_point[1])**2,0.5))

docCnt = [leftup_point, leftdown_point, rightdown_point, rightup_point]

points = []
for peak in docCnt:
    cv2.circle(img_open, peak, 10, (0, 0, 255), 2)
    points.append(peak)

# cv2.imshow("a", img_open)
# cv2.waitKey(0)
cv2.imwrite("image/img_enrode.jpg", img_open)

src = np.array([points[0], points[1], points[2], points[3]], dtype=np.float32)
dst = np.array([[0, 0], [0, hh], [ww, hh], [ww, 0]], dtype=np.float32)

m = cv2.getPerspectiveTransform(src, dst)
img_finish = cv2.warpPerspective(img_open, m, (ww, hh))
cv2.imwrite("image/img_finish.jpg", img_finish)
img = cv2.warpPerspective(img, m, (ww, hh))





locations.clear()
xx.clear()
yy.clear()
ww=[]
contours2,hierarchy=cv2.findContours(img_finish,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
for cnt in contours2:
    x,y,w,h=cv2.boundingRect(cnt)
    if w>h and w<300 and h<300:
        cv2.rectangle(img_finish,(x,y),(x+w,y+h),(0,0,255),1)
        locations.append((x,y))
        ww.append(w)
        xx.append(x)
        yy.append(y)



y=km_model = KMeans(n_clusters=2,n_init=1,init=np.array([[img.shape[1]/2, 0], [img.shape[1]/2, img.shape[0]]])).fit(locations)

labels = y.labels_



print(xx)
top=img_finish.shape[0]
new=[]
for i in range(0,len(labels)):
    new.append([locations[i],labels[i]])
    if labels[i]==0:
        _str='0'
        
    else:
        _str='1'
        del ww[xx.index(locations[i][0])]
        xx.remove(locations[i][0])
        if yy[i]<top:
            top=yy[i]+h
    cv2.putText(img_finish,_str,locations[i],1,1,(255,0,0))
ww.sort()
cv2.imshow('img',img_finish)
cv2.waitKey()

img_cut=img_finish[0:top,:]
img=img[0:top,:]
cv2.imwrite('image/example.jpg',img)
cv2.imwrite('image/img_cut.jpg',img_cut)

#cv2.waitKey()


xx=list(set(xx))
xx.sort()
print(xx)
def baidu_ocr(image_path, recognize_granularity='small'):
    
    access_token ="24.d68733a3c57e2020f01cf4ce17f83635.2592000.1718528425.282335-48885010"
    
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'access_token': access_token, 'recognize_granularity': recognize_granularity}
    with open(image_path, 'rb') as file:
        image_data = file.read()
    image_base64 = base64.b64encode(image_data).decode()
    data = {'image': image_base64}
    
    # Send OCR request
    response = requests.post(url, headers=headers, params=params, data=data)
    return response


result = baidu_ocr('image/example.jpg' ,recognize_granularity='small')

#print("OCR Result:", result)

dict1=result.json()



print(dict1)
print(ww)
maxnumber=0
clas=[]
for i in range(len(xx)):
    clas.append([])
where=[[],[],[],[],[],[],[],[],[],[]]
numbers=['0','2','3','4','5','6','7','8','9']
list0=dict1['words_result']
for i in range(0,len(list0)):
    list0_5=list0[i].get('chars')
    same_words=list0[i].get('words')
    if len(same_words)!=1:
        maxcount=0
        frequency=[[],[],[],[],[],[],[],[],[],[]]
        for i in range(0,10):
            number=str(i)
            if same_words.count(number)>0:
                if same_words.count(number)>maxcount:
                    maxcount=same_words.count(number)
                frequency[i].append(same_words.count(number))
        truenumber=str(frequency.index([maxcount]))
        # for j in range(0,len(list0_5)):
        #     list0_5[j]['char']=truenumber
    else:
        truenumber=same_words
        
   
    for j in range(0,len(list0_5)):
        str_=list0_5[j].get('char')
        if str_!=truenumber:
            pass
        else:
            for number in numbers:
                if str_.find(number)!= -1:
                #print(number)
                    where[int(number)].append(list0_5[j].get('location'))
                    if int(number)>maxnumber:
                        maxnumber=int(number)
                    for x in xx:
                        if list0_5[j].get('location').get('left') in range(x,x+ww[-1]):
                            if clas[xx.index(x)]==[]:
                                clas[xx.index(x)].append(number)
                            elif int(str_)>int(clas [xx.index(x)][-1]):
                                clas[xx.index(x)].append(number)

print(clas)
column=[member for member in clas if len(member)>maxnumber-2]
print(column)



ii=[i for i in range(0,len(clas)) if clas[i] not in column]
ii.sort(reverse=True)
for i in ii:
    if i+1>len(xx):
        pass
    else:
        xx.pop(i)
#print(where)
print(len(xx))
print(len(column))

listb=[]
listb0=column[b-1]
for i in range(0,maxnumber+1):
    i=str(i)
    if listb0.count(i)==0:
        listb.append(i)

if listb!=[1]:
    for item in listb:
        if where[int(item)]!=[] and item!='1':
            b_=int(item)
else:
    b_=1



listc=[]
listc0=column[c-1]
for i in range(0,10):
    i=str(i)
    if listc0.count(i)==0:
        listc.append(i)

if listc!=[1]:
    for item in listc:
        if where[int(item)]!=[] and item!='1':
            c_=int(item)
else:
    c_=1

print('班级:',b_,c_,sep='')

number_top=[]
for element in where:
    if element==[]:
        number_top.append(0)
    else:
        number_top.append(element[1].get('top'))
number_top[1]=(number_top[0]+number_top[2])//2

dst=dst.tolist()
dst.pop(3)
config_dict ={
    'b':b,
    'c':c,
    'number_top': number_top,
    'column_location': xx,
    'dst': dst,
    'top':top,
    'w':ww[-1]
}
with open('config.json','w') as f:
    json.dump(config_dict,f)