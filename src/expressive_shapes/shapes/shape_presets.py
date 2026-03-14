from ..geometry.corner_rounding import CornerRounding

# --- PRESET STYLES ---
SHARP = CornerRounding(radius=0.0, smoothing=0.0)
SOFT = CornerRounding(radius=0.2, smoothing=0.8)
DEEP = CornerRounding(radius=0.2, smoothing=0.0)
SMOOTH = CornerRounding(radius=0.2, smoothing=0.8)
VALLEY = CornerRounding(radius=0.2, smoothing=1.0)
SMALL_ROUND = CornerRounding(radius=0.10, smoothing=0.0)
ROUND = CornerRounding(radius=0.20, smoothing=0.0)
SEMI_MEDIUM_ROUND = CornerRounding(radius=0.3, smoothing=0.0)
MEDIUM_ROUND = CornerRounding(radius=0.4, smoothing=0.0)
LARGE_ROUND = CornerRounding(radius=0.6, smoothing=0.0)
FULL_ROUND = CornerRounding(radius=1.00, smoothing=0.0)

SEMI_MEDIUM_ROUND_SMOOTH = CornerRounding(radius=0.3, smoothing=1.0)
FULL_ROUND_SMOOTH = CornerRounding(radius=1.00, smoothing=1.0)

circle = [
    ((0.10, 0.10), FULL_ROUND),
    ((0.90, 0.10), FULL_ROUND),
    ((0.90, 0.90), FULL_ROUND),
    ((0.10, 0.90), FULL_ROUND),
]
square = [
    ((0.10, 0.10), ROUND),
    ((0.90, 0.10), ROUND),
    ((0.90, 0.90), ROUND),
    ((0.10, 0.90), ROUND),
]
slanted = [
    ((0.15, 0.10), ROUND),
    ((0.95, 0.10), ROUND),
    ((0.85, 0.90), ROUND),
    ((0.05, 0.90), ROUND),
]

arch = [
    ((0.10, 0.10), FULL_ROUND),
    ((0.90, 0.10), FULL_ROUND),
    # ((0.90, 0.50), SHARP),
    ((0.90, 0.90), SMALL_ROUND),
    ((0.10, 0.90), SMALL_ROUND),
    # ((0.10, 0.50), SHARP),
]

semicircle = [
    ((0.90, 0.70), SMALL_ROUND),
    ((0.10, 0.70), SMALL_ROUND),
    ((0.10, 0.25), LARGE_ROUND),
    ((0.90, 0.25), LARGE_ROUND),
]

oval = [
    ((0.15, 0.15), FULL_ROUND_SMOOTH),
    ((0.90, 0.10), SEMI_MEDIUM_ROUND_SMOOTH),
    ((0.85, 0.85), FULL_ROUND_SMOOTH),
    ((0.10, 0.90), SEMI_MEDIUM_ROUND_SMOOTH),
]

pill = [
    ((0.00, 0.55), MEDIUM_ROUND),
    ((0.55, 0.00), MEDIUM_ROUND),
    ((1.00, 0.45), MEDIUM_ROUND),
    ((0.45, 1.00), MEDIUM_ROUND),
]

triangle = [
    ((0.425, 0.15), ROUND), # center
    ((0.575, 0.15), ROUND),
    ((0.90, 0.75), ROUND), # right
    ((0.80, 0.85), ROUND),
    ((0.20, 0.85), ROUND), # left
    ((0.10, 0.75), ROUND),
]

arrow = [
    ((0.50, 0.80), VALLEY), # inward curve
    ((0.25, 0.90), ROUND), # left
    ((0.10, 0.75), ROUND),
    ((0.40, 0.15), ROUND), # center top
    ((0.60, 0.15), ROUND),
    ((0.90, 0.75), ROUND), # right
    ((0.75, 0.90), ROUND),
]

fan = [
    ((0.90, 0.90), ROUND),
    ((0.10, 0.90), ROUND),
    ((0.10, 0.10), ROUND),
    # TODO: fix proper clamping when radius exceeds available space
    ((0.90, 0.10), LARGE_ROUND),
]

DIAMOND_ROUNDING = CornerRounding(radius=0.15)
diamond = [
    ((0.50, 0.00), DIAMOND_ROUNDING),
    ((0.85, 0.50), DIAMOND_ROUNDING),
    ((0.50, 1.00), DIAMOND_ROUNDING),
    ((0.15, 0.50), DIAMOND_ROUNDING),
]

clamshell = [
    ((0.20, 0.20), SMALL_ROUND),
    ((0.80, 0.20), SMALL_ROUND),
    ((1.00, 0.50), SMALL_ROUND),
    ((0.80, 0.80), SMALL_ROUND),
    ((0.20, 0.80), SMALL_ROUND),
    ((0.00, 0.50), SMALL_ROUND),
]

PENTAGON_ROUNDING = CornerRounding(radius=0.12)
pentagon = [
    ((0.50, 0.100), PENTAGON_ROUNDING),
    ((0.92, 0.400), PENTAGON_ROUNDING),
    ((0.75, 0.875), PENTAGON_ROUNDING),
    ((0.25, 0.875), PENTAGON_ROUNDING),
    ((0.08, 0.400), PENTAGON_ROUNDING),
]

GEM_ROUND = CornerRounding(radius=0.12, smoothing=0.0)
gem = [
    ((0.50, 0.10), GEM_ROUND),
    ((0.815, 0.30), GEM_ROUND),
    ((0.875, 0.715), GEM_ROUND),
    ((0.50, 0.90), GEM_ROUND),
    ((0.125, 0.715), GEM_ROUND),
    ((0.185, 0.30), GEM_ROUND),
]

very_sunny = [
    ((0.500, 0.050), CornerRounding(radius=0.075)),  # Peak 1 (0°)
    ((0.622, 0.204), CornerRounding(radius=0.075)),  # Cave-in (22.5°)
    ((0.818, 0.182), CornerRounding(radius=0.075)),  # Peak 2 (45°)
    ((0.796, 0.378), CornerRounding(radius=0.075)),  # Cave-in (67.5°)
    ((0.950, 0.500), CornerRounding(radius=0.075)),  # Peak 3 (90°)
    ((0.796, 0.622), CornerRounding(radius=0.075)),  # Cave-in (112.5°)
    ((0.818, 0.818), CornerRounding(radius=0.075)),  # Peak 4 (135°)
    ((0.622, 0.796), CornerRounding(radius=0.075)),  # Cave-in (157.5°)
    ((0.500, 0.950), CornerRounding(radius=0.075)),  # Peak 5 (180°)
    ((0.378, 0.796), CornerRounding(radius=0.075)),  # Cave-in (202.5°)
    ((0.182, 0.818), CornerRounding(radius=0.075)),  # Peak 6 (225°)
    ((0.204, 0.622), CornerRounding(radius=0.075)),  # Cave-in (247.5°)
    ((0.050, 0.500), CornerRounding(radius=0.075)),  # Peak 7 (270°)
    ((0.204, 0.378), CornerRounding(radius=0.075)),  # Cave-in (292.5°)
    ((0.182, 0.182), CornerRounding(radius=0.075)),  # Peak 8 (315°)
    ((0.378, 0.204), CornerRounding(radius=0.075)),  # Cave-in (337.5°)
]

sunny = [
    ((0.500, 0.050), CornerRounding(radius=0.05)),  # Peak 1 (0°)
    ((0.640, 0.160), CornerRounding(radius=0.05)),  # Cave-in (22.5°) - Slightly Out
    ((0.818, 0.182), CornerRounding(radius=0.05)),  # Peak 2 (45°)
    ((0.840, 0.360), CornerRounding(radius=0.05)),  # Cave-in (67.5°) - Slightly Out
    ((0.950, 0.500), CornerRounding(radius=0.05)),  # Peak 3 (90°)
    ((0.840, 0.640), CornerRounding(radius=0.05)),  # Cave-in (112.5°) - Slightly Out
    ((0.818, 0.818), CornerRounding(radius=0.05)),  # Peak 4 (135°)
    ((0.640, 0.840), CornerRounding(radius=0.05)),  # Cave-in (157.5°) - Slightly Out
    ((0.500, 0.950), CornerRounding(radius=0.05)),  # Peak 5 (180°)
    ((0.360, 0.840), CornerRounding(radius=0.05)),  # Cave-in (202.5°) - Slightly Out
    ((0.182, 0.818), CornerRounding(radius=0.05)),  # Peak 6 (225°)
    ((0.160, 0.640), CornerRounding(radius=0.05)),  # Cave-in (247.5°) - Slightly Out
    ((0.050, 0.500), CornerRounding(radius=0.05)),  # Peak 7 (270°)
    ((0.160, 0.360), CornerRounding(radius=0.05)),  # Cave-in (292.5°) - Slightly Out
    ((0.182, 0.182), CornerRounding(radius=0.05)),  # Peak 8 (315°)
    ((0.360, 0.160), CornerRounding(radius=0.05)),  # Cave-in (337.5°) - Slightly Out
]


cookie_4 = [
    ((0.50, 0.20), ROUND), # cave-in
    ((0.70, 0.10), ROUND),
    ((0.90, 0.30), ROUND),
    ((0.80, 0.50), ROUND), # cave-in
    ((0.90, 0.70), ROUND),
    ((0.70, 0.90), ROUND),
    ((0.50, 0.80), ROUND), # cave-in
    ((0.30, 0.90), ROUND),
    ((0.10, 0.70), ROUND),
    ((0.20, 0.50), ROUND), # cave-in
    ((0.10, 0.30), ROUND),
    ((0.30, 0.10), ROUND),
]

cookie_8 = [
    ((0.500, 0.050), SMOOTH),  # Peak 1 (0°)
    ((0.622, 0.204), VALLEY),  # Cave-in (22.5°)
    ((0.818, 0.182), SMOOTH),  # Peak 2 (45°)
    ((0.796, 0.378), VALLEY),  # Cave-in (67.5°)
    ((0.950, 0.500), SMOOTH),  # Peak 3 (90°)
    ((0.796, 0.622), VALLEY),  # Cave-in (112.5°)
    ((0.818, 0.818), SMOOTH),  # Peak 4 (135°)
    ((0.622, 0.796), VALLEY),  # Cave-in (157.5°)
    ((0.500, 0.950), SMOOTH),  # Peak 5 (180°)
    ((0.378, 0.796), VALLEY),  # Cave-in (202.5°)
    ((0.182, 0.818), SMOOTH),  # Peak 6 (225°)
    ((0.204, 0.622), VALLEY),  # Cave-in (247.5°)
    ((0.050, 0.500), SMOOTH),  # Peak 7 (270°)
    ((0.204, 0.378), VALLEY),  # Cave-in (292.5°)
    ((0.182, 0.182), SMOOTH),  # Peak 8 (315°)
    ((0.378, 0.204), VALLEY),  # Cave-in (337.5°)
]

cookie_12 = [
    ((0.500, 0.050), SMOOTH),  # 0° Peak
    ((0.593, 0.152), VALLEY),  # 15° Valley
    ((0.725, 0.110), SMOOTH),  # 30° Peak
    ((0.755, 0.245), VALLEY),  # 45° Valley
    ((0.890, 0.275), SMOOTH),  # 60° Peak
    ((0.848, 0.407), VALLEY),  # 75° Valley
    ((0.950, 0.500), SMOOTH),  # 90° Peak
    ((0.848, 0.593), VALLEY),  # 105° Valley
    ((0.890, 0.725), SMOOTH),  # 120° Peak
    ((0.755, 0.755), VALLEY),  # 135° Valley
    ((0.725, 0.890), SMOOTH),  # 150° Peak
    ((0.593, 0.848), VALLEY),  # 165° Valley
    ((0.500, 0.950), SMOOTH),  # 180° Peak
    ((0.407, 0.848), VALLEY),  # 195° Valley
    ((0.275, 0.890), SMOOTH),  # 210° Peak
    ((0.245, 0.755), VALLEY),  # 225° Valley
    ((0.110, 0.725), SMOOTH),  # 240° Peak
    ((0.152, 0.593), VALLEY),  # 255° Valley
    ((0.050, 0.500), SMOOTH),  # 270° Peak
    ((0.152, 0.407), VALLEY),  # 285° Valley
    ((0.110, 0.275), SMOOTH),  # 300° Peak
    ((0.245, 0.245), VALLEY),  # 315° Valley
    ((0.275, 0.110), SMOOTH),  # 330° Peak
    ((0.407, 0.152), VALLEY),  # 345° Valley
]

GHOST_ROUNDING = CornerRounding(radius=0.125)
ghost_ish = [
    ((0.15, 0.10), FULL_ROUND), # semi-circle
    ((0.85, 0.10), FULL_ROUND),
    ((0.85, 0.75), ROUND), # right
    ((0.75, 0.85), ROUND),
    ((0.50, 0.70), ROUND), # cave-in
    ((0.25, 0.85), GHOST_ROUNDING), # left
    ((0.15, 0.75), GHOST_ROUNDING),
    ((0.15, 0.50), SHARP),
]


leaf_clover_4 = [
    ((0.50, 0.20), SHARP), # cave-in
    ((0.65, 0.10), SEMI_MEDIUM_ROUND),
    ((0.90, 0.35), SEMI_MEDIUM_ROUND),
    ((0.80, 0.50), SHARP), # cave-in
    ((0.90, 0.65), SEMI_MEDIUM_ROUND),
    ((0.65, 0.90), SEMI_MEDIUM_ROUND),
    ((0.50, 0.80), SHARP), # cave-in
    ((0.35, 0.90), SEMI_MEDIUM_ROUND),
    ((0.10, 0.65), SEMI_MEDIUM_ROUND),
    ((0.20, 0.50), SHARP), # cave-in
    ((0.10, 0.35), SEMI_MEDIUM_ROUND),
    ((0.35, 0.10), SEMI_MEDIUM_ROUND),
]

leaf_clover_8 = [
    ((0.500, 0.050), SMOOTH),  # 0.0° Peak
    ((0.638, 0.167), SHARP),   # 22.5° Valley
    ((0.818, 0.182), SMOOTH),  # 45.0° Peak
    ((0.833, 0.362), SHARP),   # 67.5° Valley
    ((0.950, 0.500), SMOOTH),  # 90.0° Peak
    ((0.833, 0.638), SHARP),   # 112.5° Valley
    ((0.818, 0.818), SMOOTH),  # 135.0° Peak
    ((0.638, 0.833), SHARP),   # 157.5° Valley
    ((0.500, 0.950), SMOOTH),  # 180.0° Peak
    ((0.362, 0.833), SHARP),   # 202.5° Valley
    ((0.182, 0.818), SMOOTH),  # 225.0° Peak
    ((0.167, 0.638), SHARP),   # 247.5° Valley
    ((0.050, 0.500), SMOOTH),  # 270.0° Peak
    ((0.167, 0.362), SHARP),   # 292.5° Valley
    ((0.182, 0.182), SMOOTH),  # 315.0° Peak
    ((0.362, 0.167), SHARP),   # 337.5° Valley
]

BOOM_VALLEY = CornerRounding(radius=0.005, smoothing=0.0)
boom = [
    ((0.500, 0.050), BOOM_VALLEY),
    ((0.539, 0.304), BOOM_VALLEY), # valley
    ((0.672, 0.084), BOOM_VALLEY),
    ((0.615, 0.347), BOOM_VALLEY), # valley
    ((0.818, 0.182), BOOM_VALLEY),
    ((0.678, 0.404), BOOM_VALLEY), # valley
    ((0.916, 0.328), BOOM_VALLEY),
    ((0.713, 0.461), BOOM_VALLEY), # valley
    ((0.950, 0.500), BOOM_VALLEY),
    ((0.713, 0.539), BOOM_VALLEY), # valley
    ((0.916, 0.672), BOOM_VALLEY),
    ((0.678, 0.596), BOOM_VALLEY), # valley
    ((0.818, 0.818), BOOM_VALLEY),
    ((0.615, 0.653), BOOM_VALLEY), # valley
    ((0.672, 0.916), BOOM_VALLEY),
    ((0.539, 0.696), BOOM_VALLEY), # valley
    ((0.500, 0.950), BOOM_VALLEY),
    ((0.461, 0.696), BOOM_VALLEY), # valley
    ((0.328, 0.916), BOOM_VALLEY),
    ((0.385, 0.653), BOOM_VALLEY), # valley
    ((0.182, 0.818), BOOM_VALLEY),
    ((0.322, 0.596), BOOM_VALLEY), # valley
    ((0.084, 0.672), BOOM_VALLEY),
    ((0.287, 0.539), BOOM_VALLEY), # valley
    ((0.050, 0.500), BOOM_VALLEY),
    ((0.287, 0.461), BOOM_VALLEY), # valley
    ((0.084, 0.328), BOOM_VALLEY),
    ((0.322, 0.404), BOOM_VALLEY), # valley
    ((0.182, 0.182), BOOM_VALLEY),
    ((0.385, 0.347), BOOM_VALLEY), # valley
    ((0.328, 0.084), BOOM_VALLEY),
    ((0.461, 0.304), BOOM_VALLEY), # valley
]

pixel_circle = [
    # --- TOP (North) - Wider Cap ---
    ((0.40, 0.10), SHARP),
    ((0.60, 0.10), SHARP),
    
    # --- NORTH EAST ---
    ((0.60, 0.15), SHARP),
    ((0.70, 0.15), SHARP),
    ((0.70, 0.20), SHARP),
    ((0.80, 0.20), SHARP),
    ((0.80, 0.30), SHARP),
    ((0.85, 0.30), SHARP),
    ((0.85, 0.40), SHARP),
    ((0.90, 0.40), SHARP),

    # --- RIGHT (East) - Wider Side ---
    ((0.90, 0.60), SHARP),
    
    # --- SOUTH EAST ---
    ((0.85, 0.60), SHARP),
    ((0.85, 0.70), SHARP),
    ((0.80, 0.70), SHARP),
    ((0.80, 0.80), SHARP),
    ((0.70, 0.80), SHARP),
    ((0.70, 0.85), SHARP),
    ((0.60, 0.85), SHARP),
    ((0.60, 0.90), SHARP),

    # --- BOTTOM (South) - Wider Cap ---
    ((0.40, 0.90), SHARP),
    
    # --- SOUTH WEST ---
    ((0.40, 0.85), SHARP),
    ((0.30, 0.85), SHARP),
    ((0.30, 0.80), SHARP),
    ((0.20, 0.80), SHARP),
    ((0.20, 0.70), SHARP),
    ((0.15, 0.70), SHARP),
    ((0.15, 0.60), SHARP),
    ((0.10, 0.60), SHARP),

    # --- LEFT (West) - Wider Side ---
    ((0.10, 0.40), SHARP),
    
    # --- NORTH WEST ---
    ((0.15, 0.40), SHARP),
    ((0.15, 0.30), SHARP),
    ((0.20, 0.30), SHARP),
    ((0.20, 0.20), SHARP),
    ((0.30, 0.20), SHARP),
    ((0.30, 0.15), SHARP),
    ((0.40, 0.15), SHARP),
]

pixel_triangle = [
    # --- Start at Top-Back ---
    ((0.20, 0.06), SHARP),
    # --- 5 Steps Up/Forward ---
    ((0.32, 0.06), SHARP),
    ((0.32, 0.14), SHARP),  # Step 1
    ((0.44, 0.14), SHARP),
    ((0.44, 0.22), SHARP),  # Step 2
    ((0.56, 0.22), SHARP),
    ((0.56, 0.30), SHARP),  # Step 3
    ((0.68, 0.30), SHARP),
    ((0.68, 0.38), SHARP),  # Step 4
    ((0.80, 0.38), SHARP),
    ((0.80, 0.46), SHARP),  # Step 5
    # --- Single Step Tip (The Nose) ---
    ((0.92, 0.46), SHARP),
    ((0.92, 0.54), SHARP),  # Centered around 0.50
    # --- 5 Steps Down/Back ---
    ((0.80, 0.54), SHARP),
    ((0.80, 0.62), SHARP),  # Step 5 Down
    ((0.68, 0.62), SHARP),
    ((0.68, 0.70), SHARP),  # Step 4 Down
    ((0.56, 0.70), SHARP),
    ((0.56, 0.78), SHARP),  # Step 3 Down
    ((0.44, 0.78), SHARP),
    ((0.44, 0.86), SHARP),  # Step 2 Down
    ((0.32, 0.86), SHARP),
    ((0.32, 0.94), SHARP),  # Step 1 Down
    # --- Back Edge ---
    ((0.20, 0.94), SHARP),
    ((0.20, 0.46), SHARP),  # Mid-back pivot
]

BUN_ROUND = CornerRounding(radius=0.175, smoothing=0.0)
bun = [
    # top Bun
    ((0.15, 0.15), BUN_ROUND),
    ((0.85, 0.15), BUN_ROUND),
    ((0.85, 0.5), BUN_ROUND),
    ((0.65, 0.50), SHARP),
    # bottom Bun
    ((0.85, 0.5), BUN_ROUND),
    ((0.85, 0.85), BUN_ROUND),
    ((0.15, 0.85), BUN_ROUND),
    ((0.15, 0.5), BUN_ROUND),
    ((0.35, 0.50), SHARP),
    ((0.15, 0.5), BUN_ROUND),
]

HEART_ROUNDING = CornerRounding(radius=0.15, smoothing=0.0)
heart = [
    ((0.10, 0.30), HEART_ROUNDING),
    ((0.30, 0.10), HEART_ROUNDING),
    ((0.50, 0.35), SHARP),
    ((0.70, 0.10), HEART_ROUNDING),
    ((0.90, 0.30), HEART_ROUNDING),
    ((0.50, 0.85), SHARP),
]

organic_blob = [
    ((0.50, 0.15), ROUND),
    ((0.90, 0.30), ROUND),
    ((0.75, 1.00), ROUND),
    ((0.20, 0.70), ROUND),
    ((0.10, 0.40), DIAMOND_ROUNDING),
]

FLOWER_ROUNDING = CornerRounding(radius=0.1, smoothing=1.0)
flower = [
    ((0.340, 0.100), FLOWER_ROUNDING),  # 0° Peak
    ((0.660, 0.100), FLOWER_ROUNDING),  # 0° Peak
    ((0.577, 0.315), SHARP),            # 22.5° Cave-in
    
    ((0.670, 0.104), FLOWER_ROUNDING),  # 45° Peak 
    ((0.896, 0.330), FLOWER_ROUNDING),  # 45° Peak 
    ((0.685, 0.423), SHARP),            # 67.5° Cave-in
    
    ((0.900, 0.340), FLOWER_ROUNDING),  # 90° Peak
    ((0.900, 0.660), FLOWER_ROUNDING),  # 90° Peak
    ((0.685, 0.577), SHARP),            # 112.5° Cave-in
    
    ((0.896, 0.670), FLOWER_ROUNDING),  # 135° Peak
    ((0.670, 0.896), FLOWER_ROUNDING),  # 135° Peak
    ((0.577, 0.685), SHARP),            # 157.5° Cave-in
    
    ((0.660, 0.900), FLOWER_ROUNDING),  # 180° Peak
    ((0.340, 0.900), FLOWER_ROUNDING),  # 180° Peak
    ((0.423, 0.685), SHARP),            # 202.5° Cave-in
    
    ((0.330, 0.896), FLOWER_ROUNDING),  # 225° Peak
    ((0.104, 0.670), FLOWER_ROUNDING),  # 225° Peak
    ((0.315, 0.577), SHARP),            # 247.5° Cave-in
    
    ((0.100, 0.660), FLOWER_ROUNDING),  # 270° Peak
    ((0.100, 0.340), FLOWER_ROUNDING),  # 270° Peak
    ((0.315, 0.423), SHARP),            # 292.5° Cave-in
    
    ((0.104, 0.330), FLOWER_ROUNDING),  # 315° Peak
    ((0.330, 0.104), FLOWER_ROUNDING),  # 315° Peak
    ((0.423, 0.315), SHARP),            # 337.5° Cave-in
]

FAN_ROUNDING = CornerRounding(radius=0.1, smoothing=1.0)
fan_16_sided = [
    ((0.450, 0.000), FAN_ROUNDING),
    ((0.550, 0.000), FAN_ROUNDING),
    ((0.598, 0.122), SHARP),

    ((0.641, 0.024), FAN_ROUNDING),
    ((0.732, 0.091), FAN_ROUNDING),
    ((0.720, 0.220), SHARP),

    ((0.878, 0.402), FAN_ROUNDING),
    ((0.909, 0.268), FAN_ROUNDING),
    ((0.878, 0.402), SHARP),

    ((0.976, 0.359), FAN_ROUNDING),
    ((0.909, 0.450), FAN_ROUNDING),
    ((0.878, 0.598), SHARP),

    ((1.000, 0.450), FAN_ROUNDING),
    ((1.000, 0.550), FAN_ROUNDING),
    ((0.878, 0.598), SHARP),

    ((0.976, 0.641), FAN_ROUNDING),
    ((0.909, 0.732), FAN_ROUNDING),
    ((0.720, 0.780), SHARP),

    ((0.732, 0.909), FAN_ROUNDING),
    ((0.641, 0.976), FAN_ROUNDING),
    ((0.598, 0.878), SHARP),

    ((0.550, 1.000), FAN_ROUNDING),
    ((0.450, 1.000), FAN_ROUNDING),
    ((0.402, 0.878), SHARP),

    ((0.359, 0.976), FAN_ROUNDING),
    ((0.268, 0.909), FAN_ROUNDING),
    ((0.280, 0.780), SHARP),

    ((0.122, 0.598), FAN_ROUNDING),
    ((0.091, 0.732), FAN_ROUNDING),
    ((0.122, 0.598), SHARP),

    ((0.024, 0.641), FAN_ROUNDING),
    ((0.091, 0.550), FAN_ROUNDING),
    ((0.122, 0.402), SHARP),

    ((0.000, 0.550), FAN_ROUNDING),
    ((0.000, 0.450), FAN_ROUNDING),
    ((0.122, 0.402), SHARP),

    ((0.024, 0.359), FAN_ROUNDING),
    ((0.091, 0.268), FAN_ROUNDING),
    ((0.280, 0.220), SHARP),

    ((0.268, 0.091), FAN_ROUNDING),
    ((0.359, 0.024), FAN_ROUNDING),
    ((0.402, 0.122), SHARP),

    ((0.450, 0.000), FAN_ROUNDING),
]



# FLOWER_ROUNDING = CornerRounding(radius=0.1, smoothing=1.0)
# fan_8_sided= [
#     ((0.400, 0.000), FLOWER_ROUNDING),  # 0° Peak
#     ((0.600, 0.000), FLOWER_ROUNDING),  # 0° Peak
#     ((0.596, 0.269), SHARP),  # 22.5° Cave-in
#     ((0.783, 0.076), FLOWER_ROUNDING),  # 45° Peak
#     ((0.924, 0.217), FLOWER_ROUNDING),  # 45° Peak
#     ((0.731, 0.404), SHARP),  # 67.5° Cave-in
#     ((1.000, 0.400), FLOWER_ROUNDING),  # 90° Peak
#     ((1.000, 0.600), FLOWER_ROUNDING),  # 90° Peak
#     ((0.731, 0.596), SHARP),  # 112.5° Cave-in
#     ((0.924, 0.783), FLOWER_ROUNDING),  # 135° Peak
#     ((0.783, 0.924), FLOWER_ROUNDING),  # 135° Peak
#     ((0.596, 0.731), SHARP),  # 157.5° Cave-in
#     ((0.600, 1.000), FLOWER_ROUNDING),  # 180° Peak
#     ((0.400, 1.000), FLOWER_ROUNDING),  # 180° Peak
#     ((0.404, 0.731), SHARP),  # 202.5° Cave-in
#     ((0.217, 0.924), FLOWER_ROUNDING),  # 225° Peak
#     ((0.076, 0.783), FLOWER_ROUNDING),  # 225° Peak
#     ((0.269, 0.596), SHARP),  # 247.5° Cave-in
#     ((0.000, 0.600), FLOWER_ROUNDING),  # 270° Peak
#     ((0.000, 0.400), FLOWER_ROUNDING),  # 270° Peak
#     ((0.269, 0.404), SHARP),  # 292.5° Cave-in
#     ((0.076, 0.217), FLOWER_ROUNDING),  # 315° Peak
#     ((0.217, 0.076), FLOWER_ROUNDING),  # 315° Peak
#     ((0.404, 0.269), SHARP),  # 337.5° Cave-in
# ]

shield = [
    ((0.10, 0.10), SMALL_ROUND),  # Top Left
    ((0.90, 0.10), SMALL_ROUND),  # Top Right
    ((0.90, 0.50), SMALL_ROUND),  # Side transition
    ((0.50, 1.00), SMALL_ROUND),  # Bottom Point
    ((0.10, 0.50), SMALL_ROUND),  # Side transition
]

star = [
    ((0.50, 0.05), SHARP),  # Top Spike
    ((0.60, 0.40), VALLEY),
    ((0.95, 0.40), SHARP),  # Right Spike
    ((0.70, 0.60), VALLEY),
    ((0.80, 0.95), SHARP),  # Bottom Right
    ((0.50, 0.75), VALLEY),
    ((0.20, 0.95), SHARP),  # Bottom Left
    ((0.30, 0.60), VALLEY),
    ((0.05, 0.40), SHARP),  # Left Spike
    ((0.40, 0.40), VALLEY),
]

puffy_diamond = [
    ((0.50, 0.00), HEART_ROUNDING),
    ((0.660, 0.160), HEART_ROUNDING),
    ((0.590, 0.252), SHARP),
    ((0.680, 0.180), HEART_ROUNDING),
    ((0.820, 0.320), HEART_ROUNDING),
    ((0.748, 0.415), SHARP),
    ((0.840, 0.340), HEART_ROUNDING),

    ((1.00, 0.50), HEART_ROUNDING),
    ((0.840, 0.660), HEART_ROUNDING),
    ((0.748, 0.585), SHARP),
    ((0.820, 0.680), HEART_ROUNDING),
    ((0.680, 0.820), HEART_ROUNDING),
    ((0.585, 0.748), SHARP),
    ((0.660, 0.840), HEART_ROUNDING),

    ((0.50, 1.00), HEART_ROUNDING),
    ((0.340, 0.840), HEART_ROUNDING),
    ((0.410, 0.748), SHARP),
    ((0.320, 0.820), HEART_ROUNDING),
    ((0.180, 0.680), HEART_ROUNDING),
    ((0.252, 0.590), SHARP),
    ((0.160, 0.660), HEART_ROUNDING),

    ((0.00, 0.50), HEART_ROUNDING),
    ((0.160, 0.340), HEART_ROUNDING),
    ((0.252, 0.410), SHARP),
    ((0.180, 0.320), HEART_ROUNDING),
    ((0.320, 0.180), HEART_ROUNDING),
    ((0.415, 0.252), SHARP),
    ((0.340, 0.160), HEART_ROUNDING),
]