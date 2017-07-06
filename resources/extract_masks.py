import json

from constant import GID_TO_SPRITE_MAP

with open('../assets/level_masks.json', 'r') as f:
    level = json.load(f)

physics =  {}
for tileset in level['tilesets']:
    if not 'image' in tileset:
        continue
        
    gid = tileset['firstgid']

    for tile in tileset['tiles']:
        objects = tileset['tiles'][tile]['objectgroup']['objects']
        
        shapes = []
        for obj in objects:
            polygon = obj['polygon']
            points = []
            for point in polygon:
                points.append(point['x'])
                points.append(point['y'])
            
            shape = {
                'density': 2,
                'friction': 0,
                'bounce': 0,
                'filter': {'categoryBits': 1, 'maskBits': 65535},
                'shape': points
            }
            
            shapes.append(shape)
#
        if gid in GID_TO_SPRITE_MAP:
            spriteName = GID_TO_SPRITE_MAP[gid]['name']
            physics[spriteName] = shapes

        gid += 1

with open('../assets/sprites.json', 'w') as f:
    json.dump(physics, f, indent=2)