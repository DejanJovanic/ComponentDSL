class Config:
    def __init__(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        if 'active_features' in kwargs:
            self.active_features = kwargs['active_features']
        else:
            self.active_features = None
