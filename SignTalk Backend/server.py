import os
import sys
from flask import Flask, request, jsonify, send_file


# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules from the Modules directory
# from Modules.SR.text_to_speech import text_to_speech
# from Modules.SMT.smt import SMT
from Modules.ASR.utils import load_files,load_files_mod
from Modules.ASR.main import transcribe,transcribe_mod

# Instantiate the SMT module
# smt = SMT()

# Load the ASR files
# model, decoder = load_files()
model, decoder = load_files_mod()


app = Flask(__name__)

def corsify(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/audio', methods=['POST'])
def speech():
    # The Forward path (Speech Recognition then ASL Translation)
    received_file = request.files['audio']
    received_file.save('audio.webm')
    audio_file = 'audio.wav'
    os.system(
        "ffmpeg -i {0} -vn {1}".format('audio.webm', audio_file))
    # transcript = transcribe(audio_file, model, decoder)
    transcript = transcribe_mod(audio_file, model, decoder)
    # remove the audio file
    os.remove(audio_file)
    response = jsonify({'aslg': 'aslg', 'transcript': transcript})
    return corsify(response)
    
@app.route('/video', methods=['POST'])
def video():
    # The Backward path (CV then ASL translation then Text to Speech)
    video_file = request.files['video']
    # aslg = asl_recognition(video_file)
    aslg = 'girl be in france'
    # en = smt.backward_translate(aslg)
    # audio = text_to_speech(en)
    # response = send_file(audio, mimetype='audio/mpeg', as_attachment=False)
    # return corsify(response)

if __name__ == '__main__':
    app.run()
