from flask import Flask, render_template, jsonify, request
import time
import random

app = Flask(__name__)

# System states to track live telemetry & simulation features
system_telemetry = {
    "governor_apex": 1.047,
    "current_angle": 0.000,
    "system_status": "SECURE",
    "attack_active": False,
    "processing_delta": 0.02710
}

# The 8 Complete Sync Tiers configuration referenced by the matrix layout
CYLINDER_TIERS = {
    1: {"binary": "0001", "val": 1, "name": "Alpha Base Axis"},
    2: {"binary": "0010", "val": 2, "name": "Beta Plane Layer"},
    3: {"binary": "0100", "val": 4, "name": "Gamma Vector Ring"},
    4: {"binary": "1000", "val": 8, "name": "Delta Polar Node"},
    5: {"binary": "0011", "val": 3, "name": "Epsilon Cross Sync"},
    6: {"binary": "0110", "val": 6, "name": "Zeta Lateral Shift"},
    7: {"binary": "1100", "val": 12, "name": "Eta High Boundary"},
    8: {"binary": "1111", "val": 15, "name": "Theta Apex Governor"}
}
LIMIT = 16  # Enforce Hexadecimal Modular Boundary Check

@app.route('/')
def load_interface():
    """Serves the front-end dashboard screen."""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def handle_api_request():
    """Secure API endpoint executing real matrix logic safely in the background."""
    payload = request.get_json() or {}
    data_input = payload.get("data", "").strip().upper()
    key_input = payload.get("key", "").strip().upper()

    if not data_input or not key_input:
        return jsonify({"success": False, "error": "Missing data or force key vector."}), 400

    try:
        start_time = time.perf_counter()

        # Convert standard characters to hex index integer values
        input_nodes = [int(char, 16) for char in data_input if char in "0123456789ABCDEF"]
        force_nodes = [int(char, 16) for char in key_input if char in "0123456789ABCDEF"]

        # Safeguard fallback values if conversion yields empty sets
        if not input_nodes: input_nodes = [0]
        if not force_nodes: force_nodes = [0]

        output_hex_chars = []
        telemetry_log = []

        # --- Extrapolate across all 8 tiers ---
        for idx in range(8):
            tier_id = idx + 1
            
            # Safely cycle back over the 4-character inputs using modulo (%)
            node_val = input_nodes[idx % len(input_nodes)]
            force_val = force_nodes[idx % len(force_nodes)]
            
            tier_meta = CYLINDER_TIERS.get(tier_id, {"binary": "0000", "val": 0, "name": "Undefined Axis"})
            
            # Mathematical Matrix Trajectory Calculation
            raw_trajectory = node_val + force_val + tier_meta["val"]
            
            # Enforce Clockwise Rotational Containment limit
            final_state = raw_trajectory % LIMIT
            
            if raw_trajectory >= LIMIT:
                rotation_type = f"Crossed boundary ({raw_trajectory}). Rotated CLOCKWISE to position {final_state}."
            else:
                rotation_type = "Trajectory maintained within local cylinder boundaries."
                
            out_char = hex(final_state)[2:].upper()
            output_hex_chars.append(out_char)
            
            # Package clean step logs for index.html interface list
            telemetry_log.append({
                "tier": tier_id,
                "tier_name": tier_meta["name"],
                "tier_binary": tier_meta["binary"],
                "formula": f"Input ({hex(node_val)[2:].upper()}) + Force Key ({hex(force_val)[2:].upper()}) + Tier Shift ({tier_meta['binary']}) = {raw_trajectory}",
                "boundary_enforcement": f"Gov[0.00] &rarr; {rotation_type}"
            })

        execution_delta = time.perf_counter() - start_time
        system_telemetry["processing_delta"] = execution_delta * 1000

        return jsonify({
            "success": True,
            "inventor": "Nicholas Desjardins",
            "output": "".join(output_hex_chars),
            "latency_ms": f"{system_telemetry['processing_delta']:.5f} ms",
            "telemetry": telemetry_log
        })
        
    except Exception as sys_err:
        return jsonify({"success": False, "error": f"Internal matrix failure: {str(sys_err)}"}), 500

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    """Feeds live background fluctuating 'Gov' numbers to the UI stream."""
    if system_telemetry["attack_active"]:
        system_telemetry["governor_apex"] = round(random.uniform(2.500, 3.999), 3)
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
