# --------------------------------------------------------------------------------------------
# This file removes overlap between outer and inner buffers to create disjoint rings for the
# 2000m cluster:
#   b2000_ring  = b2000  - b0
#   b4000_ring  = b4000  - 2000
#   ...
# Files are saved as b2000_cluster_b*_ring to each buffer sub-folder with name b2000_cluster_b*, 
# inside CREDIT/GLEBAS/CLUSTERS/b2000_cluster, in the clean data folder.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b2000_cluster/"
buffer_pairs = [
    ("b0", "b2000"),
    ("b2000", "b4000"),
    ("b4000", "b6000"),
    ("b6000", "b8000"),
    ("b8000", "b10000")
]


# --------------------------------------------------------------------------------------------
# Make rings
# --------------------------------------------------------------------------------------------
for inner, outer in buffer_pairs:

    inner_path = f"{cd}b2000_cluster_{inner}/b2000_cluster_{inner}.shp"
    outer_path = f"{cd}b2000_cluster_{outer}/b2000_cluster_{outer}.shp"

    inner_fixed = f"{cd}b2000_cluster_{inner}/b2000_cluster_{inner}_fixed.shp"
    outer_fixed = f"{cd}b2000_cluster_{outer}/b2000_cluster_{outer}_fixed.shp"

    ring_path = f"{cd}b2000_cluster_{outer}/b2000_cluster_{outer}_ring.shp"

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
    })