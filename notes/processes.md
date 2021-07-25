<h2>Processes</h2>
We create "processes" when we interact with Linux. A process is just a numbered instance of a running program. The <i>ps</i> command displays a list of all processes.

To long listing of all processes on the system, use:

```bash
ps -ef 
```

To see the user ID, process ID, parent process ID, CPU usage, and command name of a process, use:

```bash
ps -e --format uid,pid,ppid,%cpu,cmd 
```

* top shows the sorted list of active processes

<h2>Foreground and background</h2>

Jobs can either be in the foreground or the background. Thus far, we have run commands at the prompt and waited for them to complete. We call this running in the “foreground.”

Use the “&” operator, to run programs in the “background”:

```bash
chromium &
```

Now you can see which processes are running in the background:

```bash
jobs
```

To bring a background program to foreground, use:

```bash
fg 1
```

<h2>Terminate processes</h2>

To kill a process, use the ‘kill’ command with the five-digit process id:

```bash
kill 54356
```

Use a -9 option to cause a process to end suddenly (and with a greater likelihood of success):

```bash
kill -9 54356
```
