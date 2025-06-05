import Phaser from 'phaser';

export class BenefitsCollectionScene extends Phaser.Scene {
    private score: number;
    private scoreText: Phaser.GameObjects.Text;
    private benefits: Phaser.Physics.Arcade.Group;
    private player: Phaser.Types.Physics.Arcade.SpriteWithDynamicBody;

    constructor() {
        super({ key: 'BenefitsCollectionScene' });
        this.score = 0;
    }

    preload() {
        // Load assets
        this.load.image('background', 'assets/background.png');
        this.load.image('player', 'assets/player.png');
        this.load.image('healthInsurance', 'assets/healthInsurance.png');
        this.load.image('retirement', 'assets/retirement.png');
        this.load.image('pto', 'assets/pto.png');
        this.load.image('lifeInsurance', 'assets/lifeInsurance.png');
        this.load.image('developmentBudget', 'assets/developmentBudget.png');
    }

    create() {
        // Add background
        this.add.image(400, 300, 'background');

        // Create player
        this.player = this.physics.add.sprite(400, 500, 'player');
        this.player.setCollideWorldBounds(true);

        // Create benefits group
        this.benefits = this.physics.add.group({
            key: ['healthInsurance', 'retirement', 'pto', 'lifeInsurance', 'developmentBudget'],
            setXY: { x: 50, y: 50, stepX: 150 }
        });

        this.benefits.children.iterate((benefit: Phaser.GameObjects.GameObject) => {
            const sprite = benefit as Phaser.Physics.Arcade.Sprite;
            sprite.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
        });

        // Add score text
        this.scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', fill: '#fff' });

        // Set collision detection
        this.physics.add.collider(this.player, this.benefits, this.collectBenefit, undefined, this);

        // Add keyboard controls
        this.input.keyboard.on('keydown-LEFT', () => this.player.setVelocityX(-160));
        this.input.keyboard.on('keydown-RIGHT', () => this.player.setVelocityX(160));
        this.input.keyboard.on('keyup-LEFT', () => this.player.setVelocityX(0));
        this.input.keyboard.on('keyup-RIGHT', () => this.player.setVelocityX(0));
    }

    update() {
        // Game updates
        // Additional game logic can be added here
    }

    private collectBenefit(player: Phaser.Types.Physics.Arcade.SpriteWithDynamicBody, benefit: Phaser.GameObjects.GameObject) {
        benefit.destroy();
        this.score += 10;
        this.scoreText.setText('Score: ' + this.score);
    }
}