import Classes.expression as expres


class Term:
    def __init__(self, **kwargs):
        self.left = kwargs['left']
        self.right = kwargs['right']
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        else:
            self.parent = None

    def get_expression(self):
        expr = ""
        if isinstance(self.left, expres.Expression):
            expr = "(" + self.left.get_expression() + ")"
        else:
            expr = self.left

        if self.right is not None and len(self.right) > 0:
            for term in self.right:
                if isinstance(term, str):
                    expr = expr + " and " + term
                elif isinstance(term, expres.Expression):
                    expr = expr + " and (" + term.get_expression() + ")"

        return expr

    def evaluate(self, features):
        left_bool = False

        if self.left is not None:
            if isinstance(self.left, str):
                left_bool = self.left in features or []
            else:
                left_bool = self.left.evaluate(features)
        if not left_bool:
            return False

        if self.right is not None and len(self.right) > 0:
            for term in self.right:
                temp = False
                if isinstance(term, str):
                    temp = term in features or []
                else:
                    temp = term.evaluate(features)

                if not temp:
                    return False
            return True
        else:
            return left_bool



