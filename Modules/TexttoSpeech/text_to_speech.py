from gtts import gTTS
from io import BytesIO

def text_to_speech(english_text='This is the English translation of the video'):
    tts = gTTS(text=english_text, lang='en')
    audio = BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)
    return audio