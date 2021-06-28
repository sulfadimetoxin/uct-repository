# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Denys Chaplyhin.
#
# uct-repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_indexer.api import RecordIndexer
from invenio_records_rest.utils import allow_all, deny_all, check_elasticsearch
from invenio_search import RecordsSearch
from uct_repository.records.record import all_index_name, draft_index_name, published_index_name, AllRecords
from oarepo_records_draft import DRAFT_IMPORTANT_FACETS, DRAFT_IMPORTANT_FILTERS

RECORDS_DRAFT_ENDPOINTS = {
    'record': {
        'draft': 'draft-record',

        'pid_type': 'recid',
        'pid_minter': 'recid',
        'pid_fetcher': 'recid',
        'default_endpoint_prefix': True,

        'record_class': 'uct_repository.records.record.PublishedRecord',
        'search_class': RecordsSearch,
        'indexer_class': RecordIndexer,
        'search_index': published_index_name,
        'list_route': '/records/',
        'item_route': '/records/<pid(recid,'
                      'record_class="uct_repository.records.api.Record")'
                      ':pid_value>',

        # TODO: change this !!!
        'publish_permission_factory_imp': allow_all,
        'unpublish_permission_factory_imp': allow_all,
        'edit_permission_factory_imp': allow_all,
        'default_media_type': 'application/json',
        'max_result_window': 10000,

        'use_options_view': False,

    },
    'draft-record': {
        'pid_type': 'drcid',
        'record_class': 'uct_repository.records.record.DraftRecord',

        # TODO: change this
        # 'create_permission_factory_imp':
        #     'uct_repository.records.record.permissions.create_object_permission_impl',
        # 'read_permission_factory_imp':
        #     'uct_repository.records.record.permissions.read_object_permission_impl',
        # 'update_permission_factory_imp':
        #     'uct_repository.records.record.permissions.update_object_permission_impl',

        'record_loaders': {
            'application/json': 'oarepo_validate.json_files_loader',
            'application/json-patch+json': 'oarepo_validate.json_loader'
        },
        'search_index': draft_index_name
    }
}

RECORDS_REST_ENDPOINTS = {
    # readonly url for both endpoints, does not have item route
    # as it is accessed from the endpoints above
    'all-records': dict(
        pid_type='allrid',
        pid_minter='all-records',
        pid_fetcher='all-records',
        default_endpoint_prefix=True,
        search_class=RecordsSearch,
        record_class=AllRecords,
        search_index=all_index_name,
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        list_route='/all-records/',
        default_media_type='application/json',
        max_result_window=10000,

        # not used really
        item_route='/all-records/not-used-but-must-be-present',
        create_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        update_permission_factory_imp=deny_all,
        read_permission_factory_imp=check_elasticsearch,
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        use_options_view=False
    )
}

FILTERS = {
    **DRAFT_IMPORTANT_FILTERS
}

FACETS = {
    **DRAFT_IMPORTANT_FACETS
}

ANONYMOUS_FACETS = {

}

RECORDS_REST_FACETS = {

}

RECORDS_REST_SORT_OPTIONS = {
    all_index_name: {
        'alphabetical': {
            'title': 'alphabetical',
            'fields': [
                'title.cs.raw'
            ],
            'default_order': 'asc',
            'order': 1
        },
        'best_match': {
            'title': 'Best match',
            'fields': ['_score'],
            'default_order': 'desc',
            'order': 1,
        }
    }
}

RECORDS_REST_DEFAULT_SORT = {
    all_index_name: {
        'query': 'best_match',
        'noquery': 'alphabetical'
    }
}
