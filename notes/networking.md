## Networking

Networking is the practice of connecting computers, servers, phones, routers, printers, and other devices so they can communicate and exchange data.

A network can be very small, such as two computers connected together, or very large, such as the internet. Most modern systems depend on networking in some way, whether for browsing websites, logging into remote servers, downloading software, sharing files, using cloud services, or communicating between applications.

At a basic level, networking answers questions like:

* How does one device find another device?
* How does data move between devices?
* How does a computer know where to send traffic?
* How do names like `google.com` become IP addresses?
* How do we troubleshoot when the network fails?

To understand networking, it is important to know the basic terms: network interfaces, MAC addresses, IP addresses, DHCP, DNS, routes, gateways, and common diagnostic commands.

### Network Interfaces

A network interface is the point where a computer connects to a network.

It may be a physical device, such as an Ethernet card or wireless card, or a virtual interface created by software.

A computer can have more than one network interface. For example, a laptop may have Wi-Fi, Ethernet, loopback, VPN, and virtual machine interfaces.

```text
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

* A name
* A MAC address
* One or more IP addresses
* A status, such as `UP` or `DOWN`
* Configuration settings

Common interface names include:

| Interface | Description                                |
| --------- | ------------------------------------------ |
| `lo`      | Loopback interface                         |
| `eth0`    | Traditional Ethernet interface name        |
| `ens33`   | Modern predictable Ethernet interface name |
| `wlan0`   | Wireless interface name                    |
| `docker0` | Docker bridge interface                    |
| `tun0`    | VPN tunnel interface                       |

#### Loopback Interface

The loopback interface is used for internal communication inside the same machine.

It is usually named:

```text
lo
```

Its IPv4 address is usually:

```text
127.0.0.1
```

This address is also called localhost.

For example, if a web server is running on your own computer, you may be able to access it with:

```text
http://127.0.0.1
```

or:

```text
http://localhost
```

The loopback interface is not used to communicate with other devices. It is only for communication within the same system.

A simple way to think about it is:

```text
127.0.0.1 = this computer talking to itself
```

#### Ethernet and Wireless Interfaces

An Ethernet interface connects a device to a wired network.

A wireless interface connects a device to a Wi-Fi network.

Examples:

| Interface | Description                              |
| --------- | ---------------------------------------- |
| `eth0`    | Older Ethernet naming style              |
| `ens33`   | Common Ethernet name on virtual machines |
| `wlan0`   | Common wireless interface name           |

To see network interfaces on Linux, use:

```bash
ip link show
```

Example output:

```text
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
```

The important parts are:

| Field                 | Description               |
| --------------------- | ------------------------- |
| **eth0**              | Interface name            |
| **UP**                | Interface is enabled      |
| **LOWER_UP**          | Physical link is detected |
| **mtu 1500**          | Maximum transmission unit |
| **link/ether**        | MAC address follows       |
| **00:11:22:33:44:55** | MAC address               |

If an interface is `DOWN`, it may be disabled or disconnected.

#### MAC Addresses

A MAC address is a hardware identifier assigned to a network interface.

MAC stands for Media Access Control.

It is used mainly for communication inside a local network. Devices on the same local network use MAC addresses to deliver frames to the correct network card.

A typical MAC address looks like this:

```text
aa:bb:cc:dd:ee:ff
```

It is made of six pairs of hexadecimal digits.

```text
+-----------------------------------------+
|   Manufacturer ID   | Device Identifier |
+-----------------------------------------+
         xx:xx:xx     :     xx:xx:xx
```

The first part often identifies the manufacturer or vendor. The second part identifies the individual device or adapter.

To view MAC addresses on Linux:

```bash
ip link show
```

Example:

```text
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
```

Here, the MAC address is:

```text
00:11:22:33:44:55
```

MAC addresses are used on the local network. IP addresses are used for routing traffic between networks.

A useful comparison is:

```text
MAC address = local delivery identity
IP address  = network location identity
```

### IP Addresses

An IP address identifies a device on an IP network.

IP stands for Internet Protocol.

IP addresses allow devices to find and communicate with each other across local networks and the internet.

There are two main versions:

```text
IPv4    example: 192.168.1.10
IPv6    example: 2001:db8::10
```

These notes focus mostly on IPv4.

An IPv4 address is made of four numbers separated by dots. Each number ranges from 0 to 255.

Example:

```text
192.168.1.10
```

```text
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

```text
192.168.1.10/24
```

means the first 24 bits identify the network.

In everyday terms:

```text
192.168.1.0/24 is the network
192.168.1.10 is one device on that network
```

#### Viewing IP Addresses

To show IPv4 addresses on Linux:

```bash
ip -4 address show
```

Example output:

```text
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.10/24 brd 192.168.1.255 scope global dynamic eth0
```

The important part is:

```text
inet 192.168.1.10/24
```

This means the interface has the IPv4 address:

```text
192.168.1.10
```

with prefix length:

```text
24
```

The word `dynamic` often means the address was assigned using DHCP.

#### Private IP Addresses

Private IP addresses are used inside local networks.

They are not routed directly on the public internet.

Common private IPv4 ranges are:

```text
10.0.0.0       to 10.255.255.255
172.16.0.0     to 172.31.255.255
192.168.0.0    to 192.168.255.255
```

```text
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

```text
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

```text
192.168.1.2
192.168.1.3
192.168.1.4
```

When those devices access the internet, the router translates their private addresses to the public address.

```text
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

```bash
curl ifconfig.me
```

or:

```bash
curl icanhazip.com
```

Example output:

```text
203.0.113.10
```

Public IP addresses are visible on the internet, so systems using them should be protected with firewalls, secure configurations, and regular updates.

### DHCP

DHCP stands for Dynamic Host Configuration Protocol.

It automatically assigns network settings to devices.

Without DHCP, every device would need to be configured manually with:

* IP address
* Subnet mask or prefix
* Default gateway
* DNS servers

That would be slow and error-prone, especially on large networks.

With DHCP, a device can join the network and automatically receive the settings it needs.

```text
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

```text
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

* Automates IP address assignment
* Reduces manual configuration errors
* Prevents duplicate IP addresses
* Works well for laptops, phones, tablets, and guest devices
* Makes large networks easier to manage

DHCP is especially helpful in networks where devices frequently join and leave.

#### Static IP Addresses and DHCP Reservations

Some devices need a stable IP address.

Examples include:

* Servers
* Printers
* Routers
* DNS servers
* Network storage devices
* Monitoring systems

There are two common ways to give a device a consistent IP address.

A static IP address is manually configured on the device.

A DHCP reservation is configured on the DHCP server. The server always gives the same IP address to a device based on its MAC address.

A good rule is:

```text
Use DHCP for normal client devices.
Use static IPs or DHCP reservations for infrastructure devices.
```

### Networking Commands

Linux provides many commands for checking, configuring, and troubleshooting networks.

Some older commands are still common, but modern Linux systems usually prefer the `ip` command.

#### `ifconfig`

The `ifconfig` command was historically used to show and configure network interfaces.

Example:

```bash
ifconfig
```

To show a specific interface:

```bash
ifconfig eth0
```

However, `ifconfig` is considered deprecated on many modern Linux distributions. The modern replacement is usually `ip`.

#### `ip`

The `ip` command is the modern Linux tool for viewing and managing network configuration.

Show IP addresses:

```bash
ip addr show
```

Show only IPv4 addresses:

```bash
ip -4 addr show
```

Show interfaces and MAC addresses:

```bash
ip link show
```

Show interface statistics:

```bash
ip -s link
```

Show routes:

```bash
ip route show
```

Show IPv6 routes:

```bash
ip -6 route show
```

The `ip` command replaces many older tools, including parts of `ifconfig`, `route`, and `netstat`.

#### `ping`

The `ping` command tests whether another host is reachable.

It sends ICMP echo request packets and waits for replies.

Example:

```bash
ping google.com
```

To send only five packets:

```bash
ping -c 5 google.com
```

Example output includes round-trip time:

```text
64 bytes from 142.250.185.206: icmp_seq=1 ttl=116 time=12.4 ms
64 bytes from 142.250.185.206: icmp_seq=2 ttl=116 time=11.9 ms
```

Important values:

| Field           | Description                               |
| --------------- | ----------------------------------------- |
| **time**        | Round-trip latency                        |
| **ttl**         | Time to live                              |
| **packet loss** | Percentage of packets that did not return |

Low and consistent response times usually indicate a healthy connection.

High latency, packet loss, or no replies may indicate a network issue.

On Linux, to stop after a specific time limit, use `-w`:

```bash
ping -w 5 google.com
```

This runs for about five seconds.

To stop a continuous ping manually, press:

```text
Ctrl + C
```

#### `netstat` and `ss`

The `netstat` command shows network connections, listening ports, and network statistics.

Examples:

```bash
netstat -a
```

```bash
netstat -l
```

However, `netstat` is also considered older on many Linux systems.

The modern replacement is usually `ss`.

Show listening TCP and UDP ports:

```bash
ss -tuln
```

Show established connections:

```bash
ss -tun
```

A useful comparison:

```text
netstat = older tool
ss      = newer, faster replacement
```

#### `traceroute`

The `traceroute` command shows the path packets take to reach a remote host.

Example:

```bash
traceroute google.com
```

It displays each router, or hop, along the path.

Example:

```text
1  192.168.1.1       1.1 ms
2  10.10.0.1         8.4 ms
3  203.0.113.1      14.2 ms
4  ...
```

This is useful when troubleshooting slow or broken connections.

To avoid DNS lookups and show only IP addresses:

```bash
traceroute -n google.com
```

To set the maximum number of hops:

```bash
traceroute -m 30 google.com
```

Some systems may use `tracepath` instead:

```bash
tracepath google.com
```

#### `route`

The `route` command displays or modifies the routing table.

Example:

```bash
route -n
```

The `-n` option shows numeric IP addresses instead of trying to resolve names.

However, `route` is older. The modern command is:

```bash
ip route
```

A route tells the system where to send packets.

Example route:

```text
default via 192.168.1.1 dev eth0
```

This means:

```text
If there is no more specific route, send traffic to 192.168.1.1 through eth0.
```

### Default Gateway

The default gateway is the router your device uses to reach other networks.

If your computer wants to contact another device on the same local network, it can usually send traffic directly.

If your computer wants to contact a device outside the local network, such as a website on the internet, it sends the traffic to the default gateway.

```text
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

```bash
ip route show default
```

Example output:

```text
default via 192.168.1.1 dev eth0
```

The default gateway is:

```text
192.168.1.1
```

To extract only the gateway IP:

```bash
ip route show default | awk '{print $3}'
```

### Setting and Removing a Default Gateway

The modern way to add a default gateway is:

```bash
sudo ip route add default via 192.168.1.254
```

To remove the default route:

```bash
sudo ip route del default
```

The older `route` command can also do this:

```bash
sudo route add default gw 192.168.1.254
```

and:

```bash
sudo route del default
```

Manual route changes made this way are usually temporary. They may disappear after a reboot or network restart unless configured persistently through NetworkManager, systemd-networkd, netplan, or distribution-specific network files.

### NetworkManager

NetworkManager is a Linux service that manages network connections.

It is common on desktop Linux systems and many servers.

It can manage:

* Ethernet
* Wi-Fi
* VPNs
* Mobile broadband
* Bluetooth networking
* DNS settings
* DHCP
* Static IP profiles

NetworkManager has command-line, text-based, and graphical tools.

```text
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

```bash
nmcli -t -f RUNNING general
```

Show saved connection profiles:

```bash
nmcli con show
```

Show device status:

```bash
nmcli dev status
```

Reload connection profiles after changes:

```bash
nmcli con reload
```

Bring a connection up:

```bash
nmcli con up eth0
```

Bring a connection down:

```bash
nmcli con down eth0
```

### Configuring a Static IP with `nmcli`

A static IP is useful for devices that should keep the same address, such as servers.

Example:

```bash
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

```text
192.168.1.10/24   static IP address and network prefix
192.168.1.1       default gateway
8.8.8.8 8.8.4.4   DNS servers
```

Then activate it:

```bash
sudo nmcli con up eth0
```

### Configuring DHCP with `nmcli`

For automatic IP assignment with DHCP:

```bash
sudo nmcli con add \
  con-name eth0 \
  type ethernet \
  ifname eth0 \
  ipv4.method auto
```

Then activate it:

```bash
sudo nmcli con up eth0
```

DHCP is usually best for laptops, desktops, and devices that do not need a fixed address.

### `nmtui`

`nmtui` is the NetworkManager text user interface.

It provides a menu-based interface in the terminal.

Start it with:

```bash
nmtui
```

It can be used to:

* Edit a connection
* Activate a connection
* Set a hostname
* Configure static IP settings
* Configure DNS settings
* Enable or disable interfaces

`nmtui` is helpful when you do not have a graphical desktop but want something easier than long `nmcli` commands.

After changing network settings, you may need to restart NetworkManager:

```bash
sudo systemctl restart NetworkManager
```

Be careful when restarting networking on a remote server, because a mistake can disconnect your SSH session.

### DNS

DNS stands for Domain Name System.

DNS translates human-readable names into IP addresses.

For example:

```text
www.example.com  --->  93.184.216.34
```

DNS is often described as the phonebook of the internet.

Humans prefer names. Computers communicate using IP addresses.

```text
You type:
    www.example.com

DNS finds:
    93.184.216.34

Your computer connects to:
    93.184.216.34
```

#### How DNS Resolution Works

A simplified DNS lookup looks like this:

```text
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

1. Check /etc/hosts
2. Check DNS settings, often from /etc/resolv.conf or systemd-resolved
3. Ask the configured DNS resolver

#### `/etc/hosts`

The `/etc/hosts` file can manually map names to IP addresses.

Example:

```text
127.0.0.1       localhost
192.168.1.50    myserver.local
```

If this file contains a matching entry, the system may use it before asking DNS.

This is useful for small local mappings or testing.

#### `/etc/resolv.conf`

The `/etc/resolv.conf` file often shows which DNS servers are configured.

Example:

```text
nameserver 8.8.8.8
nameserver 8.8.4.4
```

However, on many modern Linux systems, this file may be automatically managed by NetworkManager or systemd-resolved. Manual edits may be overwritten.

To check DNS settings on systems using systemd-resolved:

```bash
resolvectl status
```

#### Changing DNS Settings

DNS settings can be changed using NetworkManager tools.

With `nmtui`:

1. Run nmtui
2. Select Edit a connection
3. Choose the connection
4. Edit IPv4 or IPv6 settings
5. Add DNS servers
6. Save and activate the connection

With `nmcli`, you can set DNS servers like this:

```bash
sudo nmcli con mod eth0 ipv4.dns "8.8.8.8 8.8.4.4"
sudo nmcli con mod eth0 ipv4.ignore-auto-dns yes
sudo nmcli con up eth0
```

This sets custom DNS servers and tells NetworkManager not to use DNS servers received from DHCP.

#### DNS Troubleshooting

DNS problems often look like this:

```text
You can ping an IP address,
but you cannot reach a domain name.
```

For example:

```bash
ping 8.8.8.8
```

works, but:

```bash
ping google.com
```

fails.

That suggests the network may be working, but name resolution is broken.

Useful DNS tools include:

```bash
dig example.com
```

```bash
nslookup example.com
```

```bash
host example.com
```

`dig` gives detailed DNS information.

`nslookup` is widely available and simple.

`host` is quick and easy for basic lookups.

Example:

```bash
dig www.example.com
```

A successful answer will include an IP address in the answer section.

### Packet Analysis

Packet analysis means capturing and inspecting network traffic.

It is useful for:

* Troubleshooting connectivity problems
* Checking whether traffic is leaving or reaching a system
* Understanding protocols
* Detecting unusual or suspicious traffic
* Measuring network behavior

```text
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

```bash
sudo tcpdump -i eth0 -w traffic.pcap
```

Explanation:

```text
-i eth0          capture on interface eth0
-w traffic.pcap  write captured packets to a file
```

To capture only 10 packets:

```bash
sudo tcpdump -i eth0 -c 10
```

To save 10 packets to a file:

```bash
sudo tcpdump -i eth0 -c 10 -w traffic.pcap
```

To capture traffic for port 80:

```bash
sudo tcpdump -i eth0 port 80
```

To capture DNS traffic:

```bash
sudo tcpdump -i eth0 port 53
```

To capture ICMP traffic, such as ping:

```bash
sudo tcpdump -i eth0 icmp
```

To read a saved capture:

```bash
tcpdump -r traffic.pcap
```

A `.pcap` file can also be opened in Wireshark for graphical analysis.

### IP Forwarding

IP forwarding allows a Linux system to forward packets between networks.

When IP forwarding is enabled, the system can act like a router.

```text
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

* Routers
* VPN gateways
* Firewalls
* Network labs
* Containers and virtual machines
* Connecting separate networks

#### Checking IP Forwarding

To check IPv4 forwarding:

```bash
cat /proc/sys/net/ipv4/ip_forward
```

Output:

```text
0
```

means forwarding is disabled.

Output:

```text
1
```

means forwarding is enabled.

#### Temporarily Enabling IP Forwarding

To enable IPv4 forwarding temporarily:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

To enable IPv6 forwarding temporarily:

```bash
sudo sysctl -w net.ipv6.conf.all.forwarding=1
```

Temporary changes may be lost after reboot.

#### Permanently Enabling IP Forwarding

Edit:

```bash
/etc/sysctl.conf
```

Add:

```text
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
```

Apply the changes:

```bash
sudo sysctl -p /etc/sysctl.conf
```

Enable IP forwarding carefully. A forwarding system may expose traffic between networks, so firewall rules and routing rules should be configured properly.

### Network Troubleshooting

Network troubleshooting works best when done step by step.

A useful order is:

1. Check physical or virtual link
2. Check interface status
3. Check IP address
4. Check default gateway and routes
5. Check DNS
6. Check firewall rules
7. Test remote connectivity
8. Capture traffic if needed

#### Step 1: Check Interfaces

Use:

```bash
ip link
```

Look for the interface state.

Example problem:

```text
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
```

The key part is:

```text
state DOWN
```

This means the interface is not active.

To bring it up:

```bash
sudo ip link set eth0 up
```

If it still does not work, check cables, Wi-Fi connection, virtual machine settings, or NetworkManager.

#### Step 2: Check IP Address

Use:

```bash
ip -4 address
```

A normal private address might look like:

```text
inet 192.168.1.10/24
```

A suspicious address may look like:

```text
inet 169.254.x.x/16
```

An address in the `169.254.x.x` range often means the device did not receive an address from DHCP and assigned itself a link-local address.

This usually indicates:

* DHCP server not reachable
* Network cable disconnected
* Wi-Fi not connected
* Wrong VLAN or network
* DHCP service problem

#### Step 3: Check Routes

Use:

```bash
ip route
```

A normal route may look like:

```text
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10
```

The default route is important because it tells the system how to reach external networks.

If there is no default route, the system may reach local devices but not the internet.

#### Step 4: Test Connectivity

Start local, then move outward.

Test loopback:

```bash
ping -c 3 127.0.0.1
```

Test your own IP:

```bash
ping -c 3 192.168.1.10
```

Test the default gateway:

```bash
ping -c 3 192.168.1.1
```

Test a public IP:

```bash
ping -c 3 8.8.8.8
```

Test DNS:

```bash
ping -c 3 google.com
```

The results help narrow down the problem.

```text
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

```bash
cat /etc/resolv.conf
```

or:

```bash
resolvectl status
```

Test DNS lookup:

```bash
dig google.com
```

or:

```bash
host google.com
```

If DNS fails, try a known DNS server:

```bash
dig @8.8.8.8 google.com
```

If that works, your configured DNS resolver may be wrong or unreachable.

#### Step 6: Check Firewall Rules

Firewalls may block traffic.

On Linux systems using iptables:

```bash
sudo iptables -L -n -v
```

On systems using nftables:

```bash
sudo nft list ruleset
```

On systems using firewalld:

```bash
sudo firewall-cmd --list-all
```

Look for rules that block required ports or protocols.

For example, if SSH is not reachable, check whether port 22 is allowed.

#### Step 7: Check Listening Ports

To see which services are listening:

```bash
ss -tuln
```

Example output:

```text
Netid  State   Local Address:Port
tcp    LISTEN  0.0.0.0:22
tcp    LISTEN  127.0.0.1:5432
tcp    LISTEN  0.0.0.0:80
```

This means:

```text
port 22 is listening on all IPv4 interfaces
port 5432 is listening only on localhost
port 80 is listening on all IPv4 interfaces
```

If a service is only listening on `127.0.0.1`, remote devices cannot connect to it.

#### Step 8: Capture Traffic

If the issue is still unclear, use `tcpdump`.

Example:

```bash
sudo tcpdump -i eth0
```

Capture only traffic to or from a host:

```bash
sudo tcpdump -i eth0 host 192.168.1.20
```

Capture traffic on a port:

```bash
sudo tcpdump -i eth0 port 443
```

Packet capture can answer questions like:

* Is the request leaving my machine?
* Is the reply coming back?
* Is traffic reaching the server?
* Is DNS being queried?
* Is the firewall dropping packets?

### Hardware and Physical Checks

Not every network problem is caused by software.

Common physical issues include:

* Unplugged Ethernet cable
* Bad cable
* Bad switch port
* Disabled Wi-Fi
* Weak wireless signal
* Wrong VLAN
* Failed router or switch
* Virtual machine adapter disconnected

Always check the simple things early.

#### Restarting Network Services

Sometimes a service restart can fix temporary network problems.

For NetworkManager:

```bash
sudo systemctl restart NetworkManager
```

For older Debian-style networking:

```bash
sudo systemctl restart networking
```

Be careful when doing this over SSH. Restarting networking can disconnect you from the remote machine.

#### Scenario 1: No IP Address

Symptoms:

```text
ip address is missing
or address is 169.254.x.x
```

Check:

```bash
ip link
ip -4 address
nmcli dev status
```

Possible causes:

* Interface is down
* DHCP failed
* Cable disconnected
* Wrong Wi-Fi network
* NetworkManager profile misconfigured

#### Scenario 2: Can Reach Router but Not Internet

Symptoms:

```text
ping 192.168.1.1 works
ping 8.8.8.8 fails
```

Check:

```bash
ip route
traceroute 8.8.8.8
```

Possible causes:

```text
router has no internet
wrong default gateway
firewall blocking traffic
ISP issue
```

#### Scenario 3: Can Reach IPs but Not Domain Names

Symptoms:

```text
ping 8.8.8.8 works
ping google.com fails
```

Check:

```bash
cat /etc/resolv.conf
resolvectl status
dig google.com
dig @8.8.8.8 google.com
```

Likely cause:

```text
DNS problem
```

#### Scenario 4: Service Not Reachable Remotely

Symptoms:

```text
service works locally
remote clients cannot connect
```

Check:

```bash
ss -tuln
sudo firewall-cmd --list-all
sudo iptables -L -n -v
```

Possible causes:

* Service is only listening on `127.0.0.1`
* Firewall is blocking the port
* Wrong IP address
* Routing issue
* Service is not running

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
