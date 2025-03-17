import json
import os
from spawn_points import locations  # Import locations from locations.py

# Template for the JSON structure
template = {
    "m_Version": 2,
    "Enabled": 1,
    "Weight": 1.0,
    "MissionMaxTime": 1200,
    "MissionName": "",  # Will be filled dynamically
    "Difficulty": 0,
    "Objective": 0,
    "Reward": "",
    "ShowNotification": 1,
    "Height": 450.0,
    "Speed": 25.0,
    "Container": "Random",
    "FallSpeed": 4.5,
    "DropLocation": {
        "x": 0.0,  # Will be filled dynamically
        "z": 0.0,  # Will be filled dynamically
        "Name": "",  # Will be filled dynamically
        "Radius": 100.0
    },
    "Infected": [],
    "ItemCount": -1,
    "InfectedCount": -1,
    "AirdropPlaneClassName": "",
    "Loot": []
}

# Create output directory if it doesn't exist
output_dir = "airdrop_files"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate JSON files
for location in locations:  # Use the imported locations directly
    name = location["Name"]
    # Replace spaces with underscores for filename
    filename_safe_name = name.replace(" ", "_")
    x_coord = location["Positions"][0][0]  # First number (X)
    z_coord = location["Positions"][0][2]  # Third number (Z)
    
    # Create a copy of the template
    config = template.copy()
    
    # Fill in dynamic values
    config["MissionName"] = f"Random_{name}"  # MissionName keeps original name with spaces
    config["DropLocation"]["x"] = x_coord
    config["DropLocation"]["z"] = z_coord
    config["DropLocation"]["Name"] = name  # DropLocation Name keeps original name with spaces
    
    # Write to file using filename_safe_name (spaces replaced with underscores)
    filename = f"Airdrop_Random_{filename_safe_name}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)

print(f"Generated {len(locations)} JSON files in the '{output_dir}' directory.")