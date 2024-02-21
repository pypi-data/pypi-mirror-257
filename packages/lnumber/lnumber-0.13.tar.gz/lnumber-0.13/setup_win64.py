from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

name='lnumber'
version='0.13'
packages=['lnumber']
author = 'Jose Capco'
#url='https://github.com/jcapco/lnumber'
#data_files = [("Lib/site-packages/%s7", ["license.txt"])]
data_files = []
python_tag='py2.py3-none-win_amd64'
dll_files = ['bin/win64/lib_lnumber.dll','bin/win64/mpir.dll']
data_files.append(('Lib/site-packages/%s' % name, dll_files))

setup(
  name=name,    
  version=version,
  packages=packages,
  python_tag = python_tag,
  package_data = {'lnumber': dll_files},
  include_package_data=True,
  author = author,
  #url=url,
  data_files = data_files
)
