# Jungle Chess

**Jungle Chess** is a network board game for two players. It is written in Python 3 using [Pygame](https://www.pygame.org) library.

## Screenshots

![Start Menu](https://github.com/barbanevosa/jungle-chess/blob/main/screenshots/screenshot_start_menu.png?raw=true "Start Menu")

![Gameplay](https://github.com/barbanevosa/jungle-chess/blob/main/screenshots/screenshot_gameplay.png?raw=true "Gameplay")

## Overview

**Jungle Chess** (aka **Dou Shou Qi**) is a modern Chinese strategy board game for two players.

The Jungle gameboard represents a jungle terrain with *dens*, *traps* "set" around dens, and *rivers*. Each player controls eight game pieces representing different animals of various rank. Stronger-ranked animals can capture ("eat") animals of weaker or equal rank. The player who is first to maneuver any one of their pieces into the opponent's den wins the game. An alternative way to win is to capture all the opponent's pieces.

Please review the rules and detailed description of the Dou Shou Qi on [Wikipedia](https://en.wikipedia.org/wiki/Jungle_(board_game)).

## Getting Started

### Installation
`pip install jungle-chess`

### Running
`jungle-chess`

or

`python -m jungle-chess`

### Playing

* To start a game server choose "Start new game" in the main menu.
* To connect to the game server choose "Connect to game server" and enter the server IP address or hostname.
* Total game time is 15 minutes per player, plus 5 second per-move free time.
* Time constants can be changed in `constants.py` file.
* You can surrender any time by clicking on the white flag button and confirming you intention by pressing `Y` after that.

## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

## Credits

* [Vecteezy](https://www.vecteezy.com/free-vector/svg) for SVG vectors
* [Pablo Pizzaro R.](https://ppizarror.com/) for [Pygame-menu](https://github.com/ppizarror/pygame-menu) library
* [Alex-Productions](https://onsound.eu) for *Chinese New Year Is Coming* music theme
