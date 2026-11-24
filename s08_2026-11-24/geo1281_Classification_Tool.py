"""geo1281 Classification tool: supervised and unsupervised classification of a multiband raster.

A QGIS Processing script (Processing Toolbox -> Scripts -> Add Script to Toolbox...). It needs only
what every QGIS has (numpy and GDAL), so it runs the same on the JupyterHub desktop and on Windows,
Linux and macOS laptops, without plugins.

Methods
  Minimum distance      each pixel gets the class whose mean spectrum is nearest (Euclidean)
  Maximum likelihood    each class is a multivariate normal distribution (mean vector and
                        covariance matrix from the training pixels); each pixel gets the class
                        with the highest likelihood (equal prior probabilities)
  k-means (unsupervised) k clusters found from the data alone; you name them afterwards

Inputs: a multiband raster (e.g. Sentinel-2), training polygons with an integer class field
(1-255) and optionally a class name field; optional validation polygons (same class ids) for the
accuracy assessment (confusion matrix, overall accuracy, kappa, producer's and user's accuracy).
Output: a classified raster (UInt8, 0 = no data) and an HTML report with the spectral signatures.

Why not GRASS i.maxlik? With GRASS 8 the QGIS GRASS provider copies the signature file to the
GRASS 7 location, so i.maxlik stops with "Unable to open signature file" (tested 2026-11-07,
QGIS 3.34 / GRASS 8.3; the same code is in QGIS 3.44).

Opengeo unit geo1280, licence CC BY-SA 4.0 (teaching material), code MIT.
"""
import html

import numpy as np
from osgeo import gdal, ogr, osr
from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSource, QgsProcessingParameterField,
                       QgsProcessingParameterFileDestination, QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterDestination, QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterString)

METHODS = ["Minimum distance", "Maximum likelihood", "k-means (unsupervised)"]
PALETTE = [(31, 120, 180), (51, 160, 44), (178, 223, 138), (255, 127, 0), (227, 26, 28),
           (106, 61, 154), (253, 191, 111), (166, 206, 227), (251, 154, 153), (202, 178, 214),
           (255, 255, 153), (177, 89, 40), (128, 128, 128), (0, 0, 0), (255, 0, 255)]


class Geo1281Classify(QgsProcessingAlgorithm):
    INPUT, BANDS, METHOD, TRAINING, CLASS_FIELD, NAME_FIELD = (
        "INPUT", "BANDS", "METHOD", "TRAINING", "CLASS_FIELD", "NAME_FIELD")
    N_CLUSTERS, VALIDATION, VAL_FIELD, OUTPUT, REPORT = (
        "N_CLUSTERS", "VALIDATION", "VAL_FIELD", "OUTPUT", "REPORT")

    def name(self):
        return "geo1281_classify"

    def displayName(self):
        return "Classify a multiband raster (geo1281)"

    def group(self):
        return "Opengeo"

    def groupId(self):
        return "opengeo"

    def shortHelpString(self):
        return ("Minimum distance, maximum likelihood or k-means classification of a multiband "
                "raster with numpy only. Training polygons need an integer class field (1-255). "
                "Validation polygons (optional, different areas than the training polygons!) give "
                "a confusion matrix, overall accuracy and kappa in the HTML report.")

    def createInstance(self):
        return Geo1281Classify()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT, "Multiband raster"))
        self.addParameter(QgsProcessingParameterString(
            self.BANDS, "Bands to use (e.g. 1,2,3,4,5,6; empty = all)", "", optional=True))
        self.addParameter(QgsProcessingParameterEnum(self.METHOD, "Method", METHODS, defaultValue=1))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.TRAINING, "Training polygons (not needed for k-means)",
            [QgsProcessing.TypeVectorPolygon], optional=True))
        self.addParameter(QgsProcessingParameterField(
            self.CLASS_FIELD, "Class id field (integer 1-255)", parentLayerParameterName=self.TRAINING,
            type=QgsProcessingParameterField.Numeric, optional=True))
        self.addParameter(QgsProcessingParameterField(
            self.NAME_FIELD, "Class name field (optional)", parentLayerParameterName=self.TRAINING,
            optional=True))
        self.addParameter(QgsProcessingParameterNumber(
            self.N_CLUSTERS, "Number of clusters (k-means only)", defaultValue=8, minValue=2, maxValue=30))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.VALIDATION, "Validation polygons (optional, for the accuracy assessment)",
            [QgsProcessing.TypeVectorPolygon], optional=True))
        self.addParameter(QgsProcessingParameterField(
            self.VAL_FIELD, "Validation class id field", parentLayerParameterName=self.VALIDATION,
            type=QgsProcessingParameterField.Numeric, optional=True))
        self.addParameter(QgsProcessingParameterRasterDestination(self.OUTPUT, "Classification"))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.REPORT, "Report (signatures, accuracy)", "HTML files (*.html)", optional=True))

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _rasterize(source, field, ds, context, feedback):
        """Burn the integer field of polygons into an array on the raster grid (0 = outside)."""
        srs = osr.SpatialReference()
        srs.ImportFromWkt(ds.GetProjection())
        mem = ogr.GetDriverByName("Memory").CreateDataSource("mem")
        lyr = mem.CreateLayer("poly", srs, ogr.wkbMultiPolygon)
        lyr.CreateField(ogr.FieldDefn("cls", ogr.OFTInteger))
        crs = QgsCoordinateReferenceSystem(ds.GetProjection())
        xform = QgsCoordinateTransform(source.sourceCrs(), crs, context.transformContext())
        bad = 0
        for f in source.getFeatures():
            v = f[field]
            if v is None or int(v) < 1 or int(v) > 255:
                bad += 1
                continue
            g = f.geometry()
            g.transform(xform)
            feat = ogr.Feature(lyr.GetLayerDefn())
            feat.SetField("cls", int(v))
            feat.SetGeometry(ogr.CreateGeometryFromWkt(g.asWkt()))
            lyr.CreateFeature(feat)
        if bad:
            feedback.pushWarning(f"{bad} polygon(s) without a class id 1-255 were skipped")
        out = gdal.GetDriverByName("MEM").Create("", ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte)
        out.SetGeoTransform(ds.GetGeoTransform())
        out.SetProjection(ds.GetProjection())
        gdal.RasterizeLayer(out, [1], lyr, options=["ATTRIBUTE=cls"])
        return out.GetRasterBand(1).ReadAsArray()

    @staticmethod
    def _kmeans(x, k, feedback, iters=30, seed=42):
        rng = np.random.default_rng(seed)
        sample = x[rng.choice(len(x), size=min(len(x), 50000), replace=False)]
        centres = [sample[rng.integers(len(sample))]]               # k-means++ start
        for _ in range(1, k):
            d2 = np.min([((sample - c) ** 2).sum(1) for c in centres], axis=0)
            centres.append(sample[rng.choice(len(sample), p=d2 / d2.sum())])
        c = np.array(centres)
        for it in range(iters):
            lab = np.argmin(((sample[:, None, :] - c[None]) ** 2).sum(2), axis=1)
            new = np.array([sample[lab == j].mean(0) if np.any(lab == j) else c[j] for j in range(k)])
            if np.allclose(new, c):
                break
            c = new
        feedback.pushInfo(f"k-means converged after {it + 1} iterations")
        return c

    # ------------------------------------------------------------------ main
    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        ds = gdal.Open(layer.source())
        if ds is None:
            raise QgsProcessingException("cannot open the raster with GDAL: " + layer.source())
        txt = (self.parameterAsString(parameters, self.BANDS, context) or "").strip()
        bands = [int(b) for b in txt.replace(";", ",").split(",") if b.strip()] or \
            list(range(1, ds.RasterCount + 1))
        names = [ds.GetRasterBand(b).GetDescription() or f"band {b}" for b in bands]
        method = self.parameterAsEnum(parameters, self.METHOD, context)
        feedback.pushInfo(f"{METHODS[method]} on bands {bands}: {names}")

        cube = np.stack([ds.GetRasterBand(b).ReadAsArray().astype("float64") for b in bands])
        valid = np.ones(cube.shape[1:], bool)
        for i, b in enumerate(bands):
            nd = ds.GetRasterBand(b).GetNoDataValue()
            if nd is not None:
                valid &= cube[i] != nd
        x = cube.reshape(len(bands), -1).T          # pixels x bands
        vflat = valid.ravel()

        class_names = {}
        if method == 2:
            k = self.parameterAsInt(parameters, self.N_CLUSTERS, context)
            means = self._kmeans(x[vflat], k, feedback)
            ids = list(range(1, k + 1))
            covs, counts = None, {}
            class_names = {i: f"cluster {i}" for i in ids}
        else:
            src = self.parameterAsSource(parameters, self.TRAINING, context)
            field = self.parameterAsString(parameters, self.CLASS_FIELD, context)
            if src is None or not field:
                raise QgsProcessingException("supervised methods need training polygons and a class id field")
            train = self._rasterize(src, field, ds, context, feedback).ravel()
            name_field = self.parameterAsString(parameters, self.NAME_FIELD, context)
            if name_field:
                for f in src.getFeatures():
                    if f[field] is not None:
                        class_names.setdefault(int(f[field]), str(f[name_field]))
            ids = sorted(int(v) for v in np.unique(train[vflat]) if v > 0)
            if len(ids) < 2:
                raise QgsProcessingException("need training pixels of at least two classes")
            means, covs, counts = [], [], {}
            for c in ids:
                xc = x[(train == c) & vflat]
                counts[c] = len(xc)
                means.append(xc.mean(0))
                if method == 1:
                    if len(xc) <= len(bands):
                        raise QgsProcessingException(
                            f"class {c}: {len(xc)} training pixels, maximum likelihood needs more than "
                            f"{len(bands)} (number of bands); digitize larger areas")
                    covs.append(np.cov(xc, rowvar=False) + np.eye(len(bands)) * 1e-6)
                feedback.pushInfo(f"class {c} {class_names.get(c, '')}: {len(xc)} training pixels")
            means = np.array(means)

        # classify in chunks
        out = np.zeros(x.shape[0], np.uint8)
        if method == 1:
            inv = [np.linalg.inv(s) for s in covs]
            logdet = [np.linalg.slogdet(s)[1] for s in covs]
        idx = np.flatnonzero(vflat)
        step = 200000
        for start in range(0, len(idx), step):
            if feedback.isCanceled():
                break
            sel = idx[start:start + step]
            xs = x[sel]
            if method == 1:
                score = np.stack([-(0.5 * logdet[j] + 0.5 * np.einsum(
                    "ij,jk,ik->i", xs - means[j], inv[j], xs - means[j])) for j in range(len(ids))], 1)
                best = np.argmax(score, 1)
            else:
                best = np.argmin(((xs[:, None, :] - means[None]) ** 2).sum(2), 1)
            out[sel] = np.array(ids, np.uint8)[best]
            feedback.setProgress(100 * min(1, (start + step) / len(idx)))
        out = out.reshape(valid.shape)

        # write GeoTIFF with a colour table
        path = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        drv = gdal.GetDriverByName("GTiff")
        dst = drv.Create(path, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte, ["COMPRESS=DEFLATE"])
        dst.SetGeoTransform(ds.GetGeoTransform())
        dst.SetProjection(ds.GetProjection())
        band = dst.GetRasterBand(1)
        ct = gdal.ColorTable()                        # colour table before the data (GeoTIFF)
        for i, c in enumerate(ids):
            ct.SetColorEntry(c, PALETTE[i % len(PALETTE)] + (255,))
        band.SetRasterColorTable(ct)
        band.SetNoDataValue(0)
        band.WriteArray(out)
        band.SetDescription(METHODS[method])
        dst.FlushCache()
        dst = None

        # accuracy assessment
        acc = None
        vsrc = self.parameterAsSource(parameters, self.VALIDATION, context)
        vfield = self.parameterAsString(parameters, self.VAL_FIELD, context)
        if vsrc is not None and vfield and method == 2:
            feedback.pushWarning("k-means: cluster numbers are not class ids. Name the clusters first "
                                 "(Reclassify by table), then compare with the validation polygons.")
        elif vsrc is not None and vfield:
            ref = self._rasterize(vsrc, vfield, ds, context, feedback)
            m = (ref > 0) & valid
            if method != 2:
                overlap = int(((train.reshape(valid.shape) > 0) & m).sum())
                if overlap:
                    feedback.pushWarning(f"{overlap} validation pixels are also training pixels: "
                                         "the accuracy will be too optimistic")
            acc = self._accuracy(ref[m], out[m], feedback)

        result = {self.OUTPUT: path}
        report = self.parameterAsFileOutput(parameters, self.REPORT, context)
        if report:
            self._report(report, layer.name(), METHODS[method], names, ids, class_names, means,
                         counts, out, acc)
            result[self.REPORT] = report
        return result

    @staticmethod
    def _accuracy(ref, pred, feedback):
        labels = sorted(set(np.unique(ref)) | set(np.unique(pred)))
        pos = {c: i for i, c in enumerate(labels)}
        cm = np.zeros((len(labels), len(labels)), int)          # rows: reference, cols: classified (as sklearn)
        np.add.at(cm, ([pos[r] for r in ref], [pos[p] for p in pred]), 1)
        n = cm.sum()
        oa = np.trace(cm) / n
        pe = (cm.sum(0) * cm.sum(1)).sum() / n ** 2
        kappa = (oa - pe) / (1 - pe) if pe < 1 else float("nan")
        feedback.pushInfo(f"overall accuracy {oa:.3f}, kappa {kappa:.3f} ({n} validation pixels)")
        return {"labels": labels, "cm": cm, "oa": oa, "kappa": kappa, "n": n}

    @staticmethod
    def _svg(names, ids, class_names, means):
        w, h, l, b = 640, 360, 70, 60
        top = max(1.0, float(np.max(means)))
        sx = lambda i: l + i * (w - l - 20) / max(1, len(names) - 1)
        sy = lambda v: h - b - v / top * (h - b - 20)
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h + 24 * len(ids)}" '
                 'font-family="sans-serif" font-size="14">',
                 f'<line x1="{l}" y1="{h - b}" x2="{w - 10}" y2="{h - b}" stroke="black"/>',
                 f'<line x1="{l}" y1="20" x2="{l}" y2="{h - b}" stroke="black"/>']
        for t in np.linspace(0, top, 5):
            parts.append(f'<text x="{l - 8}" y="{sy(t) + 5}" text-anchor="end">{t:.0f}</text>')
        for i, n in enumerate(names):
            parts.append(f'<text x="{sx(i)}" y="{h - b + 20}" text-anchor="middle">'
                         f'{html.escape(n.split()[0])}</text>')
        for j, c in enumerate(ids):
            col = "rgb(%d,%d,%d)" % PALETTE[j % len(PALETTE)]
            pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(means[j]))
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3"/>')
            parts.append(f'<rect x="{l}" y="{h + 24 * j - 10}" width="18" height="12" fill="{col}"/>'
                         f'<text x="{l + 26}" y="{h + 24 * j}">{c} {html.escape(class_names.get(c, ""))}</text>')
        parts.append("</svg>")
        return "".join(parts)

    def _report(self, path, raster, method, names, ids, class_names, means, counts, out, acc):
        area = {c: int((out == c).sum()) for c in ids}
        total = sum(area.values()) or 1
        rows = "".join(
            f"<tr><td>{c}</td><td>{html.escape(class_names.get(c, ''))}</td><td>{counts.get(c, '')}</td>"
            + "".join(f"<td>{v:.0f}</td>" for v in means[j])
            + f"<td>{area[c]}</td><td>{100 * area[c] / total:.1f}</td></tr>" for j, c in enumerate(ids))
        head = "".join(f"<th>{html.escape(n)}</th>" for n in names)
        doc = ["<html><head><meta charset='utf-8'><title>geo1281 report</title></head>"
               "<body style='font-family:sans-serif;font-size:16px'>",
               f"<h2>{html.escape(method)}: {html.escape(raster)}</h2>",
               "<h3>Spectral signatures (mean of the training pixels or cluster centres)</h3>",
               self._svg(names, ids, class_names, means),
               "<table border='1' cellpadding='4' style='border-collapse:collapse'>"
               f"<tr><th>id</th><th>name</th><th>training pixels</th>{head}<th>classified pixels</th>"
               f"<th>% of area</th></tr>{rows}</table>"]
        if acc:
            lab = acc["labels"]
            cmh = "".join(f"<th>map {c}</th>" for c in lab)
            body = ""
            for i, c in enumerate(lab):
                row = acc["cm"][i]
                pa = row[i] / row.sum() if row.sum() else float("nan")       # producer's: per reference row
                body += (f"<tr><th>reference {c}</th>" + "".join(f"<td>{v}</td>" for v in row)
                         + f"<td>{row.sum()}</td><td>{pa:.2f}</td></tr>")
            colsum = acc["cm"].sum(0)
            ua = [acc["cm"][i, i] / colsum[i] if colsum[i] else float("nan") for i in range(len(lab))]
            body += "<tr><th>sum</th>" + "".join(f"<td>{v}</td>" for v in colsum) + f"<td>{acc['n']}</td><td></td></tr>"
            body += "<tr><th>user's acc.</th>" + "".join(f"<td>{v:.2f}</td>" for v in ua) + "<td></td><td></td></tr>"
            doc.append("<h3>Accuracy on the validation polygons</h3>"
                       f"<p>Overall accuracy <b>{acc['oa']:.3f}</b>, kappa <b>{acc['kappa']:.3f}</b>, "
                       f"{acc['n']} pixels. Rows: reference (what the place is), columns: map (what the "
                       "classification says), as in scikit-learn and on the slides.</p>"
                       "<table border='1' cellpadding='4' style='border-collapse:collapse'>"
                       f"<tr><th></th>{cmh}<th>sum</th><th>producer's acc.</th></tr>{body}</table>")
        doc.append("</body></html>")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(doc))
