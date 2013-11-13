#!/usr/bin/python

# Copyright (c) 2013, Sandeep Yadav (Damballa)
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#	* Redistributions of source code must retain the above copyright
#	  notice, this list of conditions and the following disclaimer.
#	* Redistributions in binary form must reproduce the above copyright
#	  notice, this list of conditions and the following disclaimer in the
#	  documentation and/or other materials provided with the distribution.
#	* Neither the name of the <organization> nor the
#	  names of its contributors may be used to endorse or promote products
#	  derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SANDEEP YADAV (DAMBALLA) BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
	"""A class for computing sub-domains and domain labels for a given 
	FQDN (Fully Qualified Domain Name).

	"""
	
	DEFAULT_URL = 'http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1'
	etlds = dict()

	def __init__ (self, etld_url=DEFAULT_URL):
		"""Read the ETLD list provided by the user."""

		with closing(urllib2.urlopen(etld_url)) as inf:
			for line in inf:
				# Ignore comments and whitespace lines
				if ((line[:2] == '//') or 
						(line[0] == '\n')): continue

				line = line.strip()

				if line[0] == '*':
					# Any hostname matches wildcard
					etld_ = line[2:]
					if etld_ not in self.etlds:
						self.etlds[etld_] = set()
					self.etlds[line[2:]].add('*')
				elif line[0] == '!':
					# Exceptions to the wildcard rule
					lbls = line.split('.')
					etld_ = '.'.join(lbls[1:])
					if etld_ not in self.etlds:
						self.etlds[etld_] = set()
					self.etlds[etld_].add(lbls[0])
				else:
					# Else the normal case
					etld_ = line
					if etld_ not in self.etlds:
						self.etlds[etld_] = set()
		return

	def etld (self, domain):
		"""Given a domain, get the effective top level domains.
		If domain is invalid, raise InvalidDomainError

		"""
		dlabels = domain.strip().split('.')

		etld = None
		for i in range(len(dlabels)):
			etld = '.'.join(dlabels[i:])
			if etld in self.etlds:
				break
			etld = None

		# Borderline cases
		if etld == None: raise InvalidDomainError(domain)

		# Check for regex cases
		if (('*' in self.etlds[etld]) and 
				(('!' + dlabels[i-1]) not in self.etlds[etld])):
			etld = dlabels[i-1] + '.' + etld

		return etld

	def subdoms (self, domain, n=3):
		"""Given a qname, return a list of all subdomains.
		E.g. for 'www.google.com'

		returns ['com', 'google.com', 'www.google.com']

		"""

		if n == 0: return []
		etld = self.etld(domain)

		dlabels = domain[:-1*(len(etld) + 1)].split('.')
		dlabels.reverse()
		
		subdlst = list()
		subdlst.append(etld)

		# Number of sub-domains to return; if negative, return all
		nsubd = len(dlabels) if n < 0 else min(n - 1, len(dlabels))
		subd = etld
		for i in range(nsubd):
			subd = dlabels[i] + '.' + subd
			subdlst.append(subd)

		return subdlst

	def domlabels (self, domain, n=3):
		"""Returns a list of domain labels at different levels.
		E.g. for 'www.google.com'
		
		returns ['com', 'google', 'www']
		"""
		if n == 0: return []
		etld = self.etld(domain)

		dlabels = domain[:-1*(len(etld) + 1)].split('.')
		dlabels.reverse()
		
		lblst = list()
		lblst.append(etld)

		# Number of domain labels to return; if negative, return all
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
	dpy = Dnspy()

	print str(dpy.subdoms(args.qname))
	print str(dpy.domlabels(args.qname))


if __name__ == "__main__":
	sys.exit(main())
