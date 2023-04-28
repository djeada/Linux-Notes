## Performance Monitoring in Linux

Performance monitoring is essential for maintaining the health of your Linux system. It helps you identify bottlenecks or issues that may be affecting your system's performance. In this article, we'll explore some tools and techniques available for monitoring Linux performance and explain some usage statistics, such as CPU and RAM usage.

### Understanding Usage Statistics

Usage statistics provide insights into how your system resources are being utilized. These statistics include CPU usage, RAM usage, and disk usage. An increase in these statistics may be due to various factors, such as running resource-intensive applications, insufficient system resources, or a misconfiguration in your system settings.

1. **CPU Usage**: Indicates how much processing power is being used by your system. High CPU usage can cause applications to become sluggish, and your system may become unresponsive.
2. **RAM Usage**: Shows how much of your system's memory is being utilized. If your system runs out of RAM, it will start using swap space, which can significantly slow down your system.
3. **Disk Usage**: Displays how much of your system's storage is being used. High disk usage can lead to a decrease in overall system performance.

### The top command

The `top` command is a real-time system monitoring tool that allows you to view the resource usage of various processes running on your system. It provides a detailed overview of the CPU, memory, and swap usage, as well as the load average and uptime of your system.

To run `top` without any flags or arguments, simply enter:

```bash
top
```

This will display a list of processes sorted by CPU usage, with the highest usage at the top. You can use the `Shift + M` key combination to sort the processes by memory usage instead.

To monitor a specific process ID, use the `-p` flag:

```
top -p 1234
```

## Htop

`htop` is an enhanced version of `top`, with a more user-friendly interface and additional features like filtering, searching, and process tree view. It requires installation on most systems.

Installation:

```
apt install htop  # Debian/Ubuntu
yum install htop  # CentOS/RHEL
```

Usage:

```
htop
```

## Swap space

Swap space is an area on your hard drive used as virtual memory when your system runs out of physical RAM. It allows your system to continue running even when it has exhausted all available RAM, but it can negatively impact performance, as accessing data from the hard drive is slower than accessing it from RAM.

To view the amount of swap space available on your system, use the `free` command:

```
free -h
```

This will display the total, used, and free swap space in human-readable format (e.g., in MB or GB).

## Monitor RAM usage

To monitor RAM usage on your system, you can use the `free -h` command, which displays the total amount of RAM available, as well as the amount of used and free memory. If the used memory is close to the total amount of RAM, it may indicate that you are running out of RAM and may need to add more or optimize your usage.

Resident Set Size (RSS) is used to indicate how much memory a process is currently using. It does not include swap memory and includes the entire stack and heap memory. Memory from shared libraries is included as long as the pages from those libraries are physically present in memory. However, some of the memory is shared, so other applications may use it, which means that adding up all of the RSS numbers may result in more RAM than your machine actually has.

Virtual Set Size (VSZ) is the memory size allocated to a process when it is first executed. It consists of all memory that the process may access, including swapped-out memory, allocated but not used memory, and memory from shared libraries.

For example, let's consider a process with the following characteristics:

* At the moment, it uses 450K for its own binary code, 800K for shared libraries that are currently loaded, and 120K for stack and heap memory allocation.
* When the process was initially started, it reserved 600K for its binary code, 2200K for shared libraries, and 150K for stack and heap memory allocations.

With this information, we can calculate the Resident Set Size (RSS) and the Virtual Set Size (VSZ) as follows:

a) RSS: This is the total memory the process is currently using in physical RAM. We add up the memory usage for the binary code (450K), the shared libraries (800K), and the stack/heap allocations (120K):

   RSS = 450K + 800K + 120K = 1370K

b) VSZ: This is the total memory size allocated to the process when it started, including memory that might be swapped out, unused, or occupied by shared libraries. We add up the initial reserved memory for the binary code (600K), shared libraries (2200K), and stack/heap allocations (150K):

   VSZ = 600K + 2200K + 150K = 2950K

To find the 10 processes using the most RAM, use the following command:

```
ps -e -o pid,vsz,comm= | sort -n -k 2 -r | head 10
```

## Vmstat
`vmstat` displays information about system memory, swap, and CPU usage. It provides a snapshot of the current state of the system, as well as the average statistics over a period of time.

To view the current state of the system, use vmstat without any arguments. To view the average statistics over a period of time, use `vmstat [interval] [count]`, where interval is the time in seconds between each snapshot and count is the number of snapshots to take.

```
vmstat 5 10
```

This command will display 10 snapshots at 5-second intervals.

## Challenges

1. What command can you use to view the current CPU, memory, and swap usage in real-time?
1. How can you determine if your machine is running low on available memory?
1. What command can you use to view information about CPU and memory usage over time?
1. How can you identify which process is consuming the most CPU or memory resources on your system?
1. What are some common signs that a machine is reaching its limits in terms of CPU, memory, or disk usage?
