# pylint: disable=W0622
"""cubicweb-notebooks application packaging information"""


modname = "cubicweb_notebooks"
distname = "cubicweb-notebooks"

numversion = (0, 1, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "A cube to deal with Jupyter-notebooks and voici view"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/notebooks"

__depends__ = {"cubicweb": ">= 4.2.0", "cubicweb-web": ">= 1.2.9"}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
