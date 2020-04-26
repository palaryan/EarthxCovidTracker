import json
import random

coords = []
def gen(top_left, bottom_right, runs):
    points = []
    for i in range(runs):
        points.append({
            'latitude': round(random.uniform(top_left[0], bottom_right[0]), 8),
            'longitude': round(random.uniform(top_left[1], bottom_right[1]), 8),
            'weight': random.randint(20,100)
            })
    return points

coords = []
coords.extend(gen((33.216333, -97.441755),(31.109998, -93.489969), 10000))
#coords.extend(gen((32.821236, -96.803533),(32.820726, -96.802448), 10000))
#coords.extend(gen((32.819716, -96.812876),(32.811240, -96.806052), 200))
#coords.extend(gen((32.824918, -96.842525),(32.796063, -96.827590), 200))
print(coords)
