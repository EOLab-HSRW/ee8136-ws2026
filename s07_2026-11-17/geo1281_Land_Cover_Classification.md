# geo1281 Land-cover classification in QGIS: clusters, training areas, accuracy

**Tool:** QGIS Processing script `geo1281_Classification_Tool.py` (k-means, minimum distance, maximum likelihood), GeoPackage digitizing · **Time:** demo 20 min + exercise 40 min · **Slides:** `geo1220_RS_Fundamentals.pdf` (classification part) · **Builds on:** geo1221 (composites, signatures), geo1241 (NDVI)

A classification turns the six reflectance values of every pixel into one land-cover class.
**Unsupervised:** the computer groups similar pixels into clusters, you name them afterwards.
**Supervised:** you show the computer examples (training areas) of each class, it learns their
spectral signatures and assigns every pixel to the most similar class. Then you check the map with
**other** areas whose class you know (validation): the accuracy assessment.

## Files
| File | Use |
|---|---|
| `data/rs_kamp_lintfort/s2_kamp_lintfort.tif` | Sentinel-2, 6 bands (geo1221) |
| `geo1281_Classification_Tool.py` | the classification tool (QGIS Processing script, needs no plugin) |
| `data/geo1281_training_example.gpkg` | example training polygons (fallback), field `class_id`, `class_name` |
| `data/geo1281_validation_example.gpkg` | example validation polygons (other places, same classes) |
| `data/rs_kamp_lintfort/worldcover_kamp_lintfort.tif` | ESA WorldCover 2021 for comparison |

Classes used in this activity:

| `class_id` | `class_name` | Where to find it |
|---|---|---|
| 1 | water | lakes in the north-east, ponds |
| 2 | forest | dark red in the false colour composite |
| 3 | grassland | meadows, pastures, parks, sports fields |
| 4 | cropland | arable fields (green, ripening or bare in late June) |
| 5 | built-up | roofs, roads, car parks, industry |

## Setup: add the tool
*Processing → Toolbox*, click the Python icon (*Scripts*) → *Add Script to Toolbox…* → select
`geo1281_Classification_Tool.py` in your session folder. It appears under *Scripts → Opengeo →
Classify a multiband raster (geo1281)*. You can open the code with *right-click → Edit Script…*:
about 300 lines of numpy, no magic.

## Guided demo
1. **Unsupervised first.** Run the tool: *Multiband raster* `s2_kamp_lintfort`, *Method*
   `k-means (unsupervised)`, *Number of clusters* 8, *Report* `kmeans_report.html` (in your session
   folder), *Classification* `kmeans.tif`. Open the report from the *Results Viewer* (or double-click
   it in the Browser).
2. **Name the clusters.** Compare `kmeans.tif` with the false colour composite. Which cluster is water,
   which forest, which the town? Which land-cover type is split into several clusters, which clusters
   mix two types? The computer found groups of similar spectra, not land-use classes.
3. **Training areas.** *Layer → Create Layer → New GeoPackage Layer…*: database `training.gpkg` in
   your session folder, table `training`, geometry *Polygon*, CRS *EPSG:25832*; fields `class_id`
   (*Integer*) and `class_name` (*Text*). Digitize one forest polygon together (*Toggle Editing*,
   *Add Polygon Feature*): **inside** the forest, away from the edge, at least 3 × 3 pixels (30 m × 30 m).
4. **Supervised.** After the exercise below, run the tool with *Method* `Maximum likelihood`,
   *Training polygons* `training`, *Class id field* `class_id`, *Class name field* `class_name`,
   output `maxlik.tif`, report `maxlik_report.html`. The report shows the spectral signatures of your
   training areas: compare them with your hand-measured signatures from geo1221.

## Exercise (pairs)
1. **Digitize training areas** for all five classes: at least **4 polygons per class**, spread over the
   whole image, each polygon homogeneous (one field, one forest, one roof area), together at least
   50 pixels per class. Cropland: include green, ripening and bare fields. Save often
   (*Save Layer Edits*). *Stuck?* Use `data/geo1281_training_example.gpkg`.
2. **Two classifiers.** Classify with `Minimum distance` (`mindist.tif`) and with
   `Maximum likelihood` (`maxlik.tif`), same training areas. Put them side by side with the false colour
   composite. Where do they differ? Look at the town, shadows of tall buildings and forest edges, and
   the lakes.
3. **Accuracy.** Swap `training.gpkg` with the pair next to you: **their** training areas are **your**
   validation areas (they are independent of your training data). Run maximum likelihood again with
   *Validation polygons* = the other pair's layer, *Validation class id field* `class_id`. Read
   overall accuracy, kappa and the confusion matrix in the report (rows: reference = what the place
   is, columns: what your map says). (No partner? Use
   `data/geo1281_validation_example.gpkg`.)
4. **Read the confusion matrix.** Which two classes are confused most? Which class has a low
   *producer's accuracy* (pixels of that class were missed), which a low *user's accuracy* (the map
   says "class X" but it is often something else)? Explain one confusion with the spectral signatures.
5. **Improve.** Change one thing: add training areas where the map is wrong, split *cropland* into
   two classes (e.g. 4 green crops, 6 bare/ripe fields) or leave out band 6
   (*Bands to use* `1,2,3,4,5`). Run again with the same validation areas. Did the accuracy change?
6. **Compare with WorldCover.** Style `worldcover_kamp_lintfort.tif` with *Paletted/Unique values*
   and compare it with your best map. Where do they disagree, and who is right? (WorldCover is from
   2021 and made by a machine-learning model, too.)

## Why not GRASS `i.maxlik`?
QGIS also lists GRASS `i.cluster`, `i.gensig` and `i.maxlik` (the classic GRASS classification).
With GRASS 8 the QGIS GRASS provider puts the signature file where only GRASS 7 looks for it, so
`i.maxlik` stops with *Unable to open signature file* (checked in QGIS 3.44 with GRASS 8.5). Watch
out: the Processing dialog still reports success, but no output file appears; the error is only in
the log. A multiband raster also counts as one map there: the six bands must be separate files.
The tool of this activity does the same mathematics (maximum likelihood with mean vectors and
covariance matrices) in numpy. In GRASS GIS itself (outside QGIS) `i.gensig` → `i.maxlik` →
`r.kappa` works and gives exactly the same result as the tool (an option for projects, together with
`i.segment` for objects such as fields).

## Check yourself
- Why must validation areas be different from training areas? What happens to the accuracy if you
  validate with the training polygons?
- Minimum distance uses only the class means, maximum likelihood also the covariance (spread and
  correlation of the bands). For which class does that matter most, and why?
- An overall accuracy of 0.83 sounds good. Which information does it hide that the confusion matrix
  shows?
- Your training polygons sit in "nice" homogeneous areas. Is the accuracy on such areas the accuracy
  of the whole map?

## Tutorials
- QGIS user manual, digitizing: https://docs.qgis.org/latest/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html
- QGIS user manual, Processing scripts: https://docs.qgis.org/latest/en/docs/user_manual/processing/scripts.html
- Accuracy assessment (good practice): Olofsson, P. et al. (2014): Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57, https://doi.org/10.1016/j.rse.2014.02.015
