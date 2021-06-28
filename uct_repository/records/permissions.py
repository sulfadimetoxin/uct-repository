# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Denys Chaplyhin.
#
# uct-repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from flask_principal import Permission, RoleNeed

# TODO: modify permissions
# MODIFICATION_ROLE_PERMISSIONS = Permission(
#     RoleNeed('synchronizer'),
#     RoleNeed('curator'),
# )
#
# PUBLISHER_ROLE_PERMISSION = Permission(
#     RoleNeed('publisher')
# )
#
# DELETER_ROLE_PERMISSIONS = Permission(
#     RoleNeed('deleter')
# )
#
#
# def create_object_permission_impl(*args, **kwargs):
#     return MODIFICATION_ROLE_PERMISSIONS
#
#
# read_object_permission_impl = require_any(
#     MODIFICATION_ROLE_PERMISSIONS,
#     read_permission_factory,
# )
#
# update_object_permission_impl = require_any(
#     MODIFICATION_ROLE_PERMISSIONS,
#     require_all(
#         update_permission_factory,
#         state_required(None, 'filling')
#     )
# )
#
# put_file_permission_impl = update_object_permission_impl
#
# delete_file_permission_impl = update_object_permission_impl
#
# get_file_permission_impl = require_any(
#     MODIFICATION_ROLE_PERMISSIONS,
#     read_permission_factory
# )
