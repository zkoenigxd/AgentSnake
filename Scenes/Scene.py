class Scene:
    def __init__(self):
        raise NotImplementedError
    
    def collect_input(self, context):
        raise NotImplementedError
    
    def process_input(self, dt: float, context):
        raise NotImplementedError