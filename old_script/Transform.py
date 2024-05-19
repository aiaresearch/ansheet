import cv2
import numpy as np

def transform1(locations,img_open,img):
    
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
    img2 = cv2.warpPerspective(img, m, (ww, hh))
    cv2.imwrite("img.jpg",img2)
    return img2,img_finish,dst






def transform2(locations,top,dstlist,img_open):
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
    locations=[location for location in locations if location[1]<top]
    #
    img_open = cv2.warpAffine(img_open, m,tuple(map(int,tuple(dstlist[2]))))
    img_finish=img_open[0:top]
    cv2.imwrite("img_finish.jpg", img_finish)
    return locations