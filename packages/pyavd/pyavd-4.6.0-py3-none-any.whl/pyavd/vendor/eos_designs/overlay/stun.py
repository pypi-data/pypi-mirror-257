# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import itertools
from functools import cached_property

from .utils import UtilsMixin


class StunMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def stun(self) -> dict | None:
        """
        Return structured config for stun
        """

        if not self.shared_utils.wan_role:
            return None

        stun = {}
        if self.shared_utils.wan_role == "server":
            local_interfaces = [wan_interface["name"] for wan_interface in self.shared_utils.wan_interfaces]
            stun["server"] = {"local_interfaces": local_interfaces}

        if self.shared_utils.wan_role == "client":
            if server_profiles := list(itertools.chain.from_iterable(self._stun_server_profiles.values())):
                stun["client"] = {"server_profiles": server_profiles}

        return stun or None
