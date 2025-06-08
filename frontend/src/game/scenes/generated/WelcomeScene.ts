import Phaser from 'phaser';

export default class WelcomeScene extends Phaser.Scene {
    private player!: Phaser.Physics.Arcade.Sprite;
    private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
    private score: number = 0;
    private scoreText!: Phaser.GameObjects.Text;

    constructor() {
        super({ key: 'WelcomeScene' });
    }

    preload() {
        this.load.image('platform', 'assets/platform.png');
        this.load.image('background', 'assets/background.png');
        this.load.image('collectible', 'assets/collectible.png');
        this.load.spritesheet('player', 'assets/player.png', { frameWidth: 32, frameHeight: 48 });
    }

    create() {
        this.add.image(400, 300, 'background').setScale(2);

        const platforms = this.physics.add.staticGroup();
        platforms.create(400, 568, 'platform').setScale(2).refreshBody();
        platforms.create(600, 400, 'platform');
        platforms.create(50, 250, 'platform');
        platforms.create(750, 220, 'platform');

        this.player = this.physics.add.sprite(100, 450, 'player');
        this.player.setBounce(0.2);
        this.player.setCollideWorldBounds(true);

        this.anims.create({
            key: 'left',
            frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
            frameRate: 10,
            repeat: -1
        });

        this.anims.create({
            key: 'turn',
            frames: [{ key: 'player', frame: 4 }],
            frameRate: 20
        });

        this.anims.create({
            key: 'right',
            frames: this.anims.generateFrameNumbers('player', { start: 5, end: 8 }),
            frameRate: 10,
            repeat: -1
        });

        this.cursors = this.input.keyboard!.createCursorKeys();

        const collectibles = this.physics.add.group({
            key: 'collectible',
            repeat: 11,
            setXY: { x: 12, y: 0, stepX: 70 }
        });

        collectibles.children.iterate((child: Phaser.GameObjects.GameObject) => {
            const collectible = child as Phaser.Physics.Arcade.Image;
            collectible.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
            return true;
        });

        this.physics.add.collider(this.player, platforms);
        this.physics.add.collider(collectibles, platforms);

        this.physics.add.overlap(this.player, collectibles, this.collectCollectible, undefined, this);

        this.scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', color: '#000' });
    }

    update() {
        if (this.cursors.left.isDown) {
            this.player.setVelocityX(-160);
            this.player.anims.play('left', true);
        } else if (this.cursors.right.isDown) {
            this.player.setVelocityX(160);
            this.player.anims.play('right', true);
        } else {
            this.player.setVelocityX(0);
            this.player.anims.play('turn');
        }

        if (this.cursors.up.isDown && this.player.body!.touching.down) {
            this.player.setVelocityY(-330);
        }
    }

    private collectCollectible = (player: Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Physics.Arcade.Body | Phaser.Physics.Arcade.StaticBody | Phaser.Tilemaps.Tile, collectible: Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Physics.Arcade.Body | Phaser.Physics.Arcade.StaticBody | Phaser.Tilemaps.Tile) => {
        const item = collectible as Phaser.Physics.Arcade.Image;
        item.disableBody(true, true);

        this.score += 10;
        this.scoreText.setText('Score: ' + this.score);

        // Display onboarding messages upon collecting items
        const messages = [
            "Welcome to ACME Corp!",
            "Embrace our company culture.",
            "Innovation is our strength!",
            "Collaboration is key.",
            "Integrity in all actions.",
            "Customer first approach.",
            "Diversity and inclusion.",
            "Continuous learning.",
            "Work-life balance.",
            "Sustainability matters."
        ];

        const messageIndex = Phaser.Math.Between(0, messages.length - 1);
        this.add.text(100, 100, messages[messageIndex], { fontSize: '16px', color: '#00f' }).setScrollFactor(0).setDepth(1);
    }
}