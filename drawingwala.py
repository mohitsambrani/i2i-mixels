import cv2
import time
import threading
import DobotDllType as dType
import numpy as np



CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])





cap=cv2.imread('pika2.jpg',0)
cv2.imshow('asdsa',cap)
ret,thresh1 = cv2.threshold(cap,200,255,cv2.THRESH_BINARY)

resized=cv2.resize(thresh1,(400,300))
cv2.imshow('asd',resized)

count=0
ZZZ=[]
YYY=0
def fill(resized, start_coords, fill_value):
    global YYY 
    
    xsize, ysize = resized.shape
    orig_value = resized[start_coords[0], start_coords[1]]
    
    stack = set(((start_coords[0], start_coords[1]),))
    if fill_value == orig_value:
        raise ValueError("Filling region with same value "
                        "already present is unsupported. "
                        "Did you already fill this region?")
    
    while stack:
        x, y = stack.pop()
            
        if resized[x, y] == orig_value:
            resized[x, y] = fill_value
            ZZZ[YYY].append((x,y))
            if x > 0:
                stack.add((x - 1, y))
            if x < (xsize - 1):
                stack.add((x + 1, y))
            if y > 0:
                stack.add((x, y - 1))
            if y < (ysize - 1):
                stack.add((x, y + 1))
    YYY=YYY+1


for i in range(300):
    for j in range(400):
            
        if(resized[i,j]==0):
            ZZZ.append([])
            fill(resized,[i,j],255)
            print(i,j)
            count=count+1
            print(count)
print(len(ZZZ))
if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 0, 136, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetPTPJumpParams(api,7,-40,isQueued=1)
    count=0
    for i in range(0,len(ZZZ)-1):
        
        for j in range(0,len(ZZZ[i])-1):
            if(j==0):
                count=count+1;
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 300-(float(ZZZ[i][j][0])*50/float(300)), 80-(float(ZZZ[i][j][1])*50/400), -59, 0, isQueued = 1)[0]
            else:
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 300-(float(ZZZ[i][j][0])*50/float(300)), 80-(float(ZZZ[i][j][1])*50/400), -59, 0, isQueued = 1)[0]
                count=count+1
            if(count%25==0):
                dType.SetQueuedCmdStartExec(api)

                #Wait for Executing Last Command 
                while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                    dType.dSleep(100)
		
                #Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(api)
                dType.SetQueuedCmdClear(api)
                count=0




    #Start to Execute Command Queued
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
		
    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)
    
print("blah")
#Disconnect Dobot
dType.DisconnectDobot(api)

cv2.imshow("asdad",resized)
cv2.waitKey(0)
