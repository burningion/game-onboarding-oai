import Phaser from 'phaser';

export default class BenefitsScene extends Phaser.Scene {
    private benefitsCollected: number;
    private collectionGoal: number;
    private scoreText: Phaser.GameObjects.Text;

    constructor() {
        super({ key: 'BenefitsScene' });
        this.benefitsCollected = 0;
        this.collectionGoal = 6; // Number of benefits to collect
    }

    preload() {
        this.load.image('background', 'assets/background.png');
        this.load.image('benefit', 'assets/benefit.png');
        this.load.audio('collectSound', 'assets/collect.mp3');
    }

    create() {
        this.add.image(400, 300, 'background');

        this.scoreText = this.add.text(16, 16, 'Benefits Collected: 0/6', {
            fontSize: '32px',
            fill: '#ffffff'
        });

        for (let i = 0; i < this.collectionGoal; i++) {
            const x = Phaser.Math.Between(100, 700);
            const y = Phaser.Math.Between(100, 500);
            const benefit = this.add.sprite(x, y, 'benefit').setInteractive();
            benefit.setScale(0.5);

            benefit.on('pointerdown', () => {
                this.collectBenefit(benefit);
            });
        }
    }

    update() {
        // Update logic if needed
    }

    private collectBenefit(benefit: Phaser.GameObjects.Sprite) {
        benefit.disableInteractive();
        benefit.setVisible(false);
        this.sound.play('collectSound');

        this.benefitsCollected++;
        this.scoreText.setText(`Benefits Collected: ${this.benefitsCollected}/6`);

        if (this.benefitsCollected === this.collectionGoal) {
            this.add.text(200, 300, 'All Benefits Collected!', {
                fontSize: '48px',
                fill: '#00ff00'
            });
        }
    }
}