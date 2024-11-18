from nomad.config.models.plugins import ParserEntryPoint, SchemaPackageEntryPoint


class CamelsParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_parser_plugins_camels_files.parsers.parser import CamelsParser

        return CamelsParser(**self.dict())


camels_parser = CamelsParserEntryPoint(
    name='CamelsParser',
    description='New parser entry point configuration.',
    mainfile_name_re=r'^.*\.(h5|hdf5|nxs)$',
    mainfile_mime_re='(application/x-hdf)',
)


class CamelsSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_parser_plugins_camels_files.parsers.parser import m_package

        return m_package


camels_schema_package = CamelsSchemaPackageEntryPoint(
    name='CamelsSchemaPackage',
    description='Contains the data model for recording NOMAD Camels entries.',
)
