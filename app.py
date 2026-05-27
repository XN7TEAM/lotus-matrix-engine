from flask import Flask, render_template, jsonify, request, abort
from core_engine import LotusCylinderEngine
import time
import random
import secrets
import string

app = Flask(__name__)

# Complete enforcement of secure enterprise operational profiles
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

spatial_engine = LotusCylinderEngine()
ACTIVE_SESSION_TOKENS = set()

system_telemetry = {
    "governor_apex": 1.047,
    "current_angle": 0.000,
    "system_status": "SECURE",
    "attack_active": False,
    "processing_delta": 0.02110,
    "intruder_tier": None,
    "target_trajectory": 0.0,
    "incident_escrow_report": None
}

def generate_threat_codename():
    """Generates unique, non-descriptive tracking identities for spatial intruder logs."""
    prefix = random.choice(["VECTOR", "PHANTOM", "SHADOW", "INTRUDER", "SPECTRE"])
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{suffix}"

# Cryptographic Token Check Decorator
def require_session_token(f):
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            abort(401, description="Missing cryptographic session vector validation.")
        token = auth_header.split(" ")[1]
        if token not in ACTIVE_SESSION_TOKENS:
            abort(401, description="Invalid cryptographic token signature.")
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def load_interface():
    return render_template('index.html')

@app.route('/api/handshake', methods=['POST'])
def verify_handshake():
    """Hardened entry verification endpoint testing exact 60 degree coordination alignments."""
    payload = request.get_json() or {}
    alignment_state = payload.get("alignment_state", 0.0)
    
    if abs(alignment_state - 1.047) < 0.001:
        new_token = secrets.token_hex(32)
        ACTIVE_SESSION_TOKENS.add(new_token)
        return jsonify({
            "authenticated": True,
            "token": new_token,
            "message": "Spatiotemporal target confirmation match. Secure token minted."
        })
    
    return jsonify({
        "authenticated": False,
        "message": "Kinetic coordination vector mismatch."
    }), 403

@app.route('/api/process', methods=['POST'])
@require_session_token
def handle_api_request():
    payload = request.get_json() or {}
    data_input = payload.get("data", "").strip()
    key_input = payload.get("key", "").strip()

    if not data_input or not key_input:
        return jsonify({"success": False, "error": "Incomplete coordinate transmission vectors."}), 400

    try:
        start_time = time.perf_counter()
        matrix_results = spatial_engine.process_clockwise_transform(data_input, key_input)
        execution_delta = time.perf_counter() - start_time

        system_telemetry["processing_delta"] = execution_delta * 1000

        return jsonify({
            "success": True,
            "inventor": "Nicholas Desjardins",
            "output": matrix_results["cipher_output"],
            "latency_ms": f"{system_telemetry['processing_delta']:.5f} ms",
            "telemetry": matrix_results["telemetry"]
        })
    except ValueError as val_err:
        return jsonify({"success": False, "error": str(val_err)}), 400
    except Exception:
        return jsonify({"success": False, "error": "Internal core structural failure."}), 500

@app.route('/api/telemetry', methods=['GET'])
@require_session_token
def get_telemetry():
    """Streams running runtime configurations straight to the governance display layers."""
    if system_telemetry["attack_active"]:
        system_telemetry["governor_apex"] = round(random.uniform(2.500, 3.999), 3)
        system_telemetry["processing_delta"] = round(random.uniform(0.04500, 0.06500), 5)
    else:
        system_telemetry["governor_apex"] = 1.047
        
    return jsonify(system_telemetry)

@app.route('/api/simulate-attack', methods=['POST'])
@require_session_token
def simulate_attack():
    data = request.json or {}
    attack_state = data.get("active", False)
    system_telemetry["attack_active"] = attack_state
    
    if attack_state:
        codename = generate_threat_codename()
        system_telemetry["system_status"] = f"UNDER ATTACK // ALLOCATED: {codename}"
        system_telemetry["intruder_tier"] = random.randint(1, 4)
        system_telemetry["target_trajectory"] = round(random.uniform(0.0, 6.28), 3)
        
        # Real-Time Forensic Escrow JSON Architecture compiled automatically by the Governance Engine
        system_telemetry["incident_escrow_report"] = {
            "allocated_codename": codename,
            "timestamp_epoch_ms": int(time.time() * 1000),
            "spatial_entry_tier": system_telemetry["intruder_tier"],
            "network_trajectory_vector": system_telemetry["target_trajectory"],
            "captured_telemetry": {
                "inbound_latency_ms": f"{system_telemetry['processing_delta']:.5f} ms",
                "simulated_device_fingerprint": secrets.token_hex(8).upper(),
                "simulated_spatial_gps": "43.6532 N, 79.3832 W"
            },
            "status": "ISOLATED_AND_PASSED_TO_AUTHORITIES"
        }
    else:
        system_telemetry["system_status"] = "SECURE"
        system_telemetry["intruder_tier"] = None
        system_telemetry["target_trajectory"] = 0.0
        system_telemetry["incident_escrow_report"] = None
        
    return jsonify({"status": "State Confirmed", "telemetry": system_telemetry})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
