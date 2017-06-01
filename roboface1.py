import numpy as np
import cv2


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







SCALE_FACTOR_GLASS = 1.5
SCALE_FACTOR_JNT = 1.5
SCALE_FACTOR_HAT = 1.5
DISPLAY_BOUNDRY_BOX = True

sunglasses = cv2.imread('thug.jpg') 
jnt = cv2.imread('jnt.jpg')
hat = cv2.imread('hat.jpg')

# now we can try to detect faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mouth.xml')

cap = cv2.VideoCapture(0)
if (state == dType.DobotConnect.DobotConnect_NoError):
        #Clean Command Queued
        dType.SetQueuedCmdClear(api)

        #Async Motion Params Setting
        dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
        dType.SetPTPJumpParams(api,4,-55,isQueued=1)

        while(True):
                # Capture frame-by-frame
                ret, img = cap.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                

                img = cv2.medianBlur(img,3)

                
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                if len(faces) > 0:
                        filter_applied = False

                        #(x,y,w,h) = sorted(faces, key=lambda face: face[2]*face[3])[-1] #Might have more than one face -> choose the largest
                        for (x,y,w,h) in faces:
                                
                                if DISPLAY_BOUNDRY_BOX:
                                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                                    
                                roi_gray = gray[y:y+h, x:x+w]
                                eyes = eye_cascade.detectMultiScale(roi_gray) # Might have more than two 
                        ret,thresh1 = cv2.threshold(roi_gray,50,255,cv2.THRESH_BINARY)
                        resized=cv2.resize(thresh1,(400,300))
                        cv2.imshow('asd',resized)

                        count=0
                        cv2.imshow('frame',img)

                        for i in range(0,299):
                                j=0
                                #for j in range(0,335):
                                while(j<398):
                                    
                                    if(resized[i,j]==0 and resized[i,j+1]==0 and resized[i,j-1]==0 and (j+1)<398 and (j-1)>0):
                                        k=j;
                                        
                                        
                                        while(resized[i,k]==0):
                                            k=k+1
                                            if(k>399):
                                                break
                                        j=k-1
                                        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 300-((float(i*50)/float(300))), 80-((float(j*50)/float(400))), -59.3, 0, isQueued = 1)[0]
                                        
                                        count=count+1

                                    elif(resized[i,j]==0):
                                        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 300-((float(i*50)/float(300))), 80-((float(j*50)/float(400))), -59.3, 0, isQueued = 1)[0]
                                        count=count+1
                                        j=j+1
                                    else:
                                        j=j+1
                                    if(count==25):
                                        dType.SetQueuedCmdStartExec(api)

                                        #Wait for Executing Last Command 
                                        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                                            dType.dSleep(100)
                                        
                                        #Stop to Execute Command Queued
                                        dType.SetQueuedCmdStopExec(api)
                                        dType.SetQueuedCmdClear(api)
                                        count=0;
                           
                                        
                        cv2.imshow('frame',img)
                else:
                                cv2.imshow('frame',img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        dType.SetQueuedCmdStartExec(api)

        #Wait for Executing Last Command 
        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                dType.dSleep(100)

        #Stop to Execute Command Queued
        dType.SetQueuedCmdStopExec(api)
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
