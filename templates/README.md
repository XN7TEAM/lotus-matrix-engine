# Lotus Matrix Engine
### Proprietary 3D Cylindrical Spatial Matrix Transformation Engine for Enterprise Security Visualization
**© 2026 Nicholas Desjardins. All Rights Reserved.**

🔗 **Live Demo:** [lotus-matrix-engine.onrender.com](https://lotus-matrix-engine.onrender.com)
📁 **Repository:** [github.com/your-username/lotus-matrix-engine](https://github.com/your-username/lotus-matrix-engine)

---

## Executive Summary

The Lotus Matrix Engine is a full-stack security visualization platform that solves the problem of high-velocity, fragmented telemetry data in enterprise security operations. By applying a proprietary **8-tier cylindrical transformation matrix**, the engine maps incoming hexadecimal data streams into a consistent, real-time 3D coordinate space — giving security teams immediate spatial awareness of lateral movement, data state drift, and threat trajectories.

Where traditional SIEM dashboards present raw log data as flat tables, the Lotus Matrix Engine transforms abstract hex streams into a navigable 3D environment that makes anomaly detection instinctive and rapid.

**Current State:** Functional prototype deployed on Render. Live demo available.

---

## The Problem It Solves

Enterprise security teams face:
- **Signal overload:** Raw log and telemetry data is too fragmented to interpret at speed
- **Invisible lateral movement:** Traditional dashboards don't represent spatial relationships between data nodes
- **Slow incident response:** Flat data views require manual correlation before action can be taken

The Lotus Matrix Engine provides a **single spatial view** of system state, so anomalies appear as visual deviations rather than buried log entries.

---

## Core Concepts

### The 8-Tier Cylindrical Coordinate System
Data is not processed linearly. Instead, each input is run through **8 structural tiers** (Alpha → Theta), each assigned a named cardinal weight. This creates a multi-dimensional state fingerprint for every data packet processed.

| Tier | Role |
|------|------|
| Alpha | Primary node anchor |
| Beta – Eta | Cardinal drift layers |
| Theta | Final boundary lock |

### Clockwise Boundary Enforcement
Each tier applies a **modulo-16 clockwise wrap**: `final = (node_val + force_val + tier_weight) % 16`. This keeps all values within a deterministic 4-bit hex coordinate space, ensuring reproducible transforms across distributed sessions.

### Galactic Time-Scale Anchoring
A fixed `ENGINE_START_TIME` generates a **sinusoidal radial drift** offset per tier. This means each session's coordinate map drifts predictably over time — enabling detection of state changes that would be invisible in a static snapshot.

### Session Tokens
All sessions are gated by a spatiotemporal handshake: clients must submit a **1.047 RAD alignment value** to mint a cryptographically random 64-character hex token (`secrets.token_hex(32)`). No protected endpoint is accessible without it.

---

## Architecture

```
lotus-matrix/
├── app.py              # Flask application + API routes
├── core_engine.py      # Proprietary cylinder transform engine
├── requirements.txt    # Python dependencies
├── Procfile            # Gunicorn process declaration
├── templates/
│   └── index.html      # 3D dashboard frontend
└── static/
    └── css/
        └── style.css   # Supplementary styles
```

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 / Flask |
| 3D Visualization | Three.js r128 |
| Server | Gunicorn |
| Hosting | Render |

---

## API Reference

### `POST /api/handshake`
Verifies spatiotemporal alignment and issues a session token.

**Request:**
```json
{ "alignment_state": 1.047 }
```
**Response:**
```json
{ "authenticated": true, "token": "<64-char hex>", "message": "..." }
```

---

### `POST /api/process` *(auth required)*
Runs the full 8-tier cylinder transformation.

**Request:**
```json
{ "data": "ABC1", "key": "3576" }
```
**Response:**
```json
{
  "success": true,
  "output": "D9E2F1A3",
  "latency_ms": "0.02341 ms",
  "telemetry": [ ...per-tier state objects... ]
}
```

---

### `GET /api/telemetry` *(auth required)*
Returns live system state: governor apex, operational status, threat indicators.

---

### `POST /api/simulate-attack` *(auth required)*
Toggles threat simulation mode for demo and red-team exercises.

**Request:**
```json
{ "active": true }
```

---

### Authentication
All protected endpoints require:
```
Authorization: Bearer <token>
```
Tokens are issued by `/api/handshake` and stored server-side for the lifetime of the process. All inputs are validated and length-limited before processing.

---

## Dashboard Interface

The frontend is built for enterprise SOC environments:

- **3D Spatial Gateway** — Three.js-powered 360° spatial view of the matrix transformation in real time
- **Live Governance Terminal** — Draggable, resizable diagnostic shell with real-time telemetry readout
- **Threat Isolation Controls** — Toggle attack simulation and observe defensive response patterns
- **Print-Ready Forensic Reports** — CSS print styling strips interactive chrome for clean incident documentation

---

## Core Engine: How the Transform Works

`LotusCylinderEngine.process_clockwise_transform()`:

1. Converts each hex character to an integer (0–15)
2. Iterates over 8 cylindrical tiers, each with a named cardinal weight
3. Per tier: `raw = node_val + force_val + tier_weight`
4. Applies modulo-16 clockwise boundary: `final = raw % 16`
5. Computes a radial position using galactic epoch sinusoidal drift
6. Returns an 8-character cipher output + full per-tier telemetry log

---

## Local Development

**1. Clone**
```bash
git clone https://github.com/your-username/lotus-matrix-engine.git
cd lotus-matrix-engine
```

**2. Virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run**
```bash
python app.py
# → http://127.0.0.1:5000
```

---

## Deploy to Render

1. Push repository to GitHub
2. In Render, create a new **Web Service**
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Deploy — Render auto-detects the Procfile

---

## Security Notes

- The `/api/terminal/execute` shell execution endpoint from v1 has been **permanently removed** — it exposed arbitrary OS command execution incompatible with production requirements
- The diagnostic terminal in the UI runs **entirely client-side** with a fixed set of safe, read-only commands
- All API inputs are **validated and length-limited** before processing
- Session tokens are **cryptographically random 64-character hex strings** (`secrets.token_hex(32)`)

---

## Current Limitations / Prototype Status

- Session tokens are in-memory only (process restart clears all active sessions)
- Threat simulation is a toggle-based demo layer, not a live feed integration
- The 8-tier transform is currently optimized for hex-encoded inputs; arbitrary binary stream support is on the roadmap

---

## Roadmap

- [ ] Persistent session store (Redis or DB-backed)
- [ ] Streaming WebSocket telemetry feed
- [ ] Multi-user SOC collaboration layer
- [ ] Integration adapters for SIEM platforms (Splunk, Elastic)
- [ ] Exportable forensic report format (PDF/JSON)

---

*Lotus Matrix Engine © 2026 Nicholas Desjardins. All Rights Reserved.*
