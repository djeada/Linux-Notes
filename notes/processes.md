## Processes

Processes form the backbone of any operation that takes place within a system. In simplest terms, a process is a numbered component of a running program. It is instantiated every time a user executes a command, launches an application, or initiates a system service. Modern systems, leveraging the potential of powerful processors, can run numerous processes simultaneously. This is achieved through rapid context switching performed by the operating system (OS) on the Central Processing Unit (CPU). In multicore CPUs, each core has the capability to run multiple processes concurrently via swift context switching.

There are essentially two categories of processes:

* **Shell Job**: A shell job refers to a task that is initiated through a command executed in the shell. These tasks are often referred to as interactive processes since they require direct user input.

* **Daemon**: Daemons are utility applications that silently run in the background, monitoring and maintaining certain subsystems to ensure the smooth operation of the OS. Daemons are typically initiated with root privileges and serve a crucial role in system management.

### Process Management Commands

To get an overview of all the currently running processes within your system, you can make use of the `ps` command:

```bash
ps -ef
```

If you require more comprehensive information about the processes, such as the User ID (UID), Process ID (PID), Parent Process ID (PPID), CPU usage, and the path to the executable, the following command can be used:

```bash
ps -e --format uid,pid,ppid,%cpu,cmd
```

In essence, understanding processes and how to manage them is key to gaining control over your system's operation and resources.

* `aux`: Provides a condensed summary of all active processes.
* `fax`: Displays the process hierarchy, revealing parent-child relationships between processes.
* `o`: Allows you to customize the output by specifying column names.

For real-time process monitoring and management, the top command can be employed. This command will display a dynamically updated, sorted list of active processes:

```bash
top
```

## Process life cycle

```
                        +---------+
                        |         |
                        | Created |
                        |         |
                        +----+----+
                             |
                             | Schedule
                             v
                        +----+----+
                        |         |
                        | Running |
               -------- |         | ----------
             /          +----+----+            \
           /  Error           |        Complete  \ 
          v                   |                   v
  +-------+-----+     +-------+-------+     +---------+
  |             |     |               |     |         |
  | Terminated  |<----| Interrupted   |<----|  Exit   |
  |             |     |               |     |         |
  +-------------+     +---------------+     +---------+
```

- `Created`: The process is created.
- `Running`: The process has been scheduled and is executing.
- `Interrupted`: The process is stopped or paused by the system, usually due to an interrupt from the system.
- `Exit`: The process finishes its execution.
- `Terminated`: The process is killed due to an error or an explicit kill command.

## Process Spawning

Process spawning is a fundamental aspect of any operating system. It's the action of creating a new process from an existing one. Whether it's running a command from a terminal or a process creating another, spawning processes is a routine operation in system workflows.

* The first process that initiates when a system boots up is assigned Process ID (PID) 1. 

* This initial process is known as `systemd` or `init`, based on the Linux distribution in use. 

* Being the first process, it acts as the parent to all subsequently spawned processes.

Spawning a process can be as straightforward as executing a command or running a program from the command line. For instance:

```bash
echo "Hello, world!"
```

This command creates a new process that executes the echo command, resulting in the specified text being printed on the terminal.

For more complex operations, you might need to spawn processes programmatically. In the C programming language, the fork and exec functions are frequently used for this purpose.

- fork creates a copy of the currently executing process, generating a new child process.

- exec replaces the current process with a new one.

Consider the following example:

```C
#include <stdio.h>
#include <unistd.h>

int main() {
  pid_t pid = fork();
  if (pid == 0) {
    // This is the child process
    exec("/bin/ls");
  } else {
    // This is the parent process
    printf("Child process ID: %d\n", pid);
  }
  return 0;
}
```

In this program, a new process is created using the fork function, which then gets replaced by the ls command via the exec function. The parent process simply prints the child process ID on the terminal.

There are several other methods to spawn processes in Linux. Functions like system, popen, or posix_spawn from the POSIX library also provide process spawning capabilities.

## Process Termination

To manage system resources effectively, it is sometimes necessary to terminate running processes. Depending on your needs, this can be accomplished in several ways.

### Terminating Processes by PID

Each process, upon its creation, is assigned a unique Process ID (PID). To stop a process using its PID, the `kill` command is used. For instance:

```bash
kill 12345
```
In this example, a termination signal is sent to the process with PID 12345, instructing it to stop execution.

### Terminating Processes by Name

If you don't know a process's PID, but you do know its name, the pkill command is handy. This command allows you to stop a process using its name:

```bash
pkill process_name
```

In this case, a termination signal is sent to all processes that share the specified name, effectively halting their execution.

### Specifying Termination Signals

The kill and pkill commands provide the option to specify the type of signal sent to a process. For example, to send a SIGINT signal (equivalent to Ctrl+C), you can use:

```bash
kill -SIGINT 12345
```

Linux supports a variety of signals, each designed for a specific purpose. Some common signals include:

| Signal | Value |  Description |
| --- | --- | --- |
| `SIGHUP` | (1) | Hangup detected on controlling terminal or death of controlling process |
| `SIGINT` | (2) | Interrupt from keyboard; typically, caused by  `Ctrl+C` |
| `SIGKILL` | (9) | Forces immediate process termination; it cannot be ignored, blocked or caught |
| `SIGSTOP` |  (19) | Pauses the process; cannot be ignored |
| `SIGCONT` |  (18) | Resumes paused process |

Terminating processes should be performed with caution. Some processes may be critical for system operation or hold valuable data that could be lost upon abrupt termination. Therefore, it's advisable to use commands such as ps and top to observe currently running processes before attempting to stop any of them. This approach allows for more controlled and careful system management, preventing unintended disruptions or data loss.

## Methods for Searching Processes

In a Linux environment, various methods are available to search for processes, depending on the granularity of information you require or your personal preference. The search can be done using commands such as `ps`, `grep`, `pgrep`, and `htop`.

### Searching Processes with `ps` and `grep`

The `ps` command displays a list of currently running processes. To search for processes by name, you can combine `ps` with the `grep` command. The following command:

```bash
ps -ef | grep process_name
```

searches and displays all processes containing the specified name (process_name in this example). Here, ps -ef lists all processes, and grep process_name filters the list to show only the processes with the specified name.

### Searching Processes with pgrep

The pgrep command offers a quick and direct method to search for processes by their names and display their PIDs. For instance, to find all running processes named chromium, you would use:

```bash
pgrep chromium
```

This command displays the PIDs for all instances of chromium currently running on the system.

### Searching Processes with htop

htop provides a real-time, interactive view of all running processes in a system. It's a robust tool for process management, offering capabilities like process searching, sorting, and termination.

To search for processes in htop:

1. Launch htop by typing htop in the terminal.

```bash
htop
```

2. Once htop is open, press F4 to activate the search bar.

3. Type the name of the process or the user you're searching for, then press Enter.

4. The list of processes will update to show only those matching your search criteria.

## Foreground and Background Jobs

The tasks running on your system can be in one of two states, either running in the 'foreground' or in the 'background'. These two states provide flexibility for multi-tasking and efficient system utilization.

**Foreground Process**: A process is said to be running in the foreground if it is actively executing and interacting with the terminal's input and output. These are generally the tasks that you've initiated and are currently interacting with in your terminal.

**Background Process**: On the contrary, a background process operates without directly interacting with the terminal's input and output. This ability allows you to run multiple processes simultaneously, without having to wait for each one to complete before starting another.

```
+------------------------+
|                        |
| Start Job in Foreground|
|                        |
+-----------+------------+
            |
            | Ctrl+Z or bg
            v
+-----------+------------+
|                        |
|   Job Running in       |
|   Background           |
|                        |
+-----------+------------+
            |
            | fg or job completes
            v
+-----------+------------+
|                        |
|   Job Completes        |
|   or Returns to        |
|   Foreground           |
|                        |
+------------------------+
```

### Controlling Job Execution

You can direct a program to run in the background right from its initiation by appending an ampersand `&` operator after the command. Consider the following example:

```bash
sleep 1000 &
```

Here, the sleep command will operate in the background, waiting for 1000 seconds before terminating. The output typically resembles this:

```bash
[1] 3241
```

The number enclosed in square brackets (like `[1]`) represents the job number, while the subsequent number (like 3241) is the process ID (PID).

### Job and Process Management Commands

To view all active jobs in the system, use the `jobs` command.

If you wish to bring a background job to the foreground, utilize the fg command followed by the job number. For instance, to bring job number 3 to the foreground, you would use:

```bash
fg 3
```

To convert a foreground process to a background process, you can use Ctrl+Z. This operation pauses the process and allows you to resume it in the background using the bg command followed by the job number. For instance:

```bash
bg 1
```

This command will resume job number 1 in the background. Understanding and managing foreground and background jobs helps to increase productivity and efficiency when working in a shell environment.

## Challenges

1. Find the process ID (PID) of a specific process by its name.
2. List all processes that belong to a specific user.
3. Start a process in the background, bring it to the foreground, and then move it back to the background.
4. Terminate a process using both its PID and its name.
5. Write a simple C program that spawns a child process to execute a command.
6. Use the `top` command to identify the process with the highest CPU usage and terminate it.
7. Pause a running process using the appropriate signal and then resume it.
8. Find the parent process ID (PPID) of a specific process.
9. Explain the difference between a shell job and a daemon process.
10. Use the `htop` command to filter processes by a specific string and then sort them by memory usage.
