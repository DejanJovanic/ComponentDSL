from ModelGenerator import extract_model_path


if __name__ == "__main__":
    model = extract_model_path('Models/Components.model')
    for item in model.components:
        item.validate(model.config)
    for item in model.components:
        item.set_disabled_reason()
    b = model
