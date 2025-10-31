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
    MenuItemOption,
    MenuItemTerms,
    SearchQuantities,
    WidgetHistogram,
    WidgetTerms,
)

schema = 'nomad_camels_plugin.schema_packages.camels_package.CamelsMeasurement'
schema_diode = (
    'nomad_camels_plugin.schema_packages.camels_package.CamelsMeasurementDiode'
)
schemas = [f'*#{schema}', f'*#{schema_diode}']

camels_app = AppEntryPoint(
    name='CAMELS App',
    description='App that allows you to search and navigate your CAMELS measurements.',
    app=App(
        label='CAMELS App',
        path='myapp',
        category='Experiment',
        search_quantities=SearchQuantities(include=schemas),
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
        menu=Menu(
            items=[
                MenuItemTerms(
                    title='Sample name',
                    type='terms',
                    search_quantity=
                        f'data.samples.name#{schema}'
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
                    title='Type of Measurement',
                    type='terms',
                    search_quantity='results.eln.sections',
                    options={
                        'CamelsMeasurement': MenuItemOption(label='Camels Measurement'),
                        'CamelsMeasurementDiode': MenuItemOption(
                            label='Camels Measurement Diode'
                        ),
                    },
                ),
                MenuItemTerms(
                    title='Instrument name',
                    type='terms',
                    search_quantity=f'data.instruments.name#{schema}',
                ),
                MenuItemCustomQuantities(),
            ],
        ),
        filters_locked={
            'results.eln.sections': ['CamelsMeasurement', 'CamelsMeasurementDiode']
        },
    ),
)
