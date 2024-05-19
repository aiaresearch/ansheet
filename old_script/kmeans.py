import cv2
from sklearn.cluster import KMeans
import numpy as np

def kmeans(xx,yy,locations,ww,h,img):
    img_finish=cv2.imread('image/img_finish.jpg')
    y=km_model = KMeans(n_clusters=2,n_init=1,init=np.array([[img.shape[1]/2, 0], [img.shape[1]/2, img.shape[0]]])).fit(locations)

    labels = y.labels_

    #print(xx)
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

    return xx,ww,top
