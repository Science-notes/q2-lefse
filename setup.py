from setuptools import setup, find_packages
import re
import ast

# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('q2_humann3/__init__.py', 'rb') as f:
    hit = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(hit))


setup(
    name="q2-humann3",
    version=version,
    packages=find_packages(),
    install_requires=['qiime2 >= 2020.0.0',
                      'humann >= 3.0.0, < 4.0.0',
                      'biom-format >= 2.1.5, < 2.2.0'],
    author="Jiadong ZHao & Wei Xu",
    author_email="zd200572@163.com",
    description="QIIME2 plugin for running HUMAnN3",
    entry_points={
        "qiime2.plugins":
        ["q2-lefse=q2_lefse.plugin_setup:plugin"]
    }
)
