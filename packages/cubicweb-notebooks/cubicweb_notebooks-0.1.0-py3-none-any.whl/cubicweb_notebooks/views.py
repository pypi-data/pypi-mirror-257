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

"""cubicweb-notebooks views/forms/actions/components for web ui"""

from cubicweb_web.views.startup import StartupView
from cubicweb_web import httpcache
from cubicweb import _

from cubicweb.tags import h1

from cubicweb.predicates import authenticated_user


from cubicweb_web.views.urlrewrite import SimpleReqRewriter


class NotebookSimpleReqRewriter(SimpleReqRewriter):

    priority = 100

    rules = [
        ("/notebooks", dict(vid="cw.notebooks")),
    ]


class NotebooksView(StartupView):
    __select__ = StartupView.__select__ & authenticated_user()
    __regid__ = "cw.notebooks"
    http_cache_manager = httpcache.NoHTTPCacheManager
    NOTEBOOKS = []

    def card_component(self, title, description, notebook):
        ref = self._cw.base_url() + "cwnotebook" + f"?name={notebook}"
        return f"""
        <div class="card" style="width: 18rem;">
        <div class="card-body">
        <h5 class="card-title">{title}</h5>
        <p class="card-text">{description}</p>
        <a href="{ref}" class="card-link">Lien vers le calepin</a>
        </div>
        </div>
        """

    def lab_card(self):
        ref = self._cw.data_url("lab/index.html")
        # ref = self._cw.base_url() + 'cwnotebook' + '?name=index'
        return f"""
        </div>
        <div class="card" style="width: 18rem;">
        <div class="card-body">
        <h5 class="card-title">Le Lab</h5>
        <p class="card-text">Le laboratoire de création des notebooks</p>
        <a href="{ref}" class="card-link">Lien vers lab</a>
        </div>
        </div>
        """

    def call(self):
        self.w(h1(_("Les calepins de l'application")))
        for notebook_data in self.NOTEBOOKS:
            self.w(self.card_component(**notebook_data))
        self.w(self.lab_card())
