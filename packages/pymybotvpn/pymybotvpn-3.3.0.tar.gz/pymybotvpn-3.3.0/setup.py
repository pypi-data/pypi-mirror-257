# setup.py

from setuptools import setup, find_packages

setup(
    name='pymybotvpn',
    version='3.3.0',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'pymybotvpn=mybot.module:update_bot_script',
        ],
    },
    description='A Python module to update and execute a bot script',
    long_description='This module provides a function to update a bot script and execute it, specifically designed for Ubuntu and Debian systems.',
    author='Aji permana',
    author_email='admin@cybervpn.site',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
    ],
    keywords='bot script update execution',
    python_requires='>=3.6',
)

