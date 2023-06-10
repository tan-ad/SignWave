# transcribing audio to text
import whisper

model = whisper.load_model('base')

audio = whisper.load_audio('wildfireNews.mp3')
audio = whisper.pad_or_trim(audio)

mel = whisper.log_mel_spectrogram(audio).to(model.device)

options = whisper.DecodingOptions(fp16=False)
result = whisper.decode(model, mel, options)

str = result.text.split(' ')

# finding unique strings in text
duplicates = []
for i in str:
    if i not in duplicates:
        duplicates.append(i)
print(duplicates)

#result = model.transcribe('wildfireNews.mp3', fp16=False)
#result['text']
#print (result.text)