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
schema = 'nomad_parser_plugins_camels_files.parsers.parser.CamelsMeasurement' 

camels_app = AppEntryPoint(
    name="CAMELS App",
    description="App that allows you to search and navigate your CAMELS measurements.",
    app=App(
        label='CAMELS App',
        path='myapp',
        category='Experiment',
        filters=Filters(
            include=['*#nomad_parser_plugins_camels_files.parsers.parser.CamelsMeasurement'],
        ),
        columns=[
            Column(quantity='entry_id', selected=True),
            Column(
                quantity=f'entry_name',
                selected=True
            ),
            Column(
                quantity=f'resjunktest',
                selected=True
            ),
            Column(
                quantity=f'data.data.camels_user#{schema}',
                selected=True
            ),
            Column(quantity='upload_create_time')
        ],
        filter_menus=FilterMenus(
        options={
            'custom_quantities': FilterMenu(label='User Defined Quantities'),
            'author': FilterMenu(label='Author / Origin / Dataset'),
        }
        ),
        filters_locked={
            'section_defs.definition_qualified_name': [
                'nomad_parser_plugins_camels_files.parsers.parser.CamelsMeasurement',
            ],
        },

),
)
    



    











# ---------------------------------------------------------------------------------------------------
# App(
#         # Label of the App
#         label='My App',
#         # Path used in the URL, must be unique
#         path='myapp',
#         # Used to categorize apps in the explore menu
#         category='Theory',
#         # Brief description used in the app menu
#         description='An app customized for me.',
#         # Longer description that can also use markdown
#         readme='Here is a much longer description of this app.',
#         # Controls the available search filters. If you want to filter by
#         # quantities in a schema package, you need to load the schema package
#         # explicitly here. Note that you can use a glob syntax to load the
#         # entire package, or just a single schema from a package.
#         filters=Filters(
#             include=[f'*#{schema}'],
#         ),
#         # Controls which columns are shown in the results table
#         columns=[
#             Column(quantity='entry_id', selected=True),
#             # Column(
#             #     quantity=f'data.section.myquantity#{schema}',
#             #     selected=True
#             # ),
#             # Column(
#             #     quantity=f'data.my_repeated_section[*].myquantity#{schema}',
#             #     selected=True
#             # ),
#             Column(quantity='upload_create_time')
#         ],
#         # Dictionary of search filters that are always enabled for queries made
#         # within this app. This is especially important to narrow down the
#         # results to the wanted subset. Any available search filter can be
#         # targeted here. This example makes sure that only entries that use
#         # MySchema are included.
#         filters_locked={
#             "section_defs.definition_qualified_name:all": [schema]
#         },
#         # Controls the filter menus shown on the left
#         filter_menus=FilterMenus(
#             options={
#                 'material': FilterMenu(label="Material"),
#             }
#         ),
#         # Controls the default dashboard shown in the search interface
#         # dashboard={
#         #     'widgets': [
#         #         {
#         #             'type': 'histogram',
#         #             'showinput': False,
#         #             'autorange': True,
#         #             'nbins': 30,
#         #             'scale': 'linear',
#         #             'quantity': f'data.camels_user#{schema}',
#         #             'layout': {
#         #                 'lg': {
#         #                     'minH': 3,
#         #                     'minW': 3,
#         #                     'h': 4,
#         #                     'w': 12,
#         #                     'y': 0,
#         #                     'x': 0
#         #                 }
#         #             }
#         #         }
#         #     ]
#         # }
#     )
# )