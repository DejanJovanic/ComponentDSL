from sympy.logic import simplify_logic


def simplify(expression_string):
    expr = expression_string.replace(' and ', ' & ').replace(' or ', ' | ')
    simplified_expr = simplify_logic(expr=expr, force=True)
    return str(simplified_expr).replace(' & ', ' and ').replace(' | ',' or ').replace('~', ' not ')
