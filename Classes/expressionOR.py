from .expression import Expression


class ExpressionOR(Expression):
    def __init__(self, **kwargs):
        self.left = kwargs['left']
        self.right = kwargs['right']
        super().__init__(self.left, self.right, 'or')
        if 'parent' in kwargs:
            self.parent = kwargs['parent']

    def evaluate(self, features):
        left_bool = False
        right_bool = False
        if isinstance(self.left, str):
            left_bool = self.left in features
        elif isinstance(self.left, Expression):
            left_bool = self.left.evaluate(features)
        if isinstance(self.right, str):
            right_bool = self.right in features
        elif isinstance(self.right, Expression):
            left_bool = self.right.evaluate(features)
        return left_bool or right_bool
