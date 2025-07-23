from gtts import gTTS
from playsound import playsound
import os

text = "hello there , how are you doing"

tts = gTTS(text=text, lang="en")
filename = "speech.mp3"
tts.save(filename)
playsound(filename)
os.remove(filename)
