## Ports

In computer networking, ports serve as endpoints for communication between devices, similar to doors through which data flows in and out of a computer. In today's interconnected digital landscape, network security is paramount. Network ports are critical points that require diligent management and security measures. Unsecured ports can become vulnerabilities, exposing systems to unauthorized access, data breaches, and various cyber threats. 

Main idea:

- Ports control how data is directed in and out of a computer or server, ensuring proper communication between devices and services.
- They make it possible for multiple services to run simultaneously on a single device by assigning specific ports to each service, thereby organizing traffic effectively.
- While IP addresses identify individual machines on a network, ports differentiate the various services running on a single machine, allowing multiple services to coexist and function properly.
- The **Port Range** extends from 0 to 65,535, providing a wide array of port numbers for different applications and services.
- **Well-Known Ports** range from 0 to 1023 and are reserved for standard services like HTTP (port 80), HTTPS (port 443), FTP (port 21), and SSH (port 22).
- **Registered Ports**, ranging from 1024 to 49151, are assigned to non-standard, less common applications, allowing for a diverse set of services beyond the well-known ones.
- **Dynamic/Private Ports**, ranging from 49152 to 65535, are typically used for temporary purposes or private communications, often assigned dynamically for short-term needs.

Example:

```
+-----------------------------------------------+
|                  Server                       |
|        IP Address: 192.168.1.10               |
|                                               |
|  +---------+     +---------+     +----------+ |
|  | Port 22 |     | Port 80 |     | Port 443 | |
|  |  SSH    |     |  HTTP   |     |  HTTPS   | |
|  +----+----+     +----+----+     +----+-----+ |
|       |               |               |       |
+-------+---------------+---------------+-------+
|               |               |
|               |               |
Client Connections over Network
```

- The server at IP `192.168.1.10` is running services on ports 22 (SSH), 80 (HTTP), and 443 (HTTPS).
- Clients connect to these services by specifying the IP address and the port number.
- The server distinguishes incoming traffic based on the port number.

### Protocols and Their Associated Ports

There are two primary protocols employed in internet communication, each with its own set of 65,536 ports:

I. TCP (Transmission Control Protocol)

- Reliable, connection-oriented.
- Best for data requiring accuracy and completeness.
- Higher security needs, due to its susceptibility to attacks.

II. UDP (User Datagram Protocol)

- Faster, connectionless.
- Suited for streaming, real-time communication where speed is key.
- Lower security needs than TCP, as it doesn't guarantee delivery or order.

Ports in the OSI Model:

```
+-----------------------+
|       Application     |
+-----------------------+
|      Presentation     |
+-----------------------+
|        Session        |
+-----------------------+
| Transport (TCP/UDP)   |  <-- Ports operate here
+-----------------------+
|         Network       |
+-----------------------+
|       Data Link       |
+-----------------------+
|        Physical       |
+-----------------------+
```

### Common Services and Their Ports

Below is a table detailing some of the most commonly used services and their associated port numbers:

| Service            | Port Number | Protocol |
|--------------------|-------------|----------|
| HTTP (Web Server)  | 80          | TCP      |
| HTTPS (Secure Web) | 443         | TCP      |
| FTP (File Transfer)| 21          | TCP      |
| SSH (Secure Shell) | 22          | TCP      |
| Telnet             | 23          | TCP      |
| SMTP (Email Send)  | 25          | TCP      |
| DNS (Domain Name)  | 53          | TCP/UDP  |
| DHCP (Dynamic IP)  | 67, 68      | UDP      |
| TFTP (Trivial FTP) | 69          | UDP      |
| POP3 (Email Receive)| 110        | TCP      |
| IMAP (Email Access)| 143         | TCP      |
| SNMP (Network Manage)| 161       | UDP      |
| LDAP (Directory Access)| 389     | TCP/UDP  |
| SFTP (Secure File Transfer)| 22  | TCP      |
| SQL (Database Access)| Varied*   | TCP      |

Note: SQL services vary in port numbers based on the specific SQL database being used (e.g., MySQL, MSSQL, PostgreSQL, etc.).

### The Importance of Securing Network Ports

Securing network ports is a fundamental aspect of network security. Unsecured or misconfigured ports can lead to:

- Attackers may gain access to systems by exploiting open ports associated with vulnerable services.
- Sensitive information can be compromised if services handling confidential data are accessible through open ports.
- Denial-of-service (DoS) attacks can target open ports to overwhelm services, causing interruptions.
- Open ports can be entry points for malware, including worms and trojans, which can spread across networks.

### Security Measures for Network Ports

#### Implementing Firewalls

Firewalls are essential security devices or software that monitor and control incoming and outgoing network traffic based on predetermined security rules. They establish a barrier between trusted internal networks and untrusted external networks.

#### Managing Open Ports

Monitoring and managing open ports is crucial to prevent unauthorized access.

**Using `netstat`:**

```bash
sudo netstat -tuln
```

**Expected Output:**

```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp6       0      0 :::80                   :::*                    LISTEN
udp        0      0 0.0.0.0:68              0.0.0.0:*
```

- **Proto:** Protocol used (tcp, tcp6, udp).
- **Local Address:** The IP and port on the local machine. `0.0.0.0` means all IPv4 addresses on the local machine.
- **Foreign Address:** The remote IP and port; `*` indicates any.
- **State:** The state of the socket (e.g., `LISTEN` for servers).

**Using `ss`:**

```bash
sudo ss -tuln
```

**Expected Output:**

```
Netid State      Recv-Q Send-Q Local Address:Port               Peer Address:Port
udp   UNCONN     0      0      0.0.0.0:68                      0.0.0.0:*
tcp   LISTEN     0      128    0.0.0.0:22                      0.0.0.0:*
tcp   LISTEN     0      128    [::]:80                         [::]:*
```

Similar to `netstat`, but `ss` provides faster and more detailed socket information.

#### Evaluating Services

Determine if the services running on open ports are required for your system's operation.

**Stopping a Service:**

```bash
sudo systemctl stop service_name
```

The service `service_name` has been stopped.

**Disabling a Service:**

```bash
sudo systemctl disable service_name
```

**Expected Output:**

```
Removed /etc/systemd/system/multi-user.target.wants/service_name.service.
```

The service `service_name` has been disabled and will not start at boot.

#### Closing Unused Ports

Closing ports that are not in use reduces the attack surface.

**Using Nmap to Scan for Open Ports:**

```bash
nmap -sT localhost
```

**Expected Output:**

```
Starting Nmap 7.80 ( https://nmap.org ) at 2023-10-08 12:34 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000012s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
631/tcp open  ipp

Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds
```

Nmap found that ports 22 (SSH), 80 (HTTP), and 631 (Internet Printing Protocol) are open on localhost.

**Using `ufw` to Deny Access:**

```bash
sudo ufw deny 631/tcp
```

**Expected Output:**

```
Rule added
Rule added (v6)
```

Incoming TCP traffic on port 631 is now blocked.

**Verifying Port Closure:**

```bash
sudo ss -tuln | grep :631
```

If there's no output, it indicates that port 631 is no longer listening.

####  Changing Default Ports

Changing default ports can help obscure services from automated scans and reduce the likelihood of attacks targeting default port numbers.

##### Example: Changing SSH Port

**Editing the SSH Configuration:**

```bash
sudo nano /etc/ssh/sshd_config
```

Find the line:

```
#Port 22
```

Uncomment and change it to:

```
Port 2222
```

**Restarting the SSH Service:**

```bash
sudo systemctl restart sshd
```

**Updating Firewall Rules:**

```bash
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp
```

**Expected Output:**

```
Rule added
Rule added (v6)
Deleting...
Rule deleted
Rule deleted (v6)
```

The firewall now allows traffic on port 2222 and blocks port 22.

**Verifying SSH on New Port:**

```bash
sudo ss -tuln | grep :2222
```

**Expected Output:**

```
tcp   LISTEN 0      128    0.0.0.0:2222      0.0.0.0:*
tcp   LISTEN 0      128    [::]:2222         [::]:*
```

SSH is now listening on port 2222.

When connecting via SSH, specify the new port:

```bash
ssh -p 2222 user@hostname
```

While changing default ports can reduce noise from automated scans, it is not a substitute for proper security measures like strong authentication and encryption.

##### Securing Port Forwarding

Port forwarding can expose internal services to external networks if not properly configured.

**Using `iptables` to List NAT Rules:**

```bash
sudo iptables -t nat -L -n -v
```

**Expected Output:**

```
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target     prot opt in     out     source               destination
```

If there are no entries under the chains, it indicates that no port forwarding rules are set up.

Only forward necessary ports and restrict access using firewall rules.

**Example of Adding a Port Forwarding Rule:**

Forward external port 8080 to internal port 80 on a specific internal IP:

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.10:80
sudo iptables -A FORWARD -p tcp -d 192.168.1.10 --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
```

**Expected Output:**

*(No output if successful)*

Traffic arriving on port 8080 will be forwarded to port 80 on the internal IP `192.168.1.10`.

Limit port forwarding to specific external IP addresses.

**Enable Logging for Port Forwarding:**

```bash
sudo iptables -A FORWARD -j LOG --log-prefix "PORT_FORWARDING: "
```

**Expected Output:**

*(No output if successful)*

This rule logs forwarded packets with the prefix "PORT_FORWARDING:" to the system logs.

### Monitoring Ports and Processes

Proactive monitoring of network ports and associated processes is essential for detecting anomalies and potential security threats.

#### Using `lsof` (List Open Files)

**Finding Processes Using a Specific Port:**

```bash
sudo lsof -i :80
```

**Expected Output:**

```
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
apache2  1234   root    4u  IPv6  12345      0t0  TCP *:http (LISTEN)
apache2  1235 www-data 4u  IPv6  12345      0t0  TCP *:http (LISTEN)
apache2  1236 www-data 4u  IPv6  12345      0t0  TCP *:http (LISTEN)
```

- **COMMAND:** The name of the process (`apache2`).
- **PID:** Process ID.
- **USER:** The user running the process.
- **FD:** File descriptor.
- **TYPE:** Type of network (IPv4 or IPv6).
- **DEVICE/SIZE/OFF:** Device and size/offset.
- **NODE:** Network node (TCP).
- **NAME:** The port and state (e.g., `*:http (LISTEN)`).

- **Filtering for Listening Processes:**

```bash
sudo lsof -i TCP -sTCP:LISTEN
```

**Expected Output:**

```
COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd     2345     root    3u  IPv4  67890      0t0  TCP *:ssh (LISTEN)
sshd     2345     root    4u  IPv6  67891      0t0  TCP *:ssh (LISTEN)
apache2  1234     root    4u  IPv6  12345      0t0  TCP *:http (LISTEN)
```

Lists all processes that are in a `LISTEN` state for TCP connections.

#### Using `netstat`

**Listing Processes by Port:**

```bash
sudo netstat -tulpn | grep :22
```

**Expected Output:**

```
tcp   0    0 0.0.0.0:22    0.0.0.0:*    LISTEN   2345/sshd
tcp6  0    0 :::22         :::*         LISTEN   2345/sshd
```

- **Proto:** Protocol (`tcp` or `tcp6`).
- **Local Address:** IP and port (`0.0.0.0:22` means listening on all IPv4 interfaces on port 22).
- **Foreign Address:** `*` indicates any.
- **State:** `LISTEN` indicates it's waiting for incoming connections.
- **PID/Program name:** Process ID and name (`2345/sshd`).

#### Using `ss` (Socket Statistics)

- **Listing Sockets for a Specific Port:**

```bash
sudo ss -tulwn | grep :80
```

**Expected Output:**

```
tcp   LISTEN 0      128    0.0.0.0:80      0.0.0.0:*
tcp   LISTEN 0      128    [::]:80         [::]:*
```

- **State:** `LISTEN` indicates the socket is listening for connections.
- **Recv-Q/Send-Q:** Receive and send queue sizes.
- **Local Address:Port:** The IP and port on the local machine.
- **Peer Address:Port:** The remote IP and port; `*` indicates any.

### Checking Socket Status with `ss`

`ss` provides detailed information about network sockets.

- **Display Summary Statistics:**

```bash
ss -s
```

**Expected Output:**

```
Total: 100 (kernel 110)
TCP:   50 (estab 10, closed 30, orphaned 0, synrecv 0, timewait 30/0), ports 0

Transport Total     IP        IPv6
*         110       -         -
RAW       0         0         0
UDP       20        15        5
TCP       20        10        10
INET      40        25        15
FRAG      0         0         0
```

Provides a summary of socket usage, including the number of TCP connections in different states.

**List Established TCP Connections:**

```bash
ss -tan state established
```

**Expected Output:**

```
State      Recv-Q Send-Q Local Address:Port               Peer Address:Port
ESTAB      0      0      192.168.1.5:22                   192.168.1.10:54321
ESTAB      0      0      192.168.1.5:80                   192.168.1.20:12345
```

Shows TCP connections that are currently established, including the local and peer addresses and ports.

**Count Established Connections:**

```bash
ss -tan state established | wc -l
```

**Expected Output:**

```
3
```

The output number indicates the total established TCP connections (including the header line).

### Network Scanning with Nmap

Nmap (Network Mapper) is a powerful open-source tool for network exploration and security auditing. It allows you to discover hosts and services on a computer network, thereby creating a "map" of the network.

Main idea:

- Identifies live hosts on a network.
- Discovers open ports on target hosts.
- Determines the application name and version running on each port.
- Estimates the operating system and hardware characteristics of network devices.
- Extensible with scripts for advanced discovery and vulnerability detection.

Common Use Cases:

- Identify open ports and vulnerabilities.
- Map network devices and services.
- Ensure systems meet security policies.
- Gather information for ethical hacking.
- Diagnose network issues.

#### Basic Nmap Commands

I. **Default TCP Scan:**

```bash
nmap <IP-address>
```

**Expected Output:**

```
Starting Nmap 7.80 ( https://nmap.org ) at 2023-10-08 13:00 UTC
Nmap scan report for example.com (93.184.216.34)
Host is up (0.10s latency).
Not shown: 997 filtered ports
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 5.23 seconds
```

Nmap scanned the target IP and found that ports 80, 443, and 8080 are open.

II. **TCP SYN Scan (Stealth Scan):**

```bash
sudo nmap -sS <IP-address>
```

**Expected Output:**

Similar to the default scan but may find additional ports due to different scanning technique.

III. **Ping Scan (Discover Live Hosts):**

```bash
nmap -sn 192.168.1.0/24
```

**Expected Output:**

```
Starting Nmap 7.80 ( https://nmap.org ) at 2023-10-08 13:05 UTC
Nmap scan report for 192.168.1.1
Host is up (0.0010s latency).
Nmap scan report for 192.168.1.5
Host is up (0.0015s latency).
Nmap scan report for 192.168.1.10
Host is up (0.0012s latency).
Nmap done: 256 IP addresses (3 hosts up) scanned in 2.50 seconds
```

Nmap found that hosts at IP addresses `192.168.1.1`, `192.168.1.5`, and `192.168.1.10` are up.

IV. **Enable Version Detection:**

```bash
nmap -sV <IP-address>
```

**Expected Output:**

```
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http     Apache httpd 2.4.29 ((Ubuntu))
443/tcp open  ssl/http Apache httpd 2.4.29 ((Ubuntu))
```

Nmap detected the services running on the open ports and identified their versions.

V. **Enable OS Detection:**

```bash
sudo nmap -O <IP-address>
```

**Expected Output:**

```
OS details: Linux 3.10 - 4.11
Network Distance: 1 hop
```

Nmap estimates the target is running a Linux operating system with a kernel version between 3.10 and 4.11.

VI. **Combining Multiple Scans:**

```bash
sudo nmap -A <IP-address>
```

**Expected Output:**

Provides detailed information including open ports, services, versions, OS detection, and traceroute.

VII. **Saving Output to a File:**

```bash
nmap -oN output.txt <IP-address>
```

**Expected Output:**

The scan results are saved in `output.txt`.

**Interpreting Nmap Output**

| **Category**         | **Description**                                                                                          |
|----------------------|----------------------------------------------------------------------------------------------------------|
| **Host Status**      | Indicates if the host is **up** or **down**.                                                              |
| **Port State**       | - **open**: Accepting connections. <br> - **closed**: Not accepting connections but reachable. <br> - **filtered**: Status undetermined due to packet filtering. |
| **Service Detection**| Displays the **service name** and **version** running on each open port.                                 |

**Legal Implications:**

- Scanning networks without permission is illegal and unethical.
- Only scan networks and systems you own or have explicit permission to scan.

### Challenges

1. Some ports are reserved for specific services. Can they be used for other purposes? If so, what are the potential risks or benefits?
2. How can you check which port numbers are available for use on your system? Is there a difference between checking on Linux vs. Windows?
3. You suspect an unknown service is running on your machine. How can you find out which process is running on a specific port? 
4. You've installed a new service or application. How can you find out which port(s) it is using?
5. What is the primary reason for using ports in networking? How do they aid in multi-tasking or multi-service operations?
6. There are 65535 ports available. Is this number split between different protocols? How are port numbers managed and allocated in a computer system?
7. What is the difference between TCP and UDP ports? How does their underlying mechanism differ, and why might you choose one over the other?
8. Imagine you've been given access to a server. How can you view open ports on this server, and what tools might you use?
9. What is Nmap, and how is it used? Can you perform a basic scan of a given IP address or domain to view its open ports?
10. How can you identify the service or application associated with a specific port on your system?
11. What is a firewall, and why is it crucial for protecting ports? Can you configure a basic firewall rule to allow or block traffic on a specific port?
12. What happens if two applications try to bind to the same port? How would you resolve such a conflict?
13. What is the range for dynamic or private ports, and why are they essential? Can you provide a real-world scenario where they might be used?
14. How you might configure rate limiting on a specific port to prevent potential DDoS attacks?
15. What are some of the most commonly targeted ports for cyberattacks in the history of the internet? Why do you think they were targeted?
16. If you suspect a port is vulnerable or has been exploited, how would you secure it? What tools and strategies would you deploy?
17. How does Network Address Translation (NAT) relate to ports, and why is it significant for modern networks, especially in the context of private and public IP addresses?
18. Select five common networking services or protocols (e.g., HTTP, FTP, SSH). What are their default port numbers, and why is it valuable to know them?
19. How do ethical hackers utilize port scanning in their methodologies, and what are the ethics surrounding such scans?
20. With the rise of IoT devices and the ever-growing internet, do you think the current port system will remain sustainable? How might networking evolve in the future?
