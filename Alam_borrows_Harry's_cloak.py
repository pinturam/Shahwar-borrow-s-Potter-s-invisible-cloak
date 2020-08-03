# # IMPORTING MODULES
import cv2
import time
import numpy as np
# # PREPARATION FOR WRITING THE VIDEO
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc , 20.0 , (640,480))
# # READING FROM WEBCAM
cap = cv2.VideoCapture(0)
# # ALLOW SYS TO SLEEP FOR 3 sec BEFORE WEBCAM STARTS
time.sleep(3)
count = 0
background = 0
# # CAPTURING THE BACKGROUND IN RANGE OF 60
for i in range(60):
    ret,background = cap.read()
background = np.flip(background , axis = 1)
# # READ EVERY FRAME FROM THE WEBCAM UNTIL IT IS OPEN
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count = count + 1
    img = np.flip(img , axis = 1)
    # # COLOR , BGR to HSV
    hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
# # GENERATE MASK TO DETECT RED COLOR
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask_1 = cv2.inRange(hsv , lower_red , upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask_2 = cv2.inRange(hsv , lower_red , upper_red)
# # MASKS IN ONE
    mask_1 = mask_1 + mask_2
# # OPEN and DILATE , (morphology)
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN , np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1 , cv2.MORPH_DILATE , np.ones((3,3), np.uint8))
# # FOR SEGMENTING RED COLOR OUT , inverted mask req
    mask_2 = cv2.bitwise_not(mask_1)
# # SEGMENTING RED CLR OUT , bitwise and inverted mask req
    res1 = cv2.bitwise_and(img , img , mask = mask_2)
# # SHOWING STATIC BACKGROUND ONLY FOR MASKED REGION
    res2 = cv2.bitwise_and(background , background , mask = mask_1)
# # WRITING FINAL OUTPUT
    finalOutput = cv2.addWeighted(res1, 1 , res2 , 1, 0)
    out.write(finalOutput)
# # THE FINAL SHOW
    cv2.imshow("magic" , finalOutput)
    cv2.waitKey(5)
# # RELEASE and DESTROY(windows)
cap.release()
out.release()
cv2.destroyAllWindows()