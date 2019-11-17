# Meani.mo.Vision
This repository is for meani.mo project users.

# Getting Start 

|argument|shortened|default|description|example|
|-|-|-|-|-|
|`--drone_path` |`-d`|no default|drone image path for loading|-d ./images/drone1.bmp |
|`--lidar_path`|`-l`|no default|lidar image path for loading|-l ./images/lidar.bmp|
|`--dst_path`|`-o`|no default|output image path for saving|-o ./result.bmp|
|`--experiment_num`|`-e`|no default|`Experiment Number`|-e 18|
|`--drone_folder_path`|`-s`|no default|Path in which drone image folder is located|-s ./CASE_1/images|
|`--pcl_path`|`-l`|no default|Path in which lidar image is located|-l ./CASE_1/images|
|`--drone_mask_path`|`-m`|no default|Path in which mask image is located|-m ./CASE_1/mask(predict)|
|`--find_good_match`|none|True|||
|`--pcl_mask`|none|True|Applying binary mask to a pcl image||
|`--ransac_maxIters`|none|100000|The maximum number of RANSAC iterations, 2000 is the maximum it can be.||
|`--ransac_confidence`|none|0.995|Confidence level, between 0 and 1 (default:0.995).||
|`--SIFT_nfeatures`|none|0|The number of best features to retain. The features are ranked by their scores (default:0)||
|`--SIFT_nOctaveLayers`|none|3|The number of layers in each octave. 3 is the value used in D (default=3).'||
|`--SIFT_contrastThreshold`|none|0.04|The contrast threshold used to filter out weak features in semi-uniform (low-contrast) regions.||
|`--SIFT_edgeThreshold`|none|50|The threshold used to filter out edge-like features.||
|`--SIFT_sigma`|none|1.6|The sigma of the Gaussian applied to the input image at the octave #0.||

|`--debug`|none|True|Imshow Intermediate Results||
|`--save_video`|none|True|Record result video for making GIF||
|`--save_csv`|none|True|Save csv||
|`--save_masked_pcl`|none|True|Save masked pcl image||
|`--save_masked_drone`|none|True|Save masked drone image||
|`--save_matching`|none|True|Save matching images||
|`--save_keypoints`|none|True|Save keypoints images||


# PEP8 Git Commit Hook
This is a pre-commit hook for Git that checks the code to be committed for Python PEP8 style compliance. The hook will prevent the commit in case style violations are detected.

[see this for installation and applying yours](https://github.com/cbrueffer/pep8-git-hook)
