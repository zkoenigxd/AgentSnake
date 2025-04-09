import pygame

class Button:
    def __init__(self, label, callback, font_size=24):
        self.label = label
        self.callback = callback
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.font = pygame.font.SysFont("Arial", font_size)

    def draw(self, screen):
        # Draw button background (white) and border (black)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        # Render text and center it on the button
        text_surf = self.font.render(self.label, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
