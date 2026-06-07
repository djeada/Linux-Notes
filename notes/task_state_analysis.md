## Task-State Analysis for Monitoring Application Processes
Task-state analysis is a way to understand what processes and threads are doing by looking at their runtime states.

Traditional monitoring often starts with resource usage:

- CPU usage
- memory usage
- disk I/O
- network usage
- load average

These are useful, but they do not always explain why an application is slow.

For example, an application may feel sluggish even when CPU usage is low. In that case, the problem may be that its threads are waiting on disk I/O, network I/O, locks, signals, or child processes.

Task-state analysis helps answer questions like:

- Are threads running on the CPU?
- Are they sleeping?
- Are they blocked on disk I/O?
- Are they stopped?
- Are zombie processes accumulating?
- Are many threads waiting instead of doing useful work?

The main idea is:

- Resource monitoring shows how busy the system is.
- Task-state analysis shows what processes and threads are actually doing.

### Processes and Threads

- A process is a running instance of a program.
- A thread is an execution path inside a process.
- A process can have one thread or many threads.

Threads inside the same process share resources such as memory, open files, and process-level settings.

```text id="m1j6vu"
+-------------------------------------+
|             Process A               |
|                                     |
|   +-----------+    +-----------+    |
|   | Thread 1  |    | Thread 2  |    |
|   +-----------+    +-----------+    |
|         |                |          |
|         +----------------+          |
|              Shared memory          |
|                                     |
+-------------------------------------+
```

Multi-threaded applications can do multiple things at the same time.

For example, a web server may have:

- one thread accepting connections
- several threads handling requests
- one thread writing logs
- one thread talking to a database

If many threads are waiting, users may experience slow responses even if CPU usage looks low.

### Task
In Linux, a “task” is the kernel’s schedulable unit.

A task may represent:

- a process
- a thread inside a process

This is why Linux tools often expose both:

- PID    process ID
- TID    thread ID

For a single-threaded process, the PID and TID are usually the same.

For a multi-threaded process, all threads share the same process ID, but each thread has its own thread ID.

### Why Task-State Analysis Matters
Task-state analysis is useful because resource usage alone can be misleading.

Example:

- CPU usage is low.
- Users say the app is slow.
- Load average is high.

This may mean the application is not CPU-bound. Instead, threads may be blocked on disk or waiting for locks.

Another example:

- CPU usage is high.
- Many threads are in R state.
- The run queue is growing.

This may indicate CPU saturation.

Task-state analysis helps separate different types of problems:

| Condition           | Typical Task State Pattern                                |
| ------------------- | --------------------------------------------------------- |
| CPU bottleneck      | Many tasks runnable or running (**R** state)              |
| I/O bottleneck      | Many tasks blocked in uninterruptible sleep (**D** state) |
| Idle waiting        | Many tasks sleeping (**S** state)                         |
| Stopped process     | Tasks in stopped/traced (**T** state)                     |
| Zombie accumulation | Tasks in zombie (**Z** state)                             |

### Common Linux Task States
Linux process and thread states are often shown as letters.

| State | Description           |
| ----- | --------------------- |
| **R** | Running or runnable   |
| **S** | Interruptible sleep   |
| **D** | Uninterruptible sleep |
| **T** | Stopped               |
| **Z** | Zombie                |

Some tools show extra letters after the main state.

For example:

- Ss
- R+
- Sl

The first letter is usually the most important state.

### `R`: Running or Runnable
`R` means the task is either currently running on a CPU or ready to run as soon as CPU time is available.

A task in `R` may be:

- actively executing
- waiting in the CPU run queue
- ready but not currently scheduled

A few `R` tasks are normal.

Many `R` tasks for a long time may suggest CPU pressure.

```text id="t7m1ni"
Many R tasks + high CPU usage + high run queue = possible CPU bottleneck
```

### `S`: Sleeping
`S` means interruptible sleep.

The task is waiting for something and can be woken up by a signal.

Common reasons for `S` state include:

- waiting for user input
- waiting for a network response
- waiting for a timer
- waiting for a lock
- waiting for a child process
- sleeping between work cycles

Most processes on a normal Linux system are usually in `S` state most of the time.

This is not automatically bad.

- Many S tasks can be normal.
- The important question is what they are waiting for.

### `D`: Uninterruptible Sleep
`D` means uninterruptible sleep.

A task in `D` state is usually waiting for a kernel-level operation to finish, often disk I/O or another low-level I/O operation.

Common causes include:

- slow disk
- stuck network filesystem
- storage timeout
- blocked device driver operation
- filesystem issue
- I/O congestion

A short-lived `D` state can be normal.

Many tasks stuck in `D` for a long time is a warning sign.

```text id="lhkwsc"
Many D tasks + high iowait + high disk latency = likely I/O bottleneck
```

Important note:

- D-state tasks often cannot be killed immediately.
- They usually leave D state only when the kernel operation finishes.

### `T`: Stopped
`T` means the task is stopped.

This can happen when:

- a user sends SIGSTOP
- a shell job is suspended with Ctrl+Z
- a debugger stops the process

A stopped process is not running. It stays paused until continued.

### `Z`: Zombie
`Z` means zombie.

A zombie process has finished execution, but its parent process has not yet collected its exit status.

A zombie is not using CPU or memory like a normal running process, but it still has an entry in the process table.

A few short-lived zombies are usually harmless.

Many persistent zombies may indicate that a parent process is broken.

```text id="k4b609"
Zombie = child finished, parent has not reaped it
```

### Viewing Process and Thread States with `ps`
A basic command to view process states is:

```bash id="z9uzvv"
ps -eo pid,stat,comm
```

Example output:

```text id="hvsjak"
  PID STAT COMMAND
    1 Ss   systemd
 1234 S    myprocess
 1300 R    python3
 1400 Z    old-worker
```

Interpretation:

- systemd is sleeping and is a session leader.
- myprocess is sleeping.
- python3 is running or runnable.
- old-worker is a zombie process.

To include threads, use:

```bash id="fr908r"
ps -eLo pid,tid,stat,comm
```

Example output:

```text id="ar8f10"
  PID   TID STAT COMMAND
 1234  1234 Sl   myprocess
 1234  1235 Rl   myprocess
 1234  1236 Sl   myprocess
```

Interpretation:

- Process 1234 has multiple threads.
- Thread 1235 is running or runnable.
- The other threads are sleeping.

### Viewing Threads for One Process
To inspect threads for a specific PID:

```bash id="vf2uhh"
ps -L -p 1234 -o pid,tid,stat,pcpu,pmem,comm
```

Example output:

```text id="bd6zt0"
  PID   TID STAT %CPU %MEM COMMAND
 1234  1234 Sl    0.0  1.2 myprocess
 1234  1235 Rl   95.0  1.2 myprocess
 1234  1236 Sl    0.0  1.2 myprocess
```

Interpretation:

- Thread 1235 is consuming CPU.
- The process is multi-threaded.
- Only one thread appears CPU-heavy in this sample.

### Using `/proc` for Task-State Analysis
The `/proc` filesystem exposes runtime information about processes.

For a process:

```text id="dwxt6l"
/proc/PID/
```

For threads inside a process:

```text id="oz791k"
/proc/PID/task/TID/
```

To view process status:

```bash id="x7t863"
cat /proc/1234/status
```

Example:

```text id="ecz8vy"
Name:   myprocess
State:  S (sleeping)
Tgid:   1234
Pid:    1234
Threads: 3
```

Interpretation:

- The process is sleeping.
- It has 3 threads.
- Tgid is the thread group ID, usually the main process ID.

### `/proc/PID/stat`
The file `/proc/PID/stat` contains many fields.

Example:

```bash id="pswxe4"
cat /proc/1234/stat
```

Example output:

```text id="b5djmm"
1234 (myprocess) S 1000 1234 1234 0 -1 4194560 ...
```

The third field is the state.

- 1234            PID
- (myprocess)     command name
- S               state

This means the process is sleeping.

For scripting, `/proc/PID/status` is usually easier to read than `/proc/PID/stat`.

### Counting Task States
A useful quick view is to count states across the system.

```bash id="r0oaag"
ps -eo state | sort | uniq -c
```

Example output:

```text id="zuvsx5"
  4 D
  8 R
230 S
  1 Z
```

Interpretation:

- Most tasks are sleeping.
- Eight tasks are runnable or running.
- Four tasks are in uninterruptible sleep.
- One zombie exists.

A few sleeping tasks are normal. Many `D` tasks deserve investigation.

To repeat every second:

```bash id="yeu1r6"
while true; do
    date
    ps -eo state | sort | uniq -c
    sleep 1
done
```

### Finding D-State Tasks
To show tasks in uninterruptible sleep:

```bash id="gagdm5"
ps -eo state,pid,cmd | awk '$1 ~ /^D/ {print}'
```

Example output:

```text id="xefz75"
D  5678  myprocess
D  6010  backup-worker
```

Interpretation:

- These processes are blocked in uninterruptible sleep.
- They may be waiting on disk, filesystem, or device I/O.

To include kernel wait channel:

```bash id="oztb4c"
ps -eo pid,stat,wchan:30,comm | awk '$2 ~ /^D/ {print}'
```

Example:

```text id="fyi48b"
  PID STAT WCHAN                          COMMAND
 5678 D    wait_on_page_bit_common        myprocess
 6010 D    io_schedule                    backup-worker
```

Interpretation:

- The wait channel gives a hint about what the task is waiting for.
- io_schedule and wait_on_page_bit_common often point toward I/O waits.

### `htop` for Interactive State Viewing
`htop` shows processes interactively.

Run:

```bash id="e2g07m"
htop
```

Useful actions:

- F5        tree view
- F4        filter
- F3        search
- F6        sort
- H         show or hide user threads
- K         show or hide kernel threads

In `htop`, look at the state column and CPU usage.

`htop` is useful when you want to interactively explore which process or thread is active.

### `top` for Thread View
To show threads in `top`, run:

```bash id="a3yomg"
top -H -p 1234
```

Meaning:

- -H      show threads
- -p      monitor a specific process ID

Example output:

```text id="ngsjra"
  PID USER  PR NI S %CPU %MEM TIME+ COMMAND
 1235 user  20  0 R 99.0  1.0 1:20.00 myprocess
 1236 user  20  0 S  0.0  1.0 0:00.10 myprocess
 1237 user  20  0 S  0.0  1.0 0:00.05 myprocess
```

Interpretation:

- Thread 1235 is CPU-bound.
- The other threads are sleeping.

### `perf top`
`perf` can show where CPU time is being spent.

Run:

```bash id="ostcfd"
sudo perf top
```

Example output:

```text id="kzjxfy"
Samples: 20K of event 'cycles'
Overhead  Shared Object      Symbol
  35.10%  myapp              [.] calculate_hash
  18.20%  libc.so            [.] memcpy
   9.50%  kernel             [k] schedule
```

Interpretation:

- The application spends much CPU time in calculate_hash.
- memcpy also consumes noticeable CPU.
- This helps identify CPU hotspots inside code.

`perf` is useful after task-state analysis suggests the application is CPU-bound.

### Combining Task States with Other Tools
Task states are most useful when combined with other metrics.

| Observation      | What to Check                                                           |
| ---------------- | ----------------------------------------------------------------------- |
| **Many R tasks** | Check CPU usage with `top`, `uptime`, `vmstat`, `perf`                  |
| **Many D tasks** | Check disk and I/O with `iostat`, `iotop`, `dmesg`                      |
| **Many S tasks** | Check locks, network issues, application logs, and database waits       |
| **Many Z tasks** | Check parent process behavior and whether it is reaping child processes |
| **Many T tasks** | Check signals, job control, and debugger activity                       |

Task-state analysis tells you where to look next.

### Scenario 1: Simulate CPU-Bound Threads in `R` State
#### Goal
Create CPU pressure and observe runnable/running tasks.

#### Simulate the Bottleneck
Install `stress-ng` if needed:

```bash id="qzomwh"
sudo apt install stress-ng
```

Run four CPU workers:

```bash id="vvhyqk"
stress-ng --cpu 4 --timeout 60s
```

#### Check with `top`
```bash id="mkgy1h"
top
```

Example output:

```text id="xm7u7j"
%Cpu(s): 96.0 us,  3.0 sy,  0.0 ni,  1.0 id,  0.0 wa

  PID USER      PR  NI S  %CPU COMMAND
 4101 user      20   0 R 399.0 stress-ng-cpu
```

#### Check Task States
```bash id="jtbzxp"
ps -eLo pid,tid,stat,comm | grep stress-ng
```

Example output:

```text id="dtlfe5"
 4101  4101 R    stress-ng-cpu
 4101  4102 R    stress-ng-cpu
 4101  4103 R    stress-ng-cpu
 4101  4104 R    stress-ng-cpu
```

#### Interpretation
- The stress-ng workers are in R state.
- CPU user time is high.
- Idle time is very low.
- This is a CPU-bound workload.

#### What This Means in a Real Application
If an application has many `R` threads and high CPU usage, it may be doing heavy computation or spinning in a loop.

Next tools:

```bash id="plrxyo"
top -H -p PID
sudo perf top
```

Possible fixes:

- optimize CPU-heavy code
- reduce worker count
- add CPU capacity
- use caching
- move heavy jobs to off-peak hours

### Scenario 2: Simulate Sleeping Tasks in `S` State
#### Goal
Show that sleeping tasks are often normal.

#### Simulate
Run:

```bash id="wapm6u"
sleep 300
```

In another terminal, find it:

```bash id="ycbrrc"
ps -eo pid,stat,comm | grep sleep
```

Example output:

```text id="g5ly8a"
 4200 S    sleep
```

#### Interpretation
- The process is sleeping while waiting for its timer to expire.
- This is normal.
- It is not consuming CPU.

#### Real Meaning
Many services spend much of their time sleeping because they are waiting for requests.

Examples:

- web server waiting for connections
- cron waiting for scheduled time
- daemon waiting for events
- application waiting for network response

Sleeping alone is not a bottleneck.

The question is whether the sleep is expected.

### Scenario 3: Simulate a Stopped Task in `T` State
#### Goal
Show what happens when a process is paused.

#### Simulate
Run a long sleep:

```bash id="o39wp2"
sleep 300
```

Find its PID:

```bash id="fm9y8s"
pgrep -n sleep
```

Example output:

```text id="l2yjcu"
4300
```

Stop it:

```bash id="v81ozo"
kill -STOP 4300
```

Check state:

```bash id="hg31wa"
ps -p 4300 -o pid,stat,comm
```

Example output:

```text id="ta2mhy"
  PID STAT COMMAND
 4300 T    sleep
```

#### Interpretation
- T means the process is stopped.
- It will not continue until it receives SIGCONT.

Continue it:

```bash id="rqk0o4"
kill -CONT 4300
```

Check again:

```bash id="y5iuc6"
ps -p 4300 -o pid,stat,comm
```

Example output:

```text id="awursy"
  PID STAT COMMAND
 4300 S    sleep
```

#### Real Meaning
A `T` state may appear when:

- a user presses Ctrl+Z
- a debugger pauses a process
- SIGSTOP is sent
- job control suspends the process

### Scenario 4: Simulate a Zombie Process in `Z` State
#### Goal
Create a safe zombie process and learn how to identify it.

#### Simulate with Python
Create a small script:

```bash id="mplue0"
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

```bash id="lugx2y"
python3 /tmp/make-zombie.py
```

In another terminal:

```bash id="aqb66m"
ps -eo pid,ppid,state,cmd | awk '$3 == "Z" {print}'
```

Example output:

```text id="y4iwcs"
 4451  4450 Z [python3] <defunct>
```

#### Interpretation
- The child process exited.
- The parent process has not collected its exit status.
- The zombie will disappear when the parent exits or reaps it.

#### Real Meaning
A few temporary zombies are not usually a problem.

Many persistent zombies may mean:

- the parent process is buggy
- the application is not handling child processes correctly
- a service supervisor is not reaping children

Fix the parent process rather than trying to kill the zombie directly.

### Scenario 5: Simulate Disk I/O Pressure and Look for `D` State
#### Goal
Generate disk pressure, then check for blocked tasks and disk wait.

`D` state is not always easy to reproduce safely because it depends on kernel-level I/O waits. A normal disk test may create high I/O wait without leaving many visible tasks stuck in `D`.

#### Simulate Disk Pressure
Install tools:

```bash id="qzixyz"
sudo apt install fio sysstat iotop
```

Run a random write workload:

```bash id="pn2wdg"
mkdir -p ~/task-state-lab

fio --name=randwrite-test \
    --directory=~/task-state-lab \
    --size=1G \
    --rw=randwrite \
    --bs=4k \
    --numjobs=4 \
    --iodepth=32 \
    --direct=1 \
    --runtime=60 \
    --time_based
```

#### Check Task States
```bash id="jkm7kl"
ps -eo pid,stat,wchan:30,comm | awk '$2 ~ /^D/ {print}'
```

Possible output:

```text id="s24b50"
 5012 D    io_schedule                    fio
```

Or there may be no output:

```text id="fhq6fb"
```

#### Interpretation
If output shows `D`:

- The process is blocked in uninterruptible sleep.
- The wait channel suggests it is waiting on I/O.

If there is no `D` output:

- The disk can still be busy.
- D state may be brief or not captured by the sample.
- Check disk metrics with iostat and vmstat.

#### Check with `iostat`
```bash id="al2o4q"
iostat -xz 1
```

Example output:

```text id="vmvpvm"
Device            r/s     w/s    rkB/s    wkB/s   await  aqu-sz  %util
sda              0.00  5200.00    0.00  20800.0   48.30   25.60  99.90
```

#### Interpretation
- w/s is high.
- await is high.
- aqu-sz is high.
- %util is almost 100%.
- The disk is saturated even if D-state sampling does not always catch it.

#### Check with `vmstat`
```bash id="dqco3x"
vmstat 1
```

Example output:

```text id="nzrsx2"
r  b   swpd   free   buff  cache   si   so    bi    bo   in    cs us sy id wa st
1  8      0 500000  20000 700000    0    0     0 75000 3000 9000  5  8 15 72  0
```

Interpretation:

- b is high, meaning blocked tasks.
- wa is high, meaning CPU is waiting on I/O.
- This confirms an I/O bottleneck.

### Scenario 6: Simulate High Load from CPU vs High Load from I/O
#### Goal
Learn that load average can rise for different reasons.

#### CPU-Based Load
Run:

```bash id="hf687l"
stress-ng --cpu 4 --timeout 60s
```

Check:

```bash id="ytan1o"
uptime
vmstat 1
```

Example:

```text id="cepiaw"
load average: 4.20, 2.10, 1.00

r  b  us sy id wa
5  0  95  4  1  0
```

Interpretation:

- Load is high because tasks are runnable.
- r is high.
- CPU user time is high.
- I/O wait is low.
- This is CPU pressure.

#### I/O-Based Load
Run the `fio` random write test from Scenario 5.

Check:

```bash id="q1y7q9"
uptime
vmstat 1
```

Example:

```text id="bhvsa1"
load average: 6.80, 4.10, 2.30

r  b  us sy id wa
1  8   5  8 15 72
```

Interpretation:

- Load is high, but CPU is not mostly busy.
- b and wa are high.
- The load comes from tasks blocked on I/O.

### Scenario 7: Analyze a Multi-Threaded Process
#### Goal
See thread-level states inside one process.

#### Simulate a Multi-Threaded Python Program
Create a script:

```bash id="y5yq3e"
cat > /tmp/thread-states.py <<'EOF'
import threading
import time

def cpu_worker():
    while True:
        pass

def sleep_worker():
    while True:
        time.sleep(10)

threads = []

t1 = threading.Thread(target=cpu_worker, name="cpu-worker")
t2 = threading.Thread(target=sleep_worker, name="sleep-worker")
t3 = threading.Thread(target=sleep_worker, name="sleep-worker-2")

for t in (t1, t2, t3):
    t.daemon = True
    t.start()

time.sleep(300)
EOF
```

Run it:

```bash id="n2kgwo"
python3 /tmp/thread-states.py
```

Find PID:

```bash id="dyu8r6"
pgrep -f thread-states.py
```

Example output:

```text id="cmuk9s"
5200
```

#### Check Threads
```bash id="if57s7"
ps -L -p 5200 -o pid,tid,stat,pcpu,comm
```

Example output:

```text id="cfh2tg"
  PID   TID STAT %CPU COMMAND
 5200  5200 Sl    0.0 python3
 5200  5201 Rl   99.0 python3
 5200  5202 Sl    0.0 python3
 5200  5203 Sl    0.0 python3
```

#### Interpretation
- The process has multiple threads.
- One thread is CPU-bound in R state.
- Other threads are sleeping.
- Thread-level monitoring shows more detail than process-level monitoring alone.

#### Check with `top`
```bash id="odj41n"
top -H -p 5200
```

This shows CPU usage by thread.

### Scenario 8: Detect Lock or Synchronization Waiting
#### Goal
Show how an application can be slow because threads wait, even when CPU is low.

#### Simulate with File Locking
Terminal 1:

```bash id="xilfz5"
flock /tmp/demo.lock sleep 300
```

Terminal 2:

```bash id="z3rtoc"
flock /tmp/demo.lock echo "got lock"
```

The second command waits because the first command holds the lock.

#### Check State
Find the waiting process:

```bash id="s1u3ag"
ps -eo pid,stat,wchan:30,cmd | grep flock
```

Example output:

```text id="zn75jp"
 5400 S    do_wait                        flock /tmp/demo.lock sleep 300
 5410 S    locks_lock_inode_wait          flock /tmp/demo.lock echo got lock
```

#### Interpretation
- The waiting process is sleeping.
- The wait channel suggests it is waiting on a lock.
- This is not a CPU bottleneck.
- It is synchronization or lock contention.

#### Real Meaning
In real applications, many sleeping threads may indicate:

- database lock contention
- mutex contention
- thread pool exhaustion
- waiting on another service
- waiting for a shared resource

Next tools may include:

- application logs
- database lock views
- strace
- perf
- language runtime profilers

### Scenario 9: Use `strace` to See What a Sleeping Process Waits On
#### Goal
Connect task state to system calls.

#### Simulate
Run:

```bash id="x9q0es"
sleep 300
```

Find PID:

```bash id="crd4ti"
pgrep -n sleep
```

Attach `strace`:

```bash id="fhh76n"
sudo strace -p PID
```

Example output:

```text id="bhkt6i"
restart_syscall(<... resuming interrupted nanosleep ...>
```

Interpretation:

- The process is sleeping in a timer-related system call.
- This confirms the S state is expected.

For a network server, `strace` might show:

```text id="ycfvsk"
accept(...)
poll(...)
epoll_wait(...)
```

Interpretation:

```text id="ot9z5w"
The process is waiting for network events or connections.
```

Use `strace` carefully on production systems because it can add overhead and expose sensitive data.

### Scenario 10: Create a Simple Task-State Sampler
#### Goal
Collect thread state counts over time.

#### Script
```bash id="iuxt82"
cat > ~/task-state-sampler.sh <<'EOF'
#!/bin/bash

INTERVAL="${1:-1}"
COUNT="${2:-10}"

for i in $(seq 1 "$COUNT"); do
    echo "===== $(date) ====="
    ps -eo state | sort | uniq -c
    echo
    sleep "$INTERVAL"
done
EOF

chmod +x ~/task-state-sampler.sh
```

Run:

```bash id="ud3w6d"
~/task-state-sampler.sh 1 5
```

Example output:

```text id="p6n24g"
===== Mon Jun  1 15:00:01 CEST 2026 =====
  6 R
210 S
  1 Z

===== Mon Jun  1 15:00:02 CEST 2026 =====
  8 R
208 S
  1 Z
```

#### Interpretation
- Most tasks are sleeping.
- Runnable tasks are present but not extreme.
- One zombie exists.
- No D-state tasks were captured in this sample.

This kind of sampling helps show trends over time.

### Scenario 11: Sample States for One Application
#### Goal
Track only one process and its threads.

#### Script
```bash id="g6f3dv"
cat > ~/sample-process-threads.sh <<'EOF'
#!/bin/bash

PID="$1"
INTERVAL="${2:-1}"
COUNT="${3:-10}"

if [ -z "$PID" ]; then
    echo "Usage: $0 PID [interval] [count]"
    exit 1
fi

for i in $(seq 1 "$COUNT"); do
    echo "===== $(date) ====="
    ps -L -p "$PID" -o pid,tid,stat,pcpu,pmem,wchan:25,comm
    echo
    sleep "$INTERVAL"
done
EOF

chmod +x ~/sample-process-threads.sh
```

Run:

```bash id="e8dguq"
~/sample-process-threads.sh 5200 1 5
```

Example output:

```text id="tfxfnm"
===== Mon Jun  1 15:05:01 CEST 2026 =====
  PID   TID STAT %CPU %MEM WCHAN                     COMMAND
 5200  5200 Sl    0.0  0.5 hrtimer_nanosleep          python3
 5200  5201 Rl   99.0  0.5 -                          python3
 5200  5202 Sl    0.0  0.5 hrtimer_nanosleep          python3
 5200  5203 Sl    0.0  0.5 hrtimer_nanosleep          python3
```

#### Interpretation
- One thread is CPU-bound.
- Other threads are sleeping on timers.
- The application slowdown, if present, would likely be caused by the CPU-heavy thread or single-threaded bottleneck.

### Scenario 12: Database-Like I/O Wait Investigation
#### Goal
Use task states to diagnose a slow, I/O-heavy application.

#### Symptoms
- Users report slow queries.
- CPU usage is low.
- Application response time is high.

#### Check Task States
```bash id="wuij6l"
ps -eo pid,stat,wchan:30,comm | awk '$2 ~ /^D/ {print}'
```

Example output:

```text id="xowm1m"
 6200 D    wait_on_page_bit_common        postgres
 6201 D    io_schedule                    postgres
 6202 D    io_schedule                    postgres
```

#### Check Disk
```bash id="nj0d4l"
iostat -xz 1 3
```

Example output:

```text id="y0mk6j"
avg-cpu:  %user %system %iowait %idle
           5.00    2.00   90.00  3.00

Device            r/s    w/s   rkB/s   wkB/s  await  aqu-sz  %util
sda            100.00  50.00 5120.0  2560.0   50.00    5.00  75.00
```

#### Interpretation
- Several database processes are in D state.
- CPU iowait is very high.
- Disk await is high.
- The database is likely waiting on storage.

#### Possible Fixes
- optimize queries
- add indexes carefully
- increase database cache if memory allows
- move data to faster storage
- separate logs and data files
- reduce competing disk workloads
- check for disk errors

### Task-State Interpretation Guide
#### Pattern: Many `R` Tasks
Example:

```text id="jihvlg"
20 R
180 S
```

Likely meaning:

```text id="bggjx6"
CPU pressure or many runnable tasks
```

Check:

```bash id="owldld"
top
vmstat 1
uptime
sudo perf top
```

Look for:

- high CPU usage
- low idle percentage
- high run queue
- specific CPU-heavy process

### Pattern: Many `S` Tasks
Example:

```text id="pxmrpc"
2 R
250 S
```

Likely meaning:

```text id="l66flv"
Normal idle waiting, or application-level waiting
```

Check:

```bash id="vsy2fb"
ps -eo pid,stat,wchan:30,comm
application logs
strace -p PID
```

Look for:

- lock waits
- network waits
- timer sleeps
- thread pool exhaustion
- external service delays

### Pattern: Many `D` Tasks
Example:

```text id="nrsejm"
1 R
180 S
15 D
```

Likely meaning:

```text id="rmefxq"
I/O bottleneck or stuck kernel-level wait
```

Check:

```bash id="qpmy4r"
iostat -xz 1
vmstat 1
sudo iotop -o
dmesg -T | grep -iE 'error|timeout|reset|I/O'
```

Look for:

- high iowait
- high disk await
- high disk queue
- storage errors
- network filesystem problems

### Pattern: `T` Tasks
Example:

```text id="ggcz2r"
PID STAT COMMAND
4300 T    python3
```

Likely meaning:

```text id="pma0km"
process was stopped by signal, shell job control, or debugger
```

Check:

```bash id="cwshze"
jobs
ps -o pid,ppid,stat,cmd -p PID
```

Fix:

```bash id="s2x0m6"
kill -CONT PID
```

### Pattern: `Z` Tasks
Example:

```text id="s5ufqi"
PID PPID STAT CMD
4451 4450 Z    [python3] <defunct>
```

Likely meaning:

```text id="p4ixg0"
child process exited but parent did not reap it
```

Check:

```bash id="cyxzl9"
ps -eo pid,ppid,state,cmd | awk '$3 == "Z" {print}'
```

Fix:

```text id="nsvjea"
restart or fix the parent process
```

### Practical Troubleshooting Workflow
When an application is slow:

1. Identify the process ID.
2. Check overall CPU, memory, and load.
3. Inspect thread states.
4. Count state patterns.
5. Check wait channels.
6. Correlate with disk, network, or logs.
7. Use deeper tools only when needed.

### Step 1: Identify the PID
```bash id="s8ga0a"
pgrep -af myprocess
```

Example:

```text id="cvd8q6"
1234 /usr/local/bin/myprocess --config /etc/myprocess.conf
```

### Step 2: Check Overall System Health
```bash id="bc5c6v"
uptime
top
free -h
vmstat 1
```

This tells you whether the system is CPU-bound, memory-bound, or I/O-bound.

### Step 3: Inspect Threads
```bash id="fq6ni0"
ps -L -p 1234 -o pid,tid,stat,pcpu,pmem,wchan:30,comm
```

Look for:

- many R threads
- many D threads
- many sleeping threads on the same wait channel

### Step 4: Check Disk If D-State Appears
```bash id="riobgq"
iostat -xz 1
sudo iotop -o
dmesg -T | grep -iE 'I/O|error|timeout|reset'
```

### Step 5: Check CPU Hotspots If R-State Dominates
```bash id="kqcdjt"
top -H -p 1234
sudo perf top
```

### Step 6: Check Application Logs
```bash id="rqf19h"
journalctl -u myservice.service -b
tail -f /var/log/myapp.log
```

Logs can reveal errors that task states alone cannot explain.

### Caveats of Task-State Analysis
Task-state analysis is powerful, but it has limitations.

- Tasks can change state very quickly.
- Sampling may miss short events.
- State letters do not explain the full cause.
- High sampling frequency can add overhead.
- Some wait channels require kernel knowledge.
- Application context still matters.

A task in `S` state is not necessarily healthy or unhealthy.

A task in `D` state is not always a disaster if it is brief.

Interpret states together with:

- CPU metrics
- disk metrics
- network metrics
- logs
- application behavior
- user reports

### Useful Command Summary
Process and thread states:

```bash id="x8ihrd"
ps -eo pid,stat,comm
ps -eLo pid,tid,stat,comm
ps -L -p PID -o pid,tid,stat,pcpu,pmem,wchan:30,comm
```

Count states:

```bash id="oe2ew7"
ps -eo state | sort | uniq -c
```

Find D-state tasks:

```bash id="ji9yhu"
ps -eo pid,stat,wchan:30,comm | awk '$2 ~ /^D/ {print}'
```

Find zombies:

```bash id="mnfg96"
ps -eo pid,ppid,state,cmd | awk '$3 == "Z" {print}'
```

Inspect `/proc`:

```bash id="jcr6dv"
cat /proc/PID/status
cat /proc/PID/stat
ls /proc/PID/task
```

Interactive tools:

```bash id="qjnrks"
top -H -p PID
htop
sudo perf top
```

Correlate with system metrics:

```bash id="ufp6f3"
uptime
vmstat 1
iostat -xz 1
sudo iotop -o
free -h
journalctl -u service.service -b
```

### Safe Lab Cleanup
Remove test files:

```bash id="nvlvv2"
rm -f /tmp/make-zombie.py
rm -f /tmp/thread-states.py
rm -f ~/task-state-sampler.sh
rm -f ~/sample-process-threads.sh
rm -rf ~/task-state-lab
```

Stop leftover test processes if needed:

```bash id="x7xgm5"
pkill -f thread-states.py
pkill -f stress-ng
pkill -f fio
```

Be careful with `pkill` on shared systems. Confirm process names first with:

```bash id="ks2s0m"
pgrep -af process-name
```

### Challenges

1. Use the `ps` command to view the current states of all threads in a specific process. Record the states and explain the significance of each, such as `R` for running, `S` for sleeping, and `D` for uninterruptible sleep. Then, check the `/proc/[PID]/stat` file for the same process and compare the results with `ps`. Discuss how these commands help monitor thread behavior over time.
2. Write a Bash script that samples thread states every second for a specific process and logs the count of each state (`R`, `S`, `D`, etc.). Run the script for a few minutes while the process is under load, then analyze the log to determine the predominant thread state. Discuss what the observed states reveal about the application’s behavior and possible bottlenecks.
3. Identify a process with threads in the `D` (uninterruptible sleep) state, suggesting that it is waiting for I/O. Use `iostat` to measure disk performance during this time and analyze the output to identify potential disk bottlenecks. Discuss how `iowait` can impact application performance and propose ways to address high I/O wait times.
4. Launch `htop` and configure it to display thread information for a specific process. Observe the states of the threads over time. Discuss how interactive tools like `htop` complement command-line sampling for real-time monitoring of thread behavior.
5. Use a tool like `dd` or `stress-ng` to simulate high disk I/O on your system. While the tool is running, monitor thread states for various processes using `ps` and `htop`. Record the proportion of threads in the `D` state and explain how simulated disk stress impacts thread states across the system.
6. Run a multi-threaded application on your system and monitor its threads over time. Pay special attention to any threads in the `S` (sleeping) state and determine if they are waiting for locks or synchronization events. Discuss how sleeping threads might indicate contention issues and propose potential optimizations to reduce waiting times.
7. If possible, install a database server (like MySQL or PostgreSQL) and run several queries to put it under load. Use `ps` or `top` to observe the states of database threads, particularly looking for `D` or `S` states. Explain how Task-State Analysis can help diagnose database performance issues related to I/O waits or lock contention.
8. Use both `scp` and `sftp` to transfer a large file and monitor the task states of each tool’s threads during the transfer. Record the observed states and transfer times, then compare the results. Discuss which protocol is more efficient in terms of thread activity and overall performance.
9. Use the `perf top` command while running a multi-threaded application to identify functions that are consuming significant CPU time. Discuss how `perf` can supplement Task-State Analysis by providing insights into CPU-bound threads and hotspots in the code, offering a more complete view of application performance.
10. Imagine a scenario where a web application is experiencing slow response times. Use Task-State Analysis to monitor the application’s threads over time, identifying threads that are predominantly in the `S` or `D` state. Based on your observations, suggest possible reasons for the performance issue and recommend adjustments, such as increasing resources or optimizing specific parts of the application.
