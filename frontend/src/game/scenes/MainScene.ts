import Phaser from 'phaser';

export default class MainScene extends Phaser.Scene {
  private player!: Phaser.Types.Physics.Arcade.SpriteWithDynamicBody;
  private platforms!: Phaser.Physics.Arcade.StaticGroup;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private background!: Phaser.GameObjects.TileSprite;

  constructor() {
    super({ key: 'MainScene' });
  }

  preload() {
    // Create simple colored rectangles for now
    this.load.image('sky', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==');
    this.load.image('ground', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==');
    this.load.image('player', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==');
  }

  create() {
    // Create scrolling background
    this.background = this.add.tileSprite(0, 0, 800, 600, 'sky');
    this.background.setOrigin(0, 0);
    this.background.setTint(0x87CEEB);

    // Create platforms
    this.platforms = this.physics.add.staticGroup();
    
    // Ground platform
    const ground = this.platforms.create(400, 568, 'ground');
    ground.setScale(800, 64).refreshBody();
    ground.setTint(0x228B22);

    // Floating platforms
    this.platforms.create(600, 400, 'ground').setScale(200, 20).refreshBody().setTint(0x228B22);
    this.platforms.create(50, 250, 'ground').setScale(200, 20).refreshBody().setTint(0x228B22);
    this.platforms.create(750, 220, 'ground').setScale(200, 20).refreshBody().setTint(0x228B22);

    // Create player
    this.player = this.physics.add.sprite(100, 450, 'player');
    this.player.setScale(32, 32);
    this.player.setTint(0xFF0000);
    this.player.setBounce(0.2);
    this.player.setCollideWorldBounds(true);

    // Player physics
    this.physics.add.collider(this.player, this.platforms);

    // Create cursor keys
    this.cursors = this.input.keyboard!.createCursorKeys();

    // Camera follows player
    this.cameras.main.startFollow(this.player);
    this.cameras.main.setBounds(0, 0, 800, 600);
  }

  update() {
    // Player movement
    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-160);
    } else if (this.cursors.right.isDown) {
      this.player.setVelocityX(160);
    } else {
      this.player.setVelocityX(0);
    }

    // Jump
    if (this.cursors.up.isDown && this.player.body.touching.down) {
      this.player.setVelocityY(-330);
    }

    // Parallax scrolling background
    this.background.tilePositionX = this.cameras.main.scrollX * 0.5;
  }
}