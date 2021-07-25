We create "processes" when we interact with Linux. A process is just a numbered instances of running program. The ps command displays a list of all processes.

```bash
# long listing of all processes on the system
ps -ef 

# the user ID, process ID, parent process ID, CPU usage, and command name of a process
ps -e --format uid,pid,ppid,%cpu,cmd 
```

* top shows the sorted list of active processes

<h2>Foreground/background</h2>
  
  Thus far, we have run commands at the prompt and waited for them
to complete. We call this running in the “foreground.”
● Use the “&” operator, to run programs in the “background”, 

To kill the job, use the ‘kill’ command, either with the five-digit process id:

```bash
kill 54356 
```
