from flask import Flask, request, jsonify

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
    # This will be returned to the frontend and will be displayed with the avatar
    response = jsonify({'als_gloss': 'THIS X-ASL GLOSS'})
    return corsify(response)
    
@app.route('/video', methods=['POST'])
def video():
    # The Backward path (CV then ASL translation then Text to Speech)
    video_file = request.files['video']
    # asl_gloss = asl_recognition(video_file)
    # english = asl_translation(asl_gloss)
    # audio = text_to_speech(english)
    # This will be returned to the frontend and will be played
    response = jsonify({'english': 'English Audio'})
    return corsify(response)

if __name__ == '__main__':
    app.run()
