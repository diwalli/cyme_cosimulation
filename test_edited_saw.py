# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 13:12:29 2025

@author: diwalli
"""

from saw_editing_file import SAW
import pandas as pd
import os
import sys

CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(CURRENT_DIRECTORY, ".."))

master_pw="E:\\Research-Data\\Results Storage\\WECC Project\\transmission\\HighSummerWECC\\25HS3Sa1_updatedCoords_v4.pwb"
pw=SAW(master_pw)

branch_data = pw.GetParametersMultipleElement('branch',
                                              ["BusNum", "BusNum:1", "BusKVVolt", "BusKVVolt:1",
                                               'LineMaxPercent', "LineLength", "LineAMVA", "BusNomVolt", "BusNomVolt:1", "AreaName", "AreaName:1"])

Ldata = pw.GetParametersMultipleElement('load', ['BusNum', 'LoadID', 'LoadMW'])
#print(branch_data)
#Ldata['LoadMW']=20


Ldata.loc[0, 'LoadMW'] = 25

pw.change_parameters_multiple_element_df(ObjectType='load', command_df=Ldata)


Ldata = pw.GetParametersMultipleElement('load', ['BusNum', 'LoadID', 'LoadMW'])

pw.SolvePowerFlow()
pw.RunScriptCommand('SolvePrimalLP()')

branch_data = pw.GetParametersMultipleElement('branch',
                                              ["BusNum", "BusNum:1", "BusKVVolt", "BusKVVolt:1",
                                               'LineMaxPercent', "LineLength", "LineAMVA", "BusNomVolt", "BusNomVolt:1", "AreaName", "AreaName:1"])

#print(branch_data)