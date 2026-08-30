import json
import random

# Load 2D building footprints
with open('bkc_buildings.geojson', 'r') as f:
    raw_data = json.load(f)

# Append prototype building footprint
prototype_building = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[72.8648, 19.0632], [72.8654, 19.0632], [72.8654, 19.0637], [72.8648, 19.0637], [72.8648, 19.0632]]]
    },
    "properties": {
        "name": "Prototype ULPIN Tower",
        "building:levels": "6"
    }
}
raw_data['features'].append(prototype_building)

synthetic_features = []
sample_owners = [
    "Ramesh Sharma", "Priya Patel", "Amit Verma", 
    "Neha Gupta", "Vikram Shah", "Ananya Roy", 
    "Rajesh Mehta", "Sunita Deshmukh"
]

for building_idx, feature in enumerate(raw_data['features']):
    geom_type = feature['geometry']['type']
    if geom_type not in ['Polygon', 'MultiPolygon']:
        continue

    props = feature.get('properties', {})
    building_name = props.get('name', f"BKC Block {building_idx + 1}")
    bldg_id = f"BKC-BLDG-{building_idx + 1000}"
    
    osm_levels = props.get('building:levels')
    if osm_levels and str(osm_levels).isdigit():
        total_floors = int(osm_levels)
    else:
        total_floors = random.randint(6, 15)

    floor_height_meters = 3.5 

    for floor in range(1, total_floors + 1):
        base_h = (floor - 1) * floor_height_meters
        top_h = floor * floor_height_meters
        
        is_paid = random.random() > 0.30
        ulpin_code = f"27-BKC-{building_idx+1000:04d}-F{floor:02d}-U{floor}01"

        floor_feature = {
            "type": "Feature",
            "geometry": feature['geometry'],
            "properties": {
                "ulpin": ulpin_code,
                "building_id": bldg_id,
                "building_name": building_name,
                "floor": floor,
                "total_floors": total_floors,
                "base_height": base_h,
                "height": top_h,
                "owner": random.choice(sample_owners),
                "tax_status": "Paid" if is_paid else "Default",
                "tax_color": "#2ECC71" if is_paid else "#E74C3C",
                "default_color": "#3A3A3A",
                "land_type": "Commercial" if floor <= 3 else "Residential"
            }
        }
        synthetic_features.append(floor_feature)

output_geojson = {
    "type": "FeatureCollection",
    "features": synthetic_features
}

with open('bkc_3d_ulpin.geojson', 'w') as f:
    json.dump(output_geojson, f, indent=2)

print(f"Generated bkc_3d_ulpin.geojson with {len(synthetic_features)} floor records.")