#!/usr/bin/env python
"""
Copyright 2003-now Nick Chaplahin
Library of procedures.
- for image pre-processing
- for image processing
- for metadata calculation
"""
import json
import cv2
import math


# Grayscale Type of Grayscale
def f_grayscale(cr, cg, cb):
    """
    Procedure to calculate Grayscale mode basing on Grayscale Formula.
    By >>3 reducing number of Figures to 32 (256/8)
    """
    return int(0.2990 * float(cr) + 0.5870 * float(cg) + 0.1140 * float(cb))


def f_brightlevel(cr, cg, cb):
    """
    Procedure to calculate Grayscale mode basing on Brightness.
    By >>3 reducing number of Figures to 32 (256/8)
    """
    cmin = int(min(cr, cg, cb))
    cmax = int(max(cr, cg, cb))
    return (cmin + cmax) // 2


# Brightness Type of Grayscale all 3
def f_allbrightlevel(cr, cg, cb):
    """
    Procedure to calculate Grayscale mode basing on Brightness.
    Taking into consideration all 3 colors brightness levels.
    By >>3 reducing number of Figures to 32 (256/8)
    """
    return (int(cr) + int(cg) + int(cb)) // 3


def f_isneighbor(dots, i, j, bound=3):
    """
    Procedure to check if Pixel is on Outline of the Figure.
    If there is one neigbor from different Figure (different color) - it is on Outline.
    """
    if abs(dots[i][j] - dots[i - 1][j - 1]) > bound:
        return True
    if abs(dots[i][j] - dots[i - 1][j]) > bound:
        return True
    if abs(dots[i][j] - dots[i - 1][j + 1]) > bound:
        return True
    if abs(dots[i][j] - dots[i][j - 1]) > bound:
        return True
    if abs(dots[i][j] - dots[i][j + 1]) > bound:
        return True
    if abs(dots[i][j] - dots[i + 1][j - 1]) > bound:
        return True
    if abs(dots[i][j] - dots[i + 1][j]) > bound:
        return True
    if abs(dots[i][j] - dots[i + 1][j + 1]) > bound:
        return True
    return False


def f_getdelta(sv_vctr, nw_vctr, threshold):
    """
    Procedure to calculate distance between 2 vectors.
    Vector[32] used for quick filter.  It is is Sum of all other values in the vector (vector[0]+vector[1]+...)
    If distance between Vectors[32] of 2 vectors bigger than threshold - no need to calculate more, they not similar
    If less - then variants are possible, and actual distance is calculated
    """
    max_delta = int(min(sv_vctr[32], nw_vctr[32]) * threshold / 100)
    if abs(sv_vctr[32] - nw_vctr[32]) <= max_delta:
        curr_delta = 0
        for z in range(32):
            curr_delta += abs(sv_vctr[z] - nw_vctr[z])
            if curr_delta > max_delta:
                return False, 0
        return True, curr_delta
    return False, 0


def f_saveprocessed(data):
    """
    Procedure to save Meta-data data structure to file.
    """
    try:
        with open("imgSimMetadata.json", "w") as fp:
            json.dump(data, fp)
    except:
        print("ERROR:    Metadata can not be saved to imgSimMetadata.json in current folder")


def f_loadprocessed(THRESHOLD):
    """
    Procedure to load stored metadata from file.
    if error occurs for any reason - new, empty data strcuture is created
    """
    tmp_set = {"version": ["v0.1", THRESHOLD], "metadata": []}
    max_group = 0
    try:
        with open("imgSimMetadata.json", "r") as fp:
            tmp_set = json.load(fp)
        if tmp_set["version"][1] == THRESHOLD:
            for idx in range(len(tmp_set["metadata"])):
                if tmp_set["metadata"][idx][2] > max_group:
                    max_group = tmp_set["metadata"][idx][2]
        else:
            for idx in range(len(tmp_set["metadata"])):
                tmp_set["metadata"][idx][2] = 0
    except:
        print("ERROR:    Metadata can not be loaded from imgSimMetadata.json in current folder")
    return tmp_set, max_group


def f_printerr():
    """
    Procedure to display script usage arguments and examples.
    """
    print("Usage is:")
    print("")
    print("Mandatory params:")
    print("    -p  - Path to folder where images are located. Processed images in folder and sub folders.")
    print("    or ")
    print("    -r  - Re-calculate saved metadata with new similarity threshold. No new images processing.")
    print("    or ")
    print("    -d  - Calculate and display distance between image vectors - number and % of lowest vector.")
    print("")
    print("Optional params:")
    print("    -t <0 ... 100>  - Threshold for images similarity <0 ... 100>, default 4")
    print("                      0 - only copies are similar, 100 - all are similar. Recommended between 1 and 5.")
    print("    -s  - Silent, no output of similar images")
    print("    -x  - Scale images before processing. Increases processing speed, reduces accuracy.")
    print("    -P  - Color processing procedure. Values:grayscale, brightlevel, allbrightlevel. Default: grayscale")
    print("")
    print("Examples:")
    print("    To process all images in the folder and see similarity groups:")
    print("        python imgsearch.py -p <path to folder with images>")
    print("    To check processed images for similarity with another similarity threshold")
    print("        python imgsearch.py -r -t 5")
    print("    To process all images in the folder and store meta-data without displaying similarity groups:")
    print("        python imgsearch.py -p /home/user/images -s")
    print("    To re-calculate similarity of images without processing, using meta-data, with different threshold:")
    print("        python imgsearch.py -r -t 5")
    print("    To calculate and display distance between two images image 1 and image 2")
    print("        python imgsearch.py -d /home/user/images/image1.jpg /home/user/images/image2.tif -P atan2")


def f_update_groups(metadata, index, group1, group2):
    for idx in range(index):
        if metadata[idx][2] == group1:
            metadata[idx][2] = group2
    return metadata


def f_calcsimgroups(metadata, max_sim_group, THRESHOLD):
    """
    Procedure to group similar images calculating distance between neta-data vectors
    For every image in meta-data list,  calculating distance between image's meta-data vector
    and meta-data vectors of each other images in the list.
    If distance is less than configured Similarity threshold - images are treated as similar.

    To simplify the logic, in this case as similar image treated only one image with lowest distance.
    """
    for idx_i in range(1, len(metadata)):
        base_vector = metadata[idx_i][1]
        curr_threshold = float(THRESHOLD)
        curr_sim_grp_id = -1
        for idx_j in range(idx_i):
            compare_vector = metadata[idx_j][1]
            is_similar, curr_delta = f_getdelta(base_vector, compare_vector, curr_threshold)
            if is_similar:
                curr_sim_grp_id = idx_j
                if curr_delta == 0:
                    break
                else:
                    tmp = curr_delta / min(compare_vector[32], base_vector[32])
                    if tmp < curr_threshold:
                        curr_threshold = tmp
        if curr_sim_grp_id > -1:
            if metadata[curr_sim_grp_id][2] > 0:
                metadata[idx_i][2] = metadata[curr_sim_grp_id][2]
            else:
                max_sim_group += 1
                metadata[curr_sim_grp_id][2] = max_sim_group
                metadata[idx_i][2] = max_sim_group
    return metadata, max_sim_group


# ----------------IMAGE PROCESS
def f_imgread(image_path):
    return cv2.imread(image_path)


def f_scaleimg(img, min_size=400):
    xsize = img.shape[0]
    ysize = img.shape[1]
    if xsize < ysize:
        ysize = int(ysize / xsize * min_size)
        xsize = min_size
    else:
        xsize = int(xsize / ysize * min_size)
        ysize = min_size
    dim = (ysize, xsize)
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
