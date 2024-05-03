#def first():

import cv2
from sklearn.cluster import KMeans
import numpy as np
import requests
import base64
import json
import os
os.environ["OMP_NUM_THREADS"] = '1'

#a=int(input('准考证号有几位？'))
b,c=map(int,input('准考证号的第几位是班级？（两位之间用空格连接）').split())
# with open ('config.txt','w') as f:
#     f.write(str(b)+'\n')
#     f.write(str(c)+'\n')
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
rightup_point = (rightdown_point[0] - leftdown_point[0] + leftup_point[0], rightdown_point[1] - leftdown_point[1] + leftup_point[1])

docCnt = [leftup_point, leftdown_point, rightdown_point, rightup_point]

points = []
for peak in docCnt:
    cv2.circle(img_open, peak, 10, (0, 0, 255), 2)
    points.append(peak)

# cv2.imshow("a", img_open)
# cv2.waitKey(0)
cv2.imwrite("img_enrode.jpg", img_open)

src = np.array([points[0], points[1], points[2], points[3]], dtype=np.float32)
dst = np.array([[0, 0], [0, 10000], [6000, 10000], [6000, 0]], dtype=np.float32)

m = cv2.getPerspectiveTransform(src, dst)
img_finish = cv2.warpPerspective(img_open, m, (6000, 10000))
cv2.imwrite("img_finish.jpg", img_finish)
img = cv2.warpPerspective(img, m, (6000, 10000))





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
cv2.imwrite('example.jpg',img)
cv2.imwrite('img_cut.jpg',img_cut)

#cv2.waitKey()


xx=list(set(xx))
xx.sort()
print(xx)
def baidu_ocr(image_path, recognize_granularity='small'):
    
    access_token = "24.dc3e85384fb5991797758fac4bb5fe39.2592000.1715675942.282335-48885010"
    
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


#result = baidu_ocr('example.jpg' ,recognize_granularity='small')

#print("OCR Result:", result)

#dict1=result.json()

dict1=result = {'words_result': [{'chars': [{'char': '5', 'location': {'top': 758, 'left': 1034, 'width': 108, 'height': 228}}], 'words': '5', 'location': {'top': 738, 'left': 38, 'width': 1160, 'height': 287}}, {'chars': [{'char': '0', 'location': {'top': 1037, 'left': 2329, 'width': 49, 'height': 96}}], 'words': '0', 'location': {'top': 1022, 'left': 2220, 'width': 263, 'height': 123}}, {'chars': [{'char': '0', 'location': {'top': 1031, 'left': 3058, 'width': 64, 'height': 123}}, {'char': '0', 'location': {'top': 1031, 'left': 3424, 'width': 64, 'height': 123}}], 'words': '00', 'location': {'top': 1031, 'left': 2956, 'width': 626, 'height': 123}}, {'chars': [{'char': '0', 'location': {'top': 1048, 'left': 4154, 'width': 52, 'height': 93}}], 'words': '0', 'location': {'top': 1037, 'left': 4051, 'width': 260, 'height': 117}}, {'chars': [{'char': '0', 'location': {'top': 1037, 'left': 4889, 'width': 73, 'height': 152}}, {'char': '3', 'location': {'top': 1037, 'left': 4974, 'width': 76, 'height': 152}}, {'char': '0', 'location': {'top': 1037, 'left': 5238, 'width': 79, 'height': 152}}, {'char': '3', 'location': {'top': 1037, 'left': 5334, 'width': 79, 'height': 152}}], 'words': '0303', 'location': {'top': 1037, 'left': 4772, 'width': 1218, 'height': 152}}, {'chars': [{'char': '1', 'location': {'top': 1215, 'left': 2332, 'width': 64, 'height': 128}}, {'char': '1', 'location': {'top': 1218, 'left': 2698, 'width': 64, 'height': 125}}, {'char': '1', 'location': {'top': 1221, 'left': 3070, 'width': 64, 'height': 125}}, {'char': '1', 'location': {'top': 1221, 'left': 3427, 'width': 67, 'height': 125}}, {'char': '1', 'location': {'top': 1224, 'left': 3785, 'width': 67, 'height': 125}}, {'char': '1', 'location': {'top': 1227, 'left': 4151, 'width': 64, 'height': 125}}, {'char': '1', 'location': {'top': 1227, 'left': 4523, 'width': 67, 'height': 125}}, {'char': '1', 'location': {'top': 1230, 'left': 4883, 'width': 64, 'height': 125}}], 'words': '11111111', 'location': {'top': 1215, 'left': 2220, 'width': 2824, 'height': 140}}, {'chars': [{'char': '1', 'location': {'top': 1224, 'left': 5258, 'width': 76, 'height': 155}}, {'char': '3', 'location': {'top': 1224, 'left': 5332, 'width': 76, 'height': 155}}], 'words': '13', 'location': {'top': 1224, 'left': 5132, 'width': 793, 'height': 155}}, {'chars': [{'char': '2', 'location': {'top': 1400, 'left': 2695, 'width': 84, 'height': 169}}, {'char': '2', 'location': {'top': 1400, 'left': 3424, 'width': 87, 'height': 169}}, {'char': '2', 'location': {'top': 1400, 'left': 3791, 'width': 84, 'height': 169}}, {'char': '2', 'location': {'top': 1400, 'left': 4145, 'width': 84, 'height': 169}}, {'char': '3', 'location': {'top': 1400, 'left': 4242, 'width': 87, 'height': 169}}, {'char': '2', 'location': {'top': 1400, 'left': 4517, 'width': 90, 'height': 169}}, {'char': '2', 'location': {'top': 1400, 'left': 4883, 'width': 87, 'height': 169}}, {'char': '2', 'location': {'top': 1400, 'left': 5241, 'width': 84, 'height': 169}}], 'words': '22223222', 'location': {'top': 1400, 'left': 2203, 'width': 3726, 'height': 169}}, {'chars': [{'char': '0', 'location': {'top': 1555, 'left': 1807, 'width': 96, 'height': 187}}, {'char': '3', 'location': {'top': 1567, 'left': 2314, 'width': 96, 'height': 187}}, {'char': '3', 'location': {'top': 1567, 'left': 2402, 'width': 96, 'height': 190}}, {'char': '3', 'location': {'top': 1573, 'left': 2701, 'width': 96, 'height': 190}}, {'char': '3', 'location': {'top': 1576, 'left': 2791, 'width': 96, 'height': 187}}, {'char': '3', 'location': {'top': 1582, 'left': 3061, 'width': 96, 'height': 187}}], 'words': '033333', 'location': {'top': 1520, 'left': 0, 'width': 3225, 'height': 249}}, {'chars': [{'char': '3', 'location': {'top': 1611, 'left': 3791, 'width': 73, 'height': 149}}, {'char': '3', 'location': {'top': 1611, 'left': 4166, 'width': 73, 'height': 149}}, {'char': '3', 'location': {'top': 1611, 'left': 4514, 'width': 73, 'height': 149}}, {'char': '3', 'location': {'top': 1611, 'left': 4889, 'width': 73, 'height': 149}}, {'char': '3', 'location': {'top': 1611, 'left': 5264, 'width': 73, 'height': 149}}], 'words': '33333', 'location': {'top': 1611, 'left': 3676, 'width': 2320, 'height': 149}}, {'chars': [{'char': '4', 'location': {'top': 1795, 'left': 2320, 'width': 84, 'height': 166}}, {'char': '3', 'location': {'top': 1795, 'left': 2419, 'width': 84, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 2695, 'width': 84, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 3073, 'width': 82, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 3421, 'width': 82, 'height': 166}}, {'char': '3', 'location': {'top': 1795, 'left': 3515, 'width': 87, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 3793, 'width': 82, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 4168, 'width': 84, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 4517, 'width': 84, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 4883, 'width': 87, 'height': 166}}, {'char': '4', 'location': {'top': 1795, 'left': 5267, 'width': 82, 'height': 166}}], 'words': '43444344444', 'location': {'top': 1795, 'left': 2217, 'width': 3711, 'height': 166}}, {'chars': [{'char': '0', 'location': {'top': 1989, 'left': 1429, 'width': 108, 'height': 205}}, {'char': '5', 'location': {'top': 1989, 'left': 2223, 'width': 108, 'height': 205}}, {'char': '5', 'location': {'top': 1989, 'left': 2320, 'width': 102, 'height': 205}}, {'char': '3', 'location': {'top': 1989, 'left': 2402, 'width': 102, 'height': 205}}, {'char': '5', 'location': {'top': 1989, 'left': 2689, 'width': 102, 'height': 205}}, {'char': '3', 'location': {'top': 1989, 'left': 2768, 'width': 102, 'height': 205}}, {'char': '5', 'location': {'top': 1989, 'left': 3067, 'width': 102, 'height': 205}}, {'char': '3', 'location': {'top': 1989, 'left': 3166, 'width': 102, 'height': 205}}, {'char': '5', 'location': {'top': 1989, 'left': 3430, 'width': 102, 'height': 205}}, {'char': '3', 'location': {'top': 1989, 'left': 3527, 'width': 102, 'height': 205}}, {'char': '5', 'location': {'top': 1989, 'left': 3791, 'width': 102, 'height': 205}}, {'char': '3', 'location': {'top': 1989, 'left': 3881, 'width': 82, 'height': 205}}], 'words': '055353535353', 'location': {'top': 1989, 'left': 0, 'width': 3963, 'height': 205}}, {'chars': [{'char': '5', 'location': {'top': 2000, 'left': 4532, 'width': 73, 'height': 152}}, {'char': '5', 'location': {'top': 2000, 'left': 4889, 'width': 76, 'height': 152}}, {'char': '5', 'location': {'top': 2000, 'left': 5250, 'width': 76, 'height': 152}}, {'char': '3', 'location': {'top': 2000, 'left': 5334, 'width': 79, 'height': 152}}], 'words': '5553', 'location': {'top': 2000, 'left': 4415, 'width': 1514, 'height': 152}}, {'chars': [{'char': '6', 'location': {'top': 2162, 'left': 2329, 'width': 93, 'height': 190}}, {'char': '3', 'location': {'top': 2162, 'left': 2419, 'width': 93, 'height': 190}}, {'char': '6', 'location': {'top': 2162, 'left': 2695, 'width': 93, 'height': 190}}, {'char': '6', 'location': {'top': 2162, 'left': 3055, 'width': 93, 'height': 190}}, {'char': '6', 'location': {'top': 2162, 'left': 3418, 'width': 93, 'height': 190}}, {'char': '6', 'location': {'top': 2162, 'left': 3767, 'width': 99, 'height': 190}}, {'char': '6', 'location': {'top': 2162, 'left': 4145, 'width': 93, 'height': 190}}, {'char': '6', 'location': {'top': 2162, 'left': 4538, 'width': 93, 'height': 190}}, {'char': '3', 'location': {'top': 2162, 'left': 4625, 'width': 93, 'height': 190}}, {'char': '6', 'location': {'top': 2162, 'left': 5258, 'width': 93, 'height': 190}}], 'words': '6366666636', 'location': {'top': 2162, 'left': 2214, 'width': 3717, 'height': 190}}, {'chars': [{'char': '2', 'location': {'top': 2460, 'left': 609, 'width': 70, 'height': 146}}], 'words': '2', 'location': {'top': 2443, 'left': 0, 'width': 1839, 'height': 184}}, {'chars': [{'char': '7', 'location': {'top': 2378, 'left': 2334, 'width': 67, 'height': 125}}, {'char': '7', 'location': {'top': 2378, 'left': 2695, 'width': 67, 'height': 125}}, {'char': '7', 'location': {'top': 2381, 'left': 3064, 'width': 61, 'height': 125}}, {'char': '7', 'location': {'top': 2381, 'left': 3436, 'width': 67, 'height': 125}}, {'char': '7', 'location': {'top': 2384, 'left': 3796, 'width': 67, 'height': 125}}, {'char': '7', 'location': {'top': 2384, 'left': 4157, 'width': 67, 'height': 125}}, {'char': '7', 'location': {'top': 2387, 'left': 4526, 'width': 61, 'height': 125}}, {'char': '7', 'location': {'top': 2387, 'left': 4898, 'width': 67, 'height': 125}}, {'char': '7', 'location': {'top': 2390, 'left': 5258, 'width': 67, 'height': 125}}], 'words': '777777777', 'location': {'top': 2375, 'left': 2223, 'width': 3193, 'height': 140}}, {'chars': [{'char': '8', 'location': {'top': 2569, 'left': 2337, 'width': 73, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 2686, 'width': 79, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 3055, 'width': 76, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 3436, 'width': 76, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 3796, 'width': 76, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 4157, 'width': 73, 'height': 152}}, {'char': '3', 'location': {'top': 2569, 'left': 4245, 'width': 76, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 4538, 'width': 76, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 4898, 'width': 73, 'height': 152}}, {'char': '3', 'location': {'top': 2569, 'left': 4986, 'width': 76, 'height': 152}}, {'char': '8', 'location': {'top': 2569, 'left': 5258, 'width': 76, 'height': 152}}, {'char': '3', 'location': {'top': 2569, 'left': 5343, 'width': 79, 'height': 152}}], 'words': '888888388383', 'location': {'top': 2569, 'left': 2220, 'width': 3714, 'height': 152}}, {'chars': [{'char': '9', 'location': {'top': 2762, 'left': 2337, 'width': 73, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 2695, 'width': 76, 'height': 152}}, {'char': '3', 'location': {'top': 2762, 'left': 2783, 'width': 79, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 3055, 'width': 76, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 3436, 'width': 76, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 3796, 'width': 76, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 4157, 'width': 73, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 4538, 'width': 76, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 4898, 'width': 73, 'height': 152}}, {'char': '9', 'location': {'top': 2762, 'left': 5258, 'width': 76, 'height': 152}}], 'words': '9939999999', 'location': {'top': 2762, 'left': 2223, 'width': 3706, 'height': 152}}, {'chars': [{'char': '0', 'location': {'top': 3363, 'left': 1198, 'width': 67, 'height': 120}}, {'char': '3', 'location': {'top': 3363, 'left': 1529, 'width': 67, 'height': 120}}, {'char': '1', 'location': {'top': 3363, 'left': 1596, 'width': 67, 'height': 120}}, {'char': '0', 'location': {'top': 3363, 'left': 2686, 'width': 70, 'height': 120}}, {'char': '3', 'location': {'top': 3363, 'left': 2771, 'width': 67, 'height': 120}}, {'char': '6', 'location': {'top': 3363, 'left': 3067, 'width': 67, 'height': 120}}, {'char': '1', 'location': {'top': 3363, 'left': 3149, 'width': 70, 'height': 120}}], 'words': '0310361', 'location': {'top': 3363, 'left': 799, 'width': 3585, 'height': 120}}, {'chars': [{'char': '9', 'location': {'top': 3386, 'left': 4731, 'width': 55, 'height': 96}}, {'char': '1', 'location': {'top': 3386, 'left': 4798, 'width': 55, 'height': 96}}], 'words': '91', 'location': {'top': 3386, 'left': 4708, 'width': 1268, 'height': 96}}], 'words_result_num': 20, 'log_id': 1786241836429309806}        


print(dict1)
print(ww)
maxnumber=0
clas=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
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
# with open ('config.txt','a') as f:
#     f.write(str(number_top)+'\n')
#     f.write(str(xx)+'\n')
#     f.write(str(dst))
dst=dst.tolist()
dst.pop(3)
config_dict ={
    'b':b_,
    'c':c_,
    'number_top': number_top,
    'column_location': xx,
    'dst': dst,
    'top':top
}
with open('config.json','w') as f:
    json.dump(config_dict,f)

