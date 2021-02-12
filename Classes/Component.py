from Minimize_expression import simplify


def get_required_expression(require):
    if isinstance(require, str):
        if require.strip():
            return require
        else:
            return ""
    else:
        return require.get_expression()


class Component:
    def __init__(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        self.name = kwargs['name']
        if 'requirement' in kwargs:
            self.requirement = kwargs['requirement']
            if self.requirement is None:
                self.requirement = ""
        else:
            self.requirement = ""
        self.components = kwargs['components']
        self.requirement_expression = ""
        self.simplified_requirement_expression = ""
        self.disabled_reason = ""
        self.enabled = True

    def __set_self_enable(self, config):
        if isinstance(self.requirement, str):
            if self.requirement.strip():
                self.enabled = self.requirement in config.active_features if config is not None else []
            else:
                self.enabled = True
        else:
            self.enabled = self.requirement.evaluate(config.active_features if config is not None else [])

    def validate(self, config):

        if len(self.components) == 0:
            self.__set_self_enable(config)
        else:
            for component in self.components or []:
                component.validate(config)
                if not component.enabled:
                    self.enabled = False
            if self.enabled:
                self.__set_self_enable(config)

    def set_disabled_reason(self):
        if not self.enabled:
            if len(self.components) == 0:
                expr = get_required_expression(self.requirement)
                self.requirement_expression = expr
            else:
                expr = get_required_expression(self.requirement)
                for component in [item for item in self.components if not item.enabled]:
                    component.set_disabled_reason()
                    if not expr:
                        expr = component.requirement_expression
                    else:
                        expr = " ( " + expr + " ) and ( " + component.requirement_expression + " ) "
                self.requirement_expression = expr
            self.simplified_requirement_expression = simplify(self.requirement_expression)
            self.disabled_reason = "Feature requirement ({expr}) has not been met"\
                .format(expr=self.simplified_requirement_expression)
