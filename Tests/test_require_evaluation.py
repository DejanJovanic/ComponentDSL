from ModelGenerator import extract_model_string


def test_invalid_requirement1():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }
            
            component "Comp1" {
                require = a and b and f and c
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == 'a and b and f and c'
    assert 'a and b and c and f' in component.disabled_reason


def test_invalid_requirement2():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a and f) or (f or z) or (c and g)
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a and f) or (f or z) or (c and g)'
    assert 'f or z or (c and g)'.lower() in component.disabled_reason


def test_invalid_requirement3():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = a and b and (c and g)
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == 'a and b and (c and g)'
    assert 'a AND b AND c AND g'.lower() in component.disabled_reason


def test_invalid_requirement4():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a or e) and (f or g)
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a or e) and (f or g)'
    assert '(a AND f) OR (a AND g) OR (e AND f) OR (e AND g)'.lower() in component.disabled_reason


def test_invalid_requirement5():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,d
            }

            component "Comp1" {
                require = (a and b) or (a and (b or c)) or ((b or c) and b)
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a and b) or (a and (b or c)) or ((b or c) and b)'
    assert 'b or (a AND c)'.lower() in component.disabled_reason


def test_invalid_requirement6():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,c,d
            }

            component "Comp1" {
                require = (a and b) or (a and (b or c)) and ((b or c) and b)
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a and b) or (a and (b or c)) and ((b or c) and b)'
    assert 'a AND b'.lower() in component.disabled_reason


def test_invalid_gathered_requirement1():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a and b) or a and d
                
                component "Comp2" {
                    require = a and f
                }
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a and b) or a and d and a and f'
    assert 'a AND (b OR d) AND (b OR f)'.lower() in component.disabled_reason

    assert not component.components[0].enabled
    assert component.components[0].requirement_expression == 'a and f'
    assert 'a and f'.lower() in component.components[0].disabled_reason


def test_invalid_gathered_requirement2():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a and g) or (b and f)

                component "Comp2" {
                    require = a and b
                }
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a and g) or (b and f)'
    assert '(a OR b) AND (a OR f) AND (b OR g) AND (f OR g)'.lower() in component.disabled_reason

    assert component.components[0].enabled


def test_invalid_gathered_requirement3():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a and g) or (b and f)

                component "Comp2" {
                    require = a and f
                }
                
                component "Comp3"{
                    require = (a or b) and (g or f)
                }
                
                component "Comp4"{
                    require = f
                }
                
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a and g) or (b and f) and a and f and (a or b) and (g or f) and f'
    assert 'a AND (b OR g) AND (f OR g)'.lower() in component.disabled_reason

    assert not component.components[0].enabled
    assert component.components[0].requirement_expression == 'a and f'
    assert 'a and f'.lower() in component.components[0].disabled_reason

    assert not component.components[1].enabled
    assert component.components[1].requirement_expression == '(a or b) and (g or f)'
    assert '(a AND f) OR (a AND g) OR (b AND f) OR (b AND g)'.lower() in component.components[1].disabled_reason

    assert not component.components[2].enabled
    assert component.components[2].requirement_expression == 'f'
    assert 'f' in component.components[2].disabled_reason


def test_invalid_gathered_requirement4():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a and g) or (b and f)

                component "Comp2" {
                    require = a and f
                }
                
                component "Comp3"{
                    require = a
                }
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert not component.enabled
    assert component.requirement_expression == '(a and g) or (b and f) and a and f'
    assert 'a AND (b OR g) AND (f OR g)'.lower() in component.disabled_reason

    assert not component.components[0].enabled
    assert component.components[0].requirement_expression == 'a and f'
    assert 'a and f' in component.components[0].disabled_reason

    assert component.components[1].enabled


def test_valid_requirement1():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = a and b or (c and f)
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert component.enabled


def test_valid_requirement2():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = a and b and (c or f)
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert component.enabled


def test_valid_requirement3():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = a and b and (c or d)
                
                component "Comp2"{
                    require = a and d
                }
            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert component.enabled
    assert component.components[0].enabled


def test_valid_requirement4():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a or b) and (c or f) and (g or b or a or f) and (z or f or g or a)

            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert component.enabled


def test_valid_requirement5():
    model_str = """
        model 'Model1'{
            configuration{
                active_features = a,b,c,d
            }

            component "Comp1" {
                require = (a and g and c and d) or (a and b and c and z) or (a and b and c and d)

            }
        }
    """

    model = extract_model_string(model_str)
    component = model.models[0].components[0]
    assert component.enabled
