FRAMES_PER_SECOND = 10

ID_TO_KEY_MAP = {
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
    215: 'gate_blue',
    216: 'gate_red',
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

SPRITES = [
    {
     "gid":2,
     "height":32,
     "name":"wax_green",
     "width":32
    },
    {
     "gid":3,
     "height":32,
     "name":"wax_pink",
     "width":32
    },
    {
     "gid":4,
     "height":32,
     "name":"cup",
     "width":32
    },
    {
     "gid":5,
     "height":32,
     "name":"chocolate",
     "width":32
    },
    {
     "gid":36,
     "height":64,
     "name":"snow_groomer_up",
     "width":64
    },
    {
     "gid":39,
     "height":64,
     "name":"snow_groomer_right",
     "width":64
    },
    {
     "gid":21,
     "height":128,
     "name":"finish",
     "width":64
    },
    {
     "gid":6,
     "height":64,
     "name":"fence_modern_90",
     "width":64
    },
    {
     "gid":7,
     "height":64,
     "name":"fence_modern_0",
     "width":64
    },
    {
     "gid":8,
     "height":64,
     "name":"fence_modern_135",
     "width":64
    },
    {
     "gid":9,
     "height":64,
     "name":"fence_modern_45",
     "width":64
    },
    {
     "gid":10,
     "height":64,
     "name":"fence_modern_45_long",
     "width":64
    },
    {
     "gid":11,
     "height":64,
     "name":"fence_old_90",
     "width":64
    },
    {
     "gid":13,
     "height":64,
     "name":"fence_old_135",
     "width":64
    },
    {
     "gid":12,
     "height":64,
     "name":"fence_old_0",
     "width":64
    },
    {
     "gid":14,
     "height":64,
     "name":"fence_old_45",
     "width":64
    },
    {
     "gid":15,
     "height":64,
     "name":"fence_old_45_long",
     "width":64
    },
    {
     "gid":16,
     "height":64,
     "name":"mat_long_0",
     "width":64
    },
    {
     "gid":17,
     "height":64,
     "name":"mat_short_0",
     "width":64
    },
    {
     "gid":18,
     "height":64,
     "name":"mat_long_90",
     "width":64
    },
    {
     "gid":19,
     "height":64,
     "name":"mat_short_90",
     "width":64
    },
    {
     "gid":24,
     "height":64,
     "name":"tree",
     "width":64
    },
    {
     "gid":25,
     "height":64,
     "name":"car",
     "width":64
    },
    {
     "gid":26,
     "height":64,
     "name":"pylon",
     "width":64
    },
    {
     "gid":27,
     "height":64,
     "name":"skull",
     "width":64
    },
    {
     "gid":28,
     "height":64,
     "name":"lift_gate",
     "width":64
    },
    {
     "gid":30,
     "height":64,
     "name":"sign_right",
     "width":64
    },
    {
     "gid":31,
     "height":64,
     "name":"sign_left",
     "width":64
    },
    {
     "gid":32,
     "height":64,
     "name":"gate_red",
     "width":64
    },
    {
     "gid":33,
     "height":64,
     "name":"gate_blue",
     "width":64
    },
    {
     "gid":22,
     "height":64,
     "name":"gras",
     "width":64
    },
    {
     "gid":23,
     "height":64,
     "name":"ice",
     "width":64
    },
    {
     "gid":42,
     "height":64,
     "name":"player",
     "width":35
    }
]

KEY_TO_SPRITE_MAP = dict()
for s in SPRITES:
    KEY_TO_SPRITE_MAP[s['name']] = s

GID_TO_SPRITE_MAP = dict()
for s in SPRITES:
    GID_TO_SPRITE_MAP[s['gid']] = s