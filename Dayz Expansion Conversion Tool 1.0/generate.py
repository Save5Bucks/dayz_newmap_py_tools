# generate_all.py
import json
import os
from cities import cities  # Import source data

# Map name for consistency
MAP_NAME = "Raman"

# Teleport JSON template
teleport_template = {
    "m_Version": 1,
    "Enabled": 1,
    "Type": 0,
    "Name": "",
    "TelePos": {"x": 0.0, "y": 0.0, "z": 0.0},
    "Radius": 25,
    "TeleHeight": 0.0,
    "Cooldown": 0,
    "Message": ""
}

# Roaming locations template
roaming_template = {
    "m_Version": 1,
    "RoamingLocations": [],
    "ExcludedRoamingBuildings": [
        "Land_CementWorks_Hall2_Grey", "Land_Factory_Small", "Land_House_1W09",
        "Land_House_2W03", "Land_HouseBlock_1F4", "Land_Boathouse",
        "Land_Mine_Building", "Land_Shed_W2", "Land_Tenement_Big"
    ],
    "NoGoAreas": []
}

# Keywords for contaminated areas
contaminated_keywords = ["Industrial", "Military", "Antenna", "Mine", "Island", "Transformer"]

# Create teleports folder
teleports_dir = "teleports"
os.makedirs(teleports_dir, exist_ok=True)

# Process all locations
spawn_points = []
roaming_locations = []
contaminated_positions = []

for loc in cities["Locations"]:
    name = loc["Name"]
    x, y, z = loc["Position"]
    
    # 1. Generate Spawn Points
    spawn_points.append({
        "Name": name,
        "Positions": [[x, y, z]],
        "UseCooldown": 1
    })
    
    # 2. Generate Roaming Locations
    radius = 500.0 if loc["Type"] == "CityCap" else 100.0
    roaming_locations.append({
        "Name": name,
        "Position": [x, y, z],
        "Radius": radius,
        "Type": loc["Type"] if loc["Type"] else "Local",
        "Enabled": 1
    })
    
    # 3. Generate Contaminated Areas (Teleports and XML)
    if any(keyword.lower() in name.lower() for keyword in contaminated_keywords):
        # Teleports JSON
        teleport_config = teleport_template.copy()
        teleport_config["Name"] = f"Contaminated_{name}"
        teleport_config["TelePos"] = {"x": x, "y": y, "z": z}
        teleport_file = os.path.join(teleports_dir, f"Teleports_{MAP_NAME}_{name.replace(' ', '_')}.json")
        with open(teleport_file, "w") as f:
            json.dump(teleport_config, f, indent=4)
        
        # Contaminated Areas XML
        contaminated_positions.append(f'  <pos x="{x:.6f}" z="{z:.6f}" />')

# Write Spawn Points
with open("spawn_points.py", "w") as f:
    f.write("# Spawn points for Raman City\n")
    f.write("spawn_points = [\n")
    for sp in spawn_points:
        f.write(f"    {json.dumps(sp, indent=4).replace('    ', '        ')[4:-1]},\n")
    f.write("]\n")

# Write Roaming Locations
roaming_template["RoamingLocations"] = roaming_locations
with open("roaming_locations.py", "w") as f:
    f.write("# Roaming locations for Raman City\n")
    f.write("roaming_locations = ")
    f.write(json.dumps(roaming_template, indent=4))
    f.write("\n")

# Write Contaminated Areas XML
with open("contaminated_areas.xml", "w") as f:
    f.write('<event name="StaticContaminatedArea">\n')
    for line in contaminated_positions:
        f.write(line + "\n")
    f.write('</event>\n')

print(f"Generated:")
print(f"- {len(spawn_points)} spawn points in 'spawn_points.py'")
print(f"- {len(roaming_locations)} roaming locations in 'roaming_locations.py'")
print(f"- {len(contaminated_positions)} contaminated areas in 'contaminated_areas.xml' and 'teleports' folder")