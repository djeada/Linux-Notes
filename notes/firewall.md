## Firewalls

A firewall controls network traffic entering, leaving, or passing through a system.

A simple way to think about a firewall is:

```text
A firewall is a rule-based traffic guard.
```

It checks packets against rules and decides whether to allow, block, reject, forward, or log them.

```text
INTERNET TRAFFIC ---> |--------------------------| ---> INTERNAL NETWORK
   [IP:123.45.67.89]  |                          | [Accepted IP: 123.45.67.89]
   Port 80 HTTP       |    +----------------+    | Port 80 -> Allowed
                      |    |   FIREWALL     |    |
                      |    | Rules Applied: |    |
   [IP: 98.76.54.32]  |    | - Allow HTTP   |    | [Rejected IP: 98.76.54.32]
   Port 22 SSH        |    | - Block SSH    |    | Port 22 -> Blocked
                      |    +----------------+    |
                      |                          |
                      |--------------------------|
```

Firewalls are used to:

- allow trusted traffic
- block unwanted traffic
- limit exposed services
- protect servers from scans and attacks
- restrict access by source IP
- log suspicious packets
- rate-limit abusive traffic
- forward traffic to another port or host

A firewall does not make a vulnerable service safe by itself, but it reduces what can reach that service.

### Basic Firewall Concepts

A firewall rule usually answers these questions:

| Firewall Rule Component | Description                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| **Direction**           | Is the traffic **incoming**, **outgoing**, or **forwarded**?                                      |
| **Protocol**            | Does the rule apply to **TCP**, **UDP**, **ICMP**, or **all protocols**?                          |
| **Port**                | Which port(s) are affected (e.g., **22**, **80**, **443**, **8080**)?                             |
| **Source**              | Which IP address or subnet is the traffic coming from?                                            |
| **Destination**         | Which IP address or subnet is the traffic going to?                                               |
| **Action**              | What should happen to matching traffic: **allow**, **drop**, **reject**, **log**, or **forward**? |

Example:

```text
Allow incoming TCP traffic from anywhere to port 22.
```

This means SSH is reachable.

Another example:

```text
Deny incoming TCP traffic from anywhere to port 80.
```

This means HTTP is blocked.

### Common Firewall Actions

Firewalls commonly use these actions:

| Firewall Target            | Description                                                                                                            |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **ACCEPT**                 | Allow the packet to pass.                                                                                              |
| **DROP**                   | Silently discard the packet without notifying the sender.                                                              |
| **REJECT**                 | Block the packet and send an error response to the sender.                                                             |
| **LOG**                    | Record information about the packet, then continue processing subsequent rules.                                        |
| **DNAT** (Destination NAT) | Rewrite the packet's destination IP address and/or port.                                                               |
| **SNAT** (Source NAT)      | Rewrite the packet's source IP address.                                                                                |
| **MASQUERADE**             | Dynamically rewrite the source IP address for NAT, commonly used for internet sharing when the external IP may change. |

`DROP` is quiet. The client may wait until timeout.

`REJECT` is explicit. The client receives a refusal.

Example difference:

| Action     | Client Behavior                                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **DROP**   | The packet is silently discarded. The client waits and eventually times out.                                                      |
| **REJECT** | The packet is blocked and an error response is sent. The client quickly receives a "connection refused" or "unreachable" message. |

### Incoming, Outgoing, and Forwarded Traffic

Traffic direction matters.

| Traffic Direction     | Description                                         |
| --------------------- | --------------------------------------------------- |
| **Incoming traffic**  | Remote client → this machine                        |
| **Outgoing traffic**  | This machine → remote server                        |
| **Forwarded traffic** | One network → this machine/router → another network |

Diagram:

```text
Incoming:
Internet ---> Server

Outgoing:
Server ---> Internet

Forwarded:
LAN Client ---> Linux Router ---> Internet
```

Most host firewalls focus on incoming traffic.

Routers, gateways, and NAT systems also care heavily about forwarded traffic.

### Ports and Protocols

Many services listen on well-known ports.

| Port / Protocol    | Service                  |
| ------------------ | ------------------------ |
| **22/tcp**         | SSH                      |
| **53/tcp, 53/udp** | DNS                      |
| **80/tcp**         | HTTP                     |
| **443/tcp**        | HTTPS                    |
| **25/tcp**         | SMTP                     |
| **3306/tcp**       | MySQL / MariaDB          |
| **5432/tcp**       | PostgreSQL               |
| **21/tcp**         | FTP (control connection) |

Check listening services with:

```bash
sudo ss -tulnp
```

Example output:

```text
Netid State  Local Address:Port  Peer Address:Port Process
tcp   LISTEN 0.0.0.0:22          0.0.0.0:*         users:(("sshd",pid=1100,fd=3))
tcp   LISTEN 0.0.0.0:80          0.0.0.0:*         users:(("nginx",pid=2200,fd=6))
```

Interpretation:

- sshd is listening on TCP port 22.
- nginx is listening on TCP port 80.
- A firewall can decide whether remote clients can reach those ports.

### Firewall Tools on Linux

Linux has several firewall management tools.

Common ones include:

- iptables
- nftables
- ufw
- firewalld

This note focuses on:

- iptables
- ufw
- firewalld

A simple comparison:

| Firewall Tool                    | Description                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **iptables**                     | Low-level and powerful firewall framework; commonly found on older Linux systems.                                |
| **ufw** (Uncomplicated Firewall) | Simple and beginner-friendly firewall interface; commonly used on Ubuntu.                                        |
| **firewalld**                    | Zone-based, dynamic firewall management tool; commonly used on Fedora, RHEL, CentOS, AlmaLinux, and Rocky Linux. |

Modern systems often use `nftables` underneath, even when administrators use higher-level tools such as `firewalld` or `ufw`.

### Safety Warning for Remote Servers

Firewall mistakes can lock you out of a remote server.

Before changing firewall rules over SSH:

- allow SSH first
- know your current source IP
- use a temporary rollback plan
- keep a second session open
- avoid setting default deny before allowing SSH
- test carefully

A safe pattern is:

1. Allow SSH from your trusted IP.
2. Confirm the rule exists.
3. Only then enable stricter defaults.
4. Test with a new SSH session before closing the old one.

On remote servers, a bad firewall command can cause this:

- You block port 22.
- Your SSH session disconnects.
- You cannot reconnect.
- Recovery may require console, cloud rescue mode, or provider access.

### `iptables`

`iptables` is a low-level firewall tool for managing packet filtering rules.

It uses tables, chains, and rules.

The most common table for basic filtering is:

```text
filter
```

The default chains in the filter table are:

- INPUT
- FORWARD
- OUTPUT

Diagram:

```text
Packet entering local machine
        |
        v
INPUT chain
        |
        v
local service, if allowed


Packet leaving local machine
        |
        v
OUTPUT chain
        |
        v
network


Packet passing through machine
        |
        v
FORWARD chain
        |
        v
another network
```

### Viewing `iptables` Rules

Use:

```bash
sudo iptables -L
```

A more useful version includes numbers and numeric ports:

```bash
sudo iptables -L -n -v --line-numbers
```

Example output:

```text
Chain INPUT (policy ACCEPT)
num  pkts bytes target  prot opt in  out source      destination
1    1200  96K ACCEPT  all  --  *   *   0.0.0.0/0   0.0.0.0/0   ctstate RELATED,ESTABLISHED
2       5  420 DROP    icmp --  *   *   0.0.0.0/0   0.0.0.0/0   icmp echo-request
3     200 18K ACCEPT  tcp  --  *   *   0.0.0.0/0   0.0.0.0/0   tcp dpt:22
4      20 1600 ACCEPT tcp  --  *   *   0.0.0.0/0   0.0.0.0/0   tcp dpt:80

Chain FORWARD (policy DROP)
num  pkts bytes target  prot opt in  out source          destination
1       0    0 ACCEPT  all  --  *   *   192.168.1.0/24  192.168.1.0/24
2       0    0 DROP    all  --  *   *   0.0.0.0/0       0.0.0.0/0

Chain OUTPUT (policy ACCEPT)
num  pkts bytes target  prot opt in  out source      destination
```

Interpretation:

- INPUT policy is ACCEPT.
- Established connections are allowed.
- ICMP echo requests are dropped.
- SSH on port 22 is allowed.
- HTTP on port 80 is allowed.
- FORWARD policy is DROP.
- OUTPUT policy is ACCEPT.

### `iptables` Rule Order

Rule order matters.

iptables checks rules from top to bottom.

```text
Packet arrives
    |
    v
Rule 1 match? yes -> action
    |
    no
    v
Rule 2 match? yes -> action
    |
    no
    v
Rule 3 match? yes -> action
    |
    no
    v
Default policy
```

If a broad `DROP` rule appears before an `ACCEPT` rule, the later `ACCEPT` may never be reached.

Example bad order:

- DROP all traffic
- ACCEPT port 22

The SSH allow rule is useless because traffic was already dropped.

### Adding an `iptables` Rule

Allow incoming HTTP:

```bash
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

Meaning:

| iptables Option | Description                                               |
| --------------- | --------------------------------------------------------- |
| **-A INPUT**    | Append a rule to the **INPUT** chain.                     |
| **-p tcp**      | Match **TCP** packets.                                    |
| **--dport 80**  | Match packets with destination port **80**.               |
| **-j ACCEPT**   | Jump to the **ACCEPT** target and allow matching packets. |

Allow SSH:

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

Block ping:

```bash
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
```

### Deleting an `iptables` Rule

First list with line numbers:

```bash
sudo iptables -L INPUT -n -v --line-numbers
```

Example:

```text
Chain INPUT (policy ACCEPT)
num  target  prot source      destination
1    ACCEPT  tcp  0.0.0.0/0   0.0.0.0/0   tcp dpt:22
2    ACCEPT  tcp  0.0.0.0/0   0.0.0.0/0   tcp dpt:80
```

Delete rule 2:

```bash
sudo iptables -D INPUT 2
```

Interpretation:

- The second rule in the INPUT chain is removed.
- If that rule allowed HTTP, HTTP may now be blocked depending on other rules and policy.

### Saving `iptables` Rules

iptables changes are usually runtime-only unless saved.

On Debian-based systems:

```bash
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

You may need:

```bash
sudo apt install iptables-persistent
```

On older Red Hat-based systems:

```bash
sudo service iptables save
```

Important:

```text
If rules are not saved, they may disappear after reboot.
```

### `ufw`

UFW stands for Uncomplicated Firewall.

It provides a simpler interface for common firewall tasks.

It is common on Ubuntu and beginner-friendly systems.

Check status:

```bash
sudo ufw status numbered
```

Example output:

```text
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

Interpretation:

- UFW is active.
- SSH, HTTP, and HTTPS are allowed from anywhere.
- Ports 1000 through 2000 are allowed only from 192.168.1.0/24.
- IPv6 versions of some rules also exist.

### Basic `ufw` Commands

Allow SSH:

```bash
sudo ufw allow ssh
```

Allow port 22 explicitly:

```bash
sudo ufw allow 22/tcp
```

Allow HTTP:

```bash
sudo ufw allow http
```

Allow HTTPS:

```bash
sudo ufw allow https
```

Deny HTTP:

```bash
sudo ufw deny http
```

Delete a numbered rule:

```bash
sudo ufw status numbered
sudo ufw delete 2
```

Enable UFW:

```bash
sudo ufw enable
```

Disable UFW:

```bash
sudo ufw disable
```

### UFW Default Policies

A common safe server policy is:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

Meaning:

- Block unsolicited inbound traffic.
- Allow outbound traffic initiated by the server.
- Allow SSH so administrators can connect.
- Enable the firewall.

On a remote server, allow SSH before enabling UFW.

### `firewalld`

`firewalld` is a dynamic firewall manager commonly used on Fedora, RHEL, CentOS, AlmaLinux, and Rocky Linux.

It organizes rules into zones.

A zone represents a trust level.

Examples:

| Firewalld Zone | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| **public**     | For untrusted networks; only explicitly allowed services are accessible. |
| **home**       | For home networks with a moderate level of trust.                        |
| **work**       | For work networks with trusted devices and services.                     |
| **internal**   | For internal trusted networks.                                           |
| **trusted**    | All network traffic is allowed.                                          |
| **drop**       | Incoming traffic is silently dropped.                                    |
| **block**      | Incoming traffic is rejected with an error response.                     |

Diagram:

```text
eth0 connected to internet
        |
        v
public zone
        |
        v
allow ssh, http, https


eth1 connected to office LAN
        |
        v
internal zone
        |
        v
allow more trusted services
```

### Runtime vs Permanent Configuration

firewalld has two configurations:

- runtime      active now, lost after reload or reboot
- permanent    saved on disk, used after reload or reboot

Commands without `--permanent` usually affect runtime only.

Commands with `--permanent` save the rule, but the rule usually needs reload before it becomes active.

Common pattern:

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

### Viewing firewalld Rules

List active zone configuration:

```bash
sudo firewall-cmd --list-all
```

Example output:

```text
public (active)
  target: default
  interfaces: eth0
  services: ssh dhcpv6-client http https
  ports: 8080/tcp 9090/tcp
  masquerade: no
  forward-ports:
  rich rules:
    rule family="ipv4" source address="192.168.0.0/24" accept
    rule family="ipv4" source address="10.0.0.0/8" port port="443" protocol="tcp" accept
```

Interpretation:

- The active zone is public.
- Interface eth0 is assigned to it.
- SSH, HTTP, and HTTPS are allowed.
- Custom ports 8080/tcp and 9090/tcp are allowed.
- There are rich rules for specific source networks.

Check zones:

```bash
sudo firewall-cmd --get-zones
sudo firewall-cmd --get-default-zone
sudo firewall-cmd --get-active-zones
```

### Adding and Removing firewalld Rules

Allow SSH permanently:

```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

Allow a custom port:

```bash
sudo firewall-cmd --permanent --add-port=8443/tcp
sudo firewall-cmd --reload
```

Remove HTTP:

```bash
sudo firewall-cmd --permanent --remove-service=http
sudo firewall-cmd --reload
```

List again:

```bash
sudo firewall-cmd --list-all
```

### firewalld Zones and Interfaces

Move an interface to the internal zone:

```bash
sudo firewall-cmd --permanent --zone=internal --change-interface=eth1
sudo firewall-cmd --reload
sudo firewall-cmd --zone=internal --list-all
```

Create a custom zone:

```bash
sudo firewall-cmd --permanent --new-zone=web-admin
sudo firewall-cmd --permanent --zone=web-admin --add-service=https
sudo firewall-cmd --permanent --zone=web-admin --add-source=192.168.50.0/24
sudo firewall-cmd --reload
```

Interpretation:

- A new zone called web-admin is created.
- HTTPS is allowed in that zone.
- Only traffic from 192.168.50.0/24 is associated with it.

### firewalld Rich Rules

Rich rules allow more specific matching.

Allow HTTPS only from `10.0.0.0/8`:

```bash
sudo firewall-cmd --permanent \
  --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" service name="https" accept'

sudo firewall-cmd --reload
```

List rich rules:

```bash
sudo firewall-cmd --list-rich-rules
```

Example output:

```text
rule family="ipv4" source address="10.0.0.0/8" service name="https" accept
```

Interpretation:

```text
Only clients from 10.0.0.0/8 match this HTTPS allow rule.
```

### Choosing Between `iptables`, `ufw`, and `firewalld`

Use ufw:

- simple host firewall
- small servers
- desktops
- Ubuntu-style systems

Use firewalld:

- zone-based firewalling
- multiple interfaces
- enterprise distributions
- runtime and permanent rule management

Use iptables:

- low-level control
- legacy systems
- advanced packet filtering
- systems without a higher-level firewall manager

Rule of thumb:

- ufw is easiest.
- firewalld is better for zones.
- iptables is powerful but easier to misconfigure.

### Scenario 1: Allow SSH but Block HTTP with UFW

#### Goal

Allow remote administration through SSH while blocking web traffic on HTTP port 80.

#### Simulate

Check current status:

```bash
sudo ufw status numbered
```

Allow SSH:

```bash
sudo ufw allow 22/tcp
```

Deny HTTP:

```bash
sudo ufw deny 80/tcp
```

Enable UFW if not already enabled:

```bash
sudo ufw enable
```

#### Check

```bash
sudo ufw status numbered
```

Example output:

```text
Status: active

     To        Action      From
     --        ------      ----
[ 1] 22/tcp    ALLOW IN    Anywhere
[ 2] 80/tcp    DENY IN     Anywhere
```

#### Test

From another machine:

```bash
ssh user@SERVER_IP
curl -I http://SERVER_IP
```

Example SSH result:

```text
user@SERVER_IP's password:
```

Example HTTP result:

```text
curl: (7) Failed to connect to SERVER_IP port 80: Connection refused
```

or:

```text
curl: (28) Connection timed out
```

#### Interpretation

- SSH is allowed, so remote administration works.
- HTTP is blocked, so web traffic cannot reach port 80.
- A timeout usually suggests DROP-like behavior.
- Connection refused may mean no service is listening or the firewall rejected it.

### Scenario 2: Deny Incoming by Default and Allow Outgoing

#### Goal

Create a secure default host firewall posture.

#### Simulate

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

#### Check

```bash
sudo ufw status verbose
```

Example output:

```text
Status: active
Logging: on
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
```

#### Interpretation

- Unsolicited inbound traffic is blocked.
- Outbound traffic from the server is allowed.
- SSH remains reachable.
- This is a common baseline for servers.

### Scenario 3: Block ICMP Echo Requests

#### Goal

Prevent the system from replying to ping requests.

#### iptables Simulation

```bash
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
```

#### Check

```bash
sudo iptables -L INPUT -n -v --line-numbers
```

Example output:

```text
num  pkts bytes target prot opt source      destination
1       3   252 DROP   icmp --  0.0.0.0/0   0.0.0.0/0   icmp echo-request
```

#### Test

From another host:

```bash
ping SERVER_IP
```

Example output:

```text
PING SERVER_IP 56(84) bytes of data.
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2
```

#### Interpretation

- The server is not replying to ICMP echo requests.
- This can reduce casual network discovery.
- However, blocking all ICMP can also make troubleshooting harder.

#### Remove the Rule

List line numbers:

```bash
sudo iptables -L INPUT --line-numbers
```

Delete the matching rule number:

```bash
sudo iptables -D INPUT 1
```

### Scenario 4: Allow HTTP Only from One IP Address

#### Goal

Restrict access to a web service so only one trusted client can connect.

#### UFW Simulation

Allow HTTP from one IP:

```bash
sudo ufw allow from 192.168.1.50 to any port 80 proto tcp
```

Deny other HTTP traffic:

```bash
sudo ufw deny 80/tcp
```

#### Check

```bash
sudo ufw status numbered
```

Example output:

```text
Status: active

     To        Action      From
     --        ------      ----
[ 1] 80/tcp    ALLOW IN    192.168.1.50
[ 2] 80/tcp    DENY IN     Anywhere
```

#### Test

From allowed host:

```bash
curl -I http://SERVER_IP
```

Example output:

```text
HTTP/1.1 200 OK
```

From blocked host:

```bash
curl -I http://SERVER_IP
```

Example output:

```text
curl: (28) Failed to connect: Connection timed out
```

#### Interpretation

- The trusted IP can access HTTP.
- Other sources are blocked.
- This is useful for admin panels, staging sites, or private dashboards.

### Scenario 5: Safely Change Firewall Rules on a Remote Server

#### Goal

Avoid locking yourself out while changing firewall rules over SSH.

#### Safe Pattern with UFW

First, find your client IP from the server side:

```bash
echo "$SSH_CLIENT"
```

Example output:

```text
203.0.113.25 53244 22
```

Allow SSH from your IP:

```bash
sudo ufw allow from 203.0.113.25 to any port 22 proto tcp
```

Allow fallback SSH generally if needed:

```bash
sudo ufw allow 22/tcp
```

Then set defaults:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

Enable:

```bash
sudo ufw enable
```

Open a new terminal and test a second SSH connection before closing the first.

#### Optional Rollback Timer

Before risky changes, schedule a rollback:

```bash
echo "sudo ufw disable" | at now + 5 minutes
```

If the firewall works, cancel the job:

```bash
atq
atrm JOB_ID
```

#### Interpretation

- The rollback timer protects against accidental lockout.
- If you lose SSH access, UFW disables itself after 5 minutes.
- If everything works, cancel the rollback job.

### Scenario 6: Allow SSH Only from Trusted IPs

#### Goal

Reduce SSH attack surface by allowing only known source addresses.

#### UFW Simulation

Allow trusted IP:

```bash
sudo ufw allow from 203.0.113.25 to any port 22 proto tcp
```

Deny other SSH:

```bash
sudo ufw deny 22/tcp
```

#### Check

```bash
sudo ufw status numbered
```

Example output:

```text
Status: active

     To        Action      From
     --        ------      ----
[ 1] 22/tcp    ALLOW IN    203.0.113.25
[ 2] 22/tcp    DENY IN     Anywhere
```

#### Interpretation

- Only 203.0.113.25 can connect to SSH.
- Other IP addresses are denied.
- This reduces brute-force exposure.

#### Important Warning

- Do not do this unless you know your trusted IP is stable.
- If your IP changes, you may lock yourself out.

### Scenario 7: Rate-Limit Incoming Connections

#### Goal

Limit repeated connection attempts to reduce brute-force or abuse.

#### UFW SSH Rate Limit

UFW has a simple built-in rate limit:

```bash
sudo ufw limit ssh
```

Check:

```bash
sudo ufw status numbered
```

Example output:

```text
Status: active

     To        Action      From
     --        ------      ----
[ 1] 22/tcp    LIMIT IN    Anywhere
```

#### Interpretation

- UFW allows SSH but rate-limits repeated connection attempts.
- This can help reduce brute-force attempts.

#### iptables Example

Limit new TCP connections to port 8080:

```bash
sudo iptables -A INPUT -p tcp --dport 8080 -m conntrack --ctstate NEW \
  -m limit --limit 100/minute --limit-burst 20 -j ACCEPT

sudo iptables -A INPUT -p tcp --dport 8080 -j DROP
```

Check:

```bash
sudo iptables -L INPUT -n -v --line-numbers
```

Example output:

```text
num  pkts bytes target prot source      destination
1    1000  60K ACCEPT tcp  0.0.0.0/0   0.0.0.0/0 tcp dpt:8080 ctstate NEW limit: avg 100/min burst 20
2     200  12K DROP   tcp  0.0.0.0/0   0.0.0.0/0 tcp dpt:8080
```

#### Interpretation

- New connections to port 8080 are allowed up to the rate limit.
- Excess traffic is dropped.
- This can reduce simple connection floods, but it is not a full DDoS solution.

### Scenario 8: Log Dropped Packets

#### Goal

Record blocked packets for investigation.

#### iptables Simulation

Add a logging rule before a drop rule:

```bash
sudo iptables -A INPUT -m limit --limit 10/min --limit-burst 5 \
  -j LOG --log-prefix "iptables denied: " --log-level 4

sudo iptables -A INPUT -j DROP
```

#### Check Logs

On many systems:

```bash
sudo journalctl -k | grep "iptables denied"
```

or:

```bash
sudo dmesg | grep "iptables denied"
```

Example log:

```text
kernel: iptables denied: IN=eth0 OUT= MAC=... SRC=198.51.100.20 DST=203.0.113.10 LEN=60 PROTO=TCP SPT=51512 DPT=23
```

#### Interpretation

- A packet from 198.51.100.20 tried to reach port 23.
- Port 23 is Telnet, which is usually unsafe.
- The packet was logged and then dropped.

#### Important Warning

- Always rate-limit firewall logging.
- Logging every dropped packet can flood logs and hurt performance.

### Scenario 9: Forward Port 8080 to Port 80

#### Goal

Redirect traffic arriving on port 8080 to a service listening on port 80.

#### Local Redirect with iptables

This redirects local incoming TCP port 8080 to port 80:

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-port 80
```

If testing from the same host, also use OUTPUT redirect:

```bash
sudo iptables -t nat -A OUTPUT -p tcp -o lo --dport 8080 -j REDIRECT --to-port 80
```

#### Check NAT Rules

```bash
sudo iptables -t nat -L -n -v --line-numbers
```

Example output:

```text
Chain PREROUTING (policy ACCEPT)
num  pkts bytes target   prot source      destination
1      10   600 REDIRECT tcp  0.0.0.0/0   0.0.0.0/0 tcp dpt:8080 redir ports 80
```

#### Test

Run a web server on port 80, then from another host:

```bash
curl -I http://SERVER_IP:8080
```

Example output:

```text
HTTP/1.1 200 OK
```

#### Interpretation

- The client connects to port 8080.
- iptables redirects the connection to local port 80.
- The web server responds successfully.

### Scenario 10: Block Outgoing Traffic to a Specific IP

#### Goal

Prevent the server from connecting to a known unwanted destination.

#### UFW Simulation

Block outgoing traffic to a specific IP:

```bash
sudo ufw deny out to 203.0.113.200
```

#### Check

```bash
sudo ufw status numbered
```

Example output:

```text
Status: active

     To              Action      From
     --              ------      ----
[ 1] 203.0.113.200   DENY OUT    Anywhere
```

#### Test

```bash
curl http://203.0.113.200
```

Example output:

```text
curl: (7) Failed to connect to 203.0.113.200 port 80
```

#### Interpretation

- The local system is blocked from connecting to that IP.
- Outbound filtering can help prevent compromised systems from calling known malicious infrastructure.

#### Note About Domains

Firewalls usually filter IP addresses, ports, protocols, and interfaces.

Blocking domains is more complicated because domain names can resolve to changing IP addresses.

For domain-based blocking, consider:

- DNS filtering
- proxy filtering
- application-layer controls
- regularly updated IP sets

### Scenario 11: firewalld Public Zone with HTTP and HTTPS

#### Goal

Allow web traffic using firewalld.

#### Simulate

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

#### Check

```bash
sudo firewall-cmd --list-all
```

Example output:

```text
public (active)
  services: ssh http https
  ports:
```

#### Interpretation

- The public zone allows SSH, HTTP, and HTTPS.
- Web clients should be able to connect if services are listening.

Check listening services:

```bash
sudo ss -tulnp | grep -E ':80|:443'
```

### Scenario 12: firewalld Custom Port

#### Goal

Allow a custom TCP port, such as 8443.

#### Simulate

```bash
sudo firewall-cmd --permanent --add-port=8443/tcp
sudo firewall-cmd --reload
```

#### Check

```bash
sudo firewall-cmd --list-ports
```

Example output:

```text
8443/tcp
```

#### Interpretation

- TCP port 8443 is open in the active zone.
- A service still must be listening on that port for clients to connect.

### Scenario 13: firewalld Runtime vs Permanent Rule

#### Goal

Understand why a rule may disappear after reload.

#### Add Runtime Rule Only

```bash
sudo firewall-cmd --add-port=9090/tcp
```

Check:

```bash
sudo firewall-cmd --list-ports
```

Example:

```text
9090/tcp
```

Reload:

```bash
sudo firewall-cmd --reload
```

Check again:

```bash
sudo firewall-cmd --list-ports
```

Example:

```text
```

No output.

#### Interpretation

- The rule was runtime-only.
- It disappeared after reload.
- Use --permanent for persistent rules.

#### Permanent Fix

```bash
sudo firewall-cmd --permanent --add-port=9090/tcp
sudo firewall-cmd --reload
```

### Scenario 14: Diagnose “Service Is Running but Not Reachable”

#### Goal

Use firewall tools to separate service problems from firewall problems.

#### Symptom

A web service should be reachable, but clients cannot connect.

#### Step 1: Check Service

```bash
sudo systemctl status nginx
```

Example:

```text
Active: active (running)
```

#### Step 2: Check Listening Port

```bash
sudo ss -tulnp | grep ':80'
```

Example:

```text
tcp LISTEN 0 511 0.0.0.0:80 0.0.0.0:* users:(("nginx",pid=2200,fd=6))
```

Interpretation:

- nginx is running and listening on port 80.
- If remote clients cannot connect, firewall or network path may be the issue.

#### Step 3: Check Firewall

UFW:

```bash
sudo ufw status numbered
```

firewalld:

```bash
sudo firewall-cmd --list-all
```

iptables:

```bash
sudo iptables -L INPUT -n -v --line-numbers
```

#### Example Firewall Output

```text
Status: active

To        Action      From
--        ------      ----
22/tcp    ALLOW IN    Anywhere
80/tcp    DENY IN     Anywhere
```

#### Interpretation

- The service is running.
- The firewall blocks port 80.
- Allow HTTP or remove the deny rule.

#### Fix with UFW

```bash
sudo ufw allow 80/tcp
```

### Scenario 15: Diagnose “Firewall Rule Exists but Still Cannot Connect”

#### Goal

Understand that firewall rules are only one part of connectivity.

#### Checklist

1. Is the service running?
2. Is the service listening on the expected port?
3. Is it listening on the correct address?
4. Does the firewall allow the traffic?
5. Is the cloud firewall/security group open?
6. Is the client using the correct IP and port?
7. Is routing correct?
8. Is SELinux blocking the service?

Commands:

```bash
sudo systemctl status SERVICE
sudo ss -tulnp
ip addr
ip route
sudo ufw status numbered
sudo firewall-cmd --list-all
sudo iptables -L -n -v
```

Example issue:

- Firewall allows port 80.
- Service listens only on 127.0.0.1:80.
- Remote clients still cannot connect.

Check:

```bash
sudo ss -tulnp | grep ':80'
```

Output:

```text
tcp LISTEN 0 511 127.0.0.1:80 0.0.0.0:* users:(("nginx",pid=2200,fd=6))
```

Interpretation:

- The service listens only on localhost.
- The firewall is not the main problem.
- Configure the service to listen on the external interface or 0.0.0.0 if appropriate.

### Common Firewall Troubleshooting Workflow

When a connection fails:

1. Identify source IP, destination IP, protocol, and port.
2. Check whether the service is listening.
3. Check local firewall rules.
4. Check cloud or upstream firewall rules.
5. Test from the client.
6. Check logs and packet counters.
7. Confirm rule order.
8. Confirm persistence after reboot or reload.

### Step 1: Identify the Traffic

Example:

| Field         | Value          |
| ------------- | -------------- |
| **Client IP** | `192.168.1.50` |
| **Server IP** | `192.168.1.10` |
| **Protocol**  | TCP            |
| **Port**      | 443            |
| **Direction** | Incoming       |

This prevents vague troubleshooting.

### Step 2: Check Service Listening

```bash
sudo ss -tulnp | grep ':443'
```

If there is no listener, the firewall is not the only issue.

### Step 3: Check Firewall Rules

UFW:

```bash
sudo ufw status numbered
```

firewalld:

```bash
sudo firewall-cmd --list-all
```

iptables:

```bash
sudo iptables -L INPUT -n -v --line-numbers
```

### Step 4: Check Packet Counters

iptables counters can show whether traffic is matching rules.

```bash
sudo iptables -L INPUT -n -v --line-numbers
```

Example:

```text
num  pkts bytes target prot source      destination
1       0     0 ACCEPT tcp  0.0.0.0/0   0.0.0.0/0 tcp dpt:443
2     150  9K DROP   all  0.0.0.0/0   0.0.0.0/0
```

Interpretation:

- The HTTPS allow rule has 0 packet matches.
- The traffic may not be reaching this host, or another firewall is blocking it earlier.

### Step 5: Test from Client

Use:

```bash
curl -I http://SERVER_IP
nc -vz SERVER_IP 22
nc -vz SERVER_IP 443
```

Example:

```text
Connection to SERVER_IP 22 port [tcp/ssh] succeeded!
```

Interpretation:

- The TCP connection to port 22 succeeded.
- The service is reachable from this client.

### Useful Command Summary

Check listening services:

```bash
sudo ss -tulnp
```

iptables:

```bash
sudo iptables -L -n -v --line-numbers
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -D INPUT RULE_NUMBER
sudo iptables-save
```

UFW:

```bash
sudo ufw status numbered
sudo ufw status verbose
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw deny 80/tcp
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
sudo ufw delete RULE_NUMBER
```

firewalld:

```bash
sudo firewall-cmd --list-all
sudo firewall-cmd --get-zones
sudo firewall-cmd --get-default-zone
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --remove-service=http
sudo firewall-cmd --permanent --add-port=8443/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-rich-rules
```

Testing:

```bash
curl -I http://SERVER_IP
nc -vz SERVER_IP PORT
ping SERVER_IP
traceroute SERVER_IP
```

Logs:

```bash
sudo journalctl -k
sudo dmesg
sudo journalctl -u firewalld
sudo tail -f /var/log/ufw.log
```

### Safe Lab Cleanup

If you added temporary iptables rules, list them first:

```bash
sudo iptables -L INPUT -n -v --line-numbers
```

Delete only the test rules by number:

```bash
sudo iptables -D INPUT RULE_NUMBER
```

For UFW, list and delete numbered rules:

```bash
sudo ufw status numbered
sudo ufw delete RULE_NUMBER
```

For firewalld test ports:

```bash
sudo firewall-cmd --permanent --remove-port=8443/tcp
sudo firewall-cmd --permanent --remove-port=9090/tcp
sudo firewall-cmd --reload
```

If you created a custom firewalld zone:

```bash
sudo firewall-cmd --permanent --delete-zone=web-admin
sudo firewall-cmd --reload
```

### Practical Challenges

1. Configure the firewall to allow SSH on port 22 but block HTTP on port 80. Test both from another machine.
2. Set the default policy to deny incoming traffic and allow outgoing traffic. Explain why SSH must be allowed before enabling this policy remotely.
3. Block ICMP echo requests and confirm that another host cannot ping the machine. Then remove the rule and test again.
4. Allow HTTP only from a specific IP address. Test from the allowed IP and from a blocked IP.
5. Create a safe rollback plan before changing firewall rules on a remote server.
6. Restrict SSH to a trusted source IP. Explain the risk if your source IP changes.
7. Rate-limit SSH or another TCP service and explain what kind of abuse this helps reduce.
8. Add logging for dropped packets with rate limiting. Review logs and interpret one dropped packet entry.
9. Forward local port 8080 to port 80 and verify that traffic to 8080 reaches the web service.
10. Block outgoing traffic to a specific IP address and test the result with `curl` or `nc`.
11. With firewalld, add a runtime-only port rule, reload firewalld, and observe that the rule disappears.
12. With firewalld, create a permanent custom port rule and verify it survives reload.
13. Diagnose a service that is running but unreachable. Check the service, listening port, firewall rules, and client test output.
14. Compare the same rule implemented with `iptables`, `ufw`, and `firewalld`.
15. Write a short firewall troubleshooting report including source IP, destination IP, protocol, port, rule checked, test command, output, and interpretation.
