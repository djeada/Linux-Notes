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
 ip
 
 When using iproute2, how do you show routing information for an IPv6 network?
 ip -6 route show

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

<h2>NetworkManager daemon</h2>

It is a command-line tool that manages network connections.

<h2>Packet analysis</h2>

The tcpdump command allows you to do packet analysis from the command line.

```bash
tcpdump
```

