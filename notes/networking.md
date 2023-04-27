# Networking
Networking lets computers and devices talk to each other and share data. To understand networking, you need to know some important words and ideas.

## Basic networking terms

Let's first introduce some basic networking terms.

### Network Interfaces

Network interfaces let devices connect to networks. There are different types, like:

* `Loopback interface (lo)`: This is for the device itself. It has an IP address of `127.0.0.1`. Use this to see a website on your own device. It only works on your device, not others.

* `Ethernet interface (eth0)`: This connects to a local network. Even with Linux in a virtual machine (VM), you have an eth0 interface. Make sure it's on and has an IP address to connect to the network and the internet.

### MAC Addresses

A MAC address is a unique name for a network interface. It helps find a device on a network. The MAC address is set when a network adapter is made or when a virtual adapter is created. It looks like this: `aa:bb:cc:dd:ee:ff`.

To check the MAC address of a network interface on a Linux system, you can use the `ip link` command.

```
ip link show
```

The output will display information about all network interfaces on your system. The MAC address is shown after the link/ether field.

Example output:

```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
```

In this example, the MAC address for the eth0 interface is `00:11:22:33:44:55`.

### IP Addresses

An IP address is a number for each device on a network using the Internet Protocol. IP addresses are between `1.1.1.1` and `255.255.255.255`. A device can have more than one IP address, but they must be unique on the same network.

#### Private IP address

Aprivate IP address is used within a local network and is not directly exposed to the internet. Devices on the same local network use private IP addresses to communicate with each other. Private IP addresses are assigned by your router and typically fall within specific reserved IP address ranges:

* `10.0.0.0` to `10.255.255.255`
* `172.16.0.0` to `172.31.255.255`
* `192.168.0.0` to `192.168.255.255`

To check your private IP address, open a terminal and enter the following command:

```
ip -4 address show
```

The output will display information about your network interfaces, including their IPv4 addresses. Look for the inet field followed by an IP address.

Example output:

```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.10/24 brd 192.168.1.255 scope global dynamic noprefixroute eth0
```

In this example, the private IP address for the eth0 interface is `192.168.1.10`.

#### Public IP address

A public IP address is the IP address assigned to your router or modem by your Internet Service Provider (ISP). This IP address is used to identify your network on the internet. When you access a website or use an online service, your public IP address is what the remote server sees as the source of the connection.

To check your public IP address, you can use a third-party service such as curl with an online service like `ifconfig.me`, `ipify.org`, or `icanhazip.com`. Open a terminal and enter one of the following commands:

```
curl ifconfig.me
```

The output will display your public IP address, for example:

```
203.0.113.10
```

### DHCP

In big networks, it's hard to give IP addresses to every device. DHCP (Dynamic Host Configuration Protocol) helps with this. When a device connects to the network, it asks for an IP address. If a DHCP server is there, it gives the device an IP address. This IP address is saved so another device doesn't get it.

DHCP is good for devices that can change IP addresses often. For servers or devices that need a fixed IP address, you can set an IP address manually or make a static DHCP reservation.

The usual DHCP steps are:

1. A device starts and asks for an IP address.
2. If a DHCP server is there, it gives the device an IP address.
3. The IP address is saved so it's not given to another device.

To see if a device uses DHCP, look for the word "dynamic" in its interface info.

DHCP isn't good for everything. For servers or devices that need a fixed IP address, you can set an IP address manually.

In short, DHCP helps give IP addresses to devices on a network. It's good for devices that can change IP addresses often. To set up DHCP, use the `/etc/dhcp/dhclient.conf` file on the local machine.

## Networking Commands

These commands help manage and troubleshoot network connections:

### ifconfig

`ifconfig` shows information about network interfaces (IP addresses, MAC addresses, etc.). To see all interfaces, run `ifconfig`. To see a specific interface, like eth0, use `ifconfig eth0`.

### ip

`ip` is now the recommended tool for changing IP addresses. Use `ip addr show` to see IP addresses and interfaces. `ip link show` shows interfaces, their status, and MAC addresses. `ip -s link` shows interfaces and sent packet information. `ip -6 route show` shows routing information for IPv6 networks.

### ping

`ping` tests the connection between two computers. It sends a message and waits for a response. If the host can communicate, it sends a response. If not, you get a notification.

```
ping google.com
```

### route

The `route` command is useful for displaying and modifying the routing table, which determines how network packets travel through a network. Some examples of using the `route` command include:

- `route -n`: Display the routing table in full numeric form, showing IP addresses, netmasks, gateways, and other information about each route.

- `route add default gw IP_ADDRESS`: Add a default gateway by replacing IP_ADDRESS with the appropriate IP address. This creates a new route directing all packets to the specified gateway.

- `route add -host IP_ADDRESS reject`: Reject routing to a specific host or network by replacing IP_ADDRESS with the appropriate address. This adds a new route that blocks all packets destined for the specified IP address.

- `route del default`: Delete the default gateway, which removes the default route from the routing table. Packets will be dropped unless there is another route available to reach their destination.

Remember, the `route` command only affects the routing table for the current session. To make permanent changes, modify the `/etc/network/interfaces` file or use another method, such as the `ip` command or Network Manager.

## Network Manager daemon

Network Manager is a daemon that manages network connections on a Linux system. It provides:

1. A command-line interface called `nmcli` for managing and configuring network connections.
2. A graphical user interface (GUI) for configuring network connections.

Here are some useful `nmcli` commands:

- `nmcli -t -f RUNNING general`: Check if Network Manager is running. It returns "running" if it's running and "stopped" if it's not.

- `nmcli con reload`: Reload the settings after modifying one of the "ifcfg" scripts located in the `/etc/sysconfig/network-scripts` directory.

- `nmcli con show`: Display all available connections.

- `nmcli dev status`: List all available devices.

### Configuring a Static IP Address

To configure a network interface with a static IP address, you need to provide the interface name, IP address, network prefix, and default gateway. The command format is:

```
nmcli con add con-name [interface] type ethernet ifname [interface] ipv4.method manual ipv4.address [IP address]/[network prefix] ipv4.gateway [default gateway]
```

Replace `[interface]`, `[IP address]`, `[network prefix]`, and `[default gateway]` with the appropriate values for your network.

For example, to configure the network interface `eth0` with a static IP address of `192.168.1.10`, a network prefix of `24` (corresponding to a subnet mask of `255.255.255.0`), and a default gateway of `192.168.1.1`, you would use the following command:

```
nmcli con add con-name eth0 type ethernet ifname eth0 ipv4.method manual ipv4.address 192.168.1.10/24 ipv4.gateway 192.168.1.1
```

### Configuring a Dynamic IP Address with DHCP

To configure a network interface to obtain an IP address automatically from a DHCP server, you can use the `ipv4.method auto` option. The command format is:

```
nmcli con add con-name [interface] type ethernet ifname [interface] ipv4.method auto
```

Replace `[interface]` with the appropriate network interface name.

For example, to configure the network interface `eth0` to obtain an IP address automatically using DHCP, you would use the following command:

```
nmcli con add con-name eth0 type ethernet ifname eth0 ipv4.method auto
```

If you don't have the GUI version of Network Manager installed, use the `nmtui` command to modify connections, change the hostname, and activate connections. After making changes, use the `systemctl restart network` command to restart Network Manager and apply the changes.

## DNS

DNS (Domain Name System) translates human-friendly domain names (e.g., www.google.com) into IP addresses (e.g., 172.217.11.14) that computers use to identify each other on the internet.

### How DNS works

1. Computer checks `/etc/hosts` for domain-to-IP mapping.
2. If not in `/etc/hosts`, computer checks `/etc/resolv.conf` to find DNS server.
3. Request sent to DNS server to get the IP address.

### Change DNS settings

Different DNS servers can provide various benefits, such as faster browsing, better security, or the ability to access blocked websites. By changing your DNS settings, you can switch to a DNS server that best meets your needs.

#### How to change DNS settings:

1. **Using `nmtui`:** Network Manager Text User Interface (nmtui) is an easy-to-use, text-based tool that allows you to configure network settings, including DNS servers. Launch `nmtui`, navigate to "Edit a connection," select the connection you want to modify, and set the desired DNS servers in the "IPv4 CONFIGURATION" or "IPv6 CONFIGURATION" sections.

2. **Editing configuration files:** You can also manually edit the configuration files for your network connections located in the `/etc/sysconfig/network-scripts` directory. Each network interface has a corresponding file, such as `ifcfg-eth0` for the first Ethernet interface. Open the appropriate file for your connection and add or modify the `DNS1`, `DNS2`, etc., lines with the IP addresses of the DNS servers you want to use.

Example:

```
DEVICE=eth0
...
DNS1=8.8.8.8
DNS2=8.8.4.4
```

After making changes to the configuration files, restart your network service for the changes to take effect.

#### Review current DNS settings:

You can check the current DNS settings on your system by examining the `/etc/resolv.conf` file. This file lists the DNS servers your computer is using in the `nameserver` lines.

Example of `/etc/resolv.conf` content:

```
nameserver 8.8.8.8
nameserver 8.8.4.4
```

### Troubleshoot DNS

DNS issues can occur for various reasons, such as misconfigured DNS settings, unreachable DNS servers, or DNS records not being updated correctly. When experiencing issues accessing websites or online resources, it's important to check if DNS could be the problem.

#### Why DNS might be the problem:

1. Cannot access websites or resources by domain name, but can access them using their IP addresses.
2. The browser displays a "Server not found" or "DNS resolution error" message.
3. You recently changed your DNS settings or switched to a new DNS server.

#### Tools to help troubleshoot DNS:

`dig`, `nslookup`, and `host` are command-line tools that can help you investigate DNS resolution issues. They allow you to query DNS servers to check if the domain names are correctly resolved to their respective IP addresses.

1. `dig` - Performs a DNS lookup and provides detailed information about the query, such as the answer, authority, and additional sections.

   Example: `dig google.com`

2. `nslookup` - Queries DNS servers to obtain domain name or IP address mappings. It can also be used to display information about the DNS server being used.

   Example: `nslookup google.com`

3. `host` - A simple utility that performs DNS lookups and displays the results. It can be used to find the IP address of a domain or the domain name for an IP address.

   Example: `host google.com`

## Default Gateway

A default gateway is a device (e.g., a router) that directs traffic from a local network to other networks or the internet when no specific route is available.

### Display and set default gateway

Show the default gateway:

```
ip route show | grep 'default' | awk '{print $3}'
```

Set or remove a default gateway using the `route` command:

```
route add default gw 192.168.1.254
route del default
```

## Packet analysis

Packet analysis, or packet sniffing, is the process of capturing, examining, and analyzing packets (small chunks of data) that pass through a network to troubleshoot network issues, monitor traffic, or detect security threats.

### tcpdump

`tcpdump` is a command-line utility for capturing and analyzing network packets:

```
tcpdump -i eth0 -w traffic.pcap
```

Customize the packet capture process with options like `-c` (number of packets to capture), `-s` (snapshot length), and `-f` (packet filter).

### Other packet analysis tools

Wireshark and ngrep offer graphical interfaces and advanced features for packet analysis.

## IP forwarding

IP forwarding (packet forwarding or routing) sends packets between networks based on destination IP address, enabling communication between devices on different networks and internet access.

### Check and enable IP forwarding

Check IP forwarding status:

```
cat /proc/sys/net/ipv4/ip_forward
```

Enable IP forwarding temporarily:

```
sysctl -w net.ipv4.ip_forward=1 # Enable IPv4 forwarding
sysctl -w net.ipv6.conf.all.forwarding=1 # Enable IPv6 forwarding
```

Enable IP forwarding permanently:

1. Edit `/etc/sysctl.conf` and add options for IPv4 and IPv6:

```
net.ipv4.ip_forward=1 # Enable IPv4 forwarding
net.ipv6.conf.all.forwarding=1 # Enable IPv6 forwarding
```

2. Reload sysctl settings and restart networking.

```
sysctl -p /etc/sysctl.conf
service network restart # RedHat-based systems
/etc/init.d/networking restart # Debian-based systems
```

## Network troubleshooting

### Steps for network troubleshooting

1. Check network connection status and settings:

```
ip link
ip -4 address
```

2. Check routing table:

```
ip route
route -n
```

3. Check firewall rules:

```
iptables -L
netsh advfirewall firewall show rule name=all
```

4. Check network traffic using tools like tcpdump, Wireshark, or netstat:

```
tcpdump -i eth0
Wireshark
netstat -s
```

5. Check for hardware issues with cables, switches, routers, or other network hardware.

6. Reset network settings or restart networking services:

```
systemctl restart networking # Linux systems
net stop service_name; net start service_name # Windows systems
```

Overall, network troubleshooting can be a complex and time-consuming process, but by following a systematic approach and using the appropriate tools and techniques, you can often identify and resolve issues with your network.

## Challenges

1. Configure a static IP address, subnet mask, and default gateway for a network interface.
2. Set up a DNS server by editing the `/etc/resolv.conf` file and test DNS resolution using `dig`, `nslookup`, or `host`.
3. Enable and disable IP forwarding, then test the functionality by routing packets between different networks.
4. Set up a simple firewall using `iptables` to block and allow specific IP addresses, ports, and protocols.
5. Capture network packets using `tcpdump` and analyze the captured data to identify potential network issues or security threats.
6. Configure a basic VPN (Virtual Private Network) connection between two Linux systems.
7. Set up network bridging between two network interfaces to forward traffic between them.
8. Troubleshoot common network issues by checking the network connection status, settings, routing table, and firewall rules.
9. Use `traceroute` to identify the network path and possible bottlenecks between your Linux system and a remote IP address.
10. Set up a simple web server using Apache or Nginx and test its functionality using a web browser.
11. Use `netstat` or `ss` to analyze the current network connections and listening ports on your Linux system.
12. Set up network monitoring and logging using tools like `iftop`, `iptraf`, or `nethogs` to monitor network traffic in real-time.
