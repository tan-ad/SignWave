# SignWave 👋

An easy-to-use program that transcribes text or audio files into a sign language animation.

## Inspiration 

Given how much society has advanced technologically, the fact that there still isn't enough attention given to making communication more accessible for the deaf community is inexcusable. One of our teammates spoke of his first-hand experience with this issue, as his grandfather is a deaf individual who communicates primarily through sign language and visual cues.  That's when we had the idea of automating translation to sign language, similar to closed captions on videos. As a result, we have created SignWave, an accessible and convenient translator from English to American Sign Language (ASL). 


## What it does and how it can be used 🤔

SignWave can take two types of input: audio files and text. If an audio file is given, SignWave produces a transcript of the words spoken in the audio file. If a text input is given and presents an animation of the transcript in sign language and continues to the next step. When a text input is given, the process is bypassed and the program produces an animation of the text in sign language. While useful as a sign language equivalent of closed captions, SignWave also extends as an educational tool. Those looking to learn sign language can use SpeechToSign to teach themselves how to sign various phrases using both the speech-to-sign and text-to-sign functionalities. 


## Install
* Clone the repository
* Run the main ```index.html``` file

## How we built it

Our program has three main steps: 
* Convert audio to text
* Find what movement corresponds to each word
* Animate the movement
Note: when converting text-to-sign, the first step is skipped.

We used OpenAI's [Whisper API](https://openai.com/research/whisper) to recognize and convert speech to text. Once in text form, we used [ASL Sign Language Dictionary](https://www.handspeak.com/word/) to collect video demonstrations of various words in sign language. For each video, we tracked the hand joints using [MediaPipe Hand Landmarker](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker), which gave us the 3D coordinate of each hand joint at each frame of the video. We then created a dictionary, mapping each word to a multidimensional array of coordinates. This then allows us to use three.js to animate the hands as a set of points and edges. Finally, we wrapped it all together into a pleasant and usable interface using HTML, JS, and CSS. 

## Challenges we ran into

* The team was almost completely new to Git, so we had to learn to use Git commands, such as add, commit, push, and pull from scratch
* Semantics: Not having the exact translation of every word in the ASL dictionary
* Creating a model that uses both right and left hand, especially when their animations overlap
* Making User Interface design smooth, accommodating both text and audio file inputs

## Accomplishments that we're proud of

* Creating a 3D model that accurately maps the movements of both hands
* Transcribing a .mp3 file into .txt, then mapping it to our dictionary of ASL videos
* Accommodating both audio and text input
* Creating a clean and easy-to-use UI

## What we learned

* How to use OpenAI's [Whisper API]() to convert speech to text
* Using Python scripts to convert the .txt file into a list of unique strings
* Using Google's [MediaPipe Hand Landmarker](https://www.handspeak.com/word/) to retried the coordinates of each hand
* Using the ASL Dictionary to map each word to an array of coordinates
* Using [three.js](https://threejs.org/) to animate the set of points
* Using HTML, CSS, JS, and Git to create a website and repository

## What's next for SignWave
* Adding sliders to allow users to control animation speed
* Creating a model with more humanoid hands
* Implementing a reverse translation function of ASL to English by using computer recognition and Machine Learning
* Expanding it into commercial uses (eg. sign language interpreters in classrooms, TV shows, etc)
* We're excited to see where SignWave can go in the future 👋
