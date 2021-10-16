<h1>What are ports?</h1>
If you use ssh with the default settings to connect to your server, you are utilizing TCP/IP port 22. The ports can be opened or closed. As a person responsible for your server, you must identify which ports are open on your servers since each open port is a possible target for hacker attacks.

<h1>socket status</h1>

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

<h2>How can I find a process's PID if I know its port?</h2>

Sometimes you have a process whose PID you don't know and which you want to kill.

You may use top to identify the name of your process and kill it with kill -9. However, if you don't know it's name, this isn't helpful. A better method is to look for it by the port it's using:

```bash
sudo lsof -i :80
```

The PID of the process will be displayed in the second column.

<h1>nmap</h1>

<i>nmap</i> is probing 1,000 or more ports to see whether they are open.
It's typically used to scan remote machines, however scanning your server may also be quite useful for checking your own configuration. 

To check your own machine with <i>nmap</i>, use:

```bash
nmap localhost
```

Every open port presents a vulnerability. To defend yourself from attacks, use a firewall. 
