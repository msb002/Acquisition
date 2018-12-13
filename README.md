# Installation
1. Download the Git repository

     * In your MHDLab folder right click and select 'Git Bash Here'

     * type `git clone https://github.com/MHDLab/Acquisition`

     * close git bash
2. Open the Acquisition folder
2. Open the 'Common SubVis' folder in windows and double click to run `Setup_GlobalVariable.vi`. This will update the repository path that labview uses, which is contained within `GlobalVariables.vi`. 
3. Run `Monitor.vi` in the main Acquisition folder to confirm that everything is setup correctly. 
     * If you get an error saying that the python installation is not a valid excectable, the python integration toolkit is not using the correct python. In Labview, go to Tools -> Python Integration Toolkit -> Select Default python. Select the Python in the py36 anaconda environment, located at `C:\ProgramData\Anaconda3\envs\py36\python.exe`. See [LabSetup](https://github.com/MHDLab/Documentation/blob/master/labsetup.md) for more information. 

# Usage

### Setup the lab configuration files

If you have changed the phsical configuration of sensors into the DAQ, or are starting a new project, you must update the lab configuraiton files. Otherwise this section can be skipped. Labview uses these files to build a DAQmx task, naming your channels and including other metadata. See the development section below for an explanation of Lab configuration files.
1. Go to the folder `X:\Lab Configuration\` (if the X drive is unavailable, refer to MHD Common Drive Info)
2. The Lab configuration folder is a Local (i.e. not on GitHub) Git respository and changes to the configuration file should be commited. If you haven't already read See [Contributing](https://github.com/MHDLab/Documentation/blob/master/CONTRIBUTING.md) for correct practices on commiting changes.
3. Before altering any of the files open Git bash in the folder (Right click and select open Git bash here) and run 'git status' to confirm that there are no uncommited changes. If so you should commit those changes and leave a message indicating that there were uncommited changes. 
4. Update the Instruments file to reflect your configuration (if necessary)
5. Open the 'signal'_PXI_1 file corresponding to the signal types used in your experiment. Update these sensors to reflect those you edited for your experiment by filling in the information according to each column in the 'User Inputs' section.
6. To create a new project ID, add it to `ProjectIndex.csv`.
7. When done editing the configuration files commit any changes.


### Startup Labview programs
1. Open and run `monitor.Vi`. 

2. Set the test case information (found in `monitor.Vi`) for your experiment.
    * `monitor.Vi` creates and continuously writes to the 'event log' which contains the critical information needed for the post processing of data after aquisition. Most importantly instead of telling individual VIs to save files in specific locations, you just put the current test case's information into the monitor VI and the rest will be taken care of during the experiment or post processing. See the [post processing](https://github.com/MHDLab/PostProcessor) page for more information. 

        
3. If using anything that connects to the PXI chassis, Start `Senors\Chassis_Sensors.vi`. Set the sampling rate, and select the PXI devices or Alicat sensors that will be used. Open NI MAX to see information about PXI devices, which are the physical cards in the DAQ Chassis. Run `Chassis_Sensors.vi`, Data will begin logging. These VIs will now be run in the background for the rest of the experiment and can be minimized. 
4. Start any instrument Vis you will be using. Located in `Instruments\`
5. To visualize combinations of data, start a visualization vi in `Visualization\`. Note that Visualization VIs are not critical to the data acquisition. These VIs can be started and stopped independently of logging data without any affect. 

### Data Acquisition

Throughout the experiment, change the test case information in `Monitor.Vi` to write test case information changes to the event log. This will also change the file path in VIs that use direct logging. 

### Shutdown

Once the experiment is finished, close all VIs, ending with `Monitor.vi` last.

For `Chassis_Sensors.vi`, press stop in `Chassis_Sensors.vi`, not the individual sensor VIs that pop up. 
* `Chassis_Sensors.vi` can take some time to shut down, as any DAQmx-based VIs need to do a file conversion from the raw DAQmx tdms file to a npdtms-readable tdms file. 


Raw data then undergoes post processing. Raw data Files are saved into a directory dependent on the 'Raw Data Folder' variable located within `GlobalVariables.vi`, at the time of this writing `E:\Data\RawData`. 

Within the Raw Data Folder:
    * The eventlog is stored in `Todays Date\eventlog.json`.
    * Logfiles under the path `Todays Date\Logfiles\Instrument name`.
    * pre-processed and post-processed files will be saved `Todays Date\Project ID\SubFolder\Measurement Description`.


[Click here to move onto post processing](https://github.com/MHDLab/PostProcessor)

# Development

### Description of Lab configuration files

Some information about the physical infrastructure of the lab should not have a separate version for each user and so it is contained in a separate git repository on the MHDCode drive (X:\Lab Configuration\). This information is stored in a set of .csv and excel files, chosen for optimal communication labview programs. The files are listed below:

#### a) Point-to-point Master file:
This file contains all information about sensors and instruments connected in the lab. The sensor information is called from the individual chassis card csv and instrument information is called from the Instrument excel file. 

#### b) Instrument info
Instruments communicate over different protocols (RS232, GIGe, USB, etc.) and use different connections/conversions to communicate with the main lab computer. This file lists instrument information including: connection points, communication method, model number, function, (...?)

#### c) Sensor info
The chassis is equipped with cards to log the following analog signals: Currents (4..20mA), Voltages (0..5V, 0..10V, 0..20V?), and Thermocouples (specific scaled voltage). The Lab Configuration folder contains a csv for each card that can log these analog signals which has information about each channel of these cards. This information is read through labview to build a DAQmx task, which allows addition/removal of sensors in a logical streamlined manner.

#### d) Project info
Post-processed and non-log files are saved in a base folder known as the Project folder. This folder is defined in the global variables by a drop down menu. The options in this drop down menu are read from the ProjectIndex file to coordinate projects and keep project names consistent. Projects can be added to the csv and then imported to the global variables with the setup.exe, but projects should remain general (Vapor Tube, Sample Holder Testing, Powder Feeding, etc). For less general categories, please use subfolders.


### filesaving notes

Files are saved as logfiles or 'preprocessed'. The file paths are generated using generatefilepaths.vi. DaqMx files need to be processed in a special way using SubVis\DAQmx and Alicat\Fileconversion.vi. 


####     Creating a new Sensor VI template
The VI template must contain the following controls (names must match exactly): 
"Cluster" - the input cluster of information, which must match the outputs coming from the Chassis_Sensors VI
"File Size (Mb)" - a 64-bit double that tracks the size of the file of the specific sensor (the code for file size can be copied from other sensor VIs)

### Adding a new instrument VI

### Adding a new visualization VI
Data should be sent to the visualization VI using Queues just obtain a queue with the same name in both your data acquisition VI and visualization VI. Make sure to set a limit on the queue so there is not endless storage of data in the RAM if the visualization VI is not running.  *(see HVOF visulization to see how this works)*

### Adding a new event to be logged


*todo: describe folder structure for monitor VI to pick up instruments*

