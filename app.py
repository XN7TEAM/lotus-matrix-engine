from flask import Flask, render_template, jsonify, request, abort, send_from_directory
from functools import wraps
from core_engine import LotusCylinderEngine
import time
import random
import secrets
import string
import os

# Initialize Flask with explicit static/template folders
app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['ENV'] = 'production'
app.config['DEBUG'] = False

spatial_engine = LotusCylinderEngine()
ACTIVE_SESSION_TOKENS = set()

system_telemetry = {
    "governor_apex": 1.047,
    "current_angle": 0.000,
    "system_status": "SECURE",
    "attack_active": False,
    "intruder tier": None,
    "processing_delta": 0.02110,
    "target_trajectory": 0.0,
    "incident_escrow_report": None,
}

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
