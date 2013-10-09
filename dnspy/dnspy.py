#!/usr/bin/python

#
# Copyright 2013 @ Sandeep Yadav
# Released under the BSD Public License
#

import sys
import argparse
import urllib2
from contextlib import closing

class InvalidDomainError (Exception):
	def __init__ (self, domain, custmsg = 'Invalid domain entered'):
		self._custmsg = custmsg + ': ' + domain
	def __str__ (self):
		return self._custmsg

class Dnspy:
	'''
	A class for computing sub-domains and domain labels for a given FQDN (Fully Qualified Domain Name)
	'''
	
	DEFAULT_URL = 'http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1'
	etldset = set()

	def __init__ (self, etld_url=DEFAULT_URL):
		'''
		Read the ETLD list provided by the user.
		'''
		with closing(urllib2.urlopen(etld_url)) as inf:
			for line in inf:
				# Ignore comments and whitespace lines
				# Ignore lines starting with '*' or '!'
				if ((line[:2] == '//') or (line[0] in ('*', '!', '\n'))): continue
				self.etldset.add(line.strip())
		return


	def etld (self, domain):
		'''
		Given a domain, get the effective top level domains.
		IMPORTANT:	Consider only the ETLDset for ETLD identification.
				Not the DYNDNSset.
		If domain is invalid, raise InvalidDomainError
		'''
	
		dlabels = domain.strip().split('.')

		etld = None
		for i in range(len(dlabels)):
			etld = '.'.join(dlabels[i:])
			if etld in self.etldset:
				break
			etld = None

		# Borderline cases
		if etld == None: raise InvalidDomainError(domain)

		return etld


	def subdoms (self, domain, n=3):
		'''
		Given a qname, return a list of all subdomains.
		E.g. for 'www.google.com'

		returns ['com', 'google.com', 'www.google.com']
		'''
		if n == 0: return []
		etld = self.etld(domain)

		dlabels = domain[:-1*(len(etld) + 1)].split('.')
		dlabels.reverse()
		
		subdlst = list()
		subdlst.append(etld)

		# Number of sub-domains to return
		# If negative, return all
		nsubd = len(dlabels) if n < 0 else min(n - 1, len(dlabels))
		subd = etld
		for i in range(nsubd):
			subd = dlabels[i] + '.' + subd
			subdlst.append(subd)

		return subdlst


	def domlabels (self, domain, n=3):
		'''
		Returns a list of domain labels at different levels.
		E.g. for 'www.google.com'
		
		returns ['com', 'google', 'www']
		'''
		if n == 0: return []
		etld = self.etld(domain)

		dlabels = domain[:-1*(len(etld) + 1)].split('.')
		dlabels.reverse()
		
		lblst = list()
		lblst.append(etld)

		# Number of domain labels to return
		# If negative, return all
		ndl = len(dlabels) if n < 0 else min(n - 1, len(dlabels))
		for i in range(ndl):
			lblst.append(dlabels[i])

		return lblst


def main (argv=sys.argv):

	parser = argparse.ArgumentParser()
	parser.add_argument('-q', '--qname', dest='qname', 
			help='The input qname')

	if len(argv) == 1:
		parser.print_help()
		return 1	# Non-zero exit

	args = parser.parse_args()

	# Enable logging
	logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

	dpy = Dnspy()

	for lbl in dpy.domlabels(args.qname):
		print lbl

	for subd in dpy.subdoms(args.qname):
		print subd


if __name__ == "__main__":
	sys.exit(main())
