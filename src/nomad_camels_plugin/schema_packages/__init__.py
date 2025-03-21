from nomad.config.models.plugins import SchemaPackageEntryPoint


class CamelsSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_camels_plugin.schema_packages.camels_package import m_package

        return m_package

camels_schema_package = CamelsSchemaPackageEntryPoint(
    name='CamelsSchemaPackage',
    description='Contains the data model for recording NOMAD Camels entries.',
)