# --------------------------------------------------------------------------------------------
# This script creates buffer 0 shapefiles, which correspond to glebas from the SICOR, 
# without merging overlaps, and with ID contract_recipient_id. It makes two b0 files, one for
# NF_BUFFERS and another for 100M_BUFFERS. IDs were created in STATA.
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
b0_NF = os.path.join(cd, "NO_FARMS/NF_BUFFERS/b0/b0.shp")  # Final output
b0_100 = os.path.join(cd, "NO_FARMS/100M_BUFFERS/b0/b0.shp")  # Final output


# --------------------------------------------------------------------------------------------
# FIX GEOMETRIES TO MAKE B0
# --------------------------------------------------------------------------------------------
for file in [b0_NF, b0_100]:
    # Delete existing outputs if they exist
    delete_shapefile(file)

    # Make b0 twice
    processing.run("native:fixgeometries", {
        'INPUT': f"delimitedtext://file:///{csv_file}?type=csv&delimiter=%5Ct;&maxFields=10000&detectTypes=yes&wktField=gt_geometria&crs=EPSG:4326",
        'METHOD': 1,
        'OUTPUT': file
        }
    )