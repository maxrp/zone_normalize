import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1'

install_requires = []
if sys.version_info < (3, 5, 0):
    install_requires.append('typing>=3.5')

setup(name='zone_normalize',
      version=version,
      description="",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'License :: DFSG approved',
          'License :: OSI Approved :: GNU Affero General Public License v3 or \
                  later (AGPLv3+)',
          'Topic :: Internet :: Name Service (DNS)',
          'Topic :: Software Development :: Libraries',
          'Topic :: Text Processing',
          'Topic :: Utilities',
      ],
      keywords='dns zone parse highlight normalize',
      author='Max R.D. Parmer',
      author_email='maxp@trystero.is',
      url='',
      license='AGPLv3+',
      packages=find_packages('.'),
      package_dir={'': '.'}, include_package_data=True,
      install_requires=install_requires,
      setup_requires=['pytest-runner'],
      extras_require={'colors': 'colorama'},
      entry_points={
        'console_scripts':  [
            'zone-highlight=zone_normalize.__main__:main [colors]'
        ]
      })
