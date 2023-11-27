'''Outpost Tileset Cache
Usage:
    tileset.py [--input=<file>]

Options:
    -h --help       Show this screen.
    --input=<file>  [default: data/tileset.bmp]
'''

import pygame
import pygame.locals
from docopt import docopt


class TileCache:

    """Load the tilesets lazily into global cache"""
    def __init__(self,  width=32, height=None):
        self.width = width
        self.height = height or width
        self.cache = {}

    def __getitem__(self, filename):
        """Return a table of tiles, load it from disk if needed."""
        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width,
                                               self.height)
            self.cache[key] = tile_table
            return tile_table

    def _load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles."""
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, int(image_width/width)):
            line = []
            tile_table.append(line)
            for tile_y in range(0, int(image_height/height)):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table


if __name__ == '__main__':
    '''Load default tileset and display it broken into tiles'''
    MAP_TILE_WIDTH = 32
    MAP_TILE_HEIGHT = 32

    # load docopt
    arguments = docopt(__doc__)
    print(arguments)

    # Set up pygame screen
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    screen.fill((255, 255, 255))

    # Create tileset cache
    MAP_CACHE = TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)
    table = MAP_CACHE.__getitem__(arguments['--input'])

    # Display tileset to the pygame screen
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile, (x*40, y*40))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
