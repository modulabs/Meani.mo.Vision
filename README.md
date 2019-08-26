# Meani.mo.Vision
This repository is for meani.mo project users.

# Getting Start 

> python main.py -d ./images/drone1.bmp -l ./images/lidar1.bmp -o ./output.bmp
> 
|argument|shortened|description|example|
|-|-|-|-|
|`--drone_path` |`-d`|drone image path for loading|-d ./images/drone1.bmp |
|`--lidar_path`|`-l`|lidar image path for loading|-l ./images/lidar.bmp|
|`--dst_path`|`-o`|output image path for saving|-o ./result.bmp|


# PEP8 Git Commit Hook
This is a pre-commit hook for Git that checks the code to be committed for Python PEP8 style compliance. The hook will prevent the commit in case style violations are detected.

[see this for installation and applying yours](https://github.com/cbrueffer/pep8-git-hook)
