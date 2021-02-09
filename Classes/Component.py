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
        self.required_features = []
        self.disabled = False

    def validate(self, config):
        if len(self.components) == 0:
            expr, items = get_required_expression(self.requirement)
            self.requirement_expression = expr
            self.required_features = items
            if len(items) > 1:
                params = {item: (item in config.active_features) for item in items}
                ret = eval(self.requirement_expression, {}, params)
                self.disabled = not ret
            else:
                self.disabled = not items[0] in config.active_features
        if self.disabled:
            pass #Quine-McCluskey
        else:
            expr, req_items = get_required_expression(self.requirement)
            disabled_components = []
            for component in self.components:
                component.validate(config)
                req_items.extend([item for item in component.required_features if item not in req_items])
                if component.disabled:
                    self.disabled = True
                    disabled_components.append(component)
                if expr:
                    expr = " ( " + expr + " ) and ( " + component.requirement_expression + " ) "
                else:
                    expr = component.requirement_expression
            self.requirement_expression = expr
            self.required_features = req_items
            if self.disabled:
                pass #Quine-McCluskey
