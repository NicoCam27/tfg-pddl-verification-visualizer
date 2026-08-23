def reset_world(*listas):
    for lista in listas:
        if lista is not None:
            for obj in lista:
                obj.reset()