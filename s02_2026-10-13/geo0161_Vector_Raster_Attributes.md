# geo0161 Data types and formats: vector, raster, attributes, GeoPackage

**Session:** 8136 S2 · **Tool:** QGIS · **Time:** input 20 min + demo 30 min · **Data:** DVG1 (`../data/dvg1_EPSG25832_Shape/`), `data/RBZ_Codes_NRW.csv`

## Concepts
| | Vector | Raster |
|---|---|---|
| models the world as | objects: points, lines, polygons (+ attributes) | a grid of cells with one value per cell and band |
| good for | boundaries, stations, wells, roads | elevation, satellite images, temperature fields |
| typical formats | Shapefile (`.shp` + 4 companion files), **GeoPackage** (`.gpkg`), GeoJSON, CSV with coordinates | GeoTIFF (`.tif`), JPEG/PNG + world file, NetCDF |
| resolution | scale / accuracy of the vertices | cell size (e.g. 1 m DTM) |

Attribute values have **types**: text (string), integer, decimal (real), date. A key like `051` must be *text*, otherwise the leading zero is lost.

## Guided demo
1. Open your S1 project (or `../s01_2026-10-06/geo0321_NRW_Admin_Boundaries_checkpoint.qgz`).
2. **Field types:** *Layer Properties → Fields* of `dvg1krs_nw`. Which types do `GN`, `KN` and `STAND` have?
3. **One file instead of 20:** right-click `dvg1krs_nw` → *Export → Save Features As…* → format *GeoPackage*, file `nrw_admin.gpkg` (in your session folder), layer name `districts`. Repeat for `dvg1rbz_nw` (layer `regions`) and `dvg1gem_nw` (layer `municipalities`) into the *same* file. Compare the file sizes with the shapefiles.
4. **New field:** in the `districts` layer of the GeoPackage open the *Field Calculator*, create a new text field `rbz_id` with the expression `left("KN", 3)` (the first three digits of the district key are the region key). Save the edits.
5. **Table without geometry:** add `data/RBZ_Codes_NRW.csv` (*Layer → Add Layer → Add Delimited Text Layer…*, *No geometry*, uncheck *Detect field types* so the codes stay text).
6. **Attribute join:** *Layer Properties → Joins* of `districts`: join layer `RBZ_Codes_NRW`, join field `rbz_id`, target field `rbz_id`. Open the attribute table: every district now knows its region name.
7. **Raster for comparison (optional):** download `dvg1_EPSG25832_TIFF.zip` from the same portal as DVG1 and open `dvg1krs_nw.tif`. Zoom in on a boundary: what do you see that the vector layer does not show? *Identify* a pixel.

## Check yourself
- Why did `detectTypes` have to be off for the CSV?
- A join is not stored in the data. Where is it stored, and what happens if you open the GeoPackage in another project?
- When would you choose raster, when vector, for the same theme (e.g. district boundaries)?
