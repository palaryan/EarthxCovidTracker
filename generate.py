import random
coords = [[32.821002, -96.802862], [32.820871, -96.802763], [32.820556, -96.802740], [32.820480, -96.803858], [32.821470, -96.802783], [32.821211, -96.802043], [32.821064, -96.802912], [32.821340, -96.801974], [32.820478, -96.802683], [32.819979, -96.802690], [32.821386, -96.802165], [32.821001, -96.801954] ]
points = []
for coord in coords:
    for i in range(random.randrange(1000, 10000)):
        longitude = coord[1] - (random.randrange(10000, 20000) / 288200)
        lat = coord[0] - (random.randrange(10000, 20000) / 364000)
        points.append({'latitude':lat, 'longitude': longitude, 'weight':1})
print(points)

