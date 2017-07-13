import cv2
import json
import numpy as np

with open('../assets/level.json', 'r') as f:
    level = json.load(f)

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
        for id, contour in enumerate(contours):
            polygon = []
            shape = []
            for pt in contour[::-1,0,:]:
                polygon.append({'x': int(pt[0]+width/2), 'y': int(pt[1]+height/2)})

            obj = {
                'height': 0,
                'id': id + 1,
                'name': '',
                'polygon': polygon,
                'rotation': 0,
                'type': '',
                'visible': True,
                'width': 0,
                'x': -int(width/2),
                'y': -int(height/2)
            }
            objects.append(obj)

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

        gid += 1
        col += 1
        if col == columns:
            col = 0
            row += 1

    tileset['tiles'] = tiles

with open('../assets/level_masks.json', 'w') as f:
    json.dump(level, f, indent=2)
