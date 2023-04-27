## Processes

In Linux, we make "processes" when we work with the system. A process is a numbered part of a running program, and it is made every time we do a command, open an app, or start a system service. Modern systems can run many processes at the same time, with the operating system (OS) quickly changing between them on the CPU. On multicore CPUs, each core can run multiple processes at the same time by quickly changing between them.

There are two types of processes:

* `Shell job`: A task that starts using a command written in the shell. These are also known as interactive processes.
* `Daemon`: Utility apps that run quietly in the background to watch and maintain certain subsystems to make sure the operating system works properly. These processes are often started with root privileges.

To see a list of all processes on the system, use the ps command:

```
ps -ef
```

To see more detailed information about processes, such as the user ID, process ID, parent process ID, CPU usage, and the path to the executable, use the following command:

```bash
ps -e --format uid,pid,ppid,%cpu,cmd
```

Other useful options for the ps command include:

* `aux`: A short summary of all active processes.
* `fax`: Shows the process hierarchy.
* `o`: Lets you choose the column names.

To see a sorted list of active processes, use the top command:

```bash
top
```

## Foreground and background jobs
When a process is running in the foreground, it means that it is currently being run and is using the terminal's input and output. When a process is running in the background, it means that it is being run in the background and doesn't use the terminal's input and output. This lets you run multiple processes at the same time without waiting for each one to finish before starting the next.

To run a program in the background, use the & operator after the command. For example:

```bash
sleep 1000 &
```

This will run the sleep command in the background, making it wait for 1000 seconds before closing. The output will usually look something like this:

```bash
[1] 3241
```

The number in square brackets (like `[1]`) is the job number, while the second number (like 3241) is the process ID.

To see all jobs on the system, use the jobs command.

To bring a background job to the foreground, use the `fg` command with the job number. For example, to bring job number 3 to the foreground, use:

```bash
fg 3
```

To move a process that is currently running in the terminal to the background, use `Ctrl+Z`. This will stop the process, but it can be started again in the background using the `bg` command with the job number. For example:

```bash
bg 1
```

## Terminate processes
To stop a process using its process ID, use the kill command with the process ID. The process ID is a five-digit number that is given to each process when it is made. For example:

```
kill 12345
```

This will send a termination signal to the process with the specified process ID, making it stop.

To stop a process using its name, use the `pkill` command with the process name. For example:

```
pkill process_name
```

This will send a termination signal to all processes with the specified name, making them stop.

It is also possible to choose a signal to send to the process when using the `kill` or `pkill` commands. For example, to send the `SIGINT` signal (which is the same as pressing `Ctrl+C`) to a process, use:

```
kill -SIGINT 12345
```

There are many different signals that can be sent to processes, each with a specific purpose. Some common signals include:

| Signal | Value |  Description |
| --- | --- | --- |
| `SIGHUP` | (1) | Hangup |
| `SIGINT` | (2) | Stops the process, similar to pressing  `Ctrl+C` |
| `SIGKILL` | (9) | Stops the process right away, no matter what cleanup it needs to do |
| `SIGSTOP` |  (19) | Stops the process and doesn't let it run again until it is told to continue |
| `SIGCONT` |  (18) | Starts a stopped process again |

It is important to be careful when stopping processes, as some processes may be very important for the system to work or may have important data that could be lost if they are stopped unexpectedly. It is a good idea to use the ps and top commands to see the processes that are running on the system before trying to stop any of them.

## Spawning processes

* PID 1 is given to the first process that is made when the system starts up.
* This process is known as `systemd` or `init` depending on which Linux distribution you are using.
* This process is the father of all other processes.

Spawning a process means making a new process. Processes are made when a program is run, either from the command line or by another process.

There are several ways to spawn a process. One way is to simply do a command or run a program from the command line. For example:

```
echo "Hello, world!"
```

This will create a new process that runs the `echo` command, which shows the specified text on the terminal.

Another way to spawn a process is to use the `fork` and `exec` functions in a C program. The `fork` function makes a copy of the current process, while the `exec` function replaces the current process with a new one. For example:

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

This program makes a new process using the fork function, and then replaces the child process with the ls command using the exec function. The parent process just shows the child process ID on the terminal.

There are many other ways to spawn processes in Linux, like using the system function, `popen`, or `spawn` from the `posix_spawn` library.

It is important to be careful about how many processes are being made, as making too many processes can use up the system's resources and cause performance problems. It is a good idea to be careful when making processes and to make sure they are managed and stopped when they are not needed anymore.

## Searching for processes

There are several ways to search for processes in Linux. The most common way is to use the ps command, which shows a list of running processes. To search for processes by their name, use the `ps` command together with `grep`. For example:

```
ps -ef | grep process_name
```

This will show a list of all processes with the specified name.

Another way to search for processes is to use the `pgrep` command, which searches for processes by name and displays their process IDs. For example (to look for chromium):

```
pgrep chromium
```

This will display the process IDs of all processes with the specified name (chromium in our case).

Additionally, you can use the `htop` command, which provides an interactive, real-time view of running processes. To search for processes in `htop`, press the `F4` key, type the process name or user you want to search for, and press `Enter`. The list will update to show only the matching processes.

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
