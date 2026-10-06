import json
import time
from pipeline import process_actual_voice_pipeline

# Dictionary linking Dialect names to your physical file paths
regional_tests = {
    "প্রমিত বাংলা (Standard)": "voice_standard.wav",
    "কুমিল্লা আঞ্চলিক (Cumilla)": "voice_cumilla.wav",
    "চট্টগ্রাম আঞ্চলিক (Chittagong)": "voice_chatgaia.wav"
}

print("========================================================")
print("৩-৪টি ভিন্ন আঞ্চলিক উচ্চারণে বাংলা ভয়েস ল্যাটেন্সি টেস্ট রিপোর্ট")
print("========================================================")

report_card = []

for dialect_name, file_path in regional_tests.items():
    print(f"\n▶️ Running Pipeline Execution for: [{dialect_name}]")
    
    # Executing the real working voice pipeline you built
    json_res, stt_t, llm_t = process_actual_voice_pipeline(file_path)
    
    if json_res:
        total_t = stt_t + llm_t
        
        # Validating accuracy: Did the local LLM correctly capture 200 received and 500 due?
        is_correct = "Yes" if json_res.get("cash_received") == 200 and json_res.get("due_amount") == 500 else "Partial/No"
        
        report_card.append({
            "Dialect": dialect_name,
            "STT Latency": f"{stt_t:.2f}s",
            "LLM Latency": f"{llm_t:.2f}s",
            "Total Time": f"{total_t:.2f}s",
            "JSON Correct?": is_correct,
            "Extracted Data": json_res
        })
    else:
        print(f"❌ Failed to parse data for {dialect_name}")

# Print out the final aggregated metrics table
print("\n========================================================")
print("📝 Sprint Sign-Off & Technical Blog Benchmark Table:")
print("========================================================")
print(json.dumps(report_card, indent=4, ensure_ascii=False))
