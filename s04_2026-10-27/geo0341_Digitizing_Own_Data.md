# geo0341 Create your own spatial data: digitizing on the orthophoto

**Tool:** QGIS editing · **Time:** demo 30 min + exercise 30 min

You create a new GeoPackage with your own layers and digitize features on the HSRW campus in Kamp-Lintfort, including the Green Fab Lab south-east of the campus, from the orthophoto.

## Files
| File | Use |
|---|---|
| `geo0341_Digitizing_Own_Data.qgz` | orthophotos (DOP, WMS) and OSM of the Kamp-Lintfort campus; spatial bookmarks *Campus Kamp-Lintfort* and *Green Fab Lab* (*View → Panels → Spatial Bookmarks Manager*) |

## Guided demo
1. **New GeoPackage layer** (*Layer → Create Layer → New GeoPackage Layer…*): database `campus.gpkg` in this session folder, table `buildings`, geometry *Polygon*, CRS **EPSG:25832**, fields `name` (text), `use` (text), `floors` (integer).
2. Second layer in the same GeoPackage: `trees` (*Point*, field `species` text).
3. **Snapping** on (*Project → Snapping Options*, vertex + segment, 10 px), *Toggle Editing*, *Add Polygon Feature*: digitize three campus buildings and the Green Fab Lab (Friedrichstraße 2a), fill the attribute form.
4. **Edit:** *Vertex Tool* (move, add, delete vertices), *Undo*, *Save Layer Edits*. Check *Vector → Geometry Tools → Check Validity*.
5. **Attribute form:** *Layer Properties → Attributes Form*: make `use` a *Value Map* (teaching, lab, office, other).
6. Digitize 10 trees, then *Show Feature Count*. Compute the building area with a virtual field `$area`.

## Exercise
Digitize the green (vegetated) roof areas visible on the orthophoto: the Green Fab Lab and the small campus buildings in the south (new layer `green_roofs`, fields `building` text, `area_m2` as virtual field `$area`). Compare with the roof area of the five main campus buildings: what share of the roof area is green? Bonus: are there photovoltaic modules on any roof? Digitize them in a layer `pv_roofs` and estimate the installed power with 0.2 kWp per m² module area.

## Check yourself
- Why did you choose EPSG:25832 for the new layers and not EPSG:4326?
- What does snapping prevent? Give an example of a topology error.
- The orthophoto is a service (WMS). What limits the accuracy of your digitized polygons?
- Switch on the OSM layer: how well does your Green Fab Lab outline match the OSM building? Which one would you trust, and why?
