from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class CamelsParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_parser_plugins_camels_files.parsers.parser import CamelsParser

        return CamelsParser(**self.dict())


camels_parser_entry_point = CamelsParserEntryPoint(
    name='CamelsParser',
    description='New parser entry point configuration.',
    mainfile_name_re=r'^.*\.(h5|hdf5|nxs)$',
    mainfile_mime_re='(application/x-hdf)',
)
