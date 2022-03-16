from pathlib import Path

from setuptools import setup

from zanshincli import __version__

setup(
    name='zanshincli',
    description='Python command line utility to the Tenchi Security Zanshin API v1',
    long_description=Path('README.rst').read_text(),
    author='Tenchi Security',
    author_email='contact@tenchisecurity.com',
    version=__version__,
    url='https://github.com/tenchi-security/zanshin-cli',
    license='Apache Software License',
    install_requires=['zanshinsdk==1.2.0', 'typer==0.3.2', 'prettytable==2.1.0', 'boto3~=1.21.19'],
    tests_require=['pytest>=6.2,<7'],
    setup_requires=['pytest-runner>=5.3,<6'],
    packages=['zanshincli'],
    # include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Security'
    ],
    entry_points={
        'console_scripts': ['zanshin=zanshincli.main:main_app']
    }
)
