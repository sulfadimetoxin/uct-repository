# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# CESNET OA Repository Demo is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
# Dockerfile that builds a fully functional image of your app.
ARG DEPENDENCIES_VERSION=latest
FROM inveniosoftware/centos8-python:3.8

COPY uct-repository .
COPY docker/uwsgi ${INVENIO_INSTANCE_PATH}

RUN poetry config virtualenvs.create false

RUN poetry install
USER invenio
ENTRYPOINT [ "bash", "-c"]
