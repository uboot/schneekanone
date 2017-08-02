FRAMES_PER_SECOND = 10.0
PLAYER_FAR_RIGHT_FRAME = 1
PLAYER_FAR_LEFT_FRAME = 9

function SchneeSprite(game, x, y, key, frame) {
  Phaser.Sprite.call(this, game, x, y, key, frame);
  this.shapeToFrameMap = new Map();
}

SchneeSprite.prototype = Object.create(Phaser.Sprite.prototype, {});

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
  game.load.tilemap('level', 'assets/sprites.json', null, Phaser.Tilemap.TILED_JSON);

  loadSpritesheet('bonus_sprites', 32, 32);
  loadSpritesheet('fence', 64, 64);
  loadSpritesheet('snow_groomer',  64, 64);
  loadSpritesheet('ground', 64, 64);
  loadSpritesheet('obstacles', 64, 64);
  loadSpritesheet('player', 35, 64);
  loadSpritesheet('finish', 64, 128);

  game.load.image('background', 'assets/background.png');
  game.load.physics('physics', 'assets/physics.json');
}

function create() {
  game.physics.startSystem(Phaser.Physics.P2JS);

  var map = game.add.tilemap('level');
  map.createFromObjects('background', 1, 'background');

  spriteGroup = game.add.group();
  spriteGroup.physicsBodyType = Phaser.Physics.P2JS;
  spriteGroup.enableBody = true;
  spriteGroup.classType = SchneeSprite;

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
  createObjects(map, 22, 'ground', 0);
  createObjects(map, 23, 'ground', 1);
  createObjects(map, 24, 'obstacles', 0);
  createObjects(map, 25, 'obstacles', 1);
  createObjects(map, 26, 'obstacles', 2);
  createObjects(map, 27, 'obstacles', 3);
  createObjects(map, 28, 'obstacles', 4);
  createObjects(map, 30, 'obstacles', 6);
  createObjects(map, 31, 'obstacles', 7);
  createObjects(map, 32, 'obstacles', 8);
  createObjects(map, 33, 'obstacles', 9);
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
    child.body
  });

  spriteGroup.iterate('name', 'lift_gate', Phaser.RETURN_NONE, function(child) {
    child.animations.add('move', [4, 5], FRAMES_PER_SECOND / 100, true);
    child.animations.play('move');
  });

  // the finish is usually not part of the level file...
  var finish = game.add.sprite(529, 305, 'finish', 0, spriteGroup);
  finish.name = 'finish';

  // ...the same holds for the player
  player = game.add.sprite(50, 20, 'player', 5, spriteGroup);
  player.name = 'player'
  player.animations.add('turn_left', [1, 2, 3, 4, 5, 6, 7, 8, 9], 5, false);
  player.animations.add('turn_right', [9, 8, 7, 6, 5, 4, 3, 2, 1], 5, false);
  player.animations.getAnimation('turn_left').enableUpdate = true;
  player.animations.getAnimation('turn_right').enableUpdate = true;
  player.animations.getAnimation('turn_left').onUpdate.add(updateVelocity);
  player.animations.getAnimation('turn_right').onUpdate.add(updateVelocity);

  player.body.velocity.x = 3 * FRAMES_PER_SECOND;
  player.body.velocity.y = 2 * FRAMES_PER_SECOND;

  // load the body polygons
  spriteGroup.forEach(function(child) {
    child.body.clearShapes();
    child.body.motionState = Phaser.Physics.P2.Body.KINEMATIC;
    child.body.debug = true;
    child.anchor.setTo(0.0, 0.0);

    // check if this sprite is animated
    if (! child.animations._outputFrames.length) {
      // if not simply load the mask for the current frame
      child.body.loadPolygon('physics', child.key + '_' + child.animations.frame);
      child.body.data.shapes.forEach(function(shape) {
          child.shapeToFrameMap.set(shape, child.animations.frame);
      });
    } else {
      // if this is an animated sprite load the masks of each animation frame
      // and populate the shapeToFrameMap accordingly
      var startIndex = 0;
      child.animations._outputFrames.forEach(function(frame) {
        child.body.loadPolygon('physics', child.key + '_' + frame);
        for (var i=startIndex; i < child.body.data.shapes.length; i++) {
          child.shapeToFrameMap.set(child.body.data.shapes[i], child.animations.frame);
        }
        startIndex = child.body.data.shapes.length;
      })
    }
  });

  cursors = game.input.keyboard.createCursorKeys();
}

function updateVelocity(animation, frame) {
  var velocity = new Phaser.Point();
  switch (frame.index) {
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

  player.body.velocity.x = velocity.x;
  player.body.velocity.y = velocity.y;
}

function update() {
  var currentFrame = player.frame;

  // stop turning left if necessary
  if (player.animations.getAnimation('turn_left').isPlaying
      && !cursors.right.isDown) {
    player.animations.stop('turn_left');
    console.log('stop turning left, frame:', currentFrame);
  }

  // stop turning right if necessary
  if (player.animations.getAnimation('turn_right').isPlaying
      && !cursors.left.isDown) {
    player.animations.stop('turn_right');
    console.log('stop turning right, frame:', currentFrame);
  }

  // continue if we keep on turning in either direction
  if (player.animations.getAnimation('turn_left').isPlaying ||
      player.animations.getAnimation('turn_right').isPlaying) {
    return;
  }

  // continue if no arrow key is pressed
  if (! (cursors.right.isDown || cursors.left.isDown)) {
    return;
  }

  // otherwise start the right animation
  var LEFT_MOST_FRAME = 9;
  var RIGHT_MOST_FRAME = 1;
  if (cursors.right.isDown && currentFrame < LEFT_MOST_FRAME) {
    player.play('turn_left');
    player.animations.getAnimation('turn_left').setFrame(currentFrame);
    player.frame = currentFrame;
    console.log('start turning left, frame:', currentFrame);
  } else if (cursors.left.isDown && currentFrame > RIGHT_MOST_FRAME) {
    player.play('turn_right');
    player.animations.getAnimation('turn_right').setFrame(currentFrame);
    player.frame = currentFrame;
    console.log('start turning right, frame:', currentFrame);
  }
}
