from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

import os
import re
from datetime import datetime

import h5py
import numpy as np
from nomad.config import config
from nomad.datamodel.datamodel import EntryMetadata
from nomad.datamodel.metainfo.basesections import (
    CompositeSystemReference,
    InstrumentReference,
)
from nomad.parsing.parser import MatchingParser
from nomad_parser_plugins_camels_files.schema_packages.camels_package import CamelsMeasurement
from .utils import create_archive


class CamelsParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        self.archive = archive
        *_, self._fname = mainfile.rsplit('/', 1)
        data = CamelsMeasurement()
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
            description_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'protocol_description'
            ][()]
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
            description_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'measurement_description'
            ][()]
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
            print(tags_bytes_list)
            if len(tags_bytes_list) == 0:
                tags_string_list = []
            else:
                tags_string_list = [item.decode('utf-8') for item in tags_bytes_list]
            # Get the separated tags, can be white space, comma, semicolon, or newline separated
            data.measurement_tags = tags_string_list

            # Get measurement comments from the file
            comments_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'measurement_comments'
            ][()]
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
            plan_name_bytes = hdf5_file[self.camels_entry_name]['measurement_details'][
                'plan_name'
            ][()]
            data.plan_name = plan_name_bytes.decode('utf-8')

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
                sample_id_bytes = hdf5_file[self.camels_entry_name]['sample'][
                    'identifier'
                ]['full_identifier'][()]
                sample_id = sample_id_bytes.decode('utf-8')
                # Extract the upload id and entry id from the full sample id
                sample_upload_id, sample_entry_id = re.findall(
                    r'upload/id/([^/]+)/entry/id/([^/]+)', sample_id
                )[0]
                
                sample_name = hdf5_file[self.camels_entry_name]['sample']['name'][()].decode('utf-8')

                
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
                    logger.warning('No regular sample found in the CAMELS file')

            # Reference all the instruments that were used in the measurement
            # First get a list of all the instrument IDs
            instruments = hdf5_file[self.camels_entry_name]['instruments'].keys()
            for instrument_name in instruments:
                if 'full_identifier' not in hdf5_file[self.camels_entry_name][
                    'instruments'
                ][instrument_name]['fabrication']['ELN-metadata']:
                    data.instruments.append(
                        InstrumentReference(
                            name=instrument_name,
                        )
                    )
                else:
                    full_identifier_bytes = hdf5_file[self.camels_entry_name][
                        'instruments'
                    ][instrument_name]['fabrication']['ELN-metadata']['full_identifier'][()]
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

            # Add the CAMELS data file to the entry
            camels_file_path = re.search(r"/raw/(.*)", mainfile)
            data.camels_file = camels_file_path.group(1)
            # data.camels_file = f'../uploads/{datafile_entry_id}/raw/{self._fname}'
            # data.camels_file = f'../CAMELS_data/{sample_name}/{self._fname}'
            # /uploads/{upload_id}/archive/{entry_id}#/run/0/calculation/1  # same NOMAD

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
                        raise Exception('No user found with the given user id')
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

            # Get the python script that was used to generate the data
            try:
                python_script_bytes = hdf5_file[self.camels_entry_name][
                    'measurement_details'
                ]['python_script'][()]
                data.camels_python_script = python_script_bytes.decode('utf-8')
            except KeyError:
                logger.warning('No python script found in the CAMELS file')

        # -------------------------------
        # This adds all the data to the .nxs file itself, uncomment if you dont want to have two seperate files.
        # self.archive.data = data
        # -------------------------------

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # This creates a seperate .archive.yaml file for the data

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
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
