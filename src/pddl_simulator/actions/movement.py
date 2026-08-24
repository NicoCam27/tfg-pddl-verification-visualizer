from .action import Action


def create_action_move(drone, origin, destination, start, duration = 1, cost = 1, description=""):

    if description == "":
        description = f'{drone.name}.move(origin="{origin}", destination="{destination}", duration={duration}, cost={cost})'

    data = {"action_type": "move", "drone": drone, "origin": origin, "destination": destination}
    return Action(start=start, duration=duration, description=description, action_type="move", data=data, on_finish=lambda: drone.move(origin, destination, duration, cost))
