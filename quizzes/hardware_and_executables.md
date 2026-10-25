# Hardware, Executables and Disk I/O Quiz

Notes: [Hardware](../notes/hardware.md), [Running Executables](../notes/running_executables.md), [Disk I/O Analysis](../notes/disk_io_analysis.md)

Check your understanding of hardware inventory tools, how Linux finds and starts programs, shared libraries, and how to read disk I/O statistics.

#### Q. On a server with a non-hybrid CPU, `lscpu` prints the lines below. How many logical CPUs does the kernel schedule on?

```text
Thread(s) per core:  2
Core(s) per socket:  8
Socket(s):           2
```

* [ ] 8
* [ ] 16
* [x] 32
* [ ] 64

> **Explanation:** Logical CPUs = sockets × cores per socket × threads per core = 2 × 8 × 2 = 32, which `lscpu` also prints as `CPU(s)`. CPUs that mix performance and efficiency cores (such as recent Intel desktop chips) break this simple product.

#### Q. Which command prints the number of logical CPUs listed in `/proc/cpuinfo`?

* [ ] `grep -m1 'cpu cores' /proc/cpuinfo`
* [x] `grep -c '^processor' /proc/cpuinfo`
* [ ] `grep -m1 'physical id' /proc/cpuinfo`
* [ ] `wc -l /proc/cpuinfo`

> **Explanation:** `/proc/cpuinfo` has one block per logical CPU, each starting with a `processor` line, so counting them matches `nproc` (when no CPU affinity limit applies). The first `cpu cores` line gives the cores per socket, and `physical id` names a socket.

#### Q. `free -h` prints the output below. Is the system short of memory?

```text
               total        used        free      shared  buff/cache   available
Mem:            31Gi       8,5Gi       2,9Gi        75Mi        20Gi        22Gi
Swap:          2,0Gi          0B       2,0Gi
```

* [ ] Yes, only 2.9 GiB is free, so new programs will start swapping
* [x] No, about 22 GiB is available because most of the page cache can be reclaimed
* [ ] Yes, `buff/cache` is using 20 GiB that programs can never get back
* [ ] No, because swap is empty and 2 GiB of swap is always enough

> **Explanation:** Linux fills idle RAM with page cache. The `available` column (from `MemAvailable` in `/proc/meminfo`) estimates how much memory new programs can use without swapping, including reclaimable cache. `free` alone is not a useful measure.

#### Q. Which command shows which block devices are rotational hard disks rather than SSDs?

* [ ] `lsblk -f`
* [ ] `lsblk -m`
* [ ] `lspci -k`
* [x] `lsblk -d -o NAME,ROTA`

> **Explanation:** The `ROTA` column is `1` for a rotational disk and `0` for SSD or NVMe, and `-d` hides partitions. `lsblk -f` shows filesystem type, label, UUID and mount points; `lsblk -m` shows device permissions.

#### Q. You need the filesystem type and UUID of every partition, for example to write an `/etc/fstab` entry. Which command shows them without root?

* [x] `lsblk -f`
* [ ] `lsblk -d`
* [ ] `lscpu -e`
* [ ] `lsusb -t`

> **Explanation:** `lsblk -f` adds `FSTYPE`, `LABEL`, `UUID`, free space and mount points to the device tree. `blkid` shows similar data but may need root to probe devices it has not cached.

#### Q. Which command shows the kernel driver in use for each PCI device, such as a network card or GPU?

* [ ] `lsusb -v`
* [ ] `lspci -t`
* [x] `lspci -k`
* [ ] `lsmod -k`

> **Explanation:** `lspci -k` adds `Kernel driver in use:` and `Kernel modules:` lines under each device. That is the quickest way to see whether, for example, an NVIDIA GPU uses `nvidia` or `nouveau`. `lspci -t` shows the bus tree, and `lsmod` has no `-k` option.

#### Q. `lsusb` prints `Bus 001 Device 002: ID 05e3:0610 Genesys Logic, Inc. Hub`. What is `05e3:0610`?

* [x] The USB vendor ID and product ID
* [ ] The bus number and port number
* [ ] The device's serial number
* [ ] The major and minor device numbers

> **Explanation:** USB and PCI devices carry a vendor ID and a product (device) ID in hexadecimal. They are the best search terms for driver support. `lspci -nn` prints the PCI equivalent, such as `[8086:4668]`.

#### Q. Which command shows each installed RAM module with its size, speed and slot, and why does it need `sudo`?

* [ ] `free -h`, because it reads root-only kernel memory
* [ ] `lscpu --caches`, because the RAM layout is stored in the CPU
* [ ] `cat /proc/meminfo`, because the file is readable only by root
* [x] `sudo dmidecode -t memory`, because it reads the firmware's SMBIOS tables, which only root can read

> **Explanation:** `dmidecode` decodes the SMBIOS/DMI tables provided by the firmware: system, board, BIOS and memory slots. As a normal user it fails with `/sys/firmware/dmi/tables/smbios_entry_point: Permission denied`. `free` and `/proc/meminfo` only show totals.

#### Q. `ls -l /dev/null /dev/nvme0n1` prints the lines below. What do the first characters `c` and `b` mean?

```text
crw-rw-rw- 1 root root   1, 3 Oct 25 10:10 /dev/null
brw-rw---- 1 root disk 259, 0 Oct 25 10:10 /dev/nvme0n1
```

* [x] `c` is a character device and `b` is a block device
* [ ] `c` is a configuration file and `b` is a binary file
* [ ] `c` means the device is closed and `b` means it is busy
* [ ] `c` is a container device and `b` is a bus device

> **Explanation:** Device files have a type, permissions and a major/minor number pair that selects the driver. Block devices such as disks are accessed in blocks; character devices such as terminals and `/dev/null` are byte streams. The `disk` group controls raw disk access.

#### Q. What do the first four bytes of every ELF executable contain?

* [x] The magic number `0x7f` followed by `ELF`
* [ ] `#!` followed by the interpreter path
* [ ] The entry point address
* [ ] The size of the file in bytes

> **Explanation:** `head -c 4 /bin/ls | od -c` prints `177 E L F` (177 is octal for `0x7f`). The kernel and `file` use this magic number to recognise ELF; scripts instead start with `#!`.

#### Q. `file /bin/ls` reports `dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2`. What is that interpreter?

* [ ] The shell that runs `ls` when it is started from a script
* [ ] A compatibility layer that runs 32-bit programs
* [ ] A debugger that the kernel attaches when the program crashes
* [x] The dynamic linker, which the kernel starts to load the shared libraries before `main` runs

> **Explanation:** A dynamically linked ELF file has a `PT_INTERP` program header naming the dynamic linker, shown by `readelf -l /bin/ls | grep interpreter`. The kernel maps the program and this linker; the linker loads libraries such as `libc.so.6`, then jumps to the program's entry point.

#### Q. Which command prints the entry point address of an ELF executable?

* [x] `readelf -h ./hello`
* [ ] `ldd ./hello`
* [ ] `file -i ./hello`
* [ ] `strace -c ./hello`

> **Explanation:** `readelf -h` shows the ELF header, including `Class`, `Machine` and `Entry point address`. `readelf -l` lists the program headers (segments and interpreter), and `readelf -d` lists the dynamic section with `NEEDED` libraries.

#### Q. You build `gcc -static -o hello-static hello.c`. What does `ldd hello-static` print?

* [ ] Only `libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6`
* [x] `not a dynamic executable`
* [ ] `libc.so.6 => not found`
* [ ] The same list as for a dynamically linked build

> **Explanation:** A static binary contains the library code it uses and has no `PT_INTERP` header, so there is nothing for `ldd` to resolve (it also exits with status 1). `file` describes such a binary as `statically linked`. Static binaries suit minimal initramfs environments.

#### Q. You copy `/bin/busybox` from an Alpine container to an Ubuntu host. `ls -l` shows it, but `./busybox echo hi` prints the error below. Why?

```text
bash: ./busybox: cannot execute: required file not found
```

* [ ] The file lost its execute permission during the copy
* [x] Its ELF interpreter `/lib/ld-musl-x86_64.so.1` does not exist on the host
* [ ] Ubuntu refuses to run binaries that were built on another distribution
* [ ] The binary is for a different CPU architecture

> **Explanation:** `file busybox` shows `interpreter /lib/ld-musl-x86_64.so.1`. When the interpreter is missing, `execve` fails with `ENOENT`, which bash 5.2 reports as `required file not found` (older versions say `No such file or directory`) although the program file exists. A wrong architecture gives `Exec format error`.

#### Q. A script named `show` has the first line `#!/bin/echo hello`. What does `./show a b` print?

* [ ] `hello`
* [ ] `hello a b`
* [x] `hello ./show a b`
* [ ] `./show a b`

> **Explanation:** For a `#!` file, the kernel runs the interpreter with the optional shebang argument, then the script's path, then the original arguments: `/bin/echo hello ./show a b`. That is how `#!/bin/sh` scripts end up as `/bin/sh ./script args`.

#### Q. A script starts with `#!/usr/bin/env python3 -u`. Running it on Linux prints `/usr/bin/env: 'python3 -u': No such file or directory`. Why?

* [x] Linux passes everything after the interpreter path as one argument, so `env` looks for a program named `python3 -u`
* [ ] `env` cannot start Python and needs the full path `/usr/bin/python3`
* [ ] The `-u` option is not valid for Python 3
* [ ] Shebang lines may not contain spaces at all

> **Explanation:** The kernel splits a shebang only once, after the interpreter path. GNU `env -S` splits the rest itself, so `#!/usr/bin/env -S python3 -u` works, as `env`'s own hint says.

#### Q. A script copied from Windows runs fine with `sh deploy.sh`, but `./deploy.sh` fails with `cannot execute: required file not found`. `file deploy.sh` reports `with CRLF line terminators`. What is wrong?

* [ ] The script has no execute permission
* [ ] `/bin/sh` is not installed on the system
* [x] The shebang line ends with a carriage return, so the kernel looks for an interpreter named `/bin/sh\r`
* [ ] Windows scripts must be run through `wine`

> **Explanation:** The kernel takes the interpreter path up to the newline, so the trailing `\r` becomes part of the file name, which does not exist. Running `sh deploy.sh` bypasses the shebang. Convert the file with `dos2unix` or `sed -i 's/\r$//'`.

#### Q. A script has mode `-rw-r--r--` (644). What happens with `./s.sh` and with `bash s.sh`?

* [ ] Both fail with `Permission denied`
* [ ] Both run, because the file is readable
* [ ] `./s.sh` runs; `bash s.sh` fails because bash checks the `x` bit
* [x] `./s.sh` fails with `Permission denied` (status 126); `bash s.sh` runs the script

> **Explanation:** Executing a file with `execve` needs the execute bit. `bash s.sh` executes `/bin/bash`, which only reads the script, so read permission is enough. `chmod +x s.sh` lets `./s.sh` work.

#### Q. You set mode `--x--x--x` (111) on a compiled binary `hx` and on a shell script `s.sh`, both owned by you. What happens when you run each with `./`?

* [x] `./hx` runs; `./s.sh` fails because the interpreter cannot read the script
* [ ] Both run, because both have execute permission
* [ ] Both fail, because every executable also needs read permission
* [ ] `./s.sh` runs; `./hx` fails because the kernel must read the binary

> **Explanation:** For an ELF binary the kernel maps the file itself, so execute permission is enough. For a script the kernel starts `/bin/sh ./s.sh`, and the shell must open the file for reading: `/bin/sh: 0: cannot open ./s.sh: Permission denied`.

#### Q. `/t` is mounted with `noexec`. Both `/t/hello` (an ELF binary) and `/t/s.sh` have mode 755. What happens?

* [ ] Both run, because `noexec` only blocks setuid programs
* [x] `/t/hello` and `/t/s.sh` fail with `Permission denied`, but `sh /t/s.sh` still runs the script
* [ ] Only the binary is blocked; `./s.sh` runs because scripts are not executables
* [ ] Every command that reads files from `/t`, including `cat`, fails

> **Explanation:** `noexec` makes `execve` of files on that mount fail. An interpreter that only reads a script is not affected, so `noexec` on `/tmp` is a hardening layer, not a complete barrier. Starting the binary through `ld-linux` also fails (`failed to map segment from shared object`).

#### Q. An executable text file `nos.sh` has no `#!` line. What happens when you run `./nos.sh` from bash, and when Python runs `subprocess.run(["./nos.sh"])`?

* [ ] Both fail with `Exec format error`
* [ ] Both run it with `/bin/sh`, because the kernel defaults to the shell
* [x] Bash runs it as a shell script itself; Python gets `OSError: [Errno 8] Exec format error`
* [ ] Bash refuses with `bad interpreter`; Python runs it with `/bin/sh`

> **Explanation:** The kernel's `execve` fails with `ENOEXEC` because the file is neither ELF nor `#!`. Bash catches this and interprets the file in a subshell, but programs that call `execve` directly just get the error. Always add a shebang.

#### Q. A program `hello` is in the current directory. Why does `hello` give `command not found` while `./hello` works?

* [ ] The shell only searches the current directory for programs owned by root
* [ ] `hello` must first be registered with `hash -p`
* [ ] Programs without a file extension must always be run with a path
* [x] A name without a slash is looked up in `PATH`, and `PATH` does not contain the current directory

> **Explanation:** A command containing `/` is run as a path, while a bare name is searched in `PATH`. Leaving `.` out of `PATH` is a security measure: otherwise a malicious `ls` placed in a shared directory such as `/tmp` could run whenever you typed `ls` there.

#### Q. A user sets `PATH=/usr/local/bin:/usr/bin:` in their profile. What does the trailing colon do?

* [ ] Nothing; empty entries in `PATH` are ignored
* [x] It adds the current directory to the end of the search path
* [ ] It adds the user's home directory to the search path
* [ ] It makes the shell print an error at login

> **Explanation:** An empty `PATH` entry (leading, trailing or `::`) means the current directory, just like `.`. With this setting, `cd` into a directory holding `hello` and typing `hello` runs `./hello`, which brings back the risk that leaving `.` out of `PATH` is meant to avoid.

#### Q. `PATH` begins with `/opt/b1:/opt/b2`, and both directories contain an executable `tool`. Which command shows every match, in search order?

* [ ] `which tool`
* [ ] `command -v tool`
* [x] `type -a tool`
* [ ] `hash -l tool`

> **Explanation:** The first match in `PATH` order wins, so `tool` runs `/opt/b1/tool`. `type -a` lists all matches (and aliases, functions or builtins of that name); `which` and `command -v` print only the one that would run.

#### Q. In a running bash session you ran `tool` (found in `/opt/b1`), then deleted `/opt/b1/tool`. Now `tool` prints `/opt/b1/tool: No such file or directory` although `/opt/b2/tool` exists. What fixes it?

* [ ] `export PATH`
* [x] `hash -r`
* [ ] `source ~/.bashrc`
* [ ] `rehash /opt/b2`

> **Explanation:** Bash caches the full path of each command it has found. When the cached file disappears, bash reports the error instead of searching again. `hash -r` clears the cache (`hash -d tool` removes one entry), and the next `tool` finds `/opt/b2/tool`.

#### Q. Which statement about the `execve` system call is true?

* [ ] It searches `PATH` when the program name contains no slash
* [ ] It creates a new child process and returns its PID
* [x] It needs a pathname and replaces the calling process's program, keeping the same PID
* [ ] It returns 0 to the old program after the new one finishes

> **Explanation:** `execve` never searches `PATH`; the shell or library functions like `execvp` do that and then call `execve`. A successful `execve` does not return, because the old program image is gone. Shells `fork` first so the child is replaced, not the shell.

#### Q. A program fails at start-up with the message below. What does it mean?

```text
./app: error while loading shared libraries: libwho.so: cannot open shared object file: No such file or directory
```

* [x] The dynamic linker cannot find `libwho.so` in any directory it searches
* [ ] The file `./app` does not exist
* [ ] `libwho.so` exists but has no execute permission
* [ ] The program crashed in `main` while opening a file

> **Explanation:** The program file was found, but the dynamic linker could not resolve a `NEEDED` library, and the shell reports status 127. `ldd ./app` shows `libwho.so => not found`. Fix it with `LD_LIBRARY_PATH` for a test, or with `/etc/ld.so.conf.d/` and `ldconfig`.

#### Q. `app` was linked with a `RUNPATH` of `/opt/libA`, which contains `libwho.so`. `/opt/libB` holds a different `libwho.so`. Which copy does `LD_LIBRARY_PATH=/opt/libB ./app` load?

* [ ] `/opt/libA/libwho.so`, because paths in the binary always win
* [x] `/opt/libB/libwho.so`, because `LD_LIBRARY_PATH` is searched before `RUNPATH`
* [ ] Neither, because the dynamic linker refuses to choose between two copies
* [ ] The two copies are loaded, and the first symbol found is used

> **Explanation:** glibc searches the older `DT_RPATH` first, then `LD_LIBRARY_PATH`, then `DT_RUNPATH`, then `/etc/ld.so.cache` and the default directories. Modern linkers write `RUNPATH`; linking with `--disable-new-dtags` writes `RPATH`, which would make `/opt/libA` win.

#### Q. You installed a library in `/opt/myapp/lib` and want every program on the system to find it. What is the standard fix?

* [ ] Add `export LD_LIBRARY_PATH=/opt/myapp/lib` to `/etc/environment`
* [ ] Copy the library into the program's directory
* [ ] Run `ldd --update /opt/myapp/lib`
* [x] Add the directory to a file in `/etc/ld.so.conf.d/` and run `sudo ldconfig`

> **Explanation:** `ldconfig` rebuilds `/etc/ld.so.cache`, which the dynamic linker consults after `RPATH`, `LD_LIBRARY_PATH` and `RUNPATH`. Check the result with `ldconfig -p | grep myapp`. A global `LD_LIBRARY_PATH` affects every program and causes version conflicts.

#### Q. Why should you avoid running `ldd` on an untrusted binary?

* [ ] `ldd` modifies the binary's dynamic section
* [ ] `ldd` uploads the binary to check it against a library database
* [x] `ldd` may run the program's own loader code, which could execute arbitrary code
* [ ] `ldd` needs root and may change the system library cache

> **Explanation:** On glibc, `ldd` is a shell script that runs the binary's dynamic linker in a tracing mode, and a crafted binary can name its own interpreter. To see direct dependencies safely, use `objdump -p ./prog | grep NEEDED` or `readelf -d ./prog`.

#### Q. Why does the dynamic linker ignore `LD_LIBRARY_PATH` when a normal user runs a setuid-root program such as `passwd`?

* [ ] Setuid programs are always statically linked
* [ ] The kernel clears every environment variable for setuid programs
* [ ] `LD_LIBRARY_PATH` only works for programs owned by the current user
* [x] In secure-execution mode it would let the user inject a library into a privileged process

> **Explanation:** When the effective and real user IDs differ, `ld.so` runs in secure-execution mode and ignores or removes variables such as `LD_LIBRARY_PATH` and `LD_PRELOAD`. Otherwise any user could load a malicious `libc` into a root-owned process.

#### Q. You run `strace -e trace=execve bash -c 'ls | wc -l'`. Why does the trace show only bash's own `execve`, not those of `ls` and `wc`?

* [x] Without `-f`, `strace` does not follow the child processes that bash forks
* [ ] Pipelines are run by the kernel without calling `execve`
* [ ] `ls` and `wc` are bash builtins
* [ ] `-e trace=execve` shows only the first matching call

> **Explanation:** `ls` and `wc` run in children created by `fork`/`clone`. `strace -f` follows them and shows `execve("/usr/bin/ls", ...)` and `execve("/usr/bin/wc", ...)` with their PIDs. Add `-o file` to keep the trace apart from the program's output.

#### Q. Which `strace` option prints a table of system call counts, errors and time instead of each call?

* [ ] `-f`
* [ ] `-t`
* [x] `-c`
* [ ] `-p`

> **Explanation:** `strace -c ls` prints a summary with `% time`, `seconds`, `calls`, `errors` and `syscall` columns, which shows quickly which calls dominate or fail. `-f` follows children, `-t` adds timestamps and `-p PID` attaches to a running process.

#### Q. You run `strace -e trace=execve ./hello.sh`, where `hello.sh` starts with `#!/bin/sh`. What does the trace show?

* [ ] Two calls: `execve("./hello.sh", ...)` and then `execve("/bin/sh", ...)`
* [ ] Only `execve("/bin/sh", ["/bin/sh", "./hello.sh"], ...)`
* [ ] No `execve`, because scripts are read by the kernel without executing anything
* [x] One call, `execve("./hello.sh", ["./hello.sh"], ...) = 0`, because the kernel switches to the interpreter inside that call

> **Explanation:** The shebang is handled inside the same `execve`: the kernel's script handler finds `#!/bin/sh` and loads `/bin/sh` with the script path as an argument. User space never makes a second `execve` call.

#### Q. You run `iostat -x 1 5` and the first report is very different from the next four. Why?

* [ ] The first sample is taken before the disks have woken up
* [x] The first report shows averages since boot; later ones cover each 1-second interval
* [ ] `iostat` skips the first second, so the first report is empty
* [ ] The first report covers only the root disk

> **Explanation:** Both `iostat` and `vmstat` print their first report from counters accumulated since boot. Ignore it when you are looking at current load, or use `iostat -y` to omit it.

#### Q. What does the `await` column in `iostat -x` measure?

* [ ] The time the CPU spent idle while I/O was pending
* [ ] The time the disk itself spent transferring data, excluding queueing
* [ ] The number of requests waiting in the queue
* [x] The average time per I/O request in milliseconds, including time spent queued and being serviced

> **Explanation:** `await` (split into `r_await` and `w_await`) is the latency applications see from the block layer. A rise usually means queueing. The number of requests waiting is `aqu-sz`, and CPU idle time with pending I/O is `%iowait`.

#### Q. `iostat -x` shows an NVMe SSD at `%util` 100 with low `await`. Is the SSD saturated?

* [x] Not necessarily; `%util` only counts time with at least one request in flight, and NVMe drives serve many requests in parallel
* [ ] Yes; 100 % utilization always means the device can do no more work
* [ ] No; `%util` is meaningless for every kind of disk
* [ ] Yes, but only if `%iowait` is also 100

> **Explanation:** The `iostat` man page says `%util` near 100 % means saturation for devices that serve requests one at a time, like a single HDD. For SSDs and RAID arrays, check `await` and `aqu-sz` against the device's known limits.

#### Q. What does `%iowait` (`wa` in `top` and `vmstat`) actually measure?

* [ ] The percentage of time each disk is busy
* [x] The share of CPU time that was idle while at least one disk I/O request was outstanding
* [ ] The share of CPU time spent inside disk drivers
* [ ] The percentage of processes in the `D` state

> **Explanation:** iowait is a kind of idle time. On a machine with many CPUs, one process blocked on I/O hardly moves the system-wide average, so a low value does not prove the disks are fine. Confirm with `iostat -x` and per-process tools.

#### Q. `vmstat 1` prints the line below. What is the most likely bottleneck?

```text
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  8      0 300000  20000 900000    0    0    10 85000 2000 4000  3  4 20 73  0
```

* [ ] CPU, because the run queue `r` is above zero
* [ ] Memory, because `free` is low
* [x] Disk writes: 8 processes blocked on I/O, heavy `bo` and 73 % iowait
* [ ] Network, because interrupts `in` are high

> **Explanation:** `b` counts processes blocked waiting for I/O, `bo` is KiB/s written to block devices and `wa` is iowait. `si` and `so` are 0, so this is not swapping. Next, find the writer with `iotop -o` or `pidstat -d 1`.

#### Q. A slow server shows high `si` and `so` in `vmstat` together with high disk activity. What is the likely root cause?

* [ ] A failing disk that needs replacing
* [ ] Too many CPU cores competing for the disk
* [ ] An I/O scheduler set to `none`
* [x] Memory pressure that forces pages to and from swap

> **Explanation:** `si` and `so` are memory swapped in from and out to disk per second. When they stay high, the disk load comes from swapping, so the fix is to reduce memory use or add RAM, not to buy a faster disk.

#### Q. Which command shows, live, only the processes and threads that are currently doing disk I/O?

* [ ] `iostat -xz 1`
* [ ] `vmstat -d 1`
* [x] `sudo iotop -o`
* [ ] `top -o %IO`

> **Explanation:** `iotop` shows per-thread read and write bandwidth and the share of time spent waiting on I/O; `-o` hides idle ones, `-P` shows processes instead of threads and `-a` shows totals since start. It needs root. `iostat` and `vmstat -d` report per device, not per process.

#### Q. `iostat -x` shows `r/s` 5000 and `rkB/s` 20000 for a disk. What kind of workload is this?

* [ ] Large sequential reads, such as copying a video file
* [x] Many small reads of about 4 KiB each, typical of random I/O
* [ ] Mostly writes, because reads are shown separately
* [ ] An idle disk, because 20000 kB/s is very low

> **Explanation:** 20000 kB/s ÷ 5000 reads/s = 4 KiB per request (`iostat` also shows this as `rareq-sz`). High IOPS with small requests suggests database or metadata-heavy random access, which suffers most on HDDs. Large sequential I/O shows high throughput with fewer, larger requests.

#### Q. `cat /sys/block/nvme0n1/queue/scheduler` prints `[none] mq-deadline`. What does this tell you?

* [x] The `none` scheduler is active, and `mq-deadline` is also available for this device
* [ ] `mq-deadline` is active, and `none` would disable the device
* [ ] The device has no scheduler support, so I/O is refused
* [ ] Both schedulers are used in turn, one per request

> **Explanation:** The scheduler in brackets is active. Fast NVMe devices often default to `none` because reordering helps little without seek time. Writing a name to this file as root changes it until reboot; `bfq` or `kyber` appear only if their modules are available.
