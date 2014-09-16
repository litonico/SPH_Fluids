import sys
import pygame
from vec2 import length

class ParticleGraphics(object):
    def __init__(self, window_size):
        pygame.init() 
        self.window = pygame.display.set_mode(window_size) 
        self.radius = 5

    def draw(self, particles, H, scale): 
        scale = 500 // scale
        self.window.fill((0,0,0))

        for particle in particles:

            # Area of influence (H)
            pygame.draw.circle(self.window, (0, 0, 255), (
                int(particle.position.x*scale), 
                int(particle.position.y*scale)), 
                H*scale//2, 1)

            # Particles
            pygame.draw.circle(self.window, (255, 255, 255), (
                int(particle.position.x*scale), 
                int(particle.position.y*scale)), 
                self.radius)

            # Velocity vectors
            pygame.draw.line(self.window, (255, 255, 0), 
                # start
                (int(particle.position.x*scale), 
                 int(particle.position.y*scale)), 
                # end
                (int((particle.position.x+particle.velocity.x)*scale),
                 (int((particle.position.y+particle.velocity.y)*scale))))

        getch = input()

        # Draw to screen
        pygame.display.flip() 

graphics = ParticleGraphics((500, 500))
