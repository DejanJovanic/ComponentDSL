import pytest
from textx import TextXSyntaxError

from ModelGenerator import extract_model_string


def test_empty_model_no_name():
    model = """
        model {
        
        }
    """
    with pytest.raises(TextXSyntaxError):
        extract_model_string(model)
