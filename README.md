sys-avenger
===========

some weapons for sysadmin avengers

#### netns-events.py

Watches and reacts to linux network namespace events, allows to execute arbitrary commands on such
events and also at daemon startup.

```console
user@debian:~$ sudo netns-events.py --help
usage: netns-events.py [-h] [--debug] [--config CONFIG] [--list-events]

Daemon that watches netns events and allows running commands

optional arguments:
  -h, --help       show this help message and exit
  --debug          To activate debug mode
  --config CONFIG  YAML configuration file. Defaults to '/etc/netns-events-config.yaml'
  --list-events    list pyinotify events and exit

user@debian:~$ sudo netns-events.py --config netns-events-config.yaml
[netns-events.py] INFO: /var/run/netns/ doesn't exist. Briefly creating dummy netns
[netns-events.py] INFO: running command: /usr/bin/ip netns add netns-events-dummy
[netns-events.py] INFO: running command: /usr/bin/ip netns delete netns-events-dummy
[netns-events.py] INFO: starting operations
[netns-events.py] INFO: event on netns 'test' matched '.*' 'IN_CREATE'
[netns-events.py] INFO: running command: : empty command to create a log entry
[netns-events.py] INFO: event on netns 'test' matched '.*' 'IN_DELETE'
[netns-events.py] INFO: running command: : empty command to create a log entry
[..]
```
Uses a configuration file like this one:

```yaml
---
# $NETNS env var is provided by the runner daemon
- netns_regex: ^qrouter-.*
  daemon_startup_actions:
    - ip netns exec $NETNS sysctl net.netfilter.nf_conntrack_tcp_be_liberal=1
    - ip netns exec $NETNS sysctl net.netfilter.nf_conntrack_tcp_loose=1
  inotify_actions:
    - IN_CREATE:
        - ip netns exec $NETNS sysctl net.netfilter.nf_conntrack_tcp_be_liberal=1
        - ip netns exec $NETNS sysctl net.netfilter.nf_conntrack_tcp_loose=1
# this config is to simply log all netns creation/deletion events, which should
# help us better understand what the different neutron agents are doing
- netns_regex: .*
  daemon_startup_actions:
    - ": empty command to create a log entry"
  inotify_actions:
    - IN_CREATE:
        - ": empty command to create a log entry"
    - IN_DELETE:
        - ": empty command to create a log entry"
```

More info at: https://ral-arturo.org/2021/03/05/netns-events.html


#### cidrtool.py

A python script IPv4 calculator, to help dealing with CIDRs and to calculate subnets.

	user@debian:~$ src/cidrtool.py 10.0.0.224/28 -s
	CIDR:		10.0.0.224/28
	
	network:	10.0.0.224/28
	netmask:	255.255.255.240
	wildcard:	0.0.0.15
	broadcast:	10.0.0.239
	
	host min:	10.0.0.225
	host max:	10.0.0.238
	hosts number:	16
	
	subnet:		10.0.0.224/29
	subnet:		10.0.0.232/29
	
	subnet:		10.0.0.224/30
	subnet:		10.0.0.228/30
	subnet:		10.0.0.232/30
	subnet:		10.0.0.236/30


#### apt-upgrade.py

A python script to deal with upgrades in Debian systems which have a lot of different
repos configured.

	Usage:
	  % apt-upgrade [-un] [-f exclude_file] [-x regex] upgrade <suite> [-yh]
	  % apt-upgrade [-un] [-f exclude_file] [-x regex] report [<suite>] [-h]
	  % apt-upgrade [-un] [-f exclude_file] [-x regex] list [-h]

Make sure you hold+pin beforehand those packages that should not be upgraded.
The script requires the python-apt library.

More info at: https://wikitech.wikimedia.org/wiki/Apt-upgrade

#### netns_connections_list.sh

Lists all ifaces which have connections to other ifaces, in all netnamespaces.

```console
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
```

#### catell.py

Check a given x509 pem-encoded CA bundle file and show issuer/subject of each certificate.

Usage is rather simple:

```console
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
```

#### checkfqdn.py

Check if a given [FQDN] is symmetric. That is:
 - www.example.com points to 192.168.1.2
 - 192.168.1.2 points to www.example.com

Usage is quite simple:

```console
user@debian:~$ ./checkfqdn.py www.example.com
```

The output is nothing, as the FQDN is symmetric.

You can get verbose output:

```console
user@debian:~$ ./checkfqdn.py www.example.com -v
www.example.com --> 192.168.1.2 --> www.example.com
www.example.com --> fe00:123::2 --> www.example.com
```

Also work with some corner cases:

```console
user@debian:~$ ./checkfqdn.py www.facebook.com -v
www.facebook.com contains CNAME
star.c10r.facebook.com --> 173.252.73.52 --> edge-star-shv-03-prn2.facebook.com
star.c10r.facebook.com --> 2a03:2880:20:3f07:face:b00c::1 --> edge-star6-shv-03-prn2.facebook.com
```

[FQDN]:http://en.wikipedia.org/wiki/Fqdn
