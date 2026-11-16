# geo1241 Vegetation index NDVI with the Raster Calculator

**Tool:** QGIS Raster Calculator, Raster layer zonal statistics · **Time:** demo 15 min + exercise 25 min · **Slides:** `geo1220_RS_Fundamentals.pdf` (indices part) · **Builds on:** geo1221 (project `rs_kamp_lintfort.qgz`)

Plants absorb red light for photosynthesis and reflect near infrared (NIR) strongly. The
**Normalized Difference Vegetation Index** turns this into one number per pixel:

```
NDVI = (NIR − red) / (NIR + red)        Sentinel-2: (B08 − B04) / (B08 + B04)
```

It runs from −1 to +1: water below 0, bare soil and roofs around 0.1–0.3, dense green vegetation
above 0.6. Because it is a ratio, illumination and the scale factor (× 10 000) cancel out.

## Files
| File | Use |
|---|---|
| `data/rs_kamp_lintfort/s2_kamp_lintfort.tif` | band 3 = B04 red, band 5 = B08 NIR (see geo1221) |
| `data/rs_kamp_lintfort/worldcover_kamp_lintfort.tif` | ESA WorldCover 2021, 10 m: 10 tree cover, 30 grassland, 40 cropland, 50 built-up, 60 bare, 80 water (© ESA WorldCover project 2021, CC BY 4.0) |

Save new rasters in `data/rs_kamp_lintfort/` (small: about 2 MB each).

## Guided demo
1. **Predict.** Before computing: rank water, forest, a ripe cereal field, a roof and a meadow by
   their NDVI.
2. **Raster Calculator.** *Raster → Raster Calculator…*, expression:
   ```
   ("s2_kamp_lintfort@5" - "s2_kamp_lintfort@3") / ("s2_kamp_lintfort@5" + "s2_kamp_lintfort@3")
   ```
   Output `ndvi.tif`, format GeoTIFF. (If your layer has another name, double-click the bands in the
   *Raster bands* list instead of typing.)
3. **Style.** *Singleband pseudocolor*, colour ramp `RdYlGn`, *Min* −0.2, *Max* 0.9, *Apply*.
   Compare with the false colour composite of geo1221: where is the NDVI high, where low?
4. **Identify** a few pixels: lake, forest, field, roof. Did your ranking hold?

## Exercise (pairs)
1. **Threshold.** Raster Calculator `"ndvi@1" > 0.6` → `ndvi_gt06.tif`. Which share of the area is
   "dense green vegetation"? (*Layer Properties → Histogram*, or *Processing → Raster layer unique
   values report*.) Which forests and fields are *not* above 0.6, and why?
2. **NDVI per land-cover class.** *Processing → Toolbox → Raster analysis → Raster layer zonal
   statistics*: input `ndvi.tif`, *Zones layer* `worldcover_kamp_lintfort.tif`, output table
   `ndvi_by_worldcover`. Open the table: mean NDVI per class (`zone` = WorldCover code). Which classes
   overlap? What does that mean for a classification that uses NDVI only?
3. **Water index.** Compute the NDWI `(B03 − B08) / (B03 + B08)` (bands 2 and 5) as `ndwi.tif`.
   Where is it above 0? Compare with the WorldCover water class.
4. **Red edge.** Compute `(B08 − B05) / (B08 + B05)` (bands 5 and 4), the NDRE, as `ndre.tif`. Style
   both NDVI and NDRE with the same ramp, *Min* 0 / *Max* 0.9. In which areas does the NDRE show
   differences that the NDVI does not (look at forests and dense crops)? Why is it often used for
   crop monitoring, and why do agricultural drones such as the DJI Mavic 3M carry a red-edge band?
5. **One date only.** This is 25 June. Sketch the NDVI of a winter wheat field, a maize field and a
   meadow from March to October. What does one image miss?

## Optional: drone NDVI (Mavic 3M)
If your teacher provides the multispectral orthomosaic of Frohnenbruchhof (red and NIR bands):
compute the NDVI there with the same formula and compare it with the Sentinel-2 NDVI of the same
field. Same index, 10 m vs a few cm: what do you see in the drone NDVI that the satellite averages
away? Do the values agree (calibration, date, sensor)?

## Check yourself
- Why is the NDVI a *ratio* and not simply NIR − red?
- Why can the NDVI of a pixel be undefined, and where would that happen?
- Clouds have a low NDVI. Why does an NDVI time series need a cloud mask (SCL, geo1221)?

## Tutorials
- QGIS user manual, Raster Calculator: https://docs.qgis.org/latest/en/docs/user_manual/working_with_raster/raster_analysis.html
- NDVI explained (NASA Earth Observatory): https://earthobservatory.nasa.gov/features/MeasuringVegetation
- ESA WorldCover: https://esa-worldcover.org
