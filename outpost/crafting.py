'''Outpost Crafting Class
Usage:
    crafting.py [--input=<file>]

Options:
    -h --help       Show this screen.
    --input=<file>  [default: data/farm.default]
'''


from docopt import docopt
import pygame
import configparser
import tileset
import sprites
import level
import player


class Crafting(object):
    def do_stuff(self):
        pass


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
    level = level.Level()
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
