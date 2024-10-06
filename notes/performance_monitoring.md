## Performance Monitoring

Performance monitoring helps you identify bottlenecks or issues that may be affecting your system's performance. We'll now explore some tools and techniques available for monitoring performance and explain some usage statistics, such as CPU and RAM usage.

### Understanding Usage Statistics

Usage statistics provide insights into how your system resources are being utilized. These statistics include CPU usage, RAM usage, and disk usage. An increase in these statistics may be due to various factors, such as running resource-intensive applications, insufficient system resources, or a misconfiguration in your system settings.

1. **CPU Usage**: Indicates how much processing power is being used by your system. High CPU usage can cause applications to become sluggish, and your system may become unresponsive.
2. **RAM Usage**: Shows how much of your system's memory is being utilized. If your system runs out of RAM, it will start using swap space, which can significantly slow down your system.
3. **Disk Usage**: Displays how much of your system's storage is being used. High disk usage can lead to a decrease in overall system performance.

### Top: Real-Time System Monitoring

The `top` command is a fundamental tool for real-time system monitoring. It offers a dynamic view of the system's running processes, allowing you to see which processes are consuming the most resources. `top` is particularly useful for diagnosing load and performance issues on a server or a local machine.

To start `top`, simply enter the following in the terminal:

```bash
top
```

This command opens the top interface, which refreshes every few seconds to provide an up-to-date view of the system's state.

When you run top, the output is divided into two sections:

- **System Summary**: At the top, displaying CPU usage, memory usage, swap usage, load average, and uptime.
- **Process List**: Below the summary, listing individual processes. By default, processes are sorted by CPU usage, with the most resource-intensive processes at the top.

Key Features:

- **Dynamic Update**: The display updates in real-time, giving you a current snapshot of system performance.
- **Sorting Options**: By default, processes are sorted by CPU usage. You can press Shift + M to sort by memory usage.
- **Process Monitoring**: To monitor a specific process, use the -p flag followed by the process ID (PID). For example:

```bash
top -p 1234
```

An example of top output might look like this:

```
top - 15:00:02 up 1 day,  4:03,  2 users,  load average: 0.42, 0.35, 0.30
Tasks: 180 total,   2 running, 178 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.1 us,  2.2 sy,  0.0 ni, 92.1 id,  0.4 wa,  0.0 hi,  0.2 si,  0.0 st
KiB Mem :  8026792 total,  123456 free,  2345678 used,  5460658 buff/cache
KiB Swap:  2048000 total,  1755000 free,   293000 used,  1234567 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
1234 user1     20   0  162956   2212   1124 R  25.0  0.3   0:15.03 my_process
5678 user2     20   0  161256   2024   1028 S  12.5  0.2   1:20.03 another_process
```

Bottom Section lists individual processes with the following columns:

- **PID**: Process ID.
- **USER**: User running the process.
- **PR**: Priority of the process.
- **NI**: Nice value - a user-space concept to tune the scheduling priority.
- **VIRT**: Virtual memory size of the process.
- **RES**: Resident size - the non-swapped physical memory the process is using.
- **SHR**: Shared memory size.
- **S**: Process status (e.g., running, sleeping).
- **%CPU**: Percentage of the CPU used by this process.
- **%MEM**: Percentage of physical memory used.
- **TIME+**: Total CPU time used since the process started.
- **COMMAND**: Command that started this process.

Tips for using  `top`:

- **Sorting**: By default, processes are sorted by CPU usage. Press `Shift + M` to sort by memory usage.
- **Killing Processes**: Press `k` followed by the PID to kill a process.
- **Renicing Processes**: Press `r` to change the priority (nice value) of a process.
- **Refreshing and Exiting**: The display updates automatically. Press `q` to quit `top`.

### Htop

`htop` is an interactive system-monitor process viewer for Linux. It is a more advanced and user-friendly alternative to the traditional `top` command. `htop` provides a colorful and visually appealing interface, along with various features that enhance process management and system monitoring.

### Installation

`htop` is not pre-installed on most Linux distributions, but it can be easily installed through package managers.

I. Debian/Ubuntu:

```bash
sudo apt install htop
```

II. CentOS/RHEL:

```bash
sudo yum install htop
```

III. Fedora:

```bash
sudo dnf install htop
```

To start htop, simply type:

```bash
htop
```

Key Features:

- **Process Viewing**: Displays all running processes. Unlike top, it updates in real-time and uses color to provide additional information.
- **System Metrics**: Shows CPU, memory, and swap usage along with load average.
- **Filtering & Searching**: Allows filtering processes by user or text and searching for specific processes.
- **Tree View** An optional tree view to see parent-child relationships among processes.
- **Interactive Interface**: You can interact with processes (e.g., kill, renice) directly in the interface.

An example output of htop might look like this:

```
1  [||||||||||| 34.5%]   Tasks: 65, 132 thr; 2 running
2  [||||||||||  28.7%]   Load average: 1.23 0.97 0.88 
Mem[|||||||||||||||1.45G/3.84G]
Swp[|             0K/512M]

  PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command
1287 root       20   0  256M  4980  3192 R 28.6  0.1  0:03.41 /usr/bin/Xorg
2905 user1      20   0  517M  3720  2012 S 14.0  0.1  1:13.69 gnome-terminal
```

Understanding the Output

- The top bar shows CPU usage for each core, total running tasks, and load averages.
- The next bar provides a summary of memory (Mem) and swap (Swp) usage.
- The main panel lists processes with details like PID, user, priority (PRI), nice value (NI), virtual memory size (VIRT), resident set size (RES), shared memory size (SHR), status (S), and the percentage of CPU and memory used.

### Swap space

Swap space is an area on your hard drive used as virtual memory when your system runs out of physical RAM. It allows your system to continue running even when it has exhausted all available RAM, but it can negatively impact performance, as accessing data from the hard drive is slower than accessing it from RAM.

To view the amount of swap space available on your system, use the `free` command:

```
free -h
```

Here's an example of what the output might look like:

```
              total        used        free      shared  buff/cache   available
Mem:            8G         3.2G        2.1G       101M      2.7G        4.4G
Swap:           2G         1.2G        800M
```

I. Mem (Memory) Section

- `total`: Total physical RAM in the system. In this example, it's 8 gigabytes.
- `used`: Amount of RAM currently being used. Here, 3.2 gigabytes are in use.
- `free`: Amount of RAM that is not being used. This example shows 2.1 gigabytes of free memory.
- `shared`: Memory used (mostly) by tmpfs (temporary file storage) and interprocess communication. In the example, it's 101 megabytes.
- `buff/cache`: Memory used by the kernel for buffers and caching. In this case, it's 2.7 gigabytes.
- `available`: An estimate of how much memory is available for starting new applications, without swapping. Here, it's about 4.4 gigabytes.

II. Swap Section
  
- `total`: Total swap space available. In this example, it's 2 gigabytes.
- `used`: Amount of swap space currently in use. This example shows 1.2 gigabytes being used.
- `free`: Amount of swap space not currently in use. In this case, it's 800 megabytes.

Key Takeaways from the Example:

- The system has 8 GB of total RAM, out of which 3.2 GB is currently in use.
- A significant portion of RAM (2.7 GB) is dedicated to buffer/cache, which helps in speeding up processes by holding data in RAM for quick access.
- The swap space is relatively small compared to the total RAM, and a significant portion (1.2 GB) is in use, which could indicate heavy memory usage or potential memory pressure on the system.
- The 'available' memory (4.4 GB) is a more relevant indicator than 'free' memory for understanding how much memory is readily available for new applications. This is because Linux tends to use free memory for buffers and cache.

### Monitor RAM usage

Monitoring RAM usage is essential for managing system resources efficiently. To do this on Linux systems, the `free -h` command is commonly used. It provides information on the total amount of RAM, along with how much is used and free. If the used memory approaches the total amount of RAM, this could signal a need for more RAM or optimization of current usage.

I. Resident Set Size (RSS)

- RSS indicates the current memory usage of a process.
- It excludes swap memory but includes all stack and heap memory.
- Memory from shared libraries is counted, but only if the pages are physically present in memory.
- Some memory can be shared among applications, so the sum of RSS values can exceed the actual RAM.

II. Virtual Set Size (VSZ)

- VSZ represents the total memory allocated to a process at its initiation.
- It encompasses memory that might be swapped out, unused, or shared from libraries.
- This is a broader measure of a process's memory footprint.

#### Example: Calculating RSS and VSZ

Consider a process with these details:

- Current usage: 450K (binary code), 800K (shared libraries), 120K (stack and heap).
- Initial allocation: 600K (binary code), 2200K (shared libraries), 150K (stack and heap).

Calculations:

I. **RSS:** Total physical memory usage.

- RSS = Binary Code + Shared Libraries + Stack/Heap
- RSS = 450K + 800K + 120K = 1370K

II. **VSZ:** Total memory allocation at start.

- VSZ = Initial Binary Code + Initial Shared Libraries + Initial Stack/Heap
- VSZ = 600K + 2200K + 150K = 2950K

#### Identifying Top Memory-Consuming Processes

To list the 10 processes consuming the most RAM, you can use the command:

```bash
ps -e -o pid,vsz,comm= | sort -n -k 2 -r | head 10
```

#### Finding RAM Usage of a Specific Process

In addition to monitoring overall RAM usage, it's often necessary to track the memory usage of a specific process. 

For example to check the memory usage of a process named nginx:

```bash
ps -o %mem,rss,vsize,cmd -C nginx
```

### Vmstat

`vmstat` displays information about system memory, swap, and CPU usage. It provides a snapshot of the current state of the system, as well as the average statistics over a period of time.

To view the current state of the system, use vmstat without any arguments. To view the average statistics over a period of time, use `vmstat [interval] [count]`, where interval is the time in seconds between each snapshot and count is the number of snapshots to take.

```
vmstat 5 3
```

This command will display 3 snapshots at 5-second intervals.

Example output:

```
$ vmstat 5 3
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 2723288 844288 5670316    0    0    14    42   49   39  7  5 88  0  0
 2  0      0 2729716 844296 5670332    0    0     0   387 8888 12065  3  6 90  0  0
 1  0      0 2735688 844304 5670364    0    0     0   436 9379 13069  4  6 90  0  0
```

### Challenges

1. Run `top` during peak load times and identify any processes consistently using over 50% CPU. Document these processes and research ways to optimize or replace them for better performance.
2. Use `iotop` to monitor disk I/O. Select an application you suspect is causing high I/O, run it, and document its I/O usage pattern. Determine if the usage is justifiable or if it needs optimization.
3. Identify a running service or application suspected of a memory leak. Use `valgrind` or similar tools to trace its memory usage over time. Provide a report with findings and potential solutions.
4. Monitor a specific service using `nethogs` for real-time network bandwidth usage. Analyze its traffic patterns and propose optimizations to reduce unnecessary network load.
5. Write a bash script that alerts when disk usage goes beyond 80%. The script should identify the top five directories contributing to disk usage.
6. When system load average exceeds 1.0, use a combination of `uptime`, `vmstat`, and `dmesg` to diagnose the root cause. Document the methodology and findings.
7. Create a cron job script to gather CPU, memory, and disk usage statistics every hour. Store this data in a log file for a week and analyze it to identify any patterns or anomalies.
8. Set up Nagios to monitor a server. Configure it to send an email alert for critical conditions like CPU usage > 90%, disk space < 10%, and RAM usage > 90%.
