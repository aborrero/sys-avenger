#!/usr/bin/env python3

"""
Copyright (c) 2020 Arturo Borrero Gonzalez <arturo@debian.org>
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


import sys
import argparse
import ipaddress
import logging
from collections import deque


def main():
    parser = argparse.ArgumentParser(
        description="Utility to calculate information on an IPv4 CIDR"
    )
    parser.add_argument("cidr", action="store", help="IPv4 CIDR to use")
    parser.add_argument("-s", action="store_true", help="show potential subnets")
    args = parser.parse_args()

    logging_format = "%(levelname)s: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO)

    try:
        cidr = ipaddress.IPv4Interface(args.cidr)
    except ValueError as e:
        logging.error(e)
        sys.exit(1)

    print("CIDR:\t\t{}".format(cidr))
    print("")
    print("network:\t{}".format(cidr.network.exploded))
    print("netmask:\t{}".format(cidr.network.netmask))
    print("wildcard:\t{}".format(cidr.network.hostmask))
    print("broadcast:\t{}".format(cidr.network.broadcast_address))

    if cidr.network.prefixlen == 32:
        host_min = cidr.network.network_address
        host_max = cidr.network.network_address
        nhost = 1
    elif cidr.network.prefixlen == 31:
        host_min = next(cidr.network.hosts())
        host_max = deque(cidr.network.hosts(), maxlen=1).pop()
        nhost = 2
    else:
        host_min = cidr.network.network_address + 1
        host_max = cidr.network.broadcast_address - 1
        nhost = 2 ** (32 - cidr.network.prefixlen)

    print("")
    print("host min:\t{}".format(host_min))
    print("host max:\t{}".format(host_max))
    print("hosts number:\t{}".format(nhost))

    if args.s and cidr.network.prefixlen < 32:
        print("")
        for subnet in cidr.network.subnets():
            print("subnet:\t\t{}".format(subnet.exploded))

        if cidr.network.prefixlen < 31:
            print("")
            for subnet in cidr.network.subnets(prefixlen_diff=2):
                print("subnet:\t\t{}".format(subnet.exploded))


if __name__ == "__main__":
    main()
