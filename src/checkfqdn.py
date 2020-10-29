#!/usr/bin/env python3

"""
Copyright (c) 2014 Arturo Borrero Gonzalez <arturo.borrero.glez@gmail.com>
This file is released under the GPLv3 license.

Can obtain a complete copy of the license at: http://www.gnu.org/licenses/gpl-3.0.html

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# requires the python3-dnspython (debian)

import sys
import argparse
import dns.resolver
import dns.reversename

verbose = False

#
# functions
#

def str_clean_last_dot(str):
	if str[-1:] == ".":
		return str[0:-1]

	return str

def compare_regs(ptr, orig, fqdn):
	ret = True

	try:
		PTR_regs = dns.resolver.resolve(ptr, 'PTR')
	except Exception:
		print("W: Unable to get PTR:", ptr)
		pass

	for PTR in PTR_regs:
		PTR_text = str_clean_last_dot(PTR.to_text())
		if PTR_text != fqdn:
			ret = False
			print(fqdn, "-->", orig, "-->", PTR_text)
		elif verbose:
			print(fqdn, "-->", orig, "-->", PTR_text)
	return ret

def query_A(fqdn):
	ret = True
	try:
		A_regs = dns.resolver.resolve(fqdn, 'A')
		for A in A_regs:
			ptr = dns.reversename.from_address(A.to_text())
			if not compare_regs(ptr, A, fqdn):
				ret = False
	except Exception:
		print("W: Unable to get A:", fqdn)
		pass

	return ret

def query_AAAA(fqdn):
	ret = True
	try:
		AAAA_regs = dns.resolver.resolve(fqdn, 'AAAA')
		for AAAA in AAAA_regs:
			ptr = dns.reversename.from_address(AAAA.to_text())
			if not compare_regs(ptr, AAAA, fqdn):
				ret = False
	except Exception:
		print("W: Unable to get AAAA:", fqdn)
		pass

	return ret

def fqdn_symmetry(fqdn_list):
	ret = True
	first = True

	for fqdn in fqdn_list:
		if first:
			first = False
		else:
			print("")

		if not query_A(fqdn):
			ret = False

		if not query_AAAA(fqdn):
			ret = False
	return ret

def fqdns_symmetry(fqdn_list):
	fqdn_final = []
	for fqdn in fqdn_list:
		try:
			CNAME_regs = dns.resolver.resolve(fqdn, 'CNAME')
			if len(CNAME_regs) > 0:
				if verbose:
					print(fqdn, "contains CNAME")

				for CNAME in CNAME_regs:
					fqdn_final.append(str_clean_last_dot(CNAME.to_text()))
		except Exception:
			fqdn_final.append(fqdn)
			pass

	return fqdn_symmetry(fqdn_final)

#
# program
#

parser = argparse.ArgumentParser(description="Check that given FQDN's A and AAAA regs points back to it.")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument('fqdns', nargs='+', help="FQDNs to check")
args = parser.parse_args()

verbose = args.verbose

if not fqdns_symmetry(args.fqdns):
	exit(1)
