#!/usr/bin/env python
"""
Copyright 2003-now Nick Chaplahin
Program and it's functions developed to demonstrate and test technology
for Automation of Images Similarity detection patented in
 US patent US10796197B2 - Automatic method and system for similar images and image fragments detection basing on image content
"""

import os
import sys
import argparse
from common import *



def f_processimg(img, xsize, ysize):
    """
    Procedure to calculate actual meta-data Vector of the image.
    Image is segmented by Brightness: (max brightness = min brightness) / 2
    f_bright level returns grayscale values of the pixel, in range 0-31, we have 32 figures.
    This pixel is part of the Figure, is added to Area
    If pixel has neighbor pixel of different value - it is Outline and added to Figure's outline too
    """
    avector = [0] * 32
    lvector = [0] * 32
    vector = [0] * 33
    dots = []
    for x in range(xsize):
        line = []
        for y in range(ysize):
            colr = img[x, y, 2]
            colg = img[x, y, 1]
            colb = img[x, y, 0]
            line.append(f_grayscale(int(colr), int(colg), int(colb)) >> 3)
        dots.append(line)
    for x in range(1, xsize - 1):
        for y in range(1, ysize - 1):
            avector[dots[x][y]] += 1
            if f_isneighbor(dots, x, y, 0):
                lvector[dots[x][y]] += 1
    for i in range(32):
        if avector[i] > 0:
            vector[i] = int((float(lvector[i]) / math.sqrt(avector[i])) * 100.0)
            vector[32] += vector[i]
    return vector


def run_regroup(threshold):
    """
    Procedure to re-group images re-calculating distance between their vectors using new Similarity Threshold
    uses only saved meta-data structure, not processing images (neither new or previously processed)

    Demonstrates the ability of meta-data re-usage.
    """
    print("Re-group similar images with threshold {}".format(threshold))
    set_of_vectors, max_sim_group = f_loadprocessed(threshold)
    if set_of_vectors["version"][1] == threshold:
        print("Threshold is the same. Skipping.")
    if set_of_vectors["version"][1] != threshold:
        for idx in range(len(set_of_vectors["metadata"])):
            set_of_vectors["metadata"][idx][2] = 0
        print("Grouping similar images")
        set_of_vectors["version"] = ["v0.1", threshold]
        set_of_vectors["metadata"], max_sim_group = f_calcsimgroups(set_of_vectors["metadata"], max_sim_group, threshold)
        print("Grouping similar images is finished")
    print("Displaying groups of similar images")
    for z in range(1, max_sim_group + 1):
        print("SIMILAR IMAGES GROUP{}".format(z))
        for val in set_of_vectors["metadata"]:
            if val[2] == z:
                print(val[0])
    f_saveprocessed(set_of_vectors)


def run_compare(imgfile1, imgfile2, scale):
    """
    Procedure to build vectors and compare 2 files.
    Output is a distance between vectors in absolute number and
    in % of Vector size for smallest vector - this value is comparable with Threshold
    """
    # Initial values
    # Process images with following file extension
    ext = (".jpeg", ".jpg", ".bmp", ".png", ".tif")

    # Program start
    print("Images processing is started")

    # Process all images in folder and subfolders, with file extensions listed in \"ext\"
    # if files are not images - exit
    # If file extension in supported list
    if not imgfile1.lower().endswith(tuple(ext)) or not imgfile2.lower().endswith(tuple(ext)):
        print("ERROR:     Provided files are not image files")
    # Initial data structure to store image metadata.
    # img_vector[1] - meta-data (list)
    img_vector1 = []
    img_vector2 = []
    print("Processing image {}".format(imgfile1))
    # Read image file 1 and get matrix of pixels in BRG (specifics of cv2)
    img = f_imgread(imgfile1)
    # Use scale image for processing reduce
    if scale:
        img = f_scaleimg(img, 400)
    # Get image size
    xsize = img.shape[0]
    ysize = img.shape[1]
    # Calculate vector of meta-data for image
    img_vector1 = f_processimg(img, xsize, ysize)
    print("Processing image {}".format(imgfile2))
    # Read image file 1 and get matrix of pixels in BRG (specifics of cv2)
    img = f_imgread(imgfile2)
    if scale:
        img = f_scaleimg(img, 400)
    # Get images size (for cycles)
    xsize = img.shape[0]
    ysize = img.shape[1]
    # Calculate vector of meta-data for image
    img_vector2 = f_processimg(img, xsize, ysize)
    print("Images processing is finished")
    print("Calculating the distance")
    distance = 0
    for z in range(32):
        distance += abs(img_vector1[z] - img_vector2[z])
    per_cent = int(distance / min(img_vector1[32], img_vector2[32]) * 100.0)
    print("Distance is: absolute {},  percent {} %".format(distance, per_cent))


def run_proc(input_path, threshold, silent, scale):
    """
    Procedure to build data structures, that contain images meta-data and additional data required to simplify
    images grouping by similarity.
    List of data contains entry for every image, that contains of:
       - path to image file
       - image meta-data vector
       - ID of similar images group it belongs to
    Images in same group are treated as similar.
    """
    # Initial values
    # Process images with following file extension
    ext = (".jpeg", ".jpg", ".bmp", ".png", ".tif", ".pgm", ".ppm")

    # Initiate empty meta-data set
    set_of_vectors = {}
    set_of_vectors["version"] = ["v0.1", threshold]
    set_of_vectors["metadata"] = []
    max_sim_group = 0

    # Program start
    print("Images processing is started")

    # Process all images in folder and subfolders, with file extensions listed in \"ext\"
    for r, d, f in os.walk(input_path):
        # Processing all images in Folder and Sub-Folders
        for name in f:
            # If file extension in supported list
            if name.lower().endswith(tuple(ext)):
                # print("Processing image {} {}".format(os.path.join(r, name), datetime.now()))
                print("Processing image {}".format(os.path.join(r, name)))
                # Initial data structure to store image metadata.
                # img_vector[0] - full path to file and file name
                # img_vector[1] - meta-data (list)
                # img_vector[2] - ID of Similar Images Group
                img_vector = ["", [], 0]
                # print("Read Image Start {}".format(datetime.now()))
                # Read image file and get matrix of pixels in BRG (specifics of cv2)
                img = f_imgread(os.path.join(r, name))
                # print("Read Image End {}".format(datetime.now()))
                # Get images size (for cycles)
                # Use scale image for processing reduce
                if scale:
                    img = f_scaleimg(img, 400)
                # Get images size (for cycles)
                xsize = img.shape[0]
                ysize = img.shape[1]
                # Fill in data into data structure to store meta-data
                # Path to image file and file name
                img_vector[0] = os.path.join(r, name)
                # print("Process Image Start {}".format(datetime.now()))
                # Calculate vector of meta-data for image
                img_vector[1] = f_processimg(img, xsize, ysize)
                # print("Process Image End {}".format(datetime.now()))
                # Add image vector to list of vectors
                set_of_vectors["metadata"].append(img_vector)
    print("Images processing is finished")
    print("Grouping similar images")
    # To store threshold that will be used to form groups of similar images
    set_of_vectors["version"] = ["v0.1", threshold]
    # Call procedure to group similar images
    set_of_vectors["metadata"], max_sim_group = f_calcsimgroups(set_of_vectors["metadata"], max_sim_group, threshold)
    print("Grouping similar images is finished")

    if not silent:
        # If not Silent - print similarity groups
        # metadata = set_of_vectors["metadata"]
        print("Displaying groups of similar images")
        for z in range(1, max_sim_group + 1):
            print("SIMILAR IMAGES GROUP{}".format(z))
            for val in set_of_vectors["metadata"]:
                if val[2] == z:
                    print(val[0])
    else:
        print("Silent mode, similar images displaying is skipped")
    f_saveprocessed(set_of_vectors)


def process(input_path, recalc, difference, threshold, silent, scale):
    """
    Procedure to process and verify input arguments.
    """
    threshold = float(threshold)
    img_file1 = ''  # Path to image for comparison
    img_file2 = ''  # path to image for comparison
    PROC = "process"
    if input_path is None and not recalc and difference is None:
        print("ERROR:   Not enough arguments.")
        f_printerr()
        sys.exit(2)
    try:
        if 100 < threshold or threshold < 0:
            print("ERROR:   Unsupported threshold value. Allowed 0 - 100, Recommended 2 - 7.")
            f_printerr()
            sys.exit(2)
        if difference is not None:
            if len(difference) != 2:
                print("ERROR:  Two images are required to measure a difference")
                f_printerr()
                sys.exit(2)
            else:
                img_file1 = difference[0]
                img_file2 = difference[1]
                if not os.path.exists(img_file1):
                    print("ERROR:   Path for image 1 is pointing to not existing location")
                    f_printerr()
                    sys.exit(2)
                if not os.path.exists(img_file2):
                    print("ERROR:   Path for image 2 is pointing to not existing location")
                    f_printerr()
                    sys.exit(2)
                PROC = "compare"
        if input_path is not None:
            if not os.path.exists(input_path):
                print("ERROR:   Path is pointing to not existing location")
                f_printerr()
                sys.exit(2)
        if recalc:
            PROC = "recalc"

    except:
        print("ERROR:    Error occurs")
        f_printerr()
        sys.exit(2)

    if PROC == "recalc":
        run_regroup(threshold)
    elif PROC == "compare":
        run_compare(img_file1, img_file2, scale)
    else:
        run_proc(input_path, threshold, silent, scale)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find images similar by content")
    parser.add_argument("--path", "-p", help="Path to folder with images")
    parser.add_argument("--recalc", "-r", action='store_true',
                        help="Re-calculate saved metadata with new similarity threshold.")
    parser.add_argument("--difference", "-d", nargs="+",
                        help="Calculate and display value of difference between 2 images.")
    parser.add_argument("--threshold", "-t", default='4',
                        help="threshold for images similarity <0 ... 100>, default 4")
    parser.add_argument("--silent", "-s", action='store_true',
                        help="Silent, no output of similar images")
    parser.add_argument("--scale", "-x", action='store_true',
                        help="Scale images before processing. Increases processing speed, reduces accuracy.")
    args = parser.parse_args()
    process(args.path, args.recalc, args.difference, args.threshold, args.silent, args.scale)

