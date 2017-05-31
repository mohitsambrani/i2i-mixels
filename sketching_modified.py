import cv2
import time
import threading
import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])



cap=cv2.imread('index.jpg',0)
cv2.imshow('asdsa',cap)
ret,thresh1 = cv2.threshold(cap,127,255,cv2.THRESH_BINARY)
resized=cv2.resize(thresh1,(336,300))
cv2.imshow('asd',resized)
    
if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 0, 136, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetPTPJumpParams(api,4,-40,isQueued=1)

    count=0
    k=0
    for i in range(0,299):
        for j in range(0,335):
            
            if(resized[i,j]==0 and resized[i,j+1]==0 and resized[i,j-1]==0 and (j+1)<336 and (j-1)>0):
                k=j;
                
                
                while(resized[i,k]==0):
                    k=k+1
                    if(k>335):
                        break
                j=k-1
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 300-((float(i*30)/float(300))), 80-((float(j*33.6)/float(336))), -58, 0, isQueued = 1)[0]
                
                count=count+1

            elif(resized[i,j]==0):
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 300-((float(i*30)/float(300))), 80-((float(j*33.6)/float(336))), -58, 0, isQueued = 1)[0]
                count=count+1
            if(count==25):
                dType.SetQueuedCmdStartExec(api)

                #Wait for Executing Last Command 
                while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                    dType.dSleep(100)
		
                #Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(api)
                dType.SetQueuedCmdClear(api)
                count=0
           
    #Start to Execute Command Queued
    print("END")
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
		
    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

cv2.waitKey(0)
#Disconnect Dobot
dType.DisconnectDobot(api)
cv2.destroyAllWindows()
