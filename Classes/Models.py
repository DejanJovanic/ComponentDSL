class Models:
    def __init__(self, **kwargs):
        if 'models' in kwargs and kwargs['models'] is not None:
            self.models = kwargs['models']
        else:
            self.models = []