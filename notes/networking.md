## Networking

Networking is the practice of connecting computers, servers, phones, routers, printers, and other devices so they can communicate and exchange data.

A network can be very small, such as two computers connected together, or very large, such as the internet. Most modern systems depend on networking in some way, whether for browsing websites, logging into remote servers, downloading software, sharing files, using cloud services, or communicating between applications.

At a basic level, networking answers questions like:

```text id="g4qlff"
How does one device find another device?
How does data move between devices?
How does a computer know where to send traffic?
How do names like google.com become IP addresses?
How do we troubleshoot when the network fails?
```

To understand networking, it is important to know the basic terms: network interfaces, MAC addresses, IP addresses, DHCP, DNS, routes, gateways, and common diagnostic commands.

### Network Interfaces

A network interface is the point where a computer connects to a network.

It may be a physical device, such as an Ethernet card or wireless card, or a virtual interface created by software.

A computer can have more than one network interface. For example, a laptop may have Wi-Fi, Ethernet, loopback, VPN, and virtual machine interfaces.

```text id="2n854w"
+--------------------------------------------------------+
|                      COMPUTER SYSTEM                   |
|                                                        |
|   +------------------------------------------------+   |
|   |                   OPERATING SYSTEM             |   |
|   |                                                |   |
|   |   +--------------+          +--------------+   |   |
|   |   | APPLICATION  |    <->   | APPLICATION  |   |   |
|   |   +--------------+          +--------------+   |   |
|   |                      ...                       |   |
|   |   +----------------------------------------+   |   |
|   |   |            NETWORK STACK               |   |   |
|   |   +----------------------------------------+   |   |
|   +------------------------------------------------+   |
|                |                       |               |
|        +-------+-------+       +-------+-------+       |
|        | NETWORK CARD  |       | WIRELESS CARD |       |
|        +---------------+       +---------------+       |
|                                                        |
+--------------------------------------------------------+
```

The operating system uses network interfaces to send and receive data.

Each interface usually has:

```text id="66wq1t"
a name
a MAC address
one or more IP addresses
a status, such as UP or DOWN
configuration settings
```

Common interface names include:

```text id="z1id2k"
lo        loopback interface
eth0      traditional Ethernet interface name
ens33     modern predictable Ethernet interface name
wlan0     wireless interface name
docker0   Docker bridge interface
tun0      VPN tunnel interface
```

#### Loopback Interface

The loopback interface is used for internal communication inside the same machine.

It is usually named:

```text id="md43cz"
lo
```

Its IPv4 address is usually:

```text id="6aexcn"
127.0.0.1
```

This address is also called localhost.

For example, if a web server is running on your own computer, you may be able to access it with:

```text id="bijjae"
http://127.0.0.1
```

or:

```text id="439ga7"
http://localhost
```

The loopback interface is not used to communicate with other devices. It is only for communication within the same system.

A simple way to think about it is:

```text id="c1vlh0"
127.0.0.1 = this computer talking to itself
```

#### Ethernet and Wireless Interfaces

An Ethernet interface connects a device to a wired network.

A wireless interface connects a device to a Wi-Fi network.

Examples:

```text id="b5b4r3"
eth0     older Ethernet naming style
ens33    common Ethernet name on virtual machines
wlan0    common wireless interface name
```

To see network interfaces on Linux, use:

```bash id="ui7vx9"
ip link show
```

Example output:

```text id="65maqh"
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
```

The important parts are:

```text id="gj6g1g"
eth0                  interface name
UP                    interface is enabled
LOWER_UP              physical link is detected
mtu 1500              maximum transmission unit
link/ether            MAC address follows
00:11:22:33:44:55     MAC address
```

If an interface is `DOWN`, it may be disabled or disconnected.

#### MAC Addresses

A MAC address is a hardware identifier assigned to a network interface.

MAC stands for Media Access Control.

It is used mainly for communication inside a local network. Devices on the same local network use MAC addresses to deliver frames to the correct network card.

A typical MAC address looks like this:

```text id="gkbj5e"
aa:bb:cc:dd:ee:ff
```

It is made of six pairs of hexadecimal digits.

```text id="s0lrhh"
+-----------------------------------------+
|   Manufacturer ID   | Device Identifier |
+-----------------------------------------+
         xx:xx:xx     :     xx:xx:xx
```

The first part often identifies the manufacturer or vendor. The second part identifies the individual device or adapter.

To view MAC addresses on Linux:

```bash id="iz6idd"
ip link show
```

Example:

```text id="6va1im"
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
```

Here, the MAC address is:

```text id="x2g57q"
00:11:22:33:44:55
```

MAC addresses are used on the local network. IP addresses are used for routing traffic between networks.

A useful comparison is:

```text id="ahgykh"
MAC address = local delivery identity
IP address  = network location identity
```

### IP Addresses

An IP address identifies a device on an IP network.

IP stands for Internet Protocol.

IP addresses allow devices to find and communicate with each other across local networks and the internet.

There are two main versions:

```text id="4gaedi"
IPv4    example: 192.168.1.10
IPv6    example: 2001:db8::10
```

These notes focus mostly on IPv4.

An IPv4 address is made of four numbers separated by dots. Each number ranges from 0 to 255.

Example:

```text id="9i2fwy"
192.168.1.10
```

```text id="msqre4"
IPv4 Address: 192.168.1.10

+-----+-----+-----+-----+
| 192 | 168 |  1  |  10 |
+-----+-----+-----+-----+
  |     |     |      |
  |     |     |      +--- Host part, often identifying a device
  |     |     +---------- Subnet portion
  |     +---------------- Private address space
  +---------------------- Network portion
```

The exact network and host portions depend on the subnet mask or prefix length.

For example:

```text id="0p8aov"
192.168.1.10/24
```

means the first 24 bits identify the network.

In everyday terms:

```text id="ydtjsz"
192.168.1.0/24 is the network
192.168.1.10 is one device on that network
```

#### Viewing IP Addresses

To show IPv4 addresses on Linux:

```bash id="ke5j46"
ip -4 address show
```

Example output:

```text id="zlal4v"
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.10/24 brd 192.168.1.255 scope global dynamic eth0
```

The important part is:

```text id="6esfjx"
inet 192.168.1.10/24
```

This means the interface has the IPv4 address:

```text id="4vnkkp"
192.168.1.10
```

with prefix length:

```text id="bo43c8"
24
```

The word `dynamic` often means the address was assigned using DHCP.

#### Private IP Addresses

Private IP addresses are used inside local networks.

They are not routed directly on the public internet.

Common private IPv4 ranges are:

```text id="cerd4v"
10.0.0.0       to 10.255.255.255
172.16.0.0     to 172.31.255.255
192.168.0.0    to 192.168.255.255
```

```text id="sksvnc"
       +---------------------------------+
       |       Private IP Address        |
       +---------------------------------+
       |                                 |
+------|---------++-----------------++---|-------------+
| 10.x.x.x       || 172.16.x.x      || 192.168.x.x     |
| to             || to              || to              |
| 10.255.255.255 || 172.31.255.255  || 192.168.255.255 |
+----------------++-----------------++-----------------+
   |                      |                 |
   |                      |                 +---- Common in home networks
   |                      |
   |                      +---------------------- Common in medium/large networks
   |
   +--------------------------------------------- Large private address space
```

Examples of private IP addresses:

```text id="y14jt5"
192.168.1.20
10.0.0.15
172.16.5.100
```

Private addresses are commonly used by homes, schools, companies, virtual machines, containers, and cloud private networks.

Because private IP addresses are not directly reachable from the internet, routers usually use NAT to allow private devices to access public websites.

#### Public IP Addresses

A public IP address identifies a network or device on the public internet.

Your home router usually has a public IP address assigned by your Internet Service Provider.

Devices inside your home usually have private IP addresses, such as:

```text id="lk97dk"
192.168.1.2
192.168.1.3
192.168.1.4
```

When those devices access the internet, the router translates their private addresses to the public address.

```text id="asq6wk"
                           Internet
                      +----------------+
                      |                |
                      |   WWW / Cloud  |
                      |                |
                      +--------+-------+
                               |
                               | Public IP
                               | e.g. 203.0.113.10
                               |
                      +--------+-------+
                      |    Router      |
             - - - -  +--------+-------+ - - - - -
           /                   |                   \
          /                    |                    \
      Private IP           Private IP            Private IP
   192.168.1.2          192.168.1.3          192.168.1.4
    Device A             Device B             Device C
```

To check your public IP from the command line, you can use an external service:

```bash id="t7e15c"
curl ifconfig.me
```

or:

```bash id="mve3vd"
curl icanhazip.com
```

Example output:

```text id="5bum9u"
203.0.113.10
```

Public IP addresses are visible on the internet, so systems using them should be protected with firewalls, secure configurations, and regular updates.

### DHCP

DHCP stands for Dynamic Host Configuration Protocol.

It automatically assigns network settings to devices.

Without DHCP, every device would need to be configured manually with:

```text id="be6hzt"
IP address
subnet mask or prefix
default gateway
DNS servers
```

That would be slow and error-prone, especially on large networks.

With DHCP, a device can join the network and automatically receive the settings it needs.

```text id="8tjaof"
Device joins network
        |
        v
Asks for network settings
        |
        v
DHCP server replies with IP configuration
        |
        v
Device can communicate on the network
```

#### DHCP Lease Process

The DHCP process usually has four main steps.

```text id="4t8qum"
Device (DHCP Client)                 DHCP Server
      |                                  |
      |    1. DHCPDISCOVER               |
      |--------------------------------->|
      |                                  |
      |    2. DHCPOFFER                  |
      |<---------------------------------|
      |                                  |
      |    3. DHCPREQUEST                |
      |--------------------------------->|
      |                                  |
      |    4. DHCPACK                    |
      |<---------------------------------|
      |                                  |
```

The steps are:

1. The client broadcasts a DHCPDISCOVER message, asking if any DHCP server is available.
2. The DHCP server replies with a DHCPOFFER, offering an IP address and settings.
3. The client sends a DHCPREQUEST, asking to use the offered address.
4. The server sends a DHCPACK, confirming the lease.

The assigned IP address is called a lease because it is usually temporary. The device can renew the lease before it expires.

#### Benefits of DHCP

DHCP is useful because it:

```text id="e445v8"
automates IP address assignment
reduces manual configuration errors
prevents duplicate IP addresses
works well for laptops, phones, tablets, and guest devices
makes large networks easier to manage
```

DHCP is especially helpful in networks where devices frequently join and leave.

#### Static IP Addresses and DHCP Reservations

Some devices need a stable IP address.

Examples include:

```text id="k1aia8"
servers
printers
routers
DNS servers
network storage devices
monitoring systems
```

There are two common ways to give a device a consistent IP address.

A static IP address is manually configured on the device.

A DHCP reservation is configured on the DHCP server. The server always gives the same IP address to a device based on its MAC address.

A good rule is:

```text id="asgx32"
Use DHCP for normal client devices.
Use static IPs or DHCP reservations for infrastructure devices.
```

### Networking Commands

Linux provides many commands for checking, configuring, and troubleshooting networks.

Some older commands are still common, but modern Linux systems usually prefer the `ip` command.

#### `ifconfig`

The `ifconfig` command was historically used to show and configure network interfaces.

Example:

```bash id="w7z6t7"
ifconfig
```

To show a specific interface:

```bash id="gmsmw4"
ifconfig eth0
```

However, `ifconfig` is considered deprecated on many modern Linux distributions. The modern replacement is usually `ip`.

#### `ip`

The `ip` command is the modern Linux tool for viewing and managing network configuration.

Show IP addresses:

```bash id="vwmfop"
ip addr show
```

Show only IPv4 addresses:

```bash id="g19t59"
ip -4 addr show
```

Show interfaces and MAC addresses:

```bash id="eocejx"
ip link show
```

Show interface statistics:

```bash id="vdr866"
ip -s link
```

Show routes:

```bash id="uzmcn1"
ip route show
```

Show IPv6 routes:

```bash id="1tfsk0"
ip -6 route show
```

The `ip` command replaces many older tools, including parts of `ifconfig`, `route`, and `netstat`.

#### `ping`

The `ping` command tests whether another host is reachable.

It sends ICMP echo request packets and waits for replies.

Example:

```bash id="6fom83"
ping google.com
```

To send only five packets:

```bash id="9h6yab"
ping -c 5 google.com
```

Example output includes round-trip time:

```text id="92yef9"
64 bytes from 142.250.185.206: icmp_seq=1 ttl=116 time=12.4 ms
64 bytes from 142.250.185.206: icmp_seq=2 ttl=116 time=11.9 ms
```

Important values:

```text id="ytt7ro"
time       round-trip latency
ttl        time to live
packet loss   percentage of packets that did not return
```

Low and consistent response times usually indicate a healthy connection.

High latency, packet loss, or no replies may indicate a network issue.

On Linux, to stop after a specific time limit, use `-w`:

```bash id="36n0d6"
ping -w 5 google.com
```

This runs for about five seconds.

To stop a continuous ping manually, press:

```text id="rp4xr4"
Ctrl + C
```

#### `netstat` and `ss`

The `netstat` command shows network connections, listening ports, and network statistics.

Examples:

```bash id="m4709t"
netstat -a
```

```bash id="7n1rqk"
netstat -l
```

However, `netstat` is also considered older on many Linux systems.

The modern replacement is usually `ss`.

Show listening TCP and UDP ports:

```bash id="c2x76d"
ss -tuln
```

Show established connections:

```bash id="7b2f35"
ss -tun
```

A useful comparison:

```text id="6ctu2f"
netstat = older tool
ss      = newer, faster replacement
```

#### `traceroute`

The `traceroute` command shows the path packets take to reach a remote host.

Example:

```bash id="wny1sq"
traceroute google.com
```

It displays each router, or hop, along the path.

Example:

```text id="hc6yhu"
1  192.168.1.1       1.1 ms
2  10.10.0.1         8.4 ms
3  203.0.113.1      14.2 ms
4  ...
```

This is useful when troubleshooting slow or broken connections.

To avoid DNS lookups and show only IP addresses:

```bash id="46e6qw"
traceroute -n google.com
```

To set the maximum number of hops:

```bash id="3xm9ov"
traceroute -m 30 google.com
```

Some systems may use `tracepath` instead:

```bash id="g7d4pr"
tracepath google.com
```

#### `route`

The `route` command displays or modifies the routing table.

Example:

```bash id="4yen0b"
route -n
```

The `-n` option shows numeric IP addresses instead of trying to resolve names.

However, `route` is older. The modern command is:

```bash id="bavqqc"
ip route
```

A route tells the system where to send packets.

Example route:

```text id="yr2w12"
default via 192.168.1.1 dev eth0
```

This means:

```text id="o8v5fj"
If there is no more specific route, send traffic to 192.168.1.1 through eth0.
```

### Default Gateway

The default gateway is the router your device uses to reach other networks.

If your computer wants to contact another device on the same local network, it can usually send traffic directly.

If your computer wants to contact a device outside the local network, such as a website on the internet, it sends the traffic to the default gateway.

```text id="kobtpn"
+----------------+     +---------------+     +---------------------+
| Local Device A |     | Local Network |     | External Network /  |
| 192.168.1.2    |-----| 192.168.1.0/24|-----| Internet            |
+----------------+     |               |     +---------------------+
                       | Gateway:      |
+----------------+     | 192.168.1.1   |
| Local Device B |-----|               |
| 192.168.1.3    |     +---------------+
+----------------+
```

The default gateway is usually your router.

To show the default gateway on Linux:

```bash id="8au52x"
ip route show default
```

Example output:

```text id="36re7e"
default via 192.168.1.1 dev eth0
```

The default gateway is:

```text id="o3fys3"
192.168.1.1
```

To extract only the gateway IP:

```bash id="7aapxf"
ip route show default | awk '{print $3}'
```

### Setting and Removing a Default Gateway

The modern way to add a default gateway is:

```bash id="9hyg9p"
sudo ip route add default via 192.168.1.254
```

To remove the default route:

```bash id="vnn6vr"
sudo ip route del default
```

The older `route` command can also do this:

```bash id="2t016z"
sudo route add default gw 192.168.1.254
```

and:

```bash id="askmte"
sudo route del default
```

Manual route changes made this way are usually temporary. They may disappear after a reboot or network restart unless configured persistently through NetworkManager, systemd-networkd, netplan, or distribution-specific network files.

### NetworkManager

NetworkManager is a Linux service that manages network connections.

It is common on desktop Linux systems and many servers.

It can manage:

```text id="f8pzug"
Ethernet
Wi-Fi
VPNs
mobile broadband
Bluetooth networking
DNS settings
DHCP
static IP profiles
```

NetworkManager has command-line, text-based, and graphical tools.

```text id="ju30zg"
+------------+      +-------------+      +------------+
|            |      |             |      |            |
| User Tools |<---->| Network     |<---->| Network    |
| nmcli,     |      | Manager     |      | Interfaces |
| nmtui, GUI |      | Daemon      |      | eth0,wlan0 |
|            |      |             |      |            |
+------------+      +------^------+      +------------+
                           |
                           v
                      +---------+
                      | D-Bus   |
                      +----^----+
                           |
                           v
                     +------------+
                     | System     |
                     | Services   |
                     | DNS, DHCP, |
                     | VPN, etc.  |
                     +------------+
```

### Useful `nmcli` Commands

Check whether NetworkManager is running:

```bash id="8qgppw"
nmcli -t -f RUNNING general
```

Show saved connection profiles:

```bash id="1z5pv2"
nmcli con show
```

Show device status:

```bash id="dggu7u"
nmcli dev status
```

Reload connection profiles after changes:

```bash id="eujnp4"
nmcli con reload
```

Bring a connection up:

```bash id="qwaeaf"
nmcli con up eth0
```

Bring a connection down:

```bash id="gh9f2y"
nmcli con down eth0
```

### Configuring a Static IP with `nmcli`

A static IP is useful for devices that should keep the same address, such as servers.

Example:

```bash id="mglkvx"
sudo nmcli con add \
  con-name eth0 \
  type ethernet \
  ifname eth0 \
  ipv4.method manual \
  ipv4.addresses 192.168.1.10/24 \
  ipv4.gateway 192.168.1.1 \
  ipv4.dns "8.8.8.8 8.8.4.4"
```

This creates a connection profile named `eth0`.

The settings mean:

```text id="5lfa7j"
192.168.1.10/24   static IP address and network prefix
192.168.1.1       default gateway
8.8.8.8 8.8.4.4   DNS servers
```

Then activate it:

```bash id="3p61ew"
sudo nmcli con up eth0
```

### Configuring DHCP with `nmcli`

For automatic IP assignment with DHCP:

```bash id="01p1p2"
sudo nmcli con add \
  con-name eth0 \
  type ethernet \
  ifname eth0 \
  ipv4.method auto
```

Then activate it:

```bash id="fy156z"
sudo nmcli con up eth0
```

DHCP is usually best for laptops, desktops, and devices that do not need a fixed address.

### `nmtui`

`nmtui` is the NetworkManager text user interface.

It provides a menu-based interface in the terminal.

Start it with:

```bash id="gdj610"
nmtui
```

It can be used to:

```text id="p2n45g"
edit a connection
activate a connection
set a hostname
configure static IP settings
configure DNS settings
enable or disable interfaces
```

`nmtui` is helpful when you do not have a graphical desktop but want something easier than long `nmcli` commands.

After changing network settings, you may need to restart NetworkManager:

```bash id="vm6ad6"
sudo systemctl restart NetworkManager
```

Be careful when restarting networking on a remote server, because a mistake can disconnect your SSH session.

### DNS

DNS stands for Domain Name System.

DNS translates human-readable names into IP addresses.

For example:

```text id="bbhyu6"
www.example.com  --->  93.184.216.34
```

DNS is often described as the phonebook of the internet.

Humans prefer names. Computers communicate using IP addresses.

```text id="oqc0ju"
You type:
    www.example.com

DNS finds:
    93.184.216.34

Your computer connects to:
    93.184.216.34
```

#### How DNS Resolution Works

A simplified DNS lookup looks like this:

```text id="u4oxcb"
  User's Device               DNS Resolver          Root / TLD / Authoritative DNS
      |                            |                              |
      | 1. Request                 |                              |
      | "www.example.com"          |                              |
      |--------------------------->|                              |
      |                            | 2. Ask DNS hierarchy         |
      |                            |----------------------------> |
      |                            |                              |
      |                            | 3. Receive answer            |
      |                            |<---------------------------- |
      |                            |                              |
      | 4. Return IP address       |                              |
      |<---------------------------|                              |
      |                            |                              |
```

Before asking DNS servers, a Linux system may check local files first.

A common order is:

```text id="jkqqux"
1. Check /etc/hosts
2. Check DNS settings, often from /etc/resolv.conf or systemd-resolved
3. Ask the configured DNS resolver
```

#### `/etc/hosts`

The `/etc/hosts` file can manually map names to IP addresses.

Example:

```text id="xsmz13"
127.0.0.1       localhost
192.168.1.50    myserver.local
```

If this file contains a matching entry, the system may use it before asking DNS.

This is useful for small local mappings or testing.

#### `/etc/resolv.conf`

The `/etc/resolv.conf` file often shows which DNS servers are configured.

Example:

```text id="ys5lpx"
nameserver 8.8.8.8
nameserver 8.8.4.4
```

However, on many modern Linux systems, this file may be automatically managed by NetworkManager or systemd-resolved. Manual edits may be overwritten.

To check DNS settings on systems using systemd-resolved:

```bash id="u12roj"
resolvectl status
```

#### Changing DNS Settings

DNS settings can be changed using NetworkManager tools.

With `nmtui`:

```text id="0rv1gs"
1. Run nmtui
2. Select Edit a connection
3. Choose the connection
4. Edit IPv4 or IPv6 settings
5. Add DNS servers
6. Save and activate the connection
```

With `nmcli`, you can set DNS servers like this:

```bash id="by4fmf"
sudo nmcli con mod eth0 ipv4.dns "8.8.8.8 8.8.4.4"
sudo nmcli con mod eth0 ipv4.ignore-auto-dns yes
sudo nmcli con up eth0
```

This sets custom DNS servers and tells NetworkManager not to use DNS servers received from DHCP.

#### DNS Troubleshooting

DNS problems often look like this:

```text id="q74dwh"
You can ping an IP address,
but you cannot reach a domain name.
```

For example:

```bash id="9ixg2t"
ping 8.8.8.8
```

works, but:

```bash id="lwrqk4"
ping google.com
```

fails.

That suggests the network may be working, but name resolution is broken.

Useful DNS tools include:

```bash id="4q97a2"
dig example.com
```

```bash id="sj9ity"
nslookup example.com
```

```bash id="j9irm3"
host example.com
```

`dig` gives detailed DNS information.

`nslookup` is widely available and simple.

`host` is quick and easy for basic lookups.

Example:

```bash id="efebzn"
dig www.example.com
```

A successful answer will include an IP address in the answer section.

### Packet Analysis

Packet analysis means capturing and inspecting network traffic.

It is useful for:

```text id="ghm6ng"
troubleshooting connectivity problems
checking whether traffic is leaving or reaching a system
understanding protocols
detecting unusual or suspicious traffic
measuring network behavior
```

```text id="p2rrce"
                    +-----------------------+
                    |       Internet        |
                    +-----------------------+
                               |
                               v
+--------------+        +-------+-------+        +---------------+
| Source       |  ====> | Packet River  |  ====> | Destination   |
| Device       |  <==== |               |  <==== | Device        |
+--------------+        +-------+-------+        +---------------+
                                ^
                                |
                    [Packet Analysis Tool]
                         /      |      \
                        /       |       \
                    Source     Data    Destination
                   Address             Address
```

Packet analysis should be done responsibly. Only capture traffic on networks and systems where you have permission.

#### `tcpdump`

`tcpdump` is a command-line packet capture tool.

To capture packets on interface `eth0` and save them to a file:

```bash id="15xj5m"
sudo tcpdump -i eth0 -w traffic.pcap
```

Explanation:

```text id="eplivy"
-i eth0          capture on interface eth0
-w traffic.pcap  write captured packets to a file
```

To capture only 10 packets:

```bash id="3y726a"
sudo tcpdump -i eth0 -c 10
```

To save 10 packets to a file:

```bash id="5cahtu"
sudo tcpdump -i eth0 -c 10 -w traffic.pcap
```

To capture traffic for port 80:

```bash id="xvy3tv"
sudo tcpdump -i eth0 port 80
```

To capture DNS traffic:

```bash id="yl7l1a"
sudo tcpdump -i eth0 port 53
```

To capture ICMP traffic, such as ping:

```bash id="g09klv"
sudo tcpdump -i eth0 icmp
```

To read a saved capture:

```bash id="ga8ouz"
tcpdump -r traffic.pcap
```

A `.pcap` file can also be opened in Wireshark for graphical analysis.

### IP Forwarding

IP forwarding allows a Linux system to forward packets between networks.

When IP forwarding is enabled, the system can act like a router.

```text id="cc348t"
+-------------+       +------------+       +-------------+
| Network A   |       |            |       | Network B   |
| 192.168.1.0 |-------|  IP        |-------| 10.0.1.0    |
| /24         |       | Forwarding |       | /24         |
+-------------+       | Device     |       +-------------+
                      | Router     |
+-------------+       |            |       +-------------+
| Network C   |-------|            |-------| Network D   |
| 10.0.2.0    |       +------------+       | 172.16.1.0  |
| /24         |                            | /24         |
+-------------+                            +-------------+
```

This is useful for:

```text id="wi2cl6"
routers
VPN gateways
firewalls
network labs
containers and virtual machines
connecting separate networks
```

#### Checking IP Forwarding

To check IPv4 forwarding:

```bash id="15shhu"
cat /proc/sys/net/ipv4/ip_forward
```

Output:

```text id="d26a7u"
0
```

means forwarding is disabled.

Output:

```text id="6yfxag"
1
```

means forwarding is enabled.

#### Temporarily Enabling IP Forwarding

To enable IPv4 forwarding temporarily:

```bash id="7xef5j"
sudo sysctl -w net.ipv4.ip_forward=1
```

To enable IPv6 forwarding temporarily:

```bash id="bkwxes"
sudo sysctl -w net.ipv6.conf.all.forwarding=1
```

Temporary changes may be lost after reboot.

#### Permanently Enabling IP Forwarding

Edit:

```bash id="l6xpj9"
/etc/sysctl.conf
```

Add:

```text id="hfme35"
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
```

Apply the changes:

```bash id="s0r899"
sudo sysctl -p /etc/sysctl.conf
```

Enable IP forwarding carefully. A forwarding system may expose traffic between networks, so firewall rules and routing rules should be configured properly.

### Network Troubleshooting

Network troubleshooting works best when done step by step.

A useful order is:

```text id="n8gc43"
1. Check physical or virtual link
2. Check interface status
3. Check IP address
4. Check default gateway and routes
5. Check DNS
6. Check firewall rules
7. Test remote connectivity
8. Capture traffic if needed
```

#### Step 1: Check Interfaces

Use:

```bash id="jkojhq"
ip link
```

Look for the interface state.

Example problem:

```text id="9yemzg"
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
```

The key part is:

```text id="qdzadb"
state DOWN
```

This means the interface is not active.

To bring it up:

```bash id="xpxk16"
sudo ip link set eth0 up
```

If it still does not work, check cables, Wi-Fi connection, virtual machine settings, or NetworkManager.

#### Step 2: Check IP Address

Use:

```bash id="m2j9pp"
ip -4 address
```

A normal private address might look like:

```text id="mhgfro"
inet 192.168.1.10/24
```

A suspicious address may look like:

```text id="2cb5lx"
inet 169.254.x.x/16
```

An address in the `169.254.x.x` range often means the device did not receive an address from DHCP and assigned itself a link-local address.

This usually indicates:

```text id="jmo0w0"
DHCP server not reachable
network cable disconnected
Wi-Fi not connected
wrong VLAN or network
DHCP service problem
```

#### Step 3: Check Routes

Use:

```bash id="qb8u9r"
ip route
```

A normal route may look like:

```text id="bl91e6"
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10
```

The default route is important because it tells the system how to reach external networks.

If there is no default route, the system may reach local devices but not the internet.

#### Step 4: Test Connectivity

Start local, then move outward.

Test loopback:

```bash id="7t0iwm"
ping -c 3 127.0.0.1
```

Test your own IP:

```bash id="x1c95u"
ping -c 3 192.168.1.10
```

Test the default gateway:

```bash id="kvh8gh"
ping -c 3 192.168.1.1
```

Test a public IP:

```bash id="gqur53"
ping -c 3 8.8.8.8
```

Test DNS:

```bash id="2z2wd7"
ping -c 3 google.com
```

The results help narrow down the problem.

```text id="xqffcs"
If 127.0.0.1 fails:
    local network stack problem

If gateway fails:
    local network or router problem

If 8.8.8.8 works but google.com fails:
    DNS problem

If gateway works but internet IP fails:
    routing, firewall, or ISP problem
```

#### Step 5: Check DNS

Check configured DNS:

```bash id="ih24c0"
cat /etc/resolv.conf
```

or:

```bash id="3igoot"
resolvectl status
```

Test DNS lookup:

```bash id="4qxfg0"
dig google.com
```

or:

```bash id="ufonwm"
host google.com
```

If DNS fails, try a known DNS server:

```bash id="1pdv0h"
dig @8.8.8.8 google.com
```

If that works, your configured DNS resolver may be wrong or unreachable.

#### Step 6: Check Firewall Rules

Firewalls may block traffic.

On Linux systems using iptables:

```bash id="n2t9x0"
sudo iptables -L -n -v
```

On systems using nftables:

```bash id="6wmou0"
sudo nft list ruleset
```

On systems using firewalld:

```bash id="iv6hhu"
sudo firewall-cmd --list-all
```

Look for rules that block required ports or protocols.

For example, if SSH is not reachable, check whether port 22 is allowed.

#### Step 7: Check Listening Ports

To see which services are listening:

```bash id="nq8a8m"
ss -tuln
```

Example output:

```text id="c6txs0"
Netid  State   Local Address:Port
tcp    LISTEN  0.0.0.0:22
tcp    LISTEN  127.0.0.1:5432
tcp    LISTEN  0.0.0.0:80
```

This means:

```text id="t7sd9k"
port 22 is listening on all IPv4 interfaces
port 5432 is listening only on localhost
port 80 is listening on all IPv4 interfaces
```

If a service is only listening on `127.0.0.1`, remote devices cannot connect to it.

#### Step 8: Capture Traffic

If the issue is still unclear, use `tcpdump`.

Example:

```bash id="koic01"
sudo tcpdump -i eth0
```

Capture only traffic to or from a host:

```bash id="laq20j"
sudo tcpdump -i eth0 host 192.168.1.20
```

Capture traffic on a port:

```bash id="b6lvfd"
sudo tcpdump -i eth0 port 443
```

Packet capture can answer questions like:

```text id="b4i5l7"
Is the request leaving my machine?
Is the reply coming back?
Is traffic reaching the server?
Is DNS being queried?
Is the firewall dropping packets?
```

### Hardware and Physical Checks

Not every network problem is caused by software.

Common physical issues include:

```text id="af0eq4"
unplugged Ethernet cable
bad cable
bad switch port
disabled Wi-Fi
weak wireless signal
wrong VLAN
failed router or switch
virtual machine adapter disconnected
```

Always check the simple things early.

#### Restarting Network Services

Sometimes a service restart can fix temporary network problems.

For NetworkManager:

```bash id="590dbx"
sudo systemctl restart NetworkManager
```

For older Debian-style networking:

```bash id="ozqxd9"
sudo systemctl restart networking
```

Be careful when doing this over SSH. Restarting networking can disconnect you from the remote machine.

#### Scenario 1: No IP Address

Symptoms:

```text id="0g3c7z"
ip address is missing
or address is 169.254.x.x
```

Check:

```bash id="r20d3y"
ip link
ip -4 address
nmcli dev status
```

Possible causes:

```text id="3z459r"
interface is down
DHCP failed
cable disconnected
wrong Wi-Fi network
NetworkManager profile misconfigured
```

#### Scenario 2: Can Reach Router but Not Internet

Symptoms:

```text id="clcata"
ping 192.168.1.1 works
ping 8.8.8.8 fails
```

Check:

```bash id="yydnr5"
ip route
traceroute 8.8.8.8
```

Possible causes:

```text id="gyt0f5"
router has no internet
wrong default gateway
firewall blocking traffic
ISP issue
```

#### Scenario 3: Can Reach IPs but Not Domain Names

Symptoms:

```text id="mhi1kp"
ping 8.8.8.8 works
ping google.com fails
```

Check:

```bash id="fldlqe"
cat /etc/resolv.conf
resolvectl status
dig google.com
dig @8.8.8.8 google.com
```

Likely cause:

```text id="tvzdo6"
DNS problem
```

#### Scenario 4: Service Not Reachable Remotely

Symptoms:

```text id="qbnzdl"
service works locally
remote clients cannot connect
```

Check:

```bash id="lgzj0g"
ss -tuln
sudo firewall-cmd --list-all
sudo iptables -L -n -v
```

Possible causes:

```text id="kn50jo"
service is only listening on 127.0.0.1
firewall is blocking the port
wrong IP address
routing issue
service is not running
```

### Challenges

1. Configure a static IP address, subnet prefix, default gateway, and DNS server for a Linux interface. Explain what each setting does.
2. Configure a system to use DHCP. Verify that it receives an IP address automatically.
3. Use `ip addr`, `ip link`, and `ip route` to inspect a system’s network configuration. Identify the interface name, IP address, MAC address, and default gateway.
4. Edit DNS settings using `nmtui` or `nmcli`. Test DNS resolution with `dig`, `host`, or `nslookup`.
5. Enable and disable IP forwarding. Explain why forwarding is required when a Linux system acts as a router.
6. Use `tcpdump` to capture packets on a network interface. Save the capture to a `.pcap` file and inspect it with `tcpdump` or Wireshark.
7. Use `traceroute` or `tracepath` to map the route to a remote host. Identify where latency increases.
8. Install a simple web server such as Apache or Nginx. Confirm that it listens on port 80 or 443 using `ss -tuln`.
9. Simulate common network problems, such as wrong DNS, missing gateway, or disabled interface. Practice identifying and fixing each issue.
10. Use `ss`, `netstat`, or firewall tools to identify listening services and open ports. Explain how this helps with security and troubleshooting.
