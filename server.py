from flask import Flask, request, jsonify
import uuid, time, random, requests, re
from threading import Thread

app = Flask(__name__)

TEST_INDEX_URL = "https://24f1001129.github.io/tests/"
DEFAULT_TIMEOUT = 180
SERVER_BASE_URL = "http://localhost:5000"

QUIZ_ANSWERS = {
  "https://24f1001129.github.io/tests/analysis/test_1/index.html": "42.500",
  "https://24f1001129.github.io/tests/analysis/test_2/index.html": "3600",
  "https://24f1001129.github.io/tests/analysis/test_3/index.html": "1234",
  "https://24f1001129.github.io/tests/analysis/test_4/index.html": "55.1234",
  "https://24f1001129.github.io/tests/api_sourcing/test_1/index.html": "100000",
  "https://24f1001129.github.io/tests/api_sourcing/test_2/index.html": "98765",
  "https://24f1001129.github.io/tests/api_sourcing/test_3/index.html": "250.0",
  "https://24f1001129.github.io/tests/api_sourcing/test_4/index.html": "END-TOKEN-77",
  "https://24f1001129.github.io/tests/cleansing/test_1/index.html": "XF-834",
  "https://24f1001129.github.io/tests/cleansing/test_2/index.html": "REF-100001",
  "https://24f1001129.github.io/tests/cleansing/test_3/index.html": "1234567.89",
  "https://24f1001129.github.io/tests/cleansing/test_4/index.html": "50.000",
  "https://24f1001129.github.io/tests/processing/test_1/index.html": "7000",
  "https://24f1001129.github.io/tests/processing/test_2/index.html": "580",
  "https://24f1001129.github.io/tests/processing/test_3/index.html": "4321",
  "https://24f1001129.github.io/tests/processing/test_4/index.html": "123.5",
  "https://24f1001129.github.io/tests/visualization/test_1/index.html": "700",
  "https://24f1001129.github.io/tests/visualization/test_2/index.html": "1.0",
  "https://24f1001129.github.io/tests/visualization/test_3/index.html": "B",
  "https://24f1001129.github.io/tests/visualization/test_4/index.html": "12%",
  "https://24f1001129.github.io/tests/web_scraping/test_1/index.html": "TOKEN-12345",
  "https://24f1001129.github.io/tests/web_scraping/test_2/index.html": "314159",
  "https://24f1001129.github.io/tests/web_scraping/test_3/index.html": "WS-300",
  "https://24f1001129.github.io/tests/web_scraping/test_4/index.html": "5000"
}

quizzes = []
sessions = {}

def now(): return int(time.time())

def load_quizzes():
    quizzes.clear()
    for url, expected in QUIZ_ANSWERS.items():
        quizzes.append({
            "id": str(uuid.uuid4()),
            "url": url,
            "expected": expected
        })
    print(f"Loaded {len(quizzes)} quizzes.")

def pick_random_quiz(exclude=None):
    if exclude is None:
        exclude = []
    pool = [q for q in quizzes if q["id"] not in exclude]
    return random.choice(pool) if pool else None


@app.post("/start")
def start_session():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    participant = data.get("participant_callback")
    email = data.get("email")
    secret = data.get("secret")
    timeout = data.get("timeout", DEFAULT_TIMEOUT)

    if not participant or not email or not secret:
        return jsonify({"error": "participant_callback, email, secret required"}), 400

    if not quizzes:
        load_quizzes()

    first_quiz = pick_random_quiz()
    if not first_quiz:
        return jsonify({"error": "no quizzes available"}), 500

    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "id": session_id,
        "email": email,
        "secret": secret,
        "start_time": now(),
        "timeout": timeout,
        "current_quiz": first_quiz["id"],
        "history": [],
    }

    payload = {
        "email": email,
        "secret": secret,
        "url": first_quiz["url"],
        "submit_url": SERVER_BASE_URL + "/submit"
    }

    def notify():
        try:
            r = requests.post(participant, json=payload, timeout=10)
            sessions[session_id]["callback_response"] = {
                "code": r.status_code,
                "body": r.text
            }
        except Exception as e:
            sessions[session_id]["callback_response"] = {"error": str(e)}

    Thread(target=notify, daemon=True).start()

    return jsonify({"session_id": session_id, "quiz": first_quiz["url"]})

# ---------------------- SUBMIT ----------------------

@app.post("/submit")
def submit_answer():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    email = data.get("email")
    secret = data.get("secret")
    url = data.get("url")
    answer = data.get("answer")

    # Find session
    session = None
    for s in sessions.values():
        if s["email"] == email and s["secret"] == secret:
            q = next((q for q in quizzes if q["id"] == s["current_quiz"]), None)
            if q and q["url"] == url:
                session = s
                break

    if not session:
        return jsonify({"error": "no valid session"}), 403

    if now() - session["start_time"] > session["timeout"]:
        return jsonify({"error": "time expired"}), 403

    # Accept answer and verify
    session["history"].append({"url": url, "answer": answer})
    
    # Check if answer is correct
    is_correct = False
    expected_str = str(q["expected"]) if q["expected"] is not None else ""
    submitted_str = str(answer)
    
    # Simple loose comparison (case-insensitive, stripped)
    if expected_str.lower().strip() == submitted_str.lower().strip():
        is_correct = True
    
    if not is_correct:
        return jsonify({
            "correct": False, 
            "reason": f"Incorrect answer. Expected {expected_str}." 
        })

    # If correct, pick next quiz
    exclude = [h.get("quiz_id") for h in session["history"]]
    # Also exclude the current one just in case it wasn't in history yet (though we just added it)
    exclude.append(q["id"])
    
    next_quiz = pick_random_quiz(exclude)

    if not next_quiz:
        session["current_quiz"] = None
        return jsonify({"correct": True, "url": None})

    session["current_quiz"] = next_quiz["id"]
    return jsonify({"correct": True, "url": next_quiz["url"]})

# -----------------------------------------------------------

if __name__ == "__main__":
    load_quizzes()
    print("Eval server running on http://localhost:5000")
    app.run(debug=True)
