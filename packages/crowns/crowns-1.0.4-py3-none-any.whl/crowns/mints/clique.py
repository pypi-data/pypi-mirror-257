



def clique ():
	import click
	@click.group ("mints")
	def group ():
		pass


	'''
		crowns mints list-the-names
	'''
	import click
	@group.command ("list-the-names")
	def names ():
		import crowns.mints.names as mints_names
		mints_names = mints_names.start ()
	
		sorted_mints_names = sorted (mints_names)
	
		for name in sorted_mints_names:
			print (name)
	
		return;

	'''
		crowns mints save --name "mint-1"
	'''
	import click
	@group.command ("save")
	@click.option ('--name', required = True)
	def search (name):
		print ("name:", name)
	
		print ('not yet implemented')
	
		return;

	return group




#



