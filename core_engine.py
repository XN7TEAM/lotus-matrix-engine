import math
import time

# Module-level epoch anchor
# Fixed at import time so every client sees the same drift curve.
ENGINE_START_TIME: float = time.time()

def get_drift_offset() -> float:
    """
    Returns a slowly increasing float (0.1 units per second) based on
    elapsed time since the engine was loaded. Used to produce a smooth,
    shared radial drift across all active dashboard sessions.
    """
    return (time.time() - ENGINE_START_TIME) * 0.1

class LotusCylinderEngine:
    """
    Processes hex input streams through an eight-tier cylindrical
    spatial matrix. Each tier applies a named orbital-plane offset,
    a radial position derived from galactic-scale time, and enforces
    clockwise boundary wrapping within [0, 15].
    """
    # Maximum hex coordinate value (4-bit ceiling)
    LIMIT: int = 16

    # Astrometric scale: 100,000 light-years in seconds (light-travel metric)
    GALACTIC_SPACE_TIME_RADIUS: float = 3.154e13

    # Eight structural tiers: binary weight, cardinal value, and display name
    CYLINDER_TIERS: dict = {
        1: {"binary": "0001", "val": 1, "name": "Alpha Base Axis (NORTH)"},
        2: {"binary": "0010", "val": 2, "name": "Beta Plane Layer (EAST)"},
        3: {"binary": "0100", "val": 4, "name": "Gamma Vector Ring (SOUTH)"},
        4: {"binary": "1000", "val": 8, "name": "Delta Polar Node (WEST)"},
        5: {"binary": "0011", "val": 3, "name": "Epsilon Cross Sync (N-E)"},
        6: {"binary": "0110", "val": 6, "name": "Zeta Lateral Shift (S-E)"},
        7: {"binary": "1100", "val": 12, "name": "Eta High Boundary (S-W)"},
        8: {"binary": "1111", "val": 15, "name": "Theta Apex Governor (N-W)"},
    }

    def process_clockwise_transform(self, data_stream: str, key_stream: str) -> dict:
        """
        Transforms hex data through the 8-tier cylinder matrix.
        """
        clean_data = data_stream.upper().replace(" ", "")
        clean_key = key_stream.upper().replace(" ", "")

        if len(clean_data) < 1 or len(clean_key) < 1:
            raise ValueError("Input data and force key tracks cannot be null.")

        if not all(c in "0123456789ABCDEF" for c in clean_data + clean_key):
            raise ValueError("Input vectors must contain valid hexadecimal syntax.")

        input_nodes = [int(c, 16) for c in clean_data]
        force_nodes = [int(c, 16) for c in clean_key]

        output_hex_chars = []
        telemetry_log = []

        # Use the shared drift offset so all clients see the same radial curve.
        # The modulo keeps the value within the galactic radius scale.
        current_epoch_vector = (ENGINE_START_TIME + get_drift_offset()) % self.GALACTIC_SPACE_TIME_RADIUS

        for idx in range(8):
            tier_id = idx + 1
            tier_meta = self.CYLINDER_TIERS.get(
                tier_id,
                {"binary": "0000", "val": 0, "name": "Undefined Layer"}
            )

            node_val = input_nodes[idx % len(input_nodes)]
            force_val = force_nodes[idx % len(force_nodes)]

            # Orbital angle: maps combined value (0-15) onto 0 to 2π in 16 steps
            orbital_angle_rad = ((node_val + force_val) % self.LIMIT) * (math.pi / 8)

            # Radial position: base 2.0 with small sinusoidal drift from epoch
            calculated_clockwise_radius = 2.0 + (math.sin(current_epoch_vector + tier_id) * 0.05)

            # Raw trajectory: node + force + tier cardinal weight
            raw_trajectory = node_val + force_val + tier_meta["val"]
            final_state = raw_trajectory % self.LIMIT

            if raw_trajectory >= self.LIMIT:
                rotation_type = (
                    f"Orbital layer boundary shift ({raw_trajectory}). "
                    f"Rotated CLOCKWISE to coordinate {final_state}."
                )
            else:
                rotation_type = "Clockwise orbital trajectory maintained within spatial bounds."

            out_char = hex(final_state)[2:].upper()
            output_hex_chars.append(out_char)

            telemetry_log.append({
                "tier": tier_id,
                "tier_name": tier_meta["name"],
                "tier_binary": tier_meta["binary"],
                "formula": (
                    f"Input ({hex(node_val)[2:].upper()}) "
                    f"+ Force [{tier_meta['binary']}] "
                    f"@ Radius: {calculated_clockwise_radius:.4f}"
                ),
                "boundary_enforcement": (
                    f"Galactic Time-Scale Anchor -> {rotation_type} "
                    f"-> Coordinate Out: {out_char}"
                ),
            })

        return {
            "cipher_output": "".join(output_hex_chars),
            "telemetry": telemetry_log,
        }
