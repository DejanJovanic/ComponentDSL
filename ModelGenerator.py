from textx import metamodel_from_file, TextXSemanticError

from Classes.Component import Component
from Classes.Config import Config
from Classes.expression import Expression
from Classes.Term import Term
from Classes.Model import Model
from Classes.Models import Models


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
    if isinstance(model, Models):
        components_names_by_model = []
        models_names = []
        for item in model.models or []:
            check_name(item.name)
            names = []
            models_names.append(item.name)
            for component in item.components or []:
                check_component_tree_name(component, names)
            components_names_by_model.append(names)
        for name in models_names:
            for comp_names in components_names_by_model:
                if name in comp_names:
                    raise TextXSemanticError("Model name {name} already taken by another model or component"
                                             .format(name=name))


def check_feature_names(config):
    elements = set()
    for elem in config.active_features or []:
        if elem in elements:
            raise TextXSemanticError('More that 1 occurrence of {feat} feature'.format(feat=elem))
        else:
            elements.add(elem)


def extract_model_path(model_path):
    metamodel = metamodel_from_file('Grammar/grammar.tx', classes=[Model, Config,
                                                                   Component, Expression, Term,  Models])
    metamodel.register_model_processor(validate_names)
    metamodel.register_obj_processors({'Config': check_feature_names})
    model = metamodel.model_from_file(model_path)

    return model


def extract_model_string(model_string):
    metamodel = metamodel_from_file('Grammar/grammar.tx', classes=[Model, Config,
                                                                   Component, Expression, Term, Models])
    metamodel.register_model_processor(validate_names)
    metamodel.register_obj_processors({'Config': check_feature_names})
    model = metamodel.model_from_str(model_string)

    return model
