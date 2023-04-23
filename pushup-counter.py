import cv2
import numpy as np
import time
import poseModule as pm

cap = cv2.VideoCapture("project/4.fitnessTracker/videos/pushup.mp4")

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
    success, img = cap.read()
    #resuze and fit the video to frame
    img = cv2.resize(img, (1280, 720))

    # img = cv2.imread("videos/images/push-angle.jpeg")
    img = detector.findPose(img, False)

    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:

        ## --- Get tracking for right and left arm --
        #Right Arm
        angle1=detector.findAngle(img, 12, 14, 16)

        #Left Arm
        angle = detector.findAngle(img, 11, 13, 15)

        # set up range for pushup
        low = 190
        high = 290
        per = np.interp(angle1, (low, high), (0, 100))

        # print( angle ,"->" , per)
        # calculate the number of pushups
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0

        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1


        # dislpay count
        cv2.rectangle(img, (0, 0), (100, 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (35, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
        # print(count)

        #Display FPS
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        # get a loading bar
        bar = np.interp(angle1, (low, high), (650, 100))
        #Draw bar
        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650),
                        (0, 255, 0), cv2.FILLED)
        #show percentage
        cv2.putText(img, str(int(per)), (1100, 75),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 3)

    cv2.imshow('video', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break