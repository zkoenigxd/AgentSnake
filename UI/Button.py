import pygame

# Ensure the font module is initialized
if not pygame.font.get_init():
    pygame.font.init()
    
class Button:
    def __init__(self, label, callback=None, broadcast_value=None, font_size=24):
        """
        :param label: Text label for the button.
        :param callback: Optional function to call directly when clicked.
        :param broadcast_value: Value to broadcast to subscribers when clicked (optional).
        :param font_size: The font size of the button text.
        """
        self.label = label
        self.callback = callback
        self.broadcast_value = broadcast_value
        self.rect = pygame.Rect(0, 0, 0, 0)  # Will be set by layout logic.
        self.font = pygame.font.SysFont("Arial", font_size)
        self.subscribers = []  # List of functions to call on click.

    def subscribe(self, fn):
        """Registers a callback function to be notified when the button is clicked."""
        self.subscribers.append(fn)

    def on_click(self):
        """Should be called when the button is pressed. It first calls an optional direct callback,
        then notifies all subscribers, passing broadcast_value only if it exists."""
        if self.callback:
            self.callback()
        for fn in self.subscribers:
            if self.broadcast_value is not None:
                fn(self.broadcast_value)
            else:
                fn()

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