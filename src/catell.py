#!/usr/bin/env python3

"""
Copyright (c) 2015 Arturo Borrero Gonzalez <arturo.borrero.glez@gmail.com>

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

import argparse
import re
from subprocess import Popen, PIPE, STDOUT

def file_read(file):
	"Returns contents of file with name `file`."
	with open(file, 'r') as f:
		return f.read()

regexp = re.compile(u"""-----BEGIN CERTIFICATE-----\r?
.+?
-----END CERTIFICATE-----""", re.DOTALL)

parser = argparse.ArgumentParser(description="Print ca bundle information")
parser.add_argument('file', nargs='+', help="ca bundle file")
args = parser.parse_args()

for input_file in args.file:
	i = 1
	for match in re.findall(regexp, file_read(input_file)):
		print("--> certificate", i, "in file", input_file)
		p = Popen(["openssl", "x509", "-noout", "-subject", "-issuer"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		openssl_stdout = p.communicate(input = match.encode())[0]
		print(openssl_stdout.decode())
		i = i + 1
