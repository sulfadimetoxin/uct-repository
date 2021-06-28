#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# invenio-integration-tests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

set -e

echo -e "\ncookiecutter-oarepo-instace/run_tests.sh"

export INVENIO_JSONSCHEMAS_HOST=repozitar.cesnet.cz

echo -e "\npsql version:"
psql --version

setup () {
  # test database
  echo -e "\nTest database:"
  pg_isready -h localhost -p 5432
  echo $SQLALCHEMY_DATABASE_URI


  # database
  echo -e "\ninvenio db init and create"
  invenio db init
  invenio db create

  # elastisearch
  echo -e "\nelasticsearch GET:"
  curl -sX GET "http://127.0.0.1:9200" || cat /tmp/local-es.log

  # index
  echo -e "\nInvenio Index"
  invenio index destroy --force --yes-i-know
  invenio index init
#  invenio index queue init purge
#  invenio index check

  # taxonomies
  echo -e "\nTaxonomies"
  invenio taxonomies init

  # files
  echo -e "\nFiles"
  invenio files location --default 'default-s3' s3://oarepo

  # Create roles to manage access
  invenio roles create admin -d 'administrator'

  # super-user
  invenio access allow superuser-access role admin
}


setup

echo -e "\ninvenio run (testing REST):"
#export FLASK_ENV=development
export FLASK_RUN_HOST=127.0.0.1
export FLASK_RUN_PORT=5000
export INVENIO_SERVER_NAME=127.0.0.1:5000
export INVENIO_SEARCH_ELASTIC_HOSTS=127.0.0.1:9200
export APP_ALLOWED_HOSTS=127.0.0.1:5000
export INVENIO_RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY='invenio_records_rest.utils:allow_all'
export INVENIO_RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY='invenio_records_rest.utils:allow_all'
export INVENIO_RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY='invenio_records_rest.utils:allow_all'

invenio run --cert ./development/server.crt --key ./development/server.key > invenio_run.log 2>&1 &
INVEPID=$!
trap "kill $INVEPID &>/dev/null; cat invenio_run.log" EXIT
sleep 8

#echo -n "jq version:"; jq --version
python ./scripts/test_rest.py

kill $INVEPID
trap - EXIT
echo -e "\ninvenio_run.log:"
cat invenio_run.log


#echo -e "\nsave requirements"
#REQFILE="upload/requirements-${REQUIREMENTS}.txt"
#./scripts/poetry2reqs.py | sed 's/\x0D$//' | grep -v '^pywin32==' > $REQFILE
#grep -F -e invenio= -e invenio-base -e invenio-search -e invenio-db $REQFILE

echo "Done."