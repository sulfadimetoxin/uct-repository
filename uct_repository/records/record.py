# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Denys Chaplyhin.
#
# uct-repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


import os

from flask import url_for
from invenio_records_files.api import Record
from oarepo_invenio_model import InheritedSchemaRecordMixin
from oarepo_records_draft.ext import RecordsDraftState
from oarepo_records_draft.record import DraftRecordMixin, InvalidRecordAllowedMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin, \
    FilesKeepingRecordMixin

from .constants import (
    OBJECT_ALLOWED_SCHEMAS,
    OBJECT_PREFERRED_SCHEMA
)
from .marshmallow import RecordMetadataSchemaV1

current_drafts: RecordsDraftState

published_index_name = 'records-record-v1.0.0'
draft_index_name = 'draft-records-record-v1.0.0'
all_index_name = 'all-records'

prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_index_name


class BaseRecord(SchemaKeepingRecordMixin,
                 MarshmallowValidatedRecordMixin,
                 InheritedSchemaRecordMixin,
                 Record):
    """Record class for Item Record"""
    ALLOWED_SCHEMAS = OBJECT_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = OBJECT_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = RecordMetadataSchemaV1


class PublishedRecord(InvalidRecordAllowedMixin, BaseRecord):
    index_name = published_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.record_item',
                       pid_value=self['id'], _external=True)


class DraftRecord(DraftRecordMixin,
                  FilesKeepingRecordMixin,
                  BaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-record_item',
                       pid_value=self['id'], _external=True)


class AllRecords(Record):
    pass
