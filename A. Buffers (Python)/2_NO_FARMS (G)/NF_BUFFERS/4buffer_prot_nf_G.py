# --------------------------------------------------------------------------------------------
# This script removes protected land from all buffers (including b0) in the NF specification. 
# It outputs shapefiles b*_ring_prot, saved to each buffer folder.
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

# Path and buffer definitions
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/NO_FARMS/NF_BUFFERS/"
protected = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/SHAPEFILES/Brazil_UCS/brazil_UCS_fixed.shp"
buffers = [
    "b0",
    "b250",
    "b500_1",
    "b500_2",
    "b750",
    "b1000_1",
    "b1000_2",
    "b1500",
    "b2000"
]


# --------------------------------------------------------------------------------------------
# Clean buffers
# --------------------------------------------------------------------------------------------

# Protected area geometry fix
protected_src = QgsProcessingFeatureSourceDefinition(
    protected,
    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
)

# Difference
for b in buffers:

    input_vector = (
        f"{cd}{b}/{b}.shp" if b == "b0"
        else f"{cd}{b}/{b}_ring.shp"
    )

    fixed_vector = (
        f"{cd}{b}/{b}_fixed.shp" if b == "b0"
        else f"{cd}{b}/{b}_fixed_ring.shp"
    )
    
    output_vector = (
        f"{cd}{b}/{b}_prot.shp" if b == "b0"
        else f"{cd}{b}/{b}_ring_prot.shp"
    )

    # Remove old outputs
    for s in [fixed_vector, output_vector]:
        delete_shapefile(s)

    # Fix buffer/ring geometry
    processing.run("native:fixgeometries", {
        'INPUT': input_vector,
        'METHOD': 1,
        'OUTPUT': fixed_vector
    })

    fixed_src = QgsProcessingFeatureSourceDefinition(
        fixed_vector,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    # Remove protected areas
    processing.run("native:difference", {
        'INPUT': fixed_src,
        'OVERLAY': protected_src,
        'OUTPUT': output_vector
    })

    # Remove temp file
    delete_shapefile(fixed_vector)