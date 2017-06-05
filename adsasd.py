import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
cap = cv2.VideoCapture(0)
ret, img=cap.read()
cv2.namedWindow('image')
cv2.imshow('img',img)
x,y,_=img.shape

# Create trackbars for color change
cv2.createTrackbar('X','image',50,x-50,nothing)
cv2.createTrackbar('X2','image',60,x-60,nothing)
cv2.createTrackbar('Y','image',50,y-50,nothing)
cv2.createTrackbar('Y2','image',60,y-60,nothing)


while(1):
    cv2.imshow('image',img)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # Get current positions of four trackbars
    r = cv2.getTrackbarPos('X','image')
    g = cv2.getTrackbarPos('X2','image')
    b = cv2.getTrackbarPos('Y','image')
    s = cv2.getTrackbarPos('Y2','image')
    imgnew=img[r:g,b:s]
    cv2.imshow("img_new",imgnew)
    cv2.imshow("img",img)
    

cv2.destroyAllWindows()
