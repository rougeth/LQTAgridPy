from os import path

import click


def validate_files(context, param, value):
    if path.isfile(value):
        return True
    else:
        raise click.BadParameter('file does not exists')


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--gro',
    metavar='<name>',
    callback=validate_files,
    required=True,
    help='gro file'
)
@click.option('--itp',
    metavar='<name>',
    callback=validate_files,
    required=True,
    help='itp file'
)
@click.option('--matrix',
    metavar='<name>',
    required=True,
    help='matrix'
)
def main(gro, itp, matrix):
    '''LQTAgridPy is a python version of LQTAgrid, a practical application of 4D analysis methodology developed at Universidade de Campinas.

    It gives a command line interface and classes for python and non-python scripts.

    More: https://github.com/rougeth/LQTAgridPy
    '''
    click.echo('Hello World')


if __name__ == '__main__':
    main()
