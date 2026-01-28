# --------------------------------------------------------------------------------------------
# This file takes a cluster 750 shapefile and creates buffers at multiples of 750m from
# its border. These files are saved to each buffer sub-folder in foler with name 
# b750_cluster_b* inside CREDIT/GLEBAS/CLUSTERS/b750_cluster.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b750_cluster/"
buffers = {
    "750": 0.006809,
    "1500": 0.013618,
    "2250": 0.020427,
    "3000": 0.027235,
    "3750": 0.034044,
    "4500": 0.040853
}
input_vector = f"{cd}b750_cluster_b0/b750_cluster_b0_fixed.shp"


# --------------------------------------------------------------------------------------------
# Make buffers
# --------------------------------------------------------------------------------------------

for b in buffers:
    # Define output file name and get distance from dictionary
    output_vector = f"{cd}b750_cluster_b{b}/b750_cluster_b{b}.shp"
    degrees = buffers[b]
    
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