# --------------------------------------------------------------------------------------------
# This file removes overlap between outer and inner buffers to create disjoint rings for the
# NF specification. Files are saved as b*_ring to each buffer sub-folder with name b*, inside 
# CREDIT/GLEBAS/NO_FARMS/NF_BUFFERS, in the clean data folder.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/NO_FARMS/NF_BUFFERS/"
buffer_pairs = [
    ("b0", "b250"),
    ("b250", "b500_1"),
    ("b0", "b500_2"),
    ("b500_2", "b1000_1"),
    ("b0", "b750"),
    ("b750", "b1500"),
    ("b0", "b1000_2"),
    ("b1000_2", "b2000")
]


# --------------------------------------------------------------------------------------------
# Build rings
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

    # Take difference 
    processing.run("native:difference", {
        'INPUT': outer_src,
        'OVERLAY': inner_src,
        'OUTPUT': ring_path
    })

    # Remove helper files
    delete_shapefile(inner_fixed)
    delete_shapefile(outer_fixed)