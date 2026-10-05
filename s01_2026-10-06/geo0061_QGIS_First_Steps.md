# geo0061 QGIS: install and first steps

**Session:** 8136 S1 · **Tool:** QGIS on your laptop · **Time:** 50 min · **Result:** a saved QGIS project with NRW boundaries on an OpenStreetMap background

## 1. Install QGIS
Download the current **Long Term Release (LTR)** from https://qgis.org/download/ (Windows: *QGIS Standalone Installer*, macOS: the official `.dmg`, Linux: your distribution's packages or the QGIS repository). Start it once before the session; the first start takes a while.
No laptop or installation problems? Use a lab PC today and ask a tutor; installation help continues in S2.

## 2. Get the data (open data from the NRW geodata portal)
1. Create a course folder on your laptop, e.g. `Documents/ee8136-ws2026/`. Each week, download the session folder from the course repository (GitHub page → *Code → Download ZIP*, or single files) into it, so that it looks like the repository: `s01_2026-10-06/`, `s02_2026-10-13/`, …
2. Download the administrative boundaries **DVG1 NRW** as Shape files, CRS EPSG:25832:
   https://www.opengeodata.nrw.de/produkte/geobasis/vkg/dvg/dvg1/ → `dvg1_EPSG25832_Shape.zip` (about 21 MB)
3. Unzip it **once** into the shared folder `data/dvg1_EPSG25832_Shape/` of your course folder. All QGIS projects of the course find it there:
   ```
   ee8136-ws2026/
     data/dvg1_EPSG25832_Shape/dvg1krs_nw.shp   (+ .dbf .shx .prj .cpg; same for bld, rbz, gem)
     s01_2026-10-06/
       geo0321_NRW_Admin_Boundaries.qgz
       geo0321_NRW_Admin_Boundaries_checkpoint.qgz
     s02_2026-10-13/
       data/ ...        (small files that belong to one session)
   ```
   A shapefile is always a set of files with the same name; keep them together.

## 3. First steps (follow the demo)
1. **New project** (*Project → New*). Set the project CRS to **EPSG:25832** (bottom right of the status bar → search `25832`).
2. **Interface tour:** *Browser* panel, *Layers* panel, map canvas, toolbars, *Processing Toolbox*, status bar (coordinates, scale, CRS).
3. **Basemap:** in the *Browser*, open *XYZ Tiles → OpenStreetMap* and drag it onto the map.
4. **Add vector layers:** in the *Browser*, navigate to your `ee8136-ws2026/data/dvg1_EPSG25832_Shape/` folder and drag `dvg1bld_nw.shp`, `dvg1rbz_nw.shp` and `dvg1krs_nw.shp` onto the map (or *Layer → Add Layer → Add Vector Layer…*).
5. **Navigate:** pan, zoom in/out, *Zoom to Layer*, mouse wheel; watch the coordinates in the status bar. Where is the campus (Kleve campus: about E 303 000, N 5 742 000; Kamp-Lintfort: E 329 000, N 5 708 000)?
6. **Identify** (i) a district and read its attributes; open its **attribute table**.
7. **Measure** the distance Kleve – Kamp-Lintfort with the *Measure Line* tool.
8. **Save** the project as `my_first_project.qgz` in your session folder `s01_2026-10-06/` (*Project → Save As…*).

## Before session 2: log in to the JupyterHub once
From session 2 on, every session also has a notebook part. Open the course link in Moodle, log in to the EOLab JupyterHub (https://hub.eolab.de) with your HSRW account and check that the folder `ee8136-ws2026` appears. Problems? Write in the Moodle forum before the session.

## Check yourself
- What is stored in the `.qgz` project file, and what is not?
- Which unit do the coordinates in the status bar have, and why?
- Which licence do the DVG1 data have, and what does it allow you to do?

## If something goes wrong
- *Unavailable layers* when opening a project: the DVG1 data are not in `data/dvg1_EPSG25832_Shape/` one level above the session folder. Use *Browse* in the dialog.
- No basemap: check the internet connection (the tiles come from tile.openstreetmap.org).
- Everything is far away or in the wrong place: check the project CRS (EPSG:25832).
