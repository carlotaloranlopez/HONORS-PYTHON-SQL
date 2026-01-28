# --------------------------------------------------------------------------------------------
# This script dissolves overlapping buffers at 250, 500, 1000, 2000m to make clusters.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

import os
import processing
from qgis.core import QgsProcessingFeatureSourceDefinition, QgsFeatureRequest

def delete_shapefile(path):
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        p = path.replace(".shp", ext)
        if os.path.exists(p):
            os.remove(p)

# Base directories
buffers_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
clusters_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/"

# Input / output paths
sources = [
    (
        os.path.join(buffers_dir, "b250/b250.shp"),
        os.path.join(buffers_dir, "b250/b250_fixed.shp"),
        os.path.join(clusters_dir, "b250_cluster/b250_cluster_b0/b250_cluster_b0.shp")
    ),
    (
        os.path.join(buffers_dir, "b500_1/b500_1.shp"),
        os.path.join(buffers_dir, "b500_1/b500_1_fixed.shp"),
        os.path.join(clusters_dir, "b500_cluster/b500_cluster_b0/b500_cluster_b0.shp")
    ),
    (
        os.path.join(buffers_dir, "b1000_1/b1000_1.shp"),
        os.path.join(buffers_dir, "b1000_1/b1000_1_fixed.shp"),
        os.path.join(clusters_dir, "b1000_cluster/b1000_cluster_b0/b1000_cluster_b0.shp")
    ),
    (
        os.path.join(buffers_dir, "b2000/b2000.shp"),
        os.path.join(buffers_dir, "b2000/b2000_fixed.shp"),
        os.path.join(clusters_dir, "b2000_cluster/b2000_cluster_b0/b2000_cluster_b0.shp")
    )
]

# Delete existing outputs
for _, fixed, cluster in sources:
    delete_shapefile(fixed)
    delete_shapefile(cluster)

# --------------------------------------------------------------------------------------------
# FIX GEOMETRIES
# --------------------------------------------------------------------------------------------

for src, fixed, _ in sources:
    processing.run(
        "native:fixgeometries",
        {
            "INPUT": src,
            "METHOD": 1,
            "OUTPUT": fixed
        }
    )

# --------------------------------------------------------------------------------------------
# DISSOLVE USING GDAL
# --------------------------------------------------------------------------------------------

for _, fixed, cluster in sources:
    processing.run(
        "gdal:dissolve",
        {
            "INPUT": fixed,
            "FIELD": "",
            "GEOMETRY": "geometry",
            "EXPLODE_COLLECTIONS": True,
            "KEEP_ATTRIBUTES": False,
            "COUNT_FEATURES": False,
            "COMPUTE_AREA": False,
            "COMPUTE_STATISTICS": False,
            "STATISTICS_ATTRIBUTE": "",
            "OPTIONS": "GEOMETRY_NAME=geometry -nlt MULTIPOLYGON",
            "OUTPUT": cluster
        }
    )
