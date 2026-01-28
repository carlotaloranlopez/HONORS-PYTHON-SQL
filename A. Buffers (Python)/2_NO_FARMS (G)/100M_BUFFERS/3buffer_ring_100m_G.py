# --------------------------------------------------------------------------------------------
# This file removes overlap between outer and inner buffers to create disjoint rings for the
# 100M specification. Files are saved as b*_ring to each buffer sub-folder with name b*, 
# inside CREDIT/GLEBAS/NO_FARMS/100M_BUFFERS, in the clean data folder.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/NO_FARMS/100M_BUFFERS/"
buffer_pairs = [
    ("b0", "b100"),
    ("b100", "b200"),
    ("b200", "b300"),
    ("b300", "b400"),
    ("b400", "b500"),
    ("b500", "b600"),
    ("b600", "b700"),
    ("b700", "b800"),
    ("b800", "b900"),
    ("b900", "b1000"),
    ("b1000", "b1100"),
    ("b1100", "b1200"),
    ("b1200", "b1300"),
    ("b1300", "b1400"),
    ("b1400", "b1500"),
    ("b1500", "b1600"),
    ("b1600", "b1700"),
    ("b1700", "b1800"),
    ("b1800", "b1900"),
    ("b1900", "b2000")
]


# --------------------------------------------------------------------------------------------
# Make rings
# --------------------------------------------------------------------------------------------
for inner, outer in buffer_pairs:

    inner_path = f"{cd}{inner}/{inner}.shp"
    outer_path = f"{cd}{outer}/{outer}.shp"

    inner_fixed = f"{cd}{inner}/{inner}_fixed.shp"
    outer_fixed = f"{cd}{outer}/{outer}_fixed.shp"

    ring_path = f"{cd}{outer}/{outer}_ring.shp"

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

    # Delete helper files
    delete_shapefile(inner_fixed)
    delete_shapefile(outer_fixed)