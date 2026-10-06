import whisper
import speech_recognition as sr

print("Loading Whisper model...")

model = whisper.load_model("base")

recognizer = sr.Recognizer()

with sr.Microphone(device_index=1) as source:
    print("\nSpeak now...")
    audio = recognizer.listen(source)

print("\nProcessing your voice...")

with open("temp.wav", "wb") as f:
    f.write(audio.get_wav_data())

result = model.transcribe("temp.wav", language="bn")

print("\nYou said:")
print(result["text"])