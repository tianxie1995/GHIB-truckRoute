# -*- coding: utf-8 -*-
# GLOBAL SETTINGS
working_folder = r"G:\我的云端硬盘\Capstone 603 GHIB\GIS\Data\GISdata"

# NETWORK SETTINGS
road = "RoadNetwork/Roads/Roads.shp"
mask = "Mask/Mask.gdb/Mask_2_11"
plaza_mask = "Mask/Mask.gdb/Plaza"
road_output = "RoadNetwork/Roads/network_.gdb/Road"

##OLD TRUCK ROUTE
oldTruckRoute = """[
        'Wyoming' ,'Wyoming/E I 94',
        'Wyoming/US 12' ,
        'Jefferson' , 'Dearborn' ,
        'Vernor' , 'Lonyo' ,
        'Lonyo/E I 94' ,'Springwells' , 
        'Livernois' , 'Livernois/E I 94' ,
        'Livernois/S I 75' , 'Dragoon' , 
        'Dragoon/N I 75' , 'Clark' ,
        'Clark/N I 75' , 'Clark/S I 75' , 
        'Grand' , 'Grand River/W I 94' ,
        'Michigan' , 'Fort', 'Westend' ]"""

# where the truck route design goes
truckRouteDesigns = {
    "First_Design": """[
        "Buchanan",
        "Central",
        "Dearborn",
        "Dix",
        "Dragoon",
        "Fort",
        "Green",
        "Livernois",
        "Michigan",
        "Scotten",
        "Waterman",
    ]""",
    "Second_Design": None,
    "Third_Design": None,
}
