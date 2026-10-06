import os  
import requests
from flask import Flask, request, jsonify

LLM_URL = os.environ.get("LLM_URL", "http://localhost:11434/v1/chat/completions")
LLM_MODEL = os.environ.get("LLM_MODEL", "llama3:latest")

app = Flask(__name__)

@app.get("/")
def index():
    return app.send_static_file("index.html")

@app.post("/chat")
def chat():
    question = request.json.get("question")
    r = requests.post(LLM_URL, json={
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": question}],
    }, timeout=120)
    r.raise_for_status()
    answer = r.json()["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

