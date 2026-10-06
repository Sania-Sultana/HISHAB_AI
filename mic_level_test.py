import speech_recognition as sr
import audioop

recognizer = sr.Recognizer()

with sr.Microphone(device_index=1) as source:

    print("Microphone:", source)

    print("\nStay quiet for 2 seconds...")
    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("\nNow SPEAK LOUDLY for 5 seconds...")
    print("Say: আমি পাঁচশ টাকা নিয়েছি")

    audio = recognizer.listen(
        source,
        timeout=10,
        phrase_time_limit=5
    )

print("\nAudio captured!")

raw_audio = audio.get_raw_data()

rms = audioop.rms(
    raw_audio,
    audio.sample_width
)

print("\nMicrophone RMS level:", rms)

if rms < 100:
    print("\nWARNING: Very low microphone input.")
    print("Your voice is probably not reaching the microphone.")

elif rms < 500:
    print("\nMicrophone input is LOW.")

elif rms < 2000:
    print("\nMicrophone input looks NORMAL.")

else:
    print("\nMicrophone input is HIGH.")

print("\nTrying Bengali recognition...")

try:

    text = recognizer.recognize_google(
        audio,
        language="bn-BD"
    )

    print("\nRecognized text:")
    print(text)

except sr.UnknownValueError:

    print("\nMicrophone received audio, but speech could not be understood.")

except sr.RequestError as e:

    print("\nGoogle recognition error:")
    print(e)