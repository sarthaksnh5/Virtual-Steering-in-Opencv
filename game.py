import cv2
import numpy as np
import imutils
import keyboard


cap = cv2.VideoCapture(0)


lower_range = np.array([90, 60, 60])
upper_range = np.array([130, 255, 255])

def putRect(frame, sx, sy, ex, ey, stat):
    cv2.rectangle(frame, (sx, sy), (ex, ey), (0, 0, 0), 3)
    midx = int((sx + ex) / 2)
    midy = int((sy + ey) / 2)
    cv2.putText(frame, str(stat), (midx, midy), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0))


speed = [0, 0]
turn = [0, 0]

execute = False

while 1:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)    


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_range, upper_range)

    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    i = 0
    if(len(cnts) > 0):
        execute = True
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 2000:
                cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)
                m = cv2.moments(c)
                cx = int(m["m10"]/m["m00"])
                cy = int(m["m01"]/m["m00"])            
                #print(cx, cy)
                if i == 0:
                    speed[0] = cx
                    speed[1] = cy
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255))
                if i == 1:
                    turn[0] = cx
                    turn[1] = cy
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0))
                    
                i += 1         
    else:
        execute = False

    # print("Steer: ", speed)
    # print("Turn: ", turn)

    if execute: 
        if speed[0] > 200 and speed[0] < 400:
            if speed[1] > 225 and speed[1] < 325:
                print("Forward")
                keyboard.press_and_release('w')
            elif speed[1] > 375 and speed[1] < 475:
                print("Backward")
                keyboard.press_and_release('s')
            else:
                keyboard.press_and_release('space')
                print("Stop")

        if turn[1] > 20 and turn[1] < 340:
            if turn[0] > 10 and turn[0] < 180:
                keyboard.press_and_release('a')
                print("Left")
            elif turn[0] > 420 and turn[0] < 590:
                keyboard.press_and_release('d')
                print("Right")
            else:
                
                print("Straight")
        

    putRect(frame, 10, 20, 180, 340, 'L')
    putRect(frame, 420, 20, 590, 340, 'R')
    putRect(frame, 200, 225, 400, 325, 'F')
    putRect(frame, 200, 375, 400, 475, 'B')

    cv2.imshow('Frame', frame)
    #cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
