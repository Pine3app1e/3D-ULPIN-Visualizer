import pandas as pd
import json

# Load the real cleaned dataset
df = pd.read_csv('SoBo_3D_Master_Backend_Ready.csv')

features = []

for idx, row in df.iterrows():
    base_ulpin = str(row['BASE_ULPIN_ID'])
    lat = float(row['LATITUDE'])
    lng = float(row['LONGITUDE'])
    total_floors = int(row['FINAL_FLOORS']) if pd.notnull(row['FINAL_FLOORS']) and row['FINAL_FLOORS'] > 0 else 10
    
    # Calculate height per floor based on total structural height
    struct_height = float(row['STRUCTURAL_HEIGHT_M']) if pd.notnull(row['STRUCTURAL_HEIGHT_M']) else total_floors * 3.5
    floor_height = struct_height / total_floors if total_floors > 0 else 3.5
    
    # Generate a small square footprint centered around the building coordinate
    delta = 0.00018  # approximate size of footprint in degrees
    polygon_coords = [[
        [lng - delta, lat - delta],
        [lng + delta, lat - delta],
        [lng + delta, lat + delta],
        [lng - delta, lat + delta],
        [lng - delta, lat - delta]
    ]]
    
    bldg_id = f"bldg_{idx}"
    
    # Generate each floor slice vertically
    for floor_num in range(1, total_floors + 1):
        floor_ulpin = f"{base_ulpin}-FL{floor_num:02d}"
        
        base_h = (floor_num - 1) * floor_height
        top_h = floor_num * floor_height
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": polygon_coords
            },
            "properties": {
                "building_id": bldg_id,
                "ulpin": floor_ulpin,
                "base_ulpin": base_ulpin,
                "rera_id": str(row['RERA_ID']) if pd.notnull(row['RERA_ID']) else "N/A",
                "project_name": str(row['PROJECT_NAME']) if pd.notnull(row['PROJECT_NAME']) else "Unknown Project",
                "promoter_name": str(row['PROMOTER_NAME']) if pd.notnull(row['PROMOTER_NAME']) else "Private Developer",
                "district": str(row['DISTRICT']),
                "pin_code": str(row['LOCATION_PIN_CODE']),
                "floor": floor_num,
                "total_floors": total_floors,
                "base_height": base_h,
                "height": top_h,
                "default_color": "#3A3A3A",
                "tax_status": "Paid" if (idx + floor_num) % 4 != 0 else "Flagged",
                "tax_color": "#2ECC71" if (idx + floor_num) % 4 != 0 else "#E74C3C"
            }
        }
        features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

with open("sobo_3d_ulpin.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, indent=2)

print(f"Successfully generated sobo_3d_ulpin.geojson with {len(features)} 3D floor units.")