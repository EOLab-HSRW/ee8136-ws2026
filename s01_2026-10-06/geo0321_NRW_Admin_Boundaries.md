# geo0321 NRW administrative boundaries: layers, symbology, labels

**Session:** 8136 S1 · **Tool:** QGIS (on your laptop) · **Time:** demo 50 min + pair exercise 50 min · **Data:** DVG1 NRW (see geo0061)

You turn four plain boundary layers into a readable map of North Rhine-Westphalia (NRW): state, administrative regions (*Regierungsbezirke*), districts (*Kreise*) and municipalities (*Gemeinden*).

## Files in this folder

| File | Use |
|---|---|
| `geo0321_NRW_Admin_Boundaries.qgz` | start project: DVG1 layers (outlines only) + OpenStreetMap |
| `geo0321_NRW_Admin_Boundaries_checkpoint.qgz` | state after step 5 of the demo; open it if you fall behind |

Both projects expect the DVG1 data in the shared course data folder `../data/dvg1_EPSG25832_Shape/`, one level above this session folder (see geo0061, step 2). If QGIS reports *unavailable layers*, use *Browse* in that dialog and point it to your copy of `dvg1krs_nw.shp`; QGIS repairs the other layers from the same folder.

## The data: DVG1 (*Digitale Verwaltungsgrenzen*, scale 1:5000)

| Layer | Content | Attributes |
|---|---|---|
| `dvg1bld_nw` | state boundary (*Land*) | `ART` type, `GN` name, `KN` official key, `STAND` date |
| `dvg1rbz_nw` | 5 administrative regions | same |
| `dvg1krs_nw` | 53 districts and district-free cities | same; `KN` = 5-digit key (e.g. `05154` Kleve) |
| `dvg1gem_nw` | 396 municipalities | same; `KN` = 8-digit key, starts with the district key |

Source: Land NRW, Geobasis NRW, licence *Datenlizenz Deutschland – Zero – 2.0*. CRS: ETRS89 / UTM zone 32N (**EPSG:25832**, metres).

## Guided demo (follow along)

1. **Open** `geo0321_NRW_Admin_Boundaries.qgz` (or continue with your project from geo0061). Check the CRS in the status bar: `EPSG:25832`.
2. **Layer order and visibility.** Drag layers in the *Layers* panel: points and lines above polygons, small units above large ones, basemap at the bottom. Switch layers on and off.
3. **Single symbol.** *Layer Properties → Symbology*: state with a thick black outline and no fill; districts with a thin grey outline.
4. **Categorized symbol.** Regierungsbezirke: *Categorized* by `GN` → *Classify*. Set the layer *Opacity* to about 50 % so the basemap shows through.
5. **Labels.** Districts: *Layer Properties → Labels → Single labels*, value `GN`, add a white text *Buffer*.
   *Checkpoint:* `geo0321_NRW_Admin_Boundaries_checkpoint.qgz` shows the result of steps 1–5.
6. **Look inside the data.** *Open Attribute Table* of the districts, sort by `GN`; *Identify Features* (i) on the map. How many features does each layer have? (right-click a layer → *Show Feature Count*)
7. **Select by expression.** Find your district: `"GN" = 'Kleve'` (*Select Features by Expression*), then *Zoom to Selection*.
8. **Filter.** Show only the municipalities of one district: right-click `dvg1gem_nw` → *Filter…* → `left("KN", 5) = '05154'`.
9. **Save** the project (*Project → Save As…*) as `my_geo0321.qgz` in the same folder.

## Exercise in pairs (variant task)

Work on a district of your choice (the one you live in, or Wesel `05170`, or a random one from the attribute table).

1. Which values does `ART` have in the district layer? (*Categorized → Classify* lists them.) How many districts and how many district-free cities (*kreisfreie Städte*) does NRW have?
2. Show only the municipalities of your district, labelled with their names; all other districts in light grey.
3. Which of your municipalities is the largest? Add a column in the attribute table view with an expression (`$area / 1e6` gives km²) or use the *Field Calculator* with *Create virtual field*.
4. Be ready to show your map on the projector (debrief).

## Homework (present in S2)

**Map of your home district.** Make a map of the district you live in now (any district in NRW) with its municipalities, labels and the OpenStreetMap background. Export it with *Project → Import/Export → Export Map to Image* (PNG, 300 dpi) and write three sentences: which layers, which symbology and why, and one thing you noticed in the data. Upload to Moodle before the next session; two pairs present their map.

## Check yourself
- Explain the difference between a *layer* and a *project*.
- Why does the project file not contain the boundaries themselves?
- What does the coordinate `(321000, 5730000)` in EPSG:25832 mean? (Hint: easting/northing in metres.)

## Further reading
- QGIS Training Manual, *Module: Creating and Exploring a Basic Map* and *Classifying Vector Data*: https://docs.qgis.org/latest/en/docs/training_manual/
