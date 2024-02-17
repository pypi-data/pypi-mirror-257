# -*- coding: utf-8 -*-
# copyright 2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


from cubicweb import _


def define_run_workflow(add_workflow, etype):
    wf = add_workflow("execution", etype, default=True)
    # states
    wfs_in_preparation = wf.add_state(_("wfs_in_preparation"), initial=True)
    wfs_running = wf.add_state(_("wfs_running"))
    wfs_finished = wf.add_state(_("wfs_finished"))
    wfs_failed = wf.add_state(_("wfs_failed"))
    # transitions
    wf.add_transition(_("wft_start"), (wfs_in_preparation,), wfs_running, ("managers",))
    # Since cubicweb always allow firing transition when requiredgroups and
    # conditions are empty, disable permissions by adding a rql expression that
    # return no entities.
    wf.add_transition(
        _("wft_finish"), (wfs_running,), wfs_finished, (), "NOT X identity X"
    )
    wf.add_transition(_("wft_fail"), (wfs_running,), wfs_failed, (), "NOT X identity X")
    wf.add_transition(_("wft_interrupt"), (wfs_running,), wfs_failed, ("managers",))
    wf.add_transition(
        _("wft_reinit"), (wfs_finished, wfs_failed), wfs_in_preparation, ("managers",)
    )
