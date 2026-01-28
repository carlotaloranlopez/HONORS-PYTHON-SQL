# --------------------------------------------------------------------------------------------
# This file obtains farm IDs contained in each cluster
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

import os
import processing
from qgis.core import QgsProcessingFeatureSourceDefinition, QgsFeatureRequest

def delete_shapefile(path):
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        p = path.replace(".shp", ext)
        if os.path.exists(p):
            os.remove(p)

# Base directories
buffers_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
clusters_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/"
out_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/"

# Inputs
b0 = os.path.join(buffers_dir, "b0/b0.shp")
b0_fixed = os.path.join(buffers_dir, "b0/b0_fixed.shp")

clusters = [
    (
        os.path.join(clusters_dir, "b250_cluster/b250_cluster_b0/b250_cluster_b0.shp"),
        os.path.join(clusters_dir, "b250_cluster/b250_cluster_b0/b250_cluster_b0_fixed.shp"),
        os.path.join(out_dir, "cluster250_to_farm_id.csv")
    ),
    (
        os.path.join(clusters_dir, "b500_cluster/b500_cluster_b0/b500_cluster_b0.shp"),
        os.path.join(clusters_dir, "b500_cluster/b500_cluster_b0/b500_cluster_b0_fixed.shp"),
        os.path.join(out_dir, "cluster500_to_farm_id.csv")
    ),
    (
        os.path.join(clusters_dir, "b1000_cluster/b1000_cluster_b0/b1000_cluster_b0.shp"),
        os.path.join(clusters_dir, "b1000_cluster/b1000_cluster_b0/b1000_cluster_b0_fixed.shp"),
        os.path.join(out_dir, "cluster1000_to_farm_id.csv")
    ),
    (
        os.path.join(clusters_dir, "b750_cluster/b750_cluster_b0/b750_cluster_b0.shp"),
        os.path.join(clusters_dir, "b750_cluster/b750_cluster_b0/b750_cluster_b0_fixed.shp"),
        os.path.join(out_dir, "cluster750_to_farm_id.csv")
    )
]

# Delete existing outputs
delete_shapefile(b0_fixed)
for _, fixed, out in clusters:
    delete_shapefile(fixed)
    delete_shapefile(out)


# --------------------------------------------------------------------------------------------
# FIX GEOMETRIES
# --------------------------------------------------------------------------------------------

processing.run(
    "native:fixgeometries",
    {
        "INPUT": b0,
        "METHOD": 1,
        "OUTPUT": b0_fixed
    }
)
for src, fixed, _ in clusters:
    processing.run(
        "native:fixgeometries",
        {
            "INPUT": src,
            "METHOD": 1,
            "OUTPUT": fixed
        }
    )

# --------------------------------------------------------------------------------------------
# DROP IF BAD GEOMETRY
# --------------------------------------------------------------------------------------------

b0_src = QgsProcessingFeatureSourceDefinition(
    b0_fixed,
    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
)
cluster_sources = []
for _, fixed, _ in clusters:
    cluster_sources.append(
        QgsProcessingFeatureSourceDefinition(
            fixed,
            flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
            geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
        )
    )


# --------------------------------------------------------------------------------------------
# JOIN BY LOCATION
# --------------------------------------------------------------------------------------------

for i in range(len(clusters)):
    # get the cluster feature source
    cluster_src = cluster_sources[i]

    # get output path from clusters list
    cluster_info = clusters[i]
    output_csv = cluster_info[2]

    # join farms to clusters
    processing.run(
        "native:joinattributesbylocation",
        {
            "INPUT": cluster_src,
            "PREDICATE": [1, 2, 4],
            "JOIN": b0_src,
            "JOIN_FIELDS": ["fid"],
            "METHOD": 0,
            "DISCARD_NONMATCHING": False,
            "PREFIX": "c",
            "OUTPUT": output_csv
        }
    )
