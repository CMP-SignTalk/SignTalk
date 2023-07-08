import os
import sys
from flask import Flask, request, jsonify, send_file

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules from the Modules directory
# 1. Automatic Speech Recognition (ASR) module
from Modules.ASR.utils import load_files,load_files_mod
from Modules.ASR.main import transcribe,transcribe_mod
# 2. Statistical Machine Translation (SMT) module
from Modules.SMT.smt import SMT
# 3. Computer Vision (CV) module
# Abdallah Work Here
# 4. Text to Speech (TTS) module
from Modules.TTS.tts import text_to_speech

# Initialize the modules
# 1. Load the ASR files
model, decoder = load_files_mod()
# 2. Instantiate the SMT module
smt = SMT()
# 3. Instantiate the CV module
# Abdallah Work Heremodel


app = Flask(__name__)

# this is the list of string that will be filled with the sign glosses [my_sign]
my_sign = ['love']
copy_sign= []


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
    # Return the ASL Gloss and the english transcript
    response = jsonify({'transcript': transcript, 'aslg': aslg})
    return corsify(response)
    
@app.route('/video', methods=['POST'])
def video():
    # The Backward path (Computer Vision then Statistical Machine Translation then Text to Speech)
    video_file = request.files['video']
    # Get the ASL Gloss from the video file - Abdallah Work Here
    # aslg = asl_recognition(video_file)
    aslg = 'girl be in france'
    # Translate the ASL Gloss to english
    en = smt.backward_translate(aslg)
    # Convert the english to audio
    audio = text_to_speech(en)
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
