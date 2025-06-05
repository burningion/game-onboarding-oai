import Phaser from 'phaser';
import PreloadScene from './scenes/PreloadScene';
import MenuScene from './scenes/MenuScene';
import WelcomeScene from './scenes/WelcomeScene';
import CoreValuesScene from './scenes/CoreValuesScene';
import WorkScheduleScene from './scenes/WorkScheduleScene';
import MainScene from './scenes/MainScene';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  parent: 'phaser-game',
  width: 800,
  height: 600,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 300 },
      debug: false
    }
  },
  scene: [PreloadScene, MenuScene, WelcomeScene, CoreValuesScene, WorkScheduleScene, MainScene]
};

export default config;