import pygame
import tileset
import level
import player


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
        self.sprites = self.load_sprites(level)
        self.main_character = player.Player(pos=(6, 3))

        self.clock = pygame.time.Clock()
        self.load_display(self.screen, self.overlays,
                          self.sprites, self.background)

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
        SPRITE_CACHE = tileset.TileCache(32, 32)
        self.overlays = pygame.sprite.RenderUpdates()
        sprites = pygame.sprite.RenderUpdates()
        # sprites.add(player)
        for pos, tile in self.level.sprites.items():
            sprite = sprites.Sprite(pos, SPRITE_CACHE[tile["sprite"]])
            sprites.add(sprite)
        return sprites

    def load_display(self, screen, overlays, sprites, background):
        screen.blit(background, (0, 0))
        overlays.draw(screen)
        dirty = sprites.draw(screen)
        pygame.display.flip()

    def reload_display(self, screen, overlays, sprites, background):
        sprites.clear(screen, background)
        dirty = sprites.draw(screen)
        overlays.draw(screen)
        pygame.display.update(dirty)


if __name__ == '__main__':
    game = Game()
    game_over = False
    while not game_over:
        game.reload_display(game.screen, game.overlays,
                            game.sprites, game.background)
        game.clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
