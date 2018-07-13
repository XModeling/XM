# XM
eXplainable modeling package

This software is meant to ease the interpretation of various clustering/modeling results.
This code has been developed at "Università degli studi di Verona", in Verona. Users can modify and/or distribute code free of charge, provided that this notice is retained.
This tool expects a single file containing the dataset and a folder containing the clustering/modeling results.


USING

The main project directory is XM_v1.3; all further commands are given with respect to that directory.
To run the program, just execute the following command:

"python XM.py"

There might be some errors due to missing libraries, listed in libraries.txt. 

- To install gsl run: "sudo apt-get install libgsl0-dev"
- To install lblas run: "sudo apt-get install libblas-dev liblapack-dev"
- To install pandastable run: "pip install pandastable"
- To install pyitlib run: "pip install pyitlib"
- To install xkcd run: "pip install xkcd"


CODE

"subc.py" contains the function used to compute new results with the method "SubCMedians".
"SU.py" contains the function defining the symmetrical uncertainty, an entropy based measure, used to sort variables.
"VSF": vertical scrolled frame.
"CheckBar": variables checkbar.
"LoadingScreen": loading screen during tab switching.
"GUI_inserimento_dati.py" is the module used for the mask of "Generation" module.
"Grafici.py" defines all the functions used to draw graphs and tables. It also contains some utility functions regarding loading of files and datasets.
"XM.py" is the core of this software. It builds the entire GUI.


FOLDERS

DATASETS: contatins dataset files.
IMG: contains images and icons.
DOC: contains documentation.
RESULTS: contains the results of clustering/modeling
MethodLib. contains the libraries of different methods for generating cluster/models.

The folder named "SubCMediansLib" in "MethodLib/SubCMedians"contains all files related to the algorithm written by Sergio Peignier.


AUTHORS

Alberto Castellini, alberto.castellini@univr.it
Alessandro Farinelli, alessandro.farinelli@univr.it
Francesco Masillo (main developer), francesco.masillo@studenti.univr.it
