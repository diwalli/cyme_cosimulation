# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 11:32:18 2025

@author: diwalli
"""

import numpy as np
import pandas as pd
import cympy
import cympy.rm
import locale
import math
#import xlrd
import string

import os
import sys

# Location and name of .sxst file
CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

#studyFolderPath = r'C:\Program Files\CYME\CYME\tutorial\How-to'
studyFolderPath = CURRENT_DIRECTORY
studyFilename = r'\testing_cyme_fullbonnet.xst'

# Folder to save .xlrd and .csv results
saveResultsFolder = r'E:\Research-Data\Results Storage\Cyme Practice'
###############################################################################



#%% Open CYME Study and Verify that it loaded correctly

print('Opening CYME Study')
print('')

locale.setlocale(locale.LC_NUMERIC, '')
#cympy.app.ActivateRefresh(True)
cympy.app.ActivateRefresh(False)

#cympy.db.ConnectDatabaseByName("United_Network_4_RemovingHeadNodes_testing")

studyFilePath = studyFolderPath + studyFilename
cympy.study.Open(studyFilePath)
cympy.study.ActivateModifications(False)

# Run the Load Flow analysis
load_flow = cympy.sim.LoadFlow()
load_flow.Run()

# Get the list of networks
networks = cympy.study.ListNetworks()
# Create an empty list for the lines to show in the report
loads = cympy.study.ListDevices(cympy.enums.DeviceType.SpotLoad) 
print(loads)
'''
#Get customer types
customer_types=cympy.study.ListCustomerTypes()
print(customer_types)

#print(cympy.study.Load.ListLoadModels())

#List customers
list_customers=cympy.study.Load.ListCustomers()
print("Customer List")
print(list_customers)
'''
#loads=loads[0:5]
for load in loads:
    #load_id = load.GetValue("DeviceNumber")
    #load_info = cympy.study.QueryInfoDevice(KeywordID="EqState" , DeviceType=load.DeviceType, DeviceNumber=load.DeviceNumber)
    #print(load_info)
    load_id=load.DeviceNumber
    load_type=load.DeviceType
    load_loc=load.Location
    #load_loc=cympy.enums.DuctBankCoordinatesOrigin(load_id)
    load_section=load.SectionID
    #load_type = load.GetValue("DeviceType")
    print(load_id, load_type, load_loc, load_section)
#add customer load
#cympy.study.Load_AddCustomerLoad(CustomerNumber)

# Define load properties
load_name = "NewSpotLoad1"
node_id = "FeederNode123"  # Replace with the actual node ID on your feeder
load_model_id = 4 # Example load model ID
kw_demand = 100
kvar_demand = 50
phases = cympy.enums.Phase.ABC

l1=cympy.study.AddDevice("Load12345", cympy.enums.DeviceType.SpotLoad, load_id, "True")
#l1.cympy.eq.SetValue(DeviceType=cympy.enums.DeviceType.SpotLoad)
loads = cympy.study.ListDevices(cympy.enums.DeviceType.SpotLoad) 
print(loads)

# Iterating through all networks
for network in networks:
    #print("network: ",network)
    #LoadModelName=f"load_2_{network}"
    #cympy.study.AddLoadModel(LoadModelName)
    #load=cympy.dm.Load.GetObjType()
    loads=cympy.study.ListLoadModels()
    #print(loads)
    '''
    for load in loads:
        #cympy.study.LoadValue()
        #print("load: ", load)
        lm=cympy.study.GetLoadModel(load.Name)
        #print(lm)

    '''
        

'''
    try:
        cap_kvar = locale.atof(cympy.GetParameterAsText(1))
        cap_kv = locale.atof(cympy.GetParameterAsText(2))
        if cympy.GetParameterAsText(3) == 'True':
            sec_highlight = True
        else:
            sec_highlight = False
    
        print('Capacitor kVAR = ' + str(cap_kvar) + ', Capacitor kV = ' + str(cap_kv))
        print('Section Highlight: ' + str(sec_highlight))
    
    except cympy.err.CymError as e:
        print(e.GetMessage())
    except IndexError:
        print(' \n', 'Warning: Values cannot be loaded. Proceeding with the default values as')
        cap_kvar = 400.0
        cap_kv = 14.4
        sec_highlight = True
        print('Capacitor kVAR = ' + str(cap_kvar) + ', Capacitor kV = ' + str(cap_kv))
        print('Section Highlight: ' + str(sec_highlight) + '.')
        
    # Adding a shunt capacitor with ID 'MY_CAP_EQ' to the equipment database
    cympy.eq.Add('MY_CAP_EQ', cympy.enums.EquipmentType.ShuntCapacitor)
    my_cap_eq = cympy.eq.GetEquipment('MY_CAP_EQ', cympy.enums.EquipmentType.ShuntCapacitor)
    
    # Set Values of the new shunt capacitor bank 
    cympy.eq.SetValue(cap_kvar, 'RatedKVAR', 'MY_CAP_EQ', cympy.enums.EquipmentType.ShuntCapacitor)
    cympy.eq.SetValue(cap_kv, 'RatedVoltageKVLN', 'MY_CAP_EQ', cympy.enums.EquipmentType.ShuntCapacitor)
    
    # Load flow analysis and configuration of its settings
    load_flow = cympy.sim.LoadFlow()
    load_flow.SetValue('VoltageDropUnbalanced', 'ParametersConfigurations[0].AnalysisMode')
    load_flow.SetValue(20, 'ParametersConfigurations[0].MaximumIterations')
    load_flow.SetValue(0.1, 'ParametersConfigurations[0].VoltageTolerance')
    load_flow.SetValue('FromLibrary', 'ParametersConfigurations[0].LoadFlowVoltageSensitivityLoadModel.Mode')
    
'''