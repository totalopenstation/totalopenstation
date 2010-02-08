from setuptools import setup, find_packages

version = '0.2'

setup(name='totalopenstation',
      version=version,
      description="A program to download and export survey data from total stations",
      long_description="""\
""",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
        ],
      keywords='survey geodimeter',
      author='Stefano Costa',
      author_email='steko@iosa.it',
      url='http://tops.berlios.de/',
      license='GNU GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
        'pyserial',
      ],
      entry_points=""" """
      )
