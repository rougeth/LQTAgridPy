# coding: utf-8
from setuptools import setup, find_packages


setup(
    name='LQTAgridPy',
    version='0.4',
    description='Python version of LQTAgrid',
    author='Marco Rougeth, Mário Sérgio',
    author_email='marco@rougeth.com, sergio.mario_q@hotmail.com',
    url='https://github.com/rougeth/LQTAgridPy',
    license='',
    keywords='',
    install_requires=['click'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lqtagridpy = src.lqtagrid:run'
        ],
    }
)
