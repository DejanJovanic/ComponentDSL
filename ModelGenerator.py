from textx import metamodel_from_file, TextXSemanticError

from Classes.Component import Component
from Classes.Config import Config
from Classes.expressionAND import ExpressionAND
from Classes.expressionOR import ExpressionOR
from Classes.Model import Model


def check_name(model_name):
    if len(model_name) == 0 or model_name.isspace():
        raise TextXSemanticError('Name cannot be empty string.')


def check_component_tree_name(component, names):
    check_name(component.name)
    if component.name in names:
        raise TextXSemanticError('Name {name} is already taken by another component.' .format(name=component.name))
    else:
        names.append(component.name)

    for comp in component.components or []:
        check_component_tree_name(comp, names)


def validate_names(model, metamodel):
    if isinstance(model, Model):
        check_name(model.name)
        names = []
        for component in model.components or []:
            check_component_tree_name(component, names)


def check_feature_names(config):
    elements = set()
    for elem in config.active_features or []:
        if elem in elements:
            raise TextXSemanticError('More that 1 occurrence of {feat} feature'.format(feat=elem))
        else:
            elements.add(elem)


def extract_model_path(model_path):
    metamodel = metamodel_from_file('Grammar/grammar.tx', classes=[Model, Config,
                                                                   Component, ExpressionAND, ExpressionOR])
    metamodel.register_model_processor(validate_names)
    metamodel.register_obj_processors({'Config': check_feature_names})
    model = metamodel.model_from_file(model_path)

    return model


def extract_model_string(model_string):
    metamodel = metamodel_from_file('Grammar/grammar.tx', classes=[Model, Config,
                                                                   Component, ExpressionAND, ExpressionOR])
    metamodel.register_model_processor(validate_names)
    metamodel.register_obj_processors({'Config': check_feature_names})
    model = metamodel.model_from_str(model_string)

    return model
