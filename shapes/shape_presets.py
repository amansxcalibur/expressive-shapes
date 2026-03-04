from geometry.corner_rounding import CornerRounding

# --- PRESET STYLES ---
SHARP = CornerRounding(radius=0.0, smoothing=0.0)
SOFT = CornerRounding(radius=20.0, smoothing=0.8)
DEEP = CornerRounding(radius=40.0, smoothing=1.0)
ROUND = CornerRounding(radius=35.0, smoothing=0.0)
MEDIUM_ROUND = CornerRounding(radius=250.0, smoothing=0.0)
VERY_ROUND = CornerRounding(radius=750.0, smoothing=0.0)
SMOOTH = CornerRounding(radius=35.0, smoothing=0.8)
VALLEY = CornerRounding(radius=100.0, smoothing=1.0)

puffy_square = [
    ((0.20, 0.20), SMOOTH),
    ((0.80, 0.20), SMOOTH),
    ((0.80, 0.80), SMOOTH),
    ((0.20, 0.80), SMOOTH),
]

shield = [
    ((0.20, 0.20), ROUND),  # Top Left
    ((0.80, 0.20), ROUND),  # Top Right
    ((0.80, 0.50), SMOOTH),  # Side transition
    ((0.50, 0.90), SMOOTH),  # Bottom Point
    ((0.20, 0.50), SMOOTH),  # Side transition
]

clover_flower = [
    ((0.50, 0.05), ROUND),
    ((0.65, 0.18), ROUND),
    ((0.5, 0.50), SHARP),
    ((0.95, 0.50), ROUND),
    ((0.82, 0.65), ROUND),
    ((0.5, 0.5), SHARP),
    ((0.50, 0.95), ROUND),
    ((0.35, 0.82), ROUND),
    ((0.5, 0.5), SHARP),
    ((0.05, 0.50), ROUND),
    ((0.18, 0.35), ROUND),
    ((0.5, 0.5), SHARP),
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

pill = [
    ((0.15, 0.35), ROUND),
    ((0.85, 0.35), ROUND),
    ((0.85, 0.65), ROUND),
    ((0.15, 0.65), ROUND),
]

organic_blob = [
    ((0.50, 0.15), SMOOTH),
    ((0.85, 0.25), SMOOTH),
    ((0.75, 0.85), SMOOTH),
    ((0.25, 0.70), SMOOTH),
    ((0.10, 0.40), SMOOTH),
]

concave_rectangle = [
    ((0.10, 0.1), ROUND),  # Top Spike
    ((0.50, 0.40), VALLEY),
    ((0.9, 0.10), ROUND),  # Right Spike
    ((0.60, 0.50), VALLEY),
    ((0.9, 0.9), ROUND),  # Bottom Right
    ((0.50, 0.6), VALLEY),
    ((0.1, 0.9), ROUND),  # Bottom Left
    ((0.40, 0.50), VALLEY),
]

# A 12-pointed scalloped cookie (24 points total)
cookie_12 = [
    ((0.50, 0.05), SMOOTH),  # Peak 1 (Top)
    ((0.55, 0.40), VALLEY),  # Cave-in
    ((0.72, 0.11), SMOOTH),  # Peak 2
    ((0.65, 0.45), VALLEY),  # Cave-in
    ((0.89, 0.28), SMOOTH),  # Peak 3
    ((0.70, 0.50), VALLEY),  # Cave-in
    ((0.95, 0.50), SMOOTH),  # Peak 4 (Right)
    ((0.70, 0.55), VALLEY),  # Cave-in
    ((0.89, 0.72), SMOOTH),  # Peak 5
    ((0.65, 0.60), VALLEY),  # Cave-in
    ((0.72, 0.89), SMOOTH),  # Peak 6
    ((0.55, 0.65), VALLEY),  # Cave-in
    ((0.50, 0.95), SMOOTH),  # Peak 7 (Bottom)
    ((0.45, 0.65), VALLEY),  # Cave-in
    ((0.28, 0.89), SMOOTH),  # Peak 8
    ((0.35, 0.60), VALLEY),  # Cave-in
    ((0.11, 0.72), SMOOTH),  # Peak 9
    ((0.30, 0.55), VALLEY),  # Cave-in
    ((0.05, 0.50), SMOOTH),  # Peak 10 (Left)
    ((0.30, 0.50), VALLEY),  # Cave-in
    ((0.11, 0.28), SMOOTH),  # Peak 11
    ((0.35, 0.45), VALLEY),  # Cave-in
    ((0.28, 0.11), SMOOTH),  # Peak 12
    ((0.45, 0.40), VALLEY),  # Cave-in
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

fan = [
    ((0.10, 0.10), MEDIUM_ROUND),  # Bottom Pivot Point
    ((0.90, 0.10), VERY_ROUND),  # Left Blade Tip
    ((0.9, 0.9), MEDIUM_ROUND),  # Inner Gorge
    ((0.10, 0.90), MEDIUM_ROUND),  # Center Top Blade
]

apple = [
    ((0.20, 0.20), ROUND),
    ((0.40, 0.60), CornerRounding(radius=35.0, smoothing=0.8)),
    ((0.80, 0.80), ROUND),
    ((0.20, 0.80), ROUND),
]


t_apple = [
    ((0.20, 0.20), SHARP),
    ((0.40, 0.60), CornerRounding(radius=35.0, smoothing=0.8)),
    ((0.80, 0.80), SHARP),
    ((0.20, 0.80), SHARP),
]

t_fan = [
    ((0.10, 0.10), SHARP),  # Bottom Pivot Point
    ((0.90, 0.10), VERY_ROUND),  # Left Blade Tip
    ((0.9, 0.9), SHARP),  # Inner Gorge
    ((0.10, 0.90), SHARP),  # Center Top Blade
]

arrow = [
    ((0.50, 0.10), ROUND),  # Bottom Pivot Point
    ((0.90, 0.90), ROUND),  # Left Blade Tip
    ((0.5, 0.7), VALLEY),  # Inner Gorge
    ((0.10, 0.90), ROUND),  # Center Top Blade
]

slanted = [
    ((0.2, 0.15), DEEP),
    ((0.90, 0.15), DEEP),
    ((0.8, 0.85), DEEP),
    ((0.10, 0.85), DEEP),
]

triangle = [((0.50, 0.10), ROUND), ((0.90, 0.90), ROUND), ((0.10, 0.90), ROUND)]


circle = [
    ((0.50, 0.05), VERY_ROUND),
    ((0.95, 0.50), VERY_ROUND),
    ((0.50, 0.95), VERY_ROUND),
    ((0.05, 0.50), VERY_ROUND),
]

square = [
    ((0.20, 0.20), ROUND),
    ((0.80, 0.20), ROUND),
    ((0.80, 0.80), ROUND),
    ((0.20, 0.80), ROUND),
]

arch = [
    ((0.20, 0.20), VERY_ROUND),
    ((0.80, 0.20), VERY_ROUND),
    ((0.80, 0.90), ROUND),
    ((0.20, 0.90), ROUND),
]

semicircle = [
    ((0.10, 0.45), VERY_ROUND),
    ((0.90, 0.45), VERY_ROUND),
    ((0.90, 0.85), SHARP),
    ((0.10, 0.85), SHARP),
]

oval = [
    ((0.10, 0.10), VERY_ROUND),
    ((0.90, 0.10), CornerRounding(radius=140, smoothing=1.0)),
    ((0.90, 0.90), VERY_ROUND),
    ((0.10, 0.90), CornerRounding(radius=140, smoothing=1.0)),
]

pill_tilted = [
    ((0.60, 0.10), VERY_ROUND),
    ((0.90, 0.40), VERY_ROUND),
    ((0.40, 0.90), VERY_ROUND),
    ((0.10, 0.60), VERY_ROUND),
]

diamond = [
    ((0.50, 0.10), ROUND),
    ((0.85, 0.50), ROUND),
    ((0.50, 0.90), ROUND),
    ((0.15, 0.50), ROUND),
]
CLAMSHELL_ROUND = CornerRounding(radius=70, smoothing=0.0)
clamshell = [
    ((0.25, 0.25), CLAMSHELL_ROUND),
    ((0.75, 0.25), CLAMSHELL_ROUND),
    ((0.90, 0.50), CLAMSHELL_ROUND),
    ((0.75, 0.75), CLAMSHELL_ROUND),
    ((0.25, 0.75), CLAMSHELL_ROUND),
    ((0.10, 0.50), CLAMSHELL_ROUND),
]

pentagon = [
    ((0.50, 0.15), ROUND),
    ((0.85, 0.40), ROUND),
    ((0.75, 0.85), ROUND),
    ((0.25, 0.85), ROUND),
    ((0.15, 0.40), ROUND),
]

GEM_ROUND = CornerRounding(radius=70, smoothing=0.0)
gem = [
    ((0.50, 0.15), GEM_ROUND),
    ((0.80, 0.30), GEM_ROUND),
    ((0.85, 0.70), GEM_ROUND),
    ((0.50, 0.85), GEM_ROUND),
    ((0.15, 0.70), GEM_ROUND),
    ((0.20, 0.30), GEM_ROUND),
]

very_sunny = [
    ((0.50, 0.05), ROUND),
    ((0.65, 0.15), VALLEY),
    ((0.85, 0.20), ROUND),
    ((0.80, 0.40), VALLEY),
    ((0.95, 0.55), ROUND),
    ((0.80, 0.70), VALLEY),
    ((0.75, 0.90), ROUND),
    ((0.55, 0.80), VALLEY),
    ((0.35, 0.95), ROUND),
    ((0.25, 0.75), VALLEY),
    ((0.05, 0.65), ROUND),
    ((0.20, 0.45), VALLEY),
    ((0.15, 0.20), ROUND),
    ((0.40, 0.25), VALLEY),
]

sunny = [
    ((0.50, 0.10), SMOOTH),
    ((0.75, 0.25), SMOOTH),
    ((0.90, 0.50), SMOOTH),
    ((0.75, 0.75), SMOOTH),
    ((0.50, 0.90), SMOOTH),
    ((0.25, 0.75), SMOOTH),
    ((0.10, 0.50), SMOOTH),
    ((0.25, 0.25), SMOOTH),
]

four_leaf_clover = [
    ((0.50, 0.40), SHARP),
    ((0.90, 0.10), VERY_ROUND),
    ((0.60, 0.50), SHARP),
    ((0.90, 0.90), VERY_ROUND),
    ((0.50, 0.60), SHARP),
    ((0.10, 0.90), VERY_ROUND),
    ((0.40, 0.50), SHARP),
    ((0.10, 0.10), VERY_ROUND),
]


puffy_diamond = [
    ((0.50, 0.10), ROUND),
    ((0.80, 0.50), ROUND),
    ((0.50, 0.90), ROUND),
    ((0.20, 0.50), ROUND),
]

GHOST_ROUND = CornerRounding(radius=180, smoothing=0)
ghost_ish = [
    ((0.25, 0.30), VERY_ROUND),
    ((0.75, 0.30), VERY_ROUND),
    ((0.75, 0.90), GHOST_ROUND),
    ((0.50, 0.7), GHOST_ROUND),
    ((0.25, 0.90), GHOST_ROUND),
]

BUN_ROUND = CornerRounding(radius=250, smoothing=0.0)

bun = [
    # Top Bun
    ((0.20, 0.20), BUN_ROUND),
    ((0.80, 0.20), BUN_ROUND),
    ((0.80, 0.5), BUN_ROUND),
    ((0.65, 0.50), SHARP),
    # Bottom Bun
    ((0.80, 0.5), BUN_ROUND),
    ((0.80, 0.80), BUN_ROUND),
    ((0.20, 0.80), BUN_ROUND),
    ((0.20, 0.5), BUN_ROUND),
    ((0.35, 0.50), SHARP),
    ((0.20, 0.5), BUN_ROUND),
]

heart = [
    ((0.1, 0.10), CornerRounding(radius=25.0, smoothing=0.0)),
    ((0.50, 0.50), SHARP),
    ((0.9, 0.10), CornerRounding(radius=25.0, smoothing=0.0)),
    ((0.5, 0.70), SHARP),
]

pixel_triangle = [
    # --- Start at Top-Back ---
    ((0.20, 0.10), SHARP),
    
    # --- 5 Steps Up/Forward ---
    ((0.32, 0.10), SHARP), ((0.32, 0.18), SHARP), # Step 1
    ((0.44, 0.18), SHARP), ((0.44, 0.26), SHARP), # Step 2
    ((0.56, 0.26), SHARP), ((0.56, 0.34), SHARP), # Step 3
    ((0.68, 0.34), SHARP), ((0.68, 0.42), SHARP), # Step 4
    ((0.80, 0.42), SHARP), ((0.80, 0.50), SHARP), # Step 5 (Entering Tip)

    # --- Single Step Tip (The Nose) ---
    ((0.92, 0.50), SHARP), 
    ((0.92, 0.58), SHARP), # Height is 0.08, same as steps

    # --- 5 Steps Down/Back ---
    ((0.80, 0.58), SHARP), ((0.80, 0.66), SHARP), # Step 5 Down
    ((0.68, 0.66), SHARP), ((0.68, 0.74), SHARP), # Step 4 Down
    ((0.56, 0.74), SHARP), ((0.56, 0.82), SHARP), # Step 3 Down
    ((0.44, 0.82), SHARP), ((0.44, 0.90), SHARP), # Step 2 Down
    ((0.32, 0.90), SHARP), ((0.32, 0.98), SHARP), # Step 1 Down
    
    # --- Back Edge ---
    ((0.20, 0.98), SHARP),
    ((0.20, 0.50), SHARP), # Mid-back pivot
]

pixel_circle = [
    ((0.40, 0.10), SHARP),
    ((0.60, 0.10), SHARP),  # Top
    ((0.60, 0.20), SHARP),
    ((0.80, 0.20), SHARP),
    ((0.80, 0.40), SHARP),
    ((0.90, 0.40), SHARP),  # Right top
    ((0.90, 0.60), SHARP),
    ((0.80, 0.60), SHARP),  # Right bottom
    ((0.80, 0.80), SHARP),
    ((0.60, 0.80), SHARP),
    ((0.60, 0.90), SHARP),
    ((0.40, 0.90), SHARP),  # Bottom
    ((0.40, 0.80), SHARP),
    ((0.20, 0.80), SHARP),
    ((0.20, 0.60), SHARP),
    ((0.10, 0.60), SHARP),  # Left bottom
    ((0.10, 0.40), SHARP),
    ((0.20, 0.40), SHARP),  # Left top
    ((0.20, 0.20), SHARP),
    ((0.40, 0.20), SHARP),
]

BOOM_VALLEY = CornerRounding(radius=5, smoothing=0.0)

boom = [
    ((0.500, 0.050), SHARP),
    ((0.539, 0.304), BOOM_VALLEY),
    ((0.672, 0.084), SHARP),
    ((0.615, 0.347), BOOM_VALLEY),
    ((0.818, 0.182), SHARP),
    ((0.678, 0.404), BOOM_VALLEY),
    ((0.916, 0.328), SHARP),
    ((0.713, 0.461), BOOM_VALLEY),
    ((0.950, 0.500), SHARP),
    ((0.713, 0.539), BOOM_VALLEY),
    ((0.916, 0.672), SHARP),
    ((0.678, 0.596), BOOM_VALLEY),
    ((0.818, 0.818), SHARP),
    ((0.615, 0.653), BOOM_VALLEY),
    ((0.672, 0.916), SHARP),
    ((0.539, 0.696), BOOM_VALLEY),
    ((0.500, 0.950), SHARP),
    ((0.461, 0.696), BOOM_VALLEY),
    ((0.328, 0.916), SHARP),
    ((0.385, 0.653), BOOM_VALLEY),
    ((0.182, 0.818), SHARP),
    ((0.322, 0.596), BOOM_VALLEY),
    ((0.084, 0.672), SHARP),
    ((0.287, 0.539), BOOM_VALLEY),
    ((0.050, 0.500), SHARP),
    ((0.287, 0.461), BOOM_VALLEY),
    ((0.084, 0.328), SHARP),
    ((0.322, 0.404), BOOM_VALLEY),
    ((0.182, 0.182), SHARP),
    ((0.385, 0.347), BOOM_VALLEY),
    ((0.328, 0.084), SHARP),
    ((0.461, 0.304), BOOM_VALLEY),
]

puffy_diamond = [
    # --- Top Group ---
    ((0.500, 0.050), VERY_ROUND), # 0° (Top Peak)
    ((0.565, 0.330), SHARP),      # 18° (The "Pinch")
    
    # --- Top-Right ---
    ((0.780, 0.220), VERY_ROUND), # 45°
    ((0.670, 0.435), SHARP),      # 72° (The "Pinch")
    
    # --- Right Group ---
    ((0.950, 0.500), VERY_ROUND), # 90° (Right Peak)
    ((0.670, 0.565), SHARP),      # 108°
    
    # --- Bottom-Right ---
    ((0.780, 0.780), VERY_ROUND), # 135°
    ((0.565, 0.670), SHARP),      # 162°
    
    # --- Bottom Group ---
    ((0.500, 0.950), VERY_ROUND), # 180° (Bottom Peak)
    ((0.435, 0.670), SHARP),      # 198°
    
    # --- Bottom-Left ---
    ((0.220, 0.780), VERY_ROUND), # 225°
    ((0.330, 0.565), SHARP),      # 252°
    
    # --- Left Group ---
    ((0.050, 0.500), VERY_ROUND), # 270° (Left Peak)
    ((0.330, 0.435), SHARP),      # 288°
    
    # --- Top-Left ---
    ((0.220, 0.220), VERY_ROUND), # 315°
    ((0.435, 0.330), SHARP),      # 342°
]