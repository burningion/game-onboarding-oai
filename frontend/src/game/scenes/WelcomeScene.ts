import Phaser from 'phaser';

export default class WelcomeScene extends Phaser.Scene {
  private playerName: string = '';
  private nameInput?: Phaser.GameObjects.Text;
  private coachBlaze?: Phaser.GameObjects.Sprite;
  private speechBubble?: Phaser.GameObjects.Container;

  constructor() {
    super({ key: 'WelcomeScene' });
  }

  create() {
    const { width, height } = this.cameras.main;

    // Gym background
    this.add.rectangle(0, 0, width, height, 0x87CEEB).setOrigin(0);
    
    // Floor
    this.add.rectangle(0, height - 100, width, 100, 0x8B4513).setOrigin(0);

    // Coach Blaze placeholder (red square for now)
    this.coachBlaze = this.add.sprite(width - 150, height - 150, 'coach');
    this.coachBlaze.setScale(100, 100);
    this.coachBlaze.setTint(0xFF0000);

    // Speech bubble
    this.createSpeechBubble(
      "Hey there, superstar! Welcome to ACME's starting line! 🏁\n" +
      "What name should go on your badge?\n" +
      "Type your name and press ENTER!"
    );

    // Name input field
    this.nameInput = this.add.text(width / 2, height / 2 + 50, 'Type your name...', {
      fontSize: '24px',
      color: '#333333',
      backgroundColor: '#ffffff',
      padding: { x: 20, y: 10 }
    }).setOrigin(0.5);

    // Keyboard input
    this.input.keyboard?.on('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter' && this.playerName.length > 0) {
        this.confirmName();
      } else if (event.key === 'Backspace') {
        this.playerName = this.playerName.slice(0, -1);
        this.updateNameDisplay();
      } else if (event.key.length === 1 && this.playerName.length < 20) {
        this.playerName += event.key;
        this.updateNameDisplay();
      }
    });
  }

  private createSpeechBubble(text: string) {
    const bubble = this.add.graphics();
    const bubbleWidth = 400;
    const bubbleHeight = 150;
    const x = 100;
    const y = 50;

    // Draw bubble
    bubble.fillStyle(0xffffff);
    bubble.fillRoundedRect(x, y, bubbleWidth, bubbleHeight, 16);
    bubble.lineStyle(2, 0x000000);
    bubble.strokeRoundedRect(x, y, bubbleWidth, bubbleHeight, 16);

    // Add text
    const bubbleText = this.add.text(x + 20, y + 20, text, {
      fontSize: '16px',
      color: '#000000',
      wordWrap: { width: bubbleWidth - 40 }
    });

    this.speechBubble = this.add.container(0, 0, [bubble, bubbleText]);
  }

  private updateNameDisplay() {
    if (this.nameInput) {
      this.nameInput.setText(this.playerName || 'Type your name...');
    }
  }

  private confirmName() {
    // Update speech bubble
    this.speechBubble?.destroy();
    this.createSpeechBubble(
      `Fantastic form, ${this.playerName}!\n` +
      "Let's crush this onboarding workout!\n" +
      "Press SPACE to continue!"
    );

    // Wait for space key
    this.input.keyboard?.once('keydown-SPACE', () => {
      // Store player name in registry
      this.registry.set('playerName', this.playerName);
      // Move to next scene
      this.scene.start('CoreValuesScene');
    });
  }
}