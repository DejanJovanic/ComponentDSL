from abc import ABC, abstractmethod


class Expression(ABC):
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation

    def get_expression(self):
        """
        Metoda koja odredjuje string verziju required logickog izraza
        :return:
            tuple a,b -> a string koji predstavlja boolean izraz, b je lista koja sadrzi elemente u izrazu
        """
        expression = ""
        requirements = []
        if isinstance(self.left, str) and isinstance(self.right, str):
            requirements = [self.left, self.right]
            expression = self.left + ' ' + self.operation + ' ' + self.right
        elif isinstance(self.left, str):
            expr, req = self.right.get_expression()
            requirements.append(self.left)
            requirements.extend([item for item in req if item not in requirements])
            expression = self.left + " " + self.operation + " ( " + expr + " ) "
        elif isinstance(self.right, str):
            expr, req = self.left.get_expression()
            requirements = req
            if self.right not in requirements:
                requirements.append(self.right)
            expression = " ( " + expr + " ) " + self.operation + " " + self.right
        else:
            expr_left, req_left = self.left.get_expression()
            requirements = req_left
            expr_right, req_right = self.right.get_expression()
            requirements.extend([item for item in req_right if item not in requirements])
            expression = " ( " + expr_left + " ) " + self.operation + " ( " + expr_right + " ) "

        return expression, requirements

    @abstractmethod
    def evaluate(self, features):
        pass
