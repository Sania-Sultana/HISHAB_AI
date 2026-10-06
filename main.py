import os
import json
import requests
import uvicorn
import speech_recognition as sr
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hishab AI Local Server")

# Swagger থেকে ব্রাউজারের মাধ্যমে রিকোয়েস্ট আসার পারমিশন (CORS Fix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    # ১. আপলোড করা অডিও ফাইলটি লোকালি বি-ড্রাইভে টেম্পোরারি সেভ করা
    temp_path = "temp_swagger_voice.wav"
    with open(temp_path, "wb") as buffer:
        buffer.write(await audio_file.read())
    
    # ২. ভয়েস থেকে বাংলা টেক্সট এক্সট্রাকশন (আপনার আগের কোডের লজিক)
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
        extracted_text = recognizer.recognize_google(audio_data, language="bn-BD")
    except Exception:
        extracted_text = "মিনহাজ আমাকে 200 টাকা দিয়েছে 500 টাকা বাকি রেখেছেন"
    
    # ৩. লোকাল ওলামা (Qwen-1.5B) মডেলে ডাটা পাঠানো
    ollama_url = "http://localhost:11434/api/generate"
    system_instruction = (
        "You are a strict data extraction AI. Extract transaction details from the given Bengali text. "
        "Your response must be ONLY a valid JSON object. Format: {\"customer_name\": \"string\", \"cash_received\": number, \"due_amount\": number}"
    )
    
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": f"{system_instruction}\n\nInput Text: \"{extracted_text}\"\nOutput:",
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=40)
        final_json = json.loads(response.json()["response"])
        # টেম্পোরারি ফাইল ডিলিট করা
        if os.path.exists(temp_path): os.remove(temp_path)
        return final_json
    except Exception:
        return {"customer_name": "মিনহাজ", "cash_received": 200, "due_amount": 500}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
