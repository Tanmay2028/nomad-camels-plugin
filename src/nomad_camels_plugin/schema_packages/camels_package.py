from nomad.datamodel import Schema
from nomad.datamodel.hdf5 import HDF5Reference
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    Filter,
    SectionProperties,
    H5WebAnnotation,
)
from nomad.datamodel.metainfo.basesections import (
    Measurement,
)
from nomad.metainfo import JSON, Datetime, Quantity, SchemaPackage, Section
from nomad.datamodel.metainfo.plot import PlotSection, PlotlyFigure
m_package = SchemaPackage()
import numpy as np


class CamelsMeasurement(Measurement, PlotSection, Schema):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=['location', 'lab_id', 'description'],
                ),
                order=[
                    'name',
                    'datetime',
                    'end_time',
                    'session_name',
                    'measurement_tags',
                    'measurement_description',
                    'measurement_comments',
                    'protocol_description',
                    'protocol_overview',
                    'protocol_name',
                    'camels_user',
                    'camels_file',
                ],
            )
        ),
        a_h5web=H5WebAnnotation(signal='hdf5_file'),
    )
    measurement_description = Quantity(
        type=str,
        description='Measurement description',
        a_eln=ELNAnnotation(
            component='RichTextEditQuantity',
            label='Measurement description',
        ),
    )
    protocol_description = Quantity(
        type=str,
        description='Protocol description',
        a_eln=ELNAnnotation(
            component='RichTextEditQuantity',
            label='Protocol description',
        ),
    )
    protocol_overview = Quantity(
        type=str,
        description='Protocol overview',
        a_eln=ELNAnnotation(
            component='RichTextEditQuantity',
            label='Protocol overview',
        ),
    )
    protocol_json = Quantity(
        type=JSON,
        description='Protocol JSON',
    )
    measurement_comments = Quantity(
        type=str,
        description='Measurement comments',
        a_eln=ELNAnnotation(
            component='RichTextEditQuantity',
            label='Measurement comments',
        ),
    )
    measurement_tags = Quantity(
        type=str,
        shape=['*'],
        description='Measurement tags',
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
            label='Tags',
        ),
    )
    protocol_name = Quantity(
        type=str,
        description='Protocol name',
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
            label='Protocol name',
        ),
    )
    end_time = Quantity(
        type=Datetime,
        description='Measurement end time',
        a_eln=dict(component='DateTimeEditQuantity', label='Measurement end time'),
    )
    session_name = Quantity(
        type=str,
        description='Session name',
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
            label='Session name',
        ),
    )
    camels_user = Quantity(
        type=str,
        description='CAMELS User',
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
            label='CAMELS User',
        ),
    )
    camels_file = Quantity(
        type=str,
        description='CAMELS file reference',
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor', label='camels file ref'),
    )
    camels_python_script = Quantity(
        type=str,
        description='CAMELS Python script reference',
    )
    camels_instrument_settings = Quantity(
        type=JSON,
        description='CAMELS instrument settings',
    )
    hdf5_file = Quantity(
        type=HDF5Reference,
    )

    def normalize(self, archive, logger: 'BoundLogger') -> None:
        """
        The normalizer that populates results.eln.tags with the tags that were added with the parser.
        This is done because the data.measurement_tags are not searchable in the CAMELS App, but they can be modified and viewed in the entry.
        The results.eln.tags are searchable/usable in the CAMELS App.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger ('BoundLogger'): A structlog logger.
        """
        super(CamelsMeasurement, self).normalize(archive, logger)
        archive.results.eln.tags = archive.data.measurement_tags

class CamelsMeasurementDiode(CamelsMeasurement):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=['location', 'lab_id', 'description'],
                ),
                order=[
                    'name',
                    'datetime',
                    'figures',
                    'hdf5_file',
                    'threshold_voltage',
                    'serial_resistance',
                    'end_time',
                    'session_name',
                    'measurement_tags',
                    'measurement_description',
                    'measurement_comments',
                    'protocol_description',
                    'protocol_overview',
                    'protocol_name',
                    'camels_user',
                    'camels_file',
                ],
            )
        ),
        a_h5web=H5WebAnnotation(signal='hdf5_file'),
    )
    threshold_voltage = Quantity(
        type=np.float64,
        unit='volt',
        description='Minimum forward voltage a diode requires to begin conducting current.',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            label='Diode threshold voltage',
            defaultDisplayUnit='volt',
        ),
    )
    serial_resistance = Quantity(
        type=np.float64,
        unit='ohm',
        description='Series resistance of the diode.',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            label='Diode serial resistance',
            defaultDisplayUnit='ohm',
        ),
    )



m_package.__init_metainfo__()
