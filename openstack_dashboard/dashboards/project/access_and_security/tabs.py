# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
# Copyright 2012 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tabs

from openstack_dashboard.api import keystone
from openstack_dashboard.api import network
from openstack_dashboard.api import nova

from openstack_dashboard.dashboards.project.access_and_security.\
    api_access.tables import EndpointsTable
from openstack_dashboard.dashboards.project.access_and_security.\
    floating_ips.tables import FloatingIPsTable
from openstack_dashboard.dashboards.project.access_and_security.\
    keypairs.tables import KeypairsTable
from openstack_dashboard.dashboards.project.access_and_security.\
    security_groups.tables import SecurityGroupsTable


class SecurityGroupsTab(tabs.Tab):
    name = _("Network Template")
    slug = "security_groups_tab"
    template_name = "horizon/common/_detail_table.html"
   
    def get_context_data(self,request):
	return None

class KeypairsTab(tabs.TableTab):
    table_classes = (KeypairsTable,)
    name = _("Reachability Tests")
    slug = "keypairs_tab"
    template_name = "horizon/common/_detail_table.html"

    def get_keypairs_data(self):
        try:
            keypairs = nova.keypair_list(self.request)
        except Exception:
            keypairs = []
            exceptions.handle(self.request,
                              _('Unable to retrieve key pair list.'))
        return keypairs


class FloatingIPsTab(tabs.Tab):
    name = _("Troubleshoot")
    slug = "floating_ips_tab"
    template_name = "horizon/common/_detail_table.html"
        
    def get_context_data(self,request):
	return None


class APIAccessTab(tabs.TableTab):
    table_classes = (EndpointsTable,)
    name = _("Top Talkers")
    slug = "api_access_tab"
    template_name = "horizon/common/_detail_table.html"

    def get_endpoints_data(self):
        services = []
        for i, service in enumerate(self.request.user.service_catalog):
            service['id'] = i
            services.append(
                keystone.Service(service, self.request.user.services_region))

        return services


class AccessAndSecurityTabs(tabs.TabGroup):
    slug = "access_security_tabs"
    tabs = (SecurityGroupsTab, KeypairsTab, FloatingIPsTab, APIAccessTab)
    sticky = True
