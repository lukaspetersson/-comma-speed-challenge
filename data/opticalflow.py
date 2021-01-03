import numpy as np
import cv2

cap = cv2.VideoCapture('C:/Users/Lukas/Desktop/commaai-speed-challenge/data/train.mp4')

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

count = 0

while(1):
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('frame2',rgb)
    k = cv2.waitKey(30) & 0xff
    prvs = next
    cv2.imwrite("C:/Users/Lukas/Desktop/commaai-speed-challenge/data/frames/train-optical-flow/%d.jpg" % count, rgb)
    count += 1

cap.release()
cv2.destroyAllWindows()

#cred: https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html


