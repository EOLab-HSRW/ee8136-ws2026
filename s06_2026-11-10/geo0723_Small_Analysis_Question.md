# geo0723 Homework: a small analysis question with a map

**Tool:** QGIS (and/or the geo0722 notebook) · **Time:** about 2 h · **Builds on:** geo0721, geo0722 · **Hand in:** one map (PDF or PNG from a QGIS layout) and a short text (max. ½ page) in the Moodle folder of this session; the deadline and the presentations (two pairs, 5 min each) are in the course plan.

Ask **one** question, answer it with the operations of geo0721/geo0722 (buffer, dissolve, spatial join, overlay) and show the answer on **one** map.

## Option A – your county
Take your homework county from the first session (or any county of NRW):
1. Which part of the county is more than 20 km from an active DWD climate station, and which part is drinking water protection zone? Do the two overlap?
2. Make a map in a QGIS layout: county outline, uncovered part, protection zones by zone (1, 2, 3), stations with names, a background map from a WMS (geo0921 Part A), title, legend, scale bar, north arrow and the **sources** (DWD; © Geobasis NRW; opengeodata.nrw.de, *Trinkwasser- und Heilquellenschutzgebiete NRW*).
3. Text: the question, the steps (tool names), the numbers (km², %), and one sentence on a limitation (data, distance, CRS, …).

## Option B – farmland along streams (Frohnenbruch, Kamp-Lintfort)
Use §6 of the geo0722 notebook, or in QGIS: `data/geo0722/frohnenbruch.gpkg` and the WFS of the Chamber of Agriculture (`https://www.wfs.nrw.de/umwelt/lwk_eufoerderung`, *Layer ▸ Data Source Manager ▸ WFS / OGC API - Features ▸ New*, layer *Beantragte_und_als_foerderfaehig_festgestellte_Teilschlaege_in_NRW*; zoom in to the farm first).
1. Choose your own strip width and justify it (e.g. 5 m, Federal Water Act §38a; 10 m; 50 m). How many hectares of each crop group lie inside the strip?
2. Map: parcels coloured by use group (`USE_TXT`), streams, the strip, DOP background, sources (© OpenStreetMap contributors, ODbL; Landwirtschaftskammer NRW, dl-de/by-2-0; © Geobasis NRW).
3. Text as in option A; compare the official parcels with OSM landuse.

## Your own idea
Other open data of NRW work as well, e.g. flood areas (*Überschwemmungsgebiete*), groundwater measuring sites (OpenHygrisC), air-quality sites (LUQS), all on https://www.opengeodata.nrw.de/produkte/umwelt_klima/. Ask before you start if you are unsure. In your home country: which official open data would you use for the same question, and do they exist?

## Assessment (formative, 10 points)
| Criterion | 2 points | 1 point | 0 points |
|---|---|---|---|
| **Question** | one clear question that the map and the numbers answer | question vague or only partly answered | no question |
| **Method** | the right operations (buffer, dissolve, spatial join, overlay) in a metric CRS, steps with tool names so someone else can repeat them | one step unclear or a buffer/area in degrees | steps missing |
| **Numbers** | km² or ha and %, plausible, with the reference (county, AOI) | numbers without unit or reference | no numbers |
| **Map** | title, legend, scale bar, north arrow, readable symbols; the answer is visible on the map | one element missing or the answer hard to see | no layout |
| **Sources and limits** | every layer with source and licence on the map; one limitation named (data gaps, distance, simplification, date) | sources incomplete or no limitation | no sources |

A sample map for option A (county Wesel) is shown in class after the deadline.
