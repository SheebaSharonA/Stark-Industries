import cv2
import numpy as np
facecascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyecascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
while True:
    ans,frame= cap.read()
    if ans== True:
        f= facecascade.detectMultiScale(frame,1.1,4)
        e= eyecascade.detectMultiScale(frame,1.1,4)
        for (x,y,w,h) in f:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        for (x,y,w,h) in e:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
             
        cv2.imshow('video',frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break        
cap.release()
cv2.destroyAllWindows()
