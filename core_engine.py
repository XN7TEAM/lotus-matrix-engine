import math
import time

class LotusCylinderEngine:
    """
    Lotus Cylinder Engine — Core Transform Module
    Implements the clockwise cylindrical spatial matrix transformation.
    """
    
    LIMIT: int = 16  # 4-bit coordinate space
    ENGINE_START_TIME: float = time.time()
    GALACTIC_SPACE_TIME_RADIUS: float = 3.154e13
    
    # Restored 8-tier structural map
    CYLINDER_TIERS: dict = {
        1: {"binary": "0001", "val": 1,  "name": "Alpha Base Axis (NORTH)"},
        2: {"binary": "0010", "val": 2,  "name": "Beta Plane Layer (EAST)"},
        3: {"binary": "0100", "val": 4,  "name": "Gamma Vector Ring (SOUTH)"},
        4: {"binary": "1000", "val": 8,  "name": "Delta Polar Node (WEST)"},
        5: {"binary": "0011", "val": 3,  "name": "Epsilon Cross Sync (N-E)"},
        6: {"binary": "0110", "val": 6,  "name": "Zeta Lateral Shift (S-E)"},
        7: {"binary": "1100", "val": 12, "name": "Eta High Boundary (S-W)"},
        8: {"binary": "1111", "val": 15, "name": "Theta Apex Governor (N-W)"},
    }

    def get_drift_offset(self) -> float:
        """Calculates drift based on engine load time for vortex synchronization."""
        return (time.time() - self.ENGINE_START_TIME) * 0.1

    def process_transform(self, input_nodes: list, force_nodes: list):
        """
        Processes hex input streams through the 8-tier cylindrical matrix.
        Returns a hex string and a full telemetry log for the dashboard.
        """
        output_hex_chars = []
        telemetry_log = []
        
        # Use drift offset for synchronized motion
        current_epoch_vector = (self.ENGINE_START_TIME + self.get_drift_offset()) % self.GALACTIC_SPACE_TIME_RADIUS

        for idx in range(8):
            tier_id = idx + 1
            tier_meta = self.CYLINDER_TIERS.get(tier_id, {"binary": "0000", "val": 0, "name": "Undefined Layer"})
            
            node_val = input_nodes[idx % len(input_nodes)]
            force_val = force_nodes[idx % len(force_nodes)]

            # Radial calculation for kinetic motion
            radius = 2.0 + (math.sin(current_epoch_vector + tier_id) * 0.05)

            # Raw trajectory calculation
            raw_trajectory = node_val + force_val + tier_meta["val"]
            final_state = raw_trajectory % self.LIMIT

            # Rotation state tracking
            if raw_trajectory >= self.LIMIT:
                rotation_type = f"Orbital layer boundary shift ({raw_trajectory}). Rotated CLOCKWISE to {final_state}."
            else:
                rotation_type = "Clockwise orbital trajectory maintained within spatial bounds."

            out_char = hex(final_state)[2:].upper()
            output_hex_chars.append(out_char)

            # Append to telemetry log for frontend "Binary Box" display
            telemetry_log.append({
                "tier": tier_id,
                "tier_name": tier_meta["name"],
                "tier_binary": tier_meta["binary"],
                "trajectory": final_state,
                "rotation_status": rotation_type,
                "radius_vector": round(radius, 4)
            })

        return "".join(output_hex_chars), telemetry_log
        
