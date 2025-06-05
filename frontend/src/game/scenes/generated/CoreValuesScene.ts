import Phaser from 'phaser';

export default class CoreValuesScene extends Phaser.Scene {
    private score: number = 0;
    private scoreText: Phaser.GameObjects.Text;
    private coreValues: { name: string, description: string }[];

    constructor() {
        super({ key: 'CoreValuesScene' });
        this.coreValues = [
            { name: 'Innovation', description: 'We embrace new ideas' },
            { name: 'Integrity', description: 'We do the right thing' },
            { name: 'Excellence', description: 'We strive for the best' },
            { name: 'Teamwork', description: 'We work together' },
            { name: 'Customer Focus', description: 'We put customers first' }
        ];
    }

    preload() {
        this.load.image('background', 'assets/background.png');
        this.load.image('valueIcon', 'assets/valueIcon.png');
        this.load.audio('collectSound', 'assets/collectSound.mp3');
    }

    create() {
        this.add.image(400, 300, 'background');

        // Create core values icons
        this.coreValues.forEach((value, index) => {
            const x = Phaser.Math.Between(50, 750);
            const y = Phaser.Math.Between(100, 500);
            const icon = this.physics.add.sprite(x, y, 'valueIcon').setInteractive();
            icon.setData('value', value);

            icon.on('pointerdown', () => {
                this.collectValue(icon);
            });

            this.tweens.add({
                targets: icon,
                y: y + 10,
                duration: 1000,
                yoyo: true,
                repeat: -1,
                ease: 'Sine.easeInOut'
            });
        });

        // Score text
        this.scoreText = this.add.text(16, 16, 'Score: 0', {
            fontSize: '32px',
            fill: '#000'
        });
    }

    update() {
        // Any update logic goes here
    }

    private collectValue(icon: Phaser.Physics.Arcade.Sprite) {
        const value = icon.getData('value') as { name: string, description: string };
        this.sound.play('collectSound');
        icon.destroy();

        this.score += 10;
        this.scoreText.setText('Score: ' + this.score);

        this.showValueDescription(value);
    }

    private showValueDescription(value: { name: string, description: string }) {
        const descriptionText = this.add.text(400, 300, `${value.name}: ${value.description}`, {
            fontSize: '24px',
            fill: '#fff',
            backgroundColor: '#000',
            padding: { x: 10, y: 5 },
            align: 'center'
        }).setOrigin(0.5);

        this.time.delayedCall(3000, () => {
            descriptionText.destroy();
        });
    }
}