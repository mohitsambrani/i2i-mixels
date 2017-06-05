import cv2
from operator import itemgetter
img2=cv2.imread("1.png")
img1=cv2.imread("1.png",0)

_,img=cv2.threshold(img1,40,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
area=[]
for cnt in contours:
    area.append(int(cv2.contourArea(cnt)))
area.sort(reverse=True)
for cnt in contours:
    if(area[0]==int(cv2.contourArea(cnt))):
        cnt1=cnt
cnt=cnt1
cv2.imshow("wr",img2)
M=cv2.moments(cnt)
cx=int(M["m10"]/M["m00"])
cy=int(M["m01"]/M["m00"])
cv2.circle(img2, (cx, cy), 7, (0, 0, 255), -1)
cv2.imshow("ads",img2)
cv2.waitKey(0)
