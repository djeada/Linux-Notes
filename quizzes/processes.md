# Processes Quiz

Notes: [Processes](../notes/processes.md), [Task-State Analysis](../notes/task_state_analysis.md), [Performance Monitoring](../notes/performance_monitoring.md)

Check your understanding of process inspection, signals, job control, priorities and process states.

#### Q. Which command prints a one-time snapshot of every process on the system, with user, PID, CPU and memory columns?

* [ ] `ps`
* [x] `ps aux`
* [ ] `top`
* [ ] `jobs -l`

> **Explanation:** `ps aux` lists all processes for all users with `%CPU`, `%MEM`, `STAT` and the command. Plain `ps` shows only processes on the current terminal, `top` is a live view, and `jobs` lists only the current shell's jobs.

#### Q. Which `ps` option selects every process on the system in standard (UNIX) syntax, as in `ps -ef`?

* [ ] `-u`
* [x] `-e`
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
* [x] `ps -o ppid= -p 1234`
* [ ] `ps -p 1234`
* [ ] `ps -u 1234 -o pid`

> **Explanation:** `-o ppid=` selects the PPID column and the trailing `=` removes its header; `-p 1234` picks the process. `pgrep -P 1234` does the reverse: it lists the children of 1234.

#### Q. Which command shows processes as a tree, making parent-child relationships easy to see?

* [ ] `ps aux`
* [x] `pstree -p`
* [ ] `pgrep -l`
* [ ] `jobs -l`

> **Explanation:** `pstree` draws the process hierarchy, and `-p` adds PIDs. `ps fax` gives a similar ASCII-art tree. `ps aux` and `pgrep -l` print flat lists.

#### Q. Which command prints the PIDs and names of all running processes called `nginx`?

* [ ] `ps nginx`
* [x] `pgrep -l nginx`
* [ ] `pidof -l nginx`
* [ ] `jobs nginx`

> **Explanation:** `pgrep` matches process names and prints PIDs; `-l` adds the name. Add `-f` to match against the full command line, `-u user` to filter by owner, or `-n` for the newest match.

#### Q. Why does `ps -ef | grep firefox` often include an extra line that is not Firefox?

* [ ] `ps` lists each Firefox thread as a separate process
* [x] The `grep firefox` process itself matches the pattern
* [ ] `ps -ef` prints a header line containing the search term
* [ ] Firefox starts a watchdog process with the same name

> **Explanation:** The `grep` process's own command line contains `firefox`, so it matches. Use `grep '[f]irefox'`, add `grep -v grep`, or switch to `pgrep firefox`.

#### Q. Which command gives a continuously updating view of processes, sorted by CPU usage by default?

* [ ] `ps aux`
* [x] `top`
* [ ] `pgrep`
* [ ] `pstree`

> **Explanation:** `top` refreshes every few seconds and shows a system summary (load, CPU, memory) above the process list. `ps` prints a single snapshot.

#### Q. While `top` is running, which key sorts the process list by memory usage?

* [ ] `P`
* [x] `M`
* [ ] `k`
* [ ] `r`

> **Explanation:** `M` sorts by `%MEM` and `P` sorts by `%CPU`. `k` prompts for a PID to signal, and `r` renices a process.

#### Q. In `htop`, what is the difference between pressing F4 and F3?

* [ ] F4 kills the selected process and F3 stops it
* [x] F4 filters out non-matching rows and F3 searches while keeping every row
* [ ] F4 sorts by memory and F3 sorts by CPU
* [ ] F4 shows threads and F3 hides them

> **Explanation:** F4 (Filter) hides processes that do not match the typed text, and F3 (Search) jumps to matches without hiding anything else. F9 sends a signal and F6 changes the sort column.

#### Q. What is PID 1 on a systemd-based distribution?

* [ ] The kernel scheduler thread
* [x] `systemd`, the first user-space process, which starts services and adopts orphans
* [ ] The login shell of the first user to log in
* [ ] `kthreadd`, the parent of every process

> **Explanation:** The kernel starts PID 1 (`systemd` or `init`), which brings up the user-space service tree and normally adopts orphaned processes. Kernel threads descend from `kthreadd` (PID 2), not from PID 1.

#### Q. In C, what does `fork()` do?

* [ ] Replaces the current program with a new one while keeping the PID
* [x] Creates a new child process that is a copy of the calling process
* [ ] Waits for a child process to exit and collects its status
* [ ] Sends a signal to another process

> **Explanation:** `fork()` returns twice: `0` in the child and the child's PID in the parent. Replacing the program image is the `exec` family, and collecting exit status is `wait()`/`waitpid()`.

#### Q. A child process calls `execl("/bin/ls", "ls", (char *)NULL)` and it succeeds. What happens to the child's PID?

* [ ] The kernel assigns a new PID for `ls`
* [x] It stays the same, because `exec` replaces the program in the same process
* [ ] It becomes the parent's PID
* [ ] It becomes 1, because `exec` re-parents the process to `init`

> **Explanation:** The `exec` family loads a new program image into the existing process; no new process is created. That is why shells use `fork()` first, then `exec` in the child.

#### Q. What is the main difference between a process and a thread?

* [ ] Threads always run on a different CPU core from their process
* [x] Each process has its own address space, while threads in one process share memory
* [ ] A process can contain only one thread at a time
* [ ] Threads have their own PIDs and memory, while processes share memory

> **Explanation:** Threads of one process share the same memory and open files but have separate stacks and registers. `ps -eLo pid,tid,stat,comm` lists threads with their thread IDs (TID).

#### Q. Which command sends `SIGTERM`, asking process 1234 to shut down cleanly?

* [ ] `kill -9 1234`
* [x] `kill 1234`
* [ ] `kill -STOP 1234`
* [ ] `kill -0 1234`

> **Explanation:** `kill` sends `SIGTERM` (15) by default, which a program may catch to clean up. `-9` is `SIGKILL`, `-STOP` pauses the process, and signal `0` only checks whether the PID exists.

#### Q. Which signal cannot be caught, blocked or ignored, and so ends a process immediately?

* [ ] `SIGTERM`
* [ ] `SIGINT`
* [x] `SIGKILL`
* [ ] `SIGHUP`

> **Explanation:** The kernel handles `SIGKILL` (9) itself, so the program cannot run cleanup code. Use it only after `SIGTERM` fails. `SIGSTOP` is likewise uncatchable, but it pauses the process instead of killing it.

#### Q. What happens when you press Ctrl+C while a command runs in the foreground?

* [ ] The terminal sends `SIGKILL` to the command
* [x] The terminal sends `SIGINT` to the foreground process group
* [ ] The shell sends `SIGTSTP` and parks the job
* [ ] The terminal sends `SIGHUP` and closes the session

> **Explanation:** Ctrl+C generates `SIGINT` (2), an interrupt that programs may catch. Ctrl+Z generates `SIGTSTP`, which stops the job instead of ending it.

#### Q. Which command terminates every process named `firefox` without looking up PIDs first?

* [ ] `kill firefox`
* [x] `pkill firefox`
* [ ] `pgrep -k firefox`
* [ ] `kill -n firefox`

> **Explanation:** `pkill` matches processes by name (like `pgrep`) and sends them a signal, `SIGTERM` by default. `kill` expects PIDs or job specs such as `%1`, not names.

#### Q. How can you pause process 1234 and later let it continue from where it stopped?

* [ ] Send `SIGTERM`, then `SIGHUP`
* [x] Send `SIGSTOP`, then `SIGCONT`
* [ ] Send `SIGINT`, then `SIGUSR1`
* [ ] Send `SIGKILL`, then `SIGCONT`

> **Explanation:** `kill -STOP 1234` freezes the process (state `T`), and `kill -CONT 1234` resumes it. `SIGSTOP` cannot be caught or ignored. A killed process cannot be continued.

#### Q. Many daemons, such as `nginx`, do what when they receive `SIGHUP`?

* [ ] Exit immediately without cleanup
* [x] Reload their configuration files without a full restart
* [ ] Pause until they receive `SIGCONT`
* [ ] Dump their memory to a core file

> **Explanation:** `SIGHUP` originally meant "terminal hung up", and its default action is to terminate. Many daemons have no terminal, so they catch it and treat it as a request to reload configuration.

#### Q. What does `kill -s TERM -- -2345` do?

* [ ] Sends `SIGTERM` to the process with PID 2345
* [x] Sends `SIGTERM` to every process in process group 2345
* [ ] Sends `SIGTERM` to every process the user may signal
* [ ] Sends `SIGTERM` to process 2345 and its parent

> **Explanation:** A negative target (other than `-1`) means a process group, and `--` stops `kill` from reading `-2345` as an option. Target `-1` means all processes you may signal, and `0` means your own process group.

#### Q. How do you start `./backup.sh` so that it runs in the background and you get the prompt back immediately?

* [ ] `bg ./backup.sh`
* [x] `./backup.sh &`
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
* [x] `fg %2`
* [ ] `jobs %2`
* [ ] `kill -CONT 2`

> **Explanation:** `%2` is a job spec for job 2 in this shell. `bg %2` resumes it in the background instead, and `kill -CONT 2` would target PID 2, not job 2.

#### Q. In this `jobs -l` output, what does the `+` mean?

```text
[1]  + 3241 Running    sleep 1000 &
[2]  - 3250 Stopped    vi notes.txt
```

* [ ] Job 1 has a higher scheduling priority
* [x] Job 1 is the current job, used by `fg` and `bg` when no job is named
* [ ] Job 1 was started with `nohup`
* [ ] Job 1 has finished and is waiting to be cleared

> **Explanation:** `+` marks the current job and `-` the previous one. Plain `fg` or `bg` acts on the `+` job.

#### Q. In a script, what does the `wait` builtin do?

* [ ] Sleeps for a fixed number of seconds
* [x] Blocks until the script's background child processes have finished
* [ ] Waits for the user to press Enter
* [ ] Suspends the script until it receives `SIGCONT`

> **Explanation:** `wait` with no arguments waits for all background children; `wait PID` waits for one and returns its exit status. Pausing for a duration is `sleep`.

#### Q. You start `./long_job.sh &` over SSH, and the job dies when you log out. Which change keeps it running after logout?

* [ ] `nice ./long_job.sh &`
* [x] `nohup ./long_job.sh > job.log 2>&1 &`
* [ ] `./long_job.sh > job.log 2>&1 &`
* [ ] `bg ./long_job.sh`

> **Explanation:** Closing the session sends `SIGHUP` to its jobs. `nohup` makes the command ignore `SIGHUP`; redirecting alone does not, it only avoids writing to a closed terminal. For critical work, a service manager, `tmux` or `screen` is better.

#### Q. What range of nice values does Linux use, and which end gets the most CPU time?

* [ ] 0 to 100, with 100 favoured most
* [x] -20 to 19, with -20 favoured most
* [ ] -20 to 19, with 19 favoured most
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

#### Q. What is a zombie process (state `Z`)?

* [ ] A process stuck in uninterruptible disk I/O
* [x] A child that has exited but whose parent has not yet collected its exit status
* [ ] A process that has been stopped with `SIGSTOP`
* [ ] A process whose parent died and that was adopted by PID 1

> **Explanation:** A zombie has finished running and holds only a process-table entry until its parent calls `wait()`. Waiting on disk I/O is state `D`, stopped is `T`, and an adopted process is an orphan, not a zombie.

#### Q. `ps` keeps showing a zombie child of PID 800, even after `kill -9` on the zombie. What actually removes it?

* [ ] Sending `SIGKILL` again with `kill -s KILL`
* [x] Having PID 800 reap it with `wait()`, or ending PID 800 so PID 1 adopts and reaps it
* [ ] Sending `SIGCONT` to the zombie
* [ ] Running `renice -n 19` on the zombie

> **Explanation:** A zombie has already exited, so there is nothing left for a signal to kill. Only reaping removes the entry: fix or restart the parent, and if the parent dies, PID 1 adopts and reaps the zombie.

#### Q. Many processes sit in state `D` for a long time while `vmstat` shows high `wa`. What does this suggest?

* [ ] A CPU bottleneck from compute-heavy threads
* [x] An I/O bottleneck, such as a slow disk or a stuck network filesystem
* [ ] A parent process that is not reaping its children
* [ ] Processes that were stopped with Ctrl+Z

> **Explanation:** `D` is uninterruptible sleep, usually waiting on kernel I/O, and such tasks often cannot be killed until the I/O finishes. Many `R` tasks point to CPU pressure, many `Z` to a broken parent, and `T` to stopped jobs.

#### Q. In `ps -eo pid,stat,comm` output, what does a `STAT` value of `S` mean?

* [ ] The process is stopped and must be resumed with `SIGCONT`
* [x] The process is in interruptible sleep, waiting for an event such as input or a timer
* [ ] The process is a session leader and is currently running
* [ ] The process is swapped out to disk

> **Explanation:** `S` means interruptible sleep, which is normal for most processes most of the time. A trailing `s` (as in `Ss`) marks a session leader, `+` the foreground group, and `l` a multi-threaded process.

#### Q. Which command shows the 1-, 5- and 15-minute load averages, along with uptime and logged-in user count?

* [ ] `free -h`
* [x] `uptime`
* [ ] `df -h`
* [ ] `ps aux`

> **Explanation:** `uptime` prints a line such as `up 1 day, 2 users, load average: 0.42, 0.35, 0.30`. The same figures appear in the first line of `top`.

#### Q. A 4-core server shows a load average of `6.80, 4.10, 2.30`, but CPU usage is low and `vmstat` shows high `b` and `wa`. What is driving the load?

* [ ] Too many runnable CPU-bound tasks
* [x] Tasks blocked on I/O, which Linux also counts in the load average
* [ ] Too much free memory being cached
* [ ] Zombie processes using up CPU time

> **Explanation:** Linux load counts runnable tasks and tasks in uninterruptible (`D`) sleep, so I/O waits raise it even when the CPU is idle. High `b` (blocked) and `wa` (I/O wait) confirm the cause. Zombies use no CPU.

#### Q. What is a daemon?

* [ ] A process that has crashed and left a core dump
* [x] A background service process, such as one that handles logging, printing or networking
* [ ] Any process started from a terminal with `&`
* [ ] A process that runs only as root

> **Explanation:** Daemons provide services in the background and are usually started at boot or on demand by a service manager. Many run under dedicated unprivileged accounts, and a shell job started with `&` is still a shell job.

#### Q. Which command lists every thread of every process, with a thread ID column?

* [ ] `ps -ef`
* [x] `ps -eLo pid,tid,stat,comm`
* [ ] `pstree -a`
* [ ] `ps -u root`

> **Explanation:** `-L` shows one row per thread, and `tid` is the thread ID. Threads of one process share its PID but have their own TIDs and states, which helps spot the one thread using CPU.

#### Q. In a shell with background jobs, what is the difference between `kill %1` and `kill 1`?

* [ ] They are the same; `%` is optional
* [x] `kill %1` signals job number 1 in this shell, while `kill 1` targets the process with PID 1
* [ ] `kill %1` sends `SIGKILL`, while `kill 1` sends `SIGTERM`
* [ ] `kill %1` signals the first process listed by `ps`

> **Explanation:** `%N` is a job spec that the shell translates into the job's processes. A plain number is a PID, and PID 1 is `systemd` or `init`, which ordinary users are not allowed to signal.

#### Q. `ps -o pid,stat,comm -p 3250` shows `STAT` as `T`. What does that mean?

* [ ] The process is a kernel thread
* [x] The process is stopped, for example by Ctrl+Z, `SIGSTOP` or a debugger
* [ ] The process is terminating and will exit shortly
* [ ] The process is waiting on a TCP connection

> **Explanation:** `T` means stopped: the process does not run until it gets `SIGCONT`, for example from `fg` or `bg`. Exited processes that have not been reaped show `Z`.
