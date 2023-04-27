## What are ports?

Ports are ways for computers and devices to exchange data. There are 65535 communication channels, called ports, that can be used at the same time for different data transfers. There are two main ways to transfer data over ports: TCP (Transmission Control Protocol) and UDP (User Datagram Protocol).

- Some examples of services using specific ports:
  - Visiting a website uses the HTTP protocol on port 80.
  - Watching a video on YouTube uses port 80 for communication.

- Open and closed ports:
  - Open ports accept incoming connections.
  - Closed ports reject all connections.
  - Closing unused ports can help protect against hacker attacks.

## Socket status

Socket status is a tool to view open ports on a system. Here's how to use it:

- Display all open ports: `ss -tan`
- Display only TCP ports: `ss -at`
- Display both UDP and TCP ports: `ss -tul`

## Nmap

Nmap is a tool to scan for open ports on a system. Use it like this:

- Scan your own system: `nmap localhost`

## Find the process associated with a specific port

To find the process ID (PID) of a process using a specific port, use:

```
sudo lsof -i :80
```

This will display a list of processes using port 80, and the PID of each process will be shown in the second column.

## Challenges

1. Some ports are reserved for specific services. Can they be used for other purposes?
2. How can you check which port numbers are available to use?
3. How can you find out which process is running on a specific port?
4. How can you find out which port is used by a given service?
5. What is the main reason for using ports in networking?
6. How many ports are available in total, and how do they work?
7. What is the difference between TCP and UDP ports?
8. How can you see open ports on a server?
9. What is Nmap, and how is it used?
10. How can you find the process associated with a specific port?
11. What is a firewall, and why is it important for protecting ports?

