from flask import Flask, render_template, jsonify, request
from core_engine import LotusCylinderEngine
import time

app = Flask(__name__)
spatial_engine = LotusCylinderEngine()

@app.route('/')
def load_interface():
    """Serves the front-end dashboard screen."""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def handle_api_request():
    """Secure API endpoint executing matrix logic safely in the background."""
    payload = request.get_json() or {}
    data_input = payload.get("data", "").strip()
    key_input = payload.get("key", "").strip()

    if not data_input or not key_input:
        return jsonify({"success": False, "error": "Missing data or force key vector."}), 400

    try:
        start_time = time.perf_counter()
        matrix_results = spatial_engine.process_clockwise_transform(data_input, key_input)
        execution_delta = time.perf_counter() - start_time

        return jsonify({
            "success": True,
            "inventor": "Nicholas Desjardins",
            "output": matrix_results["cipher_output"],
            "latency_ms": f"{execution_delta * 1000:.5f} ms",
            "telemetry": matrix_results["telemetry"]
        })
    except ValueError as val_err:
        return jsonify({"success": False, "error": str(val_err)}), 400
    except Exception as sys_err:
        return jsonify({"success": False, "error": f"Internal matrix failure: {str(sys_err)}"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
