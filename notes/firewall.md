<h1>Firewall</h1>
Firewall is a security feature that protects your computer from unauthorized access. A command line utility called iptables is used to manage the firewall. There are other utilities that can be used to manage the firewall, but iptables is usually preinstalled on most Linux systems. It is advised to use only one utility to manage the firewall, so pick your poison and stick to it.

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

<h1>Firewalld</h1>
Firewalld is a Linux firewall that is used by Fedora and other distributions. It is a more advanced firewall than iptables. 

To see what rules are in place, use:

```bash
firewall-cmd --list-all
```

To allow SSH, but disallow HTTP, use:

```bash
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --remove-service=http
firewall-cmd --reload
```

To put the rules in place, use:

```bash
systemctl restart firewalld.service
```

<h1>Blocking ping requests</h1>

Additionally one can block ping requests by editing /etc/ufw/before.rules:

```
# Block all incoming ping requests
-A ufw-before-input -p icmp --icmp-type echo-request -j DROP
```
