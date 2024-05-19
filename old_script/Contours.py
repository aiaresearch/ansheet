import cv2

def find_contours(img_open):
    contours,hierarchy=cv2.findContours(img_open,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    #img_open=cv2.bitwise_not(img_open)
    xx=[]
    yy=[]
    locations=[]
    ww=[]

    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        if w > h and w > 10 and w < 150 and h < 150:
            #cv2.rectangle(img_open, (x, y), (x + w, y + h), (0, 0, 255), 1)
            locations.append((x, y))
            xx.append(x)
            yy.append(y)
            ww.append(w)
    return xx,yy,locations,ww,h

if __name__=='__main__':
    find_contours()