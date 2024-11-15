import yaml
from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    Columns,
    FilterMenu,
    FilterMenus,
    Filters,
)

yaml_data = """
        label: My App
        path: myapp
        category: Theory
        """
camels_app = AppEntryPoint(
    name="CAMELSApp",
    description="App defined using the new plugin mechanism.",
    app=App.parse_obj(
            yaml.safe_load(yaml_data)
    ),
)
