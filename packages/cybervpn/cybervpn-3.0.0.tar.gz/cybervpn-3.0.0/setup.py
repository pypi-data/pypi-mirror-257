# setup.py
from setuptools import setup, find_packages

setup(
    name='cybervpn',
    version='3.0.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'cybervpn=cybervpn.module:main',
        ],
    },
    author='Aji permana',
    license='MIT',
    platforms=['Linux'],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    author_email='admin@cybervpn.site',
    description='Cybervpn autoinstall script ssh-vpn installation module with layered encryption.',
    
)

