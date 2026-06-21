import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from shot import Shot
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame group
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    shots = pygame.sprite.Group()
    # Wherever a Shot is created it will be part of the shots, drawable and updatable
    # meaning it will appear in the screen even if its a local variable
    # see player::Player::shoot
    Shot.containers = (shots, drawable, updatable)
    
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()

    clock = pygame.time.Clock()
    dt = 0.0 # in second delta time
    
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill("black")
        updatable.update(dt)
        for a in asteroids:
            if player.collide_with(a):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for a in asteroids:
            for s in shots:
                if a.collide_with(s):
                    log_event("asteroid_shot")
                    a.split()
                    s.kill()
                    break
        for d in drawable:
            d.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
