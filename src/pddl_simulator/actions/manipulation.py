from .action import Action


def create_action_load(drone, arm, box, start, duration = 1, cost = 1, description=""):

    if description == "":
            description = f'{drone.name}.load(arm="{arm}", box={box.name}, duration={duration}, cost={cost})'

    data = {"action_type": "load", "drone": drone, "arm": arm, "box": box}
    return Action(start=start, duration=duration, description=description, data=data, on_finish=lambda: drone.load(arm, box, duration, cost))
                                

def create_action_unload(drone, arm, box, person, start, duration = 1, cost = 1, description=""):
    
    if description == "":
            description = f'{drone.name}.unload(arm="{arm}", box={box.name}, person={person.name}, duration={duration}, cost={cost})'

    data = {"action_type": "unload", "drone": drone, "arm": arm, "box": box, "person": person}
    return Action(start=start, duration=duration, description=description, data=data, on_finish=lambda: drone.unload(arm, box, person, duration, cost))
  

def create_action_drop(drone, arm, box, start, duration = 1, cost = 1, description=""):
        
    if description == "":
            description = f'{drone.name}.drop(arm="{arm}", box={box.name}, duration={duration}, cost={cost})'

    data = {"action_type": "drop", "drone": drone, "arm": arm, "box": box}
    return Action(start=start, duration=duration, description=description, data=data, on_finish=lambda: drone.drop(arm, box, duration, cost))
