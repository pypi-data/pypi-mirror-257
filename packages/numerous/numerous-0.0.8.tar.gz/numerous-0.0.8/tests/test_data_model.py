from numerous import app, container, html, slider
from numerous.data_model import (
    ContainerDataModel,
    HTMLElementDataModel,
    NumberFieldDataModel,
    SliderElementDataModel,
    TextFieldDataModel,
    ToolDataModel,
    dump_data_model,
)


def test_dump_data_model_expected_tool_name() -> None:
    @app
    class ToolWithAName:
        param: str

    data_model = dump_data_model(ToolWithAName)

    assert data_model.name == "ToolWithAName"


def test_dump_data_model_number_field() -> None:
    default_param_value = 5

    @app
    class Tool:
        param: float = default_param_value

    data_model = dump_data_model(Tool)

    assert data_model == ToolDataModel(
        name="Tool",
        elements=[
            NumberFieldDataModel(name="param", default=default_param_value),
        ],
    )


def test_dump_data_model_text_field() -> None:
    default_param_value = "default string"

    @app
    class Tool:
        param: str = default_param_value

    data_model = dump_data_model(Tool)

    assert data_model == ToolDataModel(
        name="Tool",
        elements=[
            TextFieldDataModel(name="param", default=default_param_value),
        ],
    )


def test_dump_data_model_html_element_field() -> None:
    @app
    class HTMLTool:
        html: str = html(default="<div></div>")

    data_model = dump_data_model(HTMLTool)

    assert data_model == ToolDataModel(
        name="HTMLTool",
        elements=[HTMLElementDataModel(name="html", default="<div></div>")],
    )


def test_dump_data_model_slider_element_field() -> None:
    @app
    class SliderTool:
        slider: float = slider(default=10.0, min_value=-20.0, max_value=30.0)

    data_model = dump_data_model(SliderTool)

    assert data_model == ToolDataModel(
        name="SliderTool",
        elements=[
            SliderElementDataModel(
                name="slider",
                default=10.0,
                slider_min_value=-20.0,
                slider_max_value=30.0,
            ),
        ],
    )


def test_dump_data_model_slider_element_field_with_defaults() -> None:
    @app
    class SliderTool:
        slider: float = slider()

    data_model = dump_data_model(SliderTool)

    assert data_model == ToolDataModel(
        name="SliderTool",
        elements=[
            SliderElementDataModel(
                name="slider",
                default=0.0,
                slider_min_value=0.0,
                slider_max_value=100.0,
            ),
        ],
    )


def test_dump_data_model_container_field() -> None:
    default_param_value = "default string"

    @container
    class Container:
        param: str = default_param_value

    @app
    class Tool:
        container: Container

    data_model = dump_data_model(Tool)

    assert data_model == ToolDataModel(
        name="Tool",
        elements=[
            ContainerDataModel(
                name="container",
                elements=[
                    TextFieldDataModel(name="param", default=default_param_value),
                ],
            ),
        ],
    )
