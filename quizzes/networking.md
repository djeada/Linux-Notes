# Networking Quiz

Notes: [Networking](../notes/networking.md), [Ports](../notes/ports.md), [Firewalls](../notes/firewall.md)

Check your understanding of interfaces, addressing, routing, DNS, ports, firewalls and network troubleshooting.

#### Q. Which command is the modern way to show the IP addresses assigned to every network interface?

* [x] `ip addr show`
* [ ] `ifconfig -a`
* [ ] `netstat -i`
* [ ] `route -n`

> **Explanation:** `ip addr show` (or `ip a`) from iproute2 lists every interface with its IPv4 and IPv6 addresses. `ifconfig`, `netstat` and `route` come from the deprecated net-tools package, which many distributions no longer install by default.

#### Q. Which command lists interfaces with their MAC addresses and `UP`/`DOWN` state, but without IP addresses?

* [ ] `ip addr show`
* [ ] `ip route show`
* [x] `ip link show`
* [ ] `ip neigh show`

> **Explanation:** `ip link` works at the link layer: interface names, MAC addresses, MTU and state. `ip addr` adds the IP addresses, `ip route` shows routes and `ip neigh` shows the ARP/neighbour cache.

#### Q. Which command shows per-interface packet counts, including RX/TX errors and dropped packets?

* [x] `ip -s link`
* [ ] `ip addr`
* [ ] `ip route`
* [ ] `ss -s`

> **Explanation:** The `-s` flag adds statistics to `ip link`, showing bytes, packets, errors and drops per interface. `ss -s` summarises sockets, not interface counters.

#### Q. What does `sudo ip link set eth0 down` do?

* [ ] Removes the IP address from `eth0` but keeps the link up
* [x] Disables the `eth0` interface until it is brought up again
* [ ] Deletes the `eth0` interface from the system permanently
* [ ] Flushes the ARP cache entries learned on `eth0`

> **Explanation:** Setting a link `down` stops the interface from sending or receiving traffic; `ip link set eth0 up` re-enables it. The device and its IPv4 addresses remain configured, and the change does not survive a reboot.

#### Q. A web server works with `curl http://127.0.0.1` on the server itself. What does this prove?

* [x] The service answers on the loopback interface inside the same machine
* [ ] Remote clients can reach the server on port 80
* [ ] The default gateway is configured correctly
* [ ] DNS resolution for the server's hostname works

> **Explanation:** `127.0.0.1` is the loopback address: the machine talking to itself through `lo`. It confirms the service runs locally but says nothing about routing, DNS or firewalls for remote clients.

#### Q. A host on `192.168.1.0/24` with default gateway `192.168.1.1` sends a packet to `8.8.8.8` over Ethernet. Which addresses does the outgoing frame carry?

* [ ] Destination IP `192.168.1.1` and the router's MAC address
* [ ] Destination IP `8.8.8.8` and a MAC address belonging to `8.8.8.8`
* [x] Destination IP `8.8.8.8` and the gateway's MAC address
* [ ] Destination IP `8.8.8.8` and the broadcast MAC `ff:ff:ff:ff:ff:ff`

> **Explanation:** IP addresses identify the end points and stay the same along the path, while MAC addresses only matter on the local link. The host learns the gateway's MAC through ARP (`ip neigh`) and hands the frame to the router.

#### Q. Which of these addresses is a private IPv4 address, not routed on the public internet?

* [ ] `172.32.10.5`
* [ ] `192.169.1.5`
* [ ] `11.0.0.5`
* [x] `172.20.10.5`

> **Explanation:** The private ranges are `10.0.0.0/8`, `172.16.0.0/12` (`172.16.0.0` to `172.31.255.255`) and `192.168.0.0/16`. `172.32.x.x` falls just outside the 172.16/12 block, and `192.169.x.x` is not `192.168.x.x`.

#### Q. In `192.168.1.0/24`, how many usable host addresses are there?

* [ ] 24
* [x] 254
* [ ] 255
* [ ] 256

> **Explanation:** `/24` means 24 network bits, leaving 8 host bits, or $2^8 = 256$ addresses. The all-zeros network address and the all-ones broadcast address are reserved, leaving $2^8 - 2 = 254$ for hosts.

#### Q. A host has the address `192.168.1.10/24` and the default gateway `192.168.1.1`. How does it deliver packets to `192.168.1.77` and to `192.168.2.20`?

* [x] `192.168.1.77` directly on the local link; `192.168.2.20` through `192.168.1.1`
* [ ] Both directly on the local link, because they share the first two octets
* [ ] Both through `192.168.1.1`, because every packet goes to the gateway
* [ ] `192.168.2.20` directly on the local link; `192.168.1.77` through `192.168.1.1`

> **Explanation:** The `/24` prefix makes `192.168.1.0`–`192.168.1.255` the local network, so `.77` is reached directly. `192.168.2.20` is outside it and is sent to the gateway. `ip route get ADDRESS` shows which case applies.

#### Q. In what order do the four DHCP lease messages occur?

* [ ] Request, Offer, Discover, Acknowledge
* [ ] Offer, Discover, Acknowledge, Request
* [ ] Discover, Request, Offer, Acknowledge
* [x] Discover, Offer, Request, Acknowledge

> **Explanation:** The client broadcasts DHCPDISCOVER, a server replies with DHCPOFFER, the client asks for that address with DHCPREQUEST, and the server confirms the lease with DHCPACK (often remembered as DORA).

#### Q. A laptop shows the address `169.254.23.7` on its Ethernet interface. What is the most likely cause?

* [ ] The interface was given a static public IP address
* [ ] DNS is returning the wrong address for the hostname
* [x] The client failed to get a lease from a DHCP server
* [ ] The firewall is blocking outgoing ICMP traffic

> **Explanation:** `169.254.x.x` is a link-local address a host assigns itself when DHCP fails. Check the cable or Wi-Fi, `ip link`, `nmcli dev status` and the DHCP server.

#### Q. A printer must always get the same IP address, but you want to keep managing addresses centrally on the DHCP server. What should you configure?

* [ ] A shorter DHCP lease time on the printer
* [ ] A static route to the printer via the gateway
* [ ] An `/etc/hosts` entry on every client
* [x] A DHCP reservation for the printer's MAC address

> **Explanation:** A DHCP reservation makes the server always hand the same address to a given MAC address. The address stays stable without manual configuration on the device itself.

#### Q. Which command shows only the default route on a Linux system?

* [ ] `ip addr show default`
* [x] `ip route show default`
* [ ] `ip link show default`
* [ ] `ip neigh show default`

> **Explanation:** `ip route show default` prints a line such as `default via 192.168.1.1 dev eth0`, where the address after `via` is the default gateway. The default route matches any destination with no more specific route.

#### Q. A host has the routing table below. Which next hop does it use for a packet to `10.20.5.9`?

```text
default via 192.168.1.1 dev eth0
10.20.0.0/16 via 192.168.1.2 dev eth0
10.20.5.0/24 via 192.168.1.3 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10
```

* [ ] `192.168.1.1`, because the default route is listed first
* [ ] `192.168.1.2`, because `10.20.0.0/16` is the first matching route
* [x] `192.168.1.3`, because `10.20.5.0/24` is the longest matching prefix
* [ ] None; the packet is delivered directly on `eth0`

> **Explanation:** Linux picks the most specific route (longest prefix), not the first one listed. Both `/16` and `/24` match `10.20.5.9`, and `/24` is longer. `10.20.9.9` would use `192.168.1.2`, and `10.30.0.1` the default route.

#### Q. Which command prints the route, outgoing interface and source address the kernel would actually use to reach `8.8.8.8`?

* [ ] `ip route show 8.8.8.8`
* [ ] `ip neigh show 8.8.8.8`
* [ ] `traceroute -n 8.8.8.8`
* [x] `ip route get 8.8.8.8`

> **Explanation:** `ip route get` performs a real route lookup and prints a line such as `8.8.8.8 via 192.168.1.1 dev eth0 src 192.168.1.10`. `ip route show 8.8.8.8` lists only routes whose prefix is exactly that address, usually none.

#### Q. Which command adds a default gateway of `192.168.1.254` until the next reboot or network restart?

* [x] `sudo ip route add default via 192.168.1.254`
* [ ] `sudo ip addr add default 192.168.1.254`
* [ ] `sudo ip link set default via 192.168.1.254`
* [ ] `sudo ip route add 192.168.1.254 dev default`

> **Explanation:** Routes are managed with `ip route`, and `via` names the next-hop router. Changes made this way are runtime only; make them persistent through NetworkManager, netplan or the distribution's network files.

#### Q. Which command adds a route to `10.20.0.0/16` through the router `192.168.1.1`?

* [ ] `ip route add 192.168.1.1 via 10.20.0.0/16`
* [ ] `ip addr add 10.20.0.0/16 via 192.168.1.1`
* [x] `ip route add 10.20.0.0/16 via 192.168.1.1`
* [ ] `ip route add 10.20.0.0/16 dev 192.168.1.1`

> **Explanation:** The syntax is `ip route add DESTINATION via GATEWAY`. `dev` expects an interface name such as `eth0`, not an IP address.

#### Q. `ping 192.168.1.1` (the router) succeeds, but `ping 8.8.8.8` fails. What should you check first?

* [ ] The DNS servers in `/etc/resolv.conf`
* [ ] The MAC address of the local interface
* [ ] The entries in `/etc/hosts`
* [x] The default route and the path beyond the router

> **Explanation:** The local network works, but traffic to other networks does not. Check `ip route` for a correct default gateway and use `traceroute 8.8.8.8` to see where packets stop. DNS is not involved when pinging a raw IP.

#### Q. `ping 8.8.8.8` works, but `ping google.com` fails with "Name or service not known". What is the most likely problem?

* [x] Name resolution (DNS) is broken
* [ ] The interface is down
* [ ] The default gateway is missing
* [ ] ICMP is blocked by the firewall

> **Explanation:** Reaching an IP address proves the interface, routing and ICMP all work. Failing only on a name points to DNS. Inspect `/etc/resolv.conf`, `resolvectl status`, and compare `dig google.com` with `dig @8.8.8.8 google.com`.

#### Q. Which command queries a specific DNS server, `8.8.8.8`, directly and bypasses the system's configured resolver?

* [ ] `dig google.com 8.8.8.8`
* [x] `dig @8.8.8.8 google.com`
* [ ] `nslookup -server 8.8.8.8`
* [ ] `host -r 8.8.8.8 google.com`

> **Explanation:** `dig @SERVER NAME` sends the query to that server. If this works while plain `dig google.com` fails, the locally configured resolver is the problem. Without `@`, `dig` treats `8.8.8.8` as a second name to look up.

#### Q. Which file traditionally lists the DNS servers the resolver uses, via `nameserver` lines?

* [ ] `/etc/hosts`
* [ ] `/etc/hostname`
* [x] `/etc/resolv.conf`
* [ ] `/etc/nsswitch.conf`

> **Explanation:** `/etc/resolv.conf` holds `nameserver` and `search` lines. On many modern systems it is generated by NetworkManager or systemd-resolved, so manual edits may be overwritten. `/etc/nsswitch.conf` sets lookup order, not servers.

#### Q. On Ubuntu with systemd-resolved, `/etc/resolv.conf` contains only `nameserver 127.0.0.53`. Which command shows the upstream DNS servers actually in use per interface?

* [ ] `cat /etc/hostname`
* [ ] `ip route show`
* [ ] `nmcli con reload`
* [x] `resolvectl status`

> **Explanation:** `127.0.0.53` is systemd-resolved's local stub resolver, which forwards queries to the real servers. `resolvectl status` shows the upstream servers configured for each link.

#### Q. In `/etc/resolv.conf`, which directive lists the domains appended to short names, so that `ping web1` can resolve `web1.corp.example`?

* [x] `search`
* [ ] `nameserver`
* [ ] `options`
* [ ] `sortlist`

> **Explanation:** `search corp.example` makes the resolver try `web1.corp.example` when you look up the short name `web1`. `nameserver` sets server addresses and `options` tunes resolver behaviour such as timeouts.

#### Q. You add `192.168.1.50 myserver.local` to `/etc/hosts`. What is the effect?

* [ ] DNS servers on the network start answering for `myserver.local`
* [ ] Traffic to `192.168.1.50` is routed through `myserver.local`
* [x] This machine resolves `myserver.local` locally, usually before asking DNS
* [ ] The machine's own hostname changes to `myserver.local`

> **Explanation:** `/etc/hosts` is a static, local name-to-IP table. The `hosts:` line in `/etc/nsswitch.conf` normally lists `files` before `dns`, so it is checked first. It affects only the machine where the file is edited.

#### Q. Which command resolves a name the same way applications do, following `/etc/nsswitch.conf` and therefore including `/etc/hosts`?

* [ ] `dig myserver.local`
* [ ] `host myserver.local`
* [ ] `nslookup myserver.local`
* [x] `getent hosts myserver.local`

> **Explanation:** `getent` goes through the system's NSS lookup order, like `ping` or `curl`. `dig`, `host` and `nslookup` only send DNS queries, so they can disagree with what applications see when `/etc/hosts` or other NSS sources are involved.

#### Q. With NetworkManager, which setting stops a connection from using the DNS servers handed out by DHCP?

* [ ] `ipv4.method manual`
* [x] `ipv4.ignore-auto-dns yes`
* [ ] `ipv4.never-default yes`
* [ ] `ipv4.dns-search ""`

> **Explanation:** After setting `ipv4.dns` with `nmcli con mod`, `ipv4.ignore-auto-dns yes` keeps the DHCP-supplied servers out. `ipv4.method manual` would turn off DHCP addressing entirely, not just DNS.

#### Q. Which `nmcli` command shows each network device and whether it is connected?

* [ ] `nmcli con reload`
* [ ] `nmcli con up eth0`
* [x] `nmcli dev status`
* [ ] `nmcli general hostname`

> **Explanation:** `nmcli dev status` lists devices with their type, state and active connection profile. `nmcli con show` lists saved connection profiles instead.

#### Q. You change the address of the active profile `eth0` with `nmcli con mod eth0 ipv4.addresses 192.168.1.20/24`, but `ip addr` still shows the old address. What applies the change?

* [ ] `nmcli con reload`
* [ ] `nmcli con show eth0`
* [ ] `ip link set eth0 up`
* [x] `nmcli con up eth0`

> **Explanation:** `nmcli con mod` only saves the profile; re-activating it with `nmcli con up` applies the new settings (`nmcli dev reapply` also works). `nmcli con reload` only re-reads profile files edited by hand on disk.

#### Q. Which command measures round-trip time to a host and stops after exactly five probes?

* [ ] `ping -w 5 example.com`
* [x] `ping -c 5 example.com`
* [ ] `traceroute -m 5 example.com`
* [ ] `ping -i 5 example.com`

> **Explanation:** `-c` sets the packet count. `-w 5` sets a five-second deadline instead, `-i 5` waits five seconds between packets, and `traceroute -m` limits hop count.

#### Q. What does `traceroute -n example.com` show?

* [ ] The bandwidth available on each link to the host
* [ ] Only the final destination's IP address
* [ ] The open ports on each router along the path
* [x] Each router hop on the path, as numeric IPs without DNS lookups

> **Explanation:** `traceroute` lists each hop and its latency, which helps locate where delay or loss begins. `-n` skips reverse DNS lookups, making the output faster and showing raw IPs. `tracepath` is a similar tool that needs no root.

#### Q. Which command shows listening TCP and UDP sockets with numeric ports and the process that owns each one?

* [x] `sudo ss -tulpn`
* [ ] `ss -tan`
* [ ] `ss -s`
* [ ] `sudo ss -tu state established`

> **Explanation:** `-t` TCP, `-u` UDP, `-l` listening only, `-p` owning process (needs root for other users' processes), `-n` numeric. `ss` replaces the older `netstat -tulpn`. `-tan` shows all TCP sockets without process names, and `-s` is a summary.

#### Q. `ss -tuln` shows `127.0.0.1:5432` in LISTEN state, and remote clients cannot connect. Why?

* [ ] Port 5432 is a well-known port that needs root
* [ ] The service is listening on UDP instead of TCP
* [x] The service is bound only to loopback, so it accepts local connections only
* [ ] The service is listening on every interface, which conflicts with routing

> **Explanation:** A socket bound to `127.0.0.1` is reachable only from the same machine. To accept remote clients the service must listen on `0.0.0.0`, `[::]` or a specific external address, and the firewall must allow the port.

#### Q. Which command shows which process is using TCP port 80?

* [ ] `sudo lsof /var/run/80`
* [ ] `sudo ss -s :80`
* [ ] `sudo netstat -r :80`
* [x] `sudo lsof -i :80`

> **Explanation:** `lsof -i :80` lists open network files on port 80 with the command, PID and user. `ss -s` only prints summary counts, and `netstat -r` shows routes.

#### Q. With OpenBSD netcat (the default `nc` on Ubuntu), which command checks whether TCP port 443 is open on `web01` without sending any data?

* [x] `nc -zv web01 443`
* [ ] `nc -l web01 443`
* [ ] `nc -u web01 443`
* [ ] `nc -p web01 443`

> **Explanation:** `-z` only checks for a listening daemon and `-v` reports the result, such as `Connection to web01 443 port [tcp/https] succeeded!`. `-l` makes `nc` listen locally, `-u` switches to UDP, and `-p` sets the local source port.

#### Q. Which port range contains the well-known ports such as 22, 80 and 443?

* [ ] 1024–49151
* [x] 0–1023
* [ ] 49152–65535
* [ ] 0–65535

> **Explanation:** Ports 0–1023 are well-known (SSH 22, HTTP 80, HTTPS 443). 1024–49151 are registered ports and 49152–65535 are dynamic/private. TCP and UDP each have their own 0–65535 space.

#### Q. Which service commonly uses port 53 over both UDP and TCP?

* [ ] SMTP
* [ ] DHCP
* [x] DNS
* [ ] SSH

> **Explanation:** DNS uses UDP 53 for most queries and TCP 53 for large responses and zone transfers. DHCP uses UDP 67/68, SMTP uses TCP 25 and SSH uses TCP 22.

#### Q. A program on Linux calls `bind()` on a TCP socket with port number 0. What happens?

* [x] The kernel assigns a free port from `net.ipv4.ip_local_port_range`
* [ ] The call fails, because port 0 is reserved
* [ ] The socket accepts connections on every port
* [ ] The socket gets port 1024, the first unprivileged port

> **Explanation:** Port 0 means "pick one for me". The kernel chooses an unused ephemeral port, by default from 32768–60999, which differs from IANA's 49152–65535 range. Check it with `sysctl net.ipv4.ip_local_port_range`.

#### Q. An `nmap` scan reports port 8080 as `filtered`. What does that mean?

* [x] Nmap cannot tell whether the port is open because packets are being filtered
* [ ] A service is accepting connections on the port
* [ ] The host is reachable but nothing listens on the port
* [ ] The host is down

> **Explanation:** `filtered` means a firewall or filter dropped the probes, so Nmap got no clear answer. `closed` means the host replied but nothing listens there; `open` means a service accepted the connection.

#### Q. You run `nmap 192.168.1.10` as an ordinary user, without `sudo`. Which TCP scan does Nmap perform?

* [ ] A SYN ("half-open") scan, the same as `-sS`
* [x] A full TCP connect scan, the same as `-sT`
* [ ] A UDP scan of the top ports, the same as `-sU`
* [ ] Host discovery only, the same as `-sn`

> **Explanation:** A SYN scan crafts raw packets, which needs root, so unprivileged Nmap falls back to completing normal `connect()` calls. With root, the default is a SYN scan. `-sn` skips port scanning entirely.

#### Q. Which command captures 100 packets on `eth0` and saves them to `capture.pcap` for later analysis in Wireshark?

* [ ] `sudo tcpdump -w eth0 -c 100 capture.pcap`
* [ ] `sudo tcpdump -r capture.pcap -i eth0 -c 100`
* [x] `sudo tcpdump -i eth0 -c 100 -w capture.pcap`
* [ ] `sudo tcpdump -i eth0 -c 100 > capture.pcap`

> **Explanation:** `-i` selects the interface, `-c` limits the packet count and `-w` writes raw packets to a file. `-r` reads a capture, and redirecting stdout saves text output, not a pcap file.

#### Q. Which command captures only HTTPS traffic between this machine and `192.168.1.20`?

* [ ] `sudo tcpdump -i eth0 host 192.168.1.20 or port 443`
* [ ] `sudo tcpdump -i eth0 port 192.168.1.20:443`
* [ ] `sudo tcpdump -i eth0 -c 443 host 192.168.1.20`
* [x] `sudo tcpdump -i eth0 host 192.168.1.20 and port 443`

> **Explanation:** Filter primitives combine with `and`, `or` and `not`. Using `or` would capture all traffic to that host plus all port 443 traffic. `port` takes only a number, and `-c 443` limits the capture to 443 packets.

#### Q. Which command enables IPv4 forwarding at runtime, so the machine can route packets between networks?

* [ ] `sudo ip link set ip_forward on`
* [x] `sudo sysctl -w net.ipv4.ip_forward=1`
* [ ] `sudo iptables -A FORWARD -j ACCEPT`
* [ ] `sudo sysctl -p net.ipv4.ip_forward`

> **Explanation:** `sysctl -w` changes the kernel parameter immediately; `cat /proc/sys/net/ipv4/ip_forward` then shows `1`. A FORWARD rule only filters forwarded packets and does not turn forwarding on.

#### Q. How do you make IPv4 forwarding survive a reboot?

* [ ] Run `echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward` once
* [ ] Run `sudo sysctl -w net.ipv4.ip_forward=1` once
* [x] Put `net.ipv4.ip_forward=1` in a file under `/etc/sysctl.d/` and run `sudo sysctl --system`
* [ ] Add `net.ipv4.ip_forward=1` to `/etc/environment` and log in again

> **Explanation:** Writing to `/proc` or using `sysctl -w` changes only the running kernel. Files in `/etc/sysctl.d/` are applied at boot, and `sysctl --system` loads them now. Ubuntu also reads `/etc/sysctl.conf` through the `99-sysctl.conf` symlink.

#### Q. What is the main purpose of NAT on a home router?

* [ ] To resolve hostnames to IP addresses
* [ ] To assign IP addresses to devices automatically
* [ ] To encrypt traffic leaving the local network
* [x] To let many devices with private addresses share one public IP address

> **Explanation:** Private addresses are not routed on the internet, so the router rewrites their source address to its public IP and tracks connections to map replies back. DNS resolves names and DHCP assigns addresses.

#### Q. A firewall rule uses `DROP` instead of `REJECT`. What does a client trying to connect over TCP experience?

* [x] No response, so the connection attempt hangs until it times out
* [ ] An immediate "connection refused" error
* [ ] A redirect to another port on the same server
* [ ] A successful connection with no data returned

> **Explanation:** `DROP` silently discards the packet. `REJECT` sends an error back, so the client fails quickly with "connection refused" or "unreachable". In UFW, `ufw deny` drops and `ufw reject` rejects.

#### Q. The INPUT chain contains a `LOG` rule followed by a `DROP` rule, both matching TCP port 23. What happens to a packet for port 23?

* [ ] It is logged and then accepted, because `LOG` ends rule processing
* [x] It is logged, then processing continues and the `DROP` rule discards it
* [ ] It is dropped without being logged, because `DROP` takes priority
* [ ] It is logged and sent back to the client as a rejection

> **Explanation:** `LOG` is a non-terminating target: it writes a kernel log entry and lets the packet continue to the next rule. `ACCEPT`, `DROP` and `REJECT` are terminating and stop evaluation. Rate-limit `LOG` rules to avoid flooding logs.

#### Q. The INPUT chain contains these rules, checked in this order. What happens to a new SSH connection on port 22?

```text
1  DROP    all  --  0.0.0.0/0  0.0.0.0/0
2  ACCEPT  tcp  --  0.0.0.0/0  0.0.0.0/0  tcp dpt:22
```

* [ ] It is accepted, because the more specific rule wins
* [ ] It is accepted, because ACCEPT rules override DROP rules
* [x] It is dropped, because rule 1 matches first
* [ ] It falls through to the chain's default policy

> **Explanation:** iptables evaluates rules top to bottom and stops at the first matching terminating rule. Rule 1 matches everything, so the SSH rule is never reached. Insert the ACCEPT above it with `iptables -I INPUT 1 ...`.

#### Q. A web server on this host listens on TCP port 80. Which `iptables` rule lets clients connect to it?

* [ ] `sudo iptables -A INPUT -p tcp --sport 80 -j ACCEPT`
* [ ] `sudo iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT`
* [ ] `sudo iptables -A FORWARD -p tcp --dport 80 -j ACCEPT`
* [x] `sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT`

> **Explanation:** Traffic addressed to this host passes the INPUT chain, and a client's request has destination port 80. `--sport 80` would match replies from remote web servers, OUTPUT covers traffic this host sends, and FORWARD handles traffic routed through it.

#### Q. On Ubuntu 24.04, `iptables -V` prints `iptables v1.8.10 (nf_tables)`. What does `(nf_tables)` mean?

* [x] The `iptables` command translates rules into the kernel's nftables framework
* [ ] The legacy iptables kernel tables are in use and nftables is disabled
* [ ] `iptables` rules are ignored, and only `nft` rules take effect
* [ ] The rules are stored by UFW in `/etc/nftables.conf`

> **Explanation:** Modern distributions ship `iptables-nft`, which keeps the iptables syntax but programs nftables underneath. The same rules then appear in `sudo nft list ruleset`. UFW and firewalld also sit on top of this framework.

#### Q. You are about to run `sudo ufw default deny incoming` and `sudo ufw enable` on a remote server over SSH. What should you do first?

* [ ] Run `sudo ufw disable`
* [x] Run `sudo ufw allow ssh`
* [ ] Run `sudo ufw default deny outgoing`
* [ ] Run `sudo ufw delete allow ssh`

> **Explanation:** With incoming traffic denied by default, enabling UFW without an SSH rule can lock you out of the server. Allow SSH (or your custom SSH port) before enabling the firewall, and test a new session before closing the old one.

#### Q. `sudo ufw status numbered` shows the rules below. Can `203.0.113.25` connect over SSH?

```text
     To        Action      From
     --        ------      ----
[ 1] 22/tcp    DENY IN     Anywhere
[ 2] 22/tcp    ALLOW IN    203.0.113.25
```

* [ ] Yes, because the rule naming a specific source is more specific
* [ ] Yes, because ALLOW rules are checked before DENY rules
* [x] No, because UFW applies the first matching rule
* [ ] No, because UFW blocks port 22 unless `ufw limit ssh` is used

> **Explanation:** UFW rules are evaluated in order and the first match wins, so rule 1 drops the connection. Put the specific rule first, for example `sudo ufw insert 1 allow from 203.0.113.25 to any port 22 proto tcp`.

#### Q. After `sudo ufw deny 631/tcp`, `sudo ss -tln` still shows `0.0.0.0:631` in LISTEN state. What does this mean?

* [ ] The UFW rule failed, because the port is still open
* [x] The firewall filters packets but does not stop the service from listening
* [ ] UFW rules apply only after the service is restarted
* [ ] `ss` shows cached data until the next reboot

> **Explanation:** A firewall rule decides which packets reach the socket; the program keeps listening. Test the block from another host (for example with `nc -zv`), and stop or disable the service if it is not needed at all.

#### Q. You run `sudo firewall-cmd --permanent --add-service=http`, but HTTP is still blocked. What is missing?

* [ ] `sudo firewall-cmd --runtime-to-permanent`
* [ ] `sudo systemctl disable firewalld`
* [ ] `sudo firewall-cmd --add-port=http`
* [x] `sudo firewall-cmd --reload`

> **Explanation:** `--permanent` writes the rule to the saved configuration but does not change the running firewall. `--reload` loads the permanent configuration into the runtime. `--runtime-to-permanent` copies in the opposite direction.

#### Q. A firewalld zone shows the settings below. Which clients can reach HTTPS on this host?

```text
public (active)
  services: ssh https
  rich rules:
    rule family="ipv4" source address="10.0.0.0/8" service name="https" accept
```

* [ ] Only clients in `10.0.0.0/8`, because the rich rule narrows the service
* [x] Any client, because the `https` service entry already allows every source
* [ ] No client, because the service entry and the rich rule conflict
* [ ] Only clients in `10.0.0.0/8`, because rich rules override zone services

> **Explanation:** Zone services and accept rich rules add permissions; neither restricts the other. To limit HTTPS to `10.0.0.0/8`, remove the service with `--remove-service=https` and keep only the rich rule, then reload.
