import pyttsx3
import queue
import sounddevice as sd
import vosk
import json
import threading
from gpt4all import GPT4All

# Load GPT4All (offline LLM)
model = GPT4All(model_name="ggml-gpt4all-j-v1.3-groovy.bin")  # Make sure you downloaded it

# Load VOSK model
vosk_model = vosk.Model("vosk-model-small-en-us-0.15")
q = queue.Queue()

# TTS setup
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Audio input callback
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Ask local model
def get_response(text):
    if "exit" in text or "stop" in text:
        return "Goodbye!", True
    print("💡 Asking local model...")
    reply = model.chat_completion([{"role": "user", "content": text}])
    return reply, False

# Voice input thread
def voice_listener():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(vosk_model, 16000)
        print("🎙️ Listening... Say 'exit' to quit.")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if not text:
                    continue
                print("🗣️ You said:", text)
                response, exit_now = get_response(text)
                print("🤖 Assistant:", response)
                speak(response)
                if exit_now:
                    break

# Console input thread
def console_input():
    while True:
        typed = input("⌨️ Type here (or 'exit' to quit): ")
        if typed:
            response, exit_now = get_response(typed)
            print("🤖 Assistant:", response)
            speak(response)
            if exit_now:
                break

# Start
speak("Hello, I am your free offline assistant.")
voice_thread = threading.Thread(target=voice_listener)
text_thread = threading.Thread(target=console_input)

voice_thread.start()
text_thread.start()

voice_thread.join()
text_thread.join()

print("👋 Assistant session ended.")
