from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1'

install_requires = []
if sys.version_info < (3, 5, 0):
    install_requires.append('typing>=3.5')

setup(name='zone_iterator',
    version=version,
    description="",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='Max R.D. Parmer',
    author_email='maxp@trystero.is',
    url='',
    license='AGPLv3',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['zone_normalize=zone_iterator.__main__:main']
    }
)
