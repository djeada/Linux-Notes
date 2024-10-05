## Ports

In computer networking, ports serve as crucial endpoints for communication between devices, similar to doors through which data flows in and out of a computer.

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

### Security Considerations

When it comes to system security, managing and securing network ports is a fundamental aspect. This involves a range of strategies and tools to prevent unauthorized access and to mitigate potential vulnerabilities. Here's a more detailed look at each consideration:

I. Firewalls

- Firewalls are essential for managing and monitoring access to network ports. They act as a barrier, controlling the traffic based on security rules.
- Use tools like `ufw` (Uncomplicated Firewall) or `iptables` for Linux systems. These allow you to configure firewall rules that are specific to each port, thereby enhancing security.
- For example use, `sudo ufw allow 80` to allow HTTP traffic on port 80.

II. Open Ports

- Ports that are open on your network can serve as potential entry points for unauthorized access or cyber attacks.
- Regularly check for open ports using commands like `sudo netstat -tuln` or `sudo ss -tuln`. This helps in identifying and managing open ports.

III. Unused Ports

- Ports that are open but not in use can be a security liability. Attackers often exploit these unused ports.
- It's advisable to close unused ports. You can do this using commands like `sudo ufw deny [port number]`.
- For example, `sudo ufw deny 8080` to block any traffic on port 8080.

IV. Default Ports

- Default ports, like port 22 for SSH, are commonly known and often targeted by attackers.
- It's recommended to change commonly used default ports to non-standard ports. This can reduce the risk of automated attacks.
- Changing the SSH port from 22 to a non-standard port can significantly decrease the risk of brute-force attacks.

V. Port Forwarding

- Improperly configured port forwarding can unintentionally expose internal services to the public internet.
- Ensure that port forwarding rules are necessary and securely configured. Avoid unnecessary port forwarding, which can create vulnerabilities.
- Regularly review and update port forwarding configurations to ensure they reflect current needs and security standards.

### Identify the Process Associated with a Specific Port

In network management and security assessments, understanding which processes are binding to specific ports is crucial. For instance, you might need to verify that the intended service is running on its designated port or to diagnose port conflicts. The `lsof` (List Open Files) command, combined with certain flags, can help identify which process is using a specific port.

I. Using the `lsof` Command

Find Processes Using a Specific Port:

```bash
sudo lsof -i :<port-number>
```

For instance, to see which process is using port 80:

```bash
sudo lsof -i :80
```

This will return a list of processes bound to port 80. The output includes essential details like the process name, user running the process, the associated PID (Process ID), and more.

If you want a more concise output showing just the PID, process name, and the user running the process, use:

``` bash
sudo lsof -i :<port-number> -n -P | awk 'NR==1 || /LISTEN/ {print $2, $1, $3}'
```

Replace `<port-number>` with the desired port number. This version filters out the non-listening states and formats the output for clarity.

II. Using the netstat command

In systems where lsof might not be available, the netstat command, combined with grep, can also help in identifying processes associated with ports:

```bash
sudo netstat -tulnp | grep :<port-number>
```

Always be cautious about unexpected processes binding to known ports. Such anomalies could indicate misconfigurations or potential security threats, like backdoors or unauthorized services.

### Socket Status

In networking, a socket represents an endpoint for sending or receiving data. When a program wants to communicate over the Internet, it creates a socket. To monitor these sockets and the status of their connections, we can use the `ss` (socket status) tool, which is a utility to investigate sockets. This tool is especially helpful for understanding current network configurations, active/inactive connections, and diagnosing various network-related issues.

I. Display All Active Connections

```
ss -tuln
```

This command lists all UDP and TCP connections, without resolving hostnames (due to `-n`).

II. Display Only TCP Ports

```
ss -tln
```

This restricts the output to only TCP connections and avoids resolving hostnames.

III. Display Only UDP Ports
  
```
ss -uln
```

This shows just the UDP connections, also without resolving hostnames.

IV. Display Listening Sockets

```
ss -tuln state listening
```

This will display all listening TCP and UDP sockets.

V. Display Established Connections

```
ss -tuln state established
```

This focuses on showing only the established connections, helping you identify active data exchanges.

### Filtering the Output

`ss` can be combined with other command-line utilities for more specific results:

I. Count Active TCP Connections

```
ss -tan | grep ESTAB | wc -l
```

This sequence counts the number of established TCP connections.

II. List All SSH Connections

```
ss -tan state established '( dport = :22 or sport = :22 )'
```

If you're specifically interested in SSH connections, this command is handy.

### Nmap

Nmap, short for "Network Mapper," is a revered tool in the cybersecurity and network administration arenas. Its primary purpose is to scan IP networks for host discovery, port scanning, and service identification.

Key Features:

- **Host Discovery** allows users to find which hosts are available on a network, helping identify active devices.
- **Port Scanning** determines which ports are open on those hosts, providing insight into the services that are accessible.
- **Version Detection** helps detect the services and their versions running on open ports, enabling a deeper understanding of the network's software landscape.
- **OS Detection** allows for determining the operating system and its version on a host, which is crucial for security assessments and system management.

Common Scenarios:

- In **Security Audits**, network administrators use Nmap to identify open ports that could be potential security vulnerabilities, helping to strengthen the network's defenses.
- For **Network Inventory**, companies might utilize Nmap for regular checks, discovering devices on a network and cataloging the services they run, ensuring accurate asset management.
- **Network Troubleshooting** involves using Nmap to determine unreachable hosts, closed ports, or service disruptions, aiding in diagnosing and resolving network issues.
- During **Penetration Testing**, ethical hackers and penetration testers employ Nmap to gather intelligence about a target, providing crucial information that helps in crafting sophisticated attacks for security assessments.

Basic Commands:

I. Scan a Single Host

```
nmap <IP-address>
```

Replace `<IP-address>` with the IP of the host you wish to scan.

II. Scan Multiple Hosts

```
nmap <IP-address1,IP-address2,...>
```

Separate the IPs with commas for scanning multiple hosts.

III. Scan a Range of Hosts

```
nmap <IP-address-start>-<IP-address-end>
```

For instance, `nmap 192.168.1.1-20` would scan hosts from `192.168.1.1` through `192.168.1.20`.

IV. Scan a Subnet
   
```
nmap <IP-address/CIDR>
```

For instance, `nmap 192.168.1.0/24` would scan all 256 hosts in the `192.168.1.0` subnet.

V. Fast Scan

The `-F` flag makes Nmap scan fewer ports than the default, making the scan faster.

```
nmap -F <IP-address>
```

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
