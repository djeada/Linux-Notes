We create "processes" when we interact with Linux. A process is just a numbered instances of running program. The ps command displays a list of all processes.

```bash
ps -ef # long listing of all processes on the system
ps -e --format uid,pid,ppid,%cpu,cmd #the user ID, process ID, parent process ID, CPU usage, and command name of a process
```


