from flask import Flask, request, jsonify

app = Flask(__name__)

def corsify(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/audio', methods=['POST'])
def speech():
    # Add our work here - The Forward path (Speech Recognition then ASL Translation)
    # english = speech_recognition()
    # als_gloss = asl_translation(english)
    print(request)
    response = jsonify({'als_gloss': 'ASL gloss'})
    return corsify(response)
    
@app.route('/video', methods=['POST'])
def video():
    # Add our work here - The Backward path
    # asl_gloss = asl_recognition()
    # english = asl_translation(asl_gloss)
    print(request)
    response = jsonify({'english': 'English'})
    return corsify(response)

if __name__ == '__main__':
    app.run()
