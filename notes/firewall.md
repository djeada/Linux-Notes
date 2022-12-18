## Introduction to Linux Firewalls

A firewall is a security feature that protects your computer from unauthorized access. It controls incoming and outgoing network traffic based on predetermined security rules. In Linux, there are several utilities that you can use to manage your firewall, including `iptables`, `ufw`, and `firewalld`.

## Iptables

`Iptables` is a command-line utility that is used to manage the firewall in Linux. It is pre-installed on most Linux systems and allows you to configure rules to control incoming and outgoing network traffic.

To view the rules that are currently in place, you can use the `-L` flag:

```bash
iptables -L
```

To add a new rule, you can use the `-A` flag followed by the rule itself. For example, to allow incoming traffic on port 80 (used for HTTP), you can use the following command:

```bash
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

To delete a rule, you can use the `-D` flag followed by the rule number (as displayed by the `-L` flag). For example, to delete the second rule in the list, you can use:

```bash
iptables -D INPUT 2
```

Keep in mind that any changes made to the firewall rules using iptables are not persistent, meaning that they will not survive a reboot. To make the changes persistent, you will need to save the rules to a file and restore them on startup.

## UFW

UFW (Uncomplicated Firewall) is a user-friendly alternative to iptables for managing the firewall in Linux. It is pre-installed on many Linux distributions, including Ubuntu.

To view the configured rules, you can use the status numbered command:

```
ufw status numbered
```

To allow incoming traffic on a specific port, you can use the allow command followed by the protocol and port number. For example, to allow incoming `SSH` connections (which use port 22 by default), you can use:

```bash
ufw allow ssh
```

To block incoming traffic on a specific port, you can use the deny command followed by the protocol and port number. For example, to block incoming `HTTP` connections (which use port 80 by default), you can use:

```bash
ufw deny http
```

To activate the firewall and apply the rules, you can use the enable command:

```bash
ufw enable
```

You can also set default policies for incoming and outgoing traffic using the default command. For example, to deny all incoming traffic and allow all outgoing traffic, you can use:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw enable
```

## Firewalld

Firewalld is a more advanced firewall that is used by Fedora and other Linux distributions. It allows you to configure firewalls using zones, which are collections of rules that apply to specific types of network interfaces.

To view the currently configured rules, you can use the --list-all flag:

```bash
firewall-cmd --list-all
```

To add a new rule, you can use the `--add-service` flag followed by the service name. For example, to allow incoming `SSH` connections, you can use:

```bash
firewall-cmd --permanent --add-service=ssh
```

To remove a rule, you can use the `--remove-service` flag followed by the service name. For example, to block incoming `HTTP` connections, you can use:

```bash
firewall-cmd --permanent --remove-service=http
```

To apply the changes and reload the firewall, you can use the `--reload` flag:

```
firewall-cmd --reload
```

To make the changes persistent across reboots, you will need to restart the `firewalld.service` using systemctl. For example:

```
systemctl restart firewalld.service
```

## Challenges

1. Block incoming traffic on port 80 and allow incoming traffic on port 22.
1. Block all incoming traffic and allow all outgoing traffic.
1. Block all incoming ping requests.
1. Allow incoming traffic on port 80 only for a specific IP address.
1. Block incoming traffic on port 80 for a specific IP address.
