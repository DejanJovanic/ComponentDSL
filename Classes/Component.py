def get_required_expression(require):
    if require is not None:
        if isinstance(require, str):
            return require, [require]
        else:
            return require.get_expression()
    else:
        return "", []


class Component:
    def __init__(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        self.name = kwargs['name']
        if 'requirement' in kwargs:
            self.requirement = kwargs['requirement']
        else:
            self.requirement = None
        self.components = kwargs['components']
        self.requirement_expression = ""
        self.enabled = False

    def validate(self, config):
        if len(self.components) == 0:
            if isinstance(self.requirement, str):
                self.enabled = self.requirement in config.active_features
            else:
                self.enabled = self.requirement.evaluate(config.active_features)
        else:
            for component in self.components:
                component.validate()
                if not component.enabled:
                    self.enabled = False
            if self.enabled:
                self.enabled = self.requirement.evaluate(config.active_features)

    def set_disabled_reason(self):
        if not self.enabled:
            if len(self.components) == 0:
                expr, items = get_required_expression(self.requirement)
                self.requirement_expression = expr
            else:
                expr, req_items = get_required_expression(self.requirement)
                for component in [item for item in self.components if not item.enabled]:
                    component.set_disabled_reason()
                    if not expr:
                        expr = component.requirement_expression
                    else:
                        expr = " ( " + expr + " ) and ( " + component.requirement_expression + " ) "
                self.requirement_expression = expr
            ## Quine-McCluskey
