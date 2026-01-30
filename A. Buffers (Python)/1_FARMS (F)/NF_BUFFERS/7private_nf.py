# --------------------------------------------------------------------------------------------
# This script fixes buffer geometries and clips them to private property polygons
# Buffers: b0, b250, b500_1, b500_2, b750, b1000_1, b1000_2, b1500, b2000
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

import os
import processing

def delete_shapefile(path):
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        p = path.replace(".shp", ext)
        if os.path.exists(p):
            os.remove(p)

private_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/SHAPEFILES/CAR/ALL_area_imovel/ALL_private_property.shp"
buffers_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS"

# --------------------------------------------------------------------------------------------
# INPUT / OUTPUT PATHS
# --------------------------------------------------------------------------------------------

sources = [
    (
        os.path.join(buffers_dir, "b0/b0_prot.shp"),
        os.path.join(buffers_dir, "b0/b0_prot_fixed.shp"),
        os.path.join(buffers_dir, "b0/b0_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b250/b250_ring_prot.shp"),
        os.path.join(buffers_dir, "b250/b250_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b250/b250_ring_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b500_1/b500_1_ring_prot.shp"),
        os.path.join(buffers_dir, "b500_1/b500_1_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b500_1/b500_1_ring_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b500_2/b500_2_ring_prot.shp"),
        os.path.join(buffers_dir, "b500_2/b500_2_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b500_2/b500_2_ring_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b750/b750_ring_prot.shp"),
        os.path.join(buffers_dir, "b750/b750_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b750/b750_ring_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b1000_1/b1000_1_ring_prot.shp"),
        os.path.join(buffers_dir, "b1000_1/b1000_1_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b1000_1/b1000_1_ring_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b1000_2/b1000_2_ring_prot.shp"),
        os.path.join(buffers_dir, "b1000_2/b1000_2_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b1000_2/b1000_2_ring_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b1500/b1500_ring_prot.shp"),
        os.path.join(buffers_dir, "b1500/b1500_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b1500/b1500_ring_prot_priv.shp")
    ),
    (
        os.path.join(buffers_dir, "b2000/b2000_ring_prot.shp"),
        os.path.join(buffers_dir, "b2000/b2000_ring_prot_fixed.shp"),
        os.path.join(buffers_dir, "b2000/b2000_ring_prot_priv.shp")
    ),
]

# --------------------------------------------------------------------------------------------
# DELETE EXISTING OUTPUTS
# --------------------------------------------------------------------------------------------

for _, fixed, clipped in sources:
    delete_shapefile(fixed)
    delete_shapefile(clipped)

# --------------------------------------------------------------------------------------------
# FIX GEOMETRIES
# --------------------------------------------------------------------------------------------

for src, fixed, _ in sources:
    processing.run(
        "native:fixgeometries",
        {
            "INPUT": src,
            "METHOD": 1,
            "OUTPUT": fixed
        }
    )

# --------------------------------------------------------------------------------------------
# CLIP TO PRIVATE PROPERTY
# --------------------------------------------------------------------------------------------

for _, fixed, clipped in sources:
    processing.run(
        "native:clip",
        {
            "INPUT": fixed,
            "OVERLAY": private_dir,
            "OUTPUT": clipped
        }
    )
