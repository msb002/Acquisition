#For windows downloads
#Right-click on the .dll
#"Properties"
#Under "General", click "Unblock"


#Requirements: This requires the pythonnet library. This is availible via pip from https://pypi.python.org/pypi/pythonnet. For more details see http://stackoverflow.com/questions/14633695/how-to-install-python-for-net-on-windows.

import clr
#This assumes that the Dlls are in the same folder as the python script
clr.AddReference('OptecHID_FilterWheelAPI')
from OptecHID_FilterWheelAPI import FilterWheels
from OptecHID_FilterWheelAPI import FilterWheel
my_instance = FilterWheels()

for HSFW in my_instance.FilterWheelList:
    print("Wheel Found")
HSFW.ClearErrorState()
HSFW.HomeDevice()
print("Number of Filters")
print(HSFW.NumberOfFilters)
print("Current Position")
print(HSFW.CurrentPosition)
print("Moving to position 3")
HSFW.CurrentPosition = 3
print("Current Position")
print(HSFW.CurrentPosition)
