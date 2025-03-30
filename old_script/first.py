import cv2
from sklearn.cluster import KMeans
import numpy as np
import requests
import base64
import json
import os
os.environ["OMP_NUM_THREADS"] = '1'


b,c=5,6#map(int,input('准考证号的第几位是班级？（两位之间用空格连接）').split())
n=8
img=cv2.imread('image/img1.jpg')
#img=cv2.pyrDown(img)
img=cv2.copyMakeBorder(img,4,4,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
img=img[:,20:img.shape[1]-20]
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#img_binary=img_thre=cv2.adaptiveThreshold(img_gray,100,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,31,30)
_,img_binary=cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
cv2.imwrite('a.jpg',img_binary)
h,w,l=img.shape

kernel=np.ones((int((h+w)/350),int((h+w)/350)),np.uint8)
#img_open=cv2.morphologyEx(img_binary,cv2.MORPH_OPEN,kernel)
img_open=(cv2.dilate(img_binary,kernel,iterations=2))
img_open=(cv2.erode(img_open,kernel,iterations=2))
cv2.imshow('a',img_open)
cv2.waitKey()

contours,hierarchy=cv2.findContours(img_open,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

#img_open=cv2.bitwise_not(img_open)
xx=[]
yy=[]
locations=[]

for contour in contours:
    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    if  w > 10 and w < 100 and h < 100:
        cv2.rectangle(img_open, (x, y), (x + w, y + h), (0, 0, 255), 1)
        locations.append((x, y))
        xx.append(x)
        yy.append(y)
cv2.imwrite('contours.jpg',img_open)
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
        cv2.rectangle(img_finish,(x,y),(x+w,y+h),(100,100,100),1)
        locations.append((x,y))
        ww.append(w)
        xx.append(x)
        yy.append(y)



locations_arr=np.array([xx,yy])
locations_arr=locations_arr.T
print(locations_arr)
# locations_arr=locations_arr.reshape((len(locations),2))
# print(locations_arr)
print(locations)
middle=np.median(yy)
print(middle)
top=0
print('start:',len(locations))
print(len(locations))
for i in range(len(locations)-1,-1,-1):
    if locations_arr[i][1]>1.5*middle:
        print(locations[i])
        print(locations_arr[i][1])
        locations.pop(i)
        locations_arr=np.delete(locations_arr,i,0)
        xx.pop(i)
        yy.pop(i)
        ww.pop(i)
    else:
        locations_arr[i][1]=500*locations[i][1]
        if yy[i]>top:
            top=yy[i]
print('end:',len(locations))
print(len(locations))

# for location in locations:
#     cv2.putText(img_finish,str(location),location,1,1,(100,100,100),1,1)
# cv2.imwrite('test.jpg',img_finish)


y=km_model = KMeans(n_clusters=2,n_init=1,init=[(img.shape[1]/2,0),(img.shape[1]/2,top)]).fit(locations_arr)
# print(np.array([[img.shape[1]/2, 0], [img.shape[1]/2, top]]))
labels = y.labels_
centers=y.cluster_centers_
print(centers)
if (locations[0][0]-centers[0][0])**2+(locations[0][1]-centers[0][1])**2>(locations[0][0]-centers[1][0])**2+(locations[0][1]-centers[1][1])**2:
    if centers[1][1]>centers[0][1]:
        up=labels[0]
    else:
        up=abs(labels[0]-1)
else:
    if centers[1][1]>centers[0][1]:
        up=abs(labels[0]-1)
    else:
        up=labels[0]

print(xx)
new=[]
for i in range(0,len(labels)):
    new.append([locations[i],labels[i]])
    if labels[i]==up:
        _str='0'
        
    else:
        _str='1'
        del ww[xx.index(locations[i][0])]
        xx.remove(locations[i][0])
        if yy[i]<top:
            top=yy[i]+h
    cv2.putText(img_finish,_str,locations[i],1,2,(0,0,0),4)
ww.sort()
cv2.imwrite('kmeans.jpg',img_finish)



# cv2.imshow('img',img_finish)
# cv2.waitKey()

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
all_top=[]
for i in range(0,len(list0)):
    list0_5=list0[i].get('chars')
    same_words=list0[i].get('words')
    for j in range(len(list0_5)):
        a=list0_5[j].get('location').get('top')
        all_top.append(a)
median=np.median(all_top)
for i in range(len(list0)):
    list0_5=list0[i].get('chars')
    same_words=list0[i].get('words')
    general_top=list0[i].get('location').get('top')
    if general_top<median-6*ww[-1] or general_top>median+6*ww[-1] :
        truenumber=-1
    elif len(same_words)!=1:
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
        if truenumber==-1:
            pass
        
        elif str_!=truenumber:
            pass
        else:
            for number in numbers:
                if str_.find(number)!= -1:
                #print(number)
                    where[int(number)].append(list0_5[j].get('location'))
                    if int(number)>maxnumber:
                        maxnumber=int(number)
                    for x in xx:
                        if list0_5[j].get('location').get('left') in range(x-int(0.2*ww[-1]),x+int(1.2*ww[-1])):
                            if clas[xx.index(x)]==[]:
                                clas[xx.index(x)].append(number)
                                print(number)
                            elif int(str_)>int(clas [xx.index(x)][-1]):
                                clas[xx.index(x)].append(number)

print(clas)
column=[member for member in clas if len(member)>maxnumber-2]
print(column)
print(where)


ii=[i for i in range(0,len(clas)) if clas[i] not in column]
ii.sort(reverse=True)
for i in ii:
    if i+1>len(xx):
        pass
    else:
        xx.pop(i)
#print(where)
print(xx)
print(column)
print(len(xx))
if len(xx) > n:
    number=len(xx)-n
    difference=[]
    for i in range(len(xx)):
        j=i+1
        if i == len(xx)-1:
            break
        diff=xx[j]-xx[i]
        difference.append(diff)
    mid=np.median(difference)
    for i in range(len(xx)-2,-1,-1):
        if difference[i]<0.8*mid:
            print(xx[i])
            xx.pop(i)
            print(column[i])
            column.pop(i)
            number-=1
            if number==0:
                break
            
print('remove result:',len(xx))

    

print(len(column))

listb=[]
listb0=column[b-1]
for i in range(maxnumber+1):
    i=str(i)
    if listb0.count(i)==0:
        listb.append(i)

b_=1
if listb!=[1]:
    for item in listb:
        if where[int(item)]!=[] and item!='1':
            b_=int(item)

listc=[]
listc0=column[c-1]
for i in range(0,10):
    i=str(i)
    if listc0.count(i)==0:
        listc.append(i)

c_=1
if listc!=[1]:
    for item in listc:
        if where[int(item)]!=[] and item!='1':
            c_=int(item)


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