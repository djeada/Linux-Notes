## Performance Monitoring

Performance monitoring helps you identify bottlenecks or issues that may be affecting your system's performance. We'll now explore some tools and techniques available for monitoring performance and explain some usage statistics, such as CPU and RAM usage.

### Understanding Usage Statistics

Usage statistics provide insights into how your system resources are being utilized. These statistics include CPU usage, RAM usage, and disk usage. An increase in these statistics may be due to various factors, such as running resource-intensive applications, insufficient system resources, or a misconfiguration in your system settings.

- **CPU Usage** indicates how much processing power is being utilized by your system. When CPU usage is high, applications may become sluggish, and the system can become unresponsive.
- **RAM Usage** shows how much of your system's memory is currently in use. If the system runs out of RAM, it starts using swap space, which can significantly slow down performance.
- **Disk Usage** displays how much of your system's storage is being consumed. High disk usage can negatively affect overall system performance and responsiveness.

### Top

The `top` command is a fundamental tool for real-time system monitoring. It offers a dynamic view of the system's running processes, allowing you to see which processes are consuming the most resources. `top` is particularly useful for diagnosing load and performance issues on a server or a local machine.

To start `top`, simply enter the following in the terminal:

```bash
top
```

This command opens the top interface, which refreshes every few seconds to provide an up-to-date view of the system's state.

When you run top, the output is divided into two sections:

- **System Summary** is displayed at the top, showing key metrics such as CPU usage, memory usage, swap usage, load average, and system uptime.
- **Process List** appears below the summary, listing individual processes, typically sorted by CPU usage, with the most resource-intensive processes displayed at the top by default.

Key Features:

- **Dynamic Update** ensures that the display refreshes in real-time, providing an up-to-date snapshot of system performance.
- **Sorting Options** allow processes to be sorted by CPU usage by default, but pressing Shift + M enables sorting by memory usage instead.
- **Process Monitoring** can be done by using the -p flag followed by the process ID (PID), allowing you to monitor a specific process closely.

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

Understanding the output:

- The current time is 15:00:02.
- The system has been running for 1 day and 4 hours.
- There are 2 users logged in.
- The load average for the past 1 minute is 0.42, for the past 5 minutes is 0.35, and for the past 15 minutes is 0.30.
- There are 180 total tasks.
- 2 tasks are currently running.
- 178 tasks are sleeping.
- 0 tasks are stopped.
- 0 tasks are zombie processes.
- The CPU is 5.1% in user mode, 2.2% in system mode, 0.0% nice processes, 92.1% idle, 0.4% waiting for I/O, 0.0% servicing hardware interrupts, 0.2% servicing software interrupts, and 0.0% stolen by virtual machines.
- The total memory is 8026792 KiB.
- 123456 KiB of memory is free.
- 2345678 KiB of memory is used.
- 5460658 KiB of memory is used for buffers and cache.
- The total swap memory is 2048000 KiB.
- 1755000 KiB of swap is free.
- 293000 KiB of swap is used.
- 1234567 KiB of memory is available.
- Process with PID 1234 is run by user1 and is using 25% of the CPU and 0.3% of memory.
- Process with PID 5678 is run by user2 and is using 12.5% of the CPU and 0.2% of memory.

Bottom Section lists individual processes with the following columns:

| **Field**   | **Description**                                                                      |
|-------------|--------------------------------------------------------------------------------------|
| **PID**     | Process ID.                                                                          |
| **USER**    | User running the process.                                                            |
| **PR**      | Priority of the process.                                                             |
| **NI**      | Nice value - a user-space concept to tune the scheduling priority.                   |
| **VIRT**    | Virtual memory size of the process.                                                  |
| **RES**     | Resident size - the non-swapped physical memory the process is using.                |
| **SHR**     | Shared memory size.                                                                  |
| **S**       | Process status (e.g., running, sleeping).                                            |
| **%CPU**    | Percentage of the CPU used by this process.                                          |
| **%MEM**    | Percentage of physical memory used.                                                  |
| **TIME+**   | Total CPU time used since the process started.                                       |
| **COMMAND** | Command that started this process.                                                   |

Tips for using  `top`:

- By default, processes are sorted by CPU usage. Press `Shift + M` to sort by memory usage.
- Press `k` followed by the PID to kill a process.
- Press `r` to change the priority (nice value) of a process.
- The display updates automatically. Press `q` to quit `top`.

### Htop

`htop` is an interactive system-monitor process viewer for Linux. It is a more advanced and user-friendly alternative to the traditional `top` command. `htop` provides a colorful and visually appealing interface, along with various features that enhance process management and system monitoring.

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

- Displays all running processes. Unlike top, it updates in real-time and uses color to provide additional information.
- Shows CPU, memory, and swap usage along with load average.
- Allows filtering processes by user or text and searching for specific processes.
- Tree View An optional tree view to see parent-child relationships among processes.
- You can interact with processes (e.g., kill, renice) directly in the interface.

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

Understanding the output:

- CPU 1 is using 34.5% of its capacity.
- There are 65 tasks and 132 threads in total.
- 2 tasks are running.
- CPU 2 is using 28.7% of its capacity.
- The load average over the last 1 minute is 1.23, over 5 minutes is 0.97, and over 15 minutes is 0.88.
- 1.45 GB of the 3.84 GB of memory is being used.
- 0 KB of the 512 MB of swap space is being used.
- Process with PID 1287, run by root, is using 28.6% of the CPU and 0.1% of the memory. It is running `/usr/bin/Xorg`.
- Process with PID 2905, run by user1, is using 14.0% of the CPU and 0.1% of the memory. It is running `gnome-terminal`.

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

Understanding the output:

- The system has 8 GB of total RAM, out of which 3.2 GB is currently in use.
- A significant portion of RAM (2.7 GB) is dedicated to buffer/cache, which helps in speeding up processes by holding data in RAM for quick access.
- The swap space is relatively small compared to the total RAM, and a significant portion (1.2 GB) is in use, which could indicate heavy memory usage or potential memory pressure on the system.
- The 'available' memory (4.4 GB) is a more relevant indicator than 'free' memory for understanding how much memory is readily available for new applications. This is because Linux tends to use free memory for buffers and cache.

I. Mem (Memory) Section

| **Field**     | **Description**                                                                                             |
|---------------|-------------------------------------------------------------------------------------------------------------|
| `total`       | Total physical RAM in the system. In this example, it's 8 gigabytes.                                         |
| `used`        | Amount of RAM currently being used. Here, 3.2 gigabytes are in use.                                          |
| `free`        | Amount of RAM that is not being used. This example shows 2.1 gigabytes of free memory.                       |
| `shared`      | Memory used (mostly) by tmpfs (temporary file storage) and interprocess communication. In the example, it's 101 megabytes. |
| `buff/cache`  | Memory used by the kernel for buffers and caching. In this case, it's 2.7 gigabytes.                         |
| `available`   | An estimate of how much memory is available for starting new applications, without swapping. Here, it's about 4.4 gigabytes. |

II. Swap Section
  
| **Field**   | **Description**                                                                        |
|-------------|----------------------------------------------------------------------------------------|
| `total`     | Total swap space available. In this example, it's 2 gigabytes.                         |
| `used`      | Amount of swap space currently in use. This example shows 1.2 gigabytes being used.     |
| `free`      | Amount of swap space not currently in use. In this case, it's 800 megabytes.            |

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

Example Output of Command:

```
  PID     VSZ  COMMAND
 1234  2048000  java
 5678  1800000  mysqld
 9101  1600000  apache2
 1213  1500000  postgres
 3141  1400000  python
 2718  1300000  node
 1928  1200000  nginx
 2930  1100000  redis-server
 3435  1000000  sshd
 4756   900000  systemd
```

Understanding the output:

- The output displays the top 10 processes sorted by virtual memory size (VSZ) in descending order.
- PID is the process identifier.
- VSZ shows the virtual memory size in kilobytes (KB) used by each process.
- COMMAND represents the name of the command or process that is running.

#### Finding RAM Usage of a Specific Process

In addition to monitoring overall RAM usage, it's often necessary to track the memory usage of a specific process. 

For example to check the memory usage of a process named `nginx`:

```bash
ps -o %mem,rss,vsize,cmd -C nginx
```

Example Output of Command:

```
%MEM   RSS     VSZ     CMD
 2.3   12000   250000  nginx: master process /usr/sbin/nginx
 1.2    6000   150000  nginx: worker process
 1.2    6000   150000  nginx: worker process
```

Understanding the output:

- The first process listed is the nginx master process, while the others are worker processes.
- The master `nginx` process uses 2.3% of the system memory, while each worker process uses 1.2%.
- The `nginx` master process is using 12000 KB of RAM, while each worker process is using 6000 KB.
- The `nginx` master process is using 250000 KB of virtual memory, while each worker process is using 150000 KB.

The output constists of following columns:

| **Field**   | **Description**                                                                                               |
|-------------|---------------------------------------------------------------------------------------------------------------|
| `%MEM`      | The percentage of the system's physical memory (RAM) used by the process.                                      |
| `RSS`       | The resident set size, which is the amount of physical memory (in kilobytes) the process is currently using.    |
| `VSZ`       | The virtual memory size (in kilobytes) allocated to the process.                                               |
| `CMD`       | The command that started the process, along with any arguments (e.g., the nginx processes).                    |

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

Understanding the output:

- 1 process is running, 0 processes are blocked in the first sample.
- No swap is in use (swpd = 0 KB).
- 2723288 KB of memory is free.
- 844288 KB of memory is used for buffers.
- 5670316 KB of memory is used for cache.
- There is no swap-in (si = 0) or swap-out (so = 0) activity.
- 14 blocks were read from disk per second (bi).
- 42 blocks were written to disk per second (bo).
- 49 interrupts occurred per second (in).
- 39 context switches occurred per second (cs).
- 7% of CPU time was spent in user mode.
- 5% of CPU time was spent in system mode.
- 88% of CPU time was idle.
- 0% of CPU time was waiting for I/O (wa).
- 0% of CPU time was stolen by the hypervisor (st).

The output constists of following columns:

| **Field** | **Description**                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------|
| `r`       | Number of processes waiting for runtime (running or runnable).                                                   |
| `b`       | Number of processes in uninterruptible sleep (blocked).                                                          |
| `swpd`    | Amount of virtual memory used (swap space) in kilobytes.                                                         |
| `free`    | Amount of idle/free memory in kilobytes.                                                                         |
| `buff`    | Amount of memory used for buffers in kilobytes.                                                                  |
| `cache`   | Amount of memory used as cache in kilobytes.                                                                     |
| `si`      | Amount of memory swapped in from disk (swap in) per second in kilobytes.                                          |
| `so`      | Amount of memory swapped out to disk (swap out) per second in kilobytes.                                          |
| `bi`      | Blocks received from a block device (blocks in) per second.                                                      |
| `bo`      | Blocks sent to a block device (blocks out) per second.                                                           |
| `in`      | Number of interrupts per second.                                                                                 |
| `cs`      | Number of context switches per second.                                                                           |
| `us`      | Percentage of CPU time spent in user mode.                                                                       |
| `sy`      | Percentage of CPU time spent in system (kernel) mode.                                                            |
| `id`      | Percentage of CPU time spent idle.                                                                               |
| `wa`      | Percentage of CPU time spent waiting for I/O.                                                                    |
| `st`      | Percentage of CPU time stolen from the VM by the hypervisor (in virtualized environments).                       |

### Challenges

1. Run `top` during peak load times and identify any processes consistently using over 50% CPU. Document these processes and research ways to optimize or replace them for better performance.
2. Use `iotop` to monitor disk I/O. Select an application you suspect is causing high I/O, run it, and document its I/O usage pattern. Determine if the usage is justifiable or if it needs optimization.
3. Identify a running service or application suspected of a memory leak. Use `valgrind` or similar tools to trace its memory usage over time. Provide a report with findings and potential solutions.
4. Monitor a specific service using `nethogs` for real-time network bandwidth usage. Analyze its traffic patterns and propose optimizations to reduce unnecessary network load.
5. Write a bash script that alerts when disk usage goes beyond 80%. The script should identify the top five directories contributing to disk usage.
6. When system load average exceeds 1.0, use a combination of `uptime`, `vmstat`, and `dmesg` to diagnose the root cause. Document the methodology and findings.
7. Create a cron job script to gather CPU, memory, and disk usage statistics every hour. Store this data in a log file for a week and analyze it to identify any patterns or anomalies.
8. Set up Nagios to monitor a server. Configure it to send an email alert for critical conditions like CPU usage > 90%, disk space < 10%, and RAM usage > 90%.
