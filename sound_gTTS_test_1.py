from gtts import gTTS #create sound from text 
from playsound import playsound # to play nthe sound
import os #to delete the spoken audio
from gtts.lang import tts_langs

text = "sawubona"

tts = gTTS(text=text, lang='en')
filename = "hello.mp3"
tts.save(filename)
playsound(filename)
os.remove(filename)
print(tts_langs())

