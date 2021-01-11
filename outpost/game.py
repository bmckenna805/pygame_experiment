import configparser
import pygame
import tileset
import sprites
import level

class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), frames=None):
        print('do stuff')

    def __load__(self):
        print('do stuff')

    def __save__(self):
        print('do stuff')


if __name__ == '__main__':
    screen = pygame.display.set_mode((680, 480))

    MAP_TILE_WIDTH = 32
    MAP_TILE_HEIGHT = 32
    MAP_CACHE = tileset.TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)

    level = Level()
    level.load_file('data/map.default')

    SPRITE_CACHE = tileset.TileCache(32, 32)
    overlays = pygame.sprite.RenderUpdates()
    sprites = pygame.sprite.RenderUpdates()
    for pos, tile in level.sprites.items():
        sprite = sprites.Sprite(pos, SPRITE_CACHE[tile["sprite"]])
        sprites.add(sprite)

    clock = pygame.time.Clock()

    background, overlay_dict = level.render()
    for (x, y), image in overlay_dict.items():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    dirty = sprites.draw(screen)
    pygame.display.flip()

    game_over = False
    while not game_over:

        # XXX draw all the objects here

        sprites.clear(screen, background)
        dirty = sprites.draw(screen)
        overlays.draw(screen)
        pygame.display.update(dirty)
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key


