# SOC Analyzer v2 - PRO - Interactive Real AI
import json
from openai import OpenAI

# PASTE YOUR SAME KEY HERE (the soc-analyzer-2 one)
API_KEY = "PASTE_YOUR_PASSKEY_HERE"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

print("="*50)
print("🛡️  SOC ANALYZER v2 - REAL AI - Type 'quit' to exit")
print("="*50)

while True:
    print("\n--- Paste your security log below ---")
    log = input("Log > ")
    
    if log.lower() in ["quit", "exit", "q"]:
        print("👋 Goodbye Analyst!")
        break
    
    if len(log) < 5:
        print("⚠️ Log too short, try again")
        continue

    print("\n🤖 AI Analyzing...")
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a Senior SOC Analyst. Analyze the log. Return ONLY JSON with: finding, severity (Critical/High/Medium/Low), impact, recommendation (list). Be concise."},
                {"role": "user", "content": f"Analyze this log:\n{log}"}
            ],
            temperature=0.2
        )
        result = response.choices[0].message.content
        print("\n--- AI REPORT ---")
        print(result)
        
        # Save each report
        with open("soc_report_v2.txt", "a") as f:
            f.write("\n\n=== LOG: " + log + " ===\n" + result)
        print("\n✅ Saved to soc_report_v2.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")