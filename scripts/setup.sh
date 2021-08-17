#!/usr/bin/.env bash

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Denys Chaplyhin.
#
# uct-repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


set -e

# Clean redis
invenio shell --no-term-title -c "import redis; redis.StrictRedis.from_url(app.config['CACHE_REDIS_URL']).flushall(); print('Cache cleared')"

invenio db create
invenio index destroy --force --yes-i-know
invenio index init
invenio index queue init purge
invenio taxonomies init

invenio files location --default 'default-s3' s3://oarepo

# Create roles to manage access
invenio roles create admin -d 'administrator'

invenio access allow superuser-access role admin

echo 'Thats all folks!'
