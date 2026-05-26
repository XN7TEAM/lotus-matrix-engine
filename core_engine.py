class LotusCylinderEngine:
    def __init__(self):
        self.LIMIT = 16
        self.GOVERNOR_POLE_START = 0  # Top absolute boundary (0)
        self.ANCHOR_POLE_END = 1      # Bottom absolute boundary (1)
        
        # Mapping your exact 8-tier binary stacking sequence from your schematics
        self.CYLINDER_TIERS = {
            1: {"binary": "0000", "val": 0b0000, "name": "Tier 1: Entry Plane (0000)"},
            2: {"binary": "0001", "val": 0b0001, "name": "Tier 2: Upper Transition (0001)"},
            3: {"binary": "0010", "val": 0b0010, "name": "Tier 3: Junction Delta (0010)"},
            4: {"binary": "0011", "val": 0b0011, "name": "Tier 4: Center Core Loop (0011)"},
            5: {"binary": "0100", "val": 0b0100, "name": "Tier 5: Lower Core Loop (0100)"},
            6: {"binary": "0101", "val": 0b0101, "name": "Tier 6: Exit Junction (0101)"},
            7: {"binary": "0110", "val": 0b0110, "name": "Tier 7: Base Transition (0110)"},
            8: {"binary": "0111", "val": 0b0111, "name": "Tier 8: Terminal Gate (0111)"}
        }

    def process_clockwise_transform(self, data_stream: str, key_stream: str) -> dict:
        """Processes hexadecimal vectors by spinning them clockwise down the infinite boundaries."""
        clean_data = data_stream.upper().replace(" ", "")
        clean_key = key_stream.upper().replace(" ", "")
        
        # Symmetrical character block handling logic
        if len(clean_data) not in [4, 8] or len(clean_key) != len(clean_data):
            raise ValueError("Lattice blocks require symmetrical 4 or 8 hexadecimal characters.")
            
        input_nodes = [int(char, 16) for char in clean_data]
        force_nodes = [int(char, 16) for char in clean_key]
        
        output_hex_chars = []
        telemetry_log = []

        # --- FIX: Explicitly loop through all 8 structural sync tiers ---
        for idx in range(8):
            tier_id = idx + 1
            tier_meta = self.CYLINDER_TIERS.get(tier_id, {"binary": "0000", "val": 0, "name": "Undefined Axis"})
            
            # Safely loop back around the input nodes/keys if they are only 4 characters long
            node_val = input_nodes[idx % len(input_nodes)]
            force_val = force_nodes[idx % len(force_nodes)]
            
            # Mathematical Trajectory: Input Vector + Key Force Vector + Tier Level Constant
            raw_trajectory = node_val + force_val + tier_meta["val"]
            
            # Enforce Clockwise Rotational Containment
            final_state = raw_trajectory % self.LIMIT
            
            if raw_trajectory >= self.LIMIT:
                rotation_type = f"Crossed boundary ({raw_trajectory}). Rotated CLOCKWISE to position {final_state}."
            else:
                rotation_type = "Trajectory maintained within local cylinder boundaries."

            out_char = hex(final_state)[2:].upper()
            output_hex_chars.append(out_char)

            # Package data steps to pass to the front-end securely
            telemetry_log.append({
                "tier": tier_id,
                "tier_name": tier_meta["name"],
                "tier_binary": tier_meta["binary"],
                "formula": f"Input ({hex(node_val)[2:].upper()}) + Force Key ({hex(force_val)[2:].upper()}) + Tier Shift ({tier_meta['binary']}) = {raw_trajectory}",
                "boundary_enforcement": f"Gov[{self.GOVERNOR_POLE_START}] &rarr; {rotation_type} &rarr; Anchor[{self.ANCHOR_POLE_END}] &rarr; Out: Hex {out_char}"
            })

        return {"cipher_output": "".join(output_hex_chars), "telemetry": telemetry_log}
