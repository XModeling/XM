XM_HeatForecast - basic usage instructions

This tool is meant to ease the forecasting of heating load and the interpretation of results and models. This code has been developed at "Università degli studi di Verona", in Verona. Users can modify and/or distribute code free of charge, provided that this notice is retained.

INSTALLATION

Run the script XM_HeatForecast/install.sh from a linux terminal. This should install the necessary libraries to make XM_HeatForecast works.

GENERATION OF PREDICTIONS

Run the python script XM_HeatForecast/XM_HeatForecast.py. Enter a forecasting horizon between 24 or 48 hours. Follow the steps described in the presentation XM_HeatForecast/Docs/Documentation.pdf to perform a basic execution.

FOLDERS

List of folders contained in XM_HeatForecast: 

	- Current_model: contains a cronology of trained models;
	- Docs: contains documentation;
	- Forecast_files: contains a cronology of predictions;
	- Pasta data: contains data used by tool;
	- Performance: contains three subfolders: Parameters, RMSE and Rsquared used to interpretability and evaluation of performance;
	- Weather_forecast: contains a cronology of weather forecasting

XM CODE FILES

List of code files:

	- XM_HeatForecast.py: the launcher;
	- gui_support.py: contains functions that support GUI;
	- install.sh: a script to install the required libraries.

AUTHORS

Alberto Castellini, Department of Computer Science, University of Verona, Italy, email: alberto.castellini@univr.it

Alessandro Farinelli, Department of Computer Science, University of Verona, Italy, email: alessandro.farinelli@univr.it

Federico Bianchi, Department of Computer Science, University of Verona, Italy, email: federico.bianchi@univr.it

Francesco Masillo, University of Verona, Italy, email: francesco.masillo@studenti.univr.it
