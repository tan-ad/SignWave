# SpeechToSign

## Inspiration

Given how much society has advanced technologically, the face that there still isn't enough attention given towards making communication more accesible towards the deaf community is inexcusable. One of our teammate spoke of his first-hand experience with this issue, as his grandfather is a deaf individual who communicates primarily through sign language and visual cues.  That's when we had the idea of automating translation to sign language, similar to closed captions on videos. As a result, we have created SpeechToSign. 


## What it does and how it can be used

SpeechToSign can take two types of input: audio files and text. When an audio file is given, SpeechToText produces a transcript of any words spoken in the audio file and presents an animation of the transcript in sign language. When text is given, SpeechToText simply takes the text and produces an animation of the text in sign language. While useful as a sign language equivalent of closed caption, SpeechToSign also extends as an educational tool. Those looking to learn sign language can use SpeechToSign to teach themselves how to sign various phrases using the both the speech-to-sign and text-to-sign functionalities. 


## Install

## How we built it

Our program has three main steps: 
* Convert audio to text
* find what movement corresponds to each word
* animate the movement
Note: when converting text-to-sign, the first step is skipped.

We used OpenAI's Whisper API to recognize and convert speech to text. Once in text form, we used [ASL Sign Language Dictionary](https://www.handspeak.com/word/) to collect video demonstrations of various words in sign language. For each video, we tracked the hand joints using [MediaPipe Hand Landmarker](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker), which gave us the 3D coordinate of each hand joint at each frame of the video. We then created a dictionary, mapping each word to a multidimensional array of coordinates. This then allows us to use three.js to animate the hands as a set of points and edges. Finally, we wrapped it all together into pleasant and usable interface using HTML and CSS. 

## Challenges we ran into

using git
semantics (not having the exact word in the dictionary)
left vs right hand
getting rid of text output
user interface


## Accomplishments that we're proud of

## What we learned

## What's next for SpeechToSign