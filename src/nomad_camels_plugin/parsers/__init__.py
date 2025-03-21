from nomad.config.models.plugins import ParserEntryPoint


class CamelsParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_camels_plugin.parsers.parser import CamelsParser

        return CamelsParser(**self.dict())


camels_parser = CamelsParserEntryPoint(
    name='CamelsParser',
    description='New parser entry point configuration.',
    mainfile_name_re=r'^.*\.(h5|hdf5|nxs)$',
    mainfile_mime_re='(application/x-hdf)',
)
