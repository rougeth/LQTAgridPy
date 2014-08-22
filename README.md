![LQTAGridPy](docs/images/LQTAGridPy.png "LQTAGridPy")

# LQTAgridPy
LQTAgridPy is a python version of [LQTAgrid](http://lqta.iqm.unicamp.br/portugues/siteLQTA/LQTAgrid.html), a practical application of 4D QSAR analysis methodology developed at Universidade de Campinas. The main difference is that LQTAgridPy has a command line interface and it is written in Python :).

In a study of QSAR main goal is to find quantitative relations between chemical structure, ie, physicochemical, structural and conformational properties and biological response through a mathematical model. These relationships help to understand and explain the mechanism of action of a drug without a molecular level and allow the planning and development of new compounds that exhibit desirable biological properties.

# Installation

Install the latest stable version of lqtaGrid with a python package manager
like `pip`:

    $ pip install lqtagrid

# Run

For the implementation `lqtagrid` just enter on the command line, passing the required parameters for generating matrix.



# Commandline Options
	
	--help            show this help message and exit
	--gro			  The command requires the path of a file with the '.gro' extension. 
	--itp			  The command requires the path of a file with the '.itp' extension. 
	-c 				  The command requires three integers numbers to determine the array coordinates. 
	-d 				  The command requires three integers numbers to determine the array dimensions. 
	-a 				  The command requires a 'string', with reference to a chemical element (atom test).
	-s 				  The command requires the float number to determine the step for navegation on matrix.