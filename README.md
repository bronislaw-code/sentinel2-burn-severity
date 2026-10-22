# Sentinel-2 Burn Severity Analysis

Processing pipeline for computing **burn severity** from Sentinel-2 L2A imagery
using the **differenced Normalized Burn Ratio (dNBR)** index.

## Case Study

- **Location:** Southern Europe (wildfire, summer 2021)
- **Pre-fire image:** 2021-07-28
- **Post-fire image:** 2021-08-27
- **Sensor:** Sentinel-2 MSI, Level-2A (bottom-of-atmosphere reflectance)

## Workflow

1. Load pre- and post-fire bands (B04, B08, B12)
2. Compute NBR, dNBR, and NDVI
3. Classify burn severity using USGS thresholds
4. Export GeoTIFF, GeoJSON, and PNG products
5. Vectorize burn perimeters for GIS use

## Project Structure

```
sentinel2-burn-severity/
├── data/
│   ├── pre_fire/          # Sentinel-2 bands (pre-fire)
│   └── post_fire/         # Sentinel-2 bands (post-fire)
├── notebooks/
│   └── burn_severity.ipynb
├── src/
│   ├── __init__.py
│   ├── indices.py         # NBR, dNBR, NDVI, severity classification
│   └── visualize.py       # PIL-based visualization helpers
├── outputs/               # Generated products (gitignored)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Data Acquisition

Imagery is downloaded manually from the **Copernicus Data Space Ecosystem**.

### Step-by-step

1. **Go to** [Copernicus Browser](https://browser.dataspace.copernicus.eu/)
   and create a free account if you don't have one.

2. **Search for imagery:**
   - Navigate to the area affected by the wildfire.
   - In the left panel, set the following filters:
     - **Data source:** `Sentinel-2` → `L2A` (Level-2A, atmospheric correction applied)
     - **Date range:** choose a cloud-free date **before** the fire (e.g. `2021-07-25` to `2021-07-31`)
     - **Cloud coverage:** ≤ 20% (lower is better)

3. **Select a scene** with minimal cloud cover over the fire area and click
   **Download** → **Custom** (or "Download bands").

4. **Choose the following bands:**
   | Band | Name | Wavelength | Resolution | Purpose |
   |------|------|------------|------------|---------|
   | B04 | Red | 665 nm | 10 m | NDVI |
   | B08 | NIR | 842 nm | 10 m | NBR, NDVI |
   | B11 | SWIR | 1610 nm | 20 m | NBR2 |
   | B12 | SWIR | 2190 nm | 20 m | NBR |

   > **Note:** If your download tool offers a resampling option, choose **10 m**
   > for all bands so they share the same grid. Otherwise, resample B12 in
   > Python before computing indices.

5. **Repeat** steps 2–4 for a **post-fire** date (e.g. `2021-08-25` to
   `2021-08-31`), ideally with similar viewing geometry.

6. **Place the files** in the project directory:
   ```
   data/pre_fire/   ← B04, B08, B12 GeoTIFFs (before the fire)
   data/post_fire/  ← B04, B08, B12 GeoTIFFs (after the fire)
   ```

### Alternative sources

- [USGS EarthExplorer](https://earthexplorer.usgs.gov/) — same Sentinel-2 data, different interface
- [sentinelhub-py](https://github.com/sentinel-hub/sentinelhub-py) — programmatic access (requires API key)

## Installation

```bash
git clone https://github.com/bronislaw-code/sentinel2-burn-severity.git
cd sentinel2-burn-severity

python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

## Usage

Open the notebook and run all cells:

```bash
jupyter notebook notebooks/burn_severity.ipynb
```

Or import the modules directly in your own scripts:

```python
from src.indices import nbr, dnbr, ndvi, classify_severity
from src.visualize import severity_to_rgb, array_to_rgb
```

## Output Products

| File | Format | Description |
|------|--------|-------------|
| `dnbr.tif` | GeoTIFF (float32) | Continuous dNBR values |
| `dnbr2.tif` | GeoTIFF (float32) | NBR2 change (soil moisture / char) |
| `severity.tif` | GeoTIFF (uint8) | Classified severity (0–4) |
| `severity_rgb.tif` | GeoTIFF (uint8, RGB) | Color-coded severity map |
| `dndvi.tif` | GeoTIFF (float32) | NDVI change (vegetation loss) |
| `burn_severity.geojson` | GeoJSON | Vector polygons of burned areas |
| `overview.png` | PNG | dNBR + Severity + dNDVI composite |

### Severity Classes (USGS)

| Code | Class | dNBR Range | Color |
|------|-------|------------|-------|
| 0 | Unburned | < 0.10 | 🟢 Green |
| 1 | Low | 0.10 – 0.27 | 🟡 Yellow |
| 2 | Moderate | 0.27 – 0.44 | 🟠 Orange |
| 3 | High | 0.44 – 0.66 | 🔴 Red |
| 4 | Very High | ≥ 0.66 | ⬛ Dark Red |

## References

- Key, C.H. & Benson, N.C. (2006). *Landscape Assessment: Ground Measure of
  Severity, the Composite Burn Index; and Remote Sensing of Severity, the
  Normalized Burn Ratio.* FIREMON.
- Copernicus Data Space Ecosystem: https://dataspace.copernicus.eu/

## License

MIT