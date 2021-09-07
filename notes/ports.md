The ports can be closed or open.

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
