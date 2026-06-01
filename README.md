Lotus Matrix Engine
© 2026 Nicholas Desjardins. All Rights Reserved.

A real-time 3D cylindrical spatial matrix dashboard built for next-generation bank security visualization and cryptographic transformation demonstration.

Overview
The Lotus Matrix Engine processes hexadecimal data streams through an 8-tier cylindrical spatial coordinate system, applying clockwise boundary enforcement and galactic-scale time anchoring. The result is rendered live in a Three.js 3D viewport alongside per-tier telemetry.

Live demo: lotus-matrix-engine.onrender.com

Stack
Layer	Technology
Backend	Python 3 / Flask
3D Engine	Three.js r128
Server	Gunicorn
Hosting	Render
Project Structure
lotus-matrix/
├── app.py              # Flask application + API routes
├── core_engine.py      # Cylinder transform engine
├── requirements.txt    # Python dependencies
├── Procfile            # Gunicorn process declaration
├── templates/
│   └── index.html      # Dashboard frontend
└── static/
    └── css/
        └── style.css   # Supplementary styles
API Endpoints
POST /api/handshake
Verifies spatiotemporal alignment and issues a session token.

Request:

{ "alignment_state": 1.047 }
Response:

{ "authenticated": true, "token": "<hex-token>", "message": "..." }
POST /api/process (auth required)
Runs the cylinder transformation.

Request:

{ "data": "ABC1", "key": "3576" }
Response:

{
  "success": true,
  "output": "D9E2F1A3",
  "latency_ms": "0.02341 ms",
  "telemetry": [ ... ]
}
GET /api/telemetry (auth required)
Returns live system state (governor apex, status, threat data).

POST /api/simulate-attack (auth required)
Toggles the threat simulation for demo/presentation mode.

Request:

{ "active": true }
Authentication
All protected endpoints require:

Authorization: Bearer <token>
Tokens are issued by /api/handshake and stored server-side for the duration of the process lifetime.

Local Development
# 1. Clone the repo
git clone https://github.com/your-username/lotus-matrix-engine.git
cd lotus-matrix-engine

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run locally
python app.py
# → http://127.0.0.1:5000
Deploy to Render
Push this repository to GitHub.
In Render, create a new Web Service.
Connect your GitHub repo.
Set:
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Deploy — Render will auto-detect the Procfile.
Security Notes
The /api/terminal/execute shell execution endpoint from v1 has been removed. It exposed arbitrary OS command execution and is incompatible with production security requirements.
The diagnostic terminal in the UI now runs entirely client-side with a fixed set of safe read-only commands.
All API inputs are validated and length-limited before processing.
Session tokens are cryptographically random 64-character hex strings (secrets.token_hex(32)).
Core Engine — How It Works
The LotusCylinderEngine.process_clockwise_transform() method:

Converts each hex character to an integer (0–15).
Iterates over 8 cylindrical tiers, each with a named cardinal weight.
For each tier: raw = node_val + force_val + tier_weight
Applies modulo-16 clockwise boundary enforcement: final = raw % 16
Computes a radial position using a galactic epoch offset (real-time sinusoidal drift).
Returns the 8-character cipher output and full per-tier telemetry log.
Proprietary Engine Pipeline — System Gate: Active Dashboard Stream
