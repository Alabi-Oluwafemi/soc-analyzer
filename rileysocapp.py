from flask import Flask, request, render_template_string
from openai import OpenAI

# PASTE YOUR KEY HERE (same one)
API_KEY = "gPASTE_YOUR_PASSKEY_HERE"

client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
app = Flask(__name__)

HTML = """
<html><head><title>SOC Analyzer</title>
<style>
body{font-family:Arial;background:#0f172a;color:white;padding:30px}
textarea{width:100%;height:100px;padding:10px}
button{background:#22c55e;color:white;padding:12px 20px;border:none;font-size:16px;cursor:pointer}
.box{background:#1e293b;padding:20px;border-radius:10px;margin-top:20px;white-space:pre-wrap}
h1{color:#22c55e}
</style></head>
<body>
<h1>🛡️ SOC ANALYZER - AI Dashboard</h1>
<form method="POST">
<textarea name="log" placeholder="Paste security log here... e.g. Failed login 500 times..."></textarea><br><br>
<button type="submit">Analyze with AI 🤖</button>
</form>
{% if result %}
<div class="box"><h3>AI REPORT:</h3>{{ result }}</div>
{% endif %}
</body></html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    result = ""
    if request.method == "POST":
        log = request.form.get("log","")
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role":"system","content":"You are a Senior SOC Analyst. Return Finding, Severity, Impact, Recommendation."},
                {"role":"user","content":f"Analyze: {log}"}
            ],
            temperature=0.2
        )
        result = resp.choices[0].message.content
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)