import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)
API_URL = os.getenv("UNSLOTH_API_URL", "http://localhost:8888/v1/systemone")
API_KEY = os.getenv("UNSLOTH_API_KEY", "").strip()
MODEL = os.getenv("LAYA_MODEL", "laya").strip() or "laya"

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "ai-maze-game", "laya_api_url": API_URL, "model": MODEL})

@app.post("/api/decide")
def decide():
    data = request.get_json(silent=True) or {}
    state = str(data.get("state", "")).strip()
    if not state:
        return jsonify({"error": "Missing maze state."}), 400

    payload = {
        "model": MODEL,
        "state": state,
        "questions": {
            "move": {
                "type": "choice",
                "instructions": "Choose the safest useful next move toward the maze exit. Do not choose a direction blocked by a wall. Prefer moves that reduce distance to the goal and avoid revisiting cells.",
                "criteria": {
                    "up": "Move one cell north/up if it is open and helps reach the exit.",
                    "right": "Move one cell east/right if it is open and helps reach the exit.",
                    "down": "Move one cell south/down if it is open and helps reach the exit.",
                    "left": "Move one cell west/left if it is open and helps reach the exit."
                }
            }
        }
    }
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=90)
        try:
            body = response.json()
        except ValueError:
            body = {"raw_response": response.text}
        if not response.ok:
            return jsonify({"error": "Unsloth/Laya API returned an error.", "status": response.status_code, "details": body}), 502
        answer = (body.get("answers") or {}).get("move", {})
        return jsonify({"choice": answer.get("choice"), "probabilities": answer.get("probabilities", {}), "confidence": answer.get("confidence"), "raw": body})
    except requests.RequestException as exc:
        return jsonify({"error": "Could not reach Unsloth Decision API.", "details": str(exc), "hint": "Make sure Unsloth is open and Settings → API → Decision API → Serve requests is enabled."}), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
