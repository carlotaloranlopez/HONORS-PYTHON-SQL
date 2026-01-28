# --------------------------------------------------------------------------------------------
# This file removes overlap between outer and inner buffers to create disjoint rings for the
# 250m cluster:
#   b250_ring  = b250  - b0
#   b500_ring  = b500  - b125
#   ...
# Files are saved as b250_cluster_b*_ring to each buffer sub-folder with name b250_cluster_b*, 
# inside CREDIT/GLEBAS/CLUSTERS/b250_cluster, in the clean data folder.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

# Dependencies & delete shapefile function definition
import os
import processing
from qgis.core import QgsProcessingFeatureSourceDefinition, QgsFeatureRequest
def delete_shapefile(path):
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        p = path.replace(".shp", ext)
        if os.path.exists(p):
            os.remove(p)

# Path and buffer pair definition
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b250_cluster/"
buffer_pairs = [
    ("b0", "b250"),
    ("b250", "b500"),
    ("b500", "b750"),
    ("b750", "b1000"),
    ("b1000", "b1250"),
    ("b1250", "b1500"),
    ("b1500", "b1750"),
    ("b1750", "b2000")
]


# --------------------------------------------------------------------------------------------
# Make rings
# --------------------------------------------------------------------------------------------
for inner, outer in buffer_pairs:

    inner_path = f"{cd}b250_cluster_{inner}/b250_cluster_{inner}.shp"
    outer_path = f"{cd}b250_cluster_{outer}/b250_cluster_{outer}.shp"

    inner_fixed = f"{cd}b250_cluster_{inner}/b250_cluster_{inner}_fixed.shp"
    outer_fixed = f"{cd}b250_cluster_{outer}/b250_cluster_{outer}_fixed.shp"

    ring_path = f"{cd}b250_cluster_{outer}/b250_cluster_{outer}_ring.shp"

    # Clean old files
    for f in [inner_fixed, outer_fixed, ring_path]:
        delete_shapefile(f)

    # Fix geometries
    processing.run("native:fixgeometries", {
        'INPUT': inner_path,
        'METHOD': 1,
        'OUTPUT': inner_fixed
    })

    processing.run("native:fixgeometries", {
        'INPUT': outer_path,
        'METHOD': 1,
        'OUTPUT': outer_fixed
    })

    # Skip any remaining invalid features
    inner_src = QgsProcessingFeatureSourceDefinition(
        inner_fixed,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    outer_src = QgsProcessingFeatureSourceDefinition(
        outer_fixed,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    # b*_ring = b* − b(previous)
    processing.run("native:difference", {
        'INPUT': outer_src,
        'OVERLAY': inner_src,
        'OUTPUT': ring_path
    })C/100