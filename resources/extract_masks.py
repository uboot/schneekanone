import cv2
import json
import numpy as np
import pprint

from constant import GID_TO_SPRITE_MAP

with open('../assets/level_masks.json', 'r') as f:
    level = json.load(f)

physics =  {}
for tileset in level['tilesets']:
    if not 'image' in tileset:
        continue
        
    gid = tileset['firstgid']

    for tile in tileset['tiles']:
        shapes = []
        
        for objectId, contour in enumerate(contours):
            polygon = []
            shape = []
            for pt in contour[::-1,0,:]:
                polygon.append({'x': int(pt[0]), 'y': int(pt[1])})
                shape.append(int(pt[0]))
                shape.append(int(pt[1]))
            shapes.append({
                'density': 2,
                'friction': 0,
                'bounce': 0,
                'filter': {'categoryBits': 1, 'maskBits': 65535},
                'shape': shape
            })

        if gid in GID_TO_SPRITE_MAP:
            spriteName = GID_TO_SPRITE_MAP[gid]['name']
            physics[spriteName] = shapes

        gid += 1

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(physics)

with open('../assets/sprites.json', 'w') as f:
    json.dump(physics, f)