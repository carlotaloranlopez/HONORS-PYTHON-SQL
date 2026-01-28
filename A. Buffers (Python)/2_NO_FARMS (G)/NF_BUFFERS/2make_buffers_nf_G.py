# --------------------------------------------------------------------------------------------
# This file takes a buffer 0 shapefile and creates buffers (for the near-far specification) at
# several different distances. These files are saved to each buffer sub-folder with name b*, 
# inside CREDIT/GLEBAS/NO_FARMS/NF_BUFFERS. 
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/NO_FARMS/NF_BUFFERS/"
buffers_nf = {
    "250": 0.00227,
    "500_1": 0.004539,
    "500_2": 0.004539,
    "750": 0.006809,
    "1000_1": 0.009079,
    "1000_2": 0.009079,
    "1500": 0.013618,
    "2000": 0.018157
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
