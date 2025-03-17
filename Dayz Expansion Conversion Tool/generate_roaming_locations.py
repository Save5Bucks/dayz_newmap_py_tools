# generate_roaming_locations.py
import json
from cities import cities  # Import cities from cities.py

# Template structure for the output
template = {
    "m_Version": 1,
    "RoamingLocations": [],
    "ExcludedRoamingBuildings": [
        "Land_CementWorks_Hall2_Grey",
        "Land_Factory_Small",
        "Land_House_1W09",
        "Land_House_2W03",
        "Land_HouseBlock_1F4",
        "Land_Boathouse",
        "Land_Mine_Building",
        "Land_Shed_W2",
        "Land_Tenement_Big"
    ],
    "NoGoAreas": []
}

# Transform locations
roaming_locations = []
for loc in cities["Locations"]:
    # Determine radius based on Type
    radius = 500.0 if loc["Type"] == "CityCap" else 100.0
    # Create roaming location entry
    roaming_loc = {
        "Name": loc["Name"],
        "Position": loc["Position"],
        "Radius": radius,
        "Type": loc["Type"] if loc["Type"] else "Local",  # Default to "Local" if Type is empty
        "Enabled": 1
    }
    roaming_locations.append(roaming_loc)

# Fill the template with roaming locations
template["RoamingLocations"] = roaming_locations

# Write to roaming_locations.py
with open("roaming_locations.py", "w") as f:
    f.write("# Roaming locations generated from Raman City Locations\n")
    f.write("roaming_locations = ")
    f.write(json.dumps(template, indent=4))
    f.write("\n")

print(f"Generated roaming_locations.py with {len(roaming_locations)} roaming locations.")