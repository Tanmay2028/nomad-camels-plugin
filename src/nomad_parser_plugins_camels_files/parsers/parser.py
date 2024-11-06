from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.parsing.parser import MatchingParser
from nomad.datamodel.metainfo.basesections import Experiment
from nomad.datamodel import EntryData
from nomad.metainfo import Quantity

from nomad.datamodel.hdf5 import HDF5Reference

import os

configuration = config.get_plugin_entry_point(
    'nomad_parser_plugins_camels_files.parsers:camels_parser_entry_point'
)

class CamelsData(Experiment, EntryData):
    quantity = Quantity(
        type=HDF5Reference,
        description='test data reference',
    )



class CamelsParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        self.archive = archive
        self._logger = logger if logger else get_logger(__name__)
        *_, self._fname = mainfile.rsplit("/", 1)
        data = CamelsData()
        data.quantity = f'{os.path.basename(mainfile)}#/CAMELS_KAUST/data/Simple_Sweep/ElapsedTime'




