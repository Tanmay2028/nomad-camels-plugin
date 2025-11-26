from collections.abc import Iterable
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

import json
import os
import re
from datetime import datetime

import h5py
import nomad_camels_toolbox as nct
import numpy as np
from nomad.config import config
from nomad.datamodel.datamodel import EntryMetadata
from nomad.datamodel.metainfo.basesections import (
    CompositeSystemReference,
    InstrumentReference,
)
from nomad.datamodel.metainfo.plot import PlotlyFigure
from nomad.parsing.parser import MatchingParser

from nomad_camels_plugin.schema_packages.camels_package import (
    CamelsMeasurement,
    CamelsMeasurementDiode,
)

from .utils import create_archive


class CamelsParser(MatchingParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mainfile_mime_re = re.compile('(application/x-hdf)')
        self._mainfile_name_re = re.compile(r'^.*\.(h5|hdf5|nxs)$')

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
        testing: bool = False,
        schema_to_use=CamelsMeasurement,
    ) -> None:
        self.archive = archive
        *_, self._fname = mainfile.rsplit('/', 1)
        data = schema_to_use()
        # Get name from file name, remove file ending
        data.name = f'{os.path.splitext(os.path.basename(mainfile))[0]}'

        with h5py.File(mainfile, 'r') as hdf5_file:
            # Get the first entry of the file. Should be the entry created by CAMELS
            self.camels_entry_name = list(hdf5_file.keys())[0]
            # Check to make sure the file is a CAMELS file

            # Get start time from the file
            start_time_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'start_time'
            ][()]
            start_time_str = start_time_bytes.decode(
                'utf-8'
            )  # Decode byte string to regular string
            data.datetime = datetime.fromisoformat(start_time_str)

            # Get protocol description from the file
            description_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['protocol_description'][()]
            # Decode byte string to regular string
            # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
            data.protocol_description = (
                description_bytes.decode('utf-8')
                .replace('\n', '<br>')
                .replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                )  # Replace tabs with four non-breaking spaces
                .replace(' ', '&nbsp;')
            )

            # Get measurement description from the file
            description_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['measurement_description'][()]
            # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
            data.measurement_description = (
                description_bytes.decode('utf-8')
                .replace('\n', '<br>')
                .replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                )  # Replace tabs with four non-breaking spaces
                .replace(' ', '&nbsp;')
            )

            # Get measurement tags from the file
            tags_bytes_list = hdf5_file[self.camels_entry_name]['measurement_details'][
                'measurement_tags'
            ][()]
            tags_string_list = [item.decode('utf-8') for item in tags_bytes_list]
            # Get the separated tags, can be white space, comma, semicolon, or newline separated
            data.measurement_tags = tags_string_list

            # Get measurement comments from the file
            if (
                'measurement_comments'
                not in hdf5_file[self.camels_entry_name]['measurement_details']
            ):
                data.measurement_comments = ''
            else:
                comments_bytes = hdf5_file[self.camels_entry_name][
                    'measurement_details'
                ]['measurement_comments'][()]
                # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
                data.measurement_comments = (
                    comments_bytes.decode('utf-8')
                    .replace('\n', '<br>')
                    .replace(
                        '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                    )  # Replace tabs with four non-breaking spaces
                    .replace(' ', '&nbsp;')
                )

            # Get protocol overview from the file
            protocol_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'protocol_overview'
            ][()]
            # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
            data.protocol_overview = (
                protocol_bytes.decode('utf-8')
                .replace('\n', '<br>')
                .replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                )  # Replace tabs with four non-breaking spaces
                .replace(' ', '&nbsp;')
            )

            # Get plan name from the file
            protocol_name_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['plan_name'][()]
            data.protocol_name = protocol_name_bytes.decode('utf-8').removesuffix(
                '_plan'
            )

            # Get protocol json from the file
            protocol_json_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['protocol_json'][()]
            data.protocol_json = json.loads(protocol_json_bytes.decode('utf-8'))

            # Get the end time from the file
            end_time_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'end_time'
            ][()]
            end_time_str = end_time_bytes.decode('utf-8')
            data.end_time = datetime.fromisoformat(end_time_str)

            # Get the session name from the file
            session_name_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['session_name'][()]
            data.session_name = session_name_bytes.decode('utf-8')
            print(data.session_name)

            # Get the user from the file

            # Reference the sample by getting sample and upload id and adding it to the default data.sample
            try:
                sample_name = hdf5_file[self.camels_entry_name]['sample']['name'][
                    ()
                ].decode('utf-8')
            except KeyError:
                logger.warning('No sample name found in the CAMELS file')
                sample_name = ''
            try:
                sample_id_bytes = hdf5_file[self.camels_entry_name]['sample'][
                    'identifier'
                ]['full_identifier'][()]
                sample_id = sample_id_bytes.decode('utf-8')
                # Extract the upload id and entry id from the full sample id
                sample_upload_id, sample_entry_id = re.findall(
                    r'upload/id/([^/]+)/entry/id/([^/]+)', sample_id
                )[0]

                sample_name = hdf5_file[self.camels_entry_name]['sample']['name'][
                    ()
                ].decode('utf-8')

                data.samples = [
                    CompositeSystemReference(
                        name=f'{sample_name}',
                        reference=f'../uploads/{sample_upload_id}/archive/{sample_entry_id}#/data',
                    )
                ]
            except KeyError:
                logger.warning('No NOMAD sample found in the CAMELS file')
                try:
                    sample_id_bytes = hdf5_file[self.camels_entry_name]['sample'][
                        'sample_id'
                    ][()]
                    # Check to see if sample_id_bytes is an int
                    if isinstance(sample_id_bytes, int) or isinstance(
                        sample_id_bytes, np.int64
                    ):
                        sample_id = str(sample_id_bytes)
                    else:
                        sample_id = sample_id_bytes.decode('utf-8')
                    sample_name_bytes = hdf5_file[self.camels_entry_name]['sample'][
                        'name'
                    ][()]
                    if isinstance(sample_name_bytes, int) or isinstance(
                        sample_name_bytes, np.int64
                    ):
                        sample_name = str(sample_name_bytes)
                    else:
                        sample_name = sample_name_bytes.decode('utf-8')
                    # Extract the upload id and entry id from the full sample id
                    if len(sample_id) == 0:
                        data.samples = [
                            CompositeSystemReference(
                                name=f'{sample_name}',
                            )
                        ]
                    else:
                        data.samples = [
                            CompositeSystemReference(
                                name=f'{sample_name} ID:{sample_id}',
                            )
                        ]
                except KeyError:
                    data.samples = [
                        CompositeSystemReference(
                            name=f'{sample_name}',
                        )
                    ]
                    logger.warning(
                        'No sample found in the NOMAD server. Only using the sample name.'
                    )

            # Reference all the instruments that were used in the measurement
            # First get a list of all the instrument IDs
            instruments = hdf5_file[self.camels_entry_name]['instruments'].keys()
            for instrument_name in instruments:
                # First check if ELN-metadata exists
                if (
                    'fabrication'
                    not in hdf5_file[self.camels_entry_name]['instruments'][
                        instrument_name
                    ]
                    or 'ELN-metadata'
                    not in hdf5_file[self.camels_entry_name]['instruments'][
                        instrument_name
                    ]['fabrication']
                    or 'full_identifier'
                    not in hdf5_file[self.camels_entry_name]['instruments'][
                        instrument_name
                    ]['fabrication']['ELN-metadata']
                ):
                    data.instruments.append(
                        InstrumentReference(
                            name=instrument_name,
                        )
                    )
                else:
                    full_identifier_bytes = hdf5_file[self.camels_entry_name][
                        'instruments'
                    ][instrument_name]['fabrication']['ELN-metadata'][
                        'full_identifier'
                    ][()]
                    full_identifier_string = full_identifier_bytes.decode('utf-8')
                    instrument_upload_id, instrument_entry_id = re.findall(
                        r'upload/id/([^/]+)/entry/id/([^/]+)', full_identifier_string
                    )[0]
                    data.instruments.append(
                        InstrumentReference(
                            name=instrument_name,
                            reference=f'../uploads/{instrument_upload_id}/archive/{instrument_entry_id}#/data',
                        )
                    )

            # Get the instrument settings from the file
            settings_dict = {}  # Dictionary to hold all instruments and their settings

            instruments = hdf5_file[self.camels_entry_name]['instruments'].keys()
            for instrument_name in instruments:
                settings_dict[
                    instrument_name
                ] = {}  # Initialize a dict for this instrument's settings
                settings_keys = hdf5_file[self.camels_entry_name]['instruments'][
                    instrument_name
                ]['settings'].keys()
                for key in settings_keys:
                    # Check if the object is of kind group
                    if isinstance(
                        hdf5_file[self.camels_entry_name]['instruments'][
                            instrument_name
                        ]['settings'][key],
                        h5py.Group,
                    ):
                        settings_dict[instrument_name][
                            key
                        ] = {}  # Initialize a dict for this key
                        # Get each element in the group
                        for sub_key in hdf5_file[self.camels_entry_name]['instruments'][
                            instrument_name
                        ]['settings'][key].keys():
                            settings_value = hdf5_file[self.camels_entry_name][
                                'instruments'
                            ][instrument_name]['settings'][key][sub_key][()]

                            # Convert numpy scalar to Python type if needed
                            if (
                                hasattr(settings_value, 'shape')
                                and settings_value.shape == ()
                            ):
                                settings_value = settings_value.item()

                            # If we have a list or array, decode each element if needed
                            if isinstance(settings_value, np.ndarray):
                                # If it's a single-element array
                                if settings_value.size == 1:
                                    settings_value = settings_value.item()
                                else:
                                    # Handle multi-element arrays here
                                    decoded_list = []
                                    for val in settings_value:
                                        if isinstance(val, bytes):
                                            val = val.decode('utf-8')
                                        val = try_convert_to_number(val)
                                        decoded_list.append(val)
                                    settings_value = (
                                        decoded_list
                                        if len(decoded_list) > 1
                                        else decoded_list[0]
                                    )
                            else:
                                # If it's already a Python type, just continue
                                # This includes the later logic you have for single values
                                if isinstance(settings_value, bytes):
                                    settings_value = settings_value.decode('utf-8')
                                settings_value = try_convert_to_number(settings_value)

                            settings_dict[instrument_name][key][sub_key] = (
                                settings_value
                            )
                    else:
                        settings_value = hdf5_file[self.camels_entry_name][
                            'instruments'
                        ][instrument_name]['settings'][key][()]
                        # Decode if bytes
                        if isinstance(settings_value, bytes):
                            settings_value = settings_value.decode('utf-8')
                        # Try to convert to number if possible
                        settings_value = try_convert_to_number(settings_value)

                        settings_dict[instrument_name][key] = settings_value

            # Convert the entire dictionary to a JSON string
            def ensure_str(obj):
                if isinstance(obj, dict):
                    return {k: ensure_str(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [ensure_str(i) for i in obj]
                elif isinstance(obj, bytes):
                    return obj.decode('utf-8')
                elif isinstance(obj, np.ndarray):
                    return ensure_str(obj.tolist())
                else:
                    return obj

            settings_dict = ensure_str(settings_dict)
            data.camels_instrument_settings = settings_dict

            # Add the CAMELS data file to the entry
            camels_file_path = re.search(r'/raw/(.*)', mainfile)
            data.camels_file = camels_file_path.group(1)

            # Get the user with the user id from the file
            try:
                user_id_bytes = hdf5_file[self.camels_entry_name]['user']['identifier'][
                    'identifier'
                ][()]
                user_id_string = user_id_bytes.decode('utf-8')
                import requests

                url = f'{config.api_url()}/v1/users?user_id={user_id_string}'
                headers = {
                    'accept': 'application/json',
                }

                response = requests.get(
                    url,
                    headers=headers,
                )

                if response.status_code == 200:
                    response_dict = response.json()
                    if 'data' in response_dict and len(response_dict['data']) > 0:
                        first_name = response_dict['data'][0].get('first_name', '')
                        last_name = response_dict['data'][0].get('last_name', '')
                    else:
                        raise KeyError('No user found with the given user id')
                else:
                    raise Exception(
                        f'Error while fetching user data from the database.\nStatus code: {response.status_code}'
                    )

                data.camels_user = f'{first_name} {last_name}'

            except KeyError:
                logger.warning('No NOMAD user found in the CAMELS file')
                user_id_bytes = hdf5_file[self.camels_entry_name]['user']['name'][()]
                if isinstance(user_id_bytes, int) or isinstance(
                    user_id_bytes, np.int64
                ):
                    user_id_string = user_id_bytes.decode('utf-8')
                else:
                    user_id_string = user_id_bytes.decode('utf-8')
                data.camels_user = user_id_string

            except Exception as e:
                logger.warning(f'Error while fetching user data from the database: {e}')
                user_id_bytes = hdf5_file[self.camels_entry_name]['user']['name'][()]
                if isinstance(user_id_bytes, int) or isinstance(
                    user_id_bytes, np.int64
                ):
                    user_id_string = user_id_bytes.decode('utf-8')
                else:
                    user_id_string = user_id_bytes.decode('utf-8')
                data.camels_user = user_id_string

            # Get the python script that was used to generate the data
            try:
                python_script_bytes = hdf5_file[self.camels_entry_name][
                    'measurement_details'
                ]['python_script'][()]
                data.camels_python_script = python_script_bytes.decode('utf-8')
            except KeyError:
                logger.warning('No python script found in the CAMELS file')
            # Get the actual file path inside the NOMAD files system where you uploaded the file
            path_in_filesystem = mainfile.split('/raw/')[1]
            print('Path in filesystem: ', path_in_filesystem)
            data.hdf5_file = f'{path_in_filesystem}#/{self.camels_entry_name}/data'
        plots_from_hdf5 = nct.recreate_plots(mainfile, show_figures=False)
        # plot_from_hdf5 = plots_from_hdf5[list(plots_from_hdf5.keys())[0]]
        for plot_from_hdf5 in plots_from_hdf5.values():
            data.figures.append(PlotlyFigure(figure=plot_from_hdf5.to_plotly_json()))
        # -------------------------------
        # This adds all the data to the .nxs file itself, uncomment if you dont want to have two seperate files.
        # self.archive.data = data
        # -------------------------------

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # This creates a seperate .archive.yaml file for the data
        if not testing:
            from nomad.datamodel.datamodel import EntryArchive

            camels_data_archive = EntryArchive(
                data=data,
                metadata=EntryMetadata(upload_id=archive.m_context.upload_id),
            )
            filetype = 'json'
            filename = f'{self._fname}.archive.{filetype}'
            create_archive(
                camels_data_archive.m_to_dict(),
                archive.m_context,
                filename,
                filetype,
                logger,
            )
        else:
            return data
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def is_mainfile(
        self,
        filename: str,
        mime: str,
        buffer: bytes,
        decoded_buffer: str,
        compression: str = None,
    ) -> Union[bool, Iterable[str]]:
        # First, run the parent's method.
        result = super().is_mainfile(
            filename, mime, buffer, decoded_buffer, compression
        )
        # If the parent's method returns False (or any value indicating a failure), return immediately.
        if not result:
            return result
        try:
            with h5py.File(filename, 'r') as f:
                # The attribute might be bytes, so decode if necessary
                file_type_value = f.attrs.get('file_type')
                if file_type_value is None:
                    print('\nNo file_type attribute found in the file.')
                    # Check to see if the file is a legacy CAMELS file
                    # Check if CAMELS_ is in any of the top level keys of the HDF5 file
                    if any('CAMELS_' in key for key in f.keys()):
                        print("File is an older 'NOMAD CAMELS' file.")
                        return True
                    else:
                        print("File is not a 'NOMAD CAMELS' file.")
                    return False
        except Exception as e:
            print(f'\nError while checking file type: {e}')
            return False
        if file_type_value == 'NOMAD CAMELS':
            with h5py.File(filename, 'r') as f:
                for key in f.keys():
                    if 'CAMELS_' in key:
                        print(f'Found CAMELS key: {key}')
                        camels_key = key
                        break
                print(
                    'Tags: ', f[f'{camels_key}/measurement_details/measurement_tags'][:]
                )
                if (
                    b'diode'
                    in f[f'{camels_key}/measurement_details/measurement_tags'][:]
                    and b'demo'
                    in f[f'{camels_key}/measurement_details/measurement_tags'][:]
                ):
                    print(
                        'This is a special diode demo measurement and has its own entry. now returning false'
                    )
                    return False
            print("File is a 'NOMAD CAMELS' file.")
            return True
        else:
            print("file type is not 'NOMAD CAMELS', but: ", file_type_value)
            return False


class CamelsParserDiode(CamelsParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
        testing: bool = False,
        schema_to_use=CamelsMeasurementDiode,
    ) -> None:
        self.archive = archive
        *_, self._fname = mainfile.rsplit('/', 1)
        data = schema_to_use()
        # Get name from file name, remove file ending
        data.name = f'{os.path.splitext(os.path.basename(mainfile))[0]}'

        with h5py.File(mainfile, 'r') as hdf5_file:
            # Get the first entry of the file. Should be the entry created by CAMELS
            self.camels_entry_name = list(hdf5_file.keys())[0]
            # Check to make sure the file is a CAMELS file

            # Get start time from the file
            start_time_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'start_time'
            ][()]
            start_time_str = start_time_bytes.decode(
                'utf-8'
            )  # Decode byte string to regular string
            data.datetime = datetime.fromisoformat(start_time_str)

            # Get protocol description from the file
            description_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['protocol_description'][()]
            # Decode byte string to regular string
            # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
            data.protocol_description = (
                description_bytes.decode('utf-8')
                .replace('\n', '<br>')
                .replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                )  # Replace tabs with four non-breaking spaces
                .replace(' ', '&nbsp;')
            )

            # Get measurement description from the file
            description_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['measurement_description'][()]
            # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
            data.measurement_description = (
                description_bytes.decode('utf-8')
                .replace('\n', '<br>')
                .replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                )  # Replace tabs with four non-breaking spaces
                .replace(' ', '&nbsp;')
            )

            # Get measurement tags from the file
            tags_bytes_list = hdf5_file[self.camels_entry_name]['measurement_details'][
                'measurement_tags'
            ][()]
            tags_string_list = [item.decode('utf-8') for item in tags_bytes_list]
            # Get the separated tags, can be white space, comma, semicolon, or newline separated
            data.measurement_tags = tags_string_list

            # Get measurement comments from the file
            if (
                'measurement_comments'
                not in hdf5_file[self.camels_entry_name]['measurement_details']
            ):
                data.measurement_comments = ''
            else:
                comments_bytes = hdf5_file[self.camels_entry_name][
                    'measurement_details'
                ]['measurement_comments'][()]
                # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
                data.measurement_comments = (
                    comments_bytes.decode('utf-8')
                    .replace('\n', '<br>')
                    .replace(
                        '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                    )  # Replace tabs with four non-breaking spaces
                    .replace(' ', '&nbsp;')
                )

            # Get protocol overview from the file
            protocol_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'protocol_overview'
            ][()]
            # encode the spaces and new line characters in HTML so that the richtext field displays them correctly
            data.protocol_overview = (
                protocol_bytes.decode('utf-8')
                .replace('\n', '<br>')
                .replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'
                )  # Replace tabs with four non-breaking spaces
                .replace(' ', '&nbsp;')
            )

            # Get plan name from the file
            protocol_name_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['plan_name'][()]
            data.protocol_name = protocol_name_bytes.decode('utf-8').removesuffix(
                '_plan'
            )

            # Get protocol json from the file
            protocol_json_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['protocol_json'][()]
            data.protocol_json = json.loads(protocol_json_bytes.decode('utf-8'))

            # Get the end time from the file
            end_time_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'end_time'
            ][()]
            end_time_str = end_time_bytes.decode('utf-8')
            data.end_time = datetime.fromisoformat(end_time_str)

            # Get the session name from the file
            session_name_bytes = hdf5_file[self.camels_entry_name][
                'measurement_details'
            ]['session_name'][()]
            data.session_name = session_name_bytes.decode('utf-8')
            print(data.session_name)

            # Get the user from the file

            # Reference the sample by getting sample and upload id and adding it to the default data.sample
            try:
                sample_name = hdf5_file[self.camels_entry_name]['sample']['name'][
                    ()
                ].decode('utf-8')
            except KeyError:
                logger.warning('No sample name found in the CAMELS file')
                sample_name = ''
            try:
                sample_id_bytes = hdf5_file[self.camels_entry_name]['sample'][
                    'identifier'
                ]['full_identifier'][()]
                sample_id = sample_id_bytes.decode('utf-8')
                # Extract the upload id and entry id from the full sample id
                sample_upload_id, sample_entry_id = re.findall(
                    r'upload/id/([^/]+)/entry/id/([^/]+)', sample_id
                )[0]

                sample_name = hdf5_file[self.camels_entry_name]['sample']['name'][
                    ()
                ].decode('utf-8')

                data.samples = [
                    CompositeSystemReference(
                        name=f'{sample_name}',
                        reference=f'../uploads/{sample_upload_id}/archive/{sample_entry_id}#/data',
                    )
                ]
            except KeyError:
                logger.warning('No NOMAD sample found in the CAMELS file')
                try:
                    sample_id_bytes = hdf5_file[self.camels_entry_name]['sample'][
                        'sample_id'
                    ][()]
                    # Check to see if sample_id_bytes is an int
                    if isinstance(sample_id_bytes, int) or isinstance(
                        sample_id_bytes, np.int64
                    ):
                        sample_id = str(sample_id_bytes)
                    else:
                        sample_id = sample_id_bytes.decode('utf-8')
                    sample_name_bytes = hdf5_file[self.camels_entry_name]['sample'][
                        'name'
                    ][()]
                    if isinstance(sample_name_bytes, int) or isinstance(
                        sample_name_bytes, np.int64
                    ):
                        sample_name = str(sample_name_bytes)
                    else:
                        sample_name = sample_name_bytes.decode('utf-8')
                    # Extract the upload id and entry id from the full sample id
                    if len(sample_id) == 0:
                        data.samples = [
                            CompositeSystemReference(
                                name=f'{sample_name}',
                            )
                        ]
                    else:
                        data.samples = [
                            CompositeSystemReference(
                                name=f'{sample_name} ID:{sample_id}',
                            )
                        ]
                except KeyError:
                    data.samples = [
                        CompositeSystemReference(
                            name=f'{sample_name}',
                        )
                    ]
                    logger.warning(
                        'No sample found in the NOMAD server. Only using the sample name.'
                    )

            # Reference all the instruments that were used in the measurement
            # First get a list of all the instrument IDs
            instruments = hdf5_file[self.camels_entry_name]['instruments'].keys()
            for instrument_name in instruments:
                # First check if ELN-metadata exists
                if (
                    'fabrication'
                    not in hdf5_file[self.camels_entry_name]['instruments'][
                        instrument_name
                    ]
                    or 'ELN-metadata'
                    not in hdf5_file[self.camels_entry_name]['instruments'][
                        instrument_name
                    ]['fabrication']
                    or 'full_identifier'
                    not in hdf5_file[self.camels_entry_name]['instruments'][
                        instrument_name
                    ]['fabrication']['ELN-metadata']
                ):
                    data.instruments.append(
                        InstrumentReference(
                            name=instrument_name,
                        )
                    )
                else:
                    full_identifier_bytes = hdf5_file[self.camels_entry_name][
                        'instruments'
                    ][instrument_name]['fabrication']['ELN-metadata'][
                        'full_identifier'
                    ][()]
                    full_identifier_string = full_identifier_bytes.decode('utf-8')
                    instrument_upload_id, instrument_entry_id = re.findall(
                        r'upload/id/([^/]+)/entry/id/([^/]+)', full_identifier_string
                    )[0]
                    data.instruments.append(
                        InstrumentReference(
                            name=instrument_name,
                            reference=f'../uploads/{instrument_upload_id}/archive/{instrument_entry_id}#/data',
                        )
                    )

            # Get the instrument settings from the file
            settings_dict = {}  # Dictionary to hold all instruments and their settings

            instruments = hdf5_file[self.camels_entry_name]['instruments'].keys()
            for instrument_name in instruments:
                settings_dict[
                    instrument_name
                ] = {}  # Initialize a dict for this instrument's settings
                settings_keys = hdf5_file[self.camels_entry_name]['instruments'][
                    instrument_name
                ]['settings'].keys()
                for key in settings_keys:
                    # Check if the object is of kind group
                    if isinstance(
                        hdf5_file[self.camels_entry_name]['instruments'][
                            instrument_name
                        ]['settings'][key],
                        h5py.Group,
                    ):
                        settings_dict[instrument_name][
                            key
                        ] = {}  # Initialize a dict for this key
                        # Get each element in the group
                        for sub_key in hdf5_file[self.camels_entry_name]['instruments'][
                            instrument_name
                        ]['settings'][key].keys():
                            settings_value = hdf5_file[self.camels_entry_name][
                                'instruments'
                            ][instrument_name]['settings'][key][sub_key][()]

                            # Convert numpy scalar to Python type if needed
                            if (
                                hasattr(settings_value, 'shape')
                                and settings_value.shape == ()
                            ):
                                settings_value = settings_value.item()

                            # If we have a list or array, decode each element if needed
                            if isinstance(settings_value, np.ndarray):
                                # If it's a single-element array
                                if settings_value.size == 1:
                                    settings_value = settings_value.item()
                                else:
                                    # Handle multi-element arrays here
                                    decoded_list = []
                                    for val in settings_value:
                                        if isinstance(val, bytes):
                                            val = val.decode('utf-8')
                                        val = try_convert_to_number(val)
                                        decoded_list.append(val)
                                    settings_value = (
                                        decoded_list
                                        if len(decoded_list) > 1
                                        else decoded_list[0]
                                    )
                            else:
                                # If it's already a Python type, just continue
                                # This includes the later logic you have for single values
                                if isinstance(settings_value, bytes):
                                    settings_value = settings_value.decode('utf-8')
                                settings_value = try_convert_to_number(settings_value)

                            settings_dict[instrument_name][key][sub_key] = (
                                settings_value
                            )
                    else:
                        settings_value = hdf5_file[self.camels_entry_name][
                            'instruments'
                        ][instrument_name]['settings'][key][()]
                        # Decode if bytes
                        if isinstance(settings_value, bytes):
                            settings_value = settings_value.decode('utf-8')
                        # Try to convert to number if possible
                        settings_value = try_convert_to_number(settings_value)

                        settings_dict[instrument_name][key] = settings_value

            # Convert the entire dictionary to a JSON string
            def ensure_str(obj):
                if isinstance(obj, dict):
                    return {k: ensure_str(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [ensure_str(i) for i in obj]
                elif isinstance(obj, bytes):
                    return obj.decode('utf-8')
                elif isinstance(obj, np.ndarray):
                    return ensure_str(obj.tolist())
                else:
                    return obj

            settings_dict = ensure_str(settings_dict)
            data.camels_instrument_settings = settings_dict

            # Add the CAMELS data file to the entry
            camels_file_path = re.search(r'/raw/(.*)', mainfile)
            data.camels_file = camels_file_path.group(1)

            # Get the user with the user id from the file
            try:
                user_id_bytes = hdf5_file[self.camels_entry_name]['user']['identifier'][
                    'identifier'
                ][()]
                user_id_string = user_id_bytes.decode('utf-8')
                import requests

                url = f'{config.api_url()}/v1/users?user_id={user_id_string}'
                headers = {
                    'accept': 'application/json',
                }

                response = requests.get(
                    url,
                    headers=headers,
                )

                if response.status_code == 200:
                    response_dict = response.json()
                    if 'data' in response_dict and len(response_dict['data']) > 0:
                        first_name = response_dict['data'][0].get('first_name', '')
                        last_name = response_dict['data'][0].get('last_name', '')
                    else:
                        raise KeyError('No user found with the given user id')
                else:
                    raise Exception(
                        f'Error while fetching user data from the database.\nStatus code: {response.status_code}'
                    )

                data.camels_user = f'{first_name} {last_name}'

            except KeyError:
                logger.warning('No NOMAD user found in the CAMELS file')
                user_id_bytes = hdf5_file[self.camels_entry_name]['user']['name'][()]
                if isinstance(user_id_bytes, int) or isinstance(
                    user_id_bytes, np.int64
                ):
                    user_id_string = user_id_bytes.decode('utf-8')
                else:
                    user_id_string = user_id_bytes.decode('utf-8')
                data.camels_user = user_id_string

            except Exception as e:
                logger.warning(f'Error while fetching user data from the database: {e}')
                user_id_bytes = hdf5_file[self.camels_entry_name]['user']['name'][()]
                if isinstance(user_id_bytes, int) or isinstance(
                    user_id_bytes, np.int64
                ):
                    user_id_string = user_id_bytes.decode('utf-8')
                else:
                    user_id_string = user_id_bytes.decode('utf-8')
                data.camels_user = user_id_string

            # Get the python script that was used to generate the data
            try:
                python_script_bytes = hdf5_file[self.camels_entry_name][
                    'measurement_details'
                ]['python_script'][()]
                data.camels_python_script = python_script_bytes.decode('utf-8')
            except KeyError:
                logger.warning('No python script found in the CAMELS file')

            data.hdf5_file = f'CAMELS_data/{sample_name}/{self._fname}#/{self.camels_entry_name}/data'
        plots_from_hdf5 = nct.recreate_plots(mainfile, show_figures=False)
        for plot_from_hdf5 in plots_from_hdf5.values():
            x_data = np.array(plot_from_hdf5['data'][0]['x'])
            y_data = np.array(plot_from_hdf5['data'][0]['y'])
            max_yvalue = max(y_data)
            mask = y_data > 0.7 * max_yvalue
            fit_result = np.polyfit(x_data[mask], y_data[mask], 1)
            slope = fit_result[0]
            intercept = fit_result[1]
            fit_line = slope * np.array(x_data) + intercept
            # calculate the x value where the line crosses y=0
            x_intercept = -intercept / slope
            data.threshold_voltage = x_intercept
            data.serial_resistance = 1 / slope
            plot_from_hdf5.add_trace(
                {
                    'type': 'scatter',
                    'mode': 'lines',
                    'name': 'Fit Line',
                    'x': x_data,
                    'y': fit_line,
                    'line': {'dash': 'dash'},
                }
            )
            data.figures.append(PlotlyFigure(figure=plot_from_hdf5.to_plotly_json()))

        # -------------------------------
        # This adds all the data to the .nxs file itself, uncomment if you dont want to have two seperate files.
        # self.archive.data = data
        # -------------------------------

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # This creates a seperate .archive.yaml file for the data
        if not testing:
            from nomad.datamodel.datamodel import EntryArchive

            camels_data_archive = EntryArchive(
                data=data,
                metadata=EntryMetadata(upload_id=archive.m_context.upload_id),
            )
            filetype = 'json'
            filename = f'{self._fname}.archive.{filetype}'
            create_archive(
                camels_data_archive.m_to_dict(),
                archive.m_context,
                filename,
                filetype,
                logger,
            )
        else:
            return data
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def is_mainfile(
        self,
        filename: str,
        mime: str,
        buffer: bytes,
        decoded_buffer: str,
        compression: str = None,
    ) -> Union[bool, Iterable[str]]:
        # If the parent's method returns False (or any value indicating a failure), return immediately.
        result = MatchingParser.is_mainfile(
            self, filename, mime, buffer, decoded_buffer, compression
        )
        if not result:
            return result
        try:
            with h5py.File(filename, 'r') as f:
                # The attribute might be bytes, so decode if necessary
                file_type_value = f.attrs.get('file_type')
                if file_type_value is None:
                    print('\nNo file_type attribute found in the file.')
                    # Check to see if the file is a legacy CAMELS file
                    # Check if CAMELS_ is in any of the top level keys of the HDF5 file
                    if any('CAMELS_' in key for key in f.keys()):
                        print("File is an older 'NOMAD CAMELS' file.")
                        return False
                    else:
                        print("File is not a 'NOMAD CAMELS' file.")
                    return False
        except Exception as e:
            print(f'\nError while checking file type: {e}')
            return False
        if file_type_value == 'NOMAD CAMELS':
            with h5py.File(filename, 'r') as f:
                for key in f.keys():
                    if 'CAMELS_' in key:
                        print(f'Found CAMELS key: {key}')
                        camels_key = key
                        break
                print(
                    'Tags: ', f[f'{camels_key}/measurement_details/measurement_tags'][:]
                )
                if (
                    b'diode'
                    in f[f'{camels_key}/measurement_details/measurement_tags'][:]
                    and b'demo'
                    in f[f'{camels_key}/measurement_details/measurement_tags'][:]
                ):
                    print(
                        'This is a special diode measurement will now be parsed by the specialty parser.'
                    )
                    return True
            print("File is a 'NOMAD CAMELS' file.")
            return False
        else:
            print("file type is not 'NOMAD CAMELS', but: ", file_type_value)
            return False


def try_convert_to_number(value):
    # Attempt to convert string to a number (int or float)
    # If it's not numeric, just return the original value.
    try:
        # Try int first
        int_val = int(value)
        return int_val
    except (ValueError, TypeError):
        pass

    try:
        # Try float if int fails
        float_val = float(value)
        return float_val
    except (ValueError, TypeError):
        # If both fail, return original value
        return value
