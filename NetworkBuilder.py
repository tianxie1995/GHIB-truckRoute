# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
import config 
import os

def select_network_by_mask(road, mask, plaza_mask, output):
    """
    Clip the road network by a specified mask

    Input:
    :road - string - file name of the road layer
    :mask - string - file name of the mask layer
    :output - string - file name of the output network

    Output:
    :output - string - file name of the output network
    """
    if not arcpy.Exists(output):
        arcpy.MakeFeatureLayer_management(road, 'road_lyr')
        print("match:{}".format(int(arcpy.GetCount_management('road_lyr')[0])))
        arcpy.SelectLayerByLocation_management('road_lyr', "INTERSECT", mask)
        print("match:{}".format(int(arcpy.GetCount_management('road_lyr')[0])))
        arcpy.SelectLayerByLocation_management('road_lyr', "INTERSECT", plaza_mask,
                                                 "", "REMOVE_FROM_SELECTION")
        print("match:{}".format(int(arcpy.GetCount_management('road_lyr')[0])))
        arcpy.SelectLayerByAttribute_management('road_lyr', 
                                            'SUBSET_SELECTION', 
                                            '"FCC" <> \'A11\'')
        print("match:{}".format(int(arcpy.GetCount_management('road_lyr')[0])))
        arcpy.CopyFeatures_management('road_lyr', output)
        return output 
    else:
        print(output, " already exist")
        return output 

def calculate_time_by_speed(road):
    arcpy.AddField_management(road, "TIME_COST", "DOUBLE")
    arcpy.AddField_management(road, "LEVEL", "SHORT")
    arcpy.AddField_management(road, "OldTrkRt", "SHORT")

    codeblock = """
def getTime(fcc, length):
    digit = int((fcc.strip())[1:])
    if digit < 20:
        return ((float(length)/ 5280 )/ 60 )*3600
    elif digit < 30:
        return ((float(length)/ 5280 )/ 40 )*3600
    elif digit < 40:
        return ((float(length)/ 5280 )/ 30 )*3600
    else:
        return ((float(length)/ 5280 )/ 20 )*3600"""
    codeblock2 = """
def getLevel(fcc):
    digit = int((fcc.strip())[1:])
    if digit < 20:
        return 1
    elif digit < 40:
        return 2
    else:
        return 3"""

    codeblock3 = """
def getOldTrkRt(FENAME):
    if FENAME in [ 'Wyoming' ,
        'Wyoming/E I 94' , 'Wyoming/US 12' ,
        'Jefferson' , 'Dearborn' ,
        'Vernor' , 'Lonyo' ,
        'Lonyo/E I 94' ,'Springwells' , 
        'Livernois' , 'Livernois/E I 94' ,
      'Livernois/S I 75' , 'Dragoon' , 
      'Dragoon/N I 75' , 'Clark' ,
       'Clark/N I 75' , 'Clark/S I 75' , 
       'Grand' , 'Grand River/W I 94' ,
        'Michigan' , 'Fort', 'Westend' ]:
        return 1
    else:
        return 0"""

    expression1 = "getTime(!FCC!, float(!LENGTH!))"
    out_table = arcpy.CalculateField_management(road, "TIME_COST", expression1, "PYTHON", 
                                    codeblock)
    expression2 = "getLevel(!FCC!)"
    out_table = arcpy.CalculateField_management(road, "LEVEL", expression2, "PYTHON", 
                                    codeblock2)

    expression3 = "getOldTrkRt(!FENAME!)"
    out_table = arcpy.CalculateField_management(road, "OldTrkRt", expression3, "PYTHON", 
                                    codeblock3)
    return out_table

def preprocess_network(road, mask, plaza_mask, output):
    env.workspace = config.working_folder
    env.overwriteOutput = True
    env.parallelProcessingFactor = "100%"
    selected_roads = select_network_by_mask(road, mask, plaza_mask, output)
    out_table = calculate_time_by_speed(selected_roads)