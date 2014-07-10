#!/usr/bin/env
# coding: utf-8

import click

import grid_generate


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--gro',
    metavar='<path>',
    type=click.Path(exists=True),
    required=True,
    help='gro file path.'
)
@click.option('--itp',
    metavar='<path>',
    type=click.Path(exists=True),
    required=True,
    help='itp file path.'
)
@click.option('--coordinates', '-c',
    metavar='<x> <y> <z>',
    type=int,
    nargs=3,
    required=True,
    help='Coordinates of the box.'
)
@click.option('--dimensions', '-d',
    metavar='<x> <y> <z>',
    type=int,
    nargs=3,
    required=True,
    help='Dimensions of the box.'
)
@click.option('--atoms', '-a',
    metavar='[atom]',
    multiple=True,
    required=True,
    help='Atom of proof.'
)

def main(gro, itp, coordinates, dimensions, atoms):
    '''LQTAgridPy is a python version of LQTAgrid, a practical application of 4D analysis methodology developed at Universidade de Campinas.

    It gives a command line interface and classes for python and non-python scripts.
    '''
    grid = grid_generate.GridGenerate(
        coordinates[0], coordinates[1], coordinates[2],
        dimensions[0], dimensions[1], dimensions[2],
        atoms,
        gro,
        itp
    )
    grid.saveGrid()


if __name__ == '__main__':
    main()
