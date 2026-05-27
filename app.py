from flask import Flask, render_template, jsonify, request
from core_engine import LotusCylinderEngine
import time
import random

app = Flask(__name__)

# Single source of truth instance for core backend operations
spatial_engine = LotusCylinderEngine()

system_telemetry = {
    "governor_apex": 1.047,
    "current_angle": 0.000,
    "system_status": "SECURE",
    "attack_active": False,
    "processing_delta": 0.02710,
    "intruder_tier": None,
    "target_trajectory": 0.0
}

@app.route('/')
def load_interface():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def handle_api_request():
    payload = request.get_json() or {}
    data_input = payload.get("data", "").strip()
    key_input = payload.get("key", "").strip()

    if not data_input or not key_input:
        return jsonify({"success": False, "error": "Missing data or force key vector."}), 400

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
    except Exception as sys_err:
        return jsonify({"success": False, "error": f"Internal matrix failure: {str(sys_err)}"}), 500

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    if system_telemetry["attack_active"]:
        system_telemetry["governor_apex"] = round(random.uniform(2.500, 3.999), 3)
        system_telemetry["processing_delta"] = round(random.uniform(0.85000, 1.45000), 5)
        # Keep the simulation shifting to model ongoing lateral threat vector tracking
        if random.random() > 0.7:
            system_telemetry["intruder_tier"] = random.randint(1, 4)  # Matched to your 4 3D node planes
            system_telemetry["target_trajectory"] = round(random.uniform(0.0, 6.28), 3)
    else:
        system_telemetry["governor_apex"] = round(1.047 + random.uniform(-0.03, 0.03), 3)
        system_telemetry["intruder_tier"] = None
        system_telemetry["target_trajectory"] = 0.0
        
    return jsonify(system_telemetry)

@app.route('/api/simulate-attack', methods=['POST'])
def simulate_attack():
    data = request.json or {}
    system_telemetry["attack_active"] = data.get("active", False)
    system_telemetry["system_status"] = "UNDER ATTACK" if system_telemetry["attack_active"] else "SECURE"
    
    if system_telemetry["attack_active"]:
        # Restrict to layers 1-4 to cleanly map against your UI cylinder rings
        system_telemetry["intruder_tier"] = random.randint(1, 4)
        system_telemetry["target_trajectory"] = round(random.uniform(0.0, 6.28), 3)
    else:
        system_telemetry["intruder_tier"] = None
        system_telemetry["target_trajectory"] = 0.0
        
    return jsonify({"status": "Signal Broadcasted", "telemetry": system_telemetry})

if __name__ == "__main__":
    app.run(debug=True)
