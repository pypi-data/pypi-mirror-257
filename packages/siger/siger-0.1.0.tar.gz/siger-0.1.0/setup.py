# PASSO 01a: cd 02_SIGER\      +      pip install -e .
# PASSO 01b: pip install -e ./02_SIGER
# PASSO 01c: py -3.12 -m pip install -e ./02_SIGER
# PASSO 01d: pip install -e "C:/Users/natha/OneDrive - Operador Nacional do Sistema Eletrico/_Home Office ONS/Ferramentas - Programação/GitHub+/02_SIGER"
#
# Distribuição PIP
# cd 02_SIGER
# python setup.py sdist bdist_wheel
# twine upload dist/*
from setuptools import setup

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='siger',
    version='0.1.0',
    description='Automações em Python para auxiliar obtenção de dados do SIGER-CEPEL',
    author='Nathan Kelvi de Almeida Bueno',
    author_email='nathankelvi@gmail.com',
    url='https://github.com/nkbueno/siger',
    packages=['siger'],
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'beautifulsoup4',
        'selenium',
        'DateTime',
        'pywin32',
        'xlsxwriter',
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
