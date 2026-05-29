# Copyright (C) 2026 Nicholas Desjardins. All Rights Reserved.
from flask import Flask, render_template, jsonify, request, abort
from core_engine import LotusCylinderEngine
import time
import random
import secrets
import string
import subprocess

app = Flask(__name__)

app.config['ENV'] = 'production'
app.config['DEBUG'] = False

spatial_engine = LotusCylinderEngine()

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
    prefix = random.choice(["VECTOR", "PHANTOM", "SHADOW", "INTRUDER", "SPECTRE"])
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{suffix}"

@app.route('/')
def load_interface():
    """Renders the primary visual matrix dashboard interface frame."""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def handle_api_request():
    """Processes clockwise spatial matrix transformations using custom core coordinate anchors."""
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
            "latency_ms": f"{system_telemetry['processing_delta']:.5f}",
            "telemetry": matrix_results["telemetry"]
        })
    except ValueError as val_err:
        return jsonify({"success": False, "error": str(val_err)}), 400
    except Exception:
        return jsonify({"success": False, "error": "Internal core structural failure."}), 500

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    """Pipes live matrix tracking and telemetry updates straight down to the dashboard gauges."""
    if system_telemetry["attack_active"]:
        system_telemetry["governor_apex"] = round(random.uniform(2.500, 3.999), 3)
        system_telemetry["processing_delta"] = round(random.uniform(0.04500, 0.06500), 5)
    else:
        system_telemetry["governor_apex"] = 1.047
        
    return jsonify(system_telemetry)

@app.route('/api/terminal/execute', methods=['POST'])
def execute_linux_shell_cmd():
    """Intercepts terminal stream inputs from the dashboard and passes commands to subprocess shells."""
    payload = request.get_json() or {}
    
    # Map key variable explicitly to frontend JavaScript request key
    raw_command = payload.get("command", "").strip()
    
    if not raw_command:
        return jsonify({"output": "Execution Blocked: Null command string passed."}), 400
        
    # Clear logs trigger capture
    if raw_command.lower() in ["clear", "cls"]:
        return jsonify({"output": "CLEAR_SCREEN"})
        
    # Prevent interactive background operations from dropping server pipelines
    forbidden_tokens = ["top", "htop", "watch", "nano", "vim", "gdb", "ssh", "sudo"]
    if any(token in raw_command.split() for token in forbidden_tokens):
        return jsonify({"output": "Execution Blocked: Interactive foreground editors or sudo access disabled for presentation stability."})

    try:
        completed_process = subprocess.run(
            raw_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=4
        )
        
        response_output = completed_process.stdout
        error_output = completed_process.stderr
        
        if not response_output and not error_output:
            combined_response = "Command executed cleanly returning no stdout indicators."
        else:
            combined_response = response_output + error_output
            
        return jsonify({"output": combined_response})
        
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Command processing timed out (Execution limit exceeded 4.0s)."}), 408
    except Exception as general_err:
        return jsonify({"output": f"OS Shell Handshake Error: {str(general_err)}"}), 500

@app.route('/api/simulate-attack', methods=['POST'])
def simulate_attack():
    """Simulates localized network vector threats to test active integrity safeguards."""
    data = request.json or {}
    attack_state = data.get("active", False)
    system_telemetry["attack_active"] = attack_state
    
    if attack_state:
        codename = generate_threat_codename()
        system_telemetry["system_status"] = f"UNDER ATTACK // ALLOCATED: {codename}"
        system_telemetry["intruder_tier"] = random.randint(1, 4)
        system_telemetry["target_trajectory"] = round(random.uniform(0.0, 6.28), 3)
        
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
