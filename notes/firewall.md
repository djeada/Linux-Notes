<h1>Iptables</h1>
The Linux kernel has built-in firewall technology known as "netfilter." We setup and query this using a variety of tools, the most basic of which being iptables and nftables. 

To see what rules are in place, use:

```bash
iptables -L
```

<h1>UFW</h1>
The "uncomplicated firewall" is a more user-friendly alternative to iptables. 


<h2>Installation</h2>
On most Linux distributions, UFW is installed by default.

If you are using Ubuntu, you can install it by running:

```bash
apt install ufw
```

<h2>Usage</h2>
To check which ports are open, use:

```bash
ufw status numbered
```

To allow SSH, but disallow HTTP, use:

```bash
ufw allow ssh
ufw deny http
ufw enable
```

To allow outgoing and deny incoming connections, use:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw enable
```

<h1>Blocking ping requests</h1>

Additionally one can block ping requests by editing /etc/ufw/before.rules:

```
# Block all incoming ping requests
-A ufw-before-input -p icmp --icmp-type echo-request -j DROP
```
