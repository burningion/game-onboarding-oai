import Phaser from 'phaser';

export default class SecurityScene extends Phaser.Scene {
    private score: number;
    private securityItems: Phaser.GameObjects.Group;

    constructor() {
        super({ key: 'SecurityScene' });
        this.score = 0;
    }

    preload() {
        this.load.image('background', 'assets/security_background.png');
        this.load.image('puzzlePiece', 'assets/puzzle_piece.png');
        this.load.image('lock', 'assets/lock.png');
    }

    create() {
        this.add.image(400, 300, 'background');
        
        this.securityItems = this.physics.add.group({
            key: 'puzzlePiece',
            repeat: 5,
            setXY: { x: 100, y: 100, stepX: 120 }
        });

        this.securityItems.children.iterate((child: Phaser.GameObjects.GameObject) => {
            const puzzlePiece = child as Phaser.Physics.Arcade.Image;
            puzzlePiece.setInteractive();
            puzzlePiece.on('pointerdown', () => this.collectItem(puzzlePiece));
        });

        this.add.text(10, 10, 'Score: 0', { fontSize: '16px', fill: '#fff' }).setOrigin(0, 0).setScrollFactor(0);

        this.add.text(100, 550, 'Assemble the security puzzle by selecting correct policies!', { fontSize: '18px', fill: '#ffffff' });
        
        this.physics.world.setBoundsCollision(true, true, true, true);
    }

    update() {
        // Game logic updates
    }

    private collectItem(puzzlePiece: Phaser.Physics.Arcade.Image) {
        this.score += 10;
        puzzlePiece.setVisible(false);
        this.add.text(puzzlePiece.x, puzzlePiece.y, '+10', { fontSize: '18px', fill: '#0f0' }).setScrollFactor(0).setAlpha(1).setInteractive();
        this.updateScore();
    }

    private updateScore() {
        this.score += 10;
        this.children.getAll('text').forEach((text: Phaser.GameObjects.GameObject) => {
            if (text instanceof Phaser.GameObjects.Text && text.text.startsWith('Score:')) {
                text.setText(`Score: ${this.score}`);
            }
        });
    }
}