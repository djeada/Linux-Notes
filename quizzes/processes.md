# Processes Quiz

Notes: [Processes](../notes/processes.md), [Task-State Analysis](../notes/task_state_analysis.md), [Performance Monitoring](../notes/performance_monitoring.md)

Check your understanding of process inspection, signals, job control, priorities, process states and the memory and load figures that go with them.

#### Q. Which command prints a one-time snapshot of every process on the system, with user, PID, CPU and memory columns?

* [ ] `ps`
* [ ] `top`
* [x] `ps aux`
* [ ] `jobs -l`

> **Explanation:** `ps aux` lists all processes for all users with `%CPU`, `%MEM`, `STAT` and the command. Plain `ps` shows only processes on the current terminal, `top` is a live view, and `jobs` lists only the current shell's jobs.

#### Q. Which `ps` option selects every process on the system in standard (UNIX) syntax, as in `ps -ef`?

* [x] `-e`
* [ ] `-u`
* [ ] `-p`
* [ ] `-a`

> **Explanation:** `-e` (same as `-A`) selects all processes, and `-f` adds full-format columns such as UID, PPID and start time. `-a` omits session leaders and processes without a terminal, `-u` filters by user and `-p` by PID.

#### Q. Which command lists only the processes owned by the user `alice`?

* [ ] `ps -e alice`
* [x] `ps -u alice`
* [ ] `ps -p alice`
* [ ] `ps --forest alice`

> **Explanation:** `ps -u alice` selects processes by effective user. `pgrep -u alice` gives just their PIDs. `-p` expects PIDs, not user names.

#### Q. Which command prints only the parent PID of process 1234, with no header line?

* [ ] `pgrep -P 1234`
* [ ] `ps -p 1234`
* [ ] `ps -u 1234 -o pid`
* [x] `ps -o ppid= -p 1234`

> **Explanation:** `-o ppid=` selects the PPID column and the trailing `=` removes its header; `-p 1234` picks the process. `pgrep -P 1234` does the reverse: it lists the children of 1234.

#### Q. Which command shows processes as a tree, making parent-child relationships easy to see?

* [ ] `ps aux`
* [ ] `pgrep -l`
* [x] `pstree -p`
* [ ] `jobs -l`

> **Explanation:** `pstree` draws the process hierarchy, and `-p` adds PIDs. `ps fax` gives a similar ASCII-art tree. `ps aux` and `pgrep -l` print flat lists.

#### Q. Which command prints the PIDs and names of all running processes called `nginx`?

* [ ] `ps nginx`
* [ ] `pidof -l nginx`
* [ ] `jobs nginx`
* [x] `pgrep -l nginx`

> **Explanation:** `pgrep` matches process names and prints PIDs; `-l` adds the name. Add `-f` to match against the full command line, `-u user` to filter by owner, or `-n` for the newest match.

#### Q. On Linux, `pgrep systemd-journald` prints a warning and finds nothing, although the daemon is running. Why?

* [x] `pgrep` matches the process name, which the kernel cuts to 15 characters (`systemd-journal`)
* [ ] `pgrep` only lists processes owned by the current user unless you add `-u root`
* [ ] `pgrep` needs the full path, such as `/usr/lib/systemd/systemd-journald`
* [ ] `pgrep` skips daemons that have no controlling terminal

> **Explanation:** By default `pgrep` compares against the short `comm` name, at most 15 characters. Use `pgrep -f systemd-journald` to match the full command line, or `pgrep -x systemd-journal` for the exact short name.

#### Q. Why does `ps -ef | grep firefox` often include an extra line that is not Firefox?

* [ ] `ps` lists each Firefox thread as a separate process
* [ ] `ps -ef` prints a header line containing the search term
* [x] The `grep firefox` process itself matches the pattern
* [ ] Firefox starts a watchdog process with the same name

> **Explanation:** The `grep` process's own command line contains `firefox`, so it matches. Use `grep '[f]irefox'`, add `grep -v grep`, or switch to `pgrep firefox`.

#### Q. Which command writes a single, non-interactive `top` snapshot that you can redirect into a log file?

* [x] `top -b -n 1`
* [ ] `top -d 1`
* [ ] `top -p 1`
* [ ] `top -H`

> **Explanation:** `-b` (batch mode) prints plain text instead of redrawing the screen, and `-n 1` stops after one update. `-d` sets the refresh delay, `-p` watches chosen PIDs and `-H` shows threads; on their own, all three stay interactive.

#### Q. While `top` is running, which key sorts the process list by memory usage?

* [ ] `P`
* [ ] `k`
* [ ] `r`
* [x] `M`

> **Explanation:** `M` sorts by `%MEM` and `P` sorts by `%CPU`. `k` prompts for a PID to signal, and `r` renices a process.

#### Q. In `htop`, what is the difference between pressing F4 and F3?

* [ ] F4 kills the selected process and F3 stops it
* [ ] F4 sorts by memory and F3 sorts by CPU
* [x] F4 filters out non-matching rows and F3 searches while keeping every row
* [ ] F4 shows threads and F3 hides them

> **Explanation:** F4 (Filter) hides processes that do not match the typed text, and F3 (Search) jumps to matches without hiding anything else. F9 sends a signal and F6 changes the sort column.

#### Q. What is PID 1 on a systemd-based distribution?

* [ ] The kernel's scheduler, running as a special thread
* [x] `systemd`, the first user-space process, which starts services and adopts orphans
* [ ] The login shell of the first user who logs in
* [ ] `kthreadd`, the parent of every process on the system

> **Explanation:** The kernel starts PID 1 (`systemd` or `init`), which brings up the user-space service tree and normally adopts orphaned processes. Kernel threads descend from `kthreadd` (PID 2), not from PID 1.

#### Q. A parent process exits while its child keeps running. What becomes the child's parent?

* [x] PID 1, or the nearest ancestor registered as a child subreaper, such as `systemd --user`
* [ ] Nobody: the child's PPID is set to 0 until the child exits
* [ ] Nothing changes, because the child is killed together with its parent
* [ ] The child turns into a zombie until a new parent calls `wait()`

> **Explanation:** Orphans are re-parented, normally to PID 1. In a desktop session they often go to `systemd --user`, which registers as a child subreaper, so `ps` can show an orphan's PPID as something other than 1.

#### Q. How many `hi` lines does this program print, assuming both `fork()` calls succeed?

```c
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
  fork();
  fork();
  printf("hi\n");
  while (wait(NULL) > 0) {}
  return 0;
}
```

* [ ] 2
* [x] 4
* [ ] 3
* [ ] 8

> **Explanation:** Each `fork()` duplicates every process that reaches it, so 1 process becomes 2, then 4, and each prints once. `fork()` returns `0` in the child and the child's PID in the parent, which is how code tells them apart.

#### Q. A child process calls `execl("/bin/ls", "ls", (char *)NULL)` and it succeeds. What happens to the child's PID?

* [x] It stays the same, because `exec` replaces the program in the same process
* [ ] The kernel assigns a new PID for `ls`
* [ ] It becomes the parent's PID
* [ ] It becomes 1, because `exec` re-parents the process to `init`

> **Explanation:** The `exec` family loads a new program image into the existing process; no new process is created. That is why shells use `fork()` first, then `exec` in the child.

#### Q. In Bash, which command normally runs without the shell creating a new process?

* [ ] `/bin/echo "Hello, world!"`
* [ ] `ls -l`
* [x] `echo "Hello, world!"`
* [ ] `sleep 1`

> **Explanation:** `echo` is a Bash builtin, so the shell runs it itself; `type echo` reports `echo is a shell builtin`. External programs such as `/bin/echo`, `ls` and `sleep` need a `fork()` followed by an `exec` in the child.

#### Q. What is the main difference between a process and a thread?

* [ ] Threads always run on a different CPU core from their process
* [ ] A process can contain only one thread at a time
* [ ] Threads have their own PIDs and memory, while processes share memory
* [x] Each process has its own address space, while threads in one process share memory

> **Explanation:** Threads of one process share the same memory and open files but have separate stacks and registers. `ps -eLo pid,tid,stat,comm` lists threads with their thread IDs (TID).

#### Q. Which command sends `SIGTERM`, asking process 1234 to shut down cleanly?

* [ ] `kill -9 1234`
* [x] `kill 1234`
* [ ] `kill -STOP 1234`
* [ ] `kill -0 1234`

> **Explanation:** `kill` sends `SIGTERM` (15) by default, which a program may catch to clean up. `-9` is `SIGKILL` and `-STOP` pauses the process. Signal `0` sends nothing: it only tests whether the PID exists and you may signal it.

#### Q. Which signal cannot be caught, blocked or ignored, so the program gets no chance to clean up before it dies?

* [ ] `SIGTERM`
* [ ] `SIGINT`
* [ ] `SIGHUP`
* [x] `SIGKILL`

> **Explanation:** The kernel handles `SIGKILL` (9) itself, so no handler or cleanup code runs. Use it only after `SIGTERM` fails. `SIGSTOP` is likewise uncatchable, but it pauses the process instead of killing it.

#### Q. What happens when you press Ctrl+C while a command runs in the foreground?

* [ ] The terminal sends `SIGKILL` to the command
* [x] The terminal sends `SIGINT` to the foreground process group
* [ ] The shell sends `SIGTSTP` and parks the job
* [ ] The terminal sends `SIGHUP` and closes the session

> **Explanation:** Ctrl+C generates `SIGINT` (2) for every process in the foreground group, so both sides of `sleep 9 | sleep 9` get it. Programs may catch it. Ctrl+Z generates `SIGTSTP`, which stops the job instead.

#### Q. Which command terminates every process named `firefox` without looking up PIDs first?

* [ ] `kill firefox`
* [ ] `pgrep -k firefox`
* [x] `pkill firefox`
* [ ] `kill -n firefox`

> **Explanation:** `pkill` matches processes by name (like `pgrep`) and sends them a signal, `SIGTERM` by default. `kill` expects PIDs or job specs such as `%1`, not names.

#### Q. How can you pause process 1234 and later let it continue from where it stopped?

* [x] Send `SIGSTOP`, then `SIGCONT`
* [ ] Send `SIGTERM`, then `SIGHUP`
* [ ] Send `SIGINT`, then `SIGUSR1`
* [ ] Send `SIGKILL`, then `SIGCONT`

> **Explanation:** `kill -STOP 1234` freezes the process (state `T`), and `kill -CONT 1234` resumes it. `SIGSTOP` cannot be caught or ignored. A killed process cannot be continued.

#### Q. You run these commands in an interactive Bash shell. What does the last one print?

```bash
sleep 600 &
kill -STOP $!
kill $!
ps -o stat= -p $!
```

* [x] `T`, because the `SIGTERM` stays pending until the process is continued
* [ ] `Z`, because the process was killed but not yet reaped
* [ ] Nothing, because the process has already exited
* [ ] `S`, because `SIGTERM` resumed the stopped process

> **Explanation:** A stopped process does not act on most signals until it gets `SIGCONT`; only `SIGKILL` ends it straight away. Bash's `kill %1` avoids this trap by also sending `SIGCONT` to a stopped job.

#### Q. Many daemons, such as `nginx`, do what when they receive `SIGHUP`?

* [ ] Exit immediately without cleanup
* [ ] Pause until they receive `SIGCONT`
* [x] Reload their configuration files without a full restart
* [ ] Dump their memory to a core file

> **Explanation:** `SIGHUP` originally meant "terminal hung up", and its default action is to terminate. Many daemons have no terminal, so they catch it and treat it as a request to reload configuration.

#### Q. What does `kill -s TERM -- -2345` do?

* [ ] Sends `SIGTERM` to the process with PID 2345
* [x] Sends `SIGTERM` to every process in process group 2345
* [ ] Sends `SIGTERM` to every process the user may signal
* [ ] Sends `SIGTERM` to process 2345 and its parent

> **Explanation:** A negative target (other than `-1`) means a process group, and `--` stops `kill` from reading `-2345` as an option. Target `-1` means all processes you may signal, and `0` means your own process group.

#### Q. How do you start `./backup.sh` so that it runs in the background and you get the prompt back immediately?

* [x] `./backup.sh &`
* [ ] `bg ./backup.sh`
* [ ] `./backup.sh | bg`
* [ ] `nohup ./backup.sh`

> **Explanation:** A trailing `&` starts the command as a background job and prints its job number and PID, such as `[1] 3241`. `bg` resumes an existing stopped job, and `nohup` alone still runs the command in the foreground.

#### Q. You press Ctrl+Z while `long_task.sh` runs in the foreground. What state is the job in afterwards?

* [ ] Running in the background
* [x] Stopped, until you resume it with `fg` or `bg`
* [ ] Terminated, with its exit status saved
* [ ] Still running in the foreground, but with output hidden

> **Explanation:** Ctrl+Z sends `SIGTSTP`, which stops (pauses) the job and returns the prompt. `bg` resumes it in the background and `fg` brings it back to the foreground.

#### Q. Which command brings job number 2 back to the foreground?

* [ ] `bg %2`
* [ ] `jobs %2`
* [ ] `kill -CONT 2`
* [x] `fg %2`

> **Explanation:** `%2` is a job spec for job 2 in this shell. `bg %2` resumes it in the background instead, and `kill -CONT 2` would target PID 2, not job 2.

#### Q. In this Bash `jobs -l` output, what does the `+` after `[2]` mean?

```text
[1]- 3241 Running                 sleep 1000 &
[2]+ 3250 Stopped                 vi notes.txt
```

* [x] Job 2 is the current job, used by `fg` and `bg` when no job is named
* [ ] Job 2 has a higher scheduling priority
* [ ] Job 2 was started with `nohup`
* [ ] Job 2 has finished and is waiting to be cleared

> **Explanation:** `+` marks the current job and `-` the previous one. Bash prefers a stopped job as the current job, so plain `fg` here resumes `vi`, while `fg %-` would bring back `sleep`.

#### Q. In a script, what does the `wait` builtin do?

* [ ] Sleeps for a fixed number of seconds
* [ ] Waits for the user to press Enter
* [x] Blocks until the script's background child processes have finished
* [ ] Suspends the script until it receives `SIGCONT`

> **Explanation:** `wait` with no arguments waits for all background children; `wait PID` waits for one and returns its exit status. Pausing for a duration is `sleep`.

#### Q. You start `./long_job.sh &` over SSH, and the job dies when you log out. Which change keeps it running after logout?

* [ ] `nice ./long_job.sh &`
* [x] `nohup ./long_job.sh > job.log 2>&1 &`
* [ ] `./long_job.sh > job.log 2>&1 &`
* [ ] `bg ./long_job.sh`

> **Explanation:** When the session hangs up, Bash sends `SIGHUP` to its jobs. `nohup` makes the command ignore `SIGHUP`; redirecting alone does not, it only avoids writing to a closed terminal. For critical work, a service manager, `tmux` or `screen` is better.

#### Q. A long job is already running as background job `%1` in your SSH session. How do you keep it alive after logout without restarting it?

* [ ] `nohup %1`
* [x] `disown %1`
* [ ] `bg %1`
* [ ] `kill -CONT %1`

> **Explanation:** `disown` removes the job from the shell's job table, so Bash does not pass `SIGHUP` on to it when the session hangs up. `nohup` only works when starting a command, and `bg` and `SIGCONT` merely resume a stopped job.

#### Q. What range of nice values does Linux use, and which end gets the most CPU time?

* [ ] 0 to 100, with 100 favoured most
* [ ] -20 to 19, with 19 favoured most
* [x] -20 to 19, with -20 favoured most
* [ ] 1 to 20, with 1 favoured most

> **Explanation:** Lower nice values mean higher priority, so `-20` is the least "nice" to other processes. The default is `0`, and ordinary users may only raise a value (lower the priority).

#### Q. Which command starts `make` with lower CPU priority so it does not slow down interactive work?

* [ ] `nice -n -10 make`
* [x] `nice -n 10 make`
* [ ] `renice -n 10 make`
* [ ] `make --nice 10`

> **Explanation:** `nice -n 10` starts a new command with niceness 10, which is lower priority. A negative value raises priority and needs root. `renice` changes an already-running process and takes a PID, not a command.

#### Q. Which command changes the priority of the running process 4321 to niceness 5?

* [ ] `nice -n 5 4321`
* [x] `renice -n 5 -p 4321`
* [ ] `kill -n 5 4321`
* [ ] `top -n 5 -p 4321`

> **Explanation:** `renice` adjusts existing processes by PID (`-p`), group or user. `nice` only launches new commands, so `nice -n 5 4321` would try to run a program called `4321`.

#### Q. As an ordinary user, you ran `renice -n 5 -p 4321` on your own process. Now `renice -n 2 -p 4321` fails with `Permission denied`. Why?

* [ ] Ordinary users may only set nice values above 10
* [ ] The process must be stopped before its priority can change again
* [ ] `renice` needs `-g` instead of `-p` for processes you own
* [x] Lowering niceness raises priority, which needs `CAP_SYS_NICE`

> **Explanation:** Unprivileged users can make their own processes nicer but cannot take that back, unless `RLIMIT_NICE` allows it. The first command raised niceness from 0 to 5, which is always allowed; going back to 2 is a priority increase.

#### Q. What is a zombie process (state `Z`)?

* [ ] A process stuck in uninterruptible disk I/O
* [ ] A process that has been stopped with `SIGSTOP`
* [ ] A process whose parent died and that was adopted by PID 1
* [x] A child that has exited but whose parent has not yet collected its exit status

> **Explanation:** A zombie has finished running and holds only a process-table entry until its parent calls `wait()`. Waiting on disk I/O is state `D`, stopped is `T`, and an adopted process is an orphan, not a zombie.

#### Q. `ps` keeps showing a zombie child of PID 800, even after `kill -9` on the zombie. What actually removes it?

* [ ] Sending `SIGKILL` again, in case the first one was lost
* [ ] Sending `SIGCONT`, so the zombie can finish exiting
* [x] Having PID 800 reap it with `wait()`, or ending PID 800 so PID 1 adopts and reaps it
* [ ] Running `renice -n 19`, so the scheduler drops its entry

> **Explanation:** A zombie has already exited, so there is nothing left for a signal to kill. Only reaping removes the entry: fix or restart the parent, and if the parent dies, PID 1 (or a subreaper) adopts and reaps the zombie.

#### Q. Many processes sit in state `D` for a long time while `vmstat` shows high `wa`. What does this suggest?

* [ ] A CPU bottleneck from compute-heavy threads
* [ ] A parent process that is not reaping its children
* [ ] Processes that were stopped with Ctrl+Z
* [x] An I/O bottleneck, such as a slow disk or a stuck network filesystem

> **Explanation:** `D` is uninterruptible sleep, usually waiting on kernel I/O, and such tasks often cannot be killed until the I/O finishes. Many `R` tasks point to CPU pressure, many `Z` to a broken parent, and `T` to stopped jobs.

#### Q. In `ps -eo pid,stat,comm` output, what does a `STAT` value of `S` mean?

* [ ] The process is stopped and must be resumed with `SIGCONT`
* [ ] The process is a session leader and is currently running
* [ ] The process is swapped out to disk
* [x] The process is in interruptible sleep, waiting for an event such as input or a timer

> **Explanation:** `S` means interruptible sleep, which is normal for most processes most of the time. A trailing `s` (as in `Ss`) marks a session leader, `+` the foreground group, and `l` a multi-threaded process.

#### Q. In `ps -o pid,stat,comm` output, one process shows `STAT` `T` and another shows `t`. What is the difference?

* [x] `T` is stopped by job control or `SIGSTOP`; `t` is stopped by a tracer such as `gdb`
* [ ] `T` is terminating; `t` has terminated and is waiting to be reaped
* [ ] `T` is a multi-threaded process; `t` is one of its threads
* [ ] `T` was stopped by root; `t` was stopped by an ordinary user

> **Explanation:** Neither runs. `T` resumes on `SIGCONT`, for example from `fg` or `bg`, while `t` is a ptrace stop that the debugger controls. Exited processes that have not been reaped show `Z`.

#### Q. Which command shows the state, parent PID and thread count of process 1234 as labelled lines such as `State:` and `Threads:`?

* [ ] `cat /proc/1234/stat`
* [ ] `cat /proc/1234/cmdline`
* [x] `cat /proc/1234/status`
* [ ] `ls /proc/1234/task`

> **Explanation:** `/proc/PID/status` is human-readable, with `State:`, `PPid:` and `Threads:` lines. `/proc/PID/stat` holds similar data as unlabelled fields (the state is the third), `cmdline` holds the arguments, and `task/` has one directory per thread.

#### Q. Which command shows the 1-, 5- and 15-minute load averages, along with uptime and logged-in user count?

* [ ] `free -h`
* [ ] `df -h`
* [x] `uptime`
* [ ] `ps aux`

> **Explanation:** `uptime` prints a line such as `up 1 day, 2 users, load average: 0.42, 0.35, 0.30`. The same figures appear in the first line of `top`.

#### Q. A 4-core server shows a load average of `6.80, 4.10, 2.30`, but CPU usage is low and `vmstat` shows high `b` and `wa`. What is driving the load?

* [ ] Too many runnable CPU-bound tasks
* [ ] Too much free memory being cached
* [ ] Zombie processes using up CPU time
* [x] Tasks blocked on I/O, which Linux also counts in the load average

> **Explanation:** Linux load counts runnable tasks and tasks in uninterruptible (`D`) sleep, so I/O waits raise it even when the CPU is idle. High `b` (blocked) and `wa` (I/O wait) confirm the cause. Zombies use no CPU.

#### Q. A 4-core server shows a load average of `8.10, 7.90, 7.50`, and `vmstat 1` shows `r` near 8, `b` 0, `us` 95, `id` 0 and `wa` 0. What is the likely bottleneck?

* [x] CPU saturation: about twice as many runnable tasks as cores
* [ ] Disk I/O, because a load above the core count always means I/O wait
* [ ] Memory, because the system must be swapping heavily
* [ ] Zombie processes filling up the process table

> **Explanation:** `r` counts tasks running or waiting for a CPU, so 8 runnable tasks on 4 cores with no idle time and no I/O wait means CPU saturation. High `b` and `wa` would point to I/O instead.

#### Q. In `ps -ef` output, `systemd-journald` and `cron` show `?` in the `TTY` column. What does that tell you?

* [ ] Their terminal was closed and they are about to exit
* [x] They have no controlling terminal, as is typical for daemons
* [ ] `ps` lacks permission to read their terminal
* [ ] They are kernel threads rather than user-space processes

> **Explanation:** Daemons are background services, usually started by a service manager such as `systemd`, and are not attached to any terminal, so `ps` shows `?`. Kernel threads show `?` too, but their names appear in brackets, like `[kthreadd]`.

#### Q. Which command lists every thread of every process, with a thread ID column?

* [x] `ps -eLo pid,tid,stat,comm`
* [ ] `ps -ef`
* [ ] `pstree -a`
* [ ] `ps -u root`

> **Explanation:** `-L` shows one row per thread, and `tid` is the thread ID. Threads of one process share its PID but have their own TIDs and states, which helps spot the one thread using CPU.

#### Q. In a shell with background jobs, what is the difference between `kill %1` and `kill 1`?

* [ ] They are the same; `%` is optional
* [ ] `kill %1` sends `SIGKILL`, while `kill 1` sends `SIGTERM`
* [x] `%1` means job 1 of this shell; `1` means the process with PID 1
* [ ] `kill %1` signals the first process listed by `ps`

> **Explanation:** `%N` is a job spec that the shell translates into the job's processes. A plain number is a PID, and PID 1 is `systemd` or `init`, which an ordinary user's `kill` fails on with `Operation not permitted`.

#### Q. In `ps aux`, a Java process shows `VSZ` 4096000 and `RSS` 1210000 (both in KiB). Which statement is correct?

* [ ] It is using about 4 GB of physical RAM right now
* [x] About 1.2 GB is in RAM; VSZ is the whole virtual address space
* [ ] RSS counts the process's swap usage, and VSZ counts its physical RAM
* [ ] The two values only differ when the process uses shared libraries

> **Explanation:** RSS is the resident set in physical RAM. VSZ also counts mapped but untouched, swapped-out and reserved memory. RSS includes shared pages, so summing it over many processes overcounts total RAM use.

#### Q. `free -h` shows the output below. About how much memory can new programs get without swapping?

```text
               total        used        free      shared  buff/cache   available
Mem:            15Gi       5.4Gi       410Mi       300Mi       9.2Gi       8.9Gi
Swap:          2.0Gi          0B       2.0Gi
```

* [ ] About 410 MiB, since only `free` memory can be handed out
* [ ] About 9.2 GiB, since `buff/cache` is memory reserved for programs
* [ ] About 2.0 GiB, since new programs are placed in free swap first
* [x] About 8.9 GiB, the `available` estimate, since most of the cache can be reclaimed

> **Explanation:** Linux uses spare RAM for the page cache and gives it back on demand. `available` estimates what new programs can use without swapping, so a low `free` figure alone is normal, not a sign of memory pressure.

#### Q. `vmstat 1` keeps showing large non-zero `si` and `so` values, high `wa`, and the system feels frozen. What is happening?

* [x] Swap thrashing: memory is short, so pages keep moving between RAM and swap
* [ ] The CPU is overheating and the kernel is throttling it
* [ ] Network sockets are being opened and closed very rapidly
* [ ] The disk is nearly full, so the kernel keeps retrying writes

> **Explanation:** `si` and `so` are memory swapped in from and out to disk per second. Some swap use is harmless, but continuous swapping both ways means the working set does not fit in RAM; check `free -h` and the top `%MEM` processes.
