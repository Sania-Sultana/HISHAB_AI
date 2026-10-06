import speech_recognition as sr

print("Available microphones:\n")

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(index, ":", name)

print("\nTesting microphones...\n")

recognizer = sr.Recognizer()

for index, name in enumerate(sr.Microphone.list_microphone_names()):

    print(f"\nTesting device {index}: {name}")

    try:
        with sr.Microphone(device_index=index) as source:

            print("Speak for 3 seconds...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=3
            )

        print("Audio captured!")

        try:
            text = recognizer.recognize_google(
                audio,
                language="bn-BD"
            )

            print("Recognized:", text)

        except sr.UnknownValueError:
            print("Voice captured but could not understand.")

        except sr.RequestError as e:
            print("Google recognition error:", e)

    except Exception as e:

        print("Cannot use this microphone.")
        print("Error:", e)