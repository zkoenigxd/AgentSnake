class Scene:
    def __init__(self):
        raise NotImplementedError
    
    def set_game_manager(self, game_manager):
        self.game_manager = game_manager
    
    def collect_input(self, context):
        raise NotImplementedError
    
    def process_input(self, dt: float, context):
        raise NotImplementedError
    
    def render_scene(self, screen, context):
        raise NotImplementedError
    
    def set_scale(self, width):
        raise NotImplementedError