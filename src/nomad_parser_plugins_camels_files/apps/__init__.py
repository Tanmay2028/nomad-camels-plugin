# import yaml
# from nomad.config.models.plugins import AppEntryPoint
# from nomad.config.models.ui import (
#     App,
#     Column,
#     Columns,
#     FilterMenu,
#     FilterMenus,
#     Filters,
# )

# yaml_data = """
#         label: My App
#         path: myapp
#         category: Theory
#         """
# myapp = AppEntryPoint(
#     name="CAMELSApp",
#     description="App defined using the new plugin mechanism.",
#     app=App(
#         label="NewApp",
#         path="app",
#         category="simulation",
#         columns=Columns(
#             selected=["entry_id"],
#             options={
#                 "entry_id": Column(),
#             },
#         ),
#         filter_menus=FilterMenus(
#             options={
#                 "material": FilterMenu(label="Material"),
#             }
#         ),
#     ),
# )
