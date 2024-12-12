from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemHistogram,
    MenuItemTerms,
    MenuItemCustomQuantities,
    SearchQuantities,
    Dashboard,
    WidgetTerms,
    WidgetHistogram,
    BreakpointEnum,
    Layout,
)

schema = 'nomad_parser_plugins_camels_files.schema_packages.camels_package.CamelsMeasurement'

camels_app = AppEntryPoint(
    name='CAMELS App',
    description='App that allows you to search and navigate your CAMELS measurements.',
    app=App(
        label='CAMELS App',
        path='myapp',
        category='Experiment',
        search_quantities=SearchQuantities(include=[f'*#{schema}']),
        columns=[
            Column(search_quantity=f'data.name#{schema}', selected=True),
            Column(search_quantity=f'data.datetime#{schema}', selected=True),
            Column(search_quantity=f'data.camels_user#{schema}', selected=True),
            Column(search_quantity=f'data.session_name#{schema}', selected=True),
            Column(search_quantity=f'data.end_time#{schema}'),
            Column(search_quantity=f'data.protocol_overview#{schema}'),
            Column(search_quantity=f'data.description#{schema}'),


        ],
        dashboard = Dashboard(
        widgets=[
            WidgetTerms(
                title="Sample name",
                type="terms",
                layout={
                    BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
                },
                search_quantity=f"data.samples.name#{schema}"
        ),
            WidgetTerms(
                title="User",
                type="terms",
                layout={
                    BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
                },
                search_quantity=f"data.camels_user#{schema}"
        ),
        WidgetTerms(
            title='Instrument name',
            type='terms',
            layout={
                BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
            },
            search_quantity=f'data.instruments.name#{schema}'
        ),
        WidgetHistogram(
            title='Start time',
            type='histogram',
            layout={
                BreakpointEnum.MD: Layout(h=6, w=6, x=0, y=0)
            },
            x=f'data.datetime#{schema}'
        ),
        WidgetTerms(
            title='Tags',
            type='terms',
            layout={
                BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
            },
            search_quantity=f'results.eln.tags'
        ),



    ]
),
        menu=Menu(
            items=[
                Menu(
                    title='Camels',
                    items=[
                        MenuItemTerms(
                            search_quantity=f'data.session_name#{schema}',
                            options=5,
                        ),
                        MenuItemCustomQuantities(

                        ),
                        MenuItemHistogram(
                            x=f'data.datetime#{schema}',
                        ),
                    ],
                ),
                Menu(
                    title='Author / Origin / Dataset',
                    items=[
                        MenuItemTerms(
                            search_quantity='authors.name',
                            options=0,
                        ),
                        MenuItemHistogram(
                            x='upload_create_time',
                        ),
                        MenuItemTerms(
                            search_quantity='external_db',
                            options=5,
                            show_input=False,
                        ),
                        MenuItemTerms(
                            search_quantity='datasets.dataset_name',
                        ),
                        MenuItemTerms(
                            search_quantity='datasets.doi',
                            options=0,
                        ),
                    ],
                ),
            ],
        ),
        filters_locked={'section_defs.definition_qualified_name': schema},
    ),
)
