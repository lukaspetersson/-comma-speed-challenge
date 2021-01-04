import numpy as np
import cv2
from PIL import Image, ImageEnhance

cap = cv2.VideoCapture('C:/Users/Lukas/Desktop/commaai-speed-challenge/data/test.mp4')

ret, frame1 = cap.read()
brightness = np.random.uniform(0.5, 1.5)
frame1 = ImageEnhance.Brightness(frame1).enhance(brightness)
frame1 = frame2.crop((0, 160, 640, 370)).resize((150,150))
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

count = 0

while(1):
    ret, frame2 = cap.read()
    
    brightness = np.random.uniform(0.5, 1.5)
    frame2 = ImageEnhance.Brightness(frame2).enhance(brightness)
    frame2 = frame2.crop((0, 160, 640, 370)).resize((150,150))

    
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 1, 15, 2, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('frame2',rgb)
    k = cv2.waitKey(30) & 0xff
    prvs = next
    #cv2.imwrite("C:/Users/Lukas/Desktop/commaai-speed-challenge/data/frames/test-optical-flow/%d.jpg" % count, rgb)
    count += 1

cap.release()
cv2.destroyAllWindows()

