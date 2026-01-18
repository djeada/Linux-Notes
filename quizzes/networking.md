#### Q. Which command shows the current IP addresses assigned to all network interfaces in modern Linux distributions?

* [ ] `ifconfig -a`
* [x] `ip addr show`
* [ ] `netstat -i`
* [ ] `route -n`
* [ ] `iptables -L`

#### Q. Where is the default gateway specified in the routing table?

* [ ] Destination `0.0.0.0` / Genmask `255.255.255.255`
* [x] Destination `0.0.0.0` / Genmask `0.0.0.0`
* [ ] Destination `127.0.0.0` / Genmask `255.0.0.0`
* [ ] Destination `255.255.255.255` / Genmask `255.255.255.255`
* [ ] Destination `192.168.1.0` / Genmask `255.255.255.0`

#### Q. Which file is used to define static DNS servers for name resolution system-wide?

* [ ] `/etc/hostname`
* [ ] `/etc/resolvconf.conf`
* [x] `/etc/resolv.conf`
* [ ] `/etc/hosts.dns`
* [ ] `/etc/dns.conf`

#### Q. How do you display all listening TCP ports and their associated processes?

* [ ] `ss -uplt`
* [ ] `netstat -ulpn`
* [x] `ss -tulpn`
* [ ] `lsof -i udp`
* [ ] `iptables -L -n`

#### Q. To permanently assign a static IP to `eth0` on a Debian-based system, which file would you edit?

* [x] `/etc/network/interfaces`
* [ ] `/etc/sysconfig/network-scripts/ifcfg-eth0`
* [ ] `/etc/netplan/config.yaml`
* [ ] `/etc/dhcp/dhclient.conf`
* [ ] `/etc/NetworkManager/system-connections/eth0.nmconnection`

#### Q. What command tests connectivity and reports round-trip time to a host?

* [ ] `traceroute`
* [x] `ping`
* [ ] `dig`
* [ ] `nslookup`
* [ ] `arping`

#### Q. Which utility shows real-time bandwidth usage per network interface?

* [x] `iftop`
* [ ] `nethogs`
* [ ] `nload`
* [ ] `iperf`
* [ ] `netcat`

#### Q. How do you flush all IPv4 routes from the routing table?

* [ ] `ip route flush all`
* [x] `ip route flush table main`
* [ ] `route del default`
* [ ] `ifdown --flush`
* [ ] `netstat -r --flush`

#### Q. In `/etc/hosts`, what does the line `127.0.0.1   localhost` achieve?

* [ ] Maps `localhost` to the public IP of the host
* [x] Resolves `localhost` to the loopback interface
* [ ] Routes all traffic to `localhost` through the router
* [ ] Disables DNS lookup for `localhost`
* [ ] Assigns a virtual IP for containers

#### Q. Which command captures packets on `eth0` and writes them to `capture.pcap`?

* [ ] `tcpdump -w eth0 capture.pcap`
* [x] `tcpdump -i eth0 -w capture.pcap`
* [ ] `wireshark -i eth0 -o capture.pcap`
* [ ] `snort -c eth0 capture.pcap`
* [ ] `nmap -sP eth0 -o capture.pcap`

#### Q. What is the purpose of the `mtu` parameter in network interface configuration?

* [ ] Maximum Transfer Unit - defines maximum bandwidth
* [x] Maximum Transmission Unit - defines maximum packet size
* [ ] Memory Transfer Unit - defines buffer size
* [ ] Multiple Terminal Unit - defines connection count
* [ ] Message Transfer Unit - defines protocol type

#### Q. Which command adds a static route to network `192.168.10.0/24` via gateway `192.168.1.1`?

* [ ] `route add -net 192.168.10.0/24 gw 192.168.1.1`
* [x] `ip route add 192.168.10.0/24 via 192.168.1.1`
* [ ] `netstat -r 192.168.10.0/24 192.168.1.1`
* [ ] `ifroute add 192.168.10.0/24 192.168.1.1`
* [ ] `gateway add 192.168.10.0/24 192.168.1.1`

#### Q. Which file contains the system's hostname on most Linux distributions?

* [ ] `/etc/hosts`
* [x] `/etc/hostname`
* [ ] `/etc/sysconfig/network`
* [ ] `/proc/sys/kernel/hostname`
* [ ] `/etc/machine-info`

#### Q. What does the command `ip link set eth0 down` accomplish?

* [ ] Removes IP address from eth0
* [x] Disables the eth0 network interface
* [ ] Deletes the eth0 interface permanently
* [ ] Sets eth0 to promiscuous mode
* [ ] Flushes the ARP cache for eth0

#### Q. Which protocol does the `dig` command primarily use for DNS queries?

* [ ] TCP only
* [x] UDP (with TCP fallback)
* [ ] ICMP
* [ ] HTTP
* [ ] DHCP

#### Q. In iptables, what does the `-j DROP` action do to packets?

* [ ] Forwards packets to another chain
* [ ] Logs packet information and continues
* [x] Silently discards the packet
* [ ] Sends ICMP unreachable message
* [ ] Redirects packet to localhost

#### Q. Which command shows network interface statistics including packet counts and errors?

* [ ] `ip addr`
* [x] `ip -s link`
* [ ] `netstat -r`
* [ ] `ss -i`
* [ ] `ifconfig -v`

#### Q. What is the default DHCP client configuration file on Ubuntu systems?

* [ ] `/etc/dhcpcd.conf`
* [ ] `/etc/network/dhcp.conf`
* [x] `/etc/dhcp/dhclient.conf`
* [ ] `/etc/netplan/dhcp.conf`
* [ ] `/etc/systemd/network/dhcp.conf`

#### Q. Which command displays the current ARP table entries?

* [ ] `route -n`
* [x] `ip neigh show`
* [ ] `netstat -arp`
* [ ] `ss -arp`
* [ ] `ifconfig -arp`

#### Q. How do you enable IP forwarding temporarily on a Linux system?

* [ ] `ip forward enable`
* [x] `echo 1 > /proc/sys/net/ipv4/ip_forward`
* [ ] `sysctl net.ipv4.ip_forward=1`
* [ ] `iptables -A FORWARD -j ACCEPT`
* [ ] `netfilter --enable-forward`

#### Q. Which port does SSH typically use for connections?

* [ ] 21
* [x] 22
* [ ] 23
* [ ] 25
* [ ] 80

#### Q. What does the `netstat -tulpn` command display?

* [ ] Only UDP connections
* [x] TCP and UDP listening ports with process information
* [ ] Only TCP connections
* [ ] Network interface statistics
* [ ] Routing table information

#### Q. Which configuration directive in `/etc/resolv.conf` specifies the DNS search domain?

* [ ] `nameserver`
* [x] `search`
* [ ] `domain`
* [ ] `options`
* [ ] `sortlist`

#### Q. How do you test if a specific TCP port is open on a remote host using netcat?

* [ ] `nc -u hostname port`
* [x] `nc -zv hostname port`
* [ ] `nc -l hostname port`
* [ ] `nc -s hostname port`
* [ ] `nc -p hostname port`

#### Q. Which systemd service manages network connections on modern Linux distributions?

* [ ] `network.service`
* [x] `NetworkManager.service`
* [ ] `networking.service`
* [ ] `systemd-networkd.service`
* [ ] `ifupdown.service`

#### Q. What does the `traceroute` command accomplish?

* [ ] Tests bandwidth between hosts
* [x] Shows the path packets take to reach a destination
* [ ] Captures network packets
* [ ] Displays network interface configuration
* [ ] Monitors real-time traffic

#### Q. In a CIDR notation `192.168.1.0/24`, what does the `/24` represent?

* [ ] The host portion of the address
* [x] The number of network bits in the subnet mask
* [ ] The maximum number of hosts
* [ ] The VLAN identifier
* [ ] The default gateway address

#### Q. Which command creates a network namespace named `test`?

* [ ] `ip netns create test`
* [x] `ip netns add test`
* [ ] `netns create test`
* [ ] `namespace add test`
* [ ] `ip namespace create test`

#### Q. What is the purpose of the loopback interface (`lo`)?

* [ ] External network communication
* [x] Internal system communication and testing
* [ ] Wireless network management
* [ ] VPN connections
* [ ] Bridge configuration

#### Q. Which file would you modify to make network interface changes persistent on CentOS/RHEL systems?

* [ ] `/etc/network/interfaces`
* [x] `/etc/sysconfig/network-scripts/ifcfg-ethX`
* [ ] `/etc/netplan/config.yaml`
* [ ] `/etc/systemd/network/ethX.network`
* [ ] `/etc/NetworkManager/conf.d/ethX.conf`

#### Q. How do you display only IPv6 addresses using the `ip` command?

* [ ] `ip -6 addr`
* [x] `ip -6 addr show`
* [ ] `ip addr show ipv6`
* [ ] `ip6 addr show`
* [ ] `ip addr -6`
