from flask import Flask, render_template, jsonify, request
from core_engine import LotusCylinderEngine
import time
import random

app = Flask(__name__)

# Initialize your core mathematical engine instance
spatial_engine = LotusCylinderEngine()

# System states to track live telemetry & simulation features
system_telemetry = {
    "governor_apex": 1.047,
    "current_angle": 0.000,
    "system_status": "SECURE",
    "attack_active": False,
    "processing_delta": 0.02710
}

@app.route('/')
def load_interface():
    """Serves the front-end dashboard screen."""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def handle_api_request():
    """Secure API endpoint executing real matrix logic safely via the core engine."""
    payload = request.get_json() or {}
    data_input = payload.get("data", "").strip()
    key_input = payload.get("key", "").strip()

    if not data_input or not key_input:
        return jsonify({"success": False, "error": "Missing data or force key vector."}), 400

    try:
        start_time = time.perf_counter()
        
        # Route processing through your updated, 8-tier core_engine.py matrix loop
        matrix_results = spatial_engine.process_clockwise_transform(data_input, key_input)
        
        execution_delta = time.perf_counter() - start_time

        # Update real-time metric tracker with true microsecond latency
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
    except Exception as sys_err:
        return jsonify({"success": False, "error": f"Internal matrix failure: {str(sys_err)}"}), 500

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    """Feeds live background fluctuating 'Gov' numbers to the UI stream."""
    if system_telemetry["attack_active"]:
        system_telemetry["governor_apex"] = round(random.uniform(2.500, 3.999), 3)
        # Force high processing latency when under simulation stress
        system_telemetry["processing_delta"] = round(random.uniform(0.85000, 1.45000), 5)
    else:
        system_telemetry["governor_apex"] = round(1.047 + random.uniform(-0.03, 0.03), 3)
        
    return jsonify(system_telemetry)

@app.route('/api/simulate-attack', methods=['POST'])
def simulate_attack():
    """Receives presentation triggers to instantly toggle the security warning state."""
    data = request.json or {}
    system_telemetry["attack_active"] = data.get("active", False)
    system_telemetry["system_status"] = "UNDER ATTACK" if system_telemetry["attack_active"] else "SECURE"
    return jsonify({"status": "Signal Broadcasted", "telemetry": system_telemetry})

if __name__ == "__main__":
    app.run(debug=True)
