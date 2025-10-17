from tkinter import *
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time

# GUI setup
root = Tk()
root.title("Simulated LED")
canvas = Canvas(root, width=100, height=100)
canvas.pack()
led = canvas.create_oval(10,10,90,90, fill="gray")

# Vosk setup
model = Model("./vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 44100)  
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=8000)
stream.start_stream()

def set_led(color):
    canvas.itemconfig(led, fill=color)
    root.update()
    time.sleep(0.1)

print("🎤 Speak 'on', 'off', 'dim', 'red', 'blue', or 'exit'...")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get("text", "")
        if text:
            print("You said:", text)
            text_lower = text.lower()
            if "on" in text_lower:
                set_led("green")
            elif "off" in text_lower or "of" in text_lower:
                set_led("gray")
            elif "yellow" in text_lower:
                set_led("yellow")
            elif "red" in text_lower or "read" in text_lower:
                set_led("red")
            elif "blue" in text_lower:
                set_led("blue")
            elif "exit" in text_lower or "quit" in text_lower:
                break

stream.stop_stream()
stream.close()
p.terminate()
root.destroy()
