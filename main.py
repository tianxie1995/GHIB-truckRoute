import os
import config
from NetworkBuilder import preprocess_network

if __name__ == "__main__":
    road = os.path.join(config.working_folder, config.road)
    mask = os.path.join(config.working_folder, config.mask)
    plaza_mask = os.path.join(config.working_folder, config.plaza_mask)
    road_output = os.path.join(config.working_folder, config.road_output)
    old_truck_route_list = config.oldTruckRoute
    designed_truck_route_dict = config.truckRouteDesigns

    preprocess_network(
        road,
        old_truck_route_list,
        designed_truck_route_dict,
        mask,
        plaza_mask,
        road_output,
    )
