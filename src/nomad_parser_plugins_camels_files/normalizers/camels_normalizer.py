from typing import Dict

from nomad.datamodel import EntryArchive
from nomad.normalizing import Normalizer


class CamelsNormalizer(Normalizer):
    def normalize(
        self,
        archive: EntryArchive,
        logger=None,
    ) -> None:
        logger.info('This normalizer does nothing at the moment. Functionality might be added in the future.')
