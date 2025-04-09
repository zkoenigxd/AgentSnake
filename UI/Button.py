import pygame

class Button:
    def __init__(self, label, callback=None, broadcast_value=None, font_size=24):
        """
        :param label: Text label for the button.
        :param callback: Optional function to call directly when clicked.
        :param broadcast_value: Value to broadcast to subscribers when clicked.
        :param font_size: The font size of the button text.
        """
        self.label = label
        self.callback = callback
        self.broadcast_value = broadcast_value
        self.rect = pygame.Rect(0, 0, 0, 0)  # Will be set by layout logic.
        self.font = pygame.font.SysFont("Arial", font_size)
        self.subscribers = []  # List of functions to call on click.

    def subscribe(self, fn):
        """Registers a callback function to be notified with self.broadcast_value when the button is clicked."""
        self.subscribers.append(fn)

    def on_click(self):
        """Should be called when the button is pressed. It first calls an optional direct callback,
        then broadcasts its event value to all subscribers."""
        if self.callback:
            self.callback()
        for fn in self.subscribers:
            fn(self.broadcast_value)

    def draw(self, screen):
        """Draws the button (background, border, and centered label) on the provided screen."""
        # Button background (white)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        # Border (black)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        # Render and center the label text.
        text_surf = self.font.render(self.label, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)