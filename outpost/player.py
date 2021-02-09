import pygame
import tileset


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, frame):
        super(Player, self).__init__()
        SPRITE_CACHE = tileset.TileCache(32, 32)
        images = SPRITE_CACHE.__getitem__('data/tileset.png')
        self.image = pygame.Surface([32, 32])
        self.image = images[frame[0]][frame[1]]
        self.rect = self.image.get_rect()
        self.pos = pos
        self._set_pos(pos)
        self.hp = 100
        self.name = 'fred johnson'
        self.cash = 10

    def _get_pos(self):
        """Check the current position of the sprite on the map."""
        return (self.rect.topleft[0]/32), (self.rect.topleft[1]/32)

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""
        self.rect.topleft = (pos[0]*32), (pos[1]*32)
        self.depth = self.rect.midbottom[1]

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""
        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
