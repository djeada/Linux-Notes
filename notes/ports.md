<h1>What are ports?</h1>

Whenever you want physically travel from one place to another you need a road.  Similarly, data is transferred between devices over specific roads known as ports. There are precisely 65535 roads for every pair of connected devices (such as computers, printers, and cameras). Each one is a two-way street (data can flow in both directions). In theory, all of them may be used at the same time. You may send and recive data simultaneously on as many ports as you wish.

Furthermore, there are two methods for transfering data via the ports. One is known as TCP and is fast and dangerous, while the other is known as UDP and is slow and safe. You can imagine each road as having two lanes stacked on top of each other (actually, it's just one lane, but it's simpler to imagine it this way). 

Internet-based services (such as web browsers, web pages, and file transfer services) rely on certain ports to transmit data. If you wish to visit a website, you most likely use the HTTP protocol. The data travels on the lane 80. When you open YouTube, you send a request to your router on lane 80, which passes it to the servers. The response comes on lane 80 as well, first from the servers to the router and then from the router to your PC. 

Ports can be opened and closed. An open port is one that has been set to accept packets. A closed port, on the other hand, is one that rejects all connections. As the server administrator, you must know which ports are open on your servers since each open port is a potential target for hacker attacks. Closing unused ports minimizes the number of possible attacks.

<h1>Socket status</h1>

Socket status is a newer tool replacing older <i>netstat</i>.

To display open ports, use:

```bash
ss -tan
```

Use the following command to display tcp ports:

```bash
ss -at
```

Use the following command to display all ports (UDP and TCP):

```bash
ss -tul
```

<h1>Nmap</h1>

<i>nmap</i> is probing 1,000 or more ports to see whether they are open.
It's typically used to scan remote machines, however scanning your server may also be quite useful for checking your own configuration. 

To check your own machine with <i>nmap</i>, use:

```bash
nmap localhost
```

Every open port presents a vulnerability. To defend yourself from attacks, use a firewall. 

<h1>Find the process knowing its port</h1>

Sometimes you have a process whose PID you don't know and which you want to kill.

You may use top to identify the name of your process and kill it with kill -9. However, if you don't know it's name, this isn't helpful. A better method is to look for it by the port it's using:

```bash
sudo lsof -i :80
```

The PID of the process will be displayed in the second column.

<h1>Challenges</h1>

1. Some ports are reserved  for specific services. Is this to say they can't be used for anything else?
2. How to check which port numbers are free to use?
3. How to find which process is running on a specific port?
4. How to find which port is used by a given service?
