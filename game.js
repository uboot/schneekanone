FRAMES_PER_SECOND = 10.0

var game = new Phaser.Game(640, 480, Phaser.AUTO, '', { preload: preload, create: create, update: update });

function createObjects(tilemap, gid, spritesheet, frame)
{
  tilemap.createFromObjects('sprites', gid, spritesheet, frame, true, false, spriteGroup);
}

function preload() {
  // https://gamedevacademy.org/html5-phaser-tutorial-top-down-games-with-tiled/
  // https://gist.github.com/jdfight/9646833f9bbdcb1104db
  game.load.tilemap('level', 'assets/level_1.json', null, Phaser.Tilemap.TILED_JSON);
  game.load.spritesheet('bonus_sprites', 'assets/bonus_sprites.png', 32, 32);
  game.load.spritesheet('fence', 'assets/fence.png', 64, 64);
  game.load.spritesheet('snow_groomer', 'assets/snow_groomer.png', 64, 64);
  game.load.spritesheet('ground', 'assets/ground.png', 64, 64);
  game.load.spritesheet('obstacles', 'assets/obstacles.png', 64, 64);
  game.load.spritesheet('player', 'assets/player.png', 35, 64);
  
  game.load.image('background', 'assets/background.png');
  game.load.image('finish', 'assets/finish.png');
  
}

function create() {
  game.physics.startSystem(Phaser.Physics.ARCADE);
    
  var map = game.add.tilemap('level');
  map.createFromObjects('background', 1, 'background');
  
  spriteGroup = game.add.group();
  spriteGroup.enableBody = true;
  createObjects(map, 2, 'bonus_sprites', 0);
  createObjects(map, 2, 'bonus_sprites', 0);
  createObjects(map, 3, 'bonus_sprites', 1);
  createObjects(map, 4, 'bonus_sprites', 2);
  createObjects(map, 5, 'bonus_sprites', 3);
  createObjects(map, 6, 'fence', 0);
  createObjects(map, 7, 'fence', 1);
  createObjects(map, 8, 'fence', 2);
  createObjects(map, 9, 'fence', 3);
  createObjects(map, 10, 'fence', 4);
  createObjects(map, 11, 'fence', 5);
  createObjects(map, 12, 'fence', 6);
  createObjects(map, 13, 'fence', 7);
  createObjects(map, 14, 'fence', 8);
  createObjects(map, 15, 'fence', 9);
  createObjects(map, 16, 'fence', 10);
  createObjects(map, 17, 'fence', 11);
  createObjects(map, 18, 'fence', 12);
  createObjects(map, 19, 'fence', 13);
  createObjects(map, 24, 'obstacles', 0);
  createObjects(map, 25, 'obstacles', 1);
  createObjects(map, 26, 'obstacles', 2);
  createObjects(map, 27, 'obstacles', 3);
  createObjects(map, 28, 'obstacles', 4);
  createObjects(map, 30, 'obstacles', 6);
  createObjects(map, 31, 'obstacles', 7);
  createObjects(map, 36, 'snow_groomer', 0);
  createObjects(map, 39, 'snow_groomer', 3);
  createObjects(map, 21, 'finish');
  
  spriteGroup.iterate('name', 'snow_groomer_up', Phaser.RETURN_NONE, function(child) {
    child.animations.add('move', [0, 1, 2], FRAMES_PER_SECOND / 5, true);
    child.animations.play('move');
  });
  
  spriteGroup.iterate('name', 'snow_groomer_right', Phaser.RETURN_NONE, function(child) {
    child.animations.add('move', [5, 4, 3], FRAMES_PER_SECOND / 5, true);
    child.animations.play('move');
  });
  
  spriteGroup.iterate('name', 'lift_gate', Phaser.RETURN_NONE, function(child) {
    child.animations.add('move', [4, 5], FRAMES_PER_SECOND / 100, true);
    child.animations.play('move');
  });
}

function update() {
}
