<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">false</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="PyrometerSettings.vi" Type="VI" URL="../PyrometerSettings.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="instr.lib" Type="Folder">
				<Item Name="FilterWheel102_win32.dll" Type="Document" URL="/&lt;instrlib&gt;/Thorlabs_FW102C/Library/FilterWheel102_win32.dll"/>
				<Item Name="FilterWheel102_win64.dll" Type="Document" URL="/&lt;instrlib&gt;/Thorlabs_FW102C/Library/FilterWheel102_win64.dll"/>
				<Item Name="Thorlabs_FW102C.lvlib" Type="Library" URL="/&lt;instrlib&gt;/Thorlabs_FW102C/Thorlabs_FW102C.lvlib"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Close File+.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Close File+.vi"/>
				<Item Name="compatReadText.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatReadText.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Find First Error.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find First Error.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="Open File+.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Open File+.vi"/>
				<Item Name="Read Delimited Spreadsheet (DBL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (DBL).vi"/>
				<Item Name="Read Delimited Spreadsheet (I64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (I64).vi"/>
				<Item Name="Read Delimited Spreadsheet (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (string).vi"/>
				<Item Name="Read Delimited Spreadsheet.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet.vi"/>
				<Item Name="Read File+ (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read File+ (string).vi"/>
				<Item Name="Read Lines From File (with error IO).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Lines From File (with error IO).vi"/>
			</Item>
			<Item Name="FilterWheel102_win32.dll" Type="Document" URL="/E/Program Files (x86)/National Instruments/LabVIEW 2011/instr.lib/Thorlabs_FW102C/Library/FilterWheel102_win32.dll"/>
			<Item Name="GenerateDateString.vi" Type="VI" URL="../../../Common SubVis/GenerateDateString.vi"/>
			<Item Name="GenerateFilePaths.vi" Type="VI" URL="../../../Common SubVis/GenerateFilePaths.vi"/>
			<Item Name="Global Variables.vi" Type="VI" URL="../../../Global Variables.vi"/>
			<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="../Kineses/Thorlabs.MotionControl.Controls.dll"/>
			<Item Name="ThorLabs.MotionControl.KCube.DCServoCLI.dll" Type="Document" URL="../Kineses/ThorLabs.MotionControl.KCube.DCServoCLI.dll"/>
			<Item Name="WlArraySplitter.vi" Type="VI" URL="../WlArraySplitter.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
