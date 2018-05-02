sys-avenger
===========

some weapons for sysadmin avengers

#### netns_connections_list.sh

Lists all ifaces which have connections to other ifaces, in all netnamespaces.

	user@debian:~ $ sudo ./netns_connections_list.sh
	if40	testveth1_p2@if41   test_netns
	if25	veth1@if26   [main]
	if36	tap8d7bc846-96@eth0   [main]
	if39	tap02dc90ca-64@eth1.2120   [main]
	if41	testveth1_p1@if40   [main]
	if4	eth1.2105@eth1   [main]
	if5	eth1.2120@eth1   [main]
	if6	tapfcf1a098-9d@eth0   [main]
	if7	tapdb1b15f9-ac@eth0   [main]
	if8	tap21e10025-d4@eth1   [main]
	if9	tap666fcda7-04@eth1.2105   [main]
	if2	ns-fcf1a098-9d@if6   qdhcp-05a5494a-184f-4d5c-9e98-77ae61c56daa
	if2	ns-8d7bc846-96@if36   qdhcp-60aa9467-253c-4fdf-9fa0-eba42dafc975
	if2	ha-db1b15f9-ac@if7   qrouter-5712e22e-134a-40d3-a75a-1c9b441717ad
	if3	qr-21e10025-d4@if8   qrouter-5712e22e-134a-40d3-a75a-1c9b441717ad
	if4	qg-666fcda7-04@if9   qrouter-5712e22e-134a-40d3-a75a-1c9b441717ad
	if5	qr-02dc90ca-64@if39   qrouter-5712e22e-134a-40d3-a75a-1c9b441717ad
	if26	veth0@if25   TEST


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
