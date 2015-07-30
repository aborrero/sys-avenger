sys-avenger
===========

some weapons for a sysadmin avenger

#### checkfqdn.py

Check if a given [FQDN] is symmetric. That is:
 - www.example.com points to 192.168.1.2
 - 192.168.1.2 points to www.example.com

Usage is quite simple:

	user@debian:~$ ./checkfqdn.py www.example.com

The output is nothing, as the FQDN is symmetric.

You can get verbose output:

	user@debian:~$ ./checkfqdn.py www.example.com -v
	www.example.com --> 192.168.1.2 --> www.example.com
	www.example.com --> fe00:123::2 --> www.example.com

Also work with some corner cases:

	user@debian:~$ ./checkfqdn.py www.facebook.com -v
	www.facebook.com contains CNAME
	star.c10r.facebook.com --> 173.252.73.52 --> edge-star-shv-03-prn2.facebook.com
	star.c10r.facebook.com --> 2a03:2880:20:3f07:face:b00c::1 --> edge-star6-shv-03-prn2.facebook.com

[FQDN]:http://en.wikipedia.org/wiki/Fqdn
