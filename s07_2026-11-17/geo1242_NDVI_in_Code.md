# geo1242 NDVI in code: from our file to any Sentinel-2 scene

**Tool:** Jupyter notebook `geo1242_NDVI_in_Code.ipynb` (internet access needed) · **Time:** about 2 h in class + 1–2 h homework · **Slides:** `geo1220_RS_Fundamentals.pdf` (parts *Sentinel-2* and *Indices*) · **Builds on:** geo1221 (composites, signatures in QGIS) · **Data:** `data/rs_kamp_lintfort/`

In QGIS (geo1241) the NDVI comes from the Raster Calculator. Here you compute it in Python, then search the Sentinel-2 archive yourself (STAC), read only your area from the cloud-optimised GeoTIFFs (COGs) over HTTP, mask clouds with the scene classification layer (SCL), map the change between two dates and build the NDVI season of one field.

## Files
| File | Content |
|---|---|
| `geo1242_NDVI_in_Code.ipynb` | the workbook: read the text cells, fill in the cells marked `# YOUR CODE HERE` |
| `data/rs_kamp_lintfort/s2_kamp_lintfort.tif` | Sentinel-2 L2A, 25 June 2026, bands B02 B03 B04 B05 B08 B11, reflectance × 10 000 |
| `data/rs_kamp_lintfort/worldcover_kamp_lintfort.tif` | ESA WorldCover 2021, same 10 m grid |
| `data/rs_kamp_lintfort/lwk_parcels_kamp_lintfort.gpkg` | agricultural parcels with their crop 2026 (`CODE_TXT`), `ID` as text |

Your results go into `geo1242_out/` next to the notebook.

**Short version (self-study, B.Sc. level):** if your notebook is titled *short version*, it contains only §1 (task 1 below), with the code given: read, predict, run, and compare with your QGIS result from geo1241. Nothing to hand in; tasks 2–7 and *Hand in* do not apply.

## Tasks
1. **NDVI from our file (§1):** `nd(a, b)` with NaN for 0/0, NDVI map, GeoTIFF (float32, nodata NaN), mean per WorldCover class; NDRE and NDMI.
2. **STAC (§2):** search tile 32ULC on Earth Search, all scenes March–October 2026 with paging; tile cloud cover over time; remove reprocessed duplicates.
3. **COG (§3):** `read_clip`: one window of one band over HTTP, the 20 m SCL on the 10 m grid; check against our file.
4. **Two dates (§4):** SCL mask, NDVI 15 September, change map, change per crop (parcels shrunk by 10 m).
5. **Season (§5, pairs, finish at home):** the NDVI of one field on every usable scene; read the farming year from the curve.
6. **Stretch (§6):** the same idea with a web service: DGM1 window via the NRW WCS.
7. **Optional (§7):** the same index from a drone: Mavic 3M over Frohnenbruchhof (25 Oct 2024) against Sentinel-2 two days earlier; what one 10 m pixel hides. Data: hub shared folder `drone_m3m/`, laptops from Moodle into `data/drone_m3m/`.

## Hints
- STAC `bbox` is always in degrees (longitude, latitude), whatever the CRS of the data.
- Filter by tile (`grid:code`): our area lies in two tiles.
- Tile cloud cover is for 110 km × 110 km: decide per pixel with the SCL (keep 4, 5, 6).
- NDVI is a ratio: the scale factor 10 000 cancels; for NDVI 0/0 must be NaN, not 0.
- Identifiers (parcel `ID`) are text.

## Hand in
Upload the notebook (with outputs) and `geo1242_out/season_<ID>.png` with your answers to the questions of §5 to Moodle.

## Sources
- Contains modified Copernicus Sentinel data 2026; Earth Search (Element 84), Sentinel-2 COGs on AWS Open Data.
- ESA WorldCover 2021 v200, CC BY 4.0. Parcels: Landwirtschaftskammer NRW, dl-de/by-2-0, "Land NRW (2026)". DGM1: Geobasis NRW, dl-de/zero-2-0.
- Further reading: SentiWiki (Sentinel-2 bands, levels, SCL), stacspec.org, cogeo.org, rasterio documentation, OGC WCS 2.0, NASA Earth Observatory *Measuring Vegetation*, EO College.
