from pathlib import Path

from setuptools import setup

setup(
    name='zanshincli',
    description='Python command line utility to the Tenchi Security Zanshin API v1',
    long_description=Path('README.rst').read_text(encoding="utf8"),
    author='Tenchi Security',
    author_email='contact@tenchisecurity.com',
    version='__PACKAGE_VERSION__',
    url='https://github.com/tenchi-security/zanshin-cli',
    license='Apache Software License',
    install_requires=['zanshinsdk==1.2.8', 'typer==0.6.1', 'prettytable==3.3.0', 'boto3~=1.24.39', 'boto3_type_annotations~=0.3.1'],
    tests_require=['pytest==7.1.2', 'moto[all]==3.1.16'],
    setup_requires=['pytest-runner==6.0.0'],
    packages=['zanshincli'],
    # include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
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
# flake8: noqa
