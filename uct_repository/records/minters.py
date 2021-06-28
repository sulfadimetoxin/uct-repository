# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Denys Chaplyhin.
#
# uct-repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from flask import current_app

from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2

# TODO: Change this and register in entry_points
def recid_minter_v2(record_uuid, data):
    """Mint record identifiers with RecordIDProviderV2.
    This minter is recommended to be used when creating records to get
    PersistentIdentifier with ``object_type='rec'`` and the new random
    alphanumeric `pid_value`.
    Raises ``AssertionError`` if a ``PIDSTORE_RECID_FIELD`` entry is already in
    ``data``. The minted ``pid_value`` will be stored in that field.
    :param record_uuid: The object UUID of the record.
    :param data: The record metadata.
    :returns: A fresh `invenio_pidstore.models.PersistentIdentifier` instance.
    """
    pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    assert pid_field not in data
    provider = RecordIdProviderV2.create(
        object_type='rec', object_uuid=record_uuid)
    data[pid_field] = provider.pid.pid_value
    return provider.pid

def records_all_minter(record_uuid, data):
    raise Exception('Should not be used as all objects are readonly')