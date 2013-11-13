# Dnspy
### A library for domain name manipulation

What
----

_Dnspy_ offers functionality to manipulate fully qualified domain names (FQDNs), such as 
extracting _subdomains_ and _domain labels_ from a FQDN.

Installation
------------

1. To install _Dnspy_, first download the compressed tar ball _dnspy-1.0.tar.gz_

2. Untar the downloaded file:
	```
	$ tar xvzf dnspy-1.0.tar.gz
	```

3. Install the library
	```
	$ cd dnspy-1.0
	$ python setup.py install
	```


Usage
-----

The following examples illustrate the use of this module:

```python
# Using the Dnspy module to get sub-domains of a domain, given the default effective 
# top-level domain (ETLD) list

>>> from dnspy.dnspy import Dnspy
>>> d = Dnspy()		# Load the default ETLD list from Mozilla
>>> d.subdoms('a.b.c.d.google.com')
['com', 'google.com', 'd.google.com']

>>> d.subdoms('a.b.c.d.google.com', n = 4)
['com', 'google.com', 'd.google.com', 'c.d.google.com']

>>> d.subdoms('a.b.c.d.google.com', n = -1)
['com',
 'google.com',
 'd.google.com',
 'c.d.google.com',
 'b.c.d.google.com',
 'a.b.c.d.google.com']

>>> d.domlabels('a.b.c.d.google.com')
['com', 'google', 'd']

>>> d.domlabels('a.b.c.d.google.com', n = 4)
['com', 'google', 'd', 'c']

```

To illustrate the use of a custom ETLD list:

```
$ cat /tmp/custom_etlds.txt
co.uk
testetld
```
Now use the custom ETLD list:
```python
>>> from dnspy.dnspy import Dnspy
>>> d = Dnspy(etld_url='file:///tmp/custom_etlds.txt')
>>> d.subdoms('www.google.testetld')
['testetld', 'google.testetld', 'www.google.testetld']
```

The `etld_url` parameter passed to the Dnspy constructor, can point to any
valid URL, including http URLs.

To run unit tests:
```
$ cd test/
$ python -m unittest test_dnspy
...
----------------------------------------------------------------------
Ran 3 tests in 2.813s

OK

```


Uninstall
---------

To uninstall, remove the directory from the disk. On debian systems, for instance:

```
$ rm -rf /usr/local/lib/python2.7/dist-packages/dnspy
```


License
-------
Copyright &copy; 2013 Sandeep Yadav (Damballa)

Distributed under the BSD license


