import tensorflow as tf 
from tensorflow import keras 
from keras import layers
from keras.models import Sequential 
from keras.layers import LSTM , Dense 
from keras.callbacks import TensorBoard
import os 
import cv2 
import time 
import mediapipe as mp 
import numpy as np 

mp_holistic = mp.solutions.holistic # Holistic model
mp_pose = mp.solutions.pose

def mediapipe_detection(image,model):
    image= cv2.cvtColor(image,cv2.COLOR_BGR2RGB) 
    image.flags.writeable=False
    results=model.process(image)
    image.flags.writeable=True
    image= cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    return image, results

def load_all_signs_model():
    signs = {"age":0,"I":1 , "love":2,"my":3,"name":4,"school":5,
         "sign":6 , "talk":7,"teacher":8,"what":9,"where":10,"yours":11}
    model=Sequential()
    model.add(LSTM(64,return_sequences=True ,activation='relu',input_shape=(40,126)))
    model.add(LSTM(64,return_sequences=False,activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(len(signs), activation='softmax'))
    model.load_weights("models/best_model_on_12_sign_(ISA).h5")
    return model

temp_nose_x = None ; 
temp_nose_y = None ; 



def create_model_check(name="age"):
    signs={f"{name}":1,f"not_{name}":0}
    model=Sequential()
    model.add(LSTM(64,return_sequences=False ,activation='relu',input_shape=(40,126)))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(len(signs), activation='softmax'))
    model.load_weights(f"models/{name}_model.h5")
    return model 

def load_signs_models():
    signs = ["age","I" , "love","my","name","school","sign" , "talk","teacher","what","where","yours"]
    models = []
    for sign in signs:
        models.append(create_model_check(sign)) 

    return models 


def extract_keypoints(results,temp_nose_x,temp_nose_y):
    try:
        X_Nose=results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
        temp_nose_x=X_Nose
    except : 
        X_Nose = temp_nose_x
    try : 
        Y_Nose=results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        temp_nose_y=Y_Nose
    except : 
        Y_Nose= temp_nose_y 
    
    # the follwoing condition is for the first time  ,when temp_nose_y and temp_nose_x was None in the first time . 
    # to be tested please please !! 
    if X_Nose == None  or  Y_Nose == None: 
         lh=np.zeros(21*3)
         rh=np.zeros(21*3)
         return np.concatenate([lh,rh])
    

    lh = np.array([[res.x - X_Nose, res.y - Y_Nose, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x - X_Nose, res.y - Y_Nose, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)

    return np.concatenate([lh,rh])


def get_keypoints(vid_name):
    num_frames=40
    path_to_current_sign=os.path.join(os.getcwd(),f"{vid_name}")
    print(path_to_current_sign)
    if os.path.exists(path_to_current_sign):
        cap = cv2.VideoCapture(path_to_current_sign); 
        
        length= int (cap.get(cv2.CAP_PROP_FRAME_COUNT))
        length = 0  
        while(True):
            ret , frame = cap.read()
            if ret :
                length+=1 
            else : 
                break 

        cap.release()
        cap = cv2.VideoCapture(path_to_current_sign);
        # print("Yes we get it ")
    else : length= 0 
    key_points_arr=[]

    done= np.zeros((length))
    done.fill(-1)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic :
        if os.path.exists(path_to_current_sign):
            index = 0
            start_frame =False
            if(length>num_frames):
                while (cap.isOpened()):
                    ret , frame = cap.read()
                    if ret == True: 
                        image, results = mediapipe_detection(frame, holistic)
                        keypoints = extract_keypoints(results,temp_nose_x,temp_nose_y)
    #                     if not(start_frame):
    #                         if (np.all(keypoints==0)):
    # #                             rest-=1 
    #                             continue
    #                         else :
    #                             start_frame=True
                        key_points_arr.append(keypoints)
                        # print(len(key_points_arr))
                    else : break 
    key_points_arr=np.array(key_points_arr)

    return key_points_arr , done , length 



def create_model_check(name="age"):
    signs={f"{name}":1,f"not_{name}":0}
    model=Sequential()
    model.add(LSTM(64,return_sequences=False ,activation='relu',input_shape=(40,126)))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(len(signs), activation='softmax'))
    model.load_weights(f"models/{name}_model.h5")
    return model 


def check_sign(key_points,model):
    model_results=model.predict(key_points)
    if(np.any(model_results>0.7)): 
            if(np.argmax(model_results)==1):
                return True 

    return False   


def detect_sign(vid_name):
    detection_list=[]
    key_points_arr, done ,length= get_keypoints(vid_name) 
    index =0 
    slide = 1
    num_of_times_1=0 

    signs_models = load_signs_models()
    


    index = 0 
    model=load_all_signs_model()
    while (length-index>=40 ): 
        # you should think a lot a bout adding it 
        # if(np.sum(done[index:index+40])!=-40):
        #     while(done[index]==-1):
        #         index+=1
        #     index+=40 
        #     continue 
        signs = {"age":0,"I":1 , "love":2,"my":3,"name":4,"school":5,
                "sign":6 , "talk":7,"teacher":8,"what":9,"where":10,"yours":11,
                }
        model_results=model.predict(key_points_arr[index:index+40][None , :])
        # print( i , model_results)
        if (np.any(model_results>0.5)):
            arg_max = np.argmax(model_results)
            if(arg_max==9 or arg_max == 11 ):
                index+=slide 
                continue 
            print(arg_max)
            is_sign = check_sign(key_points_arr[index:index+40][None , :],signs_models[arg_max])
            if is_sign: 
                done[index]=arg_max
                index+=40
                print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEES",arg_max)
                continue 
           
        index+=slide 

    detected_sign=[]
    print(done)
    detected_sign_indecies=done[done!=-1]
    print(detected_sign_indecies)
    reversed_signs={j:i for i , j in zip(signs.keys(),signs.values())}
    for sign  in detected_sign_indecies : 
        detected_sign.append(reversed_signs[sign])


    print(detection_list)
    return detected_sign



def main_func():
    signs =detect_sign("output0.mp4")
    return signs


    
    
            

                    
    
                
                            

        
