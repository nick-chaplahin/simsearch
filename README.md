# SimSearch

An app to group images by similarity of their content. In this case content is set of geometric shapes and their mutual arrangement. No AI, no 3-rd parties, easy to adjust, easy to re-use or integrate.
Technology is patented.
License: Dual License.

## Description

Each image is treated as a set of geometric shapes. Shapes are detected in any possible way. 
In this particular example the image is grayscale and the number of colors is scaled to 32 (0-31). Pixels of the same color belong to the same geometrical shape, so 32 shapes will be detected. Parameters of each shape are:  
 - Area = number of pixels in this shape, 
 - Outline Length = number of pixels of this shape that neighboring any other shape.
Shape definition is Outline Length/Area.  Each image is defined by a vector of 32 values V = [Outline Length_0/Area_0, Outline length_1/Area_1, ... Outline length_31/Area_31], per color. 

Note: In case of necessity one can introduce additional coefficients, like Area of figure / Area of image and so on. Coefficients depend on the type of images most used in the dataset. 

Similarity of images is calculated as distance between vectors of respective images: 
   Distance = Sum ( abs(V0_0 - V1_0) + abs (V0_1 - V1_1) + ... + abs(V0_31 - V1_31))

Note: depending on your goals, you can use deviation: Deviation =  SQRT (Sum (abs(V0_0 ^ 2 - V1_0 ^ 2) + abs(V0_1 ^ 2 - V1_1 ^ 2) + ... + abs(V0_31 ^ 2 - V1_31 ^ 2)) ), it will smooth out individual outbursts.

If Distance < threshold (or Deviation < threshold) then images are similar, otherwise - no.

App creates file imgSimMetadata.json where stores metadata of processed images, it is used for recalculation with different threshold procedure. And demonstrates reuse of metadata,  simplicity and small volume of storage.

Note: technology is patented.

## Getting Started

### Dependencies

App works offline, uses no AI, needs only cv2 for reading image files.

### Installing
```bash
python -m venv venv
source venv/bin/activate
pip install opencv-python
git clone https://github.com/nick-chaplahin/simsearch.git
cd simsearch
python simsearch.py -p Lenna_Variants_ordered -t 4 
python simsearch.py -r -t 7
python simsearch.py -m Lenna_Variants_ordered/01_Original_TIFF.tif Lenna_Variants_ordered/06_Mirror_vertical.jpg
```
Use -x option if images are big and processing takes too much time.

### Executing

* Regular
```bash
python simsearch.py -p <path to folder with images> -t <threshold>
```
Recommended threshold 4-11.

* To compare 2 specific images
```bash
python simsearch.py -m <path to image 1> <path to image 2>
```
* To recalculate images similarity with different Threshold
```bash
python simsearch.py -r  -t <threshold>
```
## Help

Mandatory params:
* -p <path>  - Path to folder where images are located. Processed images in folder and sub folders.
*  or 
* -r  - Re-calculate saved metadata with new similarity threshold. No new images processing.
*  or 
* -d <image1> <image2> - Calculate and display distance between image vectors - number and % of lowest vector.

Optional params:
* -t <0 ... 100>  - Threshold for images similarity <0 ... 100>, default 4. 0 - only copies are similar, 100 - all are similar.
* -s  - Silent, no output of similar images
* -x  - Scale images before processing. Increases processing speed, reduces accuracy.

Examples:
* - To process all images in the folder and see similarity groups:
```bash
python simsearch.py -p <path to folder with images>
```
- To check processed images for similarity with another similarity threshold
```bash
python simsearch.py -r -t 5
```
- To process all images in the folder and store meta-data without displaying similarity groups:
```bash
python simsearch.py -p </home/user/images> -t 4
```
- To re-calculate similarity of images without processing, using meta-data, with different threshold:
```bash
python simsearch.py -r -t 5
```
To calculate and display distance between two images image 1 and image 2
```bash
python simsearch.py -d </home/user/images/image1.jpg> </home/user/images/image2.tif>
```

## Authors

Nick Chaplahin
nickolasthb@hotmail.com


## Version History

* 0.1
    * Initial Release

## License

SimSearch uses a **dual licensing model**:

| Who you are                            | License             | Cost   |
|----------------------------------------|---------------------|--------|
| Individual / non-profit / open source  | GPL v3              | Free   |
| Small business (revenue < $5M/yr)      | GPL v3              | Free   |
| Company with revenue ≥ $5M/yr          | Commercial License  | Paid   |
| Closed-source / proprietary use        | Commercial License  | Paid   |

**→ Not sure which license you need? Read [LICENSING.md](LICENSING.md)**

**Free (GPL) License:**
If you are eligible, you may use YourProject for free under the
[GPL v3 License](LICENSE-GPL.txt). This requires that any software you
distribute that incorporates YourProject must also be open source under
a GPL-compatible license.

---
*Copyright (C) 2023 Nick Chaplahin*