from flask import Flask, request, jsonify
import uuid, time, random, requests, re
from threading import Thread

app = Flask(__name__)

TEST_INDEX_URL = "https://24f1001129.github.io/tests/"
DEFAULT_TIMEOUT = 180
SERVER_BASE_URL = "http://localhost:5000"

quizzes = []
sessions = {}

def now(): return int(time.time())

def load_links_from_file():
    """Load links from the local index.html file."""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        links = re.findall(r'href="([^"]+)"', html)
        full_links = []

        for L in links:
            # Skip non-test links (like external ones if any, though regex catches hrefs)
            # We assume links in index.html are relative paths to tests
            if not L.startswith("http"):
                # Construct the full public URL
                full_url = TEST_INDEX_URL.rstrip("/") + "/" + L.lstrip("/")
                full_links.append(full_url)
        
        return full_links
    except Exception as e:
        print("FILE LOAD ERROR:", e)
        return []

def load_quizzes():
    quizzes.clear()
    for url in load_links_from_file():
        quizzes.append({
            "id": str(uuid.uuid4()),
            "url": url,
            "expected": None
        })
    print("Loaded quizzes:", quizzes)

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

    # Accept answer and move on (this is a mock evaluator)
    session["history"].append({"url": url, "answer": answer})

    exclude = [h.get("quiz_id") for h in session["history"]]
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
