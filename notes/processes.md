<h1>Processes</h1>
We create "processes" when we interact with Linux. A process is just a numbered instance of a running program.  Many processes can run concurrently on modern systems. The OS quickly swithces between various processes running on the CPU. Multicore CPU's can acutually execute many processes at the same time. Each core quickly switches between various processes. 

There two types of processes:

1. shell job - A command written in the shell is used to launch the task. They are also known as interactive processes.
2. daemons - They are utility applications that run silently in the background to monitor and maintain particular subsystems to ensure the operating system's proper functionality. They are often launched with root privileges.

The <i>ps</i> command displays a list of all processes. To long listing of all processes on the system, use:

```bash
ps -ef 
```

To see the user ID, process ID, parent process ID, CPU usage, and command name of a process, use:

```bash
ps -e --format uid,pid,ppid,%cpu,cmd 
```

Another useful options include:

* <i>aux</i>: short summary of all active processes
* <i>fax</i>: shows the process hierarchy
* <i>o</i>: allows to specify the column names

<i>top</i> shows the sorted list of active processes:

```bash
top
```

<h2>Foreground and background</h2>

Jobs can either be in the foreground or the background. Thus far, we have run commands at the prompt and waited for them to complete. We call this running in the “foreground.”

Use the “&” operator, to run programs in the “background” (this is especially useful when the program will take a long time to execute):

```bash
sleep 1000 &
```

This process should now be displayd in the list of processes running in the background:

```bash
jobs
```

To bring a background program to foreground, use <i>fg</i> and it's number from <i>jobs</i> output:

```bash
fg 1
```

To stop a process without killing it, use <i>Ctrl+Z</i> (this will also display in the output of <i>jobs</i>).
Use <i>bg</i> to make it run again (analogous to <i>fg</i>).

```bash
bg 1
```

Another useful shortcut is <i>Ctrl+C</i>, which is used to terminate a running process.
Note: background processes launched in the shell will continue to run when the shell is terminated.
  
<h2>Terminate processes</h2>

To kill a process, use the ‘kill’ command with the five-digit process id:

```bash
kill 54356
```

Use a -9 option to cause a process to end suddenly (and with a greater likelihood of success):

```bash
kill -9 54356
```

Available signals:

| Signal | Value |  Description |
| --- | --- | --- |
| SIGHUP | (1) | Hangup |
| SIGINT | (2) | Interruptanalogous toanalogous to from keyboard |
| SIGKILL | (9) | Kill signal |
| SIGTERM |  (15) | Termination signal |
| SIGSTP |  (20) | analogous to <i>Ctrl+Z</i> |
  
Properly killing processes:
1. Send a SIGINT.
2. Send a SIGTERM.
3. Send a SIGKILL.

<h2>pgrep</h2>

<i>pgerp</i> allows to find process id when process name is known:

```bash
pgrep chromium
```

Look for a process that was launched by a certain user:

```bash
pgrep -u adam chromium
```

<h2>pkill vs killall</h2>

Both pkill and killall offer distinct options. Killall provides an option to match processes based on their age, whereas pkill contains a flag to exclusively kill processes on a certain tty. Neither is superior. They simply specialize in different areas.

```bash
pkill -SIGTERM -f chromium
```

```bash
killall -15 chromium
```
