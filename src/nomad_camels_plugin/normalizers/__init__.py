from nomad.config.models.plugins import NormalizerEntryPoint
from pydantic import Field


class CamelsNormalizerEntryPoint(NormalizerEntryPoint):
    def load(self):
        from nomad_camels_plugin.normalizers.camels_normalizer import (
            CamelsNormalizer,
        )

        return CamelsNormalizer(**self.dict())


camels_normalizer = CamelsNormalizerEntryPoint(
    name='MyNormalizer',
    description='My custom normalizer.',
)
