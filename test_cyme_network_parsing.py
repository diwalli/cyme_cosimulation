#NAME: Summary Report LF/SC
#DESCRIPTION: Create a summary report with the worst voltage, the total losses and the range of short-circuit values for each network.

import cympy
import string
import locale
import os
import sys

# Location and name of .sxst file
CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

#studyFolderPath = r'C:\Program Files\CYME\CYME\tutorial\How-to'
studyFolderPath = CURRENT_DIRECTORY
studyFilename = r'\testing_file.xst'

# Folder to save .xlrd and .csv results
saveResultsFolder = r'E:\Research-Data\Results Storage\Cyme Practice'


###############################################################################



#%% Open CYME Study and Verify that it loaded correctly

print('Opening CYME Study')
print('')

locale.setlocale(locale.LC_NUMERIC, '')
cympy.app.ActivateRefresh(True)

studyFilePath = studyFolderPath + studyFilename
cympy.study.Open(studyFilePath)
cympy.study.ActivateModifications(False)


# Run the Load Flow analysis
load_flow = cympy.sim.LoadFlow()
load_flow.Run()

# Get the list of networks
networks = cympy.study.ListNetworks()

# Create an empty list for the lines to show in the report
lines = []

# Iterating through all networks
for network in networks:
    # Create empty lists for the worst low voltage, high voltage and total losses seen by the sources
    print("Network ", network)
    
    low_voltages = cympy.study.ListAbnormalConditions(cympy.enums.AbnormalConditionType.LowVoltage, network)
    # Getting the high voltage sections on the network
    high_voltages = cympy.study.ListAbnormalConditions(cympy.enums.AbnormalConditionType.HighVoltage, network)
    
    # Low voltage sections count on the network
    low_voltage_count = (len(low_voltages))
    # High voltage sections count on the network
    high_voltage_count = (len(high_voltages))
    
    # Getting the list of sources on the current network
    sources = cympy.study.ListNodes(cympy.enums.NodeType.SourceNode, network)
    for source in sources:
        # Getting source node id
        source_id = source.ID
        print("Source ", source_id)
        # Getting list of nodes of the current network
    nodes = cympy.study.ListNodes(cympy.enums.NodeType.All, network)
    for node in nodes:
        # Getting node id
        node_id = node.ID
        #print(node_id)
        
LoadModels = cympy.study.ListLoadModels()
for ii in range(len(LoadModels)):
    print(LoadModels[ii].ID)
    LoadModel=LoadModels[ii].ID
