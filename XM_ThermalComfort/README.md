XM_ThermalComfort - basic usage instructions

This tool is designed to maximize thermal comfort based on personal preferences. The system dinamically adapts thermodinamical parameters of the environment by using sensor data of the last 24 hours.
This code has been developed at "Università degli studi di Verona", in Verona. Users can modify and/or distribute code free of charge, provided that this notice is retained.

INSTALLATION

- Run the script XM_ThermalComfort/install.sh from a linux terminal. This should install the necessary libraries to make XM_ThermalComfort work.

EXECUTION

- Run the command "python3 XM_ThermalComfort/XM_ThermalComfort.py"

-------------------------------------------------------------------------------------------------------------------------------------------

FOLDERS

List of folders contained in XM_ThermalComfort:
dataset: contains input files;
results: contains the output of the system.

- The folder named "dataset" contains all input files needed: "sensor_data.csv" has one line with three values (timestamp, external temperature, internal temperature), while "thermal_profiles.csv" has seven lines (one per day of the week) with the desired temperature values for each hour of the day.
- The folder named "results" contains the output file of the system: "heater_signal.csv". This file has only the signal (off/on) for the heating system.

XM_ThermalComfort CODE FILES

List of XM_ThermalComfort code files contained in XM_ThermalComfort:
- "XM_ThermalComfort.py" contains the main and all the necessary functions;
- "install.sh": a script to install the required libraries.

AUTHORS

Alberto Castellini, Department of Computer Science, University of Verona, Italy, email: alberto.castellini@univr.it

Alessandro Farinelli, Department of Computer Science, University of Verona, Italy, email: alessandro.farinelli@univr.it

Riccardo Sartea, Department of Computer Science, University of Verona, Italy, email: riccardo.sartea@univr.it

Maddalena Zuccotto, Department of Computer Science, University of Verona, Italy, email: maddalena.zuccotto@univr.it
