import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED,
    PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
)
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown_sec = 0

    def _can_shoot(self) -> bool:
        return self.shoot_cooldown_sec == 0

    def _update_cooldown(self, dt: float) -> None:
        self.shoot_cooldown_sec = max(self.shoot_cooldown_sec-dt, 0)

    def _reset_cooldown(self) -> None:
        self.shoot_cooldown_sec = PLAYER_SHOOT_COOLDOWN_SECONDS
        
    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)    

    def rotate(self, dt: float) -> None:
        self.rotation += dt * PLAYER_TURN_SPEED

    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        forward *= dt * PLAYER_SPEED
        self.position += forward

    def shoot(self) -> None:
        if not self._can_shoot():
            return
        ret = Shot(self.position.x, self.position.y)
        ret.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self._reset_cooldown()

    def update(self, dt: float) -> None:
        self._update_cooldown(dt)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_z]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
            
