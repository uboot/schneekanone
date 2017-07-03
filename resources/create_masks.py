import cv2
import json
import numpy as np

with open('../assets/level.json', 'r') as f:
    level = json.load(f)
    
for tileset in level['tilesets']:
    if not tileset.has_key('image'):
        continue
        
    tilecount = tileset['tilecount']
    columns = tileset['columns']
    row = 0
    col = 0
    height = tileset['tileheight']
    width = tileset['imagewidth'] // columns
    name = tileset['name']
    image = cv2.imread('../assets/{0}_mask.png'.format(name), -1)
    
    print(image.shape, width, height)
    
    for tileId in range(tilecount):
        top = row * height
        left = col * width
        bottom = top + height
        right = left + width
        
        tile = image[top:bottom, left:right]
        
        mask = np.zeros_like(tile[:,:,0])
        maskPixels = ((tile[:,:,0] == 0) & 
                      (tile[:,:,1] == 0) &
                      (tile[:,:,2] == 0) & 
                      (tile[:,:,3] == 255))
        mask[maskPixels] = 255 
        print mask[:10,:10]
        
        if tileId == 0:
            exit()
        
        col += 1
        if col == columns:
            col = 0
            row += 1
            