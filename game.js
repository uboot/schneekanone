FRAMES_PER_SECOND = 10.0
PLAYER_FAR_RIGHT_FRAME = 1
PLAYER_FAR_LEFT_FRAME = 9

function SchneeSprite(game, x, y, key, frame) {
  Phaser.Sprite.call(this, game, x, y, key, frame);
}

SchneeSprite.prototype = Object.create(Phaser.Sprite.prototype, {
});

var game = new Phaser.Game(640, 480, Phaser.AUTO, '', { 
  preload: preload, 
  create: create, 
  update: update 
});

function createObjects(tilemap, gid, spritesheet, frame) {
  tilemap.createFromObjects('sprites', gid, spritesheet, frame, true, false,
                            spriteGroup, SchneeSprite);
}

function loadSpritesheet(key, frameWidth, frameHeight) {
  var url = 'assets/' + key + '.png';
  game.load.spritesheet(key, url, frameWidth, frameHeight);
}

function preload() {
  // https://gamedevacademy.org/html5-phaser-tutorial-top-down-games-with-tiled/
  // https://gist.github.com/jdfight/9646833f9bbdcb1104db
  game.load.tilemap('level', 'assets/level.json', null, Phaser.Tilemap.TILED_JSON);

  loadSpritesheet('bonus_sprites', 32, 32);
  loadSpritesheet('fence', 64, 64);
  loadSpritesheet('snow_groomer',  64, 64);
  loadSpritesheet('ground', 64, 64);
  loadSpritesheet('obstacles', 64, 64);
  loadSpritesheet('player', 35, 64);
  loadSpritesheet('finish', 64, 128);
  
  game.load.image('background', 'assets/background.png');
  game.load.physics('physics', 'assets/sprites.json');
}

function create() {
  game.physics.startSystem(Phaser.Physics.P2JS);
    
  var map = game.add.tilemap('level');
  map.createFromObjects('background', 1, 'background');
  
  spriteGroup = game.add.group();
  spriteGroup.enableBody = true;
  spriteGroup.physicsBodyType = Phaser.Physics.P2JS;

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

  // add animations
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

  // the finish is usually not part of the level file
  var finish = game.add.sprite(529, 305, 'finish', 0, spriteGroup);
  finish.name = 'finish'

  // load the body polygons
  spriteGroup.forEach(function(child) {
    child.body.motionState = Phaser.Physics.P2.Body.STATIC;
    child.body.loadPolygon('physics', child.name);
  });
  
  player = game.add.sprite(50, 20, 'player', 5, spriteGroup);
  player.animations.add('turn_left', [1, 2, 3, 4, 5, 6, 7, 8, 9], 5);
  player.animations.add('turn_right', [9, 8, 7, 6, 5, 4, 3, 2, 1], 5);
  player.body.velocity.x = 3 * FRAMES_PER_SECOND;
  player.body.velocity.y = 2 * FRAMES_PER_SECOND;
  player.body.motionState = Phaser.Physics.P2.Body.STATIC;
  
  cursors = game.input.keyboard.createCursorKeys();
}

function updateVelocity()
{
  var velocity = new Phaser.Point();
  switch (player.frame) {
    case 1:
      velocity.set(-2 * FRAMES_PER_SECOND, 3 * FRAMES_PER_SECOND);
      break;
    case 2:
      velocity.set(-FRAMES_PER_SECOND, 3 * FRAMES_PER_SECOND);
      break;
    case 3:
      velocity.set(0, FRAMES_PER_SECOND);
      break;
    case 4:
      velocity.set(FRAMES_PER_SECOND, 3 * FRAMES_PER_SECOND);
      break;
    case 5:
      velocity.set(3 * FRAMES_PER_SECOND, 2 * FRAMES_PER_SECOND);
      break;
    case 6:
      velocity.set(3 * FRAMES_PER_SECOND, FRAMES_PER_SECOND);
      break;
    case 7:
      velocity.set(FRAMES_PER_SECOND, 0);
      break;
    case 8:
      velocity.set(3 * FRAMES_PER_SECOND, -FRAMES_PER_SECOND);
      break;
    case 9:
      velocity.set(3 * FRAMES_PER_SECOND, -2 * FRAMES_PER_SECOND);
      break;
  }
  
  player.body.velocity = velocity;
}

function update() {
  if (cursors.left.isDown && !player.animations.getAnimation('turn_right').isPlaying)
  {
    var currentFrame = player.frame;
    player.play('turn_right');
    player.animations.getAnimation('turn_right').setFrame(currentFrame);
  } else if (cursors.right.isDown && !player.animations.getAnimation('turn_left').isPlaying) {
    var currentFrame = player.frame;
    player.play('turn_left');
    player.animations.getAnimation('turn_left').setFrame(currentFrame);
  } else if (!cursors.left.isDown && !cursors.right.isDown) {
    player.animations.stop('turn_left');
    player.animations.stop('turn_right');
  }
}
