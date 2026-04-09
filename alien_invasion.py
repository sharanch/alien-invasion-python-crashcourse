import pygame
import sys
import random

# --- Init ---
pygame.init()

SCREEN_W, SCREEN_H = 1920, 1080
FPS = 60

# Colors
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
GREEN       = (0, 255, 100)
RED         = (255, 50, 50)
CYAN        = (0, 220, 255)
YELLOW      = (255, 230, 0)
DARK_GRAY   = (20, 20, 30)
PURPLE      = (150, 0, 255)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Alien Invasion")
clock = pygame.time.Clock()

font_large  = pygame.font.SysFont("monospace", 48, bold=True)
font_medium = pygame.font.SysFont("monospace", 28)
font_small  = pygame.font.SysFont("monospace", 20)


class Ship:
    def __init__(self):
        self.w, self.h = 50, 40
        self.x = SCREEN_W // 2 - self.w // 2
        self.y = SCREEN_H - self.h - 20
        self.speed = 6
        self.moving_left  = False
        self.moving_right = False
        self.color = GREEN
        self.lives = 3

    def update(self):
        if self.moving_left and self.x > 0:
            self.x -= self.speed
        if self.moving_right and self.x < SCREEN_W - self.w:
            self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x + 10, self.y + 15, 30, 25), border_radius=4)
        pygame.draw.polygon(surface, CYAN, [
            (self.x + 25, self.y),
            (self.x + 15, self.y + 18),
            (self.x + 35, self.y + 18),
        ])
        pygame.draw.polygon(surface, self.color, [
            (self.x,      self.y + 40),
            (self.x + 15, self.y + 20),
            (self.x + 15, self.y + 40),
        ])
        pygame.draw.polygon(surface, self.color, [
            (self.x + 50, self.y + 40),
            (self.x + 35, self.y + 20),
            (self.x + 35, self.y + 40),
        ])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def center(self):
        return self.x + self.w // 2


class Bullet:
    def __init__(self, x, y, color=YELLOW, speed=-10, w=4, h=14):
        self.rect = pygame.Rect(x - w // 2, y, w, h)
        self.color = color
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=2)

    def off_screen(self):
        return self.rect.y < 0 or self.rect.y > SCREEN_H


class Alien:
    SIZE = 36

    def __init__(self, x, y, row):
        self.x = x
        self.y = y
        self.row = row
        self.alive = True
        self.anim = 0

    def color(self):
        colors = [RED, PURPLE, CYAN, YELLOW]
        return colors[self.row % len(colors)]

    def draw(self, surface):
        if not self.alive:
            return
        self.anim = (self.anim + 1) % 60
        c = self.color()
        s = self.SIZE
        x, y = int(self.x), int(self.y)
        pygame.draw.ellipse(surface, c, (x + 4, y + 10, s - 8, s - 12))
        pygame.draw.ellipse(surface, c, (x + 6, y, s - 12, 20))
        eye_y = y + 6
        pygame.draw.circle(surface, BLACK, (x + 11, eye_y), 4)
        pygame.draw.circle(surface, BLACK, (x + s - 11, eye_y), 4)
        pygame.draw.circle(surface, WHITE, (x + 11, eye_y), 2)
        pygame.draw.circle(surface, WHITE, (x + s - 11, eye_y), 2)
        leg_offset = 4 if (self.anim // 10) % 2 == 0 else -4
        pygame.draw.line(surface, c, (x + 8,  y + s - 10), (x + 4,  y + s + leg_offset), 2)
        pygame.draw.line(surface, c, (x + 16, y + s - 10), (x + 14, y + s + leg_offset), 2)
        pygame.draw.line(surface, c, (x + s - 8,  y + s - 10), (x + s - 4,  y + s + leg_offset), 2)
        pygame.draw.line(surface, c, (x + s - 16, y + s - 10), (x + s - 14, y + s + leg_offset), 2)
        pygame.draw.line(surface, c, (x + 10, y), (x + 6,  y - 8), 2)
        pygame.draw.line(surface, c, (x + s - 10, y), (x + s - 6, y - 8), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.SIZE, self.SIZE)


class Explosion:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.particles = [
            [random.uniform(-4, 4), random.uniform(-4, 4), random.randint(3, 7)]
            for _ in range(12)
        ]
        self.life = 20

    def update(self):
        self.life -= 1
        for p in self.particles:
            p[0] *= 1.05
            p[1] *= 1.05
            p[2] = max(1, p[2] - 0.3)

    def draw(self, surface):
        for i, p in enumerate(self.particles):
            px = int(self.x + p[0] * (20 - self.life))
            py = int(self.y + p[1] * (20 - self.life))
            r  = int(p[2])
            col = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.circle(surface, col, (px, py), r)

    def dead(self):
        return self.life <= 0


class Star:
    def __init__(self):
        self.reset(random.randint(0, SCREEN_H))

    def reset(self, y=0):
        self.x = random.randint(0, SCREEN_W)
        self.y = y
        self.speed = random.uniform(0.3, 1.2)
        self.size  = random.randint(1, 3)
        self.bright = random.randint(100, 255)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_H:
            self.reset()

    def draw(self, surface):
        c = (self.bright,) * 3
        pygame.draw.circle(surface, c, (int(self.x), int(self.y)), self.size)


def create_fleet(level=1):
    aliens = []
    rows    = min(4 + level, 7)
    cols    = min(10 + level, 14)
    x_gap   = (SCREEN_W - cols * 50) // (cols + 1)
    y_start = 80
    for row in range(rows):
        for col in range(cols):
            x = x_gap + col * (36 + x_gap)
            y = y_start + row * 55
            aliens.append(Alien(x, y, row))
    return aliens


class Game:
    def __init__(self):
        self.reset()
        self.high_score = 0

    def reset(self, level=1):
        self.ship       = Ship()
        self.bullets    = []
        self.alien_bullets = []
        self.aliens     = create_fleet(level)
        self.explosions = []
        self.stars      = [Star() for _ in range(120)]
        self.score      = 0
        self.level      = level
        self.fleet_dir  = 1
        self.fleet_speed = 0.5 + level * 0.2
        self.drop_dist  = 18
        self.shoot_delay = max(20, 60 - level * 5)
        self.shoot_timer = 0
        self.player_shoot_delay = 15
        self.player_shoot_timer = 0
        self.state      = "playing"
        self.flash_timer = 0
        self.lives      = 3

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            if event.key == pygame.K_SPACE:
                self.try_shoot()
            if event.key == pygame.K_r and self.state in ("dead", "gameover", "win"):
                self.reset(1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.ship.moving_left = False
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False

    def try_shoot(self):
        if self.player_shoot_timer <= 0:
            self.bullets.append(Bullet(self.ship.center(), self.ship.y))
            self.player_shoot_timer = self.player_shoot_delay

    def alien_shoot(self):
        alive = [a for a in self.aliens if a.alive]
        if not alive:
            return
        shooter = random.choice(alive)
        self.alien_bullets.append(
            Bullet(int(shooter.x + Alien.SIZE // 2), int(shooter.y + Alien.SIZE),
                   color=RED, speed=5, w=3, h=10)
        )

    def update(self):
        if self.state != "playing":
            return
        for s in self.stars:
            s.update()
        self.ship.update()
        self.player_shoot_timer -= 1
        for b in self.bullets:
            b.update()
        self.bullets = [b for b in self.bullets if not b.off_screen()]
        for b in self.alien_bullets:
            b.update()
        self.alien_bullets = [b for b in self.alien_bullets if not b.off_screen()]
        alive = [a for a in self.aliens if a.alive]
        if not alive:
            self.state = "win"
            return
        edge_hit = False
        for a in alive:
            a.x += self.fleet_speed * self.fleet_dir
            if a.x + Alien.SIZE >= SCREEN_W or a.x <= 0:
                edge_hit = True
        if edge_hit:
            self.fleet_dir *= -1
            for a in alive:
                a.y += self.drop_dist
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.alien_shoot()
            self.shoot_timer = 0
        for b in self.bullets[:]:
            for a in alive:
                if b.rect.colliderect(a.rect()):
                    a.alive = False
                    self.explosions.append(Explosion(a.x + Alien.SIZE // 2, a.y + Alien.SIZE // 2, a.color()))
                    self.score += (4 - a.row) * 10
                    if b in self.bullets:
                        self.bullets.remove(b)
                    break
        for b in self.alien_bullets[:]:
            if b.rect.colliderect(self.ship.rect()):
                self.alien_bullets.remove(b)
                self.lives -= 1
                self.explosions.append(Explosion(self.ship.center(), self.ship.y + 20, GREEN))
                self.flash_timer = 40
                if self.lives <= 0:
                    self.state = "gameover"
                    self.high_score = max(self.high_score, self.score)
        for a in alive:
            if a.y + Alien.SIZE >= self.ship.y:
                self.state = "gameover"
                self.high_score = max(self.high_score, self.score)
        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if not e.dead()]
        if self.flash_timer > 0:
            self.flash_timer -= 1
        if self.state == "win":
            self.high_score = max(self.high_score, self.score)

    def draw(self):
        screen.fill(DARK_GRAY)
        for s in self.stars:
            s.draw(screen)
        if self.state == "playing":
            if self.flash_timer == 0 or self.flash_timer % 6 < 3:
                self.ship.draw(screen)
            for b in self.bullets:
                b.draw(screen)
            for b in self.alien_bullets:
                b.draw(screen)
            for a in self.aliens:
                a.draw(screen)
            for e in self.explosions:
                e.draw(screen)
            score_surf = font_medium.render(f"SCORE  {self.score:06}", True, CYAN)
            screen.blit(score_surf, (20, 14))
            hi_surf = font_medium.render(f"BEST  {self.high_score:06}", True, YELLOW)
            screen.blit(hi_surf, (SCREEN_W // 2 - hi_surf.get_width() // 2, 14))
            level_surf = font_medium.render(f"LEVEL {self.level}", True, PURPLE)
            screen.blit(level_surf, (SCREEN_W - level_surf.get_width() - 20, 14))
            for i in range(self.lives):
                lx = 20 + i * 40
                pygame.draw.polygon(screen, GREEN, [
                    (lx + 10, SCREEN_H - 30),
                    (lx + 4,  SCREEN_H - 12),
                    (lx + 16, SCREEN_H - 12),
                ])
        elif self.state == "win":
            self._overlay("LEVEL CLEAR!", f"Score: {self.score}", "Press R for next level")
        elif self.state == "gameover":
            self._overlay("GAME OVER", f"Score: {self.score}  Best: {self.high_score}", "Press R to restart")
        pygame.display.flip()

    def _overlay(self, title, sub, hint):
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        screen.blit(dim, (0, 0))
        t = font_large.render(title, True, YELLOW)
        screen.blit(t, (SCREEN_W // 2 - t.get_width() // 2, SCREEN_H // 2 - 80))
        s = font_medium.render(sub, True, WHITE)
        screen.blit(s, (SCREEN_W // 2 - s.get_width() // 2, SCREEN_H // 2))
        h = font_small.render(hint, True, CYAN)
        screen.blit(h, (SCREEN_W // 2 - h.get_width() // 2, SCREEN_H // 2 + 60))


def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if game.state == "win":
                    prev_score = game.score
                    prev_hi    = game.high_score
                    game.reset(game.level + 1)
                    game.score      = prev_score
                    game.high_score = prev_hi
        game.update()
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
