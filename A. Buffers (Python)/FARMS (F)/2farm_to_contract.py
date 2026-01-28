# --------------------------------------------------------------------------------------------
# This script take the b0 file created (which identifies unique farms with ID variable FID) 
# and calculates its overlap with contract polygons to determine how many times a farm received 
# credit and retreive its characteristics. It outputs a .csv file with variables farm_id 
# (which is really the contract ID), FID (which is really the farm ID), and year. Saved as 
# farm_to_contract in the clean data folder, under CREDIT/GLEBAS/FARMS.
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

# Set working directory and file paths
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/"
farm_file = os.path.join(cd, "FARMS/NF_BUFFERS/b0/b0.shp")
farm_fixed = os.path.join(cd, "FARMS/NF_BUFFERS/b0/b0_fixed.shp")
gleba_file = os.path.join(cd, "glebas_matched_master_nooutliers/glebas_matched_master_nooutliers.shp")
gleba_fixed = os.path.join(cd, "glebas_matched_master_nooutliers/glebas_matched_master_nooutliers_fixed.shp")
farm_to_contract = os.path.join(cd, "glebas_farm_to_contract_id.csv")


# --------------------------------------------------------------------------------------------
# FIX GEOMETRIES
# --------------------------------------------------------------------------------------------

# Fix farm and gleba geometries
processing.run("native:fixgeometries", {
    'INPUT': farm_file,
    'METHOD': 1,
    'OUTPUT': farm_fixed
})

processing.run("native:fixgeometries", {
    'INPUT': gleba_file,
    'METHOD': 1,
    'OUTPUT': gleba_fixed
})

farm_src = QgsProcessingFeatureSourceDefinition(
    farm_fixed,
    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
)

gleba_src = QgsProcessingFeatureSourceDefinition(
    gleba_fixed,
    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
)


# --------------------------------------------------------------------------------------------
# MERGE BY LOCATION
# --------------------------------------------------------------------------------------------

# Merge 1:m
processing.run("native:joinattributesbylocation", {
    'INPUT': farm_src,
    'PREDICATE':[1,2,4],
    'JOIN': gleba_src,
    'JOIN_FIELDS':['contract_r'],
    'METHOD':0,
    'DISCARD_NONMATCHING':False,
    'PREFIX':'',
    'OUTPUT':farm_to_contract
})

# Delete helper files
delete_shapefile(farm_fixed)
delete_shapefile(gleba_fixed)