
import unittest

from dnspy.dnspy import Dnspy


class DnspyTestCase(unittest.TestCase):

	def setUp (self):
		#self.dno = Dnspy('file:///tmp/effective_tld_names.dat')
		self.dno = Dnspy()

	def tearDown (self):
		pass

	def test_subdoms (self):
		expected = ['co.uk', 'google.co.uk', 'www.google.co.uk']
		result = self.dno.subdoms('1.2.3.www.google.co.uk')
		self.assertEqual(expected, result)

	def test_subdoms_n (self):
		expected = ['co.uk', 'google.co.uk', 'www.google.co.uk', '3.www.google.co.uk', '2.3.www.google.co.uk']
		result = self.dno.subdoms('1.2.3.www.google.co.uk', n=5)
		self.assertEqual(expected, result)

	def test_domlabels (self):
		expected = ['co.uk', 'google', 'www']
		result = self.dno.domlabels('1.2.3.www.google.co.uk')
		self.assertEqual(expected, result)
