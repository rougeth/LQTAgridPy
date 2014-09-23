# LQTAgridPy

![LQTAGridPy](docs/images/LQTAGridPy.png "LQTAGridPy")

LQTAgridPy is a python version of [LQTAgrid](http://lqta.iqm.unicamp.br/portugues/siteLQTA/LQTAgrid.html), a practical application of 4D QSAR analysis methodology developed at Universidade de Campinas. The main difference is that LQTAgridPy has a command line interface and it is written in Python :).

In a study of QSAR main goal is to find quantitative relations between chemical structure, ie, physicochemical, structural and conformational properties and biological response through a mathematical model. These relationships help to understand and explain the mechanism of action of a drug without a molecular level and allow the planning and development of new compounds that exhibit desirable biological properties.

## Installation

Install the latest stable version of LQTAgridPy with the python package manager `pip`:

    $ pip install lqtagridpy

## Usage

```
$ python lqtagrid.py  --help
Usage: lqtagrid.py [OPTIONS]

  LQTAgridPy is a python version of LQTAgrid, a practical application of 4D
  analysis methodology developed at Universidade de Campinas.

  More: https://github.com/rougeth/LQTAgridPy

Options:
  --mols <path>                  files path, gro and itp.  [required]
  -c, --coordinates <x> <y> <z>  Coordinates of the box.  [required]
  -d, --dimensions <x> <y> <z>   Dimensions of the box.  [required]
  -a, --atom [atom]              Atom of proof.  [required]
  -s, --step <x>                 Steps for navegation on matrix.  [required]
  -h, --help                     Show this message and exit.
```
