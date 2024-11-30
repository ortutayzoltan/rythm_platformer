# Rhythm Platformer Game

A dynamic browser-based platformer game that combines rhythm mechanics with classic platforming gameplay. The game features a running character that must jump over and navigate through various obstacles while maintaining synchronization with the background music.

## Game Overview

In this engaging platformer, players control a character that automatically runs through a dynamically generated obstacle course. The character can jump over obstacles or use them as platforms, creating an interesting mix of quick reflexes and strategic planning. The game progressively becomes more challenging as your score increases, offering an engaging experience for players of all skill levels.

## Features

### Core Gameplay Mechanics
- Continuous side-scrolling movement
- Responsive jumping mechanics with platform collision detection
- Progressive difficulty scaling based on score
- Combo system for consecutive successful jumps
- Synchronized background music that loops during gameplay
- Game over state with score display and instant restart option

### Visual Elements
- Animated character sprite with running animation
- Three distinct types of platforms with unique visual styles:
  - Narrow platforms (20-35 pixels wide) - Higher risk but lower height
  - Normal platforms (40-80 pixels wide) - Balanced difficulty
  - Extra wide platforms (120-200 pixels wide) - Safer but potentially taller
- Dynamic background effects synchronized with the music beat
- Clear visual feedback for scoring and game states

### Technical Implementation
- Built using p5.js for graphics and game logic
- Implements sprite-based animation system
- Features physics-based jumping mechanics
- Includes sound integration with p5.sound
- Responsive canvas that adapts to the game container

## Project Structure
```
./
├── index.html           # Main game file with HTML, CSS, and JavaScript
├── audio.mp3           # Background music file
└── images/            # Directory containing game sprites
    ├── player.png     # Character spritesheet (128x32 pixels, 4 frames)
    ├── narrow.png     # Narrow platform sprite
    ├── normal.png     # Normal platform sprite
    └── wide.png       # Wide platform sprite
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd rhythm-platformer
   ```

2. Start a local web server. You can use any of these methods:

   Using Python 3:
   ```bash
   python -m http.server 8000
   ```

   Using Node.js (after installing http-server):
   ```bash
   npx http-server
   ```

   Using Visual Studio Code:
   - Install the "Live Server" extension
   - Right-click index.html
   - Select "Open with Live Server"

3. Open your browser and navigate to:
   - For Python: `http://localhost:8000`
   - For Node.js: `http://localhost:8080`
   - For VS Code Live Server: It will open automatically

## How to Play

1. The game starts automatically when loaded
2. Press SPACEBAR to make your character jump
3. Time your jumps to:
   - Avoid obstacles by jumping over them
   - Land on platforms to use them as stepping stones
   - Build up your combo for a higher score
4. If you hit an obstacle from the side, the game ends
5. Press SPACEBAR to restart after game over

## Game Mechanics in Detail

### Platform Types and Strategy
The game features three types of platforms, each requiring different strategies:
- Narrow Platforms: Require precise timing but are generally shorter
- Normal Platforms: Provide a balanced challenge
- Extra Wide Platforms: Offer safe landing zones but can be taller

### Difficulty Progression
The game becomes progressively more challenging through several mechanisms:
- Obstacle speed increases with score
- Higher chance of narrow platforms appearing
- Platform heights adjust based on type and current score
- Maximum jump height is calculated based on physics for fair challenge

### Scoring System
- Base points are awarded for clearing obstacles
- Consecutive successful jumps build up a combo multiplier
- Higher risk platforms (narrow) appear more frequently at higher scores

## Development and Customization

### Sprite Requirements
- Player sprite: 128x32 pixel spritesheet containing 4 frames of animation
- Platform sprites: Individual images for each platform type
- All sprites should be PNG format for transparency support

### Adding Custom Music
Replace `audio.mp3` with your own audio file. The game will automatically:
- Loop the music during gameplay
- Stop when the player dies
- Restart when the game is reset

### Modifying Difficulty
You can adjust these variables to customize the game's difficulty:
- Initial platform speed: `this.speed = 7`
- Speed increase rate: `score / 500`
- Maximum speed increase: `maxSpeedIncrease = 5`
- Platform spawn rates and dimensions in the Obstacle constructor

## Technical Requirements

- Modern web browser with JavaScript enabled
- Browser support for:
  - ES6+ JavaScript
  - HTML5 Canvas
  - Web Audio API
- Local web server for development

## Credits

This game was built using:
- [p5.js](https://p5js.org/) for rendering and game logic
- [p5.sound](https://p5js.org/reference/#/libraries/p5.sound) for audio functionality

## License

[Add your chosen license here]

