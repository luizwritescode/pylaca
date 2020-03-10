import sys, time, os
import cv2
import numpy as np

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#THRESHOLDS
tMOVE = 100


try:
    cap = cv2.VideoCapture(0)
except:
    print("failed to open camera")
    sys.exit()

if __name__ == "__main__":
        

    
    while 1:
        ret, frame = cap.read()
        ch = cv2.waitKey(1)
        if ch == 27:
            break
        if ret is True:
            col=frame

            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            frame = cv2.flip(frame, 1)
            pupilFrame=frame
            clahe=frame
            blur=frame
            edges=frame
            cropped = np.zeros((256, 256), dtype = "uint8")
            eyes = cv2.CascadeClassifier("C:/Users/Felipe Costa/pylaca/eyetracking/haarcascade_eye.xml")
            detected = eyes.detectMultiScale(frame, 1.3, 5)
            xs = [x for (x,y,w,h) in detected]
            for (x,y,w,h) in detected: #similar to face detection

                
                cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (255,0,0),1)	 #draw rectangle around eyes
                cv2.line(frame, (x,y), ((x+w,y+h)), (255,0,0),1)   #draw cross
                cv2.line(frame, (x+w,y), ((x,y+h)), (255,0,0),1)
                pupilFrame = cv2.equalizeHist(frame) 
                cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                clahe = cl1.apply(pupilFrame)
                blur = cv2.medianBlur(clahe, 3)
                if x == min(xs): #left most eye
                    cropped[0:h, 0:w] = blur[y:y+h, x:x+w]
                #elif x == max(xs): #right most eye
                #    cropped[50:h, 50:w] = blur[50+y:y+h, 50+x:x+w]

                circles = cv2.HoughCircles(cropped, cv2.HOUGH_GRADIENT,1.2,15,param1=50,param2=30,minRadius=3,maxRadius=16)

                #MOVEMENT THRESHOLDING
                center = [x/2, y/2]
                pt1 = (center[0] - tMOVE, center[1]-2)
                pt2 = (center[0] + tMOVE, center[1]+2)
                cv2.rectangle(cropped, center, ((x/2)+100,(y/2)+100), 255,20)

                if circles is not None:
                    circles = np.round(circles[0, :]).astype("int")
                    closest = 999999
                    
                    for c in circles:
                        dist = abs(c[0] - center[0]) + abs(c[1] - center[1])
                        if dist < closest:
                            closest = dist
                            centerMost = c

                    x, y ,r = centerMost

                    cv2.circle(cropped, (x, y), r, (255), 1)
                    cv2.rectangle(cropped, (x - 2, y - 2), (x + 2, y + 2), (0,128,255), 1)
                    #print("X: ", centerMost[0], "\tY: ", centerMost[0])

                    thresh = [center[0] - tMOVE, center[0] + tMOVE]

                    pt1 = (center[0] - tMOVE, center[1])
                    pt2 = (center[0] + tMOVE, center[1])
                    cv2.rectangle(cropped, pt1[0], pt2[0], 255,2)

                    if centerMost[0] < thresh[0]:
                        print("LEFT")
                    elif centerMost[0] > thresh[1]:
                        print("RIGHT")
                    else:
                        print("CENTER")
                    

        #cv2.imshow("video", pupilFrame)
        cv2.imshow("video", pupilFrame)
        cv2.imshow("eye", cropped) 
