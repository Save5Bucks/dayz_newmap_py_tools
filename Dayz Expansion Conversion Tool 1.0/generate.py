import json
import os
from cities import cities  # Import cities from cities.py

# Define output directories
output_dirs = {
    "teleports": "teleports",
    "airdrop_files": "airdrop_files",
    "contaminated_areas_files": "contaminated_areas_files",
    "spawn_points": "spawn_points",
    "roaming_locations": "roaming_locations",
    "contaminated_areas_xml": "contaminated_areas_xml"
}

# Create directories if they don't exist
for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# Keywords for contaminated areas
contaminated_keywords = ["Industrial", "Military", "Antenna", "Mine", "Island", "Transformer"]

# Templates
airdrop_template = {
    "m_Version": 2,
    "Enabled": 1,
    "Weight": 1.0,
    "MissionMaxTime": 1200,
    "MissionName": "",
    "Difficulty": 0,
    "Objective": 0,
    "Reward": "",
    "ShowNotification": 1,
    "Height": 450.0,
    "Speed": 25.0,
    "Container": "Random",
    "FallSpeed": 4.5,
    "DropLocation": {"x": 0.0, "z": 0.0, "Name": "", "Radius": 100.0},
    "Infected": [],
    "ItemCount": -1,
    "InfectedCount": -1,
    "AirdropPlaneClassName": "",
    "Loot": []
}

contaminated_template = {
    "m_Version": 2,
    "Enabled": 1,
    "Name": "",
    "TriggerType": 1,
    "Data": {
        "Shape": 1,
        "Radius": 150.0,
        "Pos": [0.0, 0.0, 0.0]
    },
    "PPEffects": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "VerticalLevels": 1,
    "VerticalOffset": 0.0,
    "ParticleLifeTime": 60.0,
    "ParticleBirthRate": 2.0,
    "SafePos": [0.0, 0.0, 0.0],
    "SafeRadius": 5.0,
    "Infected": [],
    "InfectedCount": -1
}

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

# 1. Teleports_Raman.json
teleports = []
for loc in cities["Locations"]:
    teleports.append({
        "Name": loc["Name"],
        "Position": loc["Position"]
    })
with open(os.path.join(output_dirs["teleports"], "Teleports_Raman.json"), "w") as f:
    json.dump(teleports, f, indent=4)

# 2. Airdrop JSON files
for loc in cities["Locations"]:
    config = airdrop_template.copy()
    name = loc["Name"]
    filename_safe_name = name.replace(" ", "_")
    config["MissionName"] = f"Random_{name}"
    config["DropLocation"]["x"] = loc["Position"][0]
    config["DropLocation"]["z"] = loc["Position"][2]
    config["DropLocation"]["Name"] = name
    with open(os.path.join(output_dirs["airdrop_files"], f"Airdrop_Random_{filename_safe_name}.json"), "w") as f:
        json.dump(config, f, indent=4)

# 3. Contaminated Area JSON files
contaminated_count = 0
for loc in cities["Locations"]:
    name = loc["Name"]
    if any(keyword.lower() in name.lower() for keyword in contaminated_keywords):
        config = contaminated_template.copy()
        config["Name"] = name
        config["Data"]["Pos"] = loc["Position"]
        filename_safe_name = name.replace(" ", "_")
        with open(os.path.join(output_dirs["contaminated_areas_files"], f"ContaminatedArea_{filename_safe_name}.json"), "w") as f:
            json.dump(config, f, indent=4)
        contaminated_count += 1

# 4. spawn_points.py
spawn_points = []
for loc in cities["Locations"]:
    spawn_points.append({
        "Name": loc["Name"],
        "Positions": [loc["Position"]],
        "UseCooldown": 1
    })
with open(os.path.join(output_dirs["spawn_points"], "spawn_points.py"), "w") as f:
    f.write("# Spawn points generated from Raman City Locations\n")
    f.write("spawn_points = [\n")
    for loc in spawn_points:
        loc_str = json.dumps(loc, indent=4)[1:-1].strip()
        f.write("    {\n")
        f.write(f"{loc_str}\n")
        f.write("    },\n")
    f.write("]\n")

# 5. roaming_locations.py
roaming_locations = []
for loc in cities["Locations"]:
    radius = 500.0 if loc["Type"] == "CityCap" else 100.0
    roaming_loc = {
        "Name": loc["Name"],
        "Position": loc["Position"],
        "Radius": radius,
        "Type": loc["Type"] if loc["Type"] else "Local",
        "Enabled": 1
    }
    roaming_locations.append(roaming_loc)
roaming_template["RoamingLocations"] = roaming_locations
with open(os.path.join(output_dirs["roaming_locations"], "roaming_locations.py"), "w") as f:
    f.write("# Roaming locations generated from Raman City Locations\n")
    f.write("roaming_locations = ")
    f.write(json.dumps(roaming_template, indent=4))
    f.write("\n")

# 6. contaminated_areas.xml
contaminated_positions = []
for loc in cities["Locations"]:
    name = loc["Name"]
    if any(keyword.lower() in name.lower() for keyword in contaminated_keywords):
        x_coord = loc["Position"][0]
        z_coord = loc["Position"][2]
        pos_line = f'  <pos x="{x_coord:.6f}" z="{z_coord:.6f}" />'
        contaminated_positions.append(pos_line)
with open(os.path.join(output_dirs["contaminated_areas_xml"], "contaminated_areas.xml"), "w") as f:
    f.write('<event name="StaticContaminatedArea">\n')
    for line in contaminated_positions:
        f.write(line + "\n")
    f.write('</event>\n')

# Summary
print(f"Generated files:")
print(f"- {output_dirs['teleports']}/Teleports_Raman.json with {len(cities['Locations'])} entries")
print(f"- {len(cities['Locations'])} airdrop files in {output_dirs['airdrop_files']}")
print(f"- {contaminated_count} contaminated area files in {output_dirs['contaminated_areas_files']}")
print(f"- {output_dirs['spawn_points']}/spawn_points.py with {len(spawn_points)} entries")
print(f"- {output_dirs['roaming_locations']}/roaming_locations.py with {len(roaming_locations)} entries")
print(f"- {output_dirs['contaminated_areas_xml']}/contaminated_areas.xml with {len(contaminated_positions)} positions")
