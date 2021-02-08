import pygame
import tileset


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, frame):
        super(Sprite, self).__init__()
        SPRITE_CACHE = tileset.TileCache(32, 32)
        images = SPRITE_CACHE.__getitem__('data/tileset.png')
        self.image = pygame.Surface([32, 32])
        self.image = images[frame[0]][frame[1]]
        self.rect = self.image.get_rect()
        self.pos = pos

    def _get_pos(self):
        """Check the current position of the sprite on the map."""
        return (self.rect.midbottom[0]), (self.rect.midbottom[1])

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""
        self.rect.midbottom = pos[0]*32, pos[1]*32
        self.depth = self.rect.midbottom[1]

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""
        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
