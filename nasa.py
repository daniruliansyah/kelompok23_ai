import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BG = (25, 57, 64)
RED = (255, 0, 0)

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI TEORI KELOMPOK 23")

# Class for the player's spaceship
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.all_sprites = pygame.sprite.Group()  # Define all_sprites as an attribute
        self.all_sprites.add(self)

    def update(self):
        # Get the keys pressed
        keystate = pygame.key.get_pressed()
        # Update speed based on keys pressed
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        elif keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        else:
            self.speed_x = 0
        # Update position based on speed
        self.rect.x += self.speed_x
        # Ensure the player stays within the screen boundaries
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, bullets):  # Add bullets as a parameter
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.all_sprites.add(bullet)
        bullets.add(bullet)  # Add bullet to the bullets group

# Class for the enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 3)

    def update(self):
        # Update posisi musuh
        self.rect.y += self.speed_y
        # Jika musuh keluar dari layar, reset posisinya ke atas
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 3)

# Class for the bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        # Update posisi peluru
        self.rect.y += self.speed_y
        # Hapus peluru jika sudah di luar layar
        if self.rect.bottom < 0:
            self.kill()

# Fungsi untuk membuat musuh
def create_enemies(num_enemies):
    enemies = pygame.sprite.Group()
    for _ in range(num_enemies):
        enemy = Enemy()
        enemies.add(enemy)
    return enemies

# Fungsi untuk display teks di layar
def display_text(text, x, y):
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Fungsi utama permainan
def main():
    # Inisialisasi
    clock = pygame.time.Clock()
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    enemies = create_enemies(8)
    bullets = pygame.sprite.Group()  # Define bullets here
    enemies_killed = 0

    # Loop utama permainan
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(bullets)  # Pass bullets group as a parameter to shoot() method

        # Update
        all_sprites.update()
        enemies.update()
        bullets.update()

        # Check for collisions between player and enemies
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            running = False

        # Check for collisions between bullets and enemies
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hits:
                enemies_killed += 1
                bullet.kill()

        # Render
        screen.fill(BG)
        all_sprites.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        display_text("Enemies Killed: {}".format(enemies_killed), SCREEN_WIDTH // 2, 30)

        # Update display
        pygame.display.flip()

        # Batasi kecepatan frame
        clock.tick(60)

    # Tampilkan skor terakhir setelah permainan berakhir
    print("Musuh yang dibunuh: {}".format(enemies_killed))

    pygame.quit()

# Jalankan game
if __name__ == "__main__":
    main()
