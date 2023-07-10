import numpy as np
import cv2
import time
import os 




sign ='test'
# creating the sign folder that will have the videos related to the sign 
# sign_folder=os.path.join(os.getcwd(),sign)
# try:
#     os.mkdir(sign_folder)
# except : 
#     pass 


for i in range (30):
    cap = cv2.VideoCapture(0)
    capture_duration =3
    # the requried duartion of the video 
    print("start record")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # print(os.path.join(f'output{i}.avi'))
    out = cv2.VideoWriter(f'output{i}.avi',fourcc, 30.0, (640,480))
    # creating the output video 
    start_time = time.time()
    while( int(time.time() - start_time) < capture_duration ):
        ret, frame = cap.read()

        # index 0 is the height which is 480 and index 1 is the width which is 640
        if ret==True:
            out.write(frame)
            cv2.imshow('frame',frame)
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

            

