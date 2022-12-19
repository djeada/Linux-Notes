## What are ports?

Ports are communication channels used by computers and other devices to exchange data. When two devices are connected, they have access to 65535 two-way communication channels, or ports. These ports allow data to flow in both directions between the devices. In theory, all of the ports can be used at the same time, allowing for multiple simultaneous data transfers.

There are two main protocols for transferring data over ports: TCP (Transmission Control Protocol) and UDP (User Datagram Protocol). TCP is a fast and reliable protocol, but it can also be vulnerable to attacks. UDP is a slower but more secure protocol.

Internet-based services, such as web browsers, web pages, and file transfer services, rely on specific ports to transmit data. For example, when you visit a website, you are using the HTTP protocol, which typically uses port 80. When you open YouTube, you send a request to your router on port 80, which passes it on to the servers. The response then comes back on port 80, first from the servers to the router and then from the router to your device.

Ports can be opened or closed. An open port is one that is set to accept incoming connections, while a closed port is one that rejects all connections. It is important for server administrators to know which ports are open on their servers, as each open port presents a potential vulnerability to hacker attacks. Closing unused ports can help minimize the number of possible attacks.

## Socket status

Socket status is a tool that can be used to view open ports on a system. To display all open ports, use the following command:

```
ss -tan
```

To display only TCP ports, use:

```
ss -at
```

To display both UDP and TCP ports, use:

```
ss -tul
```

## Nmap

Nmap (Network Mapper) is a tool used to scan a system for open ports. It can be used to probe over 1000 ports to determine which ones are open. It is commonly used to scan remote systems, but it can also be useful for scanning your own system to check your configuration. To scan your own system with Nmap, use the following command:

```
nmap localhost
```

Every open port presents a vulnerability, so it is important to use a firewall to protect against attacks.
Finding the process associated with a specific port

Sometimes you may need to find the process ID (PID) of a process that you want to stop, but you don't know its name. One way to do this is to search for the process by the port it is using. To do this, use the following command:

```
sudo lsof -i :80
```

This will display a list of processes using port 80, and the PID of each process will be shown in the second column.

## Challenges

1. Some ports are reserved  for specific services. Is this to say they can't be used for anything else?
1. How to check which port numbers are free to use?
1. How to find which process is running on a specific port?
1. How to find which port is used by a given service?
1. What is the purpose of ports in networking?
1. How many ports are there in total and how do they work?
1. What is the difference between TCP and UDP ports?
1. How can you view open ports on a server?
1. What is nmap and how is it used?
1. How can you find the process associated with a specific port?
1. What is a firewall and why is it important in regards to ports?
