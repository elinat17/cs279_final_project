README.txt 

For this analysis and algorithm creation we utilized celltool packages to process cell data, and KMeans function from the sklearn.cluster package to generate our prediction algorithm. Programs must be run in a python environment. The environment file to generate the right conda environment is included in the folder. 

To create the environment: 

conda env create -f environment.yml 

To activate the environment: 

conda activate cs279-finalp 

We then ran Celltool on folders of images of the cells. Processed images are stored in folders in the submission as well. Final CSV Files obtained are stored in <testgroup>kMeansCSV folders within <testgroup>Analysis folder. Sample of workflow for processing of the images is below: 

To extract the contours from cells: 

celltool extract contours --resample-points=100 --smoothing-factor=0.001 --destination=<output folder> <input folder> 

To sort the contours: 

python sort.py <input folder> <output folder> 

To align the contours: 

celltool align contours --allow-reflection --destination=<output folder> <input folder>/*.contours 

To create the model: 

celltool shape model --variance-explained=0.95 --output-prefix=<output name> <input folder>/*.contour 

To measure area: 

celltool measure contours --output-file="area.csv" --area --shape-modes kModel.contour 1 2 - <input folder>/*.contours 

To measure path length: 

celltool measure contours --output-file="pathlength.csv" --path-length - <input folder>/*.contours 

To measure curvature: 
celltool measure contours --output-file="pathlength.csv" --curvature - <input folder>/*.contours 



A breakdown of python scripts is listed below: 

sort.py: will sort through a folder, and put the highest number image (with matching prefix) into a new directory. Useage is: python sort.py <input directory> <output directory>. This function was utilized to parse through the output folder of extracting and resampling contours of the original cell images and move the most macro polygonal spline into a separate folder as the folders with all contour images were too large to run through most of the cell tool packages. 

overallkmeans.py: will run the prediction model on a given folder of CSV files. Three CSV files for area, curvature and path length must be in the input folder. Useage: python overallkmeans.py <input folder>. Results from the kmeans prediction is printed for each iteration (10 iterations will be run on the overall). Algorithm is implemented in kmeans.py but is called from parent function overallkmeans.py. 
