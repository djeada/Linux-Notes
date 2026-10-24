# Networking Quiz

Notes: [Networking](../notes/networking.md), [Ports](../notes/ports.md), [Firewalls](../notes/firewall.md)

Check your understanding of interfaces, addressing, routing, DNS, ports, firewalls and network troubleshooting.

#### Q. Which command is the modern way to show the IP addresses assigned to every network interface?

* [ ] `ifconfig -a`
* [x] `ip addr show`
* [ ] `netstat -i`
* [ ] `route -n`

> **Explanation:** `ip addr show` (or `ip a`) lists every interface with its IPv4 and IPv6 addresses. `ifconfig` is deprecated on many distributions, `netstat -i` shows interface counters, and `route -n` shows the routing table.

#### Q. Which command lists interfaces with their MAC addresses and `UP`/`DOWN` state, but without IP addresses?

* [ ] `ip addr show`
* [x] `ip link show`
* [ ] `ip route show`
* [ ] `ip neigh show`

> **Explanation:** `ip link` works at the link layer: interface names, MAC addresses, MTU and state. `ip addr` adds the IP addresses, `ip route` shows routes and `ip neigh` shows the ARP/neighbour cache.

#### Q. Which command shows per-interface packet counts, including RX/TX errors and dropped packets?

* [ ] `ip addr`
* [x] `ip -s link`
* [ ] `ip route`
* [ ] `ss -s`

> **Explanation:** The `-s` flag adds statistics to `ip link`, showing bytes, packets, errors and drops per interface. `ss -s` summarises sockets, not interface counters.

#### Q. What does `sudo ip link set eth0 down` do?

* [ ] Removes the IP address from `eth0` but keeps the link up
* [x] Disables the `eth0` interface until it is brought up again
* [ ] Deletes the `eth0` interface from the system permanently
* [ ] Flushes the ARP cache entries learned on `eth0`

> **Explanation:** Setting a link `down` stops the interface from sending or receiving traffic; `ip link set eth0 up` re-enables it. The change is not persistent and does not delete the device.

#### Q. A web server works with `curl http://127.0.0.1` on the server itself. What does this prove?

* [ ] Remote clients can reach the server on port 80
* [x] The service answers on the loopback interface inside the same machine
* [ ] The default gateway is configured correctly
* [ ] DNS resolution for the server's hostname works

> **Explanation:** `127.0.0.1` is the loopback address: the machine talking to itself through `lo`. It confirms the service runs locally but says nothing about routing, DNS or firewalls for remote clients.

#### Q. Which of these addresses is a private IPv4 address, not routed on the public internet?

* [ ] `172.32.10.5`
* [x] `172.20.10.5`
* [ ] `192.169.1.5`
* [ ] `11.0.0.5`

> **Explanation:** The private ranges are `10.0.0.0/8`, `172.16.0.0` to `172.31.255.255`, and `192.168.0.0/16`. `172.32.x.x` falls just outside the 172.16/12 block, and `192.169.x.x` is not `192.168.x.x`.

#### Q. In `192.168.1.0/24`, how many usable host addresses are there?

* [ ] 24
* [ ] 255
* [x] 254
* [ ] 256

> **Explanation:** `/24` means 24 network bits, leaving 8 host bits, or $2^8 = 256$ addresses. The all-zeros network address and the all-ones broadcast address are reserved, leaving $2^8 - 2 = 254$ for hosts.

#### Q. What is the job of a subnet mask or prefix length such as `/24`?

* [ ] It encrypts traffic between hosts on the same network
* [x] It splits an IP address into its network part and host part
* [ ] It assigns the MAC address used on the local link
* [ ] It selects the DNS server used for name lookups

> **Explanation:** The mask tells the host which leading bits identify the network. Addresses with the same network part are reached directly; everything else is sent to the default gateway.

#### Q. In what order do the four DHCP lease messages occur?

* [ ] Request, Offer, Discover, Acknowledge
* [x] Discover, Offer, Request, Acknowledge
* [ ] Offer, Discover, Acknowledge, Request
* [ ] Discover, Request, Offer, Acknowledge

> **Explanation:** The client broadcasts DHCPDISCOVER, a server replies with DHCPOFFER, the client asks for that address with DHCPREQUEST, and the server confirms the lease with DHCPACK (often remembered as DORA).

#### Q. A laptop shows the address `169.254.23.7` on its Ethernet interface. What is the most likely cause?

* [ ] The interface was given a static public IP address
* [x] The client failed to get a lease from a DHCP server
* [ ] DNS is returning the wrong address for the hostname
* [ ] The firewall is blocking outgoing ICMP traffic

> **Explanation:** `169.254.x.x` is a link-local address a host assigns itself when DHCP fails. Check the cable or Wi-Fi, `ip link`, `nmcli dev status` and the DHCP server.

#### Q. A printer must always get the same IP address, but you want to keep managing addresses centrally on the DHCP server. What should you configure?

* [ ] A shorter DHCP lease time on the printer
* [x] A DHCP reservation for the printer's MAC address
* [ ] A static route to the printer via the gateway
* [ ] An `/etc/hosts` entry on every client

> **Explanation:** A DHCP reservation makes the server always hand the same address to a given MAC address. The address stays stable without manual configuration on the device itself.

#### Q. Which command shows only the default route on a Linux system?

* [ ] `ip addr show default`
* [x] `ip route show default`
* [ ] `ip link show default`
* [ ] `ip neigh show default`

> **Explanation:** `ip route show default` prints a line such as `default via 192.168.1.1 dev eth0`, where the address after `via` is the default gateway. The default route matches any destination with no more specific route.

#### Q. In the output of `route -n`, which entry is the default gateway?

* [ ] Destination `0.0.0.0` with Genmask `255.255.255.255`
* [x] Destination `0.0.0.0` with Genmask `0.0.0.0`
* [ ] Destination `127.0.0.0` with Genmask `255.0.0.0`
* [ ] Destination `192.168.1.0` with Genmask `255.255.255.0`

> **Explanation:** A destination of `0.0.0.0/0` (mask `0.0.0.0`) matches every address, so it is the catch-all default route. A `192.168.1.0/24` entry is the directly connected local network.

#### Q. Which command adds a default gateway of `192.168.1.254` until the next reboot or network restart?

* [ ] `sudo ip addr add default 192.168.1.254`
* [x] `sudo ip route add default via 192.168.1.254`
* [ ] `sudo ip link set default via 192.168.1.254`
* [ ] `sudo ip route add 192.168.1.254 dev default`

> **Explanation:** Routes are managed with `ip route`, and `via` names the next-hop router. Changes made this way are runtime only; make them persistent through NetworkManager, netplan or the distribution's network files.

#### Q. Which command adds a route to `10.20.0.0/16` through the router `192.168.1.1`?

* [ ] `ip route add 192.168.1.1 via 10.20.0.0/16`
* [x] `ip route add 10.20.0.0/16 via 192.168.1.1`
* [ ] `ip addr add 10.20.0.0/16 via 192.168.1.1`
* [ ] `ip route add 10.20.0.0/16 dev 192.168.1.1`

> **Explanation:** The syntax is `ip route add DESTINATION via GATEWAY`. `dev` expects an interface name such as `eth0`, not an IP address.

#### Q. `ping 192.168.1.1` (the router) succeeds, but `ping 8.8.8.8` fails. What should you check first?

* [ ] The DNS servers in `/etc/resolv.conf`
* [x] The default route and the path beyond the router
* [ ] The MAC address of the local interface
* [ ] The entries in `/etc/hosts`

> **Explanation:** The local network works, but traffic to other networks does not. Check `ip route` for a correct default gateway and use `traceroute 8.8.8.8` to see where packets stop. DNS is not involved when pinging a raw IP.

#### Q. `ping 8.8.8.8` works, but `ping google.com` fails with "Name or service not known". What is the most likely problem?

* [ ] The interface is down
* [x] Name resolution (DNS) is broken
* [ ] The default gateway is missing
* [ ] ICMP is blocked by the firewall

> **Explanation:** Reaching an IP address proves the interface, routing and ICMP all work. Failing only on a name points to DNS. Inspect `/etc/resolv.conf`, `resolvectl status`, and compare `dig google.com` with `dig @8.8.8.8 google.com`.

#### Q. Which command queries a specific DNS server, `8.8.8.8`, directly and bypasses the system's configured resolver?

* [ ] `dig google.com 8.8.8.8`
* [x] `dig @8.8.8.8 google.com`
* [ ] `nslookup -server 8.8.8.8`
* [ ] `host -r 8.8.8.8 google.com`

> **Explanation:** `dig @SERVER NAME` sends the query to that server. If this works while plain `dig google.com` fails, the locally configured resolver is the problem.

#### Q. Which file traditionally lists the DNS servers the resolver uses, via `nameserver` lines?

* [ ] `/etc/hosts`
* [x] `/etc/resolv.conf`
* [ ] `/etc/hostname`
* [ ] `/etc/nsswitch.conf`

> **Explanation:** `/etc/resolv.conf` holds `nameserver` and `search` lines. On many modern systems it is generated by NetworkManager or systemd-resolved, so manual edits may be overwritten. `/etc/nsswitch.conf` sets lookup order, not servers.

#### Q. On a system using systemd-resolved, which command shows the DNS servers actually in use per interface?

* [ ] `cat /etc/hostname`
* [x] `resolvectl status`
* [ ] `ip route show`
* [ ] `nmcli con reload`

> **Explanation:** With systemd-resolved, `/etc/resolv.conf` often only points at a local stub resolver (`127.0.0.53`). `resolvectl status` shows the real upstream servers configured for each link.

#### Q. In `/etc/resolv.conf`, which directive lists the domains appended to short names, so that `ping web1` can resolve `web1.corp.example`?

* [ ] `nameserver`
* [x] `search`
* [ ] `options`
* [ ] `sortlist`

> **Explanation:** `search corp.example` makes the resolver try `web1.corp.example` when you look up the short name `web1`. `nameserver` sets server addresses and `options` tunes resolver behaviour such as timeouts.

#### Q. You add `192.168.1.50 myserver.local` to `/etc/hosts`. What is the effect?

* [ ] DNS servers on the network start answering for `myserver.local`
* [x] This machine resolves `myserver.local` locally, usually before asking DNS
* [ ] Traffic to `192.168.1.50` is routed through `myserver.local`
* [ ] The machine's own hostname changes to `myserver.local`

> **Explanation:** `/etc/hosts` is a static, local name-to-IP table that is normally checked before DNS. It affects only the machine where the file is edited.

#### Q. With NetworkManager, which setting stops a connection from using the DNS servers handed out by DHCP?

* [ ] `ipv4.method manual`
* [x] `ipv4.ignore-auto-dns yes`
* [ ] `ipv4.never-default yes`
* [ ] `ipv4.dns-search ""`

> **Explanation:** After setting `ipv4.dns` with `nmcli con mod`, `ipv4.ignore-auto-dns yes` keeps the DHCP-supplied servers out. `ipv4.method manual` would turn off DHCP addressing entirely, not just DNS.

#### Q. Which `nmcli` command shows each network device and whether it is connected?

* [ ] `nmcli con reload`
* [x] `nmcli dev status`
* [ ] `nmcli con up eth0`
* [ ] `nmcli general hostname`

> **Explanation:** `nmcli dev status` lists devices with their type, state and active connection profile. `nmcli con show` lists saved connection profiles instead.

#### Q. You created a profile with `nmcli con add ... ipv4.method manual ipv4.addresses 192.168.1.10/24`. What must you do for it to take effect now?

* [ ] Run `nmcli con reload`
* [x] Run `nmcli con up <profile-name>`
* [ ] Run `ip link set eth0 up`
* [ ] Reboot the machine

> **Explanation:** Creating or modifying a profile only saves it. `nmcli con up <name>` activates it on the interface. `nmcli con reload` re-reads profile files from disk but does not activate anything.

#### Q. Which command measures round-trip time to a host and stops after exactly five probes?

* [ ] `ping -w 5 example.com`
* [x] `ping -c 5 example.com`
* [ ] `traceroute -m 5 example.com`
* [ ] `ping -i 5 example.com`

> **Explanation:** `-c` sets the packet count. `-w 5` sets a five-second deadline instead, `-i 5` waits five seconds between packets, and `traceroute -m` limits hop count.

#### Q. What does `traceroute -n example.com` show?

* [ ] The bandwidth available on each link to the host
* [x] Each router hop on the path, as numeric IPs without DNS lookups
* [ ] Only the final destination's IP address
* [ ] The open ports on each router along the path

> **Explanation:** `traceroute` lists each hop and its latency, which helps locate where delay or loss begins. `-n` skips reverse DNS lookups, making the output faster and showing raw IPs.

#### Q. Which command shows listening TCP and UDP sockets with numeric ports and the process that owns each one?

* [ ] `ss -tan`
* [x] `sudo ss -tulpn`
* [ ] `ss -s`
* [ ] `sudo ss -tu state established`

> **Explanation:** `-t` TCP, `-u` UDP, `-l` listening only, `-p` owning process (needs root for other users' processes), `-n` numeric. `-tan` shows all TCP sockets without process names, and `-s` is a summary.

#### Q. `ss -tuln` shows `127.0.0.1:5432` in LISTEN state, and remote clients cannot connect. Why?

* [ ] Port 5432 is a well-known port that needs root
* [x] The service is bound only to loopback, so it accepts local connections only
* [ ] The service is listening on UDP instead of TCP
* [ ] The service is listening on every interface, which conflicts with routing

> **Explanation:** A socket bound to `127.0.0.1` is reachable only from the same machine. To accept remote clients the service must listen on `0.0.0.0`, `[::]` or a specific external address, and the firewall must allow the port.

#### Q. Which command shows which process is using TCP port 80?

* [ ] `sudo lsof /var/run/80`
* [x] `sudo lsof -i :80`
* [ ] `sudo ss -s :80`
* [ ] `sudo netstat -r :80`

> **Explanation:** `lsof -i :80` lists open network files on port 80 with the command, PID and user. `ss -s` only prints summary counts, and `netstat -r` shows routes.

#### Q. Which `nc` command checks whether TCP port 443 is open on `web01` without sending any data?

* [ ] `nc -l web01 443`
* [x] `nc -zv web01 443`
* [ ] `nc -u web01 443`
* [ ] `nc -p web01 443`

> **Explanation:** `-z` scans for a listening daemon without sending data and `-v` reports the result. `-l` makes `nc` listen locally, `-u` switches to UDP, and `-p` sets the source port.

#### Q. Which port range contains the well-known ports such as 22, 80 and 443?

* [ ] 1024–49151
* [x] 0–1023
* [ ] 49152–65535
* [ ] 0–65535

> **Explanation:** Ports 0–1023 are well-known (SSH 22, HTTP 80, HTTPS 443). 1024–49151 are registered ports and 49152–65535 are dynamic/private. TCP and UDP each have their own 0–65535 space.

#### Q. Which service commonly uses port 53 over both UDP and TCP?

* [ ] SMTP
* [x] DNS
* [ ] DHCP
* [ ] SSH

> **Explanation:** DNS uses UDP 53 for most queries and TCP 53 for large responses and zone transfers. DHCP uses UDP 67/68, SMTP uses TCP 25 and SSH uses TCP 22.

#### Q. An `nmap` scan reports port 8080 as `filtered`. What does that mean?

* [ ] A service is accepting connections on the port
* [x] Nmap cannot tell whether the port is open because packets are being filtered
* [ ] The host is reachable but nothing listens on the port
* [ ] The host is down

> **Explanation:** `filtered` means a firewall or filter dropped the probes, so Nmap got no clear answer. `closed` means the host replied but nothing listens there; `open` means a service accepted the connection.

#### Q. Which command captures 100 packets on `eth0` and saves them to `capture.pcap` for later analysis in Wireshark?

* [ ] `sudo tcpdump -w eth0 -c 100 capture.pcap`
* [x] `sudo tcpdump -i eth0 -c 100 -w capture.pcap`
* [ ] `sudo tcpdump -r capture.pcap -i eth0 -c 100`
* [ ] `sudo tcpdump -i eth0 -c 100 > capture.pcap`

> **Explanation:** `-i` selects the interface, `-c` limits the packet count and `-w` writes raw packets to a file. `-r` reads a capture, and redirecting stdout saves text output, not a pcap file.

#### Q. Which `tcpdump` filter captures only DNS traffic on `eth0`?

* [ ] `sudo tcpdump -i eth0 icmp`
* [x] `sudo tcpdump -i eth0 port 53`
* [ ] `sudo tcpdump -i eth0 port 80`
* [ ] `sudo tcpdump -i eth0 host 53`

> **Explanation:** DNS uses port 53, so `port 53` matches its UDP and TCP traffic. `host` expects an IP address or hostname, not a port number.

#### Q. Which command enables IPv4 forwarding at runtime, so the machine can route packets between networks?

* [ ] `sudo ip link set ip_forward on`
* [x] `sudo sysctl -w net.ipv4.ip_forward=1`
* [ ] `sudo iptables -A FORWARD -j ACCEPT`
* [ ] `sudo sysctl -p net.ipv4.ip_forward`

> **Explanation:** `sysctl -w` changes the kernel parameter immediately; `cat /proc/sys/net/ipv4/ip_forward` then shows `1`. A FORWARD rule only filters forwarded packets and does not turn forwarding on.

#### Q. How do you make IPv4 forwarding survive a reboot?

* [ ] Run `echo 1 > /proc/sys/net/ipv4/ip_forward` once
* [x] Add `net.ipv4.ip_forward=1` to `/etc/sysctl.conf` and run `sysctl -p`
* [ ] Add `ip_forward=yes` to `/etc/resolv.conf`
* [ ] Run `sudo sysctl -w net.ipv4.ip_forward=1` once

> **Explanation:** Writing to `/proc` or using `sysctl -w` changes only the running kernel. Settings in `/etc/sysctl.conf` (or `/etc/sysctl.d/`) are applied at boot, and `sysctl -p` loads them now.

#### Q. What is the main purpose of NAT on a home router?

* [ ] To resolve hostnames to IP addresses
* [x] To let many devices with private addresses share one public IP address
* [ ] To assign IP addresses to devices automatically
* [ ] To encrypt traffic leaving the local network

> **Explanation:** Private addresses are not routed on the internet, so the router rewrites their source address to its public IP and tracks connections to map replies back. DNS resolves names and DHCP assigns addresses.

#### Q. A firewall rule uses `DROP` instead of `REJECT`. What does a client trying to connect experience?

* [ ] An immediate "connection refused" error
* [x] No response, so the connection attempt hangs until it times out
* [ ] A redirect to another port on the same server
* [ ] A successful connection with no data returned

> **Explanation:** `DROP` silently discards the packet. `REJECT` sends an error back, so the client fails quickly with "connection refused" or "unreachable".

#### Q. The INPUT chain contains these rules, checked in this order. What happens to a new SSH connection on port 22?

```text
1  DROP    all  --  0.0.0.0/0  0.0.0.0/0
2  ACCEPT  tcp  --  0.0.0.0/0  0.0.0.0/0  tcp dpt:22
```

* [ ] It is accepted, because the more specific rule wins
* [x] It is dropped, because rule 1 matches first
* [ ] It is accepted, because ACCEPT rules override DROP rules
* [ ] It falls through to the chain's default policy

> **Explanation:** iptables evaluates rules top to bottom and stops at the first matching terminating rule. Rule 1 matches everything, so the SSH rule is never reached. Insert the ACCEPT above it with `iptables -I`.

#### Q. Which command allows incoming HTTP traffic by appending a rule to the INPUT chain?

* [ ] `sudo iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT`
* [x] `sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT`
* [ ] `sudo iptables -D INPUT -p tcp --dport 80 -j ACCEPT`
* [ ] `sudo iptables -A FORWARD -p udp --dport 80 -j ACCEPT`

> **Explanation:** `-A INPUT` appends to the chain for traffic addressed to this host, `-p tcp --dport 80` matches HTTP, and `-j ACCEPT` allows it. `-D` deletes a rule, and FORWARD handles traffic routed through the host.

#### Q. You are about to run `sudo ufw default deny incoming` and `sudo ufw enable` on a remote server over SSH. What should you do first?

* [ ] Run `sudo ufw disable`
* [x] Run `sudo ufw allow ssh`
* [ ] Run `sudo ufw default deny outgoing`
* [ ] Run `sudo ufw delete allow ssh`

> **Explanation:** With incoming traffic denied by default, enabling UFW without an SSH rule can lock you out of the server. Allow SSH (or your custom SSH port) before enabling the firewall.

#### Q. You run `sudo firewall-cmd --permanent --add-service=http`, but HTTP is still blocked. What is missing?

* [ ] `sudo firewall-cmd --runtime-to-permanent`
* [x] `sudo firewall-cmd --reload`
* [ ] `sudo systemctl disable firewalld`
* [ ] `sudo firewall-cmd --add-port=http`

> **Explanation:** `--permanent` writes the rule to the saved configuration but does not change the running firewall. `--reload` loads the permanent configuration into the runtime. `--runtime-to-permanent` copies in the opposite direction.
