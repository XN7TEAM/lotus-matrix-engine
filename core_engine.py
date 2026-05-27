import time

class LotusCylinderEngine:
    def __init__(self):
        self.LIMIT = 16
        self.GOVERNOR_POLE_START = 0  
        self.ANCHOR_POLE_END = 1      
        
        # Symmetrical 8-tier structural sync configuration
        self.CYLINDER_TIERS = {
            1: {"binary": "0001", "val": 1, "name": "Alpha Base Axis"},
            2: {"binary": "0010", "val": 2, "name": "Beta Plane Layer"},
            3: {"binary": "0100", "val": 4, "name": "Gamma Vector Ring"},
            4: {"binary": "1000", "val": 8, "name": "Delta Polar Node"},
            5: {"binary": "0011", "val": 3, "name": "Epsilon Cross Sync"},
            6: {"binary": "0110", "val": 6, "name": "Zeta Lateral Shift"},
            7: {"binary": "1100", "val": 12, "name": "Eta High Boundary"},
            8: {"binary": "1111", "val": 15, "name": "Theta Apex Governor"}
        }

    def process_clockwise_transform(self, data_stream: str, key_stream: str) -> dict:
        """Processes hexadecimal blocks down the 8-tier matrix cylinder topology."""
        clean_data = data_stream.upper().replace(" ", "")
        clean_key = key_stream.upper().replace(" ", "")
        
        if not all(c in "0123456789ABCDEF" for c in clean_data + clean_key):
            raise ValueError("Input data must contain valid hexadecimal blocks.")
            
        if len(clean_data) < 1 or len(clean_key) < 1:
            raise ValueError("Data stream and force key vectors cannot be empty.")
            
        input_nodes = [int(char, 16) for char in clean_data]
        force_nodes = [int(char, 16) for char in clean_key]
        
        output_hex_chars = []
        telemetry_log = []

        for idx in range(8):
            tier_id = idx + 1
            tier_meta = self.CYLINDER_TIERS.get(tier_id, {"binary": "0000", "val": 0, "name": "Undefined Axis"})
            
            node_val = input_nodes[idx % len(input_nodes)]
            force_val = force_nodes[idx % len(force_nodes)]
            
            # Mathematical Matrix Trajectory Calculation
            raw_trajectory = node_val + force_val + tier_meta["val"]
            final_state = raw_trajectory % self.LIMIT
            
            if raw_trajectory >= self.LIMIT:
                rotation_type = f"Crossed boundary ({raw_trajectory}). Rotated CLOCKWISE to position {final_state}."
            else:
                rotation_type = "Trajectory maintained within local cylinder boundaries."

            out_char = hex(final_state)[2:].upper()
            output_hex_chars.append(out_char)

            telemetry_log.append({
                "tier": tier_id,
                "tier_name": tier_meta["name"],
                "tier_binary": tier_meta["binary"],
                "formula": f"Input ({hex(node_val)[2:].upper()}) + Force Key ({hex(force_val)[2:].upper()}) + Tier Shift ({tier_meta['binary']}) = {raw_trajectory}",
                "boundary_enforcement": f"Gov[{self.GOVERNOR_POLE_START}] &rarr; {rotation_type} &rarr; Anchor[{self.ANCHOR_POLE_END}] &rarr; Out: Hex {out_char}"
            })

        return {"cipher_output": "".join(output_hex_chars), "telemetry": telemetry_log}
