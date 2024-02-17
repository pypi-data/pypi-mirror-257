# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from pyavd.vendor.strip_empties import strip_empties_from_dict
from pyavd.vendor.utils import get, get_item

from .utils import UtilsMixin


class RouterPathSelectionMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def router_path_selection(self) -> dict | None:
        """
        Return structured config for router path-selection (DPS)
        """

        if not self.shared_utils.wan_role:
            return None

        router_path_selection = {
            "tcp_mss_ceiling": {"ipv4_segment_size": get(self.shared_utils.switch_data_combined, "dps_mss_ipv4", default="auto")},
            "path_groups": self._get_path_groups(),
        }

        if self.shared_utils.wan_role == "server":
            router_path_selection["peer_dynamic_source"] = "stun"

        return strip_empties_from_dict(router_path_selection)

    def _get_path_groups(self) -> list:
        """
        Generate the required path-groups locally
        """
        path_groups = []

        # TODO - need to have default value in one place only -> maybe facts / shared_utils ?
        ipsec_profile_name = get(self._hostvars, "wan_ipsec_profiles.control_plane.profile_name", default="CP-PROFILE")

        if self.shared_utils.wan_role == "server":
            # Configure all path-groups on Pathfinders and AutoVPN RRs
            path_groups_to_configure = self.shared_utils.wan_path_groups
        else:
            path_groups_to_configure = self.shared_utils.wan_local_path_groups

        for path_group in path_groups_to_configure:
            pg_name = path_group.get("name")

            path_group_data = {
                "name": pg_name,
                "id": self._get_path_group_id(pg_name, path_group.get("id")),
                "local_interfaces": self._get_local_interfaces_for_path_group(pg_name),
                "dynamic_peers": self._get_dynamic_peers(),
                "static_peers": self._get_static_peers_for_path_group(pg_name),
            }

            if path_group.get("ipsec", True):
                path_group_data["ipsec_profile"] = ipsec_profile_name

            path_groups.append(path_group_data)

        if self.shared_utils.cv_pathfinder_role:
            pass
            # implement LAN_HA here

        return path_groups

    def _get_path_group_id(self, path_group_name: str, config_id: int | None = None) -> int:
        """
        TODO - implement algorithm to auto assign IDs - cf internal documenation
        TODO - also implement algorithm for cross connects on public path_groups
        """
        if path_group_name == "LAN_HA":
            return 65535
        if config_id is not None:
            return config_id
        return 500

    def _get_local_interfaces_for_path_group(self, path_group_name: str) -> list | None:
        """
        Generate the router_path_selection.local_interfaces list

        For AUTOVPN clients, configure the stun server profiles as appropriate
        """
        local_interfaces = []
        path_group = get_item(self.shared_utils.wan_local_path_groups, "name", path_group_name, default={})
        for interface in path_group.get("interfaces", []):
            local_interface = {"name": get(interface, "name", required=True)}

            if self.shared_utils.wan_role == "client" and self.shared_utils.should_connect_to_wan_rs([path_group_name]):
                stun_server_profiles = self._stun_server_profiles.get(path_group_name, [])
                if stun_server_profiles:
                    local_interface["stun"] = {"server_profiles": [profile["name"] for profile in stun_server_profiles]}

            local_interfaces.append(local_interface)

        return local_interfaces

    def _get_dynamic_peers(self) -> dict | None:
        """
        TODO support ip_local and ipsec ?
        """
        if self.shared_utils.wan_role != "client":
            return None
        return {"enabled": True}

    def _get_static_peers_for_path_group(self, path_group_name: str) -> list | None:
        """
        TODO
        """
        if not self.shared_utils.wan_role:
            return None

        static_peers = []
        for wan_route_server_name, wan_route_server in self.shared_utils.filtered_wan_route_servers.items():
            if (path_group := get_item(get(wan_route_server, "wan_path_groups", default=[]), "name", path_group_name)) is not None:
                ipv4_addresses = []

                for interface_dict in get(path_group, "interfaces", required=True):
                    if (ip_address := interface_dict.get("ip_address")) is not None:
                        # TODO - removing mask using split but maybe a helper is clearer
                        ipv4_addresses.append(ip_address.split("/")[0])
                static_peers.append(
                    {
                        "router_ip": get(wan_route_server, "vtep_ip", required=True),
                        "name": wan_route_server_name,
                        "ipv4_addresses": ipv4_addresses,
                    }
                )

        return static_peers
