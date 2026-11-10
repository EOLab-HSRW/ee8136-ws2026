# geo0721 Vector analysis in QGIS: climate stations, counties and drinking water protection zones

**Tool:** QGIS Processing Toolbox (Buffer, Difference, Intersection, Dissolve, Join attributes by location, Count points in polygon), Field Calculator · **Time:** guided 25 min + exercise 25 min (+ WFS 10 min) · **Slides:** `geo0720_Vector_Analysis.pdf` · **Twin notebook:** geo0722 (the same questions with GeoPandas)

Two questions about weather and water in North Rhine-Westphalia:

1. **How well do the DWD climate stations cover NRW?** Stations per county, and the part of each county that is more than 20 km from the nearest active station.
2. **How much of each county is drinking water protection zone,** and which climate stations stand inside a zone?

You need four operations from the slides: **spatial join**, **buffer**, **dissolve**, **overlay** (difference, intersection). Work in pairs, one laptop, swap the mouse after each part.

## Files
| File | Use |
|---|---|
| `data/geo0721/dwd_kl_stations_nrw_active.csv` (+ `.csvt`) | the 42 active DWD climate stations in NRW (snapshot of the station list, made like your geo0647 file); your own CSV from that session works as well |
| `data/geo0721/wsg_nrw.gpkg` | all drinking water and spa protection zones of NRW (2 522 zones) |
| `../data/dvg1_EPSG25832_Shape/dvg1krs_nw.shp` | the 53 counties from DVG1: 31 *Kreise* and 22 independent cities (*kreisfreie Städte*); your download from geo0061 |
| `geo0721_Vector_Analysis_QGIS_checkpoint.qgz` + `data/geo0721/geo0721_checkpoint.gpkg` | **checkpoint after Part 1** (stations, counties with `n_stations`, 20 km cover, gaps with `gap_pct`): open it if you fall behind, then continue with Part 2 |

Save everything you produce in **`vector_analysis_mine.gpkg`** in your session folder (one GeoPackage, one layer per step: in every Processing dialog choose *Save to GeoPackage…* and type a layer name).

**Sources and licences:** stations: Deutscher Wetterdienst (DWD), CC BY 4.0; counties: © Geobasis NRW, dl-de/zero-2-0; protection zones: Land NRW (opengeodata.nrw.de, *Trinkwasser- und Heilquellenschutzgebiete NRW*), dl-de/zero-2-0.

## Part 1 – Stations and counties (guided, 25 min)
1. **New project, CRS first.** *Project ▸ New*, then *Project ▸ Properties ▸ CRS*: EPSG:25832. Save the project as `vector_analysis_mine.qgz` in your session folder.
2. **Counties.** Drag `dvg1krs_nw.shp` from the *Browser* (folder `data/dvg1_EPSG25832_Shape` of your course folder) into the map. Open the attribute table: `GN` is the name, `KN` the official key (text).
3. **County areas.** *Open Field Calculator* on the counties: *Create a new field* `area_km2`, type *Decimal number (real)*, expression
   ```
   area(@geometry) / 1e6
   ```
   `area(@geometry)` is the **planar** area in the layer CRS (m², here UTM). `$area` would use the ellipsoid set in the project properties; both differ by about 0.1 % here. Leave edit mode and save.
4. **Stations.** *Layer ▸ Add Layer ▸ Add Delimited Text Layer…*: file `data/geo0721/dwd_kl_stations_nrw_active.csv`, *Custom delimiters* `;`, *Point coordinates* X field `lon`, Y field `lat`, *Geometry CRS* **EPSG:4326**. Check in the attribute table that `station_id` keeps its leading zeros (`00390`).
5. **The pitfall first.** *Processing ▸ Toolbox ▸ Vector geometry ▸ Buffer* with the **station layer as it is** (EPSG:4326). Look at the unit next to *Distance*: **degrees**. Enter `0.2`, run, output *temporary layer*. Measure one buffer with the *Measure Line* tool, east–west and north–south. Is it a circle? Why not? Delete the layer.
6. **Reproject.** *Vector general ▸ Reproject layer*: input stations, target CRS EPSG:25832, output layer `stations` in `vector_analysis_mine.gpkg`. Remove the CSV layer from the project.
7. **Spatial join: count.** *Vector analysis ▸ Count points in polygon*: polygons `dvg1krs_nw`, points `stations`, count field `n_stations`, output layer `counties_stations`. Open the attribute table and sort by `n_stations`.
8. **Buffer in metres, dissolved.** *Vector geometry ▸ Buffer*: input `stations`, distance **20** *kilometers* (now the unit list offers metres and kilometres), **tick *Dissolve result***, output layer `covered_20km`.
9. **Overlay: difference.** *Vector overlay ▸ Difference*: input `counties_stations`, overlay `covered_20km`, output layer `gaps`. What remains are the parts of each county *outside* the covered area; the attributes of the counties are kept.
10. **Share per county.** Field Calculator on `gaps`: new field `gap_pct` (real), expression
    ```
    100 * area(@geometry) / 1e6 / "area_km2"
    ```
    Symbolise `gaps` with *Graduated* on `gap_pct` (*Reds*), stations on top.

## Part 2 – Drinking water protection (exercise, 25 min)
11. *(Fallen behind? Open `geo0721_Vector_Analysis_QGIS_checkpoint.qgz` now, save it under your own name with *Project ▸ Save As…* `vector_analysis_mine.qgz`.)* Add `data/geo0721/wsg_nrw.gpkg`. Look at the attribute table: `prot_type` T (drinking water) or S (spa), `areastatus` F (designated) or P (planned), `wsg_zone` 1, 2, 3, 3A, … (zone 1: well field, zone 2: 50-day line, zone 3: catchment).
12. **Select.** *Vector selection ▸ Extract by expression*:
    ```
    "areastatus" = 'F' AND "prot_type" = 'T'
    ```
    output layer `wsg_drinking`. How many zones?
13. **Dissolve.** *Vector geometry ▸ Dissolve* (no field selected), output layer `wsg_dissolved`. Compare the summed area of `wsg_drinking` (*Basic statistics for fields* on a field `a` = `area(@geometry)`) with the area of `wsg_dissolved`. Why are they different? Open the attribute table of `wsg_dissolved`: one feature, but with the attributes of *one* of the zones. After a dissolve without a field these values mean nothing.
14. **Overlay: intersection.** *Vector overlay ▸ Intersection*: input `dvg1krs_nw` (with `area_km2`), overlay `wsg_dissolved`, output `wsg_by_county`. Field Calculator: `wsg_pct` = `100 * area(@geometry) / 1e6 / "area_km2"`. Which three counties protect the largest share of their area?
15. **Stations in a zone.** *Vector general ▸ Join attributes by location*: features `stations`, compare with `wsg_drinking`, predicate *are within*, fields `name`, `wsg_zone`, tick **Discard records which could not be joined**, *Joined field prefix* `wsg_` (without it the zone name arrives as `name_2`), output `stations_in_wsg`. Which stations, which zones?

16. **Nearest station (optional).** *Vector geometry ▸ Dissolve* on `wsg_drinking` with *Dissolve field(s)* `gebiet_id` and `name`: one polygon per protection area, output `wsg_areas`. Then *Vector general ▸ Join attributes by nearest*: input `wsg_areas`, input layer 2 `stations`, fields `name`, *Maximum nearest neighbors* 1, *Joined field prefix* `station_`, output `wsg_nearest_station`. The field `distance` is in metres (layer CRS). How many areas are more than 20 km from the nearest active station?

## Part 3 – Counties from a WFS (10 min, geo0921 Part C)
17. Open your copy of `geo0921_NRW_Web_Services.md` (session with the web services) and do **Part C** steps 10–12: load the WFS connections and add the layer *Kreise* of *NW Topographische Sonderkarten; Verwaltungsgrenzen*. This time you may zoom out: there are only 53 features.
18. Run step 7 (*Count points in polygon*) with the WFS layer instead of the shapefile. Same counts? Compare the attribute names and the number of vertices of one county (*Identify* ▸ *Derived*).

## Exercise (pairs)
1. Which counties have **no** active station? Which of them are still fully covered by stations in neighbouring counties (`gap_pct` = 0)?
2. NRW as a whole: what share of the area is more than 20 km from an active station? (Hint: *Basic statistics for fields* on `area(@geometry)` of `gaps`, NRW = 34 097 km².) Repeat with 10 km and 30 km.
3. Which counties have more than 20 % drinking water protection zone **and** no station? Why could that matter for estimating groundwater recharge?
4. Spatial join or overlay: which steps kept the original geometries, which cut them? Write the step numbers. Which operation is the nearest join of step 16?

## Check yourself
- Why must the buffers be dissolved before you compute the covered area?
- What does the unit next to the *Distance* field of the *Buffer* tool tell you about the input layer?
- After *Join attributes by location* a station appears twice. What happened?

## Tutorials
- QGIS user manual, Vector overlay: https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html
- QGIS user manual, Vector geometry (Buffer, Dissolve): https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html
- QGIS Training Manual, Vector analysis: https://docs.qgis.org/latest/en/docs/training_manual/vector_analysis/index.html
- Geocomputation with R/Python: Lovelace, R., Nowosad, J., Muenchow, J. (2025): *Geocomputation with Python*, chapter 3 "Spatial data operations", https://py.geocompx.org/
