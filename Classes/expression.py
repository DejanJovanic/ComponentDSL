from Classes.Term import Term


class Expression:
    def __init__(self, **kwargs):
        self.left = kwargs['left']
        self.right = kwargs['right']
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        else:
            self.parent = None

    def get_expression(self):
        expr = ""
        if self.left is not None:
            expr = self.left.get_expression()

        if self.right is not None and len(self.right) > 0:
            for term in self.right:
                if isinstance(term, str):
                    expr = expr + " or " + term
                elif isinstance(term, Term):
                    expr = expr + " or " + term.get_expression()

        return expr

    def evaluate(self, features):
        left_bool = False

        if self.left is not None:
            if isinstance(self.left, str):
                left_bool = self.left in features or []
            else:
                left_bool = self.left.evaluate(features)
        if left_bool:
            return True

        if self.right is not None and len(self.right) > 0:
            for term in self.right:
                temp = False
                if isinstance(term, str):
                    temp = term in features or []
                else:
                    temp = term.evaluate(features)
                if temp:
                    return True
            return False
        else:
            return left_bool
