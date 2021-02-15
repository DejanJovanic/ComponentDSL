from Minimize_expression import simplify


class ExplanationGenerator:

    def set_models_disable_explanation(self, models):
        if hasattr(models, 'models'):
            if isinstance(models.models, list):
                for model in models.models:
                    self.set_model_wide_explanation(model)

    def set_model_wide_explanation(self, model):
        if hasattr(model, 'components'):
            if isinstance(model.components, list):
                for component in model.components:
                    if not component.enabled:
                        self.set_component_explanation(component)

    def set_component_explanation(self, component):
        if len(component.components) == 0:
            expr = self.__get_required_expression(component.requirement)
            component.requirement_expression = expr
        else:
            expr = self.__get_required_expression(component.requirement)
            for comp in [item for item in component.components if not item.enabled]:
                self.set_component_explanation(comp)
                if not expr:
                    expr = comp.requirement_expression
                else:
                    expr = expr + " and " + comp.requirement_expression
            component.requirement_expression = expr

        component.disabled_reason = self.__get_disabled_reason(component.requirement_expression)

    def __get_disabled_reason(self, expression_string):
        simplified_expression = simplify(expression_string)
        return "Feature requirement ({expr}) has not been met" \
            .format(expr=simplified_expression)

    def __get_required_expression(self, require):
        if isinstance(require, str):
            if require.strip():
                return require
            else:
                return ""
        else:
            return require.get_expression()
