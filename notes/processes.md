## Processes

In Linux, we create "processes" whenever we interact with the system. A process is a numbered instance of a running program, and it is created every time we execute a command, open an application, or launch a system service. Modern systems can run many processes concurrently, with the operating system (OS) quickly switching between them on the CPU. On multicore CPUs, each core can execute multiple processes at the same time by quickly switching between them.

There are two types of processes:

* `Shell job`: A task that is launched using a command written in the shell. These are also known as interactive processes.
* `Daemon`: Utility applications that run silently in the background to monitor and maintain particular subsystems to ensure the operating system's proper functionality. These processes are often launched with root privileges.

To view a list of all processes on the system, use the ps command:

```
ps -ef
```

To see more detailed information about processes, such as the user ID, process ID, parent process ID, CPU usage, and the path to the executable, use the following command:

```bash
ps -e --format uid,pid,ppid,%cpu,cmd
```

Other useful options for the ps command include:

* `aux`: A short summary of all active processes
* `fax`: Displays the process hierarchy
* `o`: Allows you to specify the column names

To see a sorted list of active processes, use the top command:

```bash
top
```

## Foreground and background jobs
When a process is running in the foreground, it means that it is currently being executed and is occupying the terminal's input and output. When a process is running in the background, it means that it is being executed in the background and does not occupy the terminal's input and output. This allows you to run multiple processes at the same time without having to wait for each one to complete before starting the next.

To run a program in the background, use the & operator after the command. For example:

```bash
sleep 1000 &
```

This will run the sleep command in the background, causing it to wait for 1000 seconds before closing. The output will typically look something like this:

```bash
[1] 3241
```

The number in square brackets (e.g. `[1]`) represents the job number, while the second number (e.g. 3241) represents the process ID.

To view all jobs on the system, use the jobs command.

To bring a background job to the foreground, use the `fg` command followed by the job number. For example, to bring job number 3 to the foreground, use:

```bash
fg 3
```

To move a process that is currently running in the terminal to the background, use `Ctrl+Z`. This will stop the process, but it can be resumed in the background using the `bg` command followed by the job number. For example:

```bash
bg 1
```

## Terminate processes
To kill a process using its process ID, use the kill command followed by the process ID. The process ID is a five-digit number that is assigned to each process when it is created. For example:

```
kill 12345
```

This will send a termination signal to the process with the specified process ID, causing it to terminate.

To kill a process using its name, use the `pkill` command followed by the process name. For example:

```
pkill process_name
```

This will send a termination signal to all processes with the specified name, causing them to terminate.

It is also possible to specify a signal to send to the process when using the `kill` or `pkill` commands. For example, to send the `SIGINT` signal (which is the same as pressing `Ctrl+C`) to a process, use:

```
kill -SIGINT 12345
```

There are many different signals that can be sent to processes, each with a specific purpose. Some common signals include:
    
| Signal | Value |  Description |
| --- | --- | --- |
| `SIGHUP` | (1) | Hangup |
| `SIGINT` | (2) | Terminates the process, similar to pressing `Ctrl+C` |
| `SIGKILL` | (9) | Terminates the process immediately, regardless of any cleanup it may need to do |
| `SIGSTOP` |  (19) | Stops the process and prevents it from running again until it is explicitly resumed |
| `SIGCONT` |  (18) | Resumes a stopped process |

It is important to be cautious when terminating processes, as some processes may be critical to the operation of the system or may have important data that could be lost if they are terminated unexpectedly. It is a good idea to use the ps and top commands to identify the processes that are running on the system before attempting to terminate any of them.

## Spawning processes

* PID 1 is assigned to the first process that is created when the system boots up.
* This process is known as `systemd` or `init` depending on which Linux distribution you are using.
* This process is the father of all other processes. 

Spawning a process refers to the creation of a new process. Processes are created when a program is executed, whether from the command line or by another process.

There are several ways to spawn a process. One way is to simply execute a command or run a program from the command line. For example:

```
echo "Hello, world!"
```

This will create a new process that runs the echo command, which prints the specified text to the terminal.

Another way to spawn a process is to use the `fork` and `exec` functions in a C program. The `fork` function creates a copy of the current process, while the `exec` function replaces the current process with a new one. For example:

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

This program creates a new process using the `fork` function, and then replaces the child process with the `ls` command using the exec function. The parent process simply prints the child process ID to the terminal.

There are many other ways to spawn processes in Linux, such as using the system function, `popen`, or `spawn` from the `posix_spawn` library.

It is important to be mindful of the number of processes being spawned, as creating too many processes can strain the system's resources and lead to performance issues. It is a good idea to use caution when spawning processes and to ensure that they are properly managed and terminated when they are no longer needed.

## Searching for processes

There are several ways to search for processes in Linux. The most common way is to use the `ps` command, which displays a list of currently running processes. To search for processes based on their name, use the `ps` command in combination with `grep`. For example:

```
ps -ef | grep process_name
```

This will display a list of all processes with the specified name.

Another way to search for processes is to use the `pgrep` command, which searches for processes by name and displays their process IDs. For example (to look for chromium):

```
pgrep chromium
```

This will display the process IDs of all processes with the specified name (chromium in our case).

It is also possible to search for processes using system tools such as `top` or `htop`, which display real-time information about processes on the system. These tools allow you to sort and filter the list of processes based on various criteria, such as CPU usage or memory usage.

## Challenges

1. How to find the status of a process?
1. What is the difference between `ps -e` and `ps -eu` commands?
1. Launch the *sleep* command three times in the background. Then bring it to the foreground and terminate it.
1. What is the difference between a shell job and a daemon process?
1. How can you view a list of all processes on the system?
1. How can you run a program in the background?
1. How can you move a process that is currently running in the terminal to the background?
1. How can you terminate a running process?
1. How can you search for processes by name?
