<h1>Processes</h1>
We create "processes" when we interact with Linux. A new process is created every time you execute a command, open an application, or launch a system service. A process is just a numbered instance of a running program. Many processes can run concurrently on modern systems. The OS quickly swithces between various processes running on the CPU. Multicore CPU's can even execute many processes at the same time. On those machines each core quickly switches between various processes. 

There two types of processes:

1. shell job - A command written in the shell is used to launch the task. They are also known as interactive processes.
2. daemons - They are utility applications that run silently in the background to monitor and maintain particular subsystems to ensure the operating system's proper functionality. They are often launched with root privileges.

The <code>ps</code> command displays a list of all processes. To long listing of all processes on the system, use:

```bash
ps -ef 
```

Processes have many properties associated with them. To see the user ID, process ID, parent process ID, CPU usage, and command name of a process, use:

```bash
ps -e --format uid,pid,ppid,%cpu,cmd 
```

Another useful options include:

* <code>aux</code>: short summary of all active processes
* <code>fax</code>: shows the process hierarchy
* <code>o</code>: allows to specify the column names

<code>top</code> shows the sorted list of active processes:

```bash
top
```

<h1>Monitor RAM usage per process</h1>
RSS is an abbreviation for Resident Set Size, is used to indicate how much memory the process is currently using. Swap memory is not included. It contains the entire stack and heap memory. Memory from shared libraries is included as long as the pages from those libraries are physically present in memory. Because some of the memory is shared, other applications may use it, thus adding up all of the RSS numbers may result in more RAM than your machine actually has.

VSS is an abbreviation for Virtual Set Size is a memory size allocated to a process during its first execution. It comprises all memory that the process may access, including swapped out memory, allocated but not utilized memory, and memory from shared libraries. 

Let's say we have a process that:
* currently have a process that has 450K of its own binary, 800K of shared libraries loaded, and 120K of stack/heap allocation in memory,
* but initially it started with 600K reserved binaries, 2200K of shared libraries, and 150K of stack/heap allocations. 

a) RSS: 450K + 800K + 120K = 1370K

b) VSZ: 600K + 2200K + 150K = 2950K

To find out which 10 processes use most of RAM:

```bash
ps -e -o pid,vsz,comm= | sort -n -k 2 -r | head 10
```

<h1>Foreground and background jobs</h1>
Jobs can either be in the foreground or in the background. Thus far, we have run commands at the prompt and waited for them to complete. We call this running in the “foreground.”

You can use the “&” operator, to run programs in the “background” (this is especially useful when the program will take a long time to execute):

```bash
sleep 1000 &
```

This process should now be displayd in the list of processes running in the background:

```bash
jobs
```

To bring a background job to foreground, use <code>fg</code> and it's number from <code>jobs</code> output:

```bash
fg 1
```

To stop a process without killing it, use <code>Ctrl+Z</code> (this will also display in the output of <code>jobs</code>).
Use <code>bg</code> to make it run again (analogous to <code>fg</code>).

```bash
bg 1
```

Another useful shortcut is <code>Ctrl+C</code>, which is used to terminate a running process.
Note: background processes launched in the shell will continue to run when the shell is terminated.
  
<h1>Terminate processes</h1>
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
| <code>SIGHUP</code> | (1) | Hangup |
| <code>SIGINT</code> | (2) | Interruptanalogous toanalogous to from keyboard |
| <code>SIGKILL</code> | (9) | Kill signal |
| <code>SIGTERM</code> |  (15) | Termination signal |
| <code>SIGSTP</code> |  (20) | analogous to <code>Ctrl+Z</code> |
  
Properly killing processes:
1. Send a SIGINT.
2. Send a SIGTERM.
3. Send a SIGKILL.

<h2>pkill vs killall</h2>

Both <code>pkill</code> and <code>killall</code> offer distinct options. Killall provides an option to match processes based on their age, whereas pkill contains a flag to exclusively kill processes on a certain tty. Neither is superior. They simply specialize in different areas.

```bash
pkill -SIGTERM -f chromium
```

```bash
killall -15 chromium
```

<h1>Spawning processes</h1>

* PID 1 is assigned to the first process that is created when the system boots up.
* This process is known as <code>systemd</code> or <code>init</code> depending on which Linux distribution you are using.
* This process is the father of all other processes. 

<h1>Search for processes</h1>

<code>pgerp</code> allows to find process id when process name is known:

```bash
pgrep chromium
```

Look for a process that was launched by a certain user:

```bash
pgrep -u adam chromium
```

<h1>Challenges</h1>

1. What is the difference between <code>ps -e</code> and <code>ps -eu</code> commands?
