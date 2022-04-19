import os
import json

import numpy as np

np.random.seed(42)

worlds = {
    0: {"cells": [[-0.04, -0.04, -0.04, +1],
                [-0.04, None, -0.04, -1],
                [-0.04, -0.04, -0.04, -0.04]],
        "terminals": [(3, 2), (3, 1)]
    }
}

for ix in range(9):
    world = np.zeros((40, 40)) - 0.1
    for _ in range(np.random.randint(1, 200)):
        x, y = (np.random.randint(1, 40), np.random.randint(1, 40))
        world[x, y] = None
    # Death cell
    x, y = (np.random.randint(1, 40), np.random.randint(1, 40))
    world[x, y] = -10000

    # Win cell
    x_, y_ = (np.random.randint(1, 40), np.random.randint(1, 40))
    while x_ == x and y_ == y:
        x_, y_ = (np.random.randint(1, 40), np.random.randint(1, 40))
    world[x_, y_] = 10000
    terminals = [(x, y), (x_, y_)]
    cells = []
    for row in world:
        r = []
        for c in row:
            if np.isnan(c):
                r.append(None)
            else:
                r.append(c)
        cells.append(r)

    worlds[ix + 1] = {"cells": cells, "terminals": terminals}

with open(os.path.join("api", "worlds.json"), "w") as file:
    json.dump(worlds, file)