from distutils.core import setup
import setuptools
packages = ['txdpy']
setup(name='txdpy',
    version='6.8.6',
    author='唐旭东',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=[
        "lxml","loguru","tqdm","colorama","xlrd","pymysql","xlsxwriter"
    ])