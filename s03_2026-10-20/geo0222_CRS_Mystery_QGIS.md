# geo0222 CRS mystery in QGIS

**Tool:** QGIS · **Time:** input (slides) 30–45 min + exercise 60 min · **Data:** `data/Gauges_NRW_CRS_A.csv` … `_E.csv`

The same 254 river gauges of North Rhine-Westphalia are stored in five files, each in a different coordinate reference system (CRS). Only file C is easy: it is in degrees. Find the CRS of the other files so that all five layers lie exactly on top of each other, and every gauge sits on its river.

## Files
| File | Use |
|---|---|
| `data/Gauges_NRW_CRS_A.csv` … `_E.csv` | the five mystery files (LANUK NRW, OpenHygon, dl-de/zero-2-0, coordinates converted) |
| `geo0222_CRS_Mystery_QGIS.qgz` | start: NRW boundaries + OpenStreetMap, project CRS EPSG:25832 |
| `geo0222_CRS_Mystery_QGIS_checkpoint.qgz` | file C loaded correctly (EPSG:4326, latitude/longitude) |
| `geo0220_CRS_Projections.pdf` | slides: datum, ellipsoid, projections, EPSG codes, Gauss-Krüger and UTM in NRW |
| `data/pub_geobasis_etrs89_2020.pdf` | background: brochure *ETRS89/UTM* of Geobasis NRW (dl-de/zero-2-0) on the change from Gauss-Krüger to UTM in NRW |

## Steps
1. Open each CSV in a text editor. Separator? Column names? Look at the **value ranges** of the coordinates: degrees (−180…180)? Metres with 6, 7 or 8 digits in the easting? Does the easting start with *32* or with *2*?
2. Load file C as *Layer → Add Layer → Add Delimited Text Layer…*: separator semicolon, **X field = longitude, Y field = latitude** (the file stores latitude first!), Geometry CRS **EPSG:4326** (= checkpoint). In *Sample Data* check that `station_no` is *Text* (an identifier, not a number); set it to *Text* if needed.
3. Load A, B, D and E. For each file make a hypothesis from the value ranges and the slides. Candidates: EPSG:4326, EPSG:25832 (UTM 32N), EPSG:4647 (UTM 32N with zone prefix 32), EPSG:31466 (Gauss-Krüger zone 2), EPSG:3857 (Web Mercator).
4. Wrong guess? *Layer Properties → Source → Assigned Coordinate Reference System* changes it without reloading. **Do not** use *Export → Save Features As…* with another CRS to "fix" it: that transforms the wrong coordinates.
5. Verify: zoom in on one gauge (e.g. Goch on the Niers) at about 1:2 000. All five points must coincide and sit on the river. Measure any offset with the *Measure Line* tool. Depending on the datum transformation QGIS uses (it may ask you to choose one), one correctly identified file can be off by up to about a metre: which one, and why? (Slides: Gauss-Krüger uses the old datum DHDN.)

## Then: verify in code (notebook geo0221)
In the notebook you read the same five files with pandas, transform them with GeoPandas and measure the offsets in metres, and how wrong distances become in the wrong CRS. QGIS shows you *where* the points land, the notebook tells you *how far off* they are.

## Check yourself
- *Assigning* a CRS vs *transforming* to a CRS: what is the difference?
- Why does the project CRS (EPSG:25832) not change the coordinates stored in the files?
- What happens if you swap X and Y for file C? Try it.
- Why is EPSG:3857 a bad choice for measuring distances in NRW?
