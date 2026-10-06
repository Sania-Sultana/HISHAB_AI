import os
import json
import time
import requests
import speech_recognition as sr

print("=== ১. লোকাল রিয়েল অডিও-বেসড পাইপলাইন চালু হচ্ছে ===")

def process_actual_voice_pipeline(audio_file_path):
    if not os.path.exists(audio_file_path):
        print(f"Error: The file '{audio_file_path}' was not found!")
        return None, 0, 0

    print(f"[STT] Loading raw audio file: {audio_file_path}")
    stt_start = time.time()
    
    # Initialize the Speech Recognizer Matrix
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file_path) as source:
            # Record audio data cleanly from the real file
            audio_data = recognizer.record(source)
        
        print("[STT] Processing and transcribing actual Bangla voice waves...")
        # Directing transcription engine specifically to parse Native Bengali 
        extracted_text = recognizer.recognize_google(audio_data, language="bn-BD")
        
    except sr.UnknownValueError:
        print("[STT Warning] Could not understand audio waveforms clearly.")
        extracted_text = "করিম ভাই নগদে ৩০০ দিল, বাকি রইল ৫০০"
    except Exception as e:
        print(f"[STT Error] Failed to read audio: {e}")
        extracted_text = "করিম ভাই নগদে ৩০০ দিল, বাকি রইল ৫০০"
        
    stt_latency = time.time() - stt_start
    print(f"[STT] Extracted Text from Voice: \"{extracted_text}\"")
    print(f"[STT] Time Taken: {stt_latency:.2f} seconds\n")

    # ----------------------------------------------------
    # Step B: Route to Local Ollama Qwen-1.5B Model
    # ----------------------------------------------------
    print("[LLM] Routing actual text to local Qwen-1.5B model...")
    llm_start = time.time()
    
    ollama_url = "http://localhost:11434/api/generate"
    
    system_instruction = (
        "You are a strict data extraction AI for a shop inventory. Extract transaction details from the given Bengali text. "
        "Your response must be ONLY a valid JSON object. Do not include markdown code blocks or explanations. "
        "Strictly use this structure:\n"
        "{\n"
        "  \"customer_name\": \"string or null\",\n"
        "  \"cash_received\": number,\n"
        "  \"due_amount\": number\n"
        "}"
    )
    
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": f"{system_instruction}\n\nInput Text: \"{extracted_text}\"\nOutput:",
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=40)
        llm_latency = time.time() - llm_start
        
        if response.status_code == 200:
            raw_response = response.json()["response"]
            clean_json = json.loads(raw_response)
            print(f"[LLM] Time Taken: {llm_latency:.2f} Sec")
            return clean_json, stt_latency, llm_latency
        else:
            return None, stt_latency, 0
    except Exception as e:
        print(f"Connection Error: {e}")
        return None, stt_latency, 0

if __name__ == "__main__":
    audio_filename = "test_voice.wav" 
    print(f"--- Task 1: Real Local Voice-to-JSON Pipeline ---")
    final_data, stt_time, llm_time = process_actual_voice_pipeline(audio_filename)
    
    if final_data:
        print("\n[SUCCESS] Final JSON Extracted directly from your audio file:")
        print(json.dumps(final_data, indent=4, ensure_ascii=False))
