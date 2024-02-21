# -*- coding: utf-8 -*-
#
# This file is a part of the LinkAhead Project.
#
# Copyright (C) 2023 Henrik tom Wörden <h.tomwoerden@indiscale.com>
# Copyright (C) 2023 IndiScale GmbH <info@indiscale.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

"""Convenience functions to retrieve a specific entity."""

from typing import Union

from ..common.models import Entity, execute_query
from .escape import escape_squoted_text


def get_entity_by_name(name: str) -> Entity:
    """Return the result of a unique query that uses the name to find the correct entity.

    Submits the query "FIND ENTITY WITH name='{name}'".
    """
    name = escape_squoted_text(name)
    return execute_query(f"FIND ENTITY WITH name='{name}'", unique=True)


def get_entity_by_id(eid: Union[str, int]) -> Entity:
    """Return the result of a unique query that uses the id to find the correct entity.

    Submits the query "FIND ENTITY WITH id='{eid}'".
    """
    return execute_query(f"FIND ENTITY WITH id='{eid}'", unique=True)


def get_entity_by_path(path: str) -> Entity:
    """Return the result of a unique query that uses the path to find the correct file.

    Submits the query "FIND FILE WHICH IS STORED AT '{path}'".
    """
    return execute_query(f"FIND FILE WHICH IS STORED AT '{path}'", unique=True)
