from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='nobar',
  version='1.0.0',
  author='NoromTin',
  author_email='aninelo@gmail.com',
  description='Usefull progress "bar"',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/NoromTin/nobar',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent'
  ],
  keywords='progress bar',
  project_urls={
    'Documentation': 'https://github.com/NoromTin/nobar/blob/main/README.md'
  },
  python_requires='>=3.0'
)