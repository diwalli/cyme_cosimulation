# Copyright 2014 Eaton.
# All rights reserved. 
# 
# Proprietary to Eaton in the U.S. and other countries. 
# You are not permitted to use this file without the prior written consent of 
# Eaton or without a valid contract with Eaton (CYME). 
# 
# For additional information, contact: cymesupport@eaton.com 

#NAME: Summary Report LF/SC
#DESCRIPTION: Create a summary report with the worst voltage, the total losses and the range of short-circuit values for each network.

import cympy
import string
import locale
import os
import sys
import _db

# Location and name of .sxst file
CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

#studyFolderPath = r'C:\Program Files\CYME\CYME\tutorial\How-to'
studyFolderPath = CURRENT_DIRECTORY


###############################################################################



#%% Open CYME Study and Verify that it loaded correctly



print('Opening CYME Database')
print('')

#cympy.db.ConnectDatabaseByName("United_Network_4_RemovingHeadNodes_testing")
_db.ConnectDatabaseByName("Bluebonnet_July24th_wtoSubstation_testing")

locale.setlocale(locale.LC_NUMERIC, '')
cympy.app.ActivateRefresh(True)

#studyFilePath = studyFolderPath + studyFilename
#cympy.study.Open(studyFilePath)
#cympy.study.ActivateModifications(False)

networks=_db.ListNetworks()
networks=networks[0:40]
print(networks)



print('Creating CYME Study')
print('')

cympy.study.New()
cympy.study.LoadNetworks(networks)

#locale.setlocale(locale.LC_NUMERIC, 'C:\\Program Files\\CYME\\CYME\\tutorial\\How-to')
locale.setlocale(locale.LC_NUMERIC, '')
# Deactivate the GUI refresh
cympy.app.ActivateRefresh(False)

studyFolderPath = CURRENT_DIRECTORY
studyFilename = r'\testing_cyme_fullbonnet.xst'

studyFilePath = studyFolderPath + studyFilename

cympy.study.Save(studyFilePath)
cympy.study.Close()

'''
loads = cympy.study.db.GetLoads() 

# Iterate and list load details
for load in loads:
    print(f"Load ID: {load.ID}, Name: {load.Name}, Bus: {load.ConnectedBus.Name}")
'''   

# Retrieve all load devices in the study
load_devices = cympy.study.ListDevices(cympy.enums.DeviceType.DCLoad)
#load_devices = cympy.study.ListDevices()
#print(load_devices)
# Prepare a list to store customer information
customer_data = []

# Iterate through each load device and extract relevant data
for load in load_devices:
    customer_id = load.GetValue('DeviceNumber')  # Assuming DeviceNumber is the customer ID
    #location = load.GetValue('Location')  # Assuming 'Location' provides location info
    # ... Add other relevant attributes from the load device
    print(load)
    
    #customer_data.append({'ID': customer_id, 'Location': location})

# Print or process the collected customer data
for customer in customer_data:
    print(f"Customer ID: {customer['ID']}, Location: {customer['Location']}")

#print(networks)
nodes=cympy.study.ListNodes()
networks_str = [str(item) for item in networks]
#print(networks_str)
devices=cympy.study.ListDevices()
#print(len(devices),len(nodes))
#custs=cympy.study.ListCustomers()
for node in nodes:
    node = str(node)
    node = node.strip("'")
'''
for d in devices:
    #print(str(d.DeviceNumber), str(node))
    if d.DeviceNumber==str(node):
        print(d.DeviceNumber, d.DeviceType)
 
for d in devices:
    load_v=cympy.study.GetLoad(d.DeviceNumber,  d.DeviceType)
    if load_v !=None:
        print(load_v)
        

for network in networks:
    for node in nodes:
        #print("node: ", node)
        node_info= _db.FindNodeInfo(str(node))
        print(node_info)

'''        
#print(d.DeviceNumber, d.DeviceType, d.)

for node in nodes:
    #print(str(node), node)
    node_info= cympy.study.FindNodeInfo(str(node), networks)
    #cympy.study.QueryInfoNode( ,str(node))
    #print(node_info)


#locale.setlocale(locale.LC_NUMERIC, 'C:\\Program Files\\CYME\\CYME\\tutorial\\How-to')
locale.setlocale(locale.LC_NUMERIC, '')
# Deactivate the GUI refresh
cympy.app.ActivateRefresh(False)

studyFolderPath = CURRENT_DIRECTORY
studyFilename = r'\testing_cyme_fullbonnet.xst'

studyFilePath = studyFolderPath + studyFilename

cympy.study.Save(studyFilePath)
cympy.study.Close()


###############################################################################



#%% Open CYME Study and Verify that it loaded correctly

print('Opening CYME Study')
print('')

locale.setlocale(locale.LC_NUMERIC, '')
#cympy.app.ActivateRefresh(True)
cympy.app.ActivateRefresh(False)

#cympy.db.ConnectDatabaseByName("United_Network_4_RemovingHeadNodes_testing")

cympy.study.Open(studyFilePath)
cympy.study.ActivateModifications(False)



networks = cympy.study.ListNetworks()


'''
# Run the Load Flow analysis
load_flow = cympy.sim.LoadFlow()
load_flow.Run()
'''
# Get the list of networks
'''
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
    for node in nodes:
        # Getting node id
        node_id = node.ID

        try:
            # Getting min LLL fault
            LLL_min = locale.atof(cympy.study.QueryInfoNode('LLLampKmin', node_id))
            if LLL_min != 0.0:
                min_LLL.append(LLL_min)

            # Getting max LLL fault
            LLL_max = locale.atof(cympy.study.QueryInfoNode('LLLampKmax', node_id))
            if LLL_max != 0.0:
                max_LLL.append(LLL_max)

            LG_min = locale.atof(cympy.study.QueryInfoNode('LGampKmin', node_id))
            if LG_min != 0.0:
                min_LG.append(LG_min)

            LG_max = locale.atof(cympy.study.QueryInfoNode('LGampKmax', node_id))
            if LG_max != 0.0:
                max_LG.append(LG_max)
        except ValueError as e:
            pass

    try:
        # Get minimal LLL fault
        min_LLL = min(min_LLL)
        # Get maximal LLL fault
        max_LLL = max(max_LLL)
        min_LG = min(min_LG)
        max_LG = max(max_LG)
    except cympy.err.CymError as e:
        print(e.GetMessage())
        min_LLL = 0.0
        max_LLL = 0.0
        min_LG = 0.0
        max_LG = 0.0
    # Appending data to line
    line.append(min_LLL)
    line.append(max_LLL)
    line.append(min_LG)
    line.append(max_LG)

# Report generation
# Create the report and the name of the columns
report = cympy.rm.CustomReport('SummaryReport', ['NetworkID', 'Worst Under\n Voltage (%)', 'Worst Over\n Voltage (%)',
                                                 'Number of\n Under Voltages', 'Number of\n High Voltages', 'Total\n Losses (kW)',
                                                 'Minimum\n LLL Fault (A)', 'Maximum\n LLL Fault (A)', 'Minimum\n LG Fault (A)', 'Maximum\n LG Fault (A)'])
for line in lines:
    # Create a list with the elements of the report line
    cells = []
    # Creating a hyperlink network cell
    c_network = cympy.rm.NetworkCell(line[0])
    cells.append(c_network)

    # Adding the other values to the report
    c_others = line[1:3]
    for cell in c_others:
        cells.append(cympy.rm.FloatCell(round(cell, 2)))

    c_others = line[3:5]
    for cell in c_others:
        cells.append(cympy.rm.IntCell(cell))

    c_others = line[5:]
    for cell in c_others:
        cells.append(cympy.rm.FloatCell(round(cell, 2)))

    # Adding the row to the report
    report.AddRow(cells)

try:
    report.Show()
except cympy.err.CymError as e:
    print(e.GetMessage())
    # If the report cannot show, print all the values to find the problem
    print('NetworkID'.rjust(20, ' ')),
    print('Worst Under Voltage'.rjust(20, ' ')),
    print('Worst Over Voltage'.rjust(20, ' ')),
    print('Number of Under Voltages'.rjust(20, ' ')),
    print('Number of High Voltages'.rjust(20, ' ')),
    print('Total Losses'.rjust(20, ' ')),
    print('Minimum Fault'.rjust(20, ' ')),
    print('Maximum Fault'.rjust(20, ' '))

    for line in lines:
        for s in line:
            print(str(s).rjust(20, ' '))
        print('\n')
finally:
    cympy.app.ActivateRefresh(True)
'''