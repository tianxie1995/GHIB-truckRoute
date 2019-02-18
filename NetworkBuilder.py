# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
import config
import os


def select_network_by_mask(road, mask, plaza_mask, output):
    """
    Clip the road network by a specified mask

    Input:
    :road   - str -  file name of the road layer
    :mask   - str -  file name of the mask layer
    :output - str -  file name of the output network

    Output:
    :output - str -  file name of the output network
    """
    if not arcpy.Exists(output):
        arcpy.MakeFeatureLayer_management(road, "road_lyr")
        print("match:{}".format(int(arcpy.GetCount_management("road_lyr")[0])))
        arcpy.SelectLayerByLocation_management("road_lyr", "INTERSECT", mask)
        print("match:{}".format(int(arcpy.GetCount_management("road_lyr")[0])))
        arcpy.SelectLayerByLocation_management(
            "road_lyr", "INTERSECT", plaza_mask, "", "REMOVE_FROM_SELECTION"
        )
        print("match:{}".format(int(arcpy.GetCount_management("road_lyr")[0])))
        arcpy.SelectLayerByAttribute_management(
            "road_lyr", "SUBSET_SELECTION", "\"FCC\" <> 'A11'"
        )
        print("match:{}".format(int(arcpy.GetCount_management("road_lyr")[0])))
        arcpy.CopyFeatures_management("road_lyr", output)
        return output
    else:
        print(output, " already exist")
        return output


def add_time_roadLevel(road):
    """
    Calculate the time cost and road level
    Input: 
    :road - str - the path of the road file 
    """
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
        return ((float(length)/ 5280 )/ 25 )*3600
    else:
        return ((float(length)/ 5280 )/ 20 )*3600"""
    codeblock2 = """Y
def getLevel(fcc):
    digit = int((fcc.strip())[1:])
    if digit < 20:
        return 1
    elif digit < 40:
        return 2
    else:
        return 3"""

    expression1 = "getTime(!FCC!, float(!LENGTH!))"
    arcpy.CalculateField_management(road, "TIME_COST", expression1, "PYTHON", codeblock)
    expression2 = "getLevel(!FCC!)"
    arcpy.CalculateField_management(road, "LEVEL", expression2, "PYTHON", codeblock2)


def add_truck_route(road):
    """
    add truck route attribute to the road file 
    Input: 
    :road - str - the path of the road file 
    """

    arcpy.AddField_management(road, "OldTrkRt", "SHORT")

    codeblock = """
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

    expression = "getOldTrkRt(!FENAME!)"
    arcpy.CalculateField_management(road, "OldTrkRt", expression, "PYTHON", codeblock)


def preprocess_network(road, mask, plaza_mask, output):
    """
    Preprocess the network for network building 
    Input: 
    :road - str -       path to the whole road file
    :mask - str -       path to mask of research area 
    :plaza_mast - str - path to the plaza mask 
    :output - str -     path to put the output road file 
    Output:
    None 
    """
    # arcpy settings
    env.workspace = config.working_folder
    env.overwriteOutput = True
    env.parallelProcessingFactor = "100%"
    # select road by mask
    selected_roads = select_network_by_mask(road, mask, plaza_mask, output)
    # add fields to the road
    add_time_roadLevel(selected_roads)
    add_truck_route(selected_roads)

