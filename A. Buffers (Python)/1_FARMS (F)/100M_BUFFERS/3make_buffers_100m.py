# --------------------------------------------------------------------------------------------
# This file takes a buffer 0 shapefile and creates buffers (for the 100m specification) at
# multiples of 100 meters. These files are saved to each buffer sub-folder in foler with name 
# b* inside CREDIT/GLEBAS/FARMS/100M_BUFFERS. Note: can also use the multi buffer function.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/"
buffers_100 = {
    "100": 0.0009079,
    "200": 0.0018157,
    "300": 0.0027235,
    "400": 0.0036314,
    "500": 0.0045392,
    "600": 0.0054471,
    "700": 0.0063550,
    "800": 0.0072628,
    "900": 0.0081707,
    "1000": 0.0090785,
    "1100": 0.0099864,
    "1200": 0.0108942,
    "1300": 0.0118021,
    "1400": 0.0127099,
    "1500": 0.0136178,
    "1600": 0.0145256,
    "1700": 0.0154335,
    "1800": 0.0163413,
    "1900": 0.0172492,
    "2000": 0.018157
}
input_vector = f"{cd}b0/b0.shp"


# --------------------------------------------------------------------------------------------
# Make buffers
# --------------------------------------------------------------------------------------------

for b in buffers_100:
    # Define output file name and get distance from dictionary
    output_vector = f"{cd}b{b}/b{b}.shp"
    degrees = buffers_100[b]
    
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