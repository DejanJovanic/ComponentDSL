from .expression import Expression


class ExpressionOR(Expression):
    def __init__(self, **kwargs):
        self.left = kwargs['left']
        self.right = kwargs['right']
        super().__init__(self.left, self.right, 'or')
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
