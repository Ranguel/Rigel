
import pygame

color = [(250, 20, 20), (20, 250, 20), (20, 20, 250), (250, 250, 20),
         (250, 20, 250), (10, 10, 10), (100, 100, 100), (255, 255, 255)]

class Text(object):
    def __init__(self, xpos, ypos, size, col, font = None, aline = 'center'):
        self.font = pygame.font.SysFont(font, size) if type(font)==str else pygame.font.Font("Util/space_invaders.ttf", size)
        self.image, self.c = pygame.Surface((30, 30)), color[col]
        self.rect = self.image.get_rect(center=(xpos, ypos))
        self.aline = aline

    def update(self, screen, text):
        self.surface = self.font.render(str(text), True, self.c)
        self.imarect = self.surface.get_rect(center=(self.rect.center)) if self.aline == 'center' else self.surface.get_rect(topleft=(self.rect.center))
        screen.blit(self.surface, self.imarect)


def err_message(self):
    pygame.mixer.pre_init(44100, -16, 1, 4096)
    pygame.init()

    sonido = pygame.mixer.Sound("Assets/sounds/erro.mp3")  # Asegúrate que el archivo esté en la misma carpeta

    sonido.play()
    self.frame_timer = 60
    self.play = True
    self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
    message1 = Text(140, 80, 240, -1, "Segoe UI", 1)
    message2 = Text(140, 400, 40, -1, "Segoe UI", 1)
    message3 = Text(140, 450, 40, -1, "Segoe UI", 1)
    message4 = Text(140, 500, 40, -1, "Segoe UI", 1)
    while self.play:
        self.frame_timer -= 1
        self.screen.fill((0, 120, 215))
        self.collisions()
        message1.update(self.screen, ":(")
        message2.update(
            self.screen, "Your PC ran into a problem and needs to restart. We're")
        message3.update(
            self.screen, "just collecting some error info, and then we'll restart for")
        message4.update(self.screen, "you")

        pygame.display.flip()
        self.frame.tick(60)
        self.input()
        if self.frame_timer < 0:
            self.play = False
        

