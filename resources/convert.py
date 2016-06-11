import json
import string
import struct

idToKeyMap = {
    201: 'fence_modern_90',
    202: 'fence_modern_0',
    203: 'fence_modern_135', 
    204: 'fence_modern_45', 
    205: 'snow_groomer_up', 
    206: 'tree', 
    207: 'gras', 
    208: 'ice', 
    210: 'finish', 
    211: 'pylon', 
    212: 'car', 
    214: 'snow_groomer_right', 
    215: 'Doppeltor rot"', 
    216: 'Doppeltor blau"', 
    217: 'fence_old_90', 
    218: 'fence_old_0', 
    219: 'fence_old_135', 
    220: 'fence_old_45', 
    221: 'mat_long_0', 
    222: 'mat_short_0', 
    223: 'mat_long_90', 
    224: 'mat_short_90', 
    225: 'sign_right', 
    226: 'sign_left', 
    227: 'lift_gate', 
    228: 'cup', 
    229: 'wax_green', 
    230: 'wax_pink', 
    231: 'fence_modern_45_long', 
    232: 'fence_old_45_long', 
    234: 'chocolate', 
    233: 'skull'
}

keyToGidMap = {
    'wax_green': 2,
    'wax_pink': 3,
    'cup': 4,
    'chocolate': 5,
    'snow_groomer_up': 36,
    'snow_groomer_right': 39,
    'finish': 21,
    'fence_modern_90': 6,
    'fence_modern_0': 7,
    'fence_modern_135': 8,
    'fence_modern_45': 9,
    'fence_modern_45_long': 10,
    'fence_old_90': 11,
    'fence_old_135': 13,
    'fence_old_0': 12,
    'fence_old_45': 14,
    'fence_old_45_long': 15,
    'mat_long_0': 16,
    'mat_short_0': 17,
    'mat_long_90': 18,
    'mat_short_90': 19,
    'tree': 24,
    'car': 25,
    'pylon': 26,
    'skull': 27,
    'lift_gate': 28,
    'sign_right': 30,
    'sign_left': 31,
    'gate_red': 32,
    'gate_blue': 33
}

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
        fixedSprites.append(readMoveSprite(f))
        
    bonusSpriteCount = readShort(f)
    bonusSprites = []
    for i in range(bonusSpriteCount):
        bonusSprites.append(readBonusSprite(f))
        
    assert (0 == len(f.read()))
    
    return {
        'fixedSprites': fixedSprites,
        'moveSprites': moveSprites,
        'bonusSprites': bonusSprites,
    }

def convertFixedSprite(sprite):
    result = {
        'gid': keyToGidMap[idToKeyMap[sprite['spriteID']]]
    }
    return result
    
def convertMoveSprite(sprite):
    result = convertFixedSprite(sprite)
    return result
    
def convertBonusSprite(sprite):
    result = convertFixedSprite(sprite)
    return result
    
def convertLevel(level):
    sprites = []
    for sprite in level['fixedSprites']:
        sprites.append(convertFixedSprite(sprite))
        
    for sprite in level['moveSprites']:
        sprites.append(convertMoveSprite(sprite))
        
    for sprite in level['moveSprites']:
        sprites.append(convertBonusSprite(sprite))
    return sprites
    
with open('01001') as f:
    level = readLevel(f)

objects = convertLevel(level)

#for name in os.listdir('.'):
#    print name
#    with open(name) as f:
#        readSpriteTemplate(f)

with open('level_template.json.in') as f:
    template = string.Template(f.read())
    
result = template.substitute(objects = json.dumps(objects))
with open('../assets/level_0.json', 'w') as f:
    f.write(result)
    