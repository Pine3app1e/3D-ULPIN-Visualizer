import json
import qrcode
import os

# Create the output directory
os.makedirs("qrcodes", exist_ok=True)

BASE_URL = "https://pine3app1e.github.io/3D-ULPIN-Visualizer/?ulpin="

with open("sobo_3d_ulpin.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

seen_ulpins = set()
count = 0

print("Generating QR code images...")

for feature in data["features"]:
    ulpin = feature["properties"]["ulpin"]
    if ulpin not in seen_ulpins:
        seen_ulpins.add(ulpin)
        
        target_url = BASE_URL + ulpin
        img = qrcode.make(target_url)
        
        # Save file with safe filename
        safe_filename = ulpin.replace("/", "_").replace("\\", "_")
        img.save(f"qrcodes/{safe_filename}.png")
        count += 1
        
        # Limit to first 100 for fast testing if needed, or let it process all
        if count % 1000 == 0:
            print(f"Generated {count} QR codes...")

print(f"Done! Successfully generated {count} QR codes in the 'qrcodes/' folder.")