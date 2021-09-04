<h1>Network Interfaces </h1>

* Loopback: The IP address of the loopback (lo) interface will be 127.0.0.1, which represents the host itself. Let's say you are hosting a website on your Linux machine. In your web browser, navigate to http://127.0.0.1 to access your website. That adress works only localy. You can't access it from other network.

* Ethernet: The ethernet 0 (eth0) interface is commonly used to connect to a local network. Even if you run Linux in a virtual machine (VM), you will still have an eth0 interface that links to the host's actual network interface. Most often, you should verify that eth0 is turned on and has an IP address so that you may connect with the local network and the Internet.
 
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

ifconfig has been deprecated. What command is now recommended for changing IP addresses in the live config?

```bash
ip
```
 
When using iproute2, how do you show routing information for an IPv6 network?
 
```bash
ip -6 route show
```

Use the following command to display network interfaces:

 ```bash
ip addr show
```

Use the following command to display  interfaces installed on your computer (more concise):

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

<h2>route</h2>
The command above is used to examine the network route information and show the routing table.

```bash
route
```

<h2>Network Manager daemon</h2>

It is a command-line tool that manages network connections. To check if it running use:

```bash
nmcli -t -f RUNNING general
```

It is a daemon configured with scripts (all having ifcfg prefix) located at /etc/sysconfig/network-scripts.

If you have modified one of those files, you must run the following command to reload the settings:

```bash
nmcli con reload
```

<h2>nmcli continued</h2>

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

<h2>DNS</h2>

DNS settings (/etc/resolv.conf):

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

