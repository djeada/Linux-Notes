## Basic networking terms

Let's first introduce some basic networking terms.

### Network Interfaces

Network interfaces are devices that allow computers or other devices to connect to a network. There are several types of network interfaces, including:

* `Loopback interface (lo)`: The loopback interface represents the host itself and has an IP address of `127.0.0.1`. This address can be used to access a website hosted on the local machine by navigating to `http://127.0.0.1` in a web browser. Note that this address is only accessible locally and cannot be accessed from other networks.

* `Ethernet interface (eth0)`: The ethernet interface is commonly used to connect to a local network. Even if you are running Linux in a virtual machine (VM), you will still have an eth0 interface that connects to the host's actual network interface. It is important to verify that eth0 is turned on and has an IP address so that you can connect to the local network and the internet.

### MAC Addresses

A MAC (Media Access Control) address, also known as a link or ether address, is a unique identifier for a network interface. It is used to identify a device on a network and is assigned when a network adapter is manufactured or, in the case of a virtualized network adapter, when the adapter is created. MAC addresses are typically formatted as six groups of two hexadecimal digits each (e.g. `aa:bb:cc:dd:ee:ff`).

### IP Addresses

An IP (Internet Protocol) address is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication. IP addresses generally fall within the range of `1.1.1.1` to `255.255.255.255`. A single device can have multiple IP addresses, but they must be unique on the same network.

### DHCP

In networks with a large number of computers (hundreds or thousands), it can be difficult to manually assign IP addresses to each device. The dynamic host configuration protocol (DHCP) is a protocol that automates this process. When a device initially connects to the network, it sends a DHCP request and, if a DHCP server is available, it responds with the IP address configuration for that device. This IP address is then reserved so that it is not accidentally given to another device.

DHCP is typically used for client systems or devices that do not experience negative consequences from changing their IP address frequently. On server systems, administrators may manually configure static IP addresses or create static DHCP reservations, which are tied to the MAC address of the network adapter.

The standard DHCP process is as follows:

1. When a device boots up, it sends a DHCP request to the network.
1. If a DHCP server is available, it responds with the IP address configuration for that device.
1. The IP address is designated as reserved so that it is not mistakenly given to another device.

The DHCP client's local configuration file is `/etc/dhcp/dhclient.conf`. This file contains information on how Linux should acquire IP configuration data from DHCP servers. You can check the status of DHCP by looking in the `/var/log/syslog file`:

```
grep dhcp /var/log/syslog
```

If a device is using DHCP, the keyword "dynamic" will be shown in the information about its interface.

It is important to note that DHCP is not suitable for all situations. For example, on server systems or devices that cannot afford to change their IP address frequently, administrators may choose to manually configure static IP addresses.

In summary, the dynamic host configuration protocol (DHCP) is a useful tool for automating the process of assigning IP addresses to devices on a network. It is typically used for client systems and devices that can handle frequent changes to their IP address, and can be configured through the `/etc/dhcp/dhclient.conf` file on the local machine.

## Networking Commands

There are a number of commands that are useful for managing and troubleshooting network connections. Below, we will discuss some of the most common ones:

### ifconfig

The `ifconfig` command is used to display information about network interfaces, such as their IP addresses, MAC addresses, and broadcast addresses. It can also be used to assign an IP address to an interface. To see information about all interfaces, you can simply run `ifconfig` without any arguments. To see information about a specific interface, such as eth0, you can use the command `ifconfig eth0`.

### ip

The ip command is now the recommended tool for changing IP addresses in the live configuration, as the ifconfig command has been deprecated. The `ip addr show` command is used to display IP addresses and network interfaces, while the `ip link show` command displays different interfaces, their status, and the MAC addresses associated with each one. The `ip -s` link command displays network interfaces and information about sent packets. To show routing information for an IPv6 network, you can use the command `ip -6 route show`.

### ping

The ping (Packet Internet Grouper) command is used to test the connection between two computers. It does this by sending an Internet Control Message Protocol (ICMP) packet over the network and waiting for a response. If a host is accessible and capable of communicating on the network, it will respond with an ICMP response. If the host is not accessible, you will receive a notification that the host was unavailable or that the ping request timed out.

```
ping google.com
```

### route

The route command is used to display and modify the routing table, which determines the path that network packets take through a network. To display the routing table in full numeric form, you can use the command `route -n`. This will show the IP address, netmask, gateway, and other information about each route in the table.

To add a default gateway, you can use the command `route add default gw IP_ADDRESS`, replacing IP_ADDRESS with the appropriate IP address. This will add a new route to the routing table that directs all packets to the specified gateway.

To reject routing to a specific host or network, you can use the command `route add -host IP_ADDRESS reject`. This will add a new route to the routing table that blocks all packets destined for the specified IP address.

To delete the default gateway, you can use the command `route del default`. This will remove the default route from the routing table, causing all packets to be dropped unless there is another route available to reach their destination.

It is important to note that the route command only affects the routing table for the current session. If you want to make changes to the routing table that will persist after a reboot, you will need to modify the `/etc/network/interfaces` file or use a different method, such as the `ip` command or a graphical tool like the Network Manager.

Overall, the route command is a useful tool for managing and troubleshooting network routes. By understanding how to use it, you can more easily control the path that network packets take through your network.

## Network Manager daemon

Network Manager is a daemon that manages network connections on a Linux system. It provides a command-line interface, called `nmcli`, that allows you to manage and configure network connections, as well as a graphical user interface (GUI) for configuring network connections.

To check if Network Manager is running, you can use the command `nmcli -t -f RUNNING general`. This command will return "running" if Network Manager is running and "stopped" if it is not.

Network Manager is configured using scripts with the prefix "ifcfg" located in the directory `/etc/sysconfig/network-scripts`. If you have modified one of these scripts, you can use the command `nmcli con reload` to reload the settings.

To display all available connections, you can use the command `nmcli con show`. To list all available devices, use the command `nmcli dev status`.

To configure a network interface statically using `nmcli`, you can use the command:

```
nmcli con add con-name [interface] type ethernet ifname [interface] ipv4.method manual ipv4.address [IP address]/[network prefix] ipv4.gateway [default gateway]
```

For example, to configure the interface eth2 with the IP address 10.10.10.4/24 and default gateway 10.10.10.1, you can use the command:

```
nmcli con add con-name eth2 type ethernet ifname eth2 ipv4.method manual ipv4.address 10.10.10.4/24 ipv4.gateway 10.10.10.1
```

To create a new ethernet connection and assign it a dynamic IP address using DHCP, you can use the ipv4.method auto option.

If you do not have the GUI version of Network Manager installed on your system, you can use the nmtui command to modify connections, change the hostname, and activate connections. After making changes, use the command systemctl restart network to restart Network Manager and apply the changes.


## DNS

DNS, or the Domain Name System, is a crucial part of the internet infrastructure that allows us to access websites and other online resources using human-readable domain names rather than numerical IP addresses. Without DNS, we would have to remember the numerical IP addresses of websites and other internet resources, which would be inconvenient and difficult to remember.

### How DNS works

When you type a domain name into your web browser, your computer will first check a local file called `/etc/hosts` for the corresponding IP address. If the name is found in this file, no further searches are carried out and the IP address is used to connect to the desired website or resource. You can edit the hosts file to manually set a static name-to-IP address mapping. For example, if you map google.com to the localhost IP address (127.0.0.1), no one on the system will be able to access Google's website through a browser.

If the desired domain name is not found in the hosts file, the computer will then use the `/etc/resolv.conf` file to determine which local domains should be searched and which server names should be used for DNS resolution. This file is usually created on the fly by systemd, so it is not usually edited manually. However, you can use this file to verify which DNS server your computer is using.

Once the appropriate DNS server has been identified, the computer will send a request to the server asking it to resolve the domain name and provide the corresponding IP address. The DNS server will then search its database for the requested domain name and, if it is found, will return the corresponding IP address to the requesting computer.

### Changing DNS settings

There are several ways to change DNS settings on your computer. One option is to use the nmtui tool to set the DNS name servers. Alternatively, you can edit the `ifcf` network connection configuration file in `/etc/sysconfig/network-scripts` to set the DNS servers. To change an existing connection, you can use the nmcli command, as shown in the example above.

To confirm your DNS settings, you can view the `/etc/resolv.conf` file.

### Troubleshooting DNS

If you are experiencing problems with DNS, you can use tools like `dig`, `nslookup`, and `host` to gather information about DNS resolution. These tools allow you to query DNS servers and troubleshoot issues with domain name resolution.

```
dig google.com
nslookup google.com
host google.com
```

## The Default Gateway

A default gateway is a routing device that provides a host with a default route for sending traffic to external networks. It is typically used as a fallback option when a host is unable to find a more specific route to a destination. The default gateway is usually configured on a host's network interface and is used to forward traffic to other networks or the Internet.

To display the default gateway on a Linux system, you can use the command `ip route show | grep 'default' | awk '{print $3}'`. This command will display the IP address of the default gateway.

To set a default gateway, you can use the route command. For example, to set the default gateway to 192.168.1.254, you can use the command `route add default gw 192.168.1.254`. To remove the default gateway, use the command `route del default`.

It is important to note that the default gateway is used as a last resort for routing traffic and may not always be the best route for a particular destination. More specific routes, such as those based on a host's IP address or network prefix, will take precedence over the default gateway.

## Packet analysis

Packet analysis, also known as packet sniffing or network sniffing, is the process of capturing, examining, and analyzing packets of data that pass through a network. This can be useful for various purposes, such as troubleshooting network issues, monitoring network traffic, or detecting security threats.

One tool that allows you to do packet analysis from the command line is tcpdump. tcpdump is a widely used command-line utility that can capture and display packets being transmitted over a network. It can be used to capture packets on a specific network interface, filter packets based on various criteria, and save the captured packets to a file for further analysis.

To use tcpdump, you simply need to enter the tcpdump command followed by any desired options and arguments. For example:

```
tcpdump -i eth0 -w traffic.pcap
```

This command will capture packets on the eth0 network interface and save them to a file called `traffic.pcap` for later analysis.

There are many options and arguments available with `tcpdump`, allowing you to customize and fine-tune the packet capture process. For example, you can use the `-c` option to specify the number of packets to capture, the `-s` option to specify the snapshot length (i.e., the number of bytes of each packet to capture), and the `-f` option to specify a packet filter to apply.

In addition to tcpdump, there are also other tools available for packet analysis, such as Wireshark and ngrep. These tools can provide a graphical user interface and additional features for more advanced packet analysis tasks.

Overall, packet analysis is a powerful tool for understanding and troubleshooting network issues, and can be a valuable tool for network administrators and security professionals.

## IP forwarding

IP forwarding, also known as packet forwarding or routing, is the process of forwarding packets from one network to another based on the destination IP address of the packet. This allows devices on a network to communicate with devices on other networks and access resources on the internet.

To check if IP forwarding is enabled on a Linux system, you can use the command `cat /proc/sys/net/ipv4/ip_forward`. This will output a value of 0 if IP forwarding is disabled, or 1 if it is enabled.

To enable IP forwarding temporarily in the current session, you can use the sysctl command with the appropriate option for IPv4 or IPv6:

```
sysctl -w net.ipv4.ip_forward=1    # Enable IPv4 forwarding
sysctl -w net.ipv6.conf.all.forwarding=1  # Enable IPv6 forwarding
```

To enable IP forwarding permanently, you will need to edit the `/etc/sysctl.conf` file and add the appropriate options for IPv4 and IPv6:

```
net.ipv4.ip_forward=1           # Enable IPv4 forwarding
net.ipv6.conf.all.forwarding=1  # Enable IPv6 forwarding
```

To apply the changes, you will need to reload the sysctl settings by running `sysctl -p /etc/sysctl.conf`. You may also need to restart networking on your system for the changes to take effect. On RedHat-based systems, you can use the service network restart command, and on Debian-based systems, you can use `/etc/init.d/networking restart`.

IP forwarding is an important feature for devices that act as routers or network gateways, allowing them to forward packets between different networks and enable communication between devices on those networks. It is also useful for certain networking configurations, such as setting up a VPN or creating a network bridge.

## Network troubleshooting

There are many tools and techniques that can be used for network troubleshooting. Here are some additional steps that you can follow:

Check your network connection status and settings. You can use the ip command to view the status of your network interfaces and the ipconfig command on Windows to view the IP address, subnet mask, and default gateway for each interface.

```
ip link
ip -4 address
```

Check your routing table. The routing table determines which network interface to use for outgoing packets based on the destination IP address. You can view the routing table using the ip or route command.

```
ip route
route -n
```

Check for any firewall rules that may be blocking network traffic. You can use the iptables command on Linux or the netsh command on Windows to view and manage firewall rules.

```
iptables -L
netsh advfirewall firewall show rule name=all
```

Check for any network traffic that may be causing congestion or other issues. You can use tools like tcpdump, Wireshark, or netstat to capture and analyze network traffic.

```
tcpdump -i eth0
Wireshark
netstat -s
```

Check for any hardware issues that may be affecting the network. This could include issues with cables, switches, routers, or other network hardware.

If you are still experiencing issues, you may want to try resetting your network settings or restarting your networking services. On Linux systems, you can use the systemctl command to restart networking services. On Windows systems, you can use the net stop and net start commands to stop and start networking services.

Overall, network troubleshooting can be a complex and time-consuming process, but by following a systematic approach and using the appropriate tools and techniques, you can often identify and resolve issues with your network.

## Challenges

1. What is the purpose of the `/etc/hosts` file in Linux?
1. How can you change the DNS settings on a Linux system using `nmcli`?
1. What is the purpose of the `sysctl` command in Linux?
1. How can you view the routing table in Linux using the `ip` command?
1. What is the purpose of the `ping` command and how is it used?
1. How can you capture and analyze packets using `tcpdump` in Linux?
1. What is the purpose of the `ifconfig` command in Linux?
1. What is the purpose of the dhcp daemon in Linux and how is it used?
