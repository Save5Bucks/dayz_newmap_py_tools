import json
import os
from spawn_points import locations  # Import locations from locations.py

# Template for the ContaminatedArea JSON structure
template = {
    "m_Version": 0,
    "Enabled": 0,
    "Weight": 1.0,
    "MissionMaxTime": 900,
    "MissionName": "",  # Will be filled dynamically
    "Difficulty": 0,
    "Objective": 0,
    "Reward": "",
    "Data": {
        "Pos": [
            0.0,  # Will be filled dynamically (x)
            0.0,  # Y stays 0.0
            0.0   # Will be filled dynamically (z)
        ],
        "Radius": 500.0,
        "PosHeight": 26.0,
        "NegHeight": 10.0,
        "InnerRingCount": 1,
        "InnerPartDist": 50,
        "OuterRingToggle": 1,
        "OuterPartDist": 50,
        "OuterOffset": 0,
        "VerticalLayers": 0,
        "VerticalOffset": 0,
        "ParticleName": "graphics/particles/contaminated_area_gas_bigass",
        "EffectInterval": 0,
        "EffectDuration": 0,
        "EffectModifier": 0
    },
    "PlayerData": {
        "AroundPartName": "graphics/particles/contaminated_area_gas_around",
        "TinyPartName": "graphics/particles/contaminated_area_gas_around_tiny",
        "PPERequesterType": "PPERequester_ContaminatedAreaTint"
    },
    "StartDecayLifetime": 600.0,
    "FinishDecayLifetime": 300.0
}

# Keywords to filter locations
keywords = ["Industrial", "Military", "Antenna", "Mine", "Island", "Transformer"]

# Create output directory if it doesn't exist
output_dir = "contaminated_areas"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Filter and generate JSON files
filtered_locations = []
for location in locations:  # Use the imported locations directly
    name = location["Name"]
    # Check if any keyword is in the name (case-insensitive)
    if any(keyword.lower() in name.lower() for keyword in keywords):
        filtered_locations.append(location)

for location in filtered_locations:
    name = location["Name"]
    # Replace spaces with underscores for filename
    filename_safe_name = name.replace(" ", "_")
    x_coord = location["Positions"][0][0]  # First number (X)
    z_coord = location["Positions"][0][2]  # Third number (Z)
    
    # Create a copy of the template
    config = template.copy()
    
    # Fill in dynamic values
    config["MissionName"] = name  # Using original name with spaces
    config["Data"]["Pos"] = [x_coord, 0.0, z_coord]
    
    # Write to file using filename_safe_name (spaces replaced with underscores)
    filename = f"ContaminatedArea_{filename_safe_name}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)

print(f"Generated {len(filtered_locations)} JSON files in the '{output_dir}' directory.")