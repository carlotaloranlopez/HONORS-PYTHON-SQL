

private_dir= "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/SHAPEFILES/CAR/TO_area_imovel/TO_private_property.shp"
buffers_dir = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS"

# Input / output paths
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
]


processing.run("native:clip", {
    'INPUT':'glebas_matched_master_nooutliers/glebas_matched_master_nooutliers.shp',
    'OVERLAY': private_dir,
    'OUTPUT':'TEMPORARY_OUTPUT'
})