#### Q. Which command displays a snapshot of all currently running processes with detailed information?

* [ ] `ps`
* [x] `ps aux`
* [ ] `top`
* [ ] `jobs`
* [ ] `pgrep`

#### Q. What does the PID stand for in process management?

* [ ] Process Indicator
* [x] Process Identifier
* [ ] Program ID
* [ ] Parent ID
* [ ] Process Index

#### Q. Which command provides a real-time, dynamic view of running processes?

* [ ] `ps aux`
* [ ] `pgrep`
* [x] `top`
* [ ] `jobs`
* [ ] `ps -ef`

#### Q. What is the PID of the first process that starts when a Linux system boots?

* [x] 1
* [ ] 0
* [ ] 2
* [ ] 100
* [ ] -1

#### Q. Which command sends the default SIGTERM signal to terminate a process with PID 1234?

* [ ] `kill -9 1234`
* [x] `kill 1234`
* [ ] `pkill 1234`
* [ ] `killall 1234`
* [ ] `stop 1234`

#### Q. What signal is sent when you press Ctrl+C in a terminal?

* [ ] SIGKILL
* [x] SIGINT
* [ ] SIGTERM
* [ ] SIGHUP
* [ ] SIGSTOP

#### Q. Which signal cannot be caught, blocked, or ignored by a process?

* [ ] SIGTERM
* [ ] SIGINT
* [x] SIGKILL
* [ ] SIGHUP
* [ ] SIGSTOP

#### Q. How do you terminate all processes with the name "firefox"?

* [ ] `kill firefox`
* [ ] `kill -name firefox`
* [x] `pkill firefox`
* [ ] `ps firefox | kill`
* [ ] `killall -pid firefox`

#### Q. What command suspends a foreground process and puts it in the background?

* [ ] `bg`
* [ ] `fg`
* [x] Ctrl+Z
* [ ] `stop`
* [ ] `pause`

#### Q. Which command brings a background job to the foreground?

* [ ] `bg`
* [x] `fg`
* [ ] `jobs`
* [ ] `bring`
* [ ] `front`

#### Q. How do you start a command in the background from the shell?

* [ ] `command &bg`
* [ ] `bg command`
* [x] `command &`
* [ ] `background command`
* [ ] `command -bg`

#### Q. Which command lists all jobs running in the current shell session?

* [ ] `ps`
* [ ] `top`
* [x] `jobs`
* [ ] `pgrep`
* [ ] `list`

#### Q. What is a daemon in Linux?

* [ ] A foreground process started by the user
* [x] A background process that runs without user interaction
* [ ] A process that has crashed
* [ ] A process waiting for user input
* [ ] A temporary process

#### Q. Which column in `ps aux` output shows the percentage of CPU used by a process?

* [ ] %MEM
* [x] %CPU
* [ ] VSZ
* [ ] RSS
* [ ] STAT

#### Q. What is the PPID of a process?

* [ ] Previous Process ID
* [x] Parent Process ID
* [ ] Primary Process ID
* [ ] Pending Process ID
* [ ] Priority Process ID

#### Q. Which command displays processes in a tree structure showing parent-child relationships?

* [ ] `ps aux`
* [ ] `ps -ef`
* [x] `ps --forest`
* [ ] `top`
* [ ] `pgrep -l`

#### Q. What is the first process (PID 1) called on systemd-based Linux distributions?

* [ ] `init`
* [x] `systemd`
* [ ] `bash`
* [ ] `kernel`
* [ ] `boot`

#### Q. Which signal pauses a process but allows it to be resumed later?

* [ ] SIGKILL
* [ ] SIGTERM
* [ ] SIGINT
* [x] SIGSTOP
* [ ] SIGHUP

#### Q. Which signal resumes a paused process?

* [ ] SIGSTART
* [x] SIGCONT
* [ ] SIGRESUME
* [ ] SIGRUN
* [ ] SIGWAKE

#### Q. What is a zombie process?

* [ ] A process consuming excessive CPU
* [ ] A process that cannot be killed
* [x] A terminated process whose parent hasn't read its exit status
* [ ] A daemon process
* [ ] A suspended process

#### Q. Which command finds the PID of a process by name?

* [ ] `ps name`
* [ ] `findpid`
* [x] `pgrep`
* [ ] `pid`
* [ ] `getpid`

#### Q. What does the `htop` command provide over `top`?

* [ ] Less CPU usage
* [x] Interactive interface with mouse support and better visuals
* [ ] Faster process listing
* [ ] Only shows system processes
* [ ] Text-only output

#### Q. Which `ps` option shows all processes for all users?

* [ ] `-u`
* [x] `-e`
* [ ] `-p`
* [ ] `-a`
* [ ] `-x`

#### Q. What happens when you send SIGHUP to a process?

* [x] The process receives a hangup signal, often used to reload configuration
* [ ] The process is immediately terminated
* [ ] The process is paused
* [ ] The process is resumed
* [ ] Nothing happens

#### Q. Which C function creates a copy of the current process?

* [ ] `exec()`
* [x] `fork()`
* [ ] `spawn()`
* [ ] `clone()`
* [ ] `create()`

#### Q. What does the `nohup` command do when running a process?

* [ ] Runs the process with higher priority
* [x] Makes the process ignore SIGHUP signals
* [ ] Runs the process as root
* [ ] Pauses the process
* [ ] Kills the process

#### Q. Which signal number corresponds to SIGKILL?

* [ ] 1
* [ ] 2
* [x] 9
* [ ] 15
* [ ] 19

#### Q. What does the `+` symbol indicate next to a job number in `jobs` output?

* [x] It is the current (default) job
* [ ] The job is paused
* [ ] The job has high priority
* [ ] The job is a daemon
* [ ] The job is complete

#### Q. Which command shows processes sorted by memory usage in real-time?

* [ ] `ps --sort=mem`
* [ ] `pgrep -m`
* [x] `top` (then press M)
* [ ] `memstat`
* [ ] `free -p`

#### Q. How do you filter processes by a specific user in `ps`?

* [ ] `ps -e user`
* [x] `ps -u username`
* [ ] `ps --filter user`
* [ ] `ps -user username`
* [ ] `ps -a username`

#### Q. What is the difference between a process and a thread?

* [ ] Threads are faster than processes
* [x] A process has its own memory space; threads share memory within a process
* [ ] Processes can only run one at a time
* [ ] Threads cannot communicate with each other
* [ ] There is no difference

#### Q. Which command shows the process tree with parent-child relationships?

* [ ] `ps aux`
* [x] `pstree`
* [ ] `top`
* [ ] `htop`
* [ ] `jobs`

#### Q. What is a zombie process?

* [ ] A process using too much CPU
* [ ] A process that cannot be killed
* [x] A terminated process whose parent hasn't read its exit status
* [ ] A process running in the background
* [ ] A process waiting for I/O

#### Q. Which command shows the current status and recent logs for the `nginx` systemd service?

* [ ] `service nginx info`
* [ ] `journalctl nginx`
* [ ] `systemctl logs nginx`
* [x] `systemctl status nginx`
* [ ] `ps -ef | grep nginx`

#### Q. Which command displays the parent process ID (PPID) of a process?

* [ ] `ps -p`
* [x] `ps -o ppid`
* [ ] `ps aux`
* [ ] `top -p`
* [ ] `pgrep -P`

#### Q. What does the `nice` command do?

* [ ] Terminates a process politely
* [x] Starts a process with a specified priority
* [ ] Pauses a process
* [ ] Resumes a suspended process
* [ ] Lists nice processes

#### Q. Which command changes the priority of a running process?

* [ ] `nice`
* [x] `renice`
* [ ] `priority`
* [ ] `setpri`
* [ ] `chprio`

#### Q. What is the range of nice values in Linux?

* [ ] 0 to 100
* [ ] 1 to 20
* [x] -20 to 19
* [ ] -100 to 100
* [ ] 0 to 39

#### Q. Which nice value gives a process the highest priority?

* [ ] 19
* [ ] 0
* [x] -20
* [ ] 1
* [ ] 100

#### Q. What does the `&` symbol do when placed at the end of a command?

* [ ] Redirects output to a file
* [x] Runs the command in the background
* [ ] Chains multiple commands
* [ ] Makes the command run faster
* [ ] Suppresses error output

#### Q. Which command displays only your own processes?

* [ ] `ps aux`
* [x] `ps -u $USER`
* [ ] `top`
* [ ] `pgrep`
* [ ] `jobs`

#### Q. What does the `wait` command do in shell scripting?

* [ ] Pauses for a specified time
* [x] Waits for background processes to complete
* [ ] Waits for user input
* [ ] Suspends the current process
* [ ] Waits for network connection

#### Q. Which signal is sent by the `kill -9` command?

* [ ] SIGTERM
* [ ] SIGINT
* [x] SIGKILL
* [ ] SIGHUP
* [ ] SIGSTOP

#### Q. What is the default signal sent by the `kill` command?

* [ ] SIGKILL (9)
* [x] SIGTERM (15)
* [ ] SIGINT (2)
* [ ] SIGHUP (1)
* [ ] SIGSTOP (19)

#### Q. Which command shows system load average?

* [ ] `ps aux`
* [x] `uptime`
* [ ] `free`
* [ ] `vmstat`
* [ ] `df`

#### Q. What do the three numbers in load average represent?

* [ ] CPU, memory, and disk usage
* [x] Average load over 1, 5, and 15 minutes
* [ ] User, system, and idle time
* [ ] Read, write, and wait operations
* [ ] Process count at different times
