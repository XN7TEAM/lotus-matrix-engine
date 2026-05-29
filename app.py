"""
Lotus Matrix Engine — Flask Application
© 2026 Nicholas Desjardins. All Rights Reserved.
"""
 
from flask import Flask, render_template, jsonify, request, abort
from functools import wraps
from core_engine import LotusCylinderEngine
import time
import random
import secrets
import string
 
app = Flask(__name__)
app.config['ENV']   = 'production'
app.config['DEBUG'] = False
 
spatial_engine = LotusCylinderEngine()
ACTIVE_SESSION_TOKENS = set()
 
system_telemetry = {
    "governor_apex":          1.047,
    "current_angle":          0.000,
    "system_status":          "SECURE",
    "attack_active":          False,
    "processing_delta":       0.02110,
    "intruder_tier":          None,
    "target_trajectory":      0.0,
    "incident_escrow_report": None,
}
 
# ── Helpers ──────────────────────────────────────────────────────────────────
 
def generate_threat_codename():
    prefix = random.choice(["VECTOR", "PHANTOM", "SHADOW", "INTRUDER", "SPECTRE"])
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{suffix}"
 
def _validate_hex(value: str) -> bool:
    return bool(value) and all(c in "0123456789ABCDEFabcdef" for c in value)
 
# ── Auth decorator ───────────────────────────────────────────────────────────
 
def require_session_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            abort(401, description="Missing session token.")
        token = auth.split(" ", 1)[1]
        if token not in ACTIVE_SESSION_TOKENS:
            abort(401, description="Invalid session token.")
        return f(*args, **kwargs)
    return decorated
 
# ── Routes ───────────────────────────────────────────────────────────────────
 
@app.route("/")
def load_interface():
    return render_template("index.html")
 
 
@app.route("/api/handshake", methods=["POST"])
def verify_handshake():
    payload = request.get_json(silent=True) or {}
    alignment_state = payload.get("alignment_state", 0.0)
 
    if not isinstance(alignment_state, (int, float)):
        return jsonify({"authenticated": False, "message": "Invalid payload."}), 400
 
    if abs(float(alignment_state) - 1.047) < 0.001:
        token = secrets.token_hex(32)
        ACTIVE_SESSION_TOKENS.add(token)
        return jsonify({
            "authenticated": True,
            "token": token,
            "message": "Spatiotemporal target confirmation match. Secure token minted."
        })
 
    return jsonify({
        "authenticated": False,
        "message": "Kinetic coordination vector mismatch."
    }), 403
 
 
@app.route("/api/process", methods=["POST"])
@require_session_token
def handle_api_request():
    payload    = request.get_json(silent=True) or {}
    data_input = payload.get("data", "").strip().upper()
    key_input  = payload.get("key",  "").strip().upper()
 
    if not data_input or not key_input:
        return jsonify({"success": False, "error": "Incomplete coordinate transmission vectors."}), 400
 
    if not _validate_hex(data_input) or not _validate_hex(key_input):
        return jsonify({"success": False, "error": "Inputs must be valid hexadecimal strings."}), 400
 
    if len(data_input) > 32 or len(key_input) > 32:
        return jsonify({"success": False, "error": "Input exceeds 32-character maximum."}), 400
 
    try:
        t0 = time.perf_counter()
        result = spatial_engine.process_clockwise_transform(data_input, key_input)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        system_telemetry["processing_delta"] = elapsed_ms
 
        return jsonify({
            "success":    True,
            "inventor":   "Nicholas Desjardins",
            "output":     result["cipher_output"],
            "latency_ms": f"{elapsed_ms:.5f} ms",
            "telemetry":  result["telemetry"],
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception:
        return jsonify({"success": False, "error": "Internal core structural failure."}), 500
 
 
@app.route("/api/telemetry", methods=["GET"])
@require_session_token
def get_telemetry():
    if system_telemetry["attack_active"]:
        system_telemetry["governor_apex"]    = round(random.uniform(2.500, 3.999), 3)
        system_telemetry["processing_delta"] = round(random.uniform(0.045, 0.065), 5)
    else:
        system_telemetry["governor_apex"] = 1.047
 
    return jsonify(system_telemetry)
 
 
@app.route("/api/simulate-attack", methods=["POST"])
@require_session_token
def simulate_attack():
    payload      = request.get_json(silent=True) or {}
    attack_state = bool(payload.get("active", False))
    system_telemetry["attack_active"] = attack_state
 
    if attack_state:
        codename = generate_threat_codename()
        tier     = random.randint(1, 4)
        traj     = round(random.uniform(0.0, 6.283), 3)
        sim_ip   = f"185.{random.randint(10,254)}.{random.randint(0,254)}.{random.randint(1,254)}"
 
        system_telemetry.update({
            "system_status":     f"UNDER ATTACK // ALLOCATED: {codename}",
            "intruder_tier":     tier,
            "target_trajectory": traj,
            "incident_escrow_report": {
                "allocated_codename":        codename,
                "timestamp_epoch_ms":        int(time.time() * 1000),
                "spatial_entry_tier":        tier,
                "network_trajectory_vector": traj,
                "captured_telemetry": {
                    "inbound_latency_ms":           f"{system_telemetry['processing_delta']:.5f} ms",
                    "simulated_device_fingerprint": secrets.token_hex(8).upper(),
                    "simulated_spatial_gps":        "43.6532 N, 79.3832 W",
                    "attacker_ip_address":          sim_ip,
                },
                "status": "ISOLATED_AND_PASSED_TO_AUTHORITIES",
            },
        })
    else:
        system_telemetry.update({
            "system_status":          "SECURE",
            "intruder_tier":          None,
            "target_trajectory":      0.0,
            "incident_escrow_report": None,
        })
 
    return jsonify({"status": "State Confirmed", "telemetry": system_telemetry})
 
 
# ── Error handlers ───────────────────────────────────────────────────────────
 
@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "Unauthorized", "message": str(e)}), 401
 
@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "Forbidden", "message": str(e)}), 403
 
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404
 
@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500
 
 
# ── Entry point ──────────────────────────────────────────────────────────────
 
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
 
