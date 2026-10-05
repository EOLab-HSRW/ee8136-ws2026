# geo0361 A first map layout

**Session:** 8136 S2 · **Tool:** QGIS Print Layout · **Time:** demo 25 min · **Result:** a PDF map that stands on its own

A screenshot is not a map. A map that others can read has a **title**, a **legend**, a **scale bar**, a **north arrow** (if north is not up, or always for beginners), the **data sources and licences**, the **author and date**, and the **CRS**.

## Guided demo
1. Prepare the map view in the main window: your S1 project plus the stations you produced with the notebook geo0641 (`data/derived/dwd_stations.gpkg`, downloaded from the JupyterHub: right-click → *Download*), OSM or no basemap.
2. *Project → New Print Layout…* → name `station_map`. Page *A4 landscape*.
3. *Add Map*: draw the frame. Lock it, set the scale to a round number (e.g. 1:1 250 000).
4. *Add Legend*: uncheck *Auto update*, remove layers you do not want to explain, rename entries (`dvg1krs_nw` → *Districts*).
5. *Add Scale Bar* (units km, segments 2 × 25 km), *Add North Arrow*.
6. *Add Label* for the title and a second label for sources, e.g.
   `Data: DVG1 © Land NRW (2024), dl-de/zero-2-0; stations: Deutscher Wetterdienst (CC BY 4.0); basemap © OpenStreetMap contributors. CRS: ETRS89 / UTM 32N (EPSG:25832). Author, date.`
   Tip: `[% format_date(now(), 'yyyy-MM-dd') %]` inserts today's date.
7. *Layout → Export as PDF…* (and *Export as Image* for slides).

## Homework (present in S3)
**Annotated station map.** A4 PDF map of the DWD climate stations in NRW (or in your district) with legend, scale bar, north arrow, source and licence line, CRS and your name. Symbolize one attribute (e.g. altitude or years of operation) and write three sentences about what the map shows. Upload to Moodle before the next session.

## Check list for every map in this course
- [ ] Title says *what*, *where*, *when*
- [ ] Legend only with what is on the map, readable names
- [ ] Scale bar with sensible units; north arrow
- [ ] Sources, licences, CRS, author, date
- [ ] Colours: classes distinguishable, also in grey scale and for colour-blind readers (ColorBrewer ramps)
