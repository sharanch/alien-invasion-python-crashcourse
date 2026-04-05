# Alien Invasion

A classic space shooter built with Python and Pygame.

## Requirements

- Python 3.8+
- Pygame

## Setup

```bash
# Clone or download the project, then:

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # bash/zsh

# Install dependency
pip install pygame

# Run the game
python alien_invasion.py
```

## Controls

| Key | Action |
|-----|--------|
| `←` `→` | Move ship |
| `Space` | Shoot |
| `R` | Restart / Next level |
| Close window | Quit |

## Features

- Animated aliens with leg movement
- Particle explosion effects
- Scrolling starfield background
- Escalating difficulty per level (speed, rows, cols)
- Lives system with ship flash on hit
- Score and high score tracking

## Project Structure

```
alien-invasion/
├── alien_invasion.py   # entire game in one file
└── README.md
```

## Notes

- The `venv/` folder should be added to `.gitignore` if using git
- All game logic is in a single file — `Ship`, `Alien`, `Bullet`, `Explosion`, `Star`, and `Game` classes
