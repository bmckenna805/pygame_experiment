'''Outpost Level Loader
Usage:
    level.py [--input=<file>]

Options:
    -h --help       Show this screen.
    --input=<file>  [default: data/map.default]
'''


from docopt import docopt
import pygame
import configparser
import sprites.tileset as tileset
import sprites.sprites as sprites
import sprites.player as player


class Level(object):
    def load_file(self, filename="levels/data/map.default"):
        # empty lists and dicts to represent level
        self.map = []
        self.key = {}
        self.sprites = {}
        self.player = {}

        # parse the level config from file
        parser = configparser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc

        # set map width, height
        self.width = len(self.map[0])
        self.height = len(self.map)

        # load sprites from map file
        for y, line in enumerate(self.map):
            for x, c in enumerate(line):
                if not self.is_wall(x, y) and 'sprite' in self.key[c]:
                    self.sprites[(x, y)] = self.key[c]['tile'].split(',')
                if not self.is_wall(x, y) and 'spawn' in self.key[c]:
                    self.player['tile'] = self.key[c]['tile'].split(',')
                    self.player['pos'] = (x, y)

    def get_tile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes',
                         'True', 'Yes', '1', 'on', 'On')

    def is_wall(self, x, y):
        """Is there a wall?"""

        return self.get_bool(x, y, 'wall')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')

    def render(self, MAP_CACHE, MAP_TILE_HEIGHT, MAP_TILE_WIDTH):
        wall = self.is_wall

        # load tileset
        tiles = MAP_CACHE.__getitem__(self.tileset)
        image = pygame.Surface((self.width*MAP_TILE_WIDTH,
                                self.height*MAP_TILE_HEIGHT))

        # Render map.  Todo: add in check for overlay
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                # if wall, set to that map's tile
                if wall(map_x, map_y):
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to wall tile
                        tile = 6, 0

                # Commented out: overlay for vision obscuring tiles

                # Add overlays if the wall may be obscuring something
                # if not wall(map_x, map_y-1):
                #     if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                #         tile = 1, 0
                #     elif wall(map_x+1, map_y):
                #         tile = 0, 0
                #     elif wall(map_x-1, map_y):
                #         tile = 2, 0
                #     else:
                #         tile = 3, 0
                #     overlays[(map_x, map_y)] = tiles[tile[0]][tile[1]]
                else:
                    try:
                        if 'spawn' not in self.key[c] and 'sprite' not in self.key[c]:
                            tile = self.key[c]['tile'].split(',')
                            tile = int(tile[0]), int(tile[1])
                        else:
                            tile = 3, 0
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 3, 0
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
        return image, overlays


if __name__ == "__main__":
    '''Load default map and display to screen'''

    # load docopt
    arguments = docopt(__doc__)

    # set up screen
    screen = pygame.display.set_mode((680, 480))

    # import tileset
    MAP_TILE_WIDTH = 32
    MAP_TILE_HEIGHT = 32
    MAP_CACHE = tileset.TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)

    # load level
    level = Level()
    level.load_file(arguments['--input'])

    # load sprites
    overlays = pygame.sprite.RenderUpdates()
    things = pygame.sprite.RenderUpdates()

    block_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()

    for pos, tile in level.sprites.items():
        tile = int(tile[0]), int(tile[1])
        thing = sprites.Sprite(pos, tile)
        block_list.add(thing)
        all_sprites_list.add(thing)

    # set up player
    tile = [level.player['tile'][0], level.player['tile'][1]]
    tile = int(tile[0]), int(tile[1])
    pos = (level.player['pos'][0], level.player['pos'][1])
    pos = int(pos[0]), int(pos[1])
    player = player.Player(pos, tile)
    all_sprites_list.add(player)

    # set up game clock
    clock = pygame.time.Clock()

    # render level
    background, overlay_dict = level.render(MAP_CACHE,
                                            MAP_TILE_HEIGHT,
                                            MAP_TILE_WIDTH)

    # render sprite overlay
    for (x, y), image in overlay_dict.items():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)

    # render background
    screen.blit(background, (0, 0))

    # render sprite overlay
    all_sprites_list.draw(screen)
    overlays.draw(screen)
    pygame.display.flip()

    # enter basic game loop
    game_over = False
    while not game_over:

        # redraw sprites
        all_sprites_list.clear(screen, background)
        all_sprites_list.draw(screen)
        overlays.draw(screen)

        # tick clock away
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
