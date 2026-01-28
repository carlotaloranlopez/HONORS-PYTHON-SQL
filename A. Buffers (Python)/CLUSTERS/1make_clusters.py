# --------------------------------------------------------------------------------------------
# This script dissolves overlapping buffers at 250, 500, 1000, 2000m to make clusters.
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
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
source250= os.path.join(cd, "b250/b250.shp")
source250_f= os.path.join(cd, "b250/b250_fixed.shp")
source500= os.path.join(cd, "b500/b500.shp")
source500_f= os.path.join(cd, "b500/b500_fixed.shp")
source1000= os.path.join(cd, "b1000/b1000.shp")
source1000_f= os.path.join(cd, "b1000/b1000_fixed.shp")
source2000= os.path.join(cd, "b2000/b2000.shp")
source2000_f= os.path.join(cd, "b2000/b2000_fixed.shp")
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/"
cluster250= os.path.join(cd, "b250_cluster/b250_cluster.shp")
cluster500= os.path.join(cd, "b500_cluster/b500_cluster.shp")
cluster1000= os.path.join(cd, "b1000_cluster/b1000_cluster.shp")
cluster2000= os.path.join(cd, "b2000_cluster/b2000_cluster.shp")

# Delete existing outputs if they exist
for f in [source250_f, source500_f, source1000_f, source2000_f, cluster250, cluster500, cluster1000, cluster2000]:
    delete_shapefile(f)


# --------------------------------------------------------------------------------------------
# FIX SOURCE GEOMETRIES
# --------------------------------------------------------------------------------------------

processing.run("native:fixgeometries", {
    'INPUT': source250,
    'METHOD': 1,
    'OUTPUT': source250_f
    }
)
processing.run("native:fixgeometries", {
    'INPUT': source500,
    'METHOD': 1,
    'OUTPUT': source500_f
    }
)
processing.run("native:fixgeometries", {
    'INPUT': source1000,
    'METHOD': 1,
    'OUTPUT': source1000_f
    }
)
processing.run("native:fixgeometries", {
    'INPUT': source2000,
    'METHOD': 1,
    'OUTPUT': source2000_f
    }
)


# --------------------------------------------------------------------------------------------
# DISSOLVE USING GDAL
# --------------------------------------------------------------------------------------------

processing.run(
    "gdal:dissolve", {
        'INPUT': source250_f,
        'FIELD':'',
        'GEOMETRY':'geometry',
        'EXPLODE_COLLECTIONS':True,
        'KEEP_ATTRIBUTES':False,
        'COUNT_FEATURES':False,
        'COMPUTE_AREA':False,
        'COMPUTE_STATISTICS':False,
        'STATISTICS_ATTRIBUTE':'',
        'OPTIONS': 'GEOMETRY_NAME=geometry -nlt MULTIPOLYGON',
        'OUTPUT': cluster250
    }
)
processing.run(
    "gdal:dissolve", {
        'INPUT': source500_f,
        'FIELD':'',
        'GEOMETRY':'geometry',
        'EXPLODE_COLLECTIONS':True,
        'KEEP_ATTRIBUTES':False,
        'COUNT_FEATURES':False,
        'COMPUTE_AREA':False,
        'COMPUTE_STATISTICS':False,
        'STATISTICS_ATTRIBUTE':'',
        'OPTIONS': 'GEOMETRY_NAME=geometry -nlt MULTIPOLYGON',
        'OUTPUT': cluster500
    }
)
processing.run(
    "gdal:dissolve", {
        'INPUT': source1000_f,
        'FIELD':'',
        'GEOMETRY':'geometry',
        'EXPLODE_COLLECTIONS':True,
        'KEEP_ATTRIBUTES':False,
        'COUNT_FEATURES':False,
        'COMPUTE_AREA':False,
        'COMPUTE_STATISTICS':False,
        'STATISTICS_ATTRIBUTE':'',
        'OPTIONS': 'GEOMETRY_NAME=geometry -nlt MULTIPOLYGON',
        'OUTPUT': cluster1000
    }
)
processing.run(
    "gdal:dissolve", {
        'INPUT': source2000_f,
        'FIELD':'',
        'GEOMETRY':'geometry',
        'EXPLODE_COLLECTIONS':True,
        'KEEP_ATTRIBUTES':False,
        'COUNT_FEATURES':False,
        'COMPUTE_AREA':False,
        'COMPUTE_STATISTICS':False,
        'STATISTICS_ATTRIBUTE':'',
        'OPTIONS': 'GEOMETRY_NAME=geometry -nlt MULTIPOLYGON',
        'OUTPUT': cluster2000
    }
)