# ACME Onboarding Game Design

## Game Concept
An interactive 2D platformer where new employees journey through the "ACME Training Gym" with Coach Blaze as their guide. Each level represents a different section of the onboarding process.

## Game Flow

### Level 0: Welcome Arena - Name Badge Creation
- Player enters the game and meets Coach Blaze (animated sprite)
- Interactive name input screen where player types their name
- Name appears on a badge that follows the player throughout the game
- Coach Blaze gives enthusiastic welcome speech in speech bubble

### Level 1: Core Values Gym - "The Powerhouse Five"
- 5 floating platforms, each representing a core value
- Player must collect 5 power-up items representing:
  - 💡 Innovation (lightbulb)
  - 🤝 Integrity (handshake)
  - ⭐ Excellence (star)
  - 👥 Teamwork (people icon)
  - 🎯 Customer Focus (target)
- Each collected item displays its meaning in a popup
- Background shows gym/training facility theme

### Level 2: Schedule Track - Work Hours & Flexibility
- Side-scrolling level with a clock mechanism
- Player navigates through different time zones:
  - 9-5 standard hours section
  - 10-3 "Core Collaboration" golden zone (bonus points)
  - Flexibility portals that demonstrate remote work options
- Collect communication tokens (Slack/Email icons)
- Obstacles represent being late - must use communication power-ups

### Level 3: Benefits Buffet - Pay & PTO
- Restaurant/cafeteria themed level
- Collect different benefit items:
  - 💰 Paychecks (bi-weekly spawning)
  - 🏖️ PTO tokens (15 to collect)
  - 🏥 Health insurance shield
  - 💼 401k treasure chest
- Info panels explain each benefit when collected
- Bonus room for parental leave information

### Level 4: Skills Gym - Growth & Development
- Training obstacle course with skill-building challenges
- $2000 training budget meter to fill
- Mentorship NPCs that give tips
- Player sets a "skill goal" at checkpoint
- Quarterly review checkpoint system

### Level 5: Team Arena - Conduct & Communication
- Multiplayer-style arena (with NPCs)
- Practice respectful communication mini-games
- 24-hour response challenge (timed sections)
- HR hotline phones placed throughout level
- Zero-tolerance zones clearly marked

### Level 6: Security Fortress - Info Security & Safety
- Stealth/puzzle elements
- Password creation mini-game (strong password builder)
- 2FA checkpoint system
- Report suspicious activity buttons
- Emergency exit mapping challenge
- Health station for sick day policy

### Level 7: Life Events Plaza - Leaves & Civic Duties
- Town square setting
- Information kiosks for:
  - FMLA portal
  - Jury duty courthouse
  - Voting booth (2-hour timer demonstration)
- Optional exploration area

### Level 8: Exit Bridge - Departure Procedures
- Optional tutorial level (can skip)
- Shows proper exit procedures:
  - 2-week notice mailbox
  - Equipment return station
  - PTO payout calculator
- Peaceful bridge setting

### Level 9: Victory Celebration - Resources & Completion
- Final celebration area
- Coach Blaze congratulates player
- Resource center hub with:
  - Handbook library
  - HR contact portal
  - Achievement gallery
- Certificate of completion ceremony

## Game Mechanics

### Core Mechanics:
- **Movement**: Arrow keys or WASD
- **Jump**: Spacebar
- **Interact**: E key
- **Info Panel**: Tab key
- **Pause/Menu**: ESC

### Special Features:
- **Progress Tracker**: Shows completion % for each section
- **Knowledge Checks**: Quick quiz popups between levels
- **Achievement System**: Badges for completing each section
- **Coach Blaze Commentary**: Motivational messages throughout
- **Handbook Access**: Can access employee handbook anytime with H key

### Visual Style:
- Bright, energetic colors matching Coach Blaze's fitness theme
- Corporate gym/training facility aesthetic
- Clean, professional but fun art style
- UI elements styled like fitness trackers/apps

### Audio:
- Upbeat, motivational background music
- Coach Blaze voice clips for key moments
- Sound effects for collectibles and achievements
- Victory fanfare for level completion

## Technical Implementation Notes:
- Use Phaser's scene system for each level
- Save progress to localStorage
- Responsive design for various screen sizes
- Accessibility options (colorblind mode, text size)
- Skip options for users who prefer reading

## Next Steps:
1. Create sprite assets for Coach Blaze and player character
2. Design tilemap for each level
3. Implement core platforming mechanics
4. Add onboarding content integration
5. Create UI/HUD system
6. Implement save/load system
7. Add achievement tracking
8. Polish with animations and effects