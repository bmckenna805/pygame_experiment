import pygame
import sprites.tileset as tileset
import levels.level as level
import sprites.sprites as sprites
import sprites.player as pc


class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.screen = pygame.display.set_mode((680, 480))

        # set up tileset
        self.MAP_TILE_WIDTH = 32
        self.MAP_TILE_HEIGHT = 32
        self.MAP_CACHE = tileset.TileCache(self.MAP_TILE_WIDTH,
                                           self.MAP_TILE_HEIGHT)

        # new game
        self.level = level.Level()
        self.level.load_file('levels/data/map.default')
        self.load_map()
        self.load_sprites()

        # start game clock
        self.clock = pygame.time.Clock()

        # display everything
        self.load_display()

    def __load__(self):
        print('load game from a file')

    def __save__(self):
        print('save a game to a file')

    def load_map(self):
        # render the level
        self.background, overlay_dict = self.level.render(self.MAP_CACHE,
                                                          self.MAP_TILE_HEIGHT,
                                                          self.MAP_TILE_WIDTH)
        # render overlays
        self.overlays = pygame.sprite.RenderUpdates()
        for (x, y), image in overlay_dict.items():
            overlay = pygame.sprite.Sprite(self.overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)

    def load_sprites(self):
        # load sprites
        self.overlays = pygame.sprite.RenderUpdates()
        # create sprite groups
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        # get sprites
        for pos, tile in self.level.sprites.items():
            tile = int(tile[0]), int(tile[1])
            thing = sprites.Sprite(pos, tile)
            self.block_list.add(thing)
            self.all_sprites_list.add(thing)
        # get player sprite
        tile = [self.level.player['tile'][0], self.level.player['tile'][1]]
        tile = int(tile[0]), int(tile[1])
        pos = (self.level.player['pos'][0], self.level.player['pos'][1])
        pos = int(pos[0]), int(pos[1])
        self.player = pc.Player(pos, tile)
        self.all_sprites_list.add(self.player)

    def load_display(self):
        # render background
        self.screen.blit(self.background, (0, 0))
        self.all_sprites_list.draw(self.screen)
        self.overlays.draw(self.screen)
        # flip display to render sprites
        pygame.display.flip()

    def reload_display(self):
        self.all_sprites_list.clear(self.screen, self.background)
        self.all_sprites_list.draw(self.screen)
        self.overlays.draw(self.screen)
        # flip display to render updates
        pygame.display.flip()
