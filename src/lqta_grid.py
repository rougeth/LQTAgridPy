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
@click.option('--atom', '-a',
    metavar='[atom]',
    multiple=True,
    required=True,
    help='Atom of proof.'
)
@click.option('--step', '-s',
    metavar='<x>',
    type=float,
    nargs=1,
    required=True,
    help='Steps for navegation on matrix.'
)

def main(gro, itp, coordinates, dimensions, atom, step):
    '''LQTAgridPy is a python version of LQTAgrid, a practical application of
    4D analysis methodology developed at Universidade de Campinas.

    More: https://github.com/rougeth/LQTAgridPy
    '''

    grid = grid_generate.GridGenerate(
        coordinates[0], coordinates[1], coordinates[2],
        dimensions[0], dimensions[1], dimensions[2],
        atom,
        gro,
        itp,
        step
    )
    grid.saveGrid()


if __name__ == '__main__':
    main()
