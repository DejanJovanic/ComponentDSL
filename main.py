from ModelGenerator import extract_model_path


if __name__ == "__main__":
    model = extract_model_path('Models/Components.model')
    for item in model.models:
        for curr_comp in item.components:
            curr_comp.validate(item.config)

    for item in model.models:
        for curr_comp in item.components:
            curr_comp.set_disabled_reason()

    b = model
