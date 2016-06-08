import os
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

sprites = [
    {
     "gid":2,
     "height":32,
     "id":18,
     "name":"wax_green",
     "width":32
    }, 
    {
     "gid":3,
     "height":32,
     "id":19,
     "name":"wax_pink",
     "width":32
    }, 
    {
     "gid":4,
     "height":32,
     "id":20,
     "name":"cup",
     "width":32
    }, 
    {
     "gid":5,
     "height":32,
     "id":21,
     "name":"chocolate",
     "width":32
    }, 
    {
     "gid":36,
     "height":64,
     "id":27,
     "name":"snow_groomer_up",
     "width":64
    }, 
    {
     "gid":39,
     "height":64,
     "id":28,
     "name":"snow_groomer_right",
     "width":64
    }, 
    {
     "gid":21,
     "height":128,
     "id":31,
     "name":"finish",
     "width":64
    }, 
    {
     "gid":6,
     "height":64,
     "id":33,
     "name":"fence_modern_90",
     "width":64
    }, 
    {
     "gid":7,
     "height":64,
     "id":34,
     "name":"fence_modern_0",
     "width":64
    }, 
    {
     "gid":8,
     "height":64,
     "id":35,
     "name":"fence_modern_135",
     "width":64
    }, 
    {
     "gid":9,
     "height":64,
     "id":36,
     "name":"fence_modern_45",
     "width":64
    }, 
    {
     "gid":10,
     "height":64,
     "id":38,
     "name":"fence_modern_45_long",
     "width":64
    }, 
    {
     "gid":11,
     "height":64,
     "id":39,
     "name":"fence_old_90",
     "width":64
    }, 
    {
     "gid":13,
     "height":64,
     "id":40,
     "name":"fence_old_135",
     "width":64
    }, 
    {
     "gid":12,
     "height":64,
     "id":43,
     "name":"fence_old_0",
     "width":64
    }, 
    {
     "gid":14,
     "height":64,
     "id":44,
     "name":"fence_old_45",
     "width":64
    }, 
    {
     "gid":15,
     "height":64,
     "id":45,
     "name":"fence_old_45_long",
     "width":64
    }, 
    {
     "gid":16,
     "height":64,
     "id":46,
     "name":"mat_long_0",
     "width":64
    }, 
    {
     "gid":17,
     "height":64,
     "id":47,
     "name":"mat_short_0",
     "width":64
    }, 
    {
     "gid":18,
     "height":64,
     "id":48,
     "name":"mat_long_90",
     "width":64
    }, 
    {
     "gid":19,
     "height":64,
     "id":49,
     "name":"mat_short_90",
     "width":64
    }, 
    {
     "gid":24,
     "height":64,
     "id":50,
     "name":"tree",
     "width":64
    }, 
    {
     "gid":25,
     "height":64,
     "id":51,
     "name":"car",
     "width":64
    }, 
    {
     "gid":26,
     "height":64,
     "id":52,
     "name":"pylon",
     "width":64
    }, 
    {
     "gid":27,
     "height":64,
     "id":53,
     "name":"skull",
     "width":64
    }, 
    {
     "gid":28,
     "height":64,
     "id":54,
     "name":"lift_gate",
     "width":64
    }, 
    {
     "gid":30,
     "height":64,
     "id":55,
     "name":"sign_right",
     "width":64
    }, 
    {
     "gid":31,
     "height":64,
     "id":56,
     "name":"sign_left",
     "width":64
    }, 
    {
     "gid":32,
     "height":64,
     "id":57,
     "name":"gate_red",
     "width":64
    }, 
    {
     "gid":33,
     "height":64,
     "id":58,
     "name":"gate_blue",
     "width":64
    }
]

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
    
with open('01001') as f:
    fixedSpriteCount = readShort(f)
    for i in range(fixedSpriteCount):
        print readFixedSprite(f)
        
    moveSpriteCount = readShort(f)
    for i in range(moveSpriteCount):
        print readMoveSprite(f)
        
    bonusSpriteCount = readShort(f)
    for i in range(bonusSpriteCount):
        print readBonusSprite(f)
    print len(f.read())
    
for name in os.listdir('.'):
    print name
    with open(name) as f:
        print readSpriteTemplate(f)


    