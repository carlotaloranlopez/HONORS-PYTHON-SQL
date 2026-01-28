# --------------------------------------------------------------------------------------------
# This script computes zonal histograms for buffer polygons in the 500m cluster 
# using land use rasters. Results are saved as buffer-year .csv files inside buffer folders 
# b500_cluster_b*, found in the clean data folder, under DEFORESTATION/CLUSTERS/250_cluster.
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
buffers = [
    "b0",
    "b500",
    "b1000",
    "b1500",
    "b2000",
    "b2500",
    "b3000",
    "b3500",
    "b4000",
    "b4500",
    "b5000"
]


# --------------------------------------------------------------------------------------------
# Fix geometries and calculate histogram for all buffers > 0
# --------------------------------------------------------------------------------------------

for b in buffers:
    # Fix geometries
    input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b500_cluster/b500_cluster_{b}/b500_cluster_{b}_ring_prot.shp"
    fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b500_cluster/b500_cluster_{b}/b500_cluster_{b}_ring_prot_fixed.shp"

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
        output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/CLUSTERS/b500_cluster/b500_cluster_{b}/b500_cluster_{b}_cover{y}_prot.csv"

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
input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b500_cluster/b500_cluster_b0/b500_cluster_b0_prot.shp"
fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b500_cluster/b500_cluster_b0/b500_cluster_b0_prot_fixed.shp"

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
    output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/CLUSTERS/b500_cluster/b500_cluster_b0/b250_cluster_b0_cover{y}_prot.csv"

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
            
# Delete helper file
delete_shapefile(fixed_vector)