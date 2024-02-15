## Firewalls

A firewall is like a guard for your computer. It keeps your computer safe from others who shouldn't use it. It checks the information going in and out and follows safety rules. In Linux, there are several utilities to manage your firewall, including `iptables`, `ufw`, and `firewalld`.

```
INTERNET TRAFFIC ---> |--------------------------| ---> INTERNAL NETWORK
   [IP:123.45.67.89]  |                          | [Accepted IP: 123.45.67.89]
   Port 80 (HTTP)     |    +----------------+    | Port 80 -> Allowed
                      |    |   FIREWALL     |    |
                      |    | Rules Applied: |    |
   [IP: 98.76.54.32]  |    | - Allow HTTP   |    | [Rejected IP: 98.76.54.32]
   Port 22 (SSH)      |    | - Block SSH    |    | Port 22 -> Blocked
                      |    +----------------+    |
                      |                          |
                      |--------------------------|
```

## Iptables

`Iptables` is a command-line utility for managing the Linux firewall. It is pre-installed on most Linux systems and lets you configure rules to control incoming and outgoing network traffic.

To view the current rules, use the `-L` flag:

```bash
iptables -L
```

An example output might look something like this:

```
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
DROP       icmp --  anywhere             anywhere             icmp echo-request
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:ssh
LOG        all  --  anywhere             anywhere             limit: avg 10/min burst 5 LOG level debug prefix "iptables denied: "

Chain FORWARD (policy DROP)
target     prot opt source               destination         
ACCEPT     all  --  192.168.1.0/24       192.168.1.0/24       
DROP       all  --  anywhere             anywhere             

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
```

Explanation:

- **Chain Names**: `INPUT`, `FORWARD`, `OUTPUT` are the default chains in iptables.
- **Policies**: Set to `ACCEPT`, `DROP`, or `REJECT`. For example, the default policy for `FORWARD` is `DROP`.
- **Rules**: Listed under each chain.
    - **Target**: The action to take, e.g., `ACCEPT`, `DROP`, `LOG`.
    - **Prot**: The protocol, e.g., `tcp`, `udp`, `icmp`, or `all`.
    - **Opt**: Options, often includes flags like `--`.
    - **Source and Destination**: IP addresses or ranges for source and/or destination.
    - **Additional Conditions**: For example, `tcp dpt:ssh` means TCP packets destined for SSH port.
    - **Logging**: The `LOG` rule can specify logging of packets, including a prefix for log messages.

To add a new rule, use the `-A` flag followed by the rule itself. For example, to allow incoming traffic on port 80 (used for HTTP), use:

```bash
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

To delete a rule, use the `-D` flag followed by the rule number (as displayed by the `-L` flag). For example, to delete the second rule in the INPUT chain, use:

```bash
iptables -D INPUT 2
```

🔴 Caution: Keep in mind that changes to the safety guard's rules with iptables don't last when you restart your computer. To keep the changes, save them in a file and bring them back when your computer starts.

1. On Debian-based systems, you can save the current iptables configuration with:

```bash
iptables-save > /etc/iptables/rules.v4
```

And ensure they are reloaded on boot by installing the `iptables-persistent` package.

2. On Red Hat-based systems, you can save the configuration with:

```bash
service iptables save
```

## UFW

UFW (Uncomplicated Firewall) is a user-friendly alternative to iptables for managing the Linux firewall. It is pre-installed on many Linux distributions, including Ubuntu.

To view the configured rules, use the status numbered command:

```
ufw status numbered
```

An example output of this command might look something like this:

```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere                  
[ 2] 80/tcp                     ALLOW IN    Anywhere                  
[ 3] 443/tcp                    ALLOW IN    Anywhere                  
[ 4] 1000:2000/tcp              ALLOW IN    192.168.1.0/24            
[ 5] 22/tcp                     ALLOW IN    Anywhere (v6)             
[ 6] 80/tcp                     ALLOW IN    Anywhere (v6)             
[ 7] 443/tcp                    ALLOW IN    Anywhere (v6)             
```

Explanation:

- **Status**: Indicates whether the firewall is active or inactive. In this case, it's `active`.

- **Columns in the Output**:
  - **To**: This column shows the port or port range and protocol (like `22/tcp`) for which the rule is applied.
  - **Action**: Specifies the action (`ALLOW IN`, `DENY`, etc.) taken by the firewall for matching traffic.
  - **From**: This column indicates the source of the traffic for which the rule is applicable. It can be an IP address, a subnet, or `Anywhere`.

- **Numbered Rules**: Each rule is prefixed with a number in square brackets (e.g., `[ 1]`). This numbering is crucial for modifying or deleting specific rules, as it allows you to reference them easily.

- **IPv4 and IPv6 Rules**: The rules apply to both IPv4 and IPv6 traffic if suffixed with `(v6)`.

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

An example output might look something like this:

```
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0
  sources: 
  services: ssh dhcpv6-client http https
  ports: 8080/tcp 9090/tcp
  protocols: 
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
    rule family="ipv4" source address="192.168.0.0/24" accept
    rule family="ipv4" source address="10.0.0.0/8" port port="443" protocol="tcp" accept
```

Explanation:

- **Zone**: The name of the zone (e.g., `public`) and its status (`active`).
- **Target**: The default action for incoming traffic not matching any other rule.
- **Interfaces**: Network interfaces (e.g., `eth0`) associated with the zone.
- **Services**: Predefined services allowed in this zone (e.g., `ssh`, `http`, `https`).
- **Ports**: Custom ports that are open (e.g., `8080/tcp`, `9090/tcp`).
- **Protocols, Masquerade, Forward-ports, Source-ports, Icmp-blocks**: Other network settings and rules.
- **Rich Rules**: More complex rules defined, like allowing specific IP ranges on certain ports. For example, the rule allowing all traffic from the `192.168.0.0/24` subnet, and allowing TCP traffic on port `443` from the `10.0.0.0/8` subnet.

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

1. Configure Firewall for Specific Port Traffic:
   - Block all incoming traffic on port 80 (HTTP).
   - Allow all incoming traffic on port 22 (SSH).

2. Set Up Default Firewall Policies:
   - Configure the firewall to deny all incoming traffic by default.
   - Allow all outgoing traffic.

3. Create a firewall rule to deny incoming ICMP echo requests, effectively blocking ping requests.
4. Configure the firewall to allow incoming traffic on port 80 (HTTP) only from a specific IP address.
5. Set up a rule to block all incoming HTTP traffic on port 80 from a specific IP address.
6. Modify firewall rules to allow SSH access (port 22) only from a set of predefined IP addresses.
7. Implement a rule to limit the rate of incoming connections to a specific port (e.g., 100 connections per minute) to mitigate potential DoS attacks.
8. Set up the firewall to log details of all dropped packets for analysis and monitoring purposes.
9. Create a rule to forward traffic incoming on a specific port (e.g., 8080) to another port (e.g., 80).
10. Configure the firewall to block all outgoing traffic to certain domains or IP addresses.
11. Implement firewall rules that specifically target IPv6 traffic for both incoming and outgoing connections.
12. Configure rules that are active only during certain hours of the day, for instance, allowing certain traffic only during business hours.


