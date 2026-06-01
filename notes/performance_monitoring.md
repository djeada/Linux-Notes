## Performance Monitoring

Performance monitoring is the process of observing how a system uses its resources.

The goal is to understand whether the system is healthy, overloaded, or waiting on a specific bottleneck.

A bottleneck is the resource that limits performance.

Common bottlenecks include:

- CPU
- RAM
- swap
- disk I/O
- disk space
- network
- process limits
- misbehaving applications

A system may feel slow for many reasons. Performance monitoring helps avoid guessing.

Instead of saying:

```text
The server is slow.
```

we want to answer:

- Is the CPU saturated?
- Is memory exhausted?
- Is the system swapping?
- Is disk I/O slow?
- Is the disk full?
- Which process is responsible?
- When did the problem start?

### Basic Performance Model

A Linux system runs many processes. Those processes compete for CPU, memory, disk, and network resources.

```text
+-------------------+
| Applications      |
| nginx, database,  |
| browser, scripts  |
+---------+---------+
          |
          v
+-------------------+
| Linux Kernel      |
| scheduler, memory |
| filesystem, I/O   |
+---------+---------+
          |
          v
+-------------------+
| Hardware          |
| CPU, RAM, disk,   |
| network card      |
+-------------------+
```

Monitoring tools observe these layers and show how busy they are.

### Important Usage Statistics

The most common system usage statistics are:

- CPU usage
- RAM usage
- swap usage
- disk usage
- disk I/O
- load average
- process states

Each statistic tells a different part of the story.

### CPU Usage

CPU usage shows how much processing work the system is doing.

High CPU usage can mean:

- an application is doing heavy computation
- too many processes are running
- a process is stuck in a loop
- encryption or compression is active
- the system is under legitimate load

CPU usage is not automatically bad. A busy CPU may be normal if the system is doing useful work.

The important question is:

```text
Is the CPU busy because of expected work,
or is one process consuming CPU unexpectedly?
```

### RAM Usage

RAM is fast working memory.

Linux uses RAM for:

- running programs
- kernel data
- file cache
- buffers
- shared libraries
- temporary files

Linux often uses available RAM for cache. This is usually good.

A system can show little “free” memory and still be healthy because cached memory can be reclaimed when applications need it.

The better field to watch is usually:

```text
available memory
```

not just:

```text
free memory
```

### Swap Usage

Swap is disk space used as overflow memory.

Swap helps prevent immediate crashes when RAM is full, but it is much slower than RAM.

Heavy swap usage can make a system feel extremely slow.

```text
RAM is fast.
Swap is much slower because it uses disk.
```

Some swap usage is not always a problem. Continuous swap-in and swap-out activity is a problem.

### Disk Usage vs Disk I/O

Disk usage and disk I/O are different.

Disk usage means how much storage space is filled.

Example:

```text
The filesystem is 95% full.
```

Disk I/O means how actively the disk is reading and writing.

Example:

```text
The disk is writing 300 MB/s and is 100% busy.
```

A disk can be almost full but not busy.

A disk can have plenty of free space but still be overloaded with reads and writes.

### Load Average

Load average shows how many processes are running or waiting to run.

It is shown over three time periods:

- 1 minute
- 5 minutes
- 15 minutes

Example:

```text
load average: 0.42, 0.35, 0.30
```

On a single-core system, a load of `1.00` roughly means the CPU is fully occupied.

On a four-core system, a load of `4.00` may be normal under full CPU use.

However, load average can also increase when processes are waiting on disk I/O, not just CPU.

So high load means:

```text
There is work waiting.
```

It does not always mean:

```text
The CPU is the bottleneck.
```

### Monitoring Workflow

A good performance investigation follows a structured path.

1. Check load average
2. Check CPU usage
3. Check memory and swap
4. Check disk I/O
5. Check disk space
6. Identify the responsible process
7. Check logs for errors
8. Decide whether the load is expected or abnormal

Useful starting commands:

```bash
uptime
top
free -h
vmstat 1
iostat -xz 1
df -h
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```

### `top`

The `top` command provides a live view of system activity.

Run:

```bash
top
```

It shows two main sections:

- system summary
- process list

The system summary shows CPU, memory, swap, load average, task count, and uptime.

The process list shows running processes, usually sorted by CPU usage.

### Example `top` Output

```text
top - 15:00:02 up 1 day,  4:03,  2 users,  load average: 0.42, 0.35, 0.30
Tasks: 180 total,   2 running, 178 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.1 us,  2.2 sy,  0.0 ni, 92.1 id,  0.4 wa,  0.0 hi,  0.2 si,  0.0 st
KiB Mem :  8026792 total,  123456 free,  2345678 used,  5460658 buff/cache
KiB Swap:  2048000 total,  1755000 free,   293000 used,  1234567 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
1234 user1     20   0  162956   2212   1124 R  25.0  0.3   0:15.03 my_process
5678 user2     20   0  161256   2024   1028 S  12.5  0.2   1:20.03 another_process
```

### Understanding the Top Summary

- 15:00:02                 current time
- up 1 day, 4:03           system uptime
- 2 users                  logged-in users
- load average             average runnable/waiting work
- Tasks                    process summary
- %Cpu(s)                  CPU time breakdown
- KiB Mem                  physical memory summary
- KiB Swap                 swap summary

### Understanding CPU Fields in `top`

- us   user CPU time
- sy   system/kernel CPU time
- ni   nice-priority process CPU time
- id   idle CPU time
- wa   I/O wait time
- hi   hardware interrupt time
- si   software interrupt time
- st   stolen time in virtual machines

Example:

```text
%Cpu(s): 5.1 us, 2.2 sy, 92.1 id, 0.4 wa
```

Interpretation:

- The CPU is mostly idle.
- There is very little I/O wait.
- The system is not CPU-bound in this sample.

### Understanding Process Columns in `top`

- PID       process ID
- USER      user running the process
- PR        kernel scheduling priority
- NI        nice value
- VIRT      virtual memory size
- RES       resident memory in physical RAM
- SHR       shared memory
- S         process state
- %CPU      CPU percentage used by process
- %MEM      physical RAM percentage used
- TIME+     total CPU time consumed
- COMMAND   command or process name

Important process states:

- R   running or runnable
- S   sleeping
- D   uninterruptible sleep, often I/O wait
- T   stopped
- Z   zombie

### Useful `top` Keys

- Shift + M   sort by memory usage
- Shift + P   sort by CPU usage
- k           kill a process
- r           renice a process
- 1           show per-core CPU usage
- q           quit

To monitor one process:

```bash
top -p 1234
```

### `htop`

`htop` is an interactive and more user-friendly alternative to `top`.

It shows CPU bars, memory bars, process lists, searching, filtering, tree view, and easier process management.

Install it on Debian or Ubuntu:

```bash
sudo apt install htop
```

On Red Hat or CentOS:

```bash
sudo yum install htop
```

On Fedora:

```bash
sudo dnf install htop
```

Run:

```bash
htop
```

### Example `htop` View

```text
1  [||||||||||| 34.5%]   Tasks: 65, 132 thr; 2 running
2  [||||||||||  28.7%]   Load average: 1.23 0.97 0.88
Mem[|||||||||||||||1.45G/3.84G]
Swp[|             0K/512M]

  PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command
1287 root       20   0  256M  4980  3192 R 28.6  0.1  0:03.41 /usr/bin/Xorg
2905 user1      20   0  517M  3720  2012 S 14.0  0.1  1:13.69 gnome-terminal
```

Interpretation:

- CPU core 1 is using 34.5%.
- CPU core 2 is using 28.7%.
- Memory usage is 1.45 GB out of 3.84 GB.
- Swap is not being used.
- Xorg is the most CPU-heavy process in this sample.

`htop` is useful when you want to interactively inspect and manage processes.

### `free`

The `free` command shows memory and swap usage.

Run:

```bash
free -h
```

The `-h` option shows human-readable units.

Example output:

```text
              total        used        free      shared  buff/cache   available
Mem:            8G         3.2G        2.1G       101M      2.7G        4.4G
Swap:           2G         1.2G        800M
```

### Understanding `free -h`

Important memory fields:

- total        total physical RAM
- used         memory currently used
- free         completely unused memory
- shared       memory used mainly by tmpfs and shared mappings
- buff/cache   memory used for buffers and filesystem cache
- available    estimated memory available for new applications

Important swap fields:

- total        total swap space
- used         swap currently used
- free         unused swap

Interpretation of the example:

- The system has 8 GB RAM.
- 3.2 GB is used by processes and system activity.
- 2.7 GB is used for buffers/cache.
- 4.4 GB is available for new programs.
- 1.2 GB of swap is used.

The most important field for practical memory pressure is usually:

```text
available
```

If `available` is low and swap activity is high, the system may be under memory pressure.

### RSS and VSZ

Linux process memory can be confusing because there are multiple memory measurements.

Two important fields are:

- RSS
- VSZ

### RSS

RSS means Resident Set Size.

It is the amount of physical RAM currently used by the process.

RSS is usually more useful than VSZ when asking:

```text
How much real RAM is this process using right now?
```

However, RSS includes shared memory pages, so adding RSS values for many processes can overcount total RAM.

### VSZ

VSZ means Virtual Set Size, or virtual memory size.

It includes memory that may be:

- actually in RAM
- mapped but unused
- shared libraries
- memory-mapped files
- swapped out
- reserved address space

VSZ can look large even when actual RAM use is modest.

A common mistake is to treat VSZ as real RAM usage. For physical RAM pressure, check RSS and `%MEM`.

### Example RSS and VSZ Calculation

Suppose a process currently uses:

- 450K binary code in RAM
- 800K shared libraries in RAM
- 120K stack and heap in RAM

RSS is:

```text
450K + 800K + 120K = 1370K
```

Suppose the process has virtually allocated:

- 600K binary code
- 2200K shared libraries
- 150K stack and heap

VSZ is:

```text
600K + 2200K + 150K = 2950K
```

The process has a larger virtual memory footprint than physical resident memory.

### Finding Top Memory Processes

To show processes sorted by real physical memory percentage:

```bash
ps aux --sort=-%mem | head -n 10
```

Example output:

```text
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
mysql     5678 12.0 18.5 2540000 1500000 ?     Sl   10:00   3:20 mysqld
java      1234 25.0 15.0 4096000 1210000 ?     Sl   09:50   8:10 java
postgres  1213  5.0  8.0 1500000  650000 ?     Sl   09:55   2:30 postgres
```

Interpretation:

- mysqld is using the most physical RAM.
- RSS shows actual resident memory.
- VSZ is larger because it includes virtual address space.

To sort by VSZ instead:

```bash
ps -e -o pid,vsz,rss,comm --sort=-vsz | head -n 10
```

Important note:

- Sorting by VSZ shows largest virtual memory allocations.
- Sorting by RSS or %MEM is usually better for real RAM pressure.

### Checking Memory for a Specific Process

Example for `nginx`:

```bash
ps -o %mem,rss,vsz,cmd -C nginx
```

Example output:

```text
%MEM   RSS     VSZ     CMD
 2.3   12000   250000  nginx: master process /usr/sbin/nginx
 1.2    6000   150000  nginx: worker process
 1.2    6000   150000  nginx: worker process
```

Interpretation:

- The master process uses 12 MB of resident RAM.
- Each worker uses about 6 MB of resident RAM.
- VSZ is larger than RSS because it includes virtual mappings.

### `vmstat`

`vmstat` shows process, memory, swap, disk I/O, system, and CPU statistics.

Run a single snapshot:

```bash
vmstat
```

Run updates every second:

```bash
vmstat 1
```

Run three samples five seconds apart:

```bash
vmstat 5 3
```

### Example `vmstat` Output

```text
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 2723288 844288 5670316    0    0    14    42   49   39  7  5 88  0  0
 2  0      0 2729716 844296 5670332    0    0     0   387 8888 12065  3  6 90  0  0
 1  0      0 2735688 844304 5670364    0    0     0   436 9379 13069  4  6 90  0  0
```

Important fields:

- r     runnable processes
- b     blocked processes
- swpd  swap used
- free  free memory
- buff  buffer memory
- cache cache memory
- si    swap in
- so    swap out
- bi    blocks read from disk
- bo    blocks written to disk
- in    interrupts per second
- cs    context switches per second
- us    user CPU
- sy    system CPU
- id    idle CPU
- wa    I/O wait
- st    stolen CPU time in virtual machines

Interpretation of this example:

- The system is mostly idle.
- There is no swap activity.
- There are no blocked processes.
- Disk I/O is light.
- I/O wait is 0.

### `uptime`

`uptime` is a quick way to check how long the system has been running and what the load average is.

Run:

```bash
uptime
```

Example output:

```text
15:00:02 up 1 day, 4:03, 2 users, load average: 0.42, 0.35, 0.30
```

Interpretation:

- The system has been running for 1 day and 4 hours.
- There are 2 logged-in users.
- Load average is low.

### `iostat`

`iostat` reports CPU and disk I/O statistics.

Install it through `sysstat` if needed:

```bash
sudo apt install sysstat
```

Run:

```bash
iostat -xz 1
```

Important disk fields:

- r/s       reads per second
- w/s       writes per second
- rkB/s     kilobytes read per second
- wkB/s     kilobytes written per second
- await     average wait time for I/O requests
- aqu-sz    average queue size
- %util     how busy the device is

Example output:

```text
Device            r/s     w/s     rkB/s     wkB/s   await  aqu-sz  %util
sda              1.00    2.00     50.00    100.00    2.20    0.01   0.15
```

Interpretation:

- The disk is barely busy.
- Read and write rates are low.
- Wait time is low.
- There is no disk I/O bottleneck in this sample.

### `iotop`

`iotop` shows disk I/O by process.

Install:

```bash
sudo apt install iotop
```

Run:

```bash
sudo iotop -o
```

The `-o` option shows only processes currently doing I/O.

Example output:

```text
Total DISK READ: 100.00 K/s | Total DISK WRITE: 50.00 K/s
PID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN     IO>    COMMAND
7890 be/4  user      50.00 K/s   25.00 K/s  0.00 %  10.00 %  process_a
5678 be/4  user      50.00 K/s   25.00 K/s  0.00 %   5.00 %  process_b
```

Interpretation:

- process_a and process_b are doing disk I/O.
- process_a has higher I/O wait impact.

`iotop` is useful when you know the disk is busy and want to know which process is responsible.

### `df` and `du`

`df` shows filesystem space usage.

Run:

```bash
df -h
```

Example:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       100G   92G  8.0G  92% /
```

Interpretation:

- The root filesystem is 92% full.
- This may become a problem soon.

`du` shows directory usage.

Example:

```bash
sudo du -h --max-depth=1 /var | sort -h
```

Example output:

```text
100M    /var/tmp
2.0G    /var/log
12G     /var/lib
15G     /var
```

Interpretation:

- /var/lib is using most of the space under /var.
- Investigate that directory next.

### Scenario 1: Simulate a CPU Bottleneck

Create high CPU usage and verify it with `top`, `htop`, and `vmstat`.

#### Simulate the Bottleneck

Install `stress-ng` if needed:

```bash
sudo apt install stress-ng
```

Run a CPU stress test:

```bash
stress-ng --cpu 4 --timeout 60s
```

This starts four CPU workers for 60 seconds.

#### Check with `top`

```bash
top
```

Example output:

```text
%Cpu(s): 96.0 us,  3.0 sy,  0.0 ni,  1.0 id,  0.0 wa

PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM COMMAND
4321 user      20   0   50000   8000   2000 R 399.0  0.1 stress-ng-cpu
```

Interpretation:
- CPU user time is very high.
- Idle time is almost zero.
- stress-ng is using about four CPU cores.
- I/O wait is zero, so this is not a disk bottleneck.

#### Check with `vmstat`

```bash
vmstat 1
```

Example output:

```text
r  b   swpd   free   buff  cache   si   so    bi    bo   in    cs us sy id wa st
5  0      0 800000  20000 500000    0    0     0     1 3000  6000 95  4  1  0  0
```

Interpretation:

- r is high because processes are waiting for CPU time.
- us is high.
- wa is zero.
- This confirms CPU saturation.

#### Possible Fixes

- stop or optimize the CPU-heavy process
- reduce worker count
- schedule the job for off-peak hours
- add CPU capacity
- use nice to lower priority

Example:

```bash
nice -n 10 command
```

### Scenario 2: Simulate Memory Pressure

Create memory pressure and observe it with `free`, `top`, and `vmstat`.

#### Simulate the Bottleneck

Run:

```bash
stress-ng --vm 2 --vm-bytes 70% --timeout 60s
```

This starts memory workers that allocate memory.

#### Check with `free`

```bash
free -h
```

Example output:

```text
              total        used        free      shared  buff/cache   available
Mem:            8.0G        6.9G        250M       120M        850M        600M
Swap:           2.0G        100M        1.9G
```

Interpretation:
- Used memory is high.
- Available memory is low.
- Swap has started to be used.
- The system is under memory pressure.

#### Check with `vmstat`

```bash
vmstat 1
```

Example output:

```text
r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
2  1 200000 100000  12000 200000  100  300  800  1500 2500 7000 30 15 45 10  0
```

Interpretation:

- si and so are nonzero, so swap activity is happening.
- wa is elevated because swap uses disk.
- The root issue is memory pressure.

#### Possible Fixes

- stop memory-heavy processes
- reduce application memory limits
- add RAM
- fix memory leaks
- tune caches or worker counts
- avoid running too many memory-heavy jobs together

### Scenario 3: Simulate Swap Thrashing

Show how heavy swap activity can slow a system.

#### Simulate Carefully

Use a stronger memory test only on a lab system:

```bash
stress-ng --vm 4 --vm-bytes 90% --timeout 60s
```

#### Check with `vmstat`

```bash
vmstat 1
```

Example output:

```text
r  b   swpd    free   buff  cache    si    so     bi     bo   in    cs us sy id wa st
3  6 1500000  50000  8000  90000  5000  7000  12000  18000 5000 15000 15 20 20 45  0
```

Interpretation:
- swpd is high.
- si and so are very high.
- b is high, meaning blocked processes.
- wa is high, meaning the CPU waits on disk.
- This is swap thrashing.

The system may feel frozen because it is constantly moving memory pages between RAM and disk.

#### Possible Fixes

- reduce memory load immediately
- stop the offending process
- add RAM
- reduce application concurrency
- investigate memory leaks
- review swap configuration

### Scenario 4: Simulate Disk I/O Bottleneck

Create heavy disk writes and verify them with `iostat`, `iotop`, and `vmstat`.

#### Simulate the Bottleneck

Install tools:

```bash
sudo apt install fio sysstat iotop
```

Run a safe file-based write test:

```bash
mkdir -p ~/perf-lab

fio --name=write-test \
    --directory=~/perf-lab \
    --size=1G \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --runtime=60 \
    --time_based
```

#### Check with `iostat`

```bash
iostat -xz 1
```

Example output:

```text
Device            r/s     w/s     rkB/s     wkB/s   await  aqu-sz  %util
sda              0.00  350.00      0.00  350000.0   32.50   10.20  99.60
```

Interpretation:
- w/s and wkB/s are high.
- await is elevated.
- aqu-sz shows queueing.
- %util is close to 100%.
- The disk is saturated by writes.

#### Check with `iotop`

```bash
sudo iotop -o
```

Example output:

```text
Total DISK WRITE: 340.00 M/s
TID  PRIO USER DISK READ DISK WRITE IO> COMMAND
5221 be/4 user 0.00 B/s  338.00 M/s 92% fio --name=write-test
```

Interpretation:

- fio is the process generating disk pressure.
- The bottleneck is disk write I/O.

#### Possible Fixes

- move heavy writes to off-peak hours
- use ionice for background jobs
- move workload to faster storage
- separate logs, databases, and backups onto different disks
- reduce unnecessary writes

Example:

```bash
ionice -c3 backup-command
```

### Scenario 5: Simulate High Disk Space Usage

Create a nearly full filesystem in a safe test directory and diagnose it.

#### Simulate the Problem

Create a large test file:

```bash
mkdir -p ~/perf-lab
fallocate -l 1G ~/perf-lab/bigfile.img
```

Check disk usage:

```bash
du -sh ~/perf-lab
```

Example output:

```text
1.1G    /home/user/perf-lab
```

Check filesystem space:

```bash
df -h ~
```

Example output:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       20G   18G  2.0G  90% /
```

Interpretation:
- The filesystem is 90% full.
- The test directory contributes about 1.1 GB.
- If this were production, the system could soon fail writes or logs.

#### Find Large Directories

```bash
du -h --max-depth=1 ~ | sort -h
```

Example output:

```text
100M    /home/user/Documents
500M    /home/user/Downloads
1.1G    /home/user/perf-lab
2.0G    /home/user
```

Interpretation:

```text
perf-lab is one of the largest directories under the home directory.
```

#### Clean Up

```bash
rm -rf ~/perf-lab
```

### Scenario 6: Simulate High Load Average from CPU

Understand load average when CPU is the bottleneck.

#### Simulate

```bash
stress-ng --cpu 4 --timeout 120s
```

#### Check Load

```bash
uptime
```

Example output:

```text
15:30:00 up 2 days,  1 user,  load average: 4.20, 2.10, 1.00
```

Check CPU count:

```bash
nproc
```

Example output:

```text
4
```

Interpretation:
- The 1-minute load is about 4.20.
- The system has 4 CPUs.
- This indicates the CPU is near full utilization.

Confirm with `top`:

```text
High us, low id, low wa = CPU-bound load.
```

### Scenario 7: Simulate High Load Average from Disk Wait

Show that high load can come from I/O wait, not just CPU work.

#### Simulate

Run a disk-heavy workload:

```bash
fio --name=randwrite-test \
    --directory=~/perf-lab \
    --size=1G \
    --rw=randwrite \
    --bs=4k \
    --numjobs=4 \
    --iodepth=32 \
    --direct=1 \
    --runtime=60 \
    --time_based
```

#### Check

```bash
uptime
vmstat 1
iostat -xz 1
```

Example `vmstat` output:

```text
r  b   swpd   free   buff  cache   si   so    bi    bo   in    cs us sy id wa st
1  8      0 500000  20000 700000    0    0     0 75000 3000 9000  5  8 15 72  0
```

Example `iostat` output:

```text
Device            r/s     w/s    rkB/s    wkB/s   await  aqu-sz  %util
sda              0.00  5200.00   0.00  20800.0   48.30   25.60  99.90
```

Interpretation:
- b is high, meaning blocked processes.
- wa is high, meaning CPU is waiting for I/O.
- Disk %util is near 100%.
- This high load is caused by disk I/O wait, not CPU computation.

### Scenario 8: Identify a Memory-Heavy Process

Find which process is consuming RAM.

#### Simulate

Start a memory workload:

```bash
stress-ng --vm 1 --vm-bytes 1G --timeout 120s
```

#### Check with `ps`

```bash
ps aux --sort=-%mem | head -n 10
```

Example output:

```text
USER       PID %CPU %MEM    VSZ     RSS COMMAND
user      7001 80.0 12.5 1200000 1024000 stress-ng-vm
mysql     5678 10.0  8.0 2500000  650000 mysqld
```

Interpretation:
- stress-ng-vm is using the most physical RAM.
- RSS is about 1 GB.
- This process is responsible for memory pressure.

#### Check Specific Process

```bash
ps -o pid,%mem,rss,vsz,cmd -p 7001
```

Example:

```text
PID  %MEM     RSS     VSZ CMD
7001 12.5 1024000 1200000 stress-ng-vm
```

### Scenario 9: Simulate a Zombie Process

Understand zombie processes and how to identify them.

A zombie process has finished running but still has an entry in the process table because its parent has not collected its exit status.

#### Simulate with a Small Script

Create a file:

```bash
cat > /tmp/make-zombie.py <<'EOF'
import os
import time

pid = os.fork()
if pid == 0:
    os._exit(0)
else:
    time.sleep(60)
EOF
```

Run it:

```bash
python3 /tmp/make-zombie.py
```

In another terminal:

```bash
ps -eo pid,ppid,state,cmd | grep ' Z '
```

Example output:

```text
8123  8122 Z [python3] <defunct>
```

Interpretation:
- State Z means zombie.
- The child process exited.
- The parent process has not collected it yet.
- A few short-lived zombies are usually harmless.
- Many zombies may indicate a broken parent process.

#### Fix

Usually fix or restart the parent process.

In this simulation, wait 60 seconds or stop the parent script.

### Scenario 10: Script an Alert for Disk Usage Above 80%

Create a simple script that warns when a filesystem is too full and lists the largest directories.

#### Script

```bash
cat > ~/check-disk-usage.sh <<'EOF'
#!/bin/bash

THRESHOLD=80
TARGET="/"

USAGE=$(df -P "$TARGET" | awk 'NR==2 {gsub("%","",$5); print $5}')

if [ "$USAGE" -ge "$THRESHOLD" ]; then
    echo "WARNING: $TARGET is ${USAGE}% full"
    echo
    echo "Top directories under /:"
    sudo du -xhd1 / 2>/dev/null | sort -h | tail -n 5
else
    echo "OK: $TARGET is ${USAGE}% full"
fi
EOF

chmod +x ~/check-disk-usage.sh
```

Run:

```bash
~/check-disk-usage.sh
```

Example output:

```text
WARNING: / is 87% full

Top directories under /:
1.2G    /opt
2.5G    /home
4.0G    /var
8.0G    /usr
18G     /
```

Interpretation:
- The root filesystem is above the threshold.
- The largest top-level directories are listed.
- Investigate /var, /usr, or /home depending on what is unexpectedly large.

### Scenario 11: Gather Hourly Performance Logs

Collect simple performance statistics over time.

#### Create a Script

```bash
cat > ~/perf-snapshot.sh <<'EOF'
#!/bin/bash

LOG="$HOME/perf-history.log"

{
    echo "===== $(date) ====="
    echo "--- uptime ---"
    uptime
    echo "--- memory ---"
    free -h
    echo "--- disk space ---"
    df -h /
    echo "--- top CPU processes ---"
    ps aux --sort=-%cpu | head -n 6
    echo "--- top memory processes ---"
    ps aux --sort=-%mem | head -n 6
    echo
} >> "$LOG"
EOF

chmod +x ~/perf-snapshot.sh
```

Run manually:

```bash
~/perf-snapshot.sh
```

Add to cron:

```bash
crontab -e
```

Add:

```text
0 * * * * /home/user/perf-snapshot.sh
```

Interpretation:
- The script records a basic hourly snapshot.
- After several days, compare timestamps to identify peak usage times.

### Performance Troubleshooting Decision Guide

Use this guide to interpret common patterns.

#### Pattern: High CPU, Low I/O Wait

Example:

```text
top: us = 95%, id = 1%, wa = 0%
```

Likely cause:

```text
CPU-bound workload
```

Check:

```bash
ps aux --sort=-%cpu | head
```

#### Pattern: High I/O Wait

Example:

```text
top: wa = 70%
vmstat: b is high
iostat: %util is 99%
```

Likely cause:

```text
disk I/O bottleneck
```

Check:

```bash
iostat -xz 1
sudo iotop -o
```

#### Pattern: Low Available Memory and Swap Activity

Example:

```text
free: available memory is low
vmstat: si and so are high
```

Likely cause:

```text
memory pressure or memory leak
```

Check:

```bash
ps aux --sort=-%mem | head
```

#### Pattern: High Load but CPU Idle

Example:

```text
uptime: load average high
top: CPU mostly idle
vmstat: b high, wa high
```

Likely cause:

```text
processes blocked on I/O
```

Check:

```bash
vmstat 1
iostat -xz 1
ps -eo pid,stat,cmd | awk '$2 ~ /D/ {print}'
```

#### Pattern: Disk Almost Full

Example:

```text
df -h: Use% above 90%
```

Likely cause:

```text
logs, cache, backups, database files, or user data consuming space
```

Check:

```bash
sudo du -xhd1 / | sort -h
```

### Useful Command Summary

General:

```bash
uptime
top
htop
vmstat 1
free -h
```

CPU:

```bash
ps aux --sort=-%cpu | head
top -p PID
```

Memory:

```bash
free -h
ps aux --sort=-%mem | head
ps -o pid,%mem,rss,vsz,cmd -p PID
```

Disk space:

```bash
df -h
du -h --max-depth=1 DIRECTORY | sort -h
```

Disk I/O:

```bash
iostat -xz 1
sudo iotop -o
vmstat 1
```

Process states:

```bash
ps -eo pid,ppid,state,cmd
ps -eo pid,stat,cmd | awk '$2 ~ /D/ {print}'
```

Stress testing in labs:

```bash
stress-ng --cpu 4 --timeout 60s
stress-ng --vm 2 --vm-bytes 70% --timeout 60s
fio --name=write-test --directory=~/perf-lab --size=1G --rw=write --bs=1M --direct=1 --runtime=60 --time_based
```

### Safe Lab Rules

Before simulating bottlenecks:

- Do not run heavy tests on production systems.
- Use a virtual machine or lab machine.
- Watch temperatures during CPU stress tests.
- Check disk space before fio tests.
- Avoid filling important filesystems.
- Stop tests if the system becomes unstable.
- Clean up test files afterward.

Clean up test data:

```bash
rm -rf ~/perf-lab
```

### Practical Challenges

1. Run `top` during normal system use. Identify the top CPU-consuming process and explain whether its usage is expected.
2. Run `htop` and sort by memory usage. Compare the top memory process with the output of `ps aux --sort=-%mem`.
3. Use `free -h` to record total, used, free, buff/cache, available, and swap usage. Explain why `available` is more useful than `free`.
4. Run `vmstat 1` during normal use and during a CPU stress test. Compare `r`, `us`, `sy`, `id`, and `wa`.
5. Simulate memory pressure with `stress-ng` and observe `free -h` and `vmstat 1`.
6. Simulate disk I/O pressure with `fio` and observe `iostat -xz 1` and `iotop`.
7. Use `df -h` and `du` to identify the largest directories on a test filesystem.
8. Create a disk usage alert script that warns when `/` is above 80% usage.
9. Create a cron job that records uptime, memory, disk space, and top processes every hour.
10. Write a short performance report for one simulated bottleneck. Include the command used to simulate it, tool output, interpretation, and recommended fix.
