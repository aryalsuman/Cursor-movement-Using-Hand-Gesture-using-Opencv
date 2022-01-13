import cv2
import mediapipe as mp  # mediapipe
import time,pyautogui
pyautogui.FAILSAFE = False
cap=cv2.VideoCapture(0)
mphands=mp.solutions.hands
hands=mphands.Hands()
drawing=mp.solutions.drawing_utils
current_time=0
previous_time=0
x_sensitivty=1.5
y_sensitivty=1.5
old_x=0
old_y=0
error=20
width,height=pyautogui.size()
while True:
    previous_time=current_time#for calculating fps
    _,frame=cap.read()
    frame=cv2.flip(frame,1)
    framergb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)  #convert to rgb for mediapipe
    result=hands.process(framergb)#process the frame
    if result.multi_hand_landmarks:#if there are hands
        for handlms in result.multi_hand_landmarks:#for each hand
            for id,lm in enumerate(handlms.landmark):#for each point in the hand of each hand
                # h,w,c= frame.shape
                if id==8:
                    # cx,cy=int(lm.x),int(lm.y)#
                    print(id,lm.x,lm.y)
                if id==8:
                    new_x=int(lm.x*width*x_sensitivty)
                    new_y=int(lm.y*height*y_sensitivty)
                    if abs(new_x-old_x)>=error or abs(new_y-old_y)>=error:
                        pyautogui.moveTo(new_x,new_y)
                        old_x=new_x
                        old_y=new_y
                    # print(int(lm.x*1920*x_sensitivty),int(lm.y*1080*y_sensitivty))
                    # pyautogui.moveTo(int(lm.x*1920*x_sensitivty),int(1080*lm.y*y_sensitivty))
            drawing.draw_landmarks(frame,handlms,mphands.HAND_CONNECTIONS)
    current_time=time.time()#for calculating fps
    fps=1/(current_time-previous_time)#for calculating fps
    cv2.putText(frame,str(int(fps)),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#put fps on frame
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()