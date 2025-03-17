# generate_contaminated_areas_xml.py
from spawn_points import spawn_points  # Import spawn points from spawn_points.py

# Keywords to filter contaminated areas
keywords = ["Industrial", "Military", "Antenna", "Mine", "Island", "Transformer"]

# Filter and format positions
contaminated_positions = []
for location in spawn_points:
    name = location["Name"]
    # Check if any keyword is in the name (case-insensitive)
    if any(keyword.lower() in name.lower() for keyword in keywords):
        x_coord = location["Positions"][0][0]  # First number (X)
        z_coord = location["Positions"][0][2]  # Third number (Z)
        # Format as requested with 6 decimal places
        pos_line = f'  <pos x="{x_coord:.6f}" z="{z_coord:.6f}" />'
        contaminated_positions.append(pos_line)

# Write to XML file
with open("contaminated_areas.xml", "w") as f:
    f.write('<event name="StaticContaminatedArea">\n')
    for line in contaminated_positions:
        f.write(line + "\n")
    f.write('</event>\n')

print(f"Generated contaminated_areas.xml with {len(contaminated_positions)} contaminated positions.")