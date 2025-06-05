import Phaser from 'phaser';

interface TimeZone {
  x: number;
  width: number;
  type: 'standard' | 'core' | 'flexible';
  color: number;
  label: string;
  points: number;
}

interface CommunicationToken {
  sprite: Phaser.GameObjects.Sprite;
  type: 'slack' | 'email';
  collected: boolean;
}

export default class WorkScheduleScene extends Phaser.Scene {
  private player!: Phaser.Types.Physics.Arcade.SpriteWithDynamicBody;
  private platforms!: Phaser.Physics.Arcade.StaticGroup;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private clockHand!: Phaser.GameObjects.Rectangle;
  private currentTime: number = 9;
  private timeText!: Phaser.GameObjects.Text;
  private scoreText!: Phaser.GameObjects.Text;
  private score: number = 0;
  private timeZones: TimeZone[] = [];
  private obstacles!: Phaser.Physics.Arcade.Group;
  private communicationTokens: CommunicationToken[] = [];
  private hasSlack: boolean = false;
  private hasEmail: boolean = false;
  private flexPortals!: Phaser.Physics.Arcade.StaticGroup;
  private isInFlexMode: boolean = false;
  private coachBubble?: Phaser.GameObjects.Container;

  constructor() {
    super({ key: 'WorkScheduleScene' });
  }

  create() {
    const { width, height } = this.cameras.main;

    // Office background
    this.add.rectangle(0, 0, width, height, 0x2C5282).setOrigin(0);

    // Create time zones
    this.createTimeZones();

    // Create platforms
    this.platforms = this.physics.add.staticGroup();
    
    // Ground
    const ground = this.platforms.create(400, 568, 'ground');
    ground.setScale(800, 64).refreshBody();
    ground.setTint(0x1A365D);

    // Office desks (platforms)
    this.platforms.create(200, 450, 'ground').setScale(150, 20).refreshBody().setTint(0x8B4513);
    this.platforms.create(600, 450, 'ground').setScale(150, 20).refreshBody().setTint(0x8B4513);
    this.platforms.create(400, 350, 'ground').setScale(200, 20).refreshBody().setTint(0x8B4513);
    this.platforms.create(150, 250, 'ground').setScale(100, 20).refreshBody().setTint(0x8B4513);
    this.platforms.create(650, 250, 'ground').setScale(100, 20).refreshBody().setTint(0x8B4513);

    // Create player
    this.player = this.physics.add.sprite(50, 450, 'player');
    this.player.setScale(32, 32);
    this.player.setTint(0x4299E1);
    this.player.setBounce(0.2);
    this.player.setCollideWorldBounds(true);

    // Create clock display
    this.createClock();

    // Create obstacles (being late)
    this.createObstacles();

    // Create communication tokens
    this.createCommunicationTokens();

    // Create flexibility portals
    this.createFlexPortals();

    // Physics
    this.physics.add.collider(this.player, this.platforms);
    this.physics.add.collider(this.obstacles, this.platforms);
    
    // Obstacle collision
    this.physics.add.overlap(this.player, this.obstacles, (player, obstacle) => {
      this.handleLateObstacle(obstacle as Phaser.GameObjects.Sprite);
    });

    // Controls
    this.cursors = this.input.keyboard!.createCursorKeys();

    // HUD
    const playerName = this.registry.get('playerName') || 'Player';
    this.scoreText = this.add.text(10, 10, `${playerName} - Score: 0`, {
      fontSize: '18px',
      color: '#ffffff',
      backgroundColor: '#000000',
      padding: { x: 10, y: 5 }
    });

    // Instructions
    this.showCoachIntro();

    // Start time progression
    this.time.addEvent({
      delay: 2000,
      callback: this.advanceTime,
      callbackScope: this,
      loop: true
    });
  }

  private createTimeZones() {
    // Define time zones
    this.timeZones = [
      { x: 0, width: 150, type: 'standard', color: 0x3B82F6, label: '9-10 AM', points: 10 },
      { x: 150, width: 250, type: 'core', color: 0xFCD34D, label: '10 AM-3 PM\nCore Hours!', points: 20 },
      { x: 400, width: 150, type: 'standard', color: 0x3B82F6, label: '3-5 PM', points: 10 },
      { x: 550, width: 250, type: 'flexible', color: 0x10B981, label: 'Flex Time\nRemote OK!', points: 15 }
    ];

    // Draw time zones
    this.timeZones.forEach(zone => {
      const zoneRect = this.add.rectangle(zone.x, 0, zone.width, 100, zone.color, 0.3).setOrigin(0);
      
      this.add.text(zone.x + zone.width / 2, 50, zone.label, {
        fontSize: '14px',
        color: '#ffffff',
        align: 'center'
      }).setOrigin(0.5);
    });
  }

  private createClock() {
    // Clock face
    const clockX = 400;
    const clockY = 150;
    
    this.add.circle(clockX, clockY, 60, 0xFFFFFF);
    this.add.circle(clockX, clockY, 55, 0x2D3748);
    
    // Clock numbers
    for (let i = 1; i <= 12; i++) {
      const angle = (i * 30 - 90) * Math.PI / 180;
      const x = clockX + Math.cos(angle) * 40;
      const y = clockY + Math.sin(angle) * 40;
      this.add.text(x, y, i.toString(), {
        fontSize: '12px',
        color: '#ffffff'
      }).setOrigin(0.5);
    }

    // Clock hand
    this.clockHand = this.add.rectangle(clockX, clockY, 3, 35, 0xFF0000).setOrigin(0.5, 0.9);
    this.updateClockHand();

    // Time display
    this.timeText = this.add.text(clockX, clockY + 80, this.getTimeString(), {
      fontSize: '20px',
      color: '#ffffff',
      fontStyle: 'bold'
    }).setOrigin(0.5);
  }

  private updateClockHand() {
    const hourAngle = (this.currentTime * 30 - 90) * Math.PI / 180;
    this.clockHand.setRotation(hourAngle + Math.PI / 2);
  }

  private getTimeString(): string {
    const hour = Math.floor(this.currentTime);
    const minutes = Math.round((this.currentTime - hour) * 60);
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour > 12 ? hour - 12 : hour;
    return `${displayHour}:${minutes.toString().padStart(2, '0')} ${period}`;
  }

  private createObstacles() {
    this.obstacles = this.physics.add.group();

    // "Being Late" obstacles
    const obstaclePositions = [
      { x: 300, y: 400 },
      { x: 500, y: 300 },
      { x: 250, y: 200 }
    ];

    obstaclePositions.forEach(pos => {
      const obstacle = this.obstacles.create(pos.x, pos.y, 'obstacle');
      obstacle.setScale(40, 40);
      obstacle.setTint(0xEF4444);
      obstacle.body.setAllowGravity(false);
      
      // Add warning sign
      this.add.text(pos.x, pos.y, '⚠️', {
        fontSize: '24px'
      }).setOrigin(0.5);

      // Floating animation
      this.tweens.add({
        targets: obstacle,
        y: pos.y - 10,
        duration: 1500,
        yoyo: true,
        repeat: -1,
        ease: 'Sine.easeInOut'
      });
    });
  }

  private createCommunicationTokens() {
    // Slack token
    const slackSprite = this.add.sprite(150, 200, 'comm');
    slackSprite.setScale(40, 40);
    slackSprite.setTint(0x4A154B);
    this.add.text(150, 200, '💬', { fontSize: '20px' }).setOrigin(0.5);
    
    // Email token
    const emailSprite = this.add.sprite(650, 200, 'comm');
    emailSprite.setScale(40, 40);
    emailSprite.setTint(0x0078D4);
    this.add.text(650, 200, '📧', { fontSize: '20px' }).setOrigin(0.5);

    this.communicationTokens = [
      { sprite: slackSprite, type: 'slack', collected: false },
      { sprite: emailSprite, type: 'email', collected: false }
    ];
  }

  private createFlexPortals() {
    this.flexPortals = this.physics.add.staticGroup();
    
    // Remote work portal
    const portal1 = this.flexPortals.create(700, 450, 'portal');
    portal1.setScale(60, 80).refreshBody();
    portal1.setTint(0x10B981);
    
    this.add.text(700, 400, '🏠', { fontSize: '24px' }).setOrigin(0.5);
    this.add.text(700, 480, 'Remote\nPortal', {
      fontSize: '12px',
      color: '#ffffff',
      align: 'center'
    }).setOrigin(0.5);

    // Add portal glow effect
    this.tweens.add({
      targets: portal1,
      alpha: 0.6,
      duration: 1000,
      yoyo: true,
      repeat: -1
    });
  }

  private showCoachIntro() {
    const bubble = this.createSpeechBubble(
      "Standard hours are 9-5, but 10-3 is prime time for team sprints!\n" +
      "Grab communication tools and avoid being late!\n" +
      "Try the flex portal for remote work bonus points!",
      100, 50
    );

    this.time.delayedCall(5000, () => bubble.destroy());
  }

  private createSpeechBubble(text: string, x: number, y: number): Phaser.GameObjects.Container {
    const bubble = this.add.graphics();
    const bubbleWidth = 500;
    const bubbleHeight = 100;

    bubble.fillStyle(0xffffff);
    bubble.fillRoundedRect(x, y, bubbleWidth, bubbleHeight, 16);
    bubble.lineStyle(2, 0xFF0000);
    bubble.strokeRoundedRect(x, y, bubbleWidth, bubbleHeight, 16);

    const bubbleText = this.add.text(x + 20, y + 20, text, {
      fontSize: '14px',
      color: '#000000',
      wordWrap: { width: bubbleWidth - 40 }
    });

    return this.add.container(0, 0, [bubble, bubbleText]);
  }

  private advanceTime() {
    this.currentTime += 0.5;
    if (this.currentTime > 17) {
      this.currentTime = 9;
    }
    
    this.updateClockHand();
    this.timeText.setText(this.getTimeString());
    
    // Award points based on current time zone
    this.checkTimeZoneBonus();
  }

  private checkTimeZoneBonus() {
    const playerZone = this.timeZones.find(zone => 
      this.player.x >= zone.x && this.player.x < zone.x + zone.width
    );

    if (playerZone) {
      // Double points during core hours
      const multiplier = playerZone.type === 'core' ? 2 : 1;
      const points = playerZone.points * multiplier;
      
      if (this.isInFlexMode && playerZone.type === 'flexible') {
        this.score += points * 1.5; // Flex bonus
        this.showFloatingText('+' + Math.floor(points * 1.5) + ' Flex!', this.player.x, this.player.y - 50, 0x10B981);
      } else {
        this.score += points;
        this.showFloatingText('+' + points, this.player.x, this.player.y - 50, 0xFFD700);
      }
      
      this.scoreText.setText(`${this.registry.get('playerName')} - Score: ${this.score}`);
    }
  }

  private showFloatingText(text: string, x: number, y: number, color: number) {
    const floatingText = this.add.text(x, y, text, {
      fontSize: '20px',
      color: '#' + color.toString(16),
      fontStyle: 'bold'
    }).setOrigin(0.5);

    this.tweens.add({
      targets: floatingText,
      y: y - 30,
      alpha: 0,
      duration: 1000,
      onComplete: () => floatingText.destroy()
    });
  }

  private handleLateObstacle(obstacle: Phaser.GameObjects.Sprite) {
    if (this.hasSlack || this.hasEmail) {
      // Protected by communication
      obstacle.destroy();
      this.showFloatingText('Communication saves the day!', this.player.x, this.player.y - 50, 0x10B981);
      this.score += 50;
      this.scoreText.setText(`${this.registry.get('playerName')} - Score: ${this.score}`);
      
      // Use up the protection
      if (this.hasSlack) this.hasSlack = false;
      else if (this.hasEmail) this.hasEmail = false;
    } else {
      // Penalty for being late
      this.score -= 20;
      this.scoreText.setText(`${this.registry.get('playerName')} - Score: ${this.score}`);
      this.cameras.main.shake(200, 0.01);
      this.showFloatingText('-20 Late!', this.player.x, this.player.y - 50, 0xEF4444);
      
      // Reset player position
      this.player.setPosition(50, 450);
    }
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

    // Check communication token collection
    this.communicationTokens.forEach(token => {
      if (!token.collected) {
        const distance = Phaser.Math.Distance.Between(
          this.player.x, this.player.y,
          token.sprite.x, token.sprite.y
        );

        if (distance < 40) {
          token.collected = true;
          token.sprite.destroy();
          
          if (token.type === 'slack') {
            this.hasSlack = true;
            this.showFloatingText('Slack collected!', this.player.x, this.player.y - 50, 0x4A154B);
          } else {
            this.hasEmail = true;
            this.showFloatingText('Email collected!', this.player.x, this.player.y - 50, 0x0078D4);
          }
        }
      }
    });

    // Check flex portal
    this.flexPortals.children.entries.forEach((portal: any) => {
      const distance = Phaser.Math.Distance.Between(
        this.player.x, this.player.y,
        portal.x, portal.y
      );

      if (distance < 50 && !this.isInFlexMode) {
        this.isInFlexMode = true;
        this.player.setTint(0x10B981);
        this.showFloatingText('Flex Mode Activated!', this.player.x, this.player.y - 50, 0x10B981);
        
        // Auto-deactivate after 10 seconds
        this.time.delayedCall(10000, () => {
          this.isInFlexMode = false;
          this.player.setTint(0x4299E1);
        });
      }
    });

    // Check for level completion
    if (this.score >= 500) {
      this.completeLevel();
    }
  }

  private completeLevel() {
    // Stop time progression
    this.time.removeAllEvents();

    const completion = this.add.text(400, 300,
      "Great schedule management!\n" +
      "You've mastered work-life balance!\n" +
      "Press SPACE for Benefits Training!",
      {
        fontSize: '24px',
        color: '#ffffff',
        backgroundColor: '#10B981',
        padding: { x: 20, y: 15 },
        align: 'center'
      }
    ).setOrigin(0.5);

    this.input.keyboard?.once('keydown-SPACE', () => {
      this.scene.start('BenefitsScene');
    });
  }
}