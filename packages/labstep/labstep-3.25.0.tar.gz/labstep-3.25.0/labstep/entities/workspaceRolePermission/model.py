#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Labstep <dev@labstep.com>

from labstep.generic.entity.model import Entity
from labstep.constants import UNSPECIFIED


class WorkspaceRolePermission(Entity):
    __entityName__ = "permission-role-setting"
    # __hasGuid__ = True
    # __unSearchable__=True

    def revoke(self):
        """
            Revokes the permission from the workspace role.

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        import labstep.entities.workspaceRolePermission.repository as WorkspaceRolePermission

        return WorkspaceRolePermission.deleteWorkspaceRolePermission(self)
