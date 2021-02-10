import pygame
import tileset
import level
import sprites
import player as pc


class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.screen = pygame.display.set_mode((680, 480))

        self.MAP_TILE_WIDTH = 32
        self.MAP_TILE_HEIGHT = 32
        self.MAP_CACHE = tileset.TileCache(self.MAP_TILE_WIDTH,
                                           self.MAP_TILE_HEIGHT)

        # new game
        self.level = level.Level()
        self.level.load_file('data/map.default')
        self.overlays, self.background = self.load_map()
        self.block_list, self.all_sprites_list, self.player = self.load_sprites(level)

        self.clock = pygame.time.Clock()
        self.load_display(self.screen, self.overlays,
                          self.all_sprites_list, self.background)

    def __load__(self):
        print('do stuff')

    def __save__(self):
        print('do stuff')

    def load_map(self):
        background, overlay_dict = self.level.render(self.MAP_CACHE,
                                                     self.MAP_TILE_HEIGHT,
                                                     self.MAP_TILE_WIDTH)
        overlays = pygame.sprite.RenderUpdates()
        for (x, y), image in overlay_dict.items():
            overlay = pygame.sprite.Sprite(overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
        return overlays, background

    def load_sprites(self, level):
        # load sprites
        self.overlays = pygame.sprite.RenderUpdates()
        # create sprite groups
        block_list = pygame.sprite.Group()
        all_sprites_list = pygame.sprite.Group()
        # get sprites
        for pos, tile in self.level.sprites.items():
            tile = int(tile[0]), int(tile[1])
            thing = sprites.Sprite(pos, tile)
            block_list.add(thing)
            all_sprites_list.add(thing)
        # get player sprite
        tile = [self.level.player['tile'][0], self.level.player['tile'][1]]
        tile = int(tile[0]), int(tile[1])
        pos = (self.level.player['pos'][0], self.level.player['pos'][1])
        pos = int(pos[0]), int(pos[1])
        player = pc.Player(pos, tile)
        all_sprites_list.add(player)
        # return sprite groups and player
        return block_list, all_sprites_list, player

    def load_display(self, screen, overlays, all_sprites_list, background):
        # render background
        screen.blit(background, (0, 0))
        # render sprite layers
        all_sprites_list.draw(screen)
        overlays.draw(screen)
        pygame.display.flip()

    def reload_display(self, screen, overlays, all_sprites_list, background):
        all_sprites_list.clear(screen, background)
        all_sprites_list.draw(screen)
        overlays.draw(screen)


if __name__ == '__main__':
    game = Game()
    game_over = False
    while not game_over:
        game.reload_display(game.screen, game.overlays,
                            game.all_sprites_list, game.background)
        game.clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
