from textx import metamodel_from_file, TextXSemanticError

from Classes.Component import Component
from Classes.Config import Config
from Classes.expressionAND import ExpressionAND
from Classes.expressionOR import ExpressionOR
from Classes.Model import Model


def extract_model_path(model_path):
    metamodel = metamodel_from_file('Grammar/grammar.tx', classes=[Model, Config,
                                                                   Component, ExpressionAND, ExpressionOR])

    model = metamodel.model_from_file(model_path)

    return model


def extract_model_string(model_string):
    metamodel = metamodel_from_file('Grammar/grammar.tx', classes=[Model, Config,
                                                                   Component, ExpressionAND, ExpressionOR])

    model = metamodel.model_from_str(model_string)

    return model
