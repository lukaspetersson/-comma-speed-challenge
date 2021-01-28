import cv2
import time

#cap = cv2.VideoCapture('C:/Users/Lukas/Desktop/commaai-speed-challenge/data/2k19/Chunk_4/99c94dc769b5d96e_2018-06-15--19-55-32/6/video.hevc')

cap = cv2.VideoCapture('C:/Users/Lukas/Desktop/commaai-speed-challenge/data/test.mp4')


f = open("C:/Users/Lukas/Desktop/commaai-speed-challenge/data/test.txt", "r")

while(cap.isOpened()):

    ret, frame = cap.read() 
  
    font = cv2.FONT_HERSHEY_SIMPLEX 
  
    caption = "Speed: "+ f.readline()
    print(caption)
    cv2.putText(frame,  
                caption,  
                (50, 50),  
                font, 1,  
                (0, 255, 255),  
                2,  
                cv2.LINE_4) 
  
    cv2.imshow('video', frame) 
    time.sleep(1/50)
  
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release() 
cv2.destroyAllWindows() 