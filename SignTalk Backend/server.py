import os
import sys
from flask import Flask, request, jsonify, send_file
import numpy as np 

from Modules.CSLR.Detecting_sign import main_func
from flask_cors import CORS
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules from the Modules directory
# 1. Automatic Speech Recognition (ASR) module
from Modules.ASR.utils import load_files,load_files_mod
from Modules.ASR.main import transcribe,transcribe_mod
# 2. Statistical Machine Translation (SMT) module

from Modules.SMT.smt import SMT
# 3. Continuous Sign Language Recognition (CSLR) module
from Modules.CSLR.Detecting_sign import main_func
# 4. Text to Speech (TTS) module

from Modules.TTS.tts import text_to_speech

# Initialize the modules
# 1. Load the ASR files
model, decoder = load_files_mod()
# 2. Instantiate the SMT module
smt = SMT()

app = Flask(__name__)
CORS(app)


def corsify(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/audio', methods=['POST'])
def speech():
    # The Forward path (Automatic Speech Recognition then Statistical Machine Translation)
    received_file = request.files['audio']
    received_file.save('audio.webm')
    audio_file = 'audio.wav'
    os.system("ffmpeg -i {0} -vn {1}".format('audio.webm', audio_file))
    # # Get the english transcript from the audio file
    # en = transcribe(audio_file, model, decoder)
    transcript = transcribe_mod(audio_file, model, decoder)
    # Remove the audio file after we're done with it
    os.remove(audio_file)
    # Translate the english to ASL Gloss
    aslg = smt.forward_translate(transcript)
    # Store the gloss in the file gloss.txt
    with open('gloss.txt', 'w') as f:
        f.write(aslg)
    # Return the ASL Gloss and the english transcript
    response = jsonify({'transcript': transcript, 'aslg': aslg})
    return corsify(response)
    
    

@app.route('/gloss', methods=['GET'])
def gloss():
    with open('gloss.txt', 'r+') as f:
        # Read the gloss from the file and remove any trailing whitespace
        gloss = f.read().strip()
        # Split the gloss into a list of words
        gloss = gloss.split()
        if len(gloss) == 0:
            # Return an empty array if the gloss is empty
            return jsonify({'gloss': []})  
        else:
            # Move the file pointer to the beginning of the file
            f.seek(0)
            # Truncate the file, removing its contents
            f.truncate()
            # Return the gloss as a JSON object
            return jsonify({'gloss': gloss})
        
        

@app.route('/video', methods=['POST'])
def video():
    # The Backward path (Continuous Sign Language Recognition then Statistical Machine Translation then Text to Speech)
    # the video that I will process , see ffmpeg  , webm- . 
    video_file = request.files['video']
    
    print(type(video_file))
    os.chdir("Modules/CSLR/")
    video_file.save("output0.mp4")
    print("I AM HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    signs = main_func()
    print(signs)
    os.chdir("../../")
    alsg=""
    i = 0 
    j = 1 
    # signs = np.unique(np.array(signs))
    # for sign in signs:
    #     print(sign)
    #     alsg+=sign
    #     alsg+=' '
    uniq= []
    for sign in signs : 
       
        
        if sign not in uniq : 
            uniq.append(sign)
    
    for sign in uniq:
        if sign =='yours': sign = 'your'       
        alsg+=sign 
        alsg+=' '
    # Translate the ASL Gloss to english
    print(alsg)

    
    # en = smt.backward_translate(alsg)
    # Convert the english to audio
    audio = text_to_speech(alsg)
    # Return the audio file - TODO: return the english transcript as well
    response = send_file(audio, mimetype='audio/mpeg', as_attachment=False)
    return corsify(response)



@app.route('/signs')
def signs():
    global my_sign
    global copy_sign
    copy_sign = my_sign[:] 
    my_sign = []
    if len(copy_sign) != 0:
        return jsonify(copy_sign)
    else :
        return ''



if __name__ == '__main__':
    app.run()