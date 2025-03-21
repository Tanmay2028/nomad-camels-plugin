from pydantic import Field
from nomad.config.models.plugins import NormalizerEntryPoint


class CamelsNormalizerEntryPoint(NormalizerEntryPoint):

    def load(self):
        from nomad_parser_plugins_camels_files.normalizers.camels_normalizer import CamelsNormalizer

        return CamelsNormalizer(**self.dict())


camels_normalizer = CamelsNormalizerEntryPoint(
    name = 'MyNormalizer',
    description = 'My custom normalizer.',
)