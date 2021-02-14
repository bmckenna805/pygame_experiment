# Pygame Experimentation

A simple game project to create a 2D top down RPG style game.  I started out following a guide but found it was incomplete, no longer had a working link to source code, and was also written for python 2.  I updated examples for python 3 initially and did some experimentation with the configurations and map drawing.

![sample level](./docs/outpost.png?raw=true)

# Original Tutorial

[Tutorial](https://qq.readthedocs.io/en/latest/)

# Tileset

I included a [tileset](https://tazmoe.itch.io/sci-fi-rougelike) that is free on itch.io because of the original for the tutorial being unavailable.  I plan to eventually replace with a homemade tileset.

# Current Classes
1.  tileset.py - provides a basic class for loading tilesets.  It also, when run by itself, will load a tileset and display to screen broken into individual tiles.
2.  level.py - provides a basic class for loading a level.  It also, when run by itself, will load a level and display it staticly.
3.  sprite.py - provides a basic class for loading sprites.
4.  player.py - provides a basic class for the main player character
5.  game.py - the game class, which binds all the classes together into a playable game loop

# Level configuration files

* map - text based representation of the map
* tileset - defines the tileset to use for the level build
* tile translation definitions - translate the text to unique tiles
  * name - can be used to define how tiles are interpreted in other classes
  * tile - defines which tile to use from tileset 
  * wall - if true, marks the tile as a wall which makes it an overlay
  * block - if true, blocks movement
  * spawn - if true, is the player spawn location
  * sprite - if true, is a sprite and gets added to the list of sprites loaded

# Todo

1. make a new tileset that isn't someone else's intellectual property
2. sprite tiles for : player character, interacterables, and enemies
3. Update level loader to load a level file supplied at launch
4. Update tileset loader to load a tileset supplied at launch
5. Implement a status box in game screen
6. Design more levels, add in transitioning between maps
7. If designing by hand is a pain, design a level designing tool (big project)
