# setup.py
from setuptools import setup, find_packages

setup(
    name='pymybotvpn',
    version='3.1.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'pymybotvpn=mybot.module:main',
        ],
    },
    author='Aji Permana',
    author_email='admin@cybervpn.site',
    description='A Python module for installing and configuring PyMyBot VPN',
    long_description='Pymybot vpn is a python bot panel module using the telethon module as its backend..',
    url='https://github.com/Azigaming404',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

