# generate_spawns.py
import json
from cities import cities  # Import cities from cities.py

# Extract and transform locations
output_locations = []
for loc in cities["Locations"]:
    transformed_loc = {
        "Name": loc["Name"],
        "Positions": [loc["Position"]],  # Wrap position in a list
        "UseCooldown": 1
    }
    output_locations.append(transformed_loc)

# Write to spawn_points.py
with open("spawn_points.py", "w") as f:
    f.write("# Spawn points generated from Raman City Locations\n")
    f.write("spawn_points = [\n")
    for loc in output_locations:
        # Format each location as a string with proper indentation
        loc_str = json.dumps(loc, indent=4)
        # Remove the outer curly braces and adjust indentation
        loc_str = loc_str[1:-1].strip()
        f.write("    {\n")
        f.write(f"{loc_str}\n")
        f.write("    },\n")
    f.write("]\n")

print(f"Generated spawn_points.py with {len(output_locations)} spawn points.")