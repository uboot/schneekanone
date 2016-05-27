import struct

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
    
with open('00200') as f:
    print readSpriteTemplate(f)
    
with open('00205') as f:
    print readSpriteTemplate(f)
    