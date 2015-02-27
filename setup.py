from setuptools import setup, find_packages

import totalopenstation

setup(
    name='totalopenstation',
    version=totalopenstation.__version__,
    author='Stefano Costa',
    author_email='steko@iosa.it',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'gui']),
    scripts=['scripts/totalopenstation-gui.py',
             'scripts/totalopenstation-cli-parser.py',
             'scripts/totalopenstation-cli-connector.py'],
    url='http://tops.iosa.it/',
    license='GNU GPLv3',
    description='Download and export survey data from your total station',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: GIS',
        ],
    keywords='survey geodimeter',
    install_requires=['pyserial'],
    include_package_data = True,
    zip_safe = False,
)
