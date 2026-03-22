# SimSearch

An app to group images by similarity of their content. In this case content is set of geometric shapes and their mutual arrangement.

## Description

    Each image is treated as a set of geometric shapes. Shapes are detected in any possible way. 
In this particular example the image is grayscale and the number of colors is scaled to 32 (0-31). Pixels of the same color belong to the same geometrical shape, so 32 shapes will be detected. Parameters of each shape are:  
 - Area = number of pixels in this shape, 
 - Outline Length = number of pixels of this shape that neighboring any other shape.
    Shape definition is Outline Length/Area.  Each image is defined by a vector of 32 values V = [Outline Length_0/Area_0, Outline length_1/Area_1, ... Outline length_31/Area_31], per color. 

Note: In case of necessity one can introduce additional coefficients, like Area of figure / Area of image and so on. Coefficients depend on the type of images most used in the dataset. 

   Similarity of images is calculated as distance between vectors of respective images: 
   Distance = Sum ( abs(V0_0 - V1_0) + abs (V0_1 - V1_1) + ... + abs(V0_31 - V1_31))

Note: depending on your goals, you can use deviation Deviation =  SQRT (Sum (abs(V0_0 ^ 2 - V1_0 ^ 2) + abs(V0_1 ^ 2 - V1_1 ^ 2) + ... + abs(V0_31 ^ 2 - V1_31 ^ 2)) ), it will smooth out individual outbursts.

    If Distance < threshold (or Deviation < threshold) then images are similar, otherwise - no.

Note: technology is patented.

## Getting Started

### Dependencies

App works offline, uses no AI, needs only cv2 for reading image files.

### Installing

python -m venv venv
source venv/bin/activate
pip install opencv-python
git clone 


### Executing program

* Regular run
python simsearch.py -p <folder with images> -t <threshold>

Recommended threshold 4-11.

* To compare 2 specific images
python simsearch.py -m <path to image 1> <path to image 2>

* To recalculate images similarity with different Threshold
python simsearch.py -r  -t <threshold>

## Help

Mandatory params:
    -p <path>  - Path to folder where images are located. Processed images in folder and sub folders.
    or 
    -r  - Re-calculate saved metadata with new similarity threshold. No new images processing.
    or 
    -d <image1> <image2> - Calculate and display distance between image vectors - number and % of lowest vector.

Optional params:
    -t <0 ... 100>  - Threshold for images similarity <0 ... 100>, default 4
                      0 - only copies are similar, 100 - all are similar. Recommended between 1 and 5.
    -s  - Silent, no output of similar images
    -x  - Scale images before processing. Increases processing speed, reduces accuracy.

Examples:
    To process all images in the folder and see similarity groups:
        python simsearch.py -p <path to folder with images>
    To check processed images for similarity with another similarity threshold
        python simsearch.py -r -t 5
    To process all images in the folder and store meta-data without displaying similarity groups:
        python simsearch.py -p /home/user/images -s
    To re-calculate similarity of images without processing, using meta-data, with different threshold:
        python simsearch.py -r -t 5
    To calculate and display distance between two images image 1 and image 2
        python simsearch.py -d /home/user/images/image1.jpg /home/user/images/image2.tif


## Authors

Nick Chaplahin
nickolasthb@hotmail.com


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Business Source License 1.1 - see the LICENSE.md file for details
