import time
import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Copyright (C) 2026 Nicholas Desjardins. All Rights Reserved.
# Proprietary and Confidential. Unauthorized copying or distribution is strictly prohibited.

# Sovereign application global telemetry and neural memory cache
system_telemetry = {
    "governor_apex": "AI_HYPERPLANE_ACTIVE",
    "system_status": "SECURE // COGNITIVE SHIELD ACTIVE",
    "attack_active": False,
    "intruder_tier": None,
    "target_trajectory": 0.0,
    "processing_delta": 2.17320,
    "incident_escrow_report": None,
    "ai_governance_matrix": {
        "model_confidence_score": "99.842%",
        "active_neural_layer": "Layer_64_Tensor",
        "decision_entropy": "0.0124",
        "regulatory_compliance_check": "PASSED // OSFI-COMPLIANT"
    }
}

def generate_threat_codename():
    return random.choice(["VECTOR-MK1R", "SPECTRE-B9BC", "LOTUS-OMEGA"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    return jsonify(system_telemetry)

@app.route('/api/simulate-attack', methods=['POST'])
def simulate_attack():
    data = request.json or {}
    attack_state = data.get("active", False)
    system_telemetry["attack_active"] = attack_state
    
    if attack_state:
        codename = generate_threat_codename()
        system_telemetry["system_status"] = "AI TRACE ALERT // MALICIOUS AGENT ISOLATED"
        system_telemetry["intruder_tier"] = random.randint(1, 4)
        system_telemetry["target_trajectory"] = round(random.uniform(0.0, 6.28), 3)
        
        system_telemetry["incident_escrow_report"] = {
            "allocated_codename": codename,
            "timestamp_epoch_ms": int(time.time() * 1000),
            "spatial_entry_tier": system_telemetry["intruder_tier"],
            "network_trajectory_vector": system_telemetry["target_trajectory"],
            "captured_telemetry": {
                "inbound_latency_ms": f"{system_telemetry['processing_delta']:.5f} ms",
                "simulated_device_fingerprint": "FDD90859E19633BF",
                "simulated_spatial_gps": "43.6532 N, 79.3832 W",
                "attacker_ip_address": "185.220.101.42"
            },
            "status": "ISOLATED_BY_AUTONOMOUS_NEURAL_SHIELD"
        }
        
        system_telemetry["ai_governance_matrix"] = {
            "model_confidence_score": "94.115%",
            "active_neural_layer": "ATTACK_ISOLATION_NODE_9",
            "decision_entropy": "0.4189 (HIGH THREAT ANOMALY)",
            "regulatory_compliance_check": "EMERGENCY BLOCK EXECUTION AUTO-LOGGED"
        }
    else:
        system_telemetry["system_status"] = "SECURE // COGNITIVE SHIELD ACTIVE"
        system_telemetry["intruder_tier"] = None
        system_telemetry["target_trajectory"] = 0.0
        system_telemetry["incident_escrow_report"] = None
        system_telemetry["ai_governance_matrix"] = {
            "model_confidence_score": "99.842%",
            "active_neural_layer": "Layer_64_Tensor",
            "decision_entropy": "0.0124",
            "regulatory_compliance_check": "PASSED // OSFI-COMPLIANT"
        }
        
    return jsonify({"status": "State Confirmed", "telemetry": system_telemetry})

@app.route('/api/terminal/execute', methods=['POST'])
def execute_terminal_command():
    data = request.json or {}
    raw_command = data.get("command", "").strip()
    
    # Explainable AI Logic Audit
    if raw_command == "ai --explain":
        gov = system_telemetry["ai_governance_matrix"]
        output_str = (
            f"=== EXPLAINABLE AI (XAI) DECISION AUDIT LOG ===\n"
            f"CURRENT MODEL CONFIDENCE : {gov['model_confidence_score']}\n"
            f"INTERACTING COGNITIVE LAYER: {gov['active_neural_layer']}\n"
            f"MATHEMATICAL ENTROPY RATIO: {gov['decision_entropy']}\n"
            f"AUDIT COMPLIANCE STANDARDS: {gov['regulatory_compliance_check']}\n"
            f"MECHANICS STATUS          : Human-in-the-Loop Override Pipeline clear."
        )
        return jsonify({"output": output_str})
    
    if raw_command == "ai --override":
        return jsonify({"output": "CRITICAL OVERRIDE SUCCESSFUL: AI model weights locked. System reverted back to baseline human governance rules."})
            
    # Direct Console Administrative Data Ingestion
    if raw_command.startswith("inject "):
        parts = raw_command.split()
        try:
            data_param = parts[parts.index("--data") + 1]
            key_param = parts[parts.index("--key") + 1]
            return jsonify({"output": f"SUCCESS: Enterprise data [{data_param}] successfully ingested via terminal command. Matrix recalculated."})
        except (ValueError, IndexError):
            return jsonify({"output": "ERROR: Invalid inject syntax. Use: inject --data [value] --key [value]"})

    # Infrastructure Environment Checks
    if raw_command == "uname -a":
        return jsonify({"output": "Linux srv-d89icdmq1p3s73fti7gg-hibernate-75768cfd9b-vq64z 6.8.0-1051-aws #54-Ubuntu SMP Wed Mar 18 23:51:09 UTC 2026 x86_64 GNU/Linux"})
    elif raw_command in ["ss -ant", "netstat"]:
        return jsonify({"output": "ESTAB      0      0      10.0.4.12:8080      185.220.101.42:49321\nLISTEN     0      128    0.0.0.0:8080        0.0.0.0:*" })
    elif raw_command == "clear":
        return jsonify({"output": "CLEAR_SCREEN"})
        
    return jsonify({"output": f"root@lotus-matrix:~# command not found: {raw_command}. Type 'ai --explain' or 'ss -ant'."})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
