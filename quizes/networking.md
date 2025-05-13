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

* [ ] `/etc/network/interfaces`
* [ ] `/etc/sysconfig/network-scripts/ifcfg-eth0`
* [ ] `/etc/netplan/config.yaml`
* [x] `/etc/network/interfaces`
* [ ] `/etc/NetworkManager/system-connections/eth0.nmconnection`

#### Q. What command tests connectivity and reports round-trip time to a host?

* [ ] `traceroute`
* [x] `ping`
* [ ] `dig`
* [ ] `nslookup`
* [ ] `arping`

#### Q. Which utility shows real-time bandwidth usage per network interface?

* [ ] `iftop`
* [ ] `nethogs`
* [x] `iftop`
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
