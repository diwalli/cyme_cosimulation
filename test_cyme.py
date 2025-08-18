import numpy as np
import pandas as pd
import cympy
import cympy.rm
import locale
import math
#import xlrd
import string

###############################################################################

#%%  Set directory paths and filenames

# Location and name of .sxst file
    
studyFolderPath = r'C:\Program Files\CYME\CYME\tutorial\How-to'
studyFilename = r'\LoadAllocation.sxst'

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

networks = cympy.study.ListNetworks()
print(networks)
nodes=cympy.study.ListNodes()
#nodes=cympy.study.ListSections()
networks_str = [str(item) for item in networks]
print(networks_str)

for node in nodes:
    #print(str(node), node)
    node_info= cympy.study.FindNodeInfo(str(node), networks_str)
    #node_info= cympy.study.FindSectionInfo(str(node), networks_str)
    #node2=cympy.study.GetNode(node)
    nod_loc=cympy.study.LocateDevice(str(node))
    print(nod_loc)

# Deactivate the GUI refresh
'''
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
    worst_low = []
    worst_high = []
    total_losses = []

    # Getting the low voltage sections on the network
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
        #print(source_id)

        try:
            # Keywords are in the string format and must be converted to float for numerical values
            # Getting the worst low three phase voltage seen by source
            worst_low.append(locale.atof(cympy.study.QueryInfoNode('DwLowVoltWorst3PH', source_id)))
            # Getting the worst high three phase voltage seen by source
            worst_high.append(locale.atof(cympy.study.QueryInfoNode('DwHighVoltWorst3PH', source_id)))
            # Getting the total downstream kw losses
            total_losses.append(locale.atof(cympy.study.QueryInfoNode('DwKWLossTotal', source_id)))
        except ValueError as e:
            pass  # Ignore source if no valid value if found

    try:
        # Get the worst case
        worst_low = min(worst_low)
        worst_high = max(worst_high)
        total_losses = max(total_losses)
        print(worst_low, worst_high, total_losses)

    # Catch a thrown exception
    except cympy.err.CymError as e:
        print(e.GetMessage())
        worst_low = 0.0
        worst_high = 0.0
        total_losses = 0.0
        low_voltage_count = 0
        high_voltage_count = 0

    # Appending data to lines
    lines.append([network, worst_low, worst_high, low_voltage_count, high_voltage_count, total_losses])

# Execute Short Circuit analysis
try:
    sc = cympy.sim.ShortCircuit()
    # Set the method to summary short-circuit in phase
    sc.SetValue('SC', 'ParametersConfigurations[0].Domain')
    sc.Run()
except cympy.err.CymError as e:
    print(e.GetMessage())

# Iterating through the existing lines of the report
for line in lines:
    # Getting network id of the data in the line
    network_id = line[0]

    # Create an empty list for the maximum and minimum faults
    min_LLL = []
    max_LLL = []
    min_LG = []
    max_LG = []

    # Getting list of nodes of the current network
    nodes = cympy.study.ListNodes(cympy.enums.NodeType.All, network_id)
    #print(nodes)
    for node in nodes:
        # Getting node id
        node_id = node.ID
        print(node)
        try:
            # Getting min LLL fault
            LLL_min = locale.atof(cympy.study.QueryInfoNode('LLLampKmin', node_id))
            if LLL_min != 0.0:
                min_LLL.append(LLL_min)

            # Getting max LLL fault
            LLL_max = locale.atof(cympy.study.QueryInfoNode('LLLampKmax', node_id))
            if LLL_max != 0.0:
                max_LLL.append(LLL_max)
        except:
            print("done")
            
'''