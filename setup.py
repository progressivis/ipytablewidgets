from setuptools import setup, find_packages
import os
import json
import os.path as osp
from os.path import join as pjoin

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    #get_version,
)


here = osp.dirname(osp.abspath(__file__))

npm_package_name = 'jupyter-tablewidgets'
python_package_name = 'ipytablewidgets'
#version = get_version(pjoin(python_package_name, '_version.py'))
package_json = pjoin(here, 'js', 'package.json')
with open(package_json) as f:
    version = json.load(f)['version']


js_dir = pjoin(here, 'js')
js_src_dir = pjoin(js_dir, 'src')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(here, python_package_name, 'static', 'index.js'),
    pjoin(here, python_package_name, 'labextension', 'package.json'),    
]

data_files_spec = [
    (f'share/jupyter/nbextensions/{npm_package_name}', f'{python_package_name}/static', 'index.js'),
    (f'share/jupyter/nbextensions/{npm_package_name}', f'{python_package_name}/static', 'extension.js'),
    (f'share/jupyter/labextensions/{npm_package_name}', f'{python_package_name}/labextension', '**'),
    (f'share/jupyter/labextensions/{npm_package_name}', 'js', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', 'js', f'{npm_package_name}.json'),
]

cmdclass = create_cmdclass('jsdeps', data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(js_dir, npm=['yarn'], source_dir=js_src_dir, build_cmd='build'), ensure_targets(jstargets),
)

setup_args = dict(
    version=version,
    include_package_data=True,
    cmdclass=cmdclass,
)

setup(**setup_args)
