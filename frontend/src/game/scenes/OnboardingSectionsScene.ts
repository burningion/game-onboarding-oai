import Phaser from 'phaser';
import { audioManager } from '../../utils/audioManager';

interface Section {
  number: number;
  title: string;
  x: number;
  y: number;
  text?: Phaser.GameObjects.Text;
  background?: Phaser.GameObjects.Rectangle;
  isPlaying?: boolean;
  audio?: HTMLAudioElement;
}

export default class OnboardingSectionsScene extends Phaser.Scene {
  private sections: Section[] = [];

  constructor() {
    super({ key: 'OnboardingSectionsScene' });
  }

  create() {
    const { width, height } = this.cameras.main;

    // Background
    this.add.rectangle(0, 0, width, height, 0x1a1a2e).setOrigin(0);

    // Title
    this.add.text(width / 2, 50, 'ACME Onboarding Sections', {
      fontSize: '32px',
      color: '#ffffff',
      fontStyle: 'bold'
    }).setOrigin(0.5);

    // Subtitle
    this.add.text(width / 2, 90, 'Hover over a number to hear Coach Blaze explain that section', {
      fontSize: '16px',
      color: '#888888'
    }).setOrigin(0.5);

    // Create sections
    const sectionData = [
      { number: 1, title: 'Core Values' },
      { number: 2, title: 'Work Schedule' },
      { number: 3, title: 'Benefits & Pay' },
      { number: 4, title: 'Growth & Development' },
      { number: 5, title: 'Security & Safety' },
      { number: 6, title: 'Resources & Wrap-up' }
    ];

    // Arrange sections in a 2x3 grid
    const startX = 200;
    const startY = 180;
    const spacingX = 200;
    const spacingY = 100;

    sectionData.forEach((data, index) => {
      const row = Math.floor(index / 2);
      const col = index % 2;
      
      const section: Section = {
        number: data.number,
        title: data.title,
        x: startX + col * spacingX,
        y: startY + row * spacingY
      };

      // Create background rectangle
      section.background = this.add.rectangle(
        section.x, 
        section.y, 
        180, 
        70, 
        0x4CAF50
      );
      section.background.setInteractive({ useHandCursor: true });

      // Create number text
      section.text = this.add.text(
        section.x - 60, 
        section.y, 
        section.number.toString(), 
        {
          fontSize: '36px',
          color: '#ffffff',
          fontStyle: 'bold'
        }
      ).setOrigin(0.5);

      // Create title text
      this.add.text(
        section.x + 20, 
        section.y, 
        section.title, 
        {
          fontSize: '14px',
          color: '#ffffff',
          wordWrap: { width: 100 }
        }
      ).setOrigin(0.5);

      // Add hover effects
      section.background.on('pointerover', () => this.handleHover(section));
      section.background.on('pointerout', () => this.handleOut(section));

      this.sections.push(section);
    });

    // Add back button
    const backButton = this.add.rectangle(width / 2, height - 50, 150, 40, 0x666666);
    const backText = this.add.text(width / 2, height - 50, 'Back to Game', {
      fontSize: '18px',
      color: '#ffffff'
    }).setOrigin(0.5);

    backButton.setInteractive({ useHandCursor: true });
    backButton.on('pointerover', () => backButton.setFillStyle(0x888888));
    backButton.on('pointerout', () => backButton.setFillStyle(0x666666));
    backButton.on('pointerdown', () => this.scene.start('MainScene'));

    // Instructions
    this.add.text(width / 2, height - 100, 'Audio will play automatically on hover', {
      fontSize: '14px',
      color: '#666666'
    }).setOrigin(0.5);
  }

  private async handleHover(section: Section) {
    // Visual feedback
    section.background?.setFillStyle(0x45a049);
    section.text?.setScale(1.2);

    // Play audio for this section using the audio manager
    if (!section.isPlaying) {
      section.isPlaying = true;
      
      try {
        await audioManager.playAudio(`http://localhost:8000/coach_blaze?step=${section.number}`);
        section.isPlaying = false;
      } catch (error) {
        console.error('Error playing audio:', error);
        section.isPlaying = false;
      }
    }
  }

  private handleOut(section: Section) {
    // Reset visual
    section.background?.setFillStyle(0x4CAF50);
    section.text?.setScale(1);

    // Don't stop audio on hover out - let it finish playing
  }

  shutdown() {
    // Stop any playing audio when scene shuts down
    audioManager.stopCurrent();
  }
}