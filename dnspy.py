#!/usr/bin/python

#
# Copyright 2013 @ Sandeep Yadav
# TODO: Released under GNU Public License
#

import sys
import logging
import argparse
import urllib2
from contextlib import closing

class InvalidDomainError (Exception):
	def __init__ (self, custmsg = 'Invalid domain entered'):
		self._custmsg = custmsg
	def __str__ (self):
		return self._custmsg

class Dnspy:
	'''
	TODO
	'''
	DEFAULT_URL = 'http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1'

	etld_hier_ = dict()

	def __init__ (self, etld_url=DEFAULT_URL):
		'''
		TODO
		'''
		logging.debug('Reading ETLD list ...')

		with closing(urllib2.urlopen(etld_url)) as inf:
			for line in inf:
				# Ignore comments and whitespace lines
				if line[:2] == '//' or line[0] == '\n': continue
				print line

				# Gotta read the UTF-8 encodings



		logging.debug('Done reading ETLD list ...')

		return

	def get (self):
		'''
		
		'''
		pass


def main (argv=sys.argv):

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--infile', dest='infile', 
			help='The input file')
	parser.add_argument('-n', '--count', dest='count', type = int, default = 3,
			help='An arbitrary count for demonstration purpose only')

	'''
	if len(argv) == 1:
		parser.print_help()
		return 1	# Non-zero exit

	args = parser.parse_args()
	print args.infile
	'''

	# Enable logging
	logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

	# Unit tests
	dpy = Dnspy()



if __name__ == "__main__":
	sys.exit(main())
