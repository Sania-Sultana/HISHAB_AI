import speech_recognition as sr
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"

recognizer = sr.Recognizer()

recognizer.pause_threshold = 1.0
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


def speech_to_text():
    print("Loading microphone...")

    with sr.Microphone(device_index=1) as source:

        print("\nAdjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("\n================================")
        print("Speak your transaction now...")
        print("Stop speaking when you are finished.")
        print("================================\n")

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=None
        )

    print("\nAudio captured!")
    print("Converting speech to Bengali text...")

    try:
        text = recognizer.recognize_google(
            audio,
            language="bn-BD"
        )

        print("\nRecognized text:")
        print(text)

        return text

    except sr.UnknownValueError:
        print("\nCould not understand the speech.")
        return None

    except sr.RequestError as e:
        print("\nGoogle Speech Recognition error:")
        print(e)
        return None


def text_to_json(text):

    prompt = f"""
You are a transaction data extraction system.

Convert the Bengali transaction into JSON.

Return ONLY a valid JSON object.

The JSON MUST have exactly these three fields:

{{
    "customer_name": null,
    "cash_received": 0,
    "due_amount": 0
}}

Rules:

1. customer_name:
   - Extract the customer's name.
   - If no name is mentioned, use null.

2. cash_received:
   - Extract the amount of money received.
   - Convert Bengali number words into numeric values.
   - Example: পাঁচশ টাকা = 500

3. due_amount:
   - Extract the remaining due amount.
   - If no due amount is mentioned, use 0.

4. Do not invent information.

5. Do not write any explanation.

6. Do not use markdown.

7. Return ONLY JSON.

Transaction:
{text}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        raw_response = result.get("response", "")

        print("\nRaw Qwen response:")
        print(raw_response)

        data = json.loads(raw_response)

        return data

    except requests.exceptions.ConnectionError:

        print("\nCould not connect to Ollama.")
        print("Make sure the Ollama Docker container is running.")

    except json.JSONDecodeError:

        print("\nQwen did not return valid JSON.")

    except requests.exceptions.Timeout:

        print("\nQwen request timed out.")

    except Exception as e:

        print("\nError while processing with Qwen:")
        print(e)

    return None


def main():

    text = speech_to_text()

    if not text:
        return

    print("\nSending text to Qwen...")

    result = text_to_json(text)

    if result:

        print("\n================================")
        print("FINAL JSON")
        print("================================")

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=4
            )
        )


if __name__ == "__main__":
    main()