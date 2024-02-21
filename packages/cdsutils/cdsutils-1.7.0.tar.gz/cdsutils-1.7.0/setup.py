from setuptools import setup


with open('README.md', 'rb') as f:
    longdesc = f.read().decode().strip()


setup(
    setup_requires=[
        'setuptools_scm',
    ],

    use_scm_version={
        'write_to': 'cdsutils/_version.py',
    },

    name='cdsutils',
    description='Advanced LIGO CDS python utilities',
    long_description=longdesc,
    long_description_content_type='text/markdown',
    author='Jameson Graef Rollins',
    author_email='jameson.rollins@ligo.org',
    url='https://git.ligo.org/cds/cdsutils',
    license='GPL-3.0-or-later',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    install_requires=[
        'gpstime',
        #'nds2-client',
        'matplotlib',
        'numpy',
        'ezca',
    ],

    packages=[
        'cdsutils',
    ],

    entry_points={
        'console_scripts': [
            'cdsutils = cdsutils.__main__:main',
        ],
    },

)
