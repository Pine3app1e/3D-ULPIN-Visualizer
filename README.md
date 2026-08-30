# 3D ULPIN Visualizer (BKC Core)

> **Extending 2D Bhu-Aadhaar into Interactive 3D Multi-Floor Spatial Models**

---

## 🏢 The Challenge: 2D Bhu-Aadhaar vs 3D ULPIN

Currently, the **Bhu-Aadhaar (ULPIN)** system maps land parcels strictly in 2D. While effective for horizontal land distribution, this 2D approach falls short in dense urban environments like the Bandra Kurla Complex (BKC), where property ownership is stacked vertically in multi-story high-rises. 

To effectively manage property taxes, ownership disputes, and unit-level spatial data, a high-fidelity 3D visualization system is required. This project bridges that gap by extruding 2D footprints into interactive, floor-separated 3D assets, allowing administrators to inspect properties unit-by-unit.

---

## 🛠️ Tech Stack

* **Map Engine:** MapLibre GL JS *(Open-source, WebGL-based vector map rendering)*
* **Data Processing:** Python *(JSON handling, synthetic data generation)*
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Deployment:** Git & GitHub Pages

---

## ⚙️ How We Built It: Step-by-Step

### 1. Data Processing & 3D Extrusion
We started with a base dataset (`bkc_buildings.geojson`) containing 2D polygon footprints of BKC buildings. Since real-world vertical property data is restricted, we wrote a custom Python script (`generate_3d_ulpin.py`) to process these footprints into 3D structures.
* **Floor Generation:** The script iterates through the 2D footprints and generates a dynamic number of floors (between 6 and 15) for each building.
* **Elevation Math:** Each floor is assigned a `base_height` and a `height` (using a standard 3.5 meters per floor) to stack them perfectly on top of each other.
* **Data Enrichment:** During generation, each specific floor slice is assigned synthetic metadata, including a unique 14-digit ULPIN code, a mock owner name, property type (Commercial/Residential), and a randomized Tax Compliance status. The output is saved as `bkc_3d_ulpin.geojson`.

### 2. Map Engine Implementation
We utilized **MapLibre GL JS** to render the frontend.
* The map initializes centered on BKC with a high pitch (tilt) and a dark-mode basemap to ensure the data stands out.
* We loaded the `bkc_3d_ulpin.geojson` file as a vector data source and applied a `fill-extrusion` layer.
* MapLibre reads the `base_height` and `height` properties from our GeoJSON to automatically draw the 3D blocks.

### 3. Dynamic Floor Explosion Mechanics
To allow users to inspect overlapping vertical units, we engineered a single-building explosion effect:
* When a user clicks a building, the map captures the specific `building_id` of the clicked unit.
* A JavaScript animation loop (`requestAnimationFrame`) gradually increases a numeric "gap" value.
* We dynamically update MapLibre's paint properties using a conditional `case` statement: if the rendered block's `building_id` matches the clicked ID, we add the gap value multiplied by the block's floor number to its base and top heights. This smoothly separates the floors of the selected building while leaving surrounding structures intact.
* Simultaneously, the camera performs a `flyTo` animation, adjusting the zoom dynamically based on the floor height to perfectly frame the expanded building.

### 4. Color Scheme & Global Tax View
To make the data immediately actionable, we implemented a dual-mode color scheme:
* **Default View:** All buildings are rendered in a sleek, neutral dark gray (`#3A3A3A`) for standard spatial viewing.
* **Global Tax View:** By checking the UI toggle, the map dynamically switches the `fill-extrusion-color` property to read from the `tax_color` attribute injected by our Python script. Paid units instantly turn green (`#2ECC71`), while defaulting units turn red (`#E74C3C`), providing an immediate, city-wide heatmap of tax compliance.

---

## ✨ Key Frontend Features

* **Unit-Level Interactivity:** Hovering over the map changes the cursor to indicate clickable 3D units.
* **Targeted Vertical Explosion:** Clicking a unit seamlessly separates the floors of that specific building for unobstructed internal viewing.
* **Dynamic Info Panel:** A responsive right-side UI panel slides in upon selection, displaying the specific floor's ULPIN, Owner, Land Type, and Tax Status.
* **Live Coordinate Tracking:** A bottom-left HUD displays real-time Latitude and Longitude based on mouse movement.
* **Smooth Camera Transitions:** Clicking a unit automatically adjusts the camera pitch, bearing, and padding to center the UI without overlapping the info panel.

---

## 🚀 Future Scope

This visualizer represents the core foundation of a 3D spatial property system. We are actively developing additional features, including advanced search by ULPIN, real-time database integrations for live property mutation tracking, and broader geographical coverage beyond the BKC prototype zone.