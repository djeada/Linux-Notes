<h1>Network Interfaces </h1>

* Loopback: The IP address of the loopback (lo) interface will be 127.0.0.1, which represents the host itself. Let's say you are hosting a website on your Linux machine. In your web browser, navigate to http://127.0.0.1 to access your website. That adress works only localy. You can't access it from other network.

* Ethernet: The ethernet 0 (eth0) interface is commonly used to connect to a local network. Even if you run Linux in a virtual machine (VM), you will still have an eth0 interface that links to the host's actual network interface. Most often, you should verify that eth0 is turned on and has an IP address so that you may connect with the local network and the Internet.

<h1>Mac address</h1>
As part of the OSI Model's layer 2—the Data Link layer—the media access control (MAC) address is used to identify a network interface.
Even if a network interface does not have an IP address, it will always have a MAC address (Media Access Control) address (also known as the hardware address). They appear as six groups of two hexadecimal digits each, and are assigned when a network adapter is manufactured or, in the case of a virtualized network adapter, when the adapter is created. It is also known as link or ether address.

<h1>Ip address</h1>
A single device can have more than one IP address, but they are always unique on the same network. IP addresses generally lie within the ranges of 1.1.1 to 255.255.255.255.

<h1>DHCP</h1>
When a network has a large number of computers (hundreds or thousands), it becomes extremely difficult to assign IP addresses to each of them separately. The dynamic host configuration protocol (DHCP), which automates the procedure, is the answer.
When a host or device initially connects to the network, DHCP is used to provide it an IP address.
This protocol is used for client systems or devices that do not suffer any negative consequences from changing their IP address on a frequent basis. Administrators on server systems may manually configure static IP addresses or generate what are known as static DHCP reservations, which are connected to the MAC address of the network adapter.

The standard DHCP procedure is as follows:
1. When a machine boots up, it sends a DHCP request to the network.
2. If a DHCP server is available, it responds with the IP address configuration for that device.
3. That IP address is designated as reserved so that it is not mistakenly given to another device.

If a device uses DHCP, the key word dynamic will be shown in the info about its interface.

The DHCP client's local configuration file is /etc/dhcp/dhclient.conf. Linux is informed in this configuration file on how to acquire IP configuration data from DHCP servers. You can look in /var/log/syslog for info about DHCP status.

```bash
grep dhcp /var/log/syslog
```

<h1>Commands</h1>

<h2>ifconfig</h2>

Informations provided by ifconfig:

1. Assign an IP address to an interface.
2. The interface's MAC address.
3. The address for broadcasting.
4. Send and receive bytes.

```bash
ifconfig
```

To only display the info about the eth0 interface:

```bash
ifconfig eth0
```

<h2>ip</h2>

Old good <i>ifconfig</i> has now been deprecated. Using <i>ip</i> command is now recommended for changing IP addresses in the live configuration.

To show routing information for an IPv6 network, use:
 
```bash
ip -6 route show
```

Use the following command to display ip addresses and network interfaces:

 ```bash
ip addr show
```

Use the following command to display different interfaces, their status, and their MAC addresses associated with each one (more concise than the previous one):

 ```bash
ip link show
```

Use the following command to display network interfaces and info about sent packets:

 ```bash
ip -s link
```

<h2>ping</h2>

The ping (Packet Internet Grouper) command is used to test the connection between the two computers.

```bash
ping google.com
```

It sends an Internet Control Message Protocol (ICMP) packet over the network and informs you of any responses. An ICMP response will be returned if a host is accessible and capable of communicating on the network. If, on the other hand, a host is not accessible, you will receive a notification that the host was unavailable or timed out (indicating that the ping test failed).

<h2>route</h2>

This command above is used to examine the network route information and show the routing table. To display routing table in full numeric form, use:

```bash
route -n 
```

To add a default gateway, use:

```bash
route add default gw 192.168.1.254
```

To reject routing to a particular host or network, use:

```bash
route add -host 192.168.1.81 reject
```

To delete the default gateway, use:

```bash
route del default
```

<h1>Network Manager daemon</h1>

It is a command-line tool that manages network connections. To check if it running use:

```bash
nmcli -t -f RUNNING general
```

It is a daemon configured with scripts (all having ifcfg prefix) located at /etc/sysconfig/network-scripts.

If you have modified one of those files, you must run the following command to reload the settings:

```bash
nmcli con reload
```

Use the following command to display all the available connections:

```bash
nmcli con show
```

To list all the available devices, use:

```bash
nmcli dev status
```

Use nmcli to configure the eth2 interface statically, using the IPv4 address and network prefix 10.10.10.4/24 and default gateway 10.10.10.1, but still make it auto connect at startup and save its configuration into /etc/sysconfig/network-scripts/ifcfg-eth2 file:

```bash
nmcli con add con-name eth2 type ethernet ifname eth2 ipv4.method manual ipv4.address 10.10.10.4/24 ipv4.gateway 10.10.10.1
```

To create a new ethernet connection and assign DHCP IP Address, use ipv4.mehod auto.

<h2>nmtu</h2>
<i>nmtui</i> is a file based version of <i>nmcli</i>. Use it to:

* modify the connections
* change the hostname
* activate a connection

After you've made the necessary modifications, use the following command to re-establish the connections:

```bash
systemctl restart network
```

<h1>DNS</h1>

It would be difficult to remember the IP addresses of each machine to which you want to connect. DNS is a system that converts IP addresses to names. It allows you to use your internet browser to write a nice name like google.com or apple.com, and be taken to the company's website without ever having to input an IP address.

* Prior to reaching out to a DNS server on the network, a local file called /etc/hosts is utilized as the initial point of query for any host name. No additional searches are carried out if the name is located there. You have the ability to change the hosts file and set a static name to IP address mapping.
* The /etc/resolv.conf file specifies which local domains should be searched and which server names should be used for DNS resolution.

DNS settings:

* use nmtui to set the DNS name servers
* set the DNS1 to DNS2 in the ifcf network connection configuration file in /etc/sysconfig/network-scripts
* To change an existing connection, use the following command:

```bash
nmcli con mod enps03 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli con mod enps03 ipv4.ignore-auto-dns yes
nmcli con down enps03
nmcli con up enps03
```

The command 'nmcli con' can be used to find the name of a connection (for example, enps03).

View the /etc/resolv.conf file to confirm the modifications. You should not manually change /etc/resolv.conf since it is created by the Network Manager daemon and is likely to be overwritten at any moment.


<h2>Packet analysis</h2>

The tcpdump command allows you to do packet analysis from the command line.

```bash
tcpdump
```
