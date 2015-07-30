sys-avenger
===========

some weapons for a sysadmin avenger

#### catell.py

Check a given x509 pem-encoded CA bundle file and show issuer/subject of each certificate.

Usage is rather simple:

	user@debian:~$ ./catell.py ca_bundle.pem
	--> certificate 1 in file ca_bundle.pem
	subject= /C=NL/ST=Noord-Holland/L=Amsterdam/O=TERENA/CN=TERENA Personal CA 2
	issuer= /C=US/ST=New Jersey/L=Jersey City/O=The USERTRUST Network/CN=USERTrust RSA Certification Authority
	
	--> certificate 2 in file ca_bundle.pem
	subject= /C=US/ST=New Jersey/L=Jersey City/O=The USERTRUST Network/CN=USERTrust RSA Certification Authority
	issuer= /C=SE/O=AddTrust AB/OU=AddTrust External TTP Network/CN=AddTrust External CA Root
	
	--> certificate 3 in file ca_bundle.pem
	subject= /C=NL/O=TERENA/CN=TERENA Personal CA
	issuer= /C=US/ST=UT/L=Salt Lake City/O=The USERTRUST Network/OU=http://www.usertrust.com/CN=UTN-USERFirst-Client Authentication and Email
	
	--> certificate 4 in file ca_bundle.pem
	subject= /C=US/ST=UT/L=Salt Lake City/O=The USERTRUST Network/OU=http://www.usertrust.com/CN=UTN-USERFirst-Client Authentication and Email
	issuer= /C=GB/ST=Greater Manchester/L=Salford/O=Comodo CA Limited/CN=AAA Certificate Services
	
	--> certificate 5 in file ca_bundle.pem
	subject= /C=GB/ST=Greater Manchester/L=Salford/O=Comodo CA Limited/CN=AAA Certificate Services
	issuer= /C=GB/ST=Greater Manchester/L=Salford/O=Comodo CA Limited/CN=AAA Certificate Services
	
	--> certificate 6 in file ca_bundle.pem
	subject= /C=SE/O=AddTrust AB/OU=AddTrust External TTP Network/CN=AddTrust External CA Root
	issuer= /C=SE/O=AddTrust AB/OU=AddTrust External TTP Network/CN=AddTrust External CA Root


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
