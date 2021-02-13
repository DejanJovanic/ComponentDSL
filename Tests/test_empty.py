import pytest
from textx import TextXSyntaxError, TextXSemanticError

from ModelGenerator import extract_model_string


def test_empty_model_no_name():
    model = """
        model {
        
        }
    """
    with pytest.raises(TextXSyntaxError):
        extract_model_string(model)


def test_model_empty_correctly():
    model = """
        model 'model'{
        
        }
    """
    gen_model = extract_model_string(model)

    assert gen_model is not None and gen_model.models and len(gen_model.models) == 1


def test_model_name_incorrect():
    model_str = """
        model 'a'{
            component 'b'{
                component 'c'{
                }
                component 'd'{
                    component 'a'{
                    }
                }
            }
        }
    """
    with pytest.raises(TextXSemanticError):
        extract_model_string(model_str)


def test_model_name_incorrect2():
    model_str = """
        model 'g'{
            component 'b'{
                component 'c'{
                }
                component 'd'{
                    component 'a'{
                    }
                }
            }
        }
        model 'a'{
        
        }
    """
    with pytest.raises(TextXSemanticError):
        extract_model_string(model_str)


def test_component_name_incorrect2():
    model_str = """
        model 'g'{
            component 'b'{
                component 'c'{
                }
                component 'd'{
                    component 'a'{
                    }
                }
            }
            component 'f'{
            }
                component 'r'{
            }
                component 'a'{
            }
        }
        model 'z'{

        }
    """
    with pytest.raises(TextXSemanticError):
        extract_model_string(model_str)


def test_component_name_correct():
    model_str = """
        model 'g'{
            component 'b'{
                component 'c'{
                }
                component 'd'{
                    component 'a'{
                    }
                }
            }
            component 'f'{
            }
                component 'r'{
            }
                component 'fa'{
            }
        }

    """
    model = extract_model_string(model_str)
    components = model.models[0].components
    assert len(components) == 4
    assert len(components[0].components) == 2
    assert len(components[0].components[1].components) == 1
    assert len(components[1].components) == 0
    assert len(components[2].components) == 0
    assert len(components[3].components) == 0


def test_config():
    model_str = """
        configuration {
            active_features = 
        }
    """

    model = extract_model_string(model_str)
    assert not model.active_features


def test_config2():
    model_str = """
        configuration {
            active_features = feature1,feature2,feat3
        }
    """

    model = extract_model_string(model_str)
    assert len(model.active_features) == 3


def test_config3():
    model_str = """
        configuration {
            active_features = feature1,feature2,feat3,
        }
    """

    with pytest.raises(TextXSyntaxError):
        extract_model_string(model_str)


def test_config4():
    model_str = """
        configuration {
            active_features = feature1,feature2,...
        }
    """

    with pytest.raises(TextXSyntaxError):
        extract_model_string(model_str)


def test_component():
    model_str = """
        component 'comp1'{
            feature = 
        }
    """

    with pytest.raises(TextXSyntaxError):
        extract_model_string(model_str)


def test_component1():
    model_str = """
        component 'comp1'{

        }
    """

    extract_model_string(model_str)


def test_component2():
    model_str = """
    model 'Model'{
        component 'comp1'{
            require = a and b
            
            component 'comp2' {
            
            }
        }
    }
      
    """

    extract_model_string(model_str)


def test_component3():
    model_str = """
    model 'Model'{
        component 'comp1'{
            require = a and b

            component 'comp2' {

            }
            
            component 'comp2' {
            
            }
        }
    }

    """
    with pytest.raises(TextXSemanticError):
        extract_model_string(model_str)


def test_component4():
    model_str = """
    model 'Model'{
        component 'comp1'{
            require = a and b

            component 'comp2' {

            }

            component 'comp3' {

            }
        }
        component 'comp1'{
        }
    }

    """
    with pytest.raises(TextXSemanticError):
        extract_model_string(model_str)


def test_component5():
    model_str = """
    model 'Model'{
        component 'comp1'{
            require = a and b

            component 'comp2' {

            }

            component 'comp3' {

            }
        }
        component 'comp3'{
        }
    }

    """
    with pytest.raises(TextXSemanticError):
        extract_model_string(model_str)
