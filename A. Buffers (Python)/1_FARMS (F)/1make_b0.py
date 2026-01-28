# --------------------------------------------------------------------------------------------
# This script processes the clean glebas csv from STATA and merges overlapping polygons to 
# create new farm IDs (buffer 0). Two shapefiles of b0 are saved, one to folder NF_BUFFERS
# and another to 100M_BUFFERS. Disjoint polygons are kept as separate features.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
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

# Set working directory and file paths
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/"
csv_file = os.path.join(cd, "glebas_matched_master_nooutliers/glebas_matched_master_nooutliers.csv")
glebas_fixed = os.path.join(cd, "glebas_matched_master_nooutliers/glebas_matched_master_nooutliers_fixed.shp")
b0_NF = os.path.join(cd, "FARMS/NF_BUFFERS/b0/b0.shp")  # Final output
b0_100 = os.path.join(cd, "FARMS/100M_BUFFERS/b0/b0.shp")  # Final output

# Delete existing outputs if they exist
for f in [glebas_fixed, b0_NF, b0_100]:
    delete_shapefile(f)


# --------------------------------------------------------------------------------------------
# FIX GEOMETRIES
# --------------------------------------------------------------------------------------------

processing.run("native:fixgeometries", {
    'INPUT': f"delimitedtext://file:///{csv_file}?type=csv&delimiter=%5Ct;&maxFields=10000&detectTypes=yes&wktField=gt_geometria&crs=EPSG:4326",
    'METHOD': 1,
    'OUTPUT': glebas_fixed
    }
)


# --------------------------------------------------------------------------------------------
# DISSOLVE USING GDAL
# --------------------------------------------------------------------------------------------

for type in [b0_NF, b0_100]:
    processing.run(
        "gdal:dissolve", {
            'INPUT': glebas_fixed,
            'FIELD':'',
            'GEOMETRY':'geometry',
            'EXPLODE_COLLECTIONS':True,
            'KEEP_ATTRIBUTES':False,
            'COUNT_FEATURES':False,
            'COMPUTE_AREA':False,
            'COMPUTE_STATISTICS':False,
            'STATISTICS_ATTRIBUTE':'',
            'OPTIONS': 'GEOMETRY_NAME=geometry -nlt MULTIPOLYGON',
            'OUTPUT': type
        }
    )

# --------------------------------------------------------------------------------------------
# DELETE HELPER FILE
# --------------------------------------------------------------------------------------------

delete_shapefile(glebas_fixed)