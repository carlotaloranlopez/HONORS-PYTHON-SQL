# --------------------------------------------------------------------------------------------
# This file takes a cluster 250 shapefile and creates buffers at multiples of 250m from
# its border. These files are saved to each buffer sub-folder in foler with name 
# b250_cluster_b* inside CREDIT/GLEBAS/CLUSTERS/b250_cluster.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b250_cluster/"
buffers = {
    "250": 0.0022696,
    "500": 0.0045392,
    "750": 0.0068089,
    "1000": 0.0090785,
    "1250": 0.0113481,
    "1500": 0.0136178,
    "1750": 0.0158874,
    "2000": 0.018157
}
input_vector = f"{cd}b250_cluster_b0/b250_cluster_b0_fixed.shp"


# --------------------------------------------------------------------------------------------
# Make buffers
# --------------------------------------------------------------------------------------------

for b in buffers:
    # Define output file name and get distance from dictionary
    output_vector = f"{cd}b250_cluster_b{b}/b250_cluster_b{b}.shp"
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