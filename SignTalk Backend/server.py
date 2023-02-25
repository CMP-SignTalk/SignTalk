import os
import sys
from flask import Flask, request, jsonify, send_file

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules from the Modules directory
from Modules.TexttoSpeech.text_to_speech import text_to_speech

app = Flask(__name__)

def corsify(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/audio', methods=['POST'])
def speech():
    # The Forward path (Speech Recognition then ASL Translation)
    audio_file = request.files['audio']
    # english = speech_recognition(audio_file)
    # als_gloss = asl_translation(english)
    response = jsonify({'asl_gloss': 'THIS X-ASL GLOSS'})
    return corsify(response)
    
@app.route('/video', methods=['POST'])
def video():
    # The Backward path (CV then ASL translation then Text to Speech)
    video_file = request.files['video']
    # asl_gloss = asl_recognition(video_file)
    # english_text = asl_translation(asl_gloss)
    english_text = 'This is the English translation of the video'
    audio = text_to_speech(english_text)
    response = send_file(audio, mimetype='audio/mpeg', as_attachment=False)
    return corsify(response)

if __name__ == '__main__':
    app.run()
