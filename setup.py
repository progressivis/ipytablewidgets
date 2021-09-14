from setuptools import setup, find_packages
import os
from os.path import join as pjoin
from distutils import log

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)


here = os.path.dirname(os.path.abspath(__file__))

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

npm_package_name = 'jupyter-tablewidgets'
python_package_name = 'ipytablewidgets'
version = get_version(pjoin(python_package_name, '_version.py'))

js_dir = pjoin(here, 'src')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(here, python_package_name, 'static', 'index.js'),
    pjoin(here, python_package_name, 'labextension', 'package.json'),    
]

data_files_spec = [
    (f'share/jupyter/nbextensions/{npm_package_name}', f'{python_package_name}/static', '*.*'),
    (f'share/jupyter/labextensions/{npm_package_name}', f'{python_package_name}/labextension', '**'),
    (f'share/jupyter/labextensions/{npm_package_name}', '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.', f'{npm_package_name}.json'),
]

cmdclass = create_cmdclass('jsdeps', data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(here, npm=['npm'], source_dir=js_dir, build_cmd='build'), ensure_targets(jstargets),
)

setup_args = dict(
    version=version,
    include_package_data=True,
    cmdclass=cmdclass,
)

setup(**setup_args)
