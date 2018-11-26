import win32com.client  # Python ActiveX Client
LabVIEW = win32com.client.Dispatch("Labview.Application")
VI = LabVIEW.getvireference('C:\\Users\\aspit\\Git\\MHDLab\\Common Subvis\\GenerateFilePaths.vi')  # Path to LabVIEW VI
VI._FlagAsMethod("Call")  # Flag "Call" as Method
VI.setcontrolvalue('Device Name', "Lightfield") 
VI.setcontrolvalue('Extension (.tdms)', ".spe")
VI.setcontrolvalue('DAQmx (F)', False) 
VI.setcontrolvalue('Logfile? (F)', False) 

# VI.Call()  # Run the VI

# filepath = VI.getcontrolvalue('Path')  # Get return value
# print(filepath)  # Print value to console