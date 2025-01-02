## Processes

Processes are fundamental elements in any computing system. They represent an instance of a running program and are essential for the execution of various tasks. A process is more than just the program code (often referred to as the text section in Unix); it also includes the current activity, including the program counter, the contents of the processor's registers, and the variable storage (stack and heap). Each process is assigned a unique process identifier (PID).

When a user executes a command, launches an application, or initiates a system service, a new process is instantiated. Modern computing systems, with their powerful processors, can handle a multitude of processes at the same time. This parallel execution is managed through a technique known as rapid context switching, where the operating system's scheduler assigns CPU time slices to each process and switches between them so quickly that it gives the illusion of simultaneous execution.

In the context of multicore CPUs, each core can handle its own set of processes independently. This multi-core processing enables even more efficient and faster handling of multiple processes.

Processes in a system can be broadly categorized into two types:

- A **Shell Job** refers to a process started from a user's command line interface or shell. It is typically interactive, requiring user input and providing output directly to the user's console. Examples of shell jobs include editing a document in a text editor or running a custom script.
- In contrast, a **Daemon** is a background process that usually starts at system boot and runs with elevated privileges. Daemons do not interact directly with the user interface; instead, they operate silently in the background, handling various system-related tasks. Common examples include the print spooler daemon, which manages print jobs, and the network daemon, which handles network connections.

### Process Management Commands

Process management is integral to system administration. The `ps` and `top` commands are pivotal for this purpose.

#### The `ps` Command

The `ps` command displays information about active processes. Here are some variants of the command:

I. Basic Process Listing

```bash
ps -ef
```

This outputs a list of all currently running processes, showing the process ID (PID), terminal associated with the process (TTY), CPU time (TIME), and the executable name (CMD).

Sample Output:

```
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 03:15 ?        00:00:01 /sbin/init
...
```

II. Detailed Process Information

```
ps -e --format uid,pid,ppid,%cpu,cmd
```

This provides detailed information including User ID (UID), Process ID (PID), Parent Process ID (PPID), CPU usage (%CPU), and the command path (CMD).

Sample Output:

```
UID     PID  PPID %CPU CMD
1000   2176  2145  0.0 /usr/bin/bash
...
```

III. Enhanced Process Summaries

One option:

```
ps aux
```

This gives a condensed summary of all active processes, including details like user, PID, CPU, and memory usage.

Sample Output:

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 169560  5892 ?        Ss   Apr10   0:01 /sbin/init
...
```

Another option:

```
ps fax
```

This displays the process hierarchy in a tree structure, showing parent-child relationships.

Sample Output:

```
PID TTY      STAT   TIME COMMAND
  2 ?        S      0:00 [kthreadd]
/-+- 3951 ?        S      0:07  \_ [kworker/u8:2]
...
```

```
ps -o
```

Customizes the output by specifying column names, tailored for specific requirements.

#### The `top` Command

For real-time process monitoring, top is used:

```
top
```

This shows a dynamic list of processes, usually sorted by CPU usage. It includes system summary information (like CPU and memory usage) and a detailed list of processes.

Sample Output:

```
top - 03:16:10 up 1 day,  6:37,  2 users,  load average: 1.20, 0.45, 0.15
Tasks: 287 total,   1 running, 286 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.0 us,  0.5 sy,  0.0 ni, 97.4 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
KiB Mem : 16316412 total,  3943404 free,  8450008 used,  3923016 buff/cache
KiB Swap:  8388604 total,  8388604 free,        0 used. 11585756 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND   
 1297 root      20   0  457472  56080  36924 S   5.6  0.3   0:03.89 Xorg     
...
```

### Process life cycle

The life cycle of a process in an operating system is a critical concept. The provided diagram illustrates the various stages a process goes through:

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

- When a process is **Created**, it enters the system and is allocated the necessary resources, but it has not yet started running.
- In the **Running** state, the process is actively executing instructions on the CPU.
- A process can be **Interrupted**, meaning it is temporarily stopped. This may occur to allow other processes to run or because the process is waiting for an input or an event.
- The **Exit** state indicates that the process has completed its execution and is ready to be removed from the system.
- If a process is **Terminated**, it means that an error occurred or an explicit kill command was issued, resulting in the process being forcefully stopped.

### Process Spawning

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

- `fork()` creates a copy of the currently executing process, generating a new child process.
- `exec()` replaces the current process with a new one.

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

In this program, a new process is created using the fork function, which then gets replaced by the `ls` command via the exec function. The parent process simply prints the child process ID on the terminal.

There are several other methods to spawn processes in Linux. Functions like `system`, `popen`, or `posix_spawn` from the POSIX library also provide process spawning capabilities.

### Process Termination

To manage system resources effectively, it is sometimes necessary to terminate running processes. Depending on your needs, this can be accomplished in several ways.

#### Terminating Processes by PID

Each process, upon its creation, is assigned a unique Process ID (PID). To stop a process using its PID, the `kill` command is used. For instance:

```bash
kill 12345
```

In this example, a termination signal is sent to the process with PID 12345, instructing it to stop execution.

#### Terminating Processes by Name

If you don't know a process's PID, but you do know its name, the `pkill` command is handy. This command allows you to stop a process using its name:

```bash
pkill process_name
```

In this case, a termination signal is sent to all processes that share the specified name, effectively halting their execution.

#### Specifying Termination Signals

The `kill` and `pkill` commands provide the option to specify the type of signal sent to a process. For example, to send a SIGINT signal (equivalent to Ctrl+C), you can use:

```bash
kill -SIGINT 12345
```

Linux supports a variety of signals, each designed for a specific purpose. Some common signals include:

| Signal | Value | Description |
| --- | --- | --- |
| `SIGHUP` | (1) | Hangup detected on controlling terminal or death of controlling process |
| `SIGINT` | (2) | Interrupt from keyboard; typically, caused by `Ctrl+C` |
| `SIGKILL` | (9) | Forces immediate process termination; it cannot be ignored, blocked, or caught |
| `SIGSTOP` | (19) | Pauses the process; cannot be ignored |
| `SIGCONT` | (18) | Resumes paused process |

Terminating processes should be performed with caution. Some processes may be critical for system operation or hold valuable data that could be lost upon abrupt termination. Therefore, it's advisable to use commands such as `ps` and `top` to observe currently running processes before attempting to stop any of them. This approach allows for more controlled and careful system management, preventing unintended disruptions or data loss.

#### Special PID Values in `kill`

When using the `kill` command, special PID values can be used to target multiple processes:

- Using **`-1`** as a signal target sends the signal to all processes that the user has permission to signal, excluding the process itself and process ID 1 (the init process).
- The **`0`** target sends the signal to all processes in the same process group as the calling process, allowing for group-wide signaling.
- When **negative values less than -1** are used, the signal is sent to all processes in the process group corresponding to the absolute value of the given number. For example, executing `kill -2 -SIGTERM` sends the SIGTERM signal to all processes in the process group with PGID 2.

These special values allow for more flexible management of processes and process groups, especially in scenarios where you need to signal multiple related processes at once. Here are examples of using these special values:

```bash
# Sending SIGTERM to all processes the user can signal
kill -1 -SIGTERM

# Sending SIGTERM to all processes in the same process group as the current process
kill 0 -SIGTERM

# Sending SIGTERM to all processes in the process group with PGID 2
kill -2 -SIGTERM
```

Using these special values carefully can help manage and control process groups effectively.

### Methods for Searching Processes

In a Linux environment, various methods are available to search for processes, depending on the granularity of information you require or your personal preference. The search can be done using commands such as `ps`, `grep`, `pgrep`, and `htop`.

#### Searching Processes with `ps` and `grep`

The `ps` command displays a list of currently running processes. To search for processes by name, you can combine `ps` with the `grep` command. The following command:

```bash
ps -ef | grep process_name
```

searches and displays all processes containing the specified name (process_name in this example). Here, ps -ef lists all processes, and grep process_name filters the list to show only the processes with the specified name.

#### Searching Processes with pgrep

The pgrep command offers a quick and direct method to search for processes by their names and display their PIDs. For instance, to find all running processes named chromium, you would use:

```bash
pgrep chromium
```

This command displays the PIDs for all instances of chromium currently running on the system.

#### Searching Processes with htop

htop provides a real-time, interactive view of all running processes in a system. It's a robust tool for process management, offering capabilities like process searching, sorting, and termination.

To search for processes in htop:

1. Launch htop by typing `htop` in the terminal.
2. Once htop is open, press `F4` to activate the search bar.
3. Type the name of the process or the user you're searching for, then press Enter.
4. The list of processes will update to show only those matching your search criteria.

### Foreground and Background Jobs

The tasks running on your system can be in one of two states, either running in the 'foreground' or in the 'background'. These two states provide flexibility for multi-tasking and efficient system utilization.

- When a process is running as a **Foreground Process**, it actively executes and interacts with the terminal's input and output. These are typically tasks that the user has initiated and is directly interacting with in the terminal.
- In contrast, a **Background Process** operates without direct interaction with the terminal's input and output. This functionality enables users to run multiple processes at the same time, allowing them to initiate new tasks without waiting for the completion of others.

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

#### Controlling Job Execution

You can direct a program to run in the background right from its initiation by appending an ampersand `&` operator after the command. Consider the following example:

```bash
sleep 1000 &
```

Here, the sleep command will operate in the background, waiting for 1000 seconds before terminating. The output typically resembles this:

```bash
[1] 3241
```

The number enclosed in square brackets (like `[1]`) represents the job number, while the subsequent number (like 3241) is the process ID (PID).

#### Job and Process Management Commands

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

### Challenges

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
