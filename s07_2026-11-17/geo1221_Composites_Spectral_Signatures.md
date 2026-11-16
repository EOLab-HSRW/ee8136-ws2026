# geo1221 Colour composites and spectral signatures (Sentinel-2)

**Tool:** QGIS (Layer Properties → Symbology, Identify Features, optional STAC search in the Data Source Manager) · **Time:** demo 15 min + exercise 25 min · **Slides:** `geo1220_RS_Fundamentals.pdf` · **Next:** geo1241 (NDVI), geo1281 (classification)

A satellite image is not a photo: it is a stack of measurements, one per wavelength band. Your screen
can show only three of them at a time (red, green, blue). Which three you choose decides what you
see. In this activity you look at the same Sentinel-2 scene in three combinations and measure the
"colour" of five surfaces in all six bands: their **spectral signatures**.

## Files
| File | Use |
|---|---|
| `data/rs_kamp_lintfort/s2_kamp_lintfort.tif` | Sentinel-2 L2A, 25 June 2026, Kamp-Lintfort / Hoerstgen, 6 bands, 10 m, EPSG:25832 |
| `data/rs_kamp_lintfort/s2_kamp_lintfort_scl.tif` | Scene Classification Layer of the same scene (clouds, shadows, water, vegetation, …) |
| `data/rs_kamp_lintfort/s2_kamp_lintfort.json` | scene id, date, band list, licence |

Values are **surface reflectance × 10 000** (0 = no data): 2 000 means 20 % of the sunlight is
reflected. The bands in the file:

| Band in QGIS | Sentinel-2 band | Wavelength (centre) | Native resolution |
|---|---|---|---|
| 1 | B02 blue | 490 nm | 10 m |
| 2 | B03 green | 560 nm | 10 m |
| 3 | B04 red | 665 nm | 10 m |
| 4 | B05 red edge | 705 nm | 20 m (resampled to 10 m) |
| 5 | B08 near infrared (NIR) | 842 nm | 10 m |
| 6 | B11 shortwave infrared (SWIR) | 1610 nm | 20 m (resampled to 10 m) |

Contains modified Copernicus Sentinel data 2026.

## Guided demo
1. **Load** `s2_kamp_lintfort.tif` (drag it from the Browser into the map). QGIS shows bands 1-2-3
   as red-green-blue: blue light appears red on screen. Not what we want.
2. **True colour.** *Layer Properties → Symbology*, *Render type* `Multiband color`: *Red band*
   `Band 3`, *Green band* `Band 2`, *Blue band* `Band 1` (QGIS shows the band names stored in the file,
   e.g. `Band 3: B04 red`; in the literature this composite is Sentinel-2 B4-B3-B2). *Min / Max Value Settings* →
   `Cumulative count cut` 2–98 %, *Apply*. Find the campus, the lakes in the east and the
   forests (overview map on the slide "Our example").  The colours depend on this stretch: the same
   field looks different in another scene or clip. Zoom in until you see the 10 m pixels.
3. **False colour (colour infrared).** Red `Band 5` (NIR), green `Band 3` (red), blue `Band 2` (green)
   (Sentinel-2 B8-B4-B3).
   **Predict first:** healthy plants reflect NIR strongly and absorb red. What colour will a forest
   be? A wheat field? A roof? Water?
4. **One layer per composite.** Duplicate the layer (*right-click → Duplicate Layer*), so you keep
   both styles, and rename the layers `true colour` and `false colour`. Save the project as
   `rs_kamp_lintfort.qgz` in your session folder: geo1241 and geo1281 continue in it.
5. **Identify a pixel.** *Identify Features* tool (`Ctrl+Shift+I`), click into a forest: the panel shows
   the values of all six bands. That list of numbers is the spectral signature of that pixel. The values
   are reflectance × 10 000: 4203 means 0.42 = 42 % of the light is reflected.

## Exercise (pairs)
1. **Third composite.** Red `Band 6` (SWIR), green `Band 5` (NIR), blue `Band 3` (red) (Sentinel-2 B11-B8-B4). Which surfaces
   look different from the false colour composite? Look at the town, the fields and the lakes.
2. **Spectral signatures.** Measure **three pixels each** of five surfaces: water (a lake),
   forest, grassland (meadow or pasture), a crop field, built-up (roofs, roads). Enter the six values
   in the template `data/geo1221/geo1221_signatures.xlsx` (yellow cells, the values as QGIS shows
   them; save your copy as `geo1221_signatures_mine.xlsx`): it computes the mean reflectance of each
   surface and draws the signatures (x = band, y = reflectance). Which band separates vegetation from everything else best? Which
   separates water from everything else? Which two surfaces are hardest to tell apart?
3. **Fields are not all the same.** Find three fields with clearly different colours in the false
   colour composite. Measure them. What could be growing there in late June (or has been harvested)?
4. **Clouds?** Load `s2_kamp_lintfort_scl.tif`, style it `Paletted/Unique values` (*Classify*).
   The classes: 4 vegetation, 5 not vegetated, 6 water, 7 unclassified, 2 dark area, 3 cloud shadow,
   8/9 cloud, 10 thin cirrus. Are there clouds in this scene? Where would you need this layer?
5. **Resolution.** Zoom to the Green Fab Lab south of the campus. How many pixels does the building
   cover? How many of them are pure roof? What could you map with Sentinel-2 here, and what not?
   (Compare: the drone of the field day flew at 25 m, its multispectral pixels are about 1 cm; slide
   "10 m pixels at the Green Fab Lab".)

## Optional: find a Sentinel-2 scene yourself (STAC, QGIS 3.40 or newer; checked in QGIS 3.44)
1. *Browser → STAC → right-click → New STAC Connection…*: name `Earth Search`, URL
   `https://earth-search.aws.element84.com/v1`, *OK*. The Browser now lists the collections, but it
   cannot search.
2. *Layer → Data Source Manager* (`Ctrl+L`) → *STAC* → connection `Earth Search` → *Connect* →
   *Filters…*: tick *Spatial Extent* and press the extent button (it takes the current map canvas, so load
   `s2_kamp_lintfort.tif` first), tick *Temporal Extent* (a few weeks, e.g. `2026-06-01 00:00:00` to
   `2026-06-30 23:59:59`), tick *Only search within specific collections* → *Deselect all* → `Sentinel-2
   Level-2A`, *OK*. There is no cloud-cover filter: judge by the thumbnails.
3. Our area lies on the border of two UTM zones: you get tiles `32ULC` and `31UGT`. Select an item of
   `32ULC` and *Add* one asset (e.g. `red` or `visual`): QGIS streams the cloud-optimized GeoTIFF over the
   internet, only the part you look at.
Which date had the fewest clouds over Kamp-Lintfort? Why is the tile cloud cover not the same as the
cloud cover over *your* area?

## Check yourself
- Why does a forest look red in the false colour composite?
- Why do you have to *choose* three bands, and why is there no "correct" colour?
- The scene has 6 bands, Sentinel-2 has 13. What is lost by leaving out the others?

## Tutorials
- QGIS user manual, raster symbology (Multiband color): https://docs.qgis.org/latest/en/docs/user_manual/working_with_raster/raster_properties.html
- Copernicus Sentinel-2 user guide (bands, resolutions): https://sentiwiki.copernicus.eu/web/s2-mission
- Earth Search STAC API: https://earth-search.aws.element84.com/v1
