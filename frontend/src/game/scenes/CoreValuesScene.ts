import Phaser from 'phaser';

interface ValueItem {
  x: number;
  y: number;
  icon: string;
  name: string;
  description: string;
  collected: boolean;
  sprite?: Phaser.GameObjects.Sprite;
}

export default class CoreValuesScene extends Phaser.Scene {
  private player!: Phaser.Types.Physics.Arcade.SpriteWithDynamicBody;
  private platforms!: Phaser.Physics.Arcade.StaticGroup;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private valueItems: ValueItem[] = [];
  private collectedCount: number = 0;
  private hudText!: Phaser.GameObjects.Text;
  private interactKey!: Phaser.Input.Keyboard.Key;

  constructor() {
    super({ key: 'CoreValuesScene' });
  }

  create() {
    const { width, height } = this.cameras.main;

    // Gym background
    this.add.rectangle(0, 0, width, height, 0x4A5568).setOrigin(0);

    // Create platforms
    this.platforms = this.physics.add.staticGroup();
    
    // Ground
    const ground = this.platforms.create(400, 568, 'ground');
    ground.setScale(800, 64).refreshBody();
    ground.setTint(0x2D3748);

    // Floating platforms for values
    this.platforms.create(150, 400, 'ground').setScale(120, 20).refreshBody().setTint(0x2D3748);
    this.platforms.create(650, 400, 'ground').setScale(120, 20).refreshBody().setTint(0x2D3748);
    this.platforms.create(400, 300, 'ground').setScale(120, 20).refreshBody().setTint(0x2D3748);
    this.platforms.create(250, 200, 'ground').setScale(120, 20).refreshBody().setTint(0x2D3748);
    this.platforms.create(550, 200, 'ground').setScale(120, 20).refreshBody().setTint(0x2D3748);

    // Create player
    this.player = this.physics.add.sprite(100, 450, 'player');
    this.player.setScale(32, 32);
    this.player.setTint(0x4299E1);
    this.player.setBounce(0.2);
    this.player.setCollideWorldBounds(true);

    // Player physics
    this.physics.add.collider(this.player, this.platforms);

    // Create value items
    this.createValueItems();

    // Controls
    this.cursors = this.input.keyboard!.createCursorKeys();
    this.interactKey = this.input.keyboard!.addKey('E');

    // HUD
    const playerName = this.registry.get('playerName') || 'Player';
    this.hudText = this.add.text(10, 10, `${playerName} - Core Values: 0/5`, {
      fontSize: '18px',
      color: '#ffffff',
      backgroundColor: '#000000',
      padding: { x: 10, y: 5 }
    });

    // Instructions
    this.add.text(width / 2, 50, 'Collect all 5 Core Values!', {
      fontSize: '24px',
      color: '#FFD700',
      fontStyle: 'bold'
    }).setOrigin(0.5);

    // Coach Blaze hint
    this.showCoachHint();
  }

  private createValueItems() {
    const values = [
      { x: 150, y: 350, icon: '💡', name: 'Innovation', description: 'Think outside the box!' },
      { x: 650, y: 350, icon: '🤝', name: 'Integrity', description: 'Always do the right thing!' },
      { x: 400, y: 250, icon: '⭐', name: 'Excellence', description: 'Strive for the best!' },
      { x: 250, y: 150, icon: '👥', name: 'Teamwork', description: 'Together we achieve more!' },
      { x: 550, y: 150, icon: '🎯', name: 'Customer Focus', description: 'Customers come first!' }
    ];

    values.forEach(value => {
      const item: ValueItem = {
        ...value,
        collected: false
      };

      // Create visual representation
      const sprite = this.add.sprite(value.x, value.y, 'value');
      sprite.setScale(40, 40);
      sprite.setTint(0xFFD700);
      
      // Add floating animation
      this.tweens.add({
        targets: sprite,
        y: value.y - 10,
        duration: 1000,
        yoyo: true,
        repeat: -1,
        ease: 'Sine.easeInOut'
      });

      // Add icon text
      this.add.text(value.x, value.y, value.icon, {
        fontSize: '24px'
      }).setOrigin(0.5);

      item.sprite = sprite;
      this.valueItems.push(item);
    });
  }

  private showCoachHint() {
    // Add Coach Blaze in corner
    const coachSprite = this.add.sprite(100, 100, 'coach');
    if (this.textures.get('coach').source[0].width > 1) {
      coachSprite.setScale(0.15);
    } else {
      coachSprite.setScale(60, 80);
      coachSprite.setTint(0xFF0000);
    }
    
    const hint = this.add.text(400, 100, 
      "Let's warm up with our core muscles—ACME's five values!\nThink of these as your daily reps for success!",
      {
        fontSize: '16px',
        color: '#ffffff',
        backgroundColor: '#FF0000',
        padding: { x: 15, y: 10 },
        align: 'center'
      }
    ).setOrigin(0.5);

    // Remove hint and coach after 5 seconds
    this.time.delayedCall(5000, () => {
      hint.destroy();
      coachSprite.destroy();
    });
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

    // Check for value collection
    this.valueItems.forEach(item => {
      if (!item.collected && item.sprite) {
        const distance = Phaser.Math.Distance.Between(
          this.player.x, this.player.y,
          item.x, item.y
        );

        if (distance < 50) {
          // Show "Press E" prompt
          if (!item.sprite.getData('promptShown')) {
            const prompt = this.add.text(item.x, item.y - 50, 'Press E', {
              fontSize: '14px',
              color: '#ffffff',
              backgroundColor: '#000000',
              padding: { x: 5, y: 2 }
            }).setOrigin(0.5);
            
            item.sprite.setData('promptShown', true);
            item.sprite.setData('prompt', prompt);
          }

          // Collect on E press
          if (Phaser.Input.Keyboard.JustDown(this.interactKey)) {
            this.collectValue(item);
          }
        } else {
          // Remove prompt when far away
          const prompt = item.sprite.getData('prompt');
          if (prompt) {
            prompt.destroy();
            item.sprite.setData('promptShown', false);
          }
        }
      }
    });
  }

  private collectValue(item: ValueItem) {
    item.collected = true;
    item.sprite?.destroy();
    
    const prompt = item.sprite?.getData('prompt');
    if (prompt) prompt.destroy();

    this.collectedCount++;
    this.hudText.setText(`${this.registry.get('playerName')} - Core Values: ${this.collectedCount}/5`);

    // Show value description
    const popup = this.add.text(400, 300, 
      `${item.icon} ${item.name}\n${item.description}`,
      {
        fontSize: '24px',
        color: '#ffffff',
        backgroundColor: '#000000',
        padding: { x: 20, y: 15 },
        align: 'center'
      }
    ).setOrigin(0.5);

    this.time.delayedCall(2000, () => popup.destroy());

    // Check if all collected
    if (this.collectedCount === 5) {
      this.time.delayedCall(2500, () => {
        this.showCompletionMessage();
      });
    }
  }

  private showCompletionMessage() {
    const message = this.add.text(400, 300,
      "Excellent work! You've mastered the Powerhouse Five!\nPress SPACE to continue to Work Schedule Training!",
      {
        fontSize: '20px',
        color: '#ffffff',
        backgroundColor: '#4CAF50',
        padding: { x: 20, y: 15 },
        align: 'center'
      }
    ).setOrigin(0.5);

    this.input.keyboard?.once('keydown-SPACE', () => {
      this.scene.start('WorkScheduleScene');
    });
  }
}