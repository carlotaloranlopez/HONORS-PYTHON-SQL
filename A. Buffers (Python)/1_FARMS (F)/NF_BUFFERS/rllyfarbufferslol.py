# --------------------------------------------------------------------------------------------
# This file takes a buffer 0 shapefile and creates buffers (for the near-far specification) at
# several different distances. These files are saved to each buffer sub-folder with name b*, 
# inside CREDIT/GLEBAS/FARMS/NF_BUFFERS. 
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

# Dependencies & delete shapefile function definition
import os
import processing
def delete_shapefile(path):
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        p = path.replace(".shp", ext)
        if os.path.exists(p):
            os.remove(p)

# Create variables to set working directory, buffer dictionary with buffer names and distance in decimal degrees, and universal input file
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
buffers_nf = {
    "4000": 0.036314
    "8000": 0.072628
}
input_vector = f"{cd}b0/b0.shp"


# --------------------------------------------------------------------------------------------
# Make buffers
# --------------------------------------------------------------------------------------------

for b in buffers_nf:
    # Define output file name and get distance from dictionary
    output_vector = f"{cd}b{b}/b{b}.shp"
    degrees = buffers_nf[b]
    
    # Remove existing buffer file if it exists
    delete_shapefile(output_vector)

    # Make buffer
    processing.run(
        "native:buffer", 
        {
            'INPUT': input_vector,
            'DISTANCE':degrees,
            'SEGMENTS':5,
            'END_CAP_STYLE':0,
            'JOIN_STYLE':0,
            'MITER_LIMIT':2,
            'DISSOLVE':False,
            'SEPARATE_DISJOINT':False,
            'OUTPUT': output_vector
        }
    )



# --------------------------------------------------------------------------------------------
# This file removes overlap between outer and inner buffers to create disjoint rings for the
# NF specification. For instance:
#   b_outer_ring  = b_outer  - b_inner
#   b_inner_ring  = b_inner  - b0
# Files are saved as b*_ring to each buffer sub-folder with name b*, inside CREDIT/
# GLEBAS/FARMS/NF_BUFFERS, in the clean data folder.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
buffer_pairs = [
    ("b0", "b4000"),
    ("b4000", "b8000")
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
protected = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/SHAPEFILES/Brazil_UCS/brazil_UCS_fixed.shp"
buffers = [
    "b0",
    "b4000",
    "b8000"
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



# --------------------------------------------------------------------------------------------
# This script computes zonal histograms for buffer polygons at NF distances 0, 250-500, … 
# using land use rasters. Results are saved as buffer-year .csv files inside buffer folders 
# b*, found in the clean data folder, under DEFORESTATION/FARMS/NF_BUFFERS.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

# Dependencies & shapefile delete function
import os
import processing
from qgis.core import QgsProcessingFeatureSourceDefinition, QgsFeatureRequest  # <-- add this
def delete_shapefile(path):
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        p = path.replace(".shp", ext)
        if os.path.exists(p):
            os.remove(p)

# Create variables to set working directory, year, and buffer lists
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/"
years = range(2016, 2025)
buffers = ["4000", "8000"]


# --------------------------------------------------------------------------------------------
# Fix geometries and calculate histogram for all buffers > 0
# --------------------------------------------------------------------------------------------

for b in buffers:
    # Fix geometries
    input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b{b}/b{b}_ring_prot.shp"
    fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b{b}/b{b}_ring_prot_fixed.shp"

    # Delete old fixed shapefile if it exists
    if os.path.exists(fixed_vector):
        os.remove(fixed_vector)

    processing.run(
        "native:fixgeometries",
        {
            'INPUT': input_vector,
            'METHOD': 1,
            'OUTPUT': fixed_vector
        }
    )
    
    # Zonal histogram for each year
    for y in years:
        input_raster = f"{cd}DATA_RAW/DEFORESTATION/Mapbiomas/{y}_cover.tif"
        output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/FARMS/NF_BUFFERS/b{b}/b{b}_cover{y}_prot.csv"

        # Delete old csv if it exists
        if os.path.exists(output_csv):
            os.remove(output_csv)

        processing.run(
            "native:zonalhistogram",
            {
                'INPUT_RASTER': input_raster,
                'RASTER_BAND': 1,
                'INPUT_VECTOR': QgsProcessingFeatureSourceDefinition(
                    fixed_vector,
                    selectedFeaturesOnly=False,
                    featureLimit=-1,
                    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
                ),
                'COLUMN_PREFIX': 'HISTO_',
                'OUTPUT': output_csv
            }
        )
    
    # Remove helper fixed vector file
    delete_shapefile(fixed_vector)


# --------------------------------------------------------------------------------------------
# Fix geometries and calculate histogram for buffer = 0
# --------------------------------------------------------------------------------------------

# Fix geometries
input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b0/b0_prot.shp"
fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b0/b0_prot_fixed.shp"

# Delete old fixed shapefile if it exists
if os.path.exists(fixed_vector):
    os.remove(fixed_vector)

# Fix
processing.run(
    "native:fixgeometries",
        {
        'INPUT': input_vector,
        'METHOD': 1,
        'OUTPUT': fixed_vector
        }
)
    
# Zonal histogram for each year
for y in years:
    input_raster = f"{cd}DATA_RAW/DEFORESTATION/Mapbiomas/{y}_cover.tif"
    output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/FARMS/NF_BUFFERS/b0/b0_cover{y}_prot.csv"

    # Delete old CSV if it exists
    if os.path.exists(output_csv):
        os.remove(output_csv)

    processing.run(
        "native:zonalhistogram",
        {
            'INPUT_RASTER': input_raster,
            'RASTER_BAND': 1,
            'INPUT_VECTOR': QgsProcessingFeatureSourceDefinition(
                fixed_vector,
                selectedFeaturesOnly=False,
                featureLimit=-1,
                flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
            ),
            'COLUMN_PREFIX': 'HISTO_',
            'OUTPUT': output_csv
        }
    )
            

delete_shapefile(fixed_vector)