from setuptools import find_packages, setup
import re
import ast

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open('q2_lefse/__init__.py', 'rb') as f:
    hit = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(hit))

setup(
    name='q2-lefse',
    version=version,
    packages=find_packages(),
    install_requires=[
        'qiime2 >= 2023.2',
        'q2-types >= 2023.2',
    ],
    author='Jiadong ZHao & Wei Xu',
    author_email='zd200572@163.com',
    description='QIIME2 plugin for running LEfSe',
    entry_points={
        'qiime2.plugins': ['q2-lefse=q2_lefse.plugin_setup:plugin']
    },
)
