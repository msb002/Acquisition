# Usage 

### Setup your experiment. 
See the develop section below for an explanation of Lab configuration files.

Once the sensors and instruments needed for your experiment are in place:
1. Go to the folder `X:\Lab Configuration\` (if unavailable, refer to MHD Common Drive Info)
2. Update the Instruments file to reflect your configuration (if necessary)
3. Open the 'signal'_PXI_1 file corresponding to the signal types used in your experiment. Update these sensors to reflect those you edited for your experiment. (if necessary)
4. Save changes and run git commiting script


### Startup Labview programs
1. Open and run `monitor.Vi`. 

* If you get an error from the python integration toolkit about a python installation:
  1. In labview Go to Tools->Python Integration Toolkit
  2. Set the path for the python installation to the python of your anaconda installation. Typically `C:\ProgramData\Anaconda3\python.exe`. You can find the path of your anaconda path by typing 'anaconda prompt' into windows, right clicking, and selecting open file location. 

This VI creates and continuously writes to the 'event log' (eventlog.json) which is critical for the post processing of data after aquisition. The event log contains information about the experiment (see Development) suchas when Vis are stopped and started, etc. Importantly, the Monitor Vi is used to write 'Test Case Information' to the eventlog. In short, instead of telling individual VIs to save files in specific locations, you just put the current test case's information into the monitor VI and the rest will be taken care of afterwards. See the [post processing](https://github.com/aspitarl/MHDlab/wiki/Post-Processing) page for more information. 

2. Set the test case information (found in `monitor.Vi`, which must be running) for your experiment. To create a new project ID, add it to `ProjectIndex.csv`. Files will saved or eventually post processed into the path `Z\Data\Raw Data\Todays Date\Project ID\SubFolder\Measurement Description`. Log files are saved under the path `Z\Data\Raw Data\Todays Date\Logfiles\Instrument name`

3. If using anything that connects to the PXI chassis, Start `Senors\Chassis_Sensors.vi`. Set the sampling rate, and select the PXI cards and tasks to be used (or an Alicat sensor). Open NI MAX to see information about DAQmx tasks. Run Chassis_Sensors.vi, Data will begin logging. These VIs will now be run in the background for the rest of the experiment and should not be interacted with. 
4. Start any instrument Vis you will be using. Located in `Instruments\`
5. To visualize combinations of data, start a visualization vi in `Visualization\`. Note that Visualization VIs are not critical to the data acquisition. These VIs can be started and stopped independently of logging data without any affect. 

### Data Acquisition

Throughout the experiment, change the test case information in the `monitor.Vi` to write test case information changes to the event log. This will also change the file path in VIs that use direct logging.

### Shutdown

Once the experiment is finished, close all VIs, ending with `Monitor.vi` last.

For `Chassis_Sensors.vi`, press stop in `Chassis_Sensors.vi`, not the individual sensor VIs that pop up. 
* `Chassis_Sensors.vi` can take some time to shut down, as any DAQmx-based VIs need to do a file conversion from the raw DAQmx tdms file to a npdtms-readable tdms file. 

Raw Data is saved in `Z:Data\Raw Data`. Raw data then undergoes  before being moved onto your personal computer for analysis.  

[Click here to read the instructions for post processing](https://github.com/aspitarl/MHDlab/wiki/Post-Processing)

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


### Adding a new Analog sensor:
Adding a new sensor requires little editing to the actual code running the data acquisition system. Here is a set of general steps to add a sensor to MHD Lab:
1. Signal type: In the MHDCode\Lab Configuration\ folder, there are files specific to each Chassis Card for analog signals. A csv exists for each chassis card where the individual channel information is stored. Open the card that your signal will be logged from. I.E. Current, Voltage, or Thermocouple (specific type of voltage signal) and fill in the information according to each column in the 'User Inputs' section.

2. Power off voltage source for the signals (if you're not sure, seek help from a more experienced labmate). Connect your signal as specified in the sensor manual/by the manufacturer.

3. Once the information for the sensor has been added to the appropriate csv, save and push changes. 

###

####     Creating a new Sensor VI template
The VI template must contain the following controls (names must match exactly): 
"Cluster" - the input cluster of information, which must match the outputs coming from the Chassis_Sensors VI
"File Size (Mb)" - a 64-bit double that tracks the size of the file of the specific sensor (the code for file size can be copied from other sensor VIs)

### Adding a new instrument VI

### Adding a new visualization VI
Data should be sent to the visualization VI using Queues just obtain a queue with the same name in both your data acquisition VI and visualization VI. Make sure to set a limit on the queue so there is not endless storage of data in the RAM if the visualization VI is not running.  *(see Vaportubes visulization to see how this works)*

### Adding a new event to be logged


*todo: describe folder structure for monitor VI to pick up instruments*

