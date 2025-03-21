from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    BreakpointEnum,
    Column,
    Dashboard,
    Layout,
    Menu,
    MenuItemCustomQuantities,
    MenuItemHistogram,
    MenuItemTerms,
    SearchQuantities,
    WidgetHistogram,
    WidgetTerms,
)

schema = (
    'nomad_parser_plugins_camels_files.schema_packages.camels_package.CamelsMeasurement'
)

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
            Column(search_quantity=f'data.protocol_name#{schema}', selected=True),
            Column(search_quantity=f'data.session_name#{schema}', selected=True),
            Column(search_quantity=f'data.end_time#{schema}'),
            Column(search_quantity=f'data.protocol_overview#{schema}'),
            Column(search_quantity=f'data.description#{schema}'),
        ],
        # dashboard = Dashboard(
        # widgets=[
        #             WidgetTerms(
        #                 title="Sample name",
        #                 type="terms",
        #                 layout={
        #                     BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
        #                 },
        #                 search_quantity=f"data.samples.name#{schema}"
        #         ),
        #             WidgetTerms(
        #                 title="User",
        #                 type="terms",
        #                 layout={
        #                     BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
        #                 },
        #                 search_quantity=f"data.camels_user#{schema}"
        #         ),
        #         WidgetTerms(
        #             title='Instrument name',
        #             type='terms',
        #             layout={
        #                 BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
        #             },
        #             search_quantity=f'data.instruments.name#{schema}'
        #         ),
        #         WidgetHistogram(
        #             title='Start time',
        #             type='histogram',
        #             layout={
        #                 BreakpointEnum.MD: Layout(h=6, w=6, x=0, y=0)
        #             },
        #             x=f'data.datetime#{schema}'
        #         ),
        #         WidgetTerms(
        #             title='Tags',
        #             type='terms',
        #             layout={
        #                 BreakpointEnum.MD: Layout(h=6, w=4, x=1, y=0)
        #             },
        #             search_quantity=f'results.eln.tags'
        #         ),
        #     ]
        # ),
        menu=Menu(
            items=[
                MenuItemTerms(
                    title='Sample name',
                    type='terms',
                    search_quantity=f'data.samples.name#{schema}',
                ),
                MenuItemHistogram(
                    title='Start time', type='histogram', x=f'data.datetime#{schema}'
                ),
                MenuItemTerms(
                    search_quantity=f'data.protocol_name#{schema}',
                    options=5,
                ),
                MenuItemTerms(
                    search_quantity=f'data.session_name#{schema}',
                    options=5,
                ),
                MenuItemTerms(
                    title='Tags', type='terms', search_quantity='results.eln.tags'
                ),
                MenuItemTerms(
                    title='User',
                    type='terms',
                    search_quantity=f'data.camels_user#{schema}',
                ),
                MenuItemTerms(
                    title='Instrument name',
                    type='terms',
                    search_quantity=f'data.instruments.name#{schema}',
                ),
                MenuItemCustomQuantities(),
            ],
        ),
        filters_locked={'section_defs.definition_qualified_name': schema},
    ),
)
