# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Denys Chaplyhin.
#
# uct-repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from invenio_records_rest.schemas import StrictKeysMixin
from oarepo_dc.marshmallow import DCObjectSchemaV2Mixin
from oarepo_invenio_model.marshmallow import InvenioRecordMetadataSchemaV1Mixin, \
    InvenioRecordMetadataFilesMixin


class RecordMetadataSchemaV1(
    InvenioRecordMetadataFilesMixin,
    InvenioRecordMetadataSchemaV1Mixin,
    DCObjectSchemaV2Mixin,
    StrictKeysMixin):
    """Schema for records drafts metadata."""
    # TODO: Change me
    pass
