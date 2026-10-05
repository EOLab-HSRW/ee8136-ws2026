# geo0121 Why GIS? Motivation and core concepts

**Session:** 8136 S1 (input + pair activity) · **Time:** 35 min

## Why this course
We live in a spatio-temporal world. Almost every environmental and energy question has a *where* and a *when*: air temperature, groundwater quality, land use, flood extent, wind and solar potential, the grid. Data that carry a location are called **geodata** (spatial data); if they also change over time we speak of **spatio-temporal data**.

A **Geographic Information System (GIS)** is software (plus data, methods and people) to capture, store, check, analyse and present geodata. In this course you use **free and open-source software (FOSS)**:

- **QGIS**: desktop GIS to see, check, analyse and map data
- **Python / Jupyter** (on the EOLab JupyterHub): to automate what you clicked
- **PostgreSQL/PostGIS**: a database that keeps (geo)data and answers spatial questions
- **open data**: NRW geodata portal (opengeodata.nrw.de), German Weather Service (DWD), Copernicus/Sentinel and more

> See it (QGIS) → automate it (Python/PyQGIS) → keep it (PostGIS) → animate it (Temporal Controller)

## Core concepts (first contact; each comes back later)
| Concept | In one sentence | Session |
|---|---|---|
| layer | one theme (e.g. districts) drawn on top of others | S1 |
| vector / raster | objects with geometry and attributes vs. a grid of cells | S2 |
| attribute table | the "spreadsheet" behind a vector layer | S1, S2 |
| coordinate reference system (CRS) | how coordinates relate to places on Earth | S3 |
| web services | maps and data streamed from a server (WMS/WFS) | S3 |
| spatial analysis | answering questions with geometry (buffer, overlay, statistics) | S5–S7 |
| geodatabase | tables with geometry columns and spatial queries | S10–S13 |

## Pair activity: where is the *where*?
1. With your neighbour, write down three questions from environment and energy that need a map or spatial data (examples: Which wells exceed the nitrate limit? Where can wind turbines be built? Which districts got the most rain in July 2021?).
2. For each question note: which **data** (layers) you need, whether they are **vector or raster**, and the **question type**: *where is …?*, *what is at …?*, *what is near …?*, *what has changed …?*
3. Two pairs share one question each with the group.

## Self-study (optional)
- GIS Practicum, Baruch College (CUNY): a well-structured QGIS course for beginners: https://guides.newman.baruch.cuny.edu/gis/gisprac
- QGIS Training Manual: https://docs.qgis.org/latest/en/docs/training_manual/
