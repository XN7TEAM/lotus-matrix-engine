import math
import time

# Use a fixed start time for the engine instance to ensure 
# consistent telemetry drift across all connected clients.
ENGINE_START_TIME = time.time()

def get_drift_offset():
    return (time.time() - ENGINE_START_TIME) * 0.1     
        
        # Astrometric Space Scale Threshold: 100,000 Light Years mapped to light-travel metric limits
        self.GALACTIC_SPACE_TIME_RADIUS = 3.154e13 
        
        # 8-Tier Structural System Matrix Layer Layout
        self.CYLINDER_TIERS = {
            1: {"binary": "0001", "val": 1, "name": "Alpha Base Axis (NORTH)"},
            2: {"binary": "0010", "val": 2, "name": "Beta Plane Layer (EAST)"},
            3: {"binary": "0100", "val": 4, "name": "Gamma Vector Ring (SOUTH)"},
            4: {"binary": "1000", "val": 8, "name": "Delta Polar Node (WEST)"},
            5: {"binary": "0011", "val": 3, "name": "Epsilon Cross Sync (N-E)"},
            6: {"binary": "0110", "val": 6, "name": "Zeta Lateral Shift (S-E)"},
            7: {"binary": "1100", "val": 12, "name": "Eta High Boundary (S-W)"},
            8: {"binary": "1111", "val": 15, "name": "Theta Apex Governor (N-W)"}
        }

    def process_clockwise_transform(self, data_stream: str, key_stream: str) -> dict:
        """Processes hex inputs sequentially through an active expanding spatial cylinder matrix layout."""
        clean_data = data_stream.upper().replace(" ", "")
        clean_key = key_stream.upper().replace(" ", "")
        
        if not all(c in "0123456789ABCDEF" for c in clean_data + clean_key):
            raise ValueError("Input vectors must contain valid hexadecimal syntax.")
            
        if len(clean_data) < 1 or len(clean_key) < 1:
            raise ValueError("Input data and force key tracks cannot be null.")
            
        input_nodes = [int(char, 16) for char in clean_data]
        force_nodes = [int(char, 16) for char in clean_key]
        
        output_hex_chars = []
        telemetry_log = []
        
        current_epoch_vector = time.time() % self.GALACTIC_SPACE_TIME_RADIUS

        for idx in range(8):
            tier_id = idx + 1
            tier_meta = self.CYLINDER_TIERS.get(tier_id, {"binary": "0000", "val": 0, "name": "Undefined Layer"})
            
            node_val = input_nodes[idx % len(input_nodes)]
            force_val = force_nodes[idx % len(force_nodes)]
            
            orbital_angle_rad = ((node_val + force_val) % self.LIMIT) * (math.pi / 8)
            calculated_clockwise_radius = 2.0 + (math.sin(current_epoch_vector + tier_id) * 0.05)
            
            raw_trajectory = node_val + force_val + tier_meta["val"]
            final_state = raw_trajectory % self.LIMIT
            
            if raw_trajectory >= self.LIMIT:
                rotation_type = f"Orbital layer boundary shift ({raw_trajectory}). Rotated CLOCKWISE to coordinate {final_state}."
            else:
                rotation_type = "Clockwise orbital trajectory maintained within spatial bounds."

            out_char = hex(final_state)[2:].upper()
            output_hex_chars.append(out_char)

            telemetry_log.append({
                "tier": tier_id,
                "tier_name": tier_meta["name"],
                "tier_binary": tier_meta["binary"],
                "formula": f"Input ({hex(node_val)[2:].upper()}) + Force [{tier_meta['binary']}] @ Radius: {calculated_clockwise_radius:.4f}",
                "boundary_enforcement": f"Galactic Time-Scale Anchor -> {rotation_type} -> Coordinate Out: {out_char}"
            })

        return {"cipher_output": "".join(output_hex_chars), "telemetry": telemetry_log}
