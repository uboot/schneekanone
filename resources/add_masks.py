import cv2
import json
import numpy as np
import pprint

from constant import GID_TO_SPRITE_MAP

with open('../assets/level.json', 'r') as f:
    level = json.load(f)

physics =  {}
for tileset in level['tilesets']:
    if not 'image' in tileset:
        continue
        
    tileCount = tileset['tilecount']
    columns = tileset['columns']
    row = 0
    col = 0
    height = tileset['tileheight']
    width = tileset['imagewidth'] // columns
    name = tileset['name']
    gid = tileset['firstgid']
    image = cv2.imread('../assets/{0}_mask.png'.format(name), -1)

    tiles = {}
    for tileId in range(tileCount):
        top = row * height
        left = col * width
        bottom = top + height
        right = left + width
        
        tileImage = image[top:bottom, left:right]
        
        mask = np.zeros_like(tileImage[:,:,0])
        maskPixels = ((tileImage[:,:,0] == 0) &
                      (tileImage[:,:,1] == 0) &
                      (tileImage[:,:,2] == 0) &
                      (tileImage[:,:,3] == 255))
        mask[maskPixels] = 255
        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        objects = []
        shapes = []
        for id, contour in enumerate(contours):
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

            object = {
                'height': 0,
                'id': id + 1,
                'name': '',
                'polygon': polygon,
                'rotation': 0,
                'type': '',
                'visible': True,
                'width': 0,
                'x': 0,
                'y': 0
            }
            objects.append(object)

        objectgroup = {
            'draworder': 'index',
            'height': 0,
            'name': '',
            'objects': objects,
            'opacity': 1,
            'type': 'objectgroup',
            'visible': True,
            'width': 0,
            'x': 0,
            'y': 0
        }

        tiles[str(tileId)] = {'objectgroup': objectgroup}

        if gid in GID_TO_SPRITE_MAP:
            spriteName = GID_TO_SPRITE_MAP[gid]['name']
            physics[spriteName] = shapes

        gid += 1
        col += 1
        if col == columns:
            col = 0
            row += 1

    tileset['tiles'] = tiles

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(physics)

with open('../assets/level_masks.json', 'w') as f:
    json.dump(level, f)

with open('../assets/sprites.json', 'w') as f:
    json.dump(physics, f)