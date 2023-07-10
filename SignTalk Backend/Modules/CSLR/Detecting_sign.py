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
    """
    Loading the First Model for Sign Detection

    Args:

    None
    Returns:

    model (Sequential): The model used for sign detection.
    Description:
    This function loads the first-stage model that will be used for sign detection before the stages of checking. It does not take any arguments and returns the loaded model.
    """
    signs = {"hello":0,"I":1,"live":2,"love":3,"my":4,"name":5,
                "sign":6,"talk":7,"teacher":8,"what":9,"where":10,"yours":11}
    model=Sequential()
    model.add(LSTM(64,return_sequences=True ,activation='relu',input_shape=(40,126)))
    model.add(LSTM(64,return_sequences=False,activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(len(signs), activation='softmax'))
    model.load_weights("models/no_clownv0.4(ISA).h5")
    return model

temp_nose_x = None ; 
temp_nose_y = None ; 






def create_model_check(name="Hello"):
    """
    Creating the Checker Model for Sign Verification

    Args:

    name (str): The name of the required model.
    Returns:

    model (Sequential): The checker model for the sign.
    Description:
    This function loads the model for the corresponding sign, which will be used as a checker in the second stage after the sign detection stage. It takes the name of the required model as input and returns the loaded model.
    """
    signs={f"{name}":1,f"not_{name}":0}
    model=Sequential()
    model.add(LSTM(64,return_sequences=False ,activation='relu',input_shape=(40,126)))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(len(signs), activation='softmax'))
    model.load_weights(f"models/{name}_model.h5")
    return model 

def load_signs_models():
    """
    Loading All Sign Models into Memory

    Args:

    None
    Returns:

    models (list): A list of all models that will be used in the verification stage.
    Description:
    This function loads all the sign models into memory to reduce the number of I/O operations. It does not take any arguments and returns a list of all the loaded models that will be used in the verification stage.
    """
    signs = ["hello","I","live","love","my","name","sign","talk","teacher","what","where","yours"]
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





def check_sign(key_points,model,argmax):
    """
    Verification Stage Function

    Args:

    keyp_points (numpy.ndarray): Numpy array containing the keypoints of 40 frames used for verification.
    model: The model corresponding to the sign that will be used for verification.
    argmax: The sign number.
    Description:
    This function is used for the verification stage. It takes the keypoints of 40 frames, the corresponding sign model, and the sign number as input. It verifies if the detected sign is correct by using the provided model. If the verification is successful, it returns True; otherwise, it returns False.
    """
    model_results=model.predict(key_points) 
    print(argmax)
    if (argmax ==1 or argmax==0):
        if(np.any(model_results>0.9)): 
            
            if(np.argmax(model_results)==1):
                return True 
        else : return False 

    print(model_results)
    if(np.any(model_results>0.7)): 
            
            if(np.argmax(model_results)==1):
                return True 

    return False   


def detect_sign(vid_name):
    """
    Main Function for Sign Detection

    Args:

    vid_name (str): The name of the video on which you want to detect the sign.
    Returns:

    detected_signs (list): A list containing all the signs that have been detected within the video.
    Description:
    This function combines the first stage and the second stage of sign detection together into one function. It can be considered as the complete pipeline for sign detection. It takes the video name as input and returns a list of all the signs that have been detected within the video.
    """

    detection_list=[]
    key_points_arr, done ,length= get_keypoints(vid_name) 
    index =0 
    slide = 1
    num_of_times_1=0 

    signs_models = load_signs_models()
    


    index = 0 
    model=load_all_signs_model()
    while (length-index>=40 ): 

        signs = {"hello":0,"I":1,"live":2,"love":3,"my":4,"name":5,
                 "sign":6,"talk":7,"teacher":8,"what":9,"where":10,"yours":11}
        
        model_results=model.predict(key_points_arr[index:index+40][None , :])
        # print( i , model_results)
        print(np.argmax(model_results))
        print(model_results)
        if (np.any(model_results>0.90)):
            arg_max = np.argmax(model_results)
            # if(arg_max==0) :index+=1; continue  
            # print(arg_max)
            is_sign = check_sign(key_points_arr[index:index+40][None , :],signs_models[arg_max],arg_max)
            if is_sign: 
                done[index]=arg_max
                index+=40
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


    
    
            

                    
    
                
                            

        
