import pygame

FPS = 60
WIN_WIDHT = 700
WIN_HEIGHT = 500
window = pygame.display.set_mode((WIN_WIDHT, WIN_HEIGHT))
pygame.display.set_caption('ЛАБИРИНТ!')
clock = pygame.time.Clock()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img_path, x, y, w, h):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, img_path, x, y, w, h, speed_x, speed_y):
        super().__init__(img_path, x, y, w, h)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x + 80 > WIN_WIDHT:
            self.rect.x -= self.speed_x

        if self.rect.y <= 0 or self.rect.y + 80 > WIN_HEIGHT:
            self.rect.y -= self.speed_y

        walls_collided = pygame.sprite.spritecollide(self, walls, False)
        if walls_collided:
            if self.speed_x != 0:
                self.rect.x -= self.speed_x
            if self.speed_y != 0:
                self.rect.y -= self.speed_y

class Enemy(GameSprite):
    def __init__(self,  img_path, x, y, w, h, speed):
        super().__init__(img_path, x, y, w, h)
        self.speed = speed
        self.down = True
    
    def update(self):
        
        if self.down:
            self.rect.y += self.speed
            if self.rect.y + 80 >= WIN_HEIGHT:
                self.down = False
        
        if not self.down:
            self.rect.y -= self.speed
            if self.rect.colliderect(wall2):
                self.down = True



hero = Player('hero.png', 20, 400, 80, 80, 0, 0)
bg = GameSprite('galaxy_2.jpg', 0, 0, 700, 500)
wall1 = GameSprite('platform_h.png', 250, 60, 40, 330)
wall2 = GameSprite('platform_v.png', 250, 60, 330, 40)
final = GameSprite('enemy2.png', 600, 400, 80, 80)
enemy = Enemy('enemy.png', 300, 250, 80, 80, 2)
game_over = GameSprite('game-over_1.png', 0, 0, 700, 500)
win_bg = GameSprite('thumb.jpg', 0, 0, 700, 500)

walls = pygame.sprite.Group()
walls.add(wall1)
walls.add(wall2)


state = 'game'
run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                hero.speed_x = -5
            if e.key == pygame.K_RIGHT:
                hero.speed_x = 5
            if e.key == pygame.K_UP:
                hero.speed_y = -5
            if e.key == pygame.K_DOWN:
                hero.speed_y = 5
        if e.type == pygame.KEYUP:
            if e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                hero.speed_x = 0
                hero.speed_y = 0

    if state == 'game':
        bg.draw()
        walls.draw(window)
        hero.draw()
        enemy.draw()
        final.draw()
        hero.update()
        enemy.update()

        if hero.rect.colliderect(final):
            state = 'win'

        if hero.rect.colliderect(enemy):
            state = 'loose'

    if state == 'win':
        win_bg.draw()

    if state == 'loose':
        game_over.draw()

    clock.tick(FPS)
    pygame.display.update()
