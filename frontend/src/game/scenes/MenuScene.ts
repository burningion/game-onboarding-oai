import Phaser from 'phaser';

export default class MenuScene extends Phaser.Scene {
  constructor() {
    super({ key: 'MenuScene' });
  }

  create() {
    const { width, height } = this.cameras.main;

    // Background
    this.add.rectangle(0, 0, width, height, 0x1a1a2e).setOrigin(0);

    // Title
    this.add.text(width / 2, height / 3, 'ACME Onboarding', {
      fontSize: '48px',
      color: '#ffffff',
      fontStyle: 'bold'
    }).setOrigin(0.5);

    // Subtitle
    this.add.text(width / 2, height / 3 + 60, 'with Coach Blaze', {
      fontSize: '24px',
      color: '#ffd700'
    }).setOrigin(0.5);

    // Start Button
    const startButton = this.add.rectangle(width / 2, height / 2 + 50, 200, 50, 0x4CAF50);
    const startText = this.add.text(width / 2, height / 2 + 50, 'Start Training', {
      fontSize: '20px',
      color: '#ffffff'
    }).setOrigin(0.5);

    // Make button interactive
    startButton.setInteractive({ useHandCursor: true });
    
    startButton.on('pointerover', () => {
      startButton.setFillStyle(0x45a049);
    });
    
    startButton.on('pointerout', () => {
      startButton.setFillStyle(0x4CAF50);
    });
    
    startButton.on('pointerdown', () => {
      this.scene.start('WelcomeScene');
    });

    // Sections Button
    const sectionsButton = this.add.rectangle(width / 2, height / 2 + 120, 200, 50, 0x2196F3);
    const sectionsText = this.add.text(width / 2, height / 2 + 120, 'View Sections', {
      fontSize: '20px',
      color: '#ffffff'
    }).setOrigin(0.5);

    // Make sections button interactive
    sectionsButton.setInteractive({ useHandCursor: true });
    
    sectionsButton.on('pointerover', () => {
      sectionsButton.setFillStyle(0x1976D2);
    });
    
    sectionsButton.on('pointerout', () => {
      sectionsButton.setFillStyle(0x2196F3);
    });
    
    sectionsButton.on('pointerdown', () => {
      this.scene.start('OnboardingSectionsScene');
    });

    // Instructions
    this.add.text(width / 2, height - 100, 'Use Arrow Keys to Move, Space to Jump, E to Interact', {
      fontSize: '16px',
      color: '#888888'
    }).setOrigin(0.5);
  }
}