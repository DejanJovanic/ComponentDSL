from Classes.Models import Models


class ComponentValidator:

    def validate_models(self, models: Models):
        if hasattr(models, 'models'):
            if isinstance(models.models, list):
                for model in models.models:
                    self.__validate_model(model)

    def __validate_model(self, model):
        if hasattr(model, 'components') and hasattr(model, 'config'):
            if isinstance(model.components, list):
                features = model.config.active_features if hasattr(model.config, 'active_features') else []
                for component in model.components:
                    self.__validate_component(component, features)
        else:
            raise TypeError("Invalid model supplied")



    def __validate_component(self, component, active_features):
        if len(component.components) == 0:
            self.__validate_component_requirement(component, active_features)
        else:
            for comp in component.components or []:
                self.__validate_component(comp, active_features)
                if not comp.enabled:
                    component.enabled = False
            if component.enabled:
                self.__validate_component_requirement(component, active_features)

    def __validate_component_requirement(self, component, active_features):
        if isinstance(component.requirement, str):
            if component.requirement.strip():
                component.enabled = component.requirement in active_features
            else:
                component.enabled = True
        else:
            component.enabled = component.requirement.evaluate(active_features)
