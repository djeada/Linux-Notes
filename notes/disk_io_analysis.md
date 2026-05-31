## Disk I/O Analysis and Performance Monitoring

Disk I/O analysis is the process of observing how data is read from and written to storage devices.

Disk I/O matters because many applications depend heavily on storage performance. Databases, file servers, virtual machines, build systems, backup jobs, logging systems, and data-processing workloads can all slow down if the disk cannot keep up.

A system can have plenty of CPU and memory but still feel slow if processes are waiting for disk reads or writes to finish.

In simple terms:

```text id="rp4mq9"
Disk I/O bottleneck = the system is waiting too long for storage
```

Common symptoms include:

- applications respond slowly
- commands hang while reading or writing files
- high load average with low CPU usage
- high iowait percentage
- long disk queues
- slow database queries
- slow file copies
- processes stuck in D state

Disk I/O analysis helps answer questions like:

- Is the disk busy?
- Which process is using the disk?
- Is the workload read-heavy or write-heavy?
- Is the workload sequential or random?
- Are requests waiting in a queue?
- Is latency high?
- Is the storage device saturated?

### How Disk I/O Works

When an application reads or writes data, the request passes through several layers before reaching the physical storage device.

```text id="ozkd4y"
+--------------------+
|    Application     |
+--------------------+
          |
          v
+--------------------+
|  File System API   |
| read(), write()    |
+--------------------+
          |
          v
+--------------------+
|    File System     |
|  ext4, xfs, btrfs  |
+--------------------+
          |
          v
+--------------------+
|   Block Device     |
| /dev/sda, nvme0n1  |
+--------------------+
          |
          v
+--------------------+
|    Disk Driver     |
+--------------------+
          |
          v
+--------------------+
| Physical Storage   |
| HDD, SSD, NVMe     |
+--------------------+
```

- The application asks for data using system calls such as `read()` or `write()`.
- The filesystem translates file-level operations into block-level operations.
- The block device layer sends requests to the storage device.
- The disk driver communicates with the hardware.
- Finally, the physical storage device reads or writes the data.

### Read Operations

A read operation happens when an application requests data from storage.

```text id="pp0emh"
Application asks for data
        |
        v
Kernel checks page cache
        |
        +--> If data is cached, return it from RAM
        |
        +--> If data is not cached, read from disk
                         |
                         v
              Data is returned to application
```

- A read may be fast if the data is already in memory.
- A read may be slow if the system must fetch the data from disk.
- This is why repeated reads of the same file often become faster: the data may be cached in RAM.

### Write Operations

A write operation happens when an application sends data to be stored.

```text id="b4jd8m"
Application writes data
        |
        v
Kernel stores data in memory buffer
        |
        v
Data is written to disk now or later
        |
        v
Application receives confirmation
```

Linux often caches and buffers writes for performance. This means an application may finish writing before the data is physically committed to storage.

This improves speed but also means that sudden power loss or device removal can risk data loss if writes have not been flushed.

The `sync` command can force cached writes to be flushed:

```bash id="suqr1w"
sync
```

### Important Disk I/O Concepts

Disk I/O performance is usually described using a few important metrics.

| Metric          | Description                                 |
| --------------- | ------------------------------------------- |
| **Latency**     | How long one I/O request takes              |
| **Throughput**  | How much data is transferred per second     |
| **IOPS**        | Input/output operations per second          |
| **Queue depth** | How many I/O requests are waiting or active |
| **Utilization** | How busy the device is                      |
| **iowait**      | CPU idle time while waiting for I/O         |

### Latency

Latency is the delay for an I/O operation to complete.

For example, if a program asks the disk for a small file and waits 20 milliseconds, the read latency is about 20 ms.

Low latency is important for:

- databases
- interactive applications
- virtual machines
- small random reads and writes
- metadata-heavy workloads

High latency often makes systems feel slow, even if total throughput is not very high.

### Throughput

Throughput is the amount of data transferred per second.

It is usually measured in:

```text id="l43tog"
KB/s
MB/s
GB/s
```

High throughput is important for:

- copying large files
- backups
- video processing
- scientific data processing
- large sequential reads and writes

A disk can have good throughput but poor latency, or good latency but limited throughput. The workload determines which metric matters most.

### IOPS

IOPS means Input/Output Operations Per Second.

This measures how many individual read or write operations the storage system can handle per second.

IOPS is especially important for random workloads.

Examples:

- database transactions
- many small files
- mail servers
- virtual machine disks
- container storage

An HDD may handle sequential reads reasonably well but perform poorly with random I/O because the mechanical disk head must move around.

SSDs and NVMe drives handle random I/O much better because they have no moving parts.

### Queue Depth

Queue depth is the number of I/O requests waiting or being processed.

A short queue usually means the storage device is keeping up.

A long queue often means requests are arriving faster than the disk can complete them.

```text id="z75epk"
Application requests
        |
        v
+----------------------+
| Disk I/O Queue       |
| req1 req2 req3 req4  |
+----------------------+
        |
        v
Storage device processes requests
```

If the queue keeps growing, users may experience slow response times.

### I/O Wait

I/O wait is the percentage of time the CPU is idle while waiting for I/O to complete.

In tools such as `top`, `vmstat`, and `iostat`, I/O wait often appears as:

```text id="s6lxvk"
wa
```

or:

```text id="jerhnm"
%iowait
```

High I/O wait can mean the CPU has work to do but cannot continue because it is waiting for storage.

However, I/O wait must be interpreted carefully. A low iowait value does not always mean disk performance is good, especially on systems with many CPU cores.

### Sequential vs Random I/O

Sequential I/O reads or writes data in order.

Example:

```text id="pw4cje"
read block 1
read block 2
read block 3
read block 4
```

Sequential I/O is common when copying large files, streaming video, or writing large backups.

Random I/O jumps around the disk.

Example:

```text id="r0d8vd"
read block 900
read block 12
read block 4501
read block 33
```

Random I/O is common in databases, virtual machines, and workloads with many small files.

HDDs are much slower at random I/O because the disk head must physically move. SSDs and NVMe drives are much better at random I/O.

### HDD, SSD, and NVMe Performance

Different storage technologies behave differently.

HDD:

- mechanical
- slower random access
- higher latency
- cheaper per GB
- good for large capacity storage

SSD:

- no moving parts
- faster latency
- better random I/O
- more expensive per GB than HDD

NVMe:

- SSD technology over PCIe
- very high throughput
- very low latency
- excellent for demanding workloads

A workload that performs badly on an HDD may perform much better on SSD or NVMe storage.

### Disk Scheduling

The Linux kernel uses I/O schedulers to decide how disk requests are ordered.

The scheduler can affect latency, fairness, and throughput.

Older scheduler names include:

- CFQ
- Deadline
- Noop

Newer systems may use schedulers such as:

- mq-deadline
- kyber
- bfq
- none

The available schedulers depend on the kernel and storage device.

To see the scheduler for a device:

```bash id="zbfz5f"
cat /sys/block/sda/queue/scheduler
```

Example output:

```text id="kqzda1"
[mq-deadline] kyber bfq none
```

The scheduler in brackets is currently active.

To temporarily change the scheduler:

```bash id="u0zwy8"
echo bfq | sudo tee /sys/block/sda/queue/scheduler
```

This change is temporary and may reset after reboot.

### Elevator Algorithm

One classic way to understand disk scheduling is the elevator algorithm.

The disk head moves in one direction, servicing requests along the way, then reverses direction.

```text id="gem2h3"
Cylinder Positions:
0---|---|---|---|---|---|---|---|---|---|---|
    2   10      20 22       35    40

Requests: 10, 22, 20, 35, 2, 40

Disk arm starts at 20 and moves upward:

1. Service 20
2. Service 22
3. Service 35
4. Service 40
5. Reverse direction
6. Service 10
7. Service 2
```

This reduces unnecessary disk head movement compared to simply handling every request in arrival order.

This matters more for HDDs than SSDs because HDDs have mechanical seek time.

### Useful Disk I/O Tools

Linux has many tools for monitoring disk I/O.

| Tool         | Description                                  |
| ------------ | -------------------------------------------- |
| **iostat**   | Device-level I/O statistics                  |
| **vmstat**   | CPU, memory, process, and block I/O overview |
| **iotop**    | Per-process live I/O usage                   |
| **pidstat**  | Per-process I/O over time                    |
| **sar**      | Historical system activity reports           |
| **dstat**    | Combined live system statistics              |
| **fio**      | Generate controlled I/O workloads            |
| **blktrace** | Detailed block layer tracing                 |
| **perf**     | Performance event tracing                    |

The most useful beginner tools are:

- iostat
- vmstat
- iotop
- pidstat
- fio

### Installing Common Tools

On Debian or Ubuntu:

```bash id="gg160j"
sudo apt update
sudo apt install sysstat iotop fio
```

On Red Hat, CentOS, or Fedora:

```bash id="wucd21"
sudo dnf install sysstat iotop fio
```

or on older systems:

```bash id="dqw9g1"
sudo yum install sysstat iotop fio
```

The `sysstat` package provides tools such as:

- iostat
- pidstat
- sar

### Using `iostat`

`iostat` shows CPU and disk I/O statistics.

A common command is:

```bash id="n7m4eq"
iostat -xz 1
```

This shows extended disk statistics every second.

Important columns include:

| Metric     | Description                   |
| ---------- | ----------------------------- |
| **r/s**    | Reads per second              |
| **w/s**    | Writes per second             |
| **rkB/s**  | Kilobytes read per second     |
| **wkB/s**  | Kilobytes written per second  |
| **await**  | Average time for I/O requests |
| **aqu-sz** | Average queue size            |
| **%util**  | How busy the device is        |

Example output:

```text id="lg6anb"
Device            r/s     w/s     rkB/s    wkB/s   await  aqu-sz  %util
sda              2.00  950.00     80.0  98000.0   45.20   12.40  99.80
```

Interpretation:

| Observation           | Meaning                               |
| --------------------- | ------------------------------------- |
| **w/s is high**       | Many writes are happening             |
| **wkB/s is high**     | Large amount of data is being written |
| **await is 45.20 ms** | Requests are taking noticeable time   |
| **aqu-sz is 12.40**   | Queue is building                     |
| **%util is 99.80**    | Disk is almost fully busy             |

This suggests the disk is saturated by write activity.

### Using `vmstat`

`vmstat` gives a broad system overview.

Run:

```bash id="d2mz0b"
vmstat 1
```

Important columns include:

| Field  | Description                       |
| ------ | --------------------------------- |
| **r**  | Runnable processes                |
| **b**  | Blocked processes                 |
| **bi** | Blocks received from block device |
| **bo** | Blocks sent to block device       |
| **us** | User CPU time                     |
| **sy** | System CPU time                   |
| **id** | Idle CPU time                     |
| **wa** | I/O wait time                     |

Example output:

```text id="p9rruc"
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  8      0 300000  20000 900000    0    0    10 85000 2000 4000  3  4 20 73  0
```

Interpretation:

```text id="a23fud"
b = 8       eight processes are blocked, likely waiting for I/O
bo = 85000  many blocks are being written
wa = 73     CPU is spending much time waiting on I/O
```

This strongly suggests disk I/O pressure.

### Using `iotop`

`iotop` shows per-process disk I/O usage.

Run:

```bash id="ahh0ae"
sudo iotop -o
```

The `-o` option shows only processes currently doing I/O.

Example output:

```text id="k79z09"
Total DISK READ: 0.00 B/s | Total DISK WRITE: 115.42 M/s
TID  PRIO  USER  DISK READ  DISK WRITE  SWAPIN  IO>  COMMAND
2451 be/4  user    0.00 B/s  112.00 M/s  0.00 % 89%  fio --name=write-test
```

Interpretation:

```text id="bamxxg"
fio is writing heavily
IO> is high
this process is likely responsible for disk pressure
```

`iotop` is one of the easiest tools for answering:

```text id="hmsxrp"
Which process is using the disk right now?
```

### Using `pidstat`

`pidstat` can show disk I/O per process over time.

Run:

```bash id="ku0gut"
pidstat -d 1
```

Example output:

```text id="tbh976"
Linux 6.x (host)     05/31/2026

12:00:01 UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command
12:00:02 1000     2451      0.00  98000.00      0.00     120  fio
```

Interpretation:

- PID 2451 is writing about 98 MB/s
- iodelay is increasing
- fio is a major disk writer

`pidstat -d` is useful when you want per-process disk activity but do not want a full-screen interactive tool.

### Using `sar`

`sar` records and reports historical system activity.

To view disk statistics every second for five samples:

```bash id="uvcjon"
sar -d 1 5
```

Example output:

```text id="cbppz1"
12:00:01 DEV       tps   rkB/s    wkB/s   await  %util
12:00:02 sda    950.00    0.00 98000.00   44.50  99.40
```

Interpretation:

```text id="ck72mg"
sda is almost fully utilized
writes dominate
average wait time is high
```

`sar` is especially useful for answering:

```text id="n24o9j"
Was the disk busy earlier, when the problem happened?
```

### Using `fio`

`fio` is a flexible I/O workload generator.

It can simulate:

- sequential reads
- sequential writes
- random reads
- random writes
- mixed read/write workloads
- database-like workloads
- high queue depth workloads
- latency-sensitive workloads

Important warning:

- Only run fio against test files or safe scratch space.
- Do not run destructive tests on important disks.
- Avoid using raw devices unless you know exactly what you are doing.

A safe test usually writes to a regular file in a test directory.

Example:

```bash id="h6dswq"
mkdir -p ~/fio-test
```

### Scenario 1: Simulate a Sequential Write Bottleneck

This scenario simulates a large write-heavy workload, such as backups, log generation, file copying, or data export.

#### Goal

Create heavy sequential writes and observe disk saturation.

#### Simulate the Bottleneck

Run this in one terminal:

```bash id="uambj8"
mkdir -p ~/fio-test

fio --name=seq-write-test \
    --directory=~/fio-test \
    --size=2G \
    --rw=write \
    --bs=1M \
    --numjobs=1 \
    --iodepth=16 \
    --direct=1 \
    --runtime=60 \
    --time_based \
    --group_reporting
```

What this does:

```text id="evpi59"
--rw=write       sequential write workload
--bs=1M          writes in large 1 MB blocks
--iodepth=16     allows multiple outstanding requests
--direct=1       bypasses page cache
--runtime=60     runs for 60 seconds
```

#### Check with `iostat`

In another terminal, run:

```bash id="j1jdm2"
iostat -xz 1
```

Example output:

```text id="iyfqb8"
Device            r/s     w/s     rkB/s     wkB/s   await  aqu-sz  %util
sda              0.00  420.00      0.00  420000.0   38.10   14.20  99.90
```

Interpretation

- wkB/s is very high
- %util is close to 100%
- await is elevated
- aqu-sz is high

This means the disk is busy handling sequential writes and may be saturated.

If applications are slow during this test, the disk is likely the bottleneck.

#### Check with `iotop`

Run:

```bash id="jvx6ic"
sudo iotop -o
```

Example output:

```text id="uawts0"
Total DISK WRITE: 410.00 M/s
TID  PRIO USER DISK READ DISK WRITE IO> COMMAND
3124 be/4 user 0.00 B/s  408.00 M/s 95% fio --name=seq-write-test
```

Interpretation:

- fio is the process generating the write pressure
- IO> is very high
- the bottleneck is caused by heavy writes

### Scenario 2: Simulate a Random Read Bottleneck

This scenario simulates workloads such as databases, virtual machines, or many small-file reads.

#### Goal

Generate random reads and observe latency and IOPS behavior.

#### Prepare a Test File

First create a file:

```bash id="ibanjx"
mkdir -p ~/fio-test

fio --name=prepare-file \
    --directory=~/fio-test \
    --size=2G \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --numjobs=1
```

#### Simulate Random Reads

Run:

```bash id="cqbn7v"
fio --name=random-read-test \
    --directory=~/fio-test \
    --filename=randomfile \
    --size=2G \
    --rw=randread \
    --bs=4k \
    --numjobs=4 \
    --iodepth=32 \
    --direct=1 \
    --runtime=60 \
    --time_based \
    --group_reporting
```

What this does:

```text id="e0q1vh"
--rw=randread    random read workload
--bs=4k          small 4 KB reads
--numjobs=4      four worker jobs
--iodepth=32     many outstanding requests
```

#### Check with `iostat`

```bash id="unj1kr"
iostat -xz 1
```

Example output:

```text id="mkwoaw"
Device            r/s     w/s    rkB/s   wkB/s  await  aqu-sz  %util
sda           5800.00    0.00 23200.0    0.00   22.80   31.50  99.60
```

Interpretation:

| Observation           | Meaning                          |
| --------------------- | -------------------------------- |
| **r/s is high**       | Many read operations per second  |
| **rkB/s is moderate** | Small reads, not huge throughput |
| **await is high**     | Reads are taking time            |
| **aqu-sz is high**    | Queue is building                |
| **%util is near 100** | Device is saturated              |

This is typical of random I/O bottlenecks.

On an HDD, this workload may perform very poorly. On an SSD or NVMe drive, it should perform much better.

### Scenario 3: Simulate a Random Write Bottleneck

Random writes are common in databases, logs, virtual machines, and metadata-heavy workloads.

#### Goal

Generate small random writes and observe queueing and latency.

#### Simulate the Bottleneck

```bash id="g3u2jm"
fio --name=random-write-test \
    --directory=~/fio-test \
    --size=2G \
    --rw=randwrite \
    --bs=4k \
    --numjobs=4 \
    --iodepth=32 \
    --direct=1 \
    --runtime=60 \
    --time_based \
    --group_reporting
```

#### Check with `vmstat`

Run:

```bash id="l6swii"
vmstat 1
```

Example output:

```text id="j0ry5k"
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2 10      0 200000  40000 800000    0    0     0 72000 3500 7000  5  8 15 72  0
```

Interpretation

| Observation    | Meaning                |
| -------------- | ---------------------- |
| **b = 10**     | Many blocked processes |
| **bo = 72000** | Heavy block output     |
| **wa = 72**    | High I/O wait          |

This indicates that processes are waiting on disk writes.

#### Check with `pidstat`

```bash id="ffu7ij"
pidstat -d 1
```

Example output:

```text id="o9q8ay"
12:10:01 UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command
12:10:02 1000     3381      0.00  71000.00      0.00     300  fio
```

Interpretation:

- fio is writing heavily
- iodelay is high
- this process is contributing to disk wait

### Scenario 4: Simulate High I/O Wait

High I/O wait appears when the CPU is idle but the system has pending disk operations.

#### Goal

Create enough disk pressure that CPU time shifts into I/O wait.

#### Simulate the Bottleneck

Use a random read/write workload:

```bash id="ka4k15"
fio --name=high-iowait-test \
    --directory=~/fio-test \
    --size=2G \
    --rw=randrw \
    --rwmixread=50 \
    --bs=4k \
    --numjobs=8 \
    --iodepth=64 \
    --direct=1 \
    --runtime=60 \
    --time_based \
    --group_reporting
```

#### Check with `top`

Run:

```bash id="szn0mp"
top
```

Look at the CPU line near the top.

Example:

```text id="snlpea"
%Cpu(s):  3.0 us,  6.0 sy,  0.0 ni, 18.0 id, 72.0 wa,  0.0 hi,  1.0 si,  0.0 st
```

Interpretation:

- us = user CPU time
- sy = system CPU time
- id = idle CPU time
- wa = I/O wait

Here:

```text id="xfzdwp"
wa = 72.0
```

This means the CPU is spending a large amount of time waiting for I/O.

Important note:

- top shows iowait as a CPU-level metric.
- It does not reliably show per-process iowait.
- Use iotop or pidstat -d to identify the responsible process.

#### Confirm with `iostat`

```bash id="pmgx4j"
iostat -xz 1
```

Example:

```text id="q88htk"
Device            r/s     w/s    rkB/s    wkB/s   await  aqu-sz  %util
sda           3200.00 3100.00 12800.0 12400.0   55.30   45.00 100.00
```

Interpretation:

- mixed reads and writes are active
- await is high
- queue size is high
- disk utilization is 100%

This confirms storage saturation.

### Scenario 5: Simulate a Background Job Interfering with Foreground Work

This scenario shows how a background disk-heavy task can slow down normal work.

#### Goal

Run a heavy background write job, then observe how it affects another command.

#### Simulate the Background Job

Terminal 1:

```bash id="rtm98c"
fio --name=background-writer \
    --directory=~/fio-test \
    --size=4G \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --runtime=120 \
    --time_based
```

#### Run a Foreground Test

Terminal 2:

```bash id="mhj8w2"
time find /usr -type f > /tmp/file-list.txt
```

This command walks many files and writes output to `/tmp/file-list.txt`.

#### Check Disk Usage

Terminal 3:

```bash id="f61d8k"
sudo iotop -o
```

Example output:

```text id="s16z24"
TID  PRIO USER DISK READ DISK WRITE IO> COMMAND
4001 be/4 user 0.00 B/s  360.00 M/s 92% fio --name=background-writer
4050 be/4 user 4.00 M/s    2.00 M/s 35% find /usr -type f
```

Interpretation:

- fio is consuming most disk bandwidth
- find is also waiting on I/O
- foreground work may slow down because the disk is busy

#### Reduce Background Impact with `ionice`

Stop the fio job, then rerun it with idle I/O priority:

```bash id="shvt3n"
ionice -c3 fio --name=background-writer \
    --directory=~/fio-test \
    --size=4G \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --runtime=120 \
    --time_based
```

The `-c3` option means idle I/O class.

Interpretation:

- The background job should only receive disk time when other processes are not using the disk.
- This can reduce the impact on interactive or foreground workloads.

### Scenario 6: Simulate Slow Disk with I/O Throttling Using `ionice`

This scenario does not make the disk physically slower. Instead, it changes how aggressively a process competes for disk access.

#### Goal

Show how I/O priority affects competing disk workloads.

#### Run a Low-Priority Job

```bash id="lr9wkj"
ionice -c3 fio --name=idle-writer \
    --directory=~/fio-test \
    --size=2G \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --runtime=60 \
    --time_based
```

#### Run a Normal Job at the Same Time

In another terminal:

```bash id="j3illq"
fio --name=normal-reader \
    --directory=~/fio-test \
    --size=2G \
    --rw=read \
    --bs=1M \
    --direct=1 \
    --runtime=60 \
    --time_based
```

#### Check with `iotop`

```bash id="xxbwla"
sudo iotop -o
```

Example output:

```text id="xxyd7b"
TID  PRIO USER DISK READ DISK WRITE IO> COMMAND
5102 be/4 user 300.00 M/s 0.00 B/s 40% fio --name=normal-reader
5088 idle user 0.00 B/s  40.00 M/s 15% fio --name=idle-writer
```

Interpretation:

- normal-reader receives more disk service
- idle-writer runs only when disk has spare capacity
- ionice can make background jobs less disruptive

### Scenario 7: Simulate Cache Effects

Linux uses RAM as page cache. This can make repeated reads much faster.

#### Goal

Show the difference between cached and uncached reads.

#### Create a Test File

```bash id="hp4rva"
dd if=/dev/zero of=~/fio-test/cache-test.img bs=1M count=1024 status=progress
```

#### First Read

```bash id="ces8gt"
time cat ~/fio-test/cache-test.img > /dev/null
```

#### Second Read

Run it again:

```bash id="b6nbee"
time cat ~/fio-test/cache-test.img > /dev/null
```

Example output:

```text id="kgvrxx"
First read:
real    0m4.800s

Second read:
real    0m0.420s
```

Interpretation:

- The second read is faster because the file was cached in RAM.
- This does not necessarily mean the disk became faster.
- It means Linux avoided reading from disk again.

#### Drop Cache for Testing

For lab testing only:

```bash id="xsny68"
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches
```

Then repeat the read.

Warning:

```text id="pz9jx4"
Do not drop caches on production systems just to test performance.
It can temporarily reduce performance for running workloads.
```

### Scenario 8: Simulate Many Small Files

Many small files can create metadata pressure. This affects build systems, package managers, source trees, and mail directories.

#### Goal

Create many small files and observe metadata-heavy I/O.

#### Simulate the Workload

```bash id="d5svkh"
mkdir -p ~/small-files-test

for i in $(seq 1 50000); do
    echo "test $i" > ~/small-files-test/file_$i.txt
done
```

#### Check with `iostat`

```bash id="nnjbnk"
iostat -xz 1
```

Example output:

```text id="teozxk"
Device            r/s     w/s    rkB/s    wkB/s  await  aqu-sz  %util
sda             20.00 1800.00   500.0  9000.0   18.40    8.20  88.00
```

Interpretation:

- w/s is high
- throughput is not extremely high
- many small writes are happening
- metadata operations may be significant

This is different from large sequential writes. The disk is handling many small operations rather than a few large transfers.

#### Clean Up

```bash id="yputh1"
rm -rf ~/small-files-test
```

### Scenario 9: Simulate Swap-Related Disk Pressure

When a system runs out of RAM, it may use swap. Heavy swapping can create severe disk I/O pressure.

#### Goal

Observe how memory pressure can become disk pressure.

#### Safer Simulation Method

Use `stress-ng` if available:

```bash id="l356e6"
sudo apt install stress-ng
```

Then run a memory stress test carefully:

```bash id="o7wkm4"
stress-ng --vm 2 --vm-bytes 70% --timeout 60s
```

#### Check with `vmstat`

```bash id="kpgv11"
vmstat 1
```

Example output:

```text id="eu391a"
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  4 900000  50000  10000 120000 1200 1800  8000 12000 4000 8000 20 15 40 25  0
```

#### Interpretation

```text id="vl7ot4"
si is high    swap-in activity
so is high    swap-out activity
wa is high    CPU waits on disk
system may feel very slow
```

If swap activity is high, the problem may not be the disk itself. The root cause may be memory pressure.

### Process States and Disk I/O

Linux processes can enter different states.

A process waiting on disk I/O may enter uninterruptible sleep, shown as:

```text id="whm62i"
D
```

This is often called D state.

To look for processes in D state:

```bash id="hrbs7y"
ps -eo pid,stat,comm,wchan:30 | awk '$2 ~ /D/ {print}'
```

Example output:

```text id="zejyxu"
PID   STAT COMMAND         WCHAN
5678  D    myapp           wait_on_page_bit_common
```

Interpretation:

```text id="mr3nec"
The process is blocked in uninterruptible sleep.
It may be waiting for disk, filesystem, or storage-related I/O.
```

Important:

```text id="hxj31z"
A few short-lived D-state processes can be normal.
Many processes stuck in D state for a long time may indicate an I/O bottleneck or storage problem.
```

### I/O Priority with `ionice`

`ionice` controls a process’s I/O scheduling priority.

There are three main classes:

```text id="kvlkj5"
-c1   real-time
-c2   best-effort
-c3   idle
```

Best-effort has priority levels from 0 to 7:

```text id="xahna5"
0 = highest priority
7 = lowest priority
```

Example: set an existing process to best-effort priority 0:

```bash id="lu4euf"
sudo ionice -c2 -n0 -p 5678
```

Example: run a backup job with idle priority:

```bash id="q8q2ne"
ionice -c3 rsync -a /data/ /backup/
```

Interpretation:

```text id="atwp5c"
Use idle priority for background tasks.
Avoid real-time I/O priority unless absolutely necessary.
Real-time I/O can starve other processes.
```

### Filesystem Choices

Different filesystems have different strengths.

```text id="ux66no"
ext4:
- common general-purpose Linux filesystem
- stable and widely supported
- good default choice

XFS:
- strong performance with large files and parallel I/O
- common on servers
- good for large storage volumes

Btrfs:
- supports snapshots, checksums, compression, and pooling
- useful for advanced storage features
- may require more understanding and operational care
```

The filesystem alone rarely fixes a bad workload, but it can affect performance, reliability, and manageability.

### Mount Options for I/O Performance

Mount options can affect disk behavior.

Common options include:

```text id="k9ig3x"
noatime
relatime
data=writeback
discard
```

#### `noatime`

The `noatime` option disables access-time updates when files are read.

Example `/etc/fstab` option:

```text id="caf61n"
UUID=xxxx  /data  ext4  defaults,noatime  0  2
```

Benefit:

```text id="m1dum6"
Reduces small metadata writes caused by file reads.
```

#### `data=writeback`

This ext4 option may improve performance but can reduce data safety after crashes.

Use carefully.

```text id="pl84fg"
Higher performance
Higher risk during crashes
```

#### `discard`

The `discard` option enables online TRIM for SSDs.

However, many systems prefer periodic TRIM using:

```bash id="p7gpjo"
systemctl status fstrim.timer
```

Periodic TRIM is often less disruptive than continuous discard.

### RAID and Disk I/O

RAID can affect performance and reliability.

```text id="hwxxby"
RAID 0:
- stripes data across disks
- improves performance
- no redundancy

RAID 1:
- mirrors data
- improves redundancy
- read performance may improve
- write performance often similar to one disk

RAID 5/6:
- uses parity
- provides redundancy
- write performance can suffer due to parity overhead

RAID 10:
- combines striping and mirroring
- good performance and redundancy
- requires more disks
```

RAID is not a backup. It protects against some disk failures, but it does not protect against accidental deletion, corruption, ransomware, or disasters.

### Bottleneck Interpretation Guide

When checking disk I/O, use several metrics together.

#### High `%util`

Example:

```text id="g82n78"
%util = 99%
```

Possible meaning:

```text id="kff2xw"
The disk is very busy.
It may be saturated.
```

But on modern fast devices, `%util` can be less clear because devices may process many requests in parallel.

#### High `await`

Example:

```text id="rhdzw4"
await = 80 ms
```

Possible meaning:

```text id="q5kjlv"
I/O requests are taking a long time.
Applications may feel slow.
```

#### High `aqu-sz`

Example:

```text id="jln9g6"
aqu-sz = 30
```

Possible meaning:

```text id="y5xl2k"
The I/O queue is building.
Requests are waiting.
```

#### High `wa`

Example:

```text id="u1ox9e"
wa = 70%
```

Possible meaning:

```text id="qdldbx"
CPU is often idle while waiting for I/O.
The workload may be storage-bound.
```

#### High `r/s` or `w/s` with Low Throughput

Example:

```text id="o0oh5g"
r/s = 5000
rkB/s = 20000
```

Possible meaning:

```text id="bk58bd"
Many small reads are happening.
This may be random I/O.
```

#### High Throughput with Moderate IOPS

Example:

```text id="s725cp"
w/s = 200
wkB/s = 400000
```

Possible meaning:

```text id="ee2t8b"
Large sequential writes are happening.
This may be backups, copying, streaming, or export jobs.
```

### Practical Troubleshooting Workflow

When a system feels slow and disk I/O may be involved, follow a structured process.

```text id="cvmie5"
1. Check overall system load
2. Check CPU iowait
3. Check disk utilization and latency
4. Identify the process causing I/O
5. Determine workload type
6. Check for memory pressure and swapping
7. Check filesystem or disk errors
8. Decide on mitigation
```

### Step 1: Check Overall System Load

Use:

```bash id="sxm1pk"
uptime
```

Example:

```text id="l6htth"
12:00:00 up 3 days,  load average: 12.50, 10.20, 8.70
```

High load with low CPU usage may suggest processes are blocked on I/O.

### Step 2: Check CPU I/O Wait

Use:

```bash id="e0tsdd"
top
```

Look at:

```text id="v2sczs"
wa
```

Example:

```text id="gt98uh"
%Cpu(s):  2.0 us,  5.0 sy, 20.0 id, 73.0 wa
```

High `wa` suggests the system is waiting on I/O.

### Step 3: Check Disk-Level Metrics

Use:

```bash id="ohl3hu"
iostat -xz 1
```

Look for:

```text id="nft1d2"
high %util
high await
high aqu-sz
high read or write rates
```

### Step 4: Identify the Process

Use:

```bash id="pvvcar"
sudo iotop -o
```

or:

```bash id="ihgt9q"
pidstat -d 1
```

This helps identify which process is producing disk activity.

### Step 5: Determine the Workload Type

Use `iostat` to compare operations and throughput.

```text id="c75pq3"
High IOPS + low throughput:
    random small I/O

Low IOPS + high throughput:
    large sequential I/O

High writes:
    backups, logs, database writes, copying

High reads:
    scans, queries, file serving, cache misses
```

### Step 6: Check Memory and Swap

Use:

```bash id="hl89h9"
free -h
vmstat 1
```

If `si` and `so` are high in `vmstat`, the system is swapping.

This means the disk problem may be caused by memory shortage.

### Step 7: Check Disk Errors

Use:

```bash id="m8yn52"
dmesg | grep -iE 'error|fail|reset|timeout|I/O'
```

Example warning signs:

```text id="zjgr9r"
I/O error
buffer I/O error
reset SuperSpeed USB device
blk_update_request
ata timeout
nvme timeout
```

Disk errors can cause severe latency and should be investigated quickly.

### Step 8: Mitigate the Bottleneck

Possible fixes depend on the cause.

* If a background job is too aggressive: use `ionice`, `nice`, scheduling, or rate limits
* If memory pressure causes swapping: reduce memory usage or add RAM
* If random I/O is too high: add caching, optimize queries, or use SSD/NVMe
* If sequential throughput is too low: improve storage bandwidth or distribute workload
* If the disk is failing: replace hardware and restore from backup
* If many services share one disk: separate workloads across disks

### Common Disk I/O Problems and Fixes

#### Problem: Backup Job Slows Everything Down

Symptoms:

* High writes
* High `iowait`
* Foreground apps feel slow
* `iotop` shows `rsync`, `tar`, backup agent, or `fio`

Fixes:

* Run backups during off-hours
* Use `ionice -c3`
* Limit bandwidth if supported
* Write backups to a separate disk

Example:

```bash id="kl2zjj"
ionice -c3 rsync -a /data/ /backup/
```

#### Problem: Database Has High Latency

Symptoms:

* High random reads/writes
* High `await`
* High queue depth
* Database process appears in `iotop` or `pidstat`

Fixes:

* Add RAM for cache
* Optimize queries
* Reduce unnecessary indexes or writes
* Move database to SSD/NVMe
* Separate logs and data files

#### Problem: System Is Swapping

Symptoms:

* `vmstat` shows high `si` and `so`
* Disk busy even with no obvious file workload
* System becomes extremely slow

Fixes:

* Reduce memory pressure
* Stop memory-heavy processes
* Add RAM
* Adjust application memory limits
* Review `swappiness` carefully

#### Problem: Many Small Files Are Slow

Symptoms:

* High IOPS
* Low throughput
* Metadata-heavy workload
* Builds or package installs are slow

Fixes:

* Use SSD/NVMe
* Reduce file count where possible
* Use caching
* Avoid unnecessary filesystem scans
* Choose a suitable filesystem

### Challenges

1. Research and describe the process of both read and write operations in the disk I/O pathway, starting from the application layer down to physical storage. Illustrate each layer involved, such as the file system, block device, disk driver, and physical storage, and explain the role of each in the process.
2. Use the `iostat` command to monitor disk I/O performance on your system. Record metrics such as read/write rates and I/O wait times over a period of five minutes. Analyze the results, and explain any spikes or patterns you observe in relation to the applications running on your system during this time.
3. Investigate the impact of storage types on disk I/O performance. Compare HDDs and SSDs by researching their read/write speeds, latency, and performance in random vs. sequential I/O operations. Summarize the key differences, and describe scenarios where each storage type would be most appropriate.
4. Use the `vmstat` command to track block I/O on your system. Record your observations and explain how the block I/O activity correlates with other system metrics, such as CPU usage and memory activity. Based on your findings, discuss any potential I/O bottlenecks that may affect system performance.
5. Research the concept of disk scheduling algorithms and examine at least two, such as First-Come, First-Served (FCFS) and the Elevator Algorithm (SCAN). Write a summary explaining how these algorithms prioritize disk requests, and consider how each might affect overall disk performance in different workloads.
6. Experiment with the `blktrace` command to monitor block I/O events on a specific disk (e.g., `/dev/sda`). Capture I/O activity for a few minutes, then analyze the data to identify trends or patterns. Discuss how such detailed I/O tracking can help diagnose complex disk performance issues.
7. Set up a simple benchmarking test using the `fio` tool to simulate disk I/O activity under various workloads, such as sequential and random reads/writes. Compare the results to observe how each workload affects the disk's performance, and explain what these differences reveal about disk behavior under different access patterns.
8. Monitor your system’s disk I/O using the `iotop` command to identify the processes consuming the most I/O resources. Record which processes are most active and evaluate how their activity impacts overall disk performance. Explain how monitoring active processes can aid in identifying performance bottlenecks.
9. Research I/O scheduling classes and priorities, such as idle, best-effort, and real-time, and use the `ionice` command to set these priorities for a particular process. Conduct a small experiment by setting different priorities for a test process and observing the impact on its performance relative to other processes. Summarize how I/O prioritization can be leveraged for optimizing disk access.
10. Use the `iostat` and `dstat` commands to collect baseline disk I/O performance data under normal system conditions. Record metrics such as average I/O wait times, queue lengths, and transfer rates over a period of time. Identify any recurring patterns and hypothesize potential causes, considering how this baseline data could inform system tuning or optimization efforts in the future.
