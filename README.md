# NOMAD CAMELS Plugin

Plugin for HDF5 (`.h5`) measurement files coming from NOMAD CAMELS.

It provides a data schema, parser and Search App for CAMELS measurement files. This allows you to immeadiatly search and filter your measurmeent data after uploading it to your NOMAD instance.

The following information from the measurement file is parsed and made searchable:

- Name of the datafile (not including the `.h5` ending)
- Measurement starting time (time the measurement was started)
- Measurement end time (time the measurement was ended)
- Session
- Tags (as a list)
- Measurement description
- Measurement comments
- Protocol description
- Protocol overview
- Protocol name
- User
- Sample

It can reference the user and sample if they are also entries in your NOMAD instance and are assigned in CAMELS before you perform the measurement (for this you must first login into NOMAD in CAMELS).

## Adding this plugin to NOMAD

Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/docs/howto/plugins/plugins.html) for all details on how to generally deploy plugins on your NOMAD instance.

You should add the `nomad-camels-plugin` to your `nomad.yaml` dependencies(or `pyproject.toml` for local development):

```yaml
dependencies = [
  "nomad-camels-plugin==0.1.8",
]
```

## Main contributors
| Name | E-mail     |
|------|------------|
|NOMAD CAMELS Development Team| [nomad-camels@fau.de](mailto:nomad-camels@fau.de)
