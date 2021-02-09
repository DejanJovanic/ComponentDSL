class Model:
    def __init__(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        self.name = kwargs['name']
        if 'config' in kwargs:
            self.config = kwargs['config']
        else:
            self.config = None
        self.components = kwargs['components']