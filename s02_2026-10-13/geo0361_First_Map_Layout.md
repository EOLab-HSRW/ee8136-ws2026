# geo0361 A first map layout

**Session:** 8136 S2 · **Tool:** QGIS Print Layout · **Time:** demo 35 min (A stations 10, B layout 25) · **Data:** station CSV from geo0647 · **Result:** a PDF map that stands on its own

A screenshot is not a map. A map that others can read has a **title**, a **legend**, a **scale bar**, a **north arrow** (if north is not up, or always for beginners), the **data sources and licences**, the **author and date**, and the **CRS**.

## Guided demo
**A. The stations as a layer** (data from the notebook geo0647)
1. On the JupyterHub, open `data/derived/` and download (right-click → *Download*) `dwd_kl_stations_nrw_active.csv` **and** `dwd_kl_stations_nrw_active.csvt`.
   Save both into `data/derived/` of this session folder on your laptop. The `.csvt` file must stay next to the CSV with the same name: it tells QGIS the field types.
2. Open your S1 project (or `../s01_2026-10-06/geo0321_NRW_Admin_Boundaries_checkpoint.qgz`) and save it under a new name in this session folder, e.g. `my_geo0361.qgz`. Project CRS: **EPSG:25832**.
3. *Layer → Add Layer → Add Delimited Text Layer…* → the CSV file:
   * **File format:** *Custom delimiters*, tick **Semicolon**,
   * **Record and Fields Options:** *First record has field names*, *Detect field types*,
   * **Geometry definition:** *Point coordinates*, **X field `lon`**, **Y field `lat`**, **Geometry CRS: EPSG:4326 – WGS 84**,
   * in the sample table at the bottom: `station_id` must be **Text** (`05792`, not 5792); change it if not. *Add*.
4. **Keep it as a GeoPackage:** right-click the layer → *Export → Save Features As…* → format *GeoPackage*, file `data/derived/dwd_stations_nrw.gpkg`, layer name `stations_active`, CRS **EPSG:25832**. Remove the CSV layer from the project and keep the GeoPackage layer.
   *Layer Properties → Fields:* which types do `station_id`, `date_from` and `altitude` have now?
5. **Symbology:** *Graduated* on `altitude` (e.g. 5 classes, *Natural breaks*), or *Categorized* on the decade of `date_from`. Labels with `name` for a few stations only (e.g. rule `"altitude" > 300`).

**B. The layout**
6. *Project → New Print Layout…* → name `station_map`. Page *A4 landscape*.
7. *Add Map*: draw the frame. Lock it, set the scale to a round number (e.g. 1:1 250 000).
8. *Add Legend*: uncheck *Auto update*, remove layers you do not want to explain, rename entries (`dvg1krs_nw` → *Districts*, `stations_active` → *DWD climate stations (active)*).
9. *Add Scale Bar* (units km, segments 2 × 25 km), *Add North Arrow*.
10. *Add Label* for the title and a second label for sources, e.g.
   `Data: DVG1 © Land NRW (2024), dl-de/zero-2-0; stations: Deutscher Wetterdienst (CC BY 4.0); basemap © OpenStreetMap contributors. CRS: ETRS89 / UTM 32N (EPSG:25832). Author, date.`
   Tip: `[% format_date(now(), 'yyyy-MM-dd') %]` inserts today's date.
11. *Layout → Export as PDF…* (and *Export as Image* for slides). Save the project.

**Check yourself:** what happens if you choose EPSG:25832 as *Geometry CRS* for the CSV in step 3? Why is the GeoPackage of step 4 better for further work than the CSV?

## Homework (present in S3)
**Annotated station map.** A4 PDF map of the DWD climate stations in NRW (or in your district) with legend, scale bar, north arrow, source and licence line, CRS and your name. Symbolize one attribute (e.g. altitude or years of operation) and write three sentences about what the map shows. Upload to Moodle before the next session.

## Check list for every map in this course
- [ ] Title says *what*, *where*, *when*
- [ ] Legend only with what is on the map, readable names
- [ ] Scale bar with sensible units; north arrow
- [ ] Sources, licences, CRS, author, date
- [ ] Colours: classes distinguishable, also in grey scale and for colour-blind readers (ColorBrewer ramps)
