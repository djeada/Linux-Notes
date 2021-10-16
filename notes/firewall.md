<h1>iptables</h1>
The Linux kernel has built-in firewall technology known as "netfilter." We setup and query this using a variety of tools, the most basic of which being iptables and nftables. 

To see what rules are in place, use:

```bash
iptables -L
```

<h1>ufw</h1>
The "uncomplicated firewall" is a more user-friendly alternative to iptables. 

To allow SSH, but disallow HTTP, use:

```bash
sudo ufw allow ssh
sudo ufw deny http
sudo ufw enable
```
