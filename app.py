from flask import Flask, render_template, jsonify
from core_engine import LotusCylinderEngine
import random

app = Flask(__name__)
engine = LotusCylinderEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/telemetry')
def get_telemetry():
    # Simulate a threat if random trigger hits
    threat = random.choice([True, False])
    data, log = engine.process_transform("ABCDEF12", "12345678")
    
    return jsonify({
        "status": "SECURE" if not threat else "ATTACK_ACTIVE",
        "telemetry": log,
        "threat_ip": f"185.{random.randint(10,254)}.0.{random.randint(1,254)}" if threat else None
    })

if __name__ == '__main__':
    app.run(debug=True)

# --- ROUTES ---

@app.route('/')
def index():
    """Serves the main Lotus Matrix interface."""
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    """Ensures CSS and JS files are served correctly."""
    return send_from_directory('static', path)

# --- HELPERS & AUTH ---

def generate_threat_codename():
    prefix = random.choice(["VECTOR", "PHANTOM", "SHADOW", "INTRUDER", "SPECTRE"])
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{suffix}"

def validate_hex(value: str) -> bool:
    return bool(value) and all(c in "0123456789ABCDEFabcdef" for c in value)

def require_session_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if auth not in ACTIVE_SESSION_TOKENS:
            abort(401)
        return f(*args, **kwargs)
    return decorated

# --- TELEMETRY ENDPOINT ---

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    return jsonify({"status": "State Confirmed", "telemetry": system_telemetry})

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "Unauthorized Access"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
