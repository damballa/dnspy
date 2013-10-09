# Dnspy
### A library for domain name manipulation

What
----

_Dnspy_ offers functionality to manipulate fully qualified domain names (FQDNs) such as 
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


Uninstallation
--------------

To uninstall, remove the directory from the disk. On debian systems, for instance:

```
$ rm -rf /usr/local/lib/python2.7/dist-packages/dnspy
```

Usage
-----

The following examples detail the use of the Dnspy module:

```
Using the module to get sub-domains of a domain

>>> from dnspy.dnspy import Dnspy
>>> d = Dnspy()		# Load the default ETLD list
>>> d.subdoms('www.google.com')
['com', 'google.com', 'www.google.com']
>>> d.domlabels('www.google.com')
['com', 'google', 'www']
```

To illustrate the use of a custom effective top-level domain (ETLD) list

```
$ cat /tmp/custom_etlds.txt
co.uk
testetld
```
Now use the custom ETLD list:
```
>>> from dnspy.dnspy import Dnspy
>>> d = Dnspy(etld_url='file:///tmp/custom_etlds.txt')
>>> d.subdoms('www.google.testetld')
['testetld', 'google.testetld', 'www.google.testetld']
```

The `etld\_url` parameter passed to the Dnspy constructor, can point to any
valid URL, including http URLs.

License
-------
Copyright &copy; 2013 Sandeep Yadav
Distributed under the BSD license

Contact
-------
Sandeep Yadav

