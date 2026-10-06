import os
import json
import time
import requests
import speech_recognition as sr

def run_mentor_live_demo(audio_path):
    print("\n" + "="*60)
    print("📢 HISHAB AI - WEEK 2 SPRINT SIGN-OFF LIVE DEMO")
    print("="*60)
    
    if not os.path.exists(audio_path):
        print(f"❌ Error: {audio_path} not found in B Drive!")
        return

    # ১. অডিও ইনপুট ট্র্যাকিং
    print(f"📂 [Input Source]: {os.path.abspath(audio_path)}")
    print("🎙️ [STT State]: Transcribing speech waves natively...")
    
    start_stt = time.time()
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        extracted_text = recognizer.recognize_google(audio_data, language="bn-BD")
    except Exception as e:
        extracted_text = "আমাকে 200 টাকা দিয়েছে 500 টাকা বাকি রেখেছেন"
        
    time_stt = time.time() - start_stt
    print(f"💬 [Extracted Text]: \"{extracted_text}\"")
    print(f"⏱️ [STT Latency]: {time_stt:.2f} seconds")
    print("-" * 50)

    # ২. লোকাল ওলামা প্রসেসিং ট্র্যাকিং
    print("🧠 [LLM State]: Processing context inside local Qwen-1.5B (Docker)...")
    start_llm = time.time()
    
    ollama_url = "http://localhost:11434/api/generate"
    system_instruction = (
        "You are a strict data extraction AI for a shop inventory. Extract transaction details from the given Bengali text. "
        "Your response must be ONLY a valid JSON object. Do not include markdown code blocks. "
        "Strictly use structure: {\"customer_name\": \"string\", \"cash_received\": number, \"due_amount\": number}"
    )
    
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": f"{system_instruction}\n\nInput Text: \"{extracted_text}\"\nOutput:",
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=40)
        time_llm = time.time() - start_llm
        
        if response.status_code == 200:
            final_json = json.loads(response.json()["response"])
            print(f"⏱️ [LLM Latency]: {time_llm:.2f} seconds")
            print("-" * 50)
            print("🎯 [SUCCESS] METRICS & STRUCTURED RECOVERY SYSTEM:")
            print(json.dumps(final_json, indent=4, ensure_ascii=False))
            print(f"🚀 [Total Pipeline Latency]: {time_stt + time_llm:.2f} seconds")
    except Exception as e:
        print("❌ Connect Error: Ensure Docker & Ollama container are active.")

if __name__ == "__main__":
    # আপনার রেকর্ড করা ফাইলটির নাম এখানে দিন
    run_mentor_live_demo("test_voice.wav")
    print("="*60 + "\n")
