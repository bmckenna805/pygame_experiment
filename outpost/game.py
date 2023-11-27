import pygame
import core.game as core


if __name__ == '__main__':
    game = core.Game()
    game_over = False
    while not game_over:
        game.reload_display(game.screen, game.overlays,
                            game.all_sprites_list, game.background)
        game.clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    position = game.player._get_pos()
                    if not game.level.is_blocking(int(position[0]), int(position[1]) - 1):
                        game.player.move(0, -32)
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    position = game.player._get_pos()
                    if not game.level.is_blocking(int(position[0]) - 1, int(position[1])):
                        game.player.move(-32, 0)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    position = game.player._get_pos()
                    if not game.level.is_blocking(int(position[0]), int(position[1]) + 1):
                        game.player.move(0, 32)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    position = game.player._get_pos()
                    if not game.level.is_blocking(int(position[0]) + 1, int(position[1])):
                        game.player.move(32, 0)
                if event.key == ord('q'):
                    game_over = True
