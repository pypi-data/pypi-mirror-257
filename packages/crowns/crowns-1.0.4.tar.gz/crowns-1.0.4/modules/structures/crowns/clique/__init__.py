




#from .group import clique as clique_group
from crowns.mints import clique as mints_group
from crowns.treasuries import clique as treasuries_group


import crowns

import click

def clique ():
	'''
		This configures the crowns module.
	'''
	crowns.start ()

	@click.group ()
	def group ():
		pass
	
	@click.command ("help")
	def help_command ():
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		this_module = str (normpath (join (this_directory, "..")))

		import somatic
		somatic.start ({
			"directory": this_module,
			"extension": ".s.HTML",
			"relative path": this_module
		})
		
		import time
		while True:
			time.sleep (1)

	'''
	import click
	@click.command ("example")
	def example_command ():	
		print ("example")
	
	'''

	group.add_command (help_command)

	group.add_command (mints_group.clique ())
	group.add_command (treasuries_group.clique ())
	group ()




#
