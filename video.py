import sys, time, os
import cv2
import numpy as np
import pathlib

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#THRESHOLDS
tMOVE = 100


class Tracking():
    def __init__(self):



        try:
            self.cap = cv2.VideoCapture(0)
        except:
            print("failed to open camera")
            sys.exit()

        self.WIDTH = self.cap.get(3)
        self.HEIGHT = self.cap.get(4)

        path = pathlib.Path(__file__).parent.absolute()
        eyes_path = str(path) + "\\et\\haarcascade_eye.xml"
        nose_path = str(path) +  "\\et\\haarcascade_msc_nose.xml"
        face_path = str(path) +  "\\et\\haarcascade_frontalface_default.xml"
        self.eyes = cv2.CascadeClassifier(eyes_path)
        self.face = cv2.CascadeClassifier(face_path)

        self.center = (0,0)
        self.move = 0
        self.screen = None

    def get_center(self):
        return self.center

    def get_movement(self):
        return self.move

    def get_screen(self):
        return self.screen

    def run(self):
        ret, frame = self.cap.read()
        if ret is True:
            col=frame

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            pupilFrame=gray
            clahe=gray
            blur=gray
            edges=gray
            cropped = np.zeros((256, 256), dtype = "uint8")

            self.screen = gray 
            #detected = self.eyes.detectMultiScale(frame, 1.3, 5)
            detected_face = self.face.detectMultiScale(frame, 1.3, 5)


            #DRAW THRESHOLD
            center_x = int(self.WIDTH//2)
            center_y = int(self.HEIGHT//2)

            T = int(self.WIDTH//12)
            cv2.rectangle(frame, (center_x - T, center_y + 50),(center_x + T,center_y - 50),(255,0,0),2)
            
            self.move = False 
            xs = [x for (x,y,w,h) in detected_face]
            for (x,y,w,h) in detected_face: #similar to face detection
                
                face_center_x = x + (w//2)
                face_center_y = y + (h//2)
                center = (x + (w//2), y + (h//2))
                cv2.circle(frame, center, 5, (255,0,255), 10)
                cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (255,0,0),1)	 #draw rectangle around face
                cv2.line(frame, (x,y), ((x+w,y+h)), (255,0,0),1)   #draw cross
                cv2.line(frame, (x+w,y), ((x,y+h)), (255,0,0),1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
                

                if (face_center_x < center_x - T):
                    self.move = -T
                elif (face_center_x > center_x + T):
                   self.move = T
                else:
                    d = face_center_x - center_x
                    self.move = d
                
                # EYE TRACKING STUFF
                #
                #pupilFrame = cv2.equalizeHist(pupilFrame) 
                #cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                #clahe = cl1.apply(pupilFrame)
                #blur = cv2.medianBlur(clahe, 3)
                # if x == min(xs): #left most eye
                #     cropped[0:h, 0:w] = blur[y:y+h, x:x+w]
                #elif x == max(xs): #right most eye
                #    cropped[50:h, 50:w] = blur[50+y:y+h, 50+x:x+w]

                #circles = cv2.HoughCircles(cropped, cv2.HOUGH_GRADIENT,1.3,15,param1=60,param2=30,minRadius=3,maxRadius=16)

                # if circles is not None:
                #     circles = np.round(circles[0, :]).astype("int")
                #     closest = 999999
                    
                #     for c in circles:
                #         dist = abs(c[0] - center[0]) + abs(c[1] - center[1])
                #         if dist < closest:
                #             closest = dist
                #             centerMost = c

                #     x, y ,r = centerMost

                    # tDETECTION = [ center[0] // 2 - tMOVE, center[0] // 2 + tMOVE]
                    # cv2.circle(cropped, (x, y), r, (255), 1)
                    
                    # #print("X: ", centerMost[0], "\tY: ", centerMost[0])
                    # cv2.rectangle(cropped, (x -10, y + 5) , (x + 10, y - 2), (255,255,255,0.5),1)

                    # dirColor = white
                    # if centerMost[0] < tDETECTION[0]:
                    #     print("LEFT")
                    #     dirColor = (255,0,0)
                    # elif centerMost[0] > tDETECTION[1]:
                    #     print("RIGHT")
                    #     dirColor = (0,123,0)
                    # else:
                    #     print("CENTER")
                    #     dirColor = (0,0,255)
                    
                    # cv2.rectangle(cropped, (center[0] - 10, center[1] - 10), (center[0] + 2, center[1] + 2), dirColor, 1)

                #MOVEMENT THRESHOLDING


        #cv2.imshow("video", pupilFrame)
        #cv2.imshow("eye", cropped) 
        #cv2.imshow("video", blur)
