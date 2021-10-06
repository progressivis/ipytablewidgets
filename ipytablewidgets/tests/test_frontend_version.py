# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import os
from os.path import join as pjoin
import json
from .._frontend import npm_module_name, npm_package_version

here = os.path.dirname(os.path.abspath(__file__))


def test_frontend():
    package_json_file = pjoin(here, '..', '..', 'js', 'package.json')
    with open(package_json_file) as pjf:
        package_json = json.load(pjf)
        print(package_json)
        assert package_json['name'] == npm_module_name
        assert f"^{package_json['version']}" == npm_package_version
