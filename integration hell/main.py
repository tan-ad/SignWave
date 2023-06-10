import json
import re
from Levenshtein import ratio
import nltk
from nltk.corpus import words
from flask import Flask, render_template, request
import os
import whisper

# Download the English word corpus from NLTK
nltk.download('words')

# Load the English word corpus from NLTK
english_words = set(words.words())

# Open the reference JSON file
with open('reference.json', 'r') as json_file:
    # Load the JSON data
    reference_data = json.load(json_file)

app = Flask(__name__)

# Define the route for file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded.'

        file = request.files['file']
        if file.filename == '':
            return 'No file selected.'
        
        # Save the file to the server
        file.save('uploads')

        # Load the audio file and transcribe it
        model = whisper.load_model('base')
        audio = whisper.load_audio('transcribes/raw_transcribe.txt')
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)

        # Write the transcribed text to the raw transcript file
        with open('transcribes/raw_transcribe.txt', 'w') as file:
            file.write(result.text)

        # Read the content of the raw transcript file
        with open('transcribes/raw_transcribe.txt', 'r') as file:
            content = file.read()

        # Remove punctuation and convert to lowercase
        words = re.findall(r'\b\w+\b', content.lower())

        # Filter out one or two-letter words that are not English words
        filtered_words = [word for word in words if len(word) > 2 and word in english_words]

        # Create a modified word list with variations
        modified_words = []

        for word in filtered_words:
            modified_word = None
            for reference_word in reference_data:
                # Calculate the similarity ratio using Levenshtein distance
                similarity = ratio(word, reference_word)
                if similarity >= 0.8:  # Adjust the threshold as needed
                    modified_word = reference_word
                    break

            if modified_word is None:
                modified_word = word

            modified_words.append(modified_word)

        # Save the modified transcript to a new file
        modified_transcript_path = os.path.join('transcribes', 'modified_transcript.txt')
        with open(modified_transcript_path, 'w') as f:
            f.write(' '.join(modified_words))  # Join modified words into a single paragraph

        # Pass the clean transcript to the template
        clean_transcript = ' '.join(modified_words)  # Join modified words into a single paragraph

        return render_template('upload.html', clean_transcript=clean_transcript)

    return render_template('upload.html')

if __name__ == '__main__':
    # Generate the modified transcript using the raw transcript file
    with open('transcribes/raw_transcribe.txt', 'r') as file:
        content = file.read()

    words = re.findall(r'\b\w+\b', content.lower())

    filtered_words = [word for word in words if len(word) > 2 and word in english_words]

    modified_words = []

    for word in filtered_words:
        modified_word = None
        for reference_word in reference_data:
            similarity = ratio(word, reference_word)
            if similarity >= 0.8:
                modified_word = reference_word
                break

        if modified_word is None:
            modified_word = word

        modified_words.append(modified_word)

    modified_transcript_path = os.path.join('transcribes', 'modified_transcript.txt')
    with open(modified_transcript_path, 'w') as f:
        f.write(' '.join(modified_words))  # Join modified words into a single paragraph

    print("Modified transcript generated and saved to modified_transcript.txt")

    app.run(debug=True)
