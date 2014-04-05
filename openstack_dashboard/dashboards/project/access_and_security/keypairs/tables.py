# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
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

from django.utils.translation import string_concat  # noqa
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from openstack_dashboard import api
from openstack_dashboard.usage import quotas


class DeleteKeyPairs(tables.DeleteAction):
    data_type_singular = _("Test")
    data_type_plural = _("Tests")

    def delete(self, request, obj_id):
        api.nova.keypair_delete(request, obj_id)

class CreateKeyPair(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Test")
    url = "horizon:project:access_and_security:keypairs:create"
    classes = ("ajax-modal", "btn-create")

class ReachabilityTestFilterAction(tables.FilterAction):
    
    def filter(self, table, keypairs, filter_string):
	"""Naive case-insentitive search."""
	q = filter_string.lower()
	return [keypair for keypair in keypairs
		if q in keypairs.name.lower()]

class RunTest(tables.LinkAction):
    name = "run"
    verbose_name = _("Run Test")
    url = "horizon:project:access_and_security:keypairs:create"
    classes = ("btn-edit",)

class UpdateTest(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit Test")
    url = "horizon:admin:access_and_security:update"
    classes = ( "btn-edit",)


class KeypairsTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    last_run = tables.Column("last_run", verbose_name=_("Last Run"))
    status = tables.Column("status", verbose_name=_("Status"))    

    def get_object_id(self, keypair):
        return keypair.name

    class Meta:
        name = "keypairs"
        verbose_name = _("Reachability Tests")
        table_actions = (CreateKeyPair, DeleteKeyPairs, ReachabilityTestFilterAction)
        row_actions = (RunTest,UpdateTest,DeleteKeyPairs)
