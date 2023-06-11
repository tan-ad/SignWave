from flask import Flask,render_template, request, jsonify
import numpy as np
from subprocess import CalledProcessError, run
import whisper

#libraries for text modification
from Levenshtein import ratio
import re
import json

app = Flask(__name__, template_folder='templates')

model = whisper.load_model('base')

SAMPLE_RATE = 16000
def custom_load_audio(byte_data: bytes, sr=SAMPLE_RATE): #converts byte data to what whisper can use (adapted from https://github.com/openai/whisper/blob/main/whisper/audio.py)
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-threads", "0",
        "-i", "-",
        "-f", "s16le",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        "-ar", str(sr),
        "-"
    ]
    try:
        out = run(cmd, input=byte_data, capture_output=True, check=True).stdout
    except CalledProcessError as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

def process_audio(audio):
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    return result.text

with open('static/json/reference.json', 'r') as json_file:
    reference_data = json.load(json_file)

def modify_words(text): #modifies words so all of them are in the dictionary 
    words = re.findall(r'\b\w+\b', text.lower().strip()) 
    filtered_words = [word for word in words if len(word) > 2]
    modified_words = []
    for word in filtered_words:
        modified_word = None
        for reference_word in reference_data:
            # Calculate the similarity ratio using Levenshtein distance
            similarity = ratio(word, reference_word)
            if similarity >= 0.8:  # Adjust the threshold as needed
                modified_word = reference_word
                break
        if not modified_word is None:
            modified_words.append(modified_word) #we're just removing words that dont match to make it easier (needs to be fixed)
    return ' '.join(modified_words)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/", methods=['POST']) #check for empty files or no file updated
def upload_file():
    f = request.files['file']
    rawText = process_audio(custom_load_audio(f.read()))
    modText = modify_words(rawText)
    return jsonify({'rawText':rawText,'modText': modText})


if __name__ == '__main__':
    app.run(port=5001)