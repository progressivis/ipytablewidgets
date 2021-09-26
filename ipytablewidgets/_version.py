# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import os
import os.path as osp
from os.path import join as pjoin
import json

here = osp.dirname(osp.abspath(__file__))
package_json = pjoin(here, 'labextension', 'package.json')
with open(package_json) as f:
    __version__ = json.load(f)['version']


