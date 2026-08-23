from .action import Action


def create_action_load(drone, arm_name, box, start, duration = 1, cost = 1, description=""):

    if description == "":
            description = f'{drone.name}.load(arm_name="{arm_name}", box={box.name}, duration={duration}, cost={cost})'

    data = {"action_type": "load", "drone": drone, "arm_name": arm_name, "box": box}
    return Action(start=start, duration=duration, description=description, data=data, on_finish=lambda: drone.load(arm_name, box, duration, cost))
                                

def create_action_unload(drone, arm_name, box, person, start, duration = 1, cost = 1, description=""):
    
    if description == "":
            description = f'{drone.name}.unload(arm_name="{arm_name}", box={box.name}, person={person.name}, duration={duration}, cost={cost})'

    data = {"action_type": "unload", "drone": drone, "arm_name": arm_name, "box": box, "person": person}
    return Action(start=start, duration=duration, description=description, data=data, on_finish=lambda: drone.unload(arm_name, box, person, duration, cost))
  

def create_action_drop(drone, arm_name, box, start, duration = 1, cost = 1, description=""):
        
    if description == "":
            description = f'{drone.name}.drop(arm_name="{arm_name}", box={box.name}, duration={duration}, cost={cost})'

    data = {"action_type": "drop", "drone": drone, "arm_name": arm_name, "box": box}
    return Action(start=start, duration=duration, description=description, data=data, on_finish=lambda: drone.drop(arm_name, box, duration, cost))
