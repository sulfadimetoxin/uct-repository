# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Denys Chaplyhin.
#
# uct-repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from collections import namedtuple
from flask import current_app

from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2


FetchedPID = namedtuple('FetchedPID', ['provider', 'pid_type', 'pid_value'])


# TODO: Change this and register in entry_points (pyproject.toml)
def recid_fetcher_v2(record_uuid, data):
    """Fetch a record's identifiers.
    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    return FetchedPID(
        provider=RecordIdProviderV2,
        pid_type=RecordIdProviderV2.pid_type,
        pid_value=str(data[pid_field])
    )

def records_all_fetcher(record_uuid, data):
    fetched_pid = recid_fetcher_v2(record_uuid, data)
    print(data)
    if 'oarepo:validity' in data:
        return FetchedPID(
            provider=fetched_pid.provider,
            pid_type='drcid',
            pid_value=fetched_pid.pid_value,
        )
    else:
        return fetched_pid
