# HONORS: PYTHON & SQL PORTION

## BUFFERS FOLDER
This folder contains Python scripts to construct buffers for the 100m and near-far specifications, with and without farm estimates, and compute thier zonal histograms based on land cover rasters. Scripts are designed to be run sequentially and rely on intermediate shapefiles. Running all scripts together may crash (hence why I separated them), and our lab computers need babysitting. Independent files run fine in the lab, but some take several hours.

### SETUP: 
Make sure the relevant paths exist! Below is an outline.

Buffers are constructed from gleba shapefiles, which come from the SICOR. These files were given as wkt geometries in .csv format. I cleaned the raw files in STATA and removed outliers in GIS (see Appendix A). The clean file has unique contract identifier contract_recipient_id. This file is stored in the clean data folder, under CREDIT/GLEBAS/glebas_matched_nooutliers. Land use rasters are stored in the raw data folder, under DEFORESTATION_DATA/Mapbiomas.

In the 01_FARMS (F) folder, I use a farm estimate of farm area created by dissolving overlapping contract geometries. The 02_NO_FARMS (G) folder considers the first buffer to be the polt associated with a contract, without taking the union of overlapping geometries. Each of these folders creates buffers at 1000m increments from the border (100M) and near-far buffers at 2 constant jumps of 250, 500, 750, and 1000m (NF).

The 03_CLUSTERS folder creates farm clusters by dissolving overlapping buffers from the folders above at different distances, 250, 500, 750, 1000. These become the cluster's buffer 0 and more buffers are created around them. I first create several buffers at the constant distance at which they were dissolved, i.e., in 250m increments for buffers dissolved at 250m, 500m increments for the 500m cluster, and so on. I might create near-far estimates for these once I run the regression...


### 01 FARMS (F)
I use a farm estimate of farm area created by dissolving overlapping contract geometries. This folder creates buffers at 1000m increments from the border (100M) and near-far buffers at 2 constant jumps of 250, 500, 750, and 1000m (NF).

#### 01.1 FARMS: MAKE BUFFER 0
This file makes farm plot shapefiles, which I call buffer 0. It does so by dissolving all geometries that overlap in the clean SICOR gleba files, creating new identifiers, FID. It makes the file twice, one for the near-far specification (NF) and another for the 100m specification (100M). They are saved to folders CREDIT/GLEBAS/FARMS/NF_BUFFERS/b0 and CREDIT/GLEBAS/FARMS/100M_BUFFERS/b0 in the clean data folder, respectively. This takes about 1 hour.

#### 01.2 FARMS: MATCH FARM TO CONTRACT
This script take the b0 file created (which identifies unique farms with ID variable FID) and calculates its overlap with contract polygons to determine how many times a farm received credit and retreive its characteristics. It outputs a .csv file with variables farm_id (which is really the contract ID), FID (which is really the farm ID), and year. Saved as farm_to_contract in the clean data folder, under CREDIT/GLEBAS. This takes about 8 hours... for some cursed reason.

#### 01.3 FARMS: MAKE BUFFERS, 100M AND NF
Each of these files makes buffers from b0 at different distances for each specification (NF and 100M). They are saved to folders CREDIT/GLEBAS/FARMS/**specification**_BUFFERS/b**distance** as b**distance**. The NF specification makes pairs (250-500, 500-1000, 750-1500, 1000-2000), and the 100M specification makes buffers at multiples of 100m until reaching 2000. One meter is approximated to 9.0785x10^-6 decimal degrees (see Appendix A). This takes 15 minutes for the NF specification, and 30 for the 100M specification.

#### 01.4 FARMS: MAKE RINGS, 100M AND NF
These files convert buffers at all distances into disjoint rings by subtracting inner buffer overlap, for both specifications. They are saved to folders CREDIT/GLEBAS/FARMS/**specification**_BUFFERS/b**distance** as b**distance**_ring. This runs in about 45m for the NF specification and 1.5h for the 100M specification.

#### 01.5 FARMS: REMOVE PROTECTED AREAS, 100M AND NF
These files remove overlap with protected areas from all buffers (including b0), and both specifications. They are saved to folders CREDIT/GLEBAS/FARMS/**specification**_BUFFERS/b**distance** as b**distance**_ring_prot. This runs in about 1h for the NF specification and 1.5h for the 100M specification.

#### 01.6. FARMS: ZONAL HISTOGRAM 1 (PROT), 100M AND NF
These files compute zonal histograms for each buffer–year combination using Mapbiomas rasters. Each new variable represents a pixel count of all unique values from the raster, for each polygon. Output from this script is saved as several .csv files in the clean data folder, under DEFORESTATION/FARMS/**specification**_BUFFERS/b**distance**. This takes about 1.5h for the NF specification and 3h for the 100M specification.

#### 01.7 FARMS: STUVA CHECK, NF ONLY
WIP

#### 01.8 FARMS: HISTOGRAM 2 (STUVA), NF ONLY
WIP

#### 01.9. FARMS: REMOVE PUBLIC LAND, NF ONLY
WIP

#### 01.10. FARMS: ZONAL HISTOGRAM 3 (PRIVATE), NF ONLY
WIP


### 02 NO FARMS (G)
I consider b0 to be the plot itself. This folder creates buffers at 1000m increments from the border (100M) and near-far buffers at 2 constant jumps of 250, 500, 750, and 1000m (NF). It follows the same steps as above, without but without an equivalent script to 01_02 (because there is no farm id).


### 03 CLUSTERS
This folder creates farm clusters by dissolving overlapping buffers from the folders above at different distances, 250, 500, 750, 1000. These become the cluster's buffer 0 and more buffers are created around them. I first create several buffers at the constant distance at which they were dissolved, i.e., in 250m increments for buffers dissolved at 250m, 500m increments for the 500m cluster, and so on. I might create near-far estimates for these once I run the regression...


#### 03.1 CLUSTERS: MAKE CLUSTERS
This script dissolves geometries that overlap at three distances: 250, 500, 750, and 1000 (which correspond with the NF treatment buffer) to create clusters. These become the buffer 0 for their cluster, and they are saved to folders DATA/DATA_CLEAN/CREDIT/GLEBAS/CLUSTERS/b**clusterdistance**_cluster as b**clusterdistance**_cluster_b0.shp.

#### 03.2 CLUSTERS: FARM TO CLUSTER
This scripts obtains the farms that are contained in each buffer at each distance, saved in folder DATA/DATA_CLEAN/CREDIT/GLEBAS as cluster**clusterdistance**_to_farm_id.csv

#### 03.3 CLUSTERS: MAKE CLUSTER BUFFERS, AT EACH CLUSTER DISTANCE
These scripts make a sequence of buffers around each cluster. The increment between buffers is determined by the size of the buffer, i.e., 250m increments for buffers dissolved at 250m, 500m increments for the 500m cluster, and so on. They are saved to each cluster-distance folder, inside a buffer sub-folder as b**clusterdistance**_cluster_b**maxdistance**.

#### 03.4 CLUSTERS: MAKE CLUSTER RINGS, AT EACH CLUSTER DISTANCE
These scripts compute the symmetric difference of each buffer in each cluster with interior buffers, saved to each cluster-distance folder, inside a buffer sub-folder as b**clusterdistance**_cluster_b**maxdistance**_ring.

#### 03.5 CLUSTERS: CROP CLUSTER TO PROTECTED LAND, AT EACH CLUSTER DISTANCE
These files crop all buffers, including b0, at all cluster distances to non-protected land. Files are saved to each cluster-distance folder, inside a buffer sub-folder as b**clusterdistance**_cluster_b**maxdistance**_ring_prot.

#### 03.6 CLUSTERS: ZONAL HISTOGRAM, AT EACH CLUSTER DISTANCE
These files compute zonal histograms for each buffer–year combination using Mapbiomas rasters. Each new variable represents a pixel count of all unique values from the raster, for each polygon. Output from this script is saved as several .csv files in the clean data folder, under DEFORESTATION/CLUSTERS/b**clusterdistance**_cluster/b**clusterdistance**_cluster_b**maxdistance**/b**clusterdistance**_cluster_b**maxdistance** with name b**clusterdistance**_cluster_**maxdistance**_cover**year**_prot.csv.


### 04 GET BUFFER, CLUSTER INFORMATION
This folder will get buffer information such as area, state, distance to other farms, etc. 


### Path outline:
    CREDIT_DEFOREST
        DATA
            DATA_CLEAN
                CREDIT
                    GLEBAS
                        glebas_matched_nooutliers <-- clean gleba .csv lived here
                        FARMS
                            NF_BUFFERS <-- buffer shapefiles are here, in their own folder each
                            100M_BUFFERS  <-- buffer shapefiles are here, in their own folder each
                        NO_FARMS
                            NF_BUFFERS
                            100M_BUFFERS 
                        CLUSTERS
                            b250_cluster <-- cluster shapefiles and buffers around them will appear here, in their own sub-buffer folder each
                            b500_cluster
                            b1000_cluster
                            b2000_cluster
                DEFORESTATION
                    FARMS
                        NF_BUFFERS <-- zonal histogram csv files are saved here!
                        100M_BUFFERS <-- zonal histogram csv files are saved here!
                    NO_FARMS
                        NF_BUFFERS
                        100M_BUFFERS
                    CLUSTERS
                        b250_cluster <-- cluster zonal histograms saved here!
                        b500_cluster
                        b750_cluster
                        b1000_cluster
            DATA_RAW
                DEFORESTATION
                    Mapbiomas <-- land use files live here
            SHAPEFILES
                Brazil_UCS <-- protected land shapefiles live here
                

## CLASSIFY CONTRACTS FOLDER
 This folder contains two scripts to re-classify credit contracts into cost and investment categories (see Theoretical Framework), edited but heavily written by ChatGPT. They use two strict definitions for cost credit, discussed in the Appendix, one more restrictive than the other. The scripts input the contract file 'operacao_gleba_master', cleaned in STATA, and output two re-classified files, 'classifyA.csv' and 'classifyB.csv', mapping contract IDs to the new classification. Both files are found in folder 'CREDIT/OPERACAO_GLEBA'. Run this script on the local terminal.

## (SOME) SUMMARY STATISTICS FOLDER
This folder contains SQL queries to obtain summary statistics included from several rounds of agricultural surveys. 