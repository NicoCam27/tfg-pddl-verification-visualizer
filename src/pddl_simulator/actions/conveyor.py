from .action import Action 


def create_action_move_conveyor(drone, conveyor, origin, destination, start, duration = 1, cost = 1, description=""):

    if description == "":
        description = f'{drone.name}.move_conveyor(conveyor={conveyor.name}, origin="{origin}", destination="{destination}", duration={duration}, cost={cost})'
 
    data = {"action_type": "move_conveyor", "drone": drone, "conveyor": conveyor, "origin": origin, "destination": destination}
    return Action(start=start, duration=duration, description=description, action_type="move_conveyor", data=data, on_start=lambda: drone.move_conveyor(conveyor, origin, destination, duration, cost))

    
def create_action_load_conveyor_with_box(drone, arm, box, conveyor, start, duration = 1, cost = 1, description=""):
        
    if description == "":
            description = f'{drone.name}.load_conveyor_with_box(arm={arm.name}, box={box.name}, conveyor={conveyor.name}, duration={duration}, cost={cost})'

    data = {"action_type": "load_conveyor_with_box", "drone": drone, "arm": arm, "box": box, "conveyor": conveyor}
    return Action(start=start, duration=duration, description=description, data=data, on_start=lambda: drone.load_conveyor_with_box(arm, box, conveyor, duration, cost))


def create_action_unload_box_from_conveyor(drone, arm, box, conveyor, start, duration = 1, cost = 1, description=""):
        
    if description == "":
            description = f'{drone.name}.unload_box_from_conveyor(arm={arm.name}, box={box.name}, conveyor={conveyor.name}, duration={duration}, cost={cost})'

    data = {"action_type": "unload_box_from_conveyor", "drone": drone, "arm": arm, "box": box, "conveyor": conveyor}
    return Action(start=start, duration=duration, description=description, data=data, on_start=lambda: drone.unload_box_from_conveyor(arm, box, conveyor, duration, cost))
