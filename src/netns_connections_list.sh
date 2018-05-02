#!/bin/bash

#
# this script prints ifaces with connections to other ifaces
# format of the output is:
#	ifindex  iface@connection netns

if [ "$(id -u)" != "0" ] ; then
	echo "root required!" >&2
	exit 1
fi

list=$(ip l | grep ^[0-9] | grep @ | awk -F' ' '{print "if"$1"\t"$2}' \
	| tr -d ':' | sed s/$/"   [main]"/g)

for netns in $(ip netns list) ; do
	netns_list=$(ip netns exec $netns ip l | grep ^[0-9] | grep @ \
			| awk -F' ' '{print "if"$1"\t"$2}' | tr -d ':' | sed s/$/"   ${netns}"/g)
	list=$(echo "${list}" ; echo "${netns_list}")
done

sort --version-sort <<< "$list" | sort -t" " -k3
