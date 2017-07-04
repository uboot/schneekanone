import json
import string
import struct

from constant import FRAMES_PER_SECOND, KEY_TO_SPRITE_MAP, ID_TO_KEY_MAP

def readShort(stream):
    v, = struct.unpack('>h', stream.read(2))
    return v

def readLong(stream):
    v, = struct.unpack('>l', stream.read(4))
    return v
    
def readOSType(stream):
    data = []
    for i in range(4):
        data += struct.unpack('c', stream.read(1))
    return ''.join(data)
    
def readFixedSprite(stream):
    data = {
        'objectPosX': readShort(stream),
        'objectPosY': readShort(stream),
        'spriteID': readShort(stream),
        'spriteCount': readShort(stream),
        'deltaX': readShort(stream),
        'deltaY': readShort(stream)
    }
    return data
    
def readMoveSprite(stream):
    data = {
        'objectPosX': readShort(stream),
        'objectPosY': readShort(stream),
        'spriteID': readShort(stream),
        'moveX': readShort(stream),
        'moveY': readShort(stream),
        'moveDelay': readShort(stream),
        'moveDelayMult': readShort(stream),
        'baseX': readShort(stream),
        'baseY': readShort(stream),
        'spriteCount': readShort(stream),
        'deltaX': readShort(stream),
        'deltaY': readShort(stream)
    }
    return data
    
def readBonusSprite(stream):
    data = {
        'objectPosX': readShort(stream),
        'objectPosY': readShort(stream),
        'spriteID': readShort(stream),
        'spriteCount': readShort(stream),
        'deltaX': readShort(stream),
        'deltaY': readShort(stream),
        'lives': readShort(stream),
        'score': readShort(stream),
        'xLScore': readShort(stream)
    }
    return data
    
def readSpriteTemplate(stream):
    data = {
        'id': readOSType(stream),
        'horzPosition': readShort(stream),
        'vertPosition': readShort(stream),
        'moveDelay': readLong(stream),
        'moveDelayMult': readLong(stream),
        'celDelay': readLong(stream),
        'celDelayMult': readLong(stream),
        'visible': readShort(stream),
        'celIndex': readShort(stream),
        'celCount': readShort(stream),
        'cicnIDs': readShort(stream)
    }
    return data
    
def readLevel(stream):
    fixedSpriteCount = readShort(f)
    fixedSprites = []
    for i in range(fixedSpriteCount):
        fixedSprites.append(readFixedSprite(f))
        
    moveSpriteCount = readShort(f)
    moveSprites = []
    for i in range(moveSpriteCount):
        moveSprites.append(readMoveSprite(f))
        
    bonusSpriteCount = readShort(f)
    bonusSprites = []
    for i in range(bonusSpriteCount):
        bonusSprites.append(readBonusSprite(f))
    
    return {
        'fixedSprites': fixedSprites,
        'moveSprites': moveSprites,
        'bonusSprites': bonusSprites,
    }

def convertFixedSprite(sprite):
    properties = KEY_TO_SPRITE_MAP[ID_TO_KEY_MAP[sprite['spriteID']]]
    newSprite = []
    newSprite = {
        'gid': properties['gid'],
        'name': properties['name'],
        'rotation': 0,
        'visible': True,
        'width': properties['width'],
        'height':  properties['height']
    }
    return newSprite
    
def convertMoveSprite(sprite):
    newSprite = convertFixedSprite(sprite)
    speed = (FRAMES_PER_SECOND * 
             float(sprite['moveDelayMult']) / sprite['moveDelay'])
    properties = dict()
    properties['body.velocity.x'] = sprite['moveX'] * speed
    properties['body.velocity.y'] = sprite['moveY'] * speed
    propertyTypes = dict()
    propertyTypes['body.velocity.x'] = 'float'
    propertyTypes['body.velocity.y'] = 'float'
    newSprite['properties'] = properties
    newSprite['propertytypes'] = propertyTypes
    return newSprite
    
def convertBonusSprite(sprite):
    newSprite = convertFixedSprite(sprite)
    return newSprite
    
def replicateSprite(sprite, newSprite):
    properties = KEY_TO_SPRITE_MAP[ID_TO_KEY_MAP[sprite['spriteID']]]
    count = sprite['spriteCount']
    x = sprite['objectPosX']
    y = sprite['objectPosY'] + properties['height']
    deltaX = sprite['deltaX']
    deltaY = sprite['deltaY']
    newSprites = []
    for i in range(count):
        copy = newSprite.copy()
        copy['x'] = x
        copy['y'] = y
        x += deltaX
        y += deltaY
        newSprites.append(copy)
    return newSprites
    
def convertLevel(level):
    sprites = []
    for sprite in level['fixedSprites']:
        newSprite = convertFixedSprite(sprite)
        sprites += replicateSprite(sprite, newSprite)
        
    for sprite in level['moveSprites']:
        newSprite = convertMoveSprite(sprite)
        sprites += replicateSprite(sprite, newSprite)
        
    for sprite in level['bonusSprites']:
        newSprite = convertBonusSprite(sprite)
        sprites += replicateSprite(sprite, newSprite)
        
    index  = 2
    for newSprite in sprites:
        newSprite['id'] = index
        index += 1
    return sprites
    
with open('01000') as f:
    level = readLevel(f)

objects = convertLevel(level)

#import os
#for name in os.listdir('.'):
#    print name
#    with open(name) as f:
#        print readSpriteTemplate(f)

with open('level_template.json.in') as f:
    template = string.Template(f.read())
    
result = template.substitute(objects=json.dumps(objects),
                             nextobjectid=len(objects) + 2)
with open('../assets/level_1.json', 'w') as f:
    f.write(result)
