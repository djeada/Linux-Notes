## Linux Firewalls

A firewall is like a guard for your computer. It keeps your computer safe from others who shouldn't use it. It checks the information going in and out and follows safety rules. In Linux, there are several utilities to manage your firewall, including `iptables`, `ufw`, and `firewalld`.

## Iptables

`Iptables` is a command-line utility for managing the Linux firewall. It is pre-installed on most Linux systems and lets you configure rules to control incoming and outgoing network traffic.

To view the current rules, use the `-L` flag:

```bash
iptables -L
```

To add a new rule, use the `-A` flag followed by the rule itself. For example, to allow incoming traffic on port 80 (used for HTTP), use:

```bash
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

To delete a rule, use the `-D` flag followed by the rule number (as displayed by the `-L` flag). For example, to delete the second rule in the list, use:

```bash
iptables -D INPUT 2
```

Keep in mind that changes to the safety guard's rules with iptables don't last when you restart your computer. To keep the changes, save them in a file and bring them back when your computer starts.

## UFW

UFW (Uncomplicated Firewall) is a user-friendly alternative to iptables for managing the Linux firewall. It is pre-installed on many Linux distributions, including Ubuntu.

To view the configured rules, use the status numbered command:

```
ufw status numbered
```

To allow incoming traffic on a specific port, use the allow command followed by the protocol and port number. For example, to allow incoming `SSH` connections (which use port 22 by default), use:

```bash
ufw allow ssh
```

To block incoming traffic on a specific port, use the deny command followed by the protocol and port number. For example, to block incoming `HTTP` connections (which use port 80 by default), use:

```bash
ufw deny http
```

To activate the firewall and apply the rules, use the enable command:

```bash
ufw enable
```

You can also set default policies for incoming and outgoing traffic using the default command. For example, to deny all incoming traffic and allow all outgoing traffic, use:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw enable
```

## Firewalld

Firewalld is a more advanced firewall used by Fedora and other Linux distributions. It lets you configure firewalls using zones, which are collections of rules that apply to specific types of network interfaces.

To view the currently configured rules, use the `--list-all flag`:

```bash
firewall-cmd --list-all
```

To add a new rule, use the `--add-service` flag followed by the service name. For example, to allow incoming `SSH` connections, use:

```bash
firewall-cmd --permanent --add-service=ssh
```

To remove a rule, use the `--remove-service` flag followed by the service name. For example, to block incoming `HTTP` connections, use:

```bash
firewall-cmd --permanent --remove-service=http
```

To apply the changes and reload the firewall, use the `--reload` flag:

```
firewall-cmd --reload
```

To make the changes persistent across reboots, restart the `firewalld.service` using systemctl. For example:

```
systemctl restart firewalld.service
```

## Challenges

1. Configure the firewall to block incoming traffic on port 80 (HTTP) and allow incoming traffic on port 22 (SSH).
2. Set up rules to deny all incoming traffic while allowing all outgoing traffic.
3. Create a rule to block incoming ICMP echo requests (ping).
4. Allow incoming traffic on port 80 (HTTP) only for a specific IP address.
5. Block incoming traffic on port 80 (HTTP) for a specific IP address.

