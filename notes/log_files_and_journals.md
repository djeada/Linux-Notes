## Log Files, Journals, and Logging Systems

Understanding how logging works in Linux is like learning the language your system uses to communicate. Logs are the detailed records that your system keeps about its activities, and they are invaluable for troubleshooting, monitoring performance, and ensuring security. Let's embark on a journey to demystify log files, journals, and the various logging systems used in Linux.

### What Is a Log?

A **log** is a record of events produced by an operating system, application, service, script, device, or security component.

Logs answer questions like:

* What happened?
* When did it happen?
* Who or what caused it?
* Was it normal, suspicious, or broken?
* Where should I look next?

A typical log entry contains:

```text
+--------------------------------------------------------------------------------+
| TIMESTAMP           | SEVERITY | SOURCE / SERVICE | MESSAGE                    |
|---------------------|----------|------------------|----------------------------|
| 2026-05-03 09:00:01 | INFO     | nginx            | Server started             |
| 2026-05-03 09:01:10 | WARNING  | kernel           | CPU temperature high       |
| 2026-05-03 09:02:44 | ERROR    | myapp            | Database connection failed |
+--------------------------------------------------------------------------------+
```

#### Important Parts of a Log Entry

```text
May 03 09:02:44 web01 myapp[1234]: ERROR Database connection failed
│              │     │     │        │
│              │     │     │        └── Message
│              │     │     └────────── Process ID
│              │     └──────────────── Service / program name
│              └────────────────────── Hostname
└───────────────────────────────────── Timestamp
```

#### Why Logs Matter

Logs are used for:

```text
+--------------------+--------------------------------------------------+
| Purpose            | Example                                          |
|--------------------|--------------------------------------------------|
| Troubleshooting    | Why did nginx fail to start?                     |
| Security           | Who tried to SSH into the server?                |
| Auditing           | Who used sudo?                                   |
| Monitoring         | Is disk space filling up?                        |
| Performance        | Why is the app slow?                             |
| Compliance         | Can we prove access attempts were recorded?      |
+--------------------+--------------------------------------------------+
```

Without logs, debugging becomes guessing.

With logs, debugging becomes investigation.

### The Linux Logging Landscape

Linux systems usually have more than one logging system working together.

```text
#
                         +----------------------+
                         |      Applications    |
                         | Python, nginx, SSHD  |
                         +----------+-----------+
                                    |
                                    v
+-------------+           +---------+----------+          +----------------+
|   Kernel    |---------> | systemd-journald   | -------> | journalctl     |
|  hardware   |           | binary journal     |          | query journal  |
+-------------+           +---------+----------+          +----------------+
                                    |
                                    v
                         +----------+-----------+
                         | rsyslog / syslog     |
                         | text log routing     |
                         +----------+-----------+
                                    |
                                    v
                         +----------+-----------+
                         | /var/log/*.log       |
                         | plain text logs      |
                         +----------------------+
```

Modern Linux systems commonly use:

| System     | Purpose                                             |
| ---------- | --------------------------------------------------- |
| journald   | Collects structured logs from systemd, kernel, apps |
| journalctl | Reads and filters journald logs                     |
| rsyslog    | Routes logs into text files or remote log servers   |
| /var/log   | Directory where many plain-text logs live           |
| logrotate  | Rotates, compresses, and deletes old text logs      |
| logger     | Sends custom log messages from shell scripts        |
| dmesg      | Reads kernel ring buffer messages                   |

### Common Linux Log Locations

Most traditional logs live under:

```bash
/var/log
```

Example:

```text
/var/log/
├── syslog
├── auth.log
├── kern.log
├── dmesg
├── boot.log
├── dpkg.log
├── apt/
│   ├── history.log
│   └── term.log
├── nginx/
│   ├── access.log
│   └── error.log
├── apache2/
│   ├── access.log
│   └── error.log
├── mysql/
├── postgresql/
├── journal/
└── rotated logs:
    ├── syslog.1
    ├── syslog.2.gz
    └── auth.log.1.gz
```

Different distributions use different files.

For example:

```text
Debian / Ubuntu:
  /var/log/syslog
  /var/log/auth.log

RHEL / CentOS / Fedora:
  /var/log/messages
  /var/log/secure
```

### Plain Text Logs

Plain text logs are ordinary files you can read with tools like:

- `cat`
- `less`
- `tail`
- `grep`
- `awk`
- `sed`

Example:

```bash
sudo tail -n 50 /var/log/syslog
```

Example log lines:

```text
May 03 10:15:42 web01 NetworkManager[1234]: device eth0 state changed
May 03 10:15:45 web01 kernel: eth0: Link is Down
May 03 10:16:01 web01 CRON[2222]: (root) CMD (/usr/local/bin/backup.sh)
```

#### Anatomy of a Syslog Line

```text
May 03 10:16:01 web01 CRON[2222]: (root) CMD (/usr/local/bin/backup.sh)
│              │     │    │       │
│              │     │    │       └── Message
│              │     │    └────────── PID
│              │     └─────────────── Program
│              └──────────────────── Hostname
└─────────────────────────────────── Timestamp
```

### Journald and `journalctl`

Many modern Linux distributions use **systemd-journald**.

`journald` collects logs from:

```text
+-------------------------+
|     systemd-journald    |
+-----------+-------------+
            ^
            |
+-----------+------------+----------------+----------------+----------------+
|                        |                |                |                |
| systemd services       | kernel         | applications   | stdout/stderr  |
| nginx.service          | hardware       | custom apps    | service logs   |
+------------------------+----------------+----------------+----------------+
```

Unlike plain text logs, the systemd journal is structured and usually stored in binary format.

You do not normally read the journal file directly.

You use:

```bash
journalctl
```

#### Basic `journalctl` Commands

View all logs:

```bash
journalctl
```

This command displays all logs stored in the systemd journal. It shows logs from system services, kernel messages, user sessions, boot activity, and other system events. By default, the output is shown in a pager, so you can scroll through it using keyboard controls.

Example output:

```text
May 03 09:15:01 server systemd[1]: Started Session 12 of User root.
May 03 09:15:05 server sshd[1245]: Accepted publickey for admin from 192.168.1.20
May 03 09:15:10 server sudo[1302]: admin : TTY=pts/0 ; COMMAND=/usr/bin/systemctl status nginx
```

Explanation:

* Shows all available journal entries.
* Useful for general troubleshooting.
* Can produce a large amount of output on active systems.
* Press `q` to exit the log viewer.

View newest logs:

```bash
journalctl -n 50
```

This command displays the newest 50 log entries. It is useful when you only want to inspect the most recent system activity instead of scrolling through the entire journal.

Example output:

```text
May 03 10:01:22 server nginx[2210]: Configuration file /etc/nginx/nginx.conf test is successful
May 03 10:01:23 server systemd[1]: Reloaded nginx.service - A high performance web server
May 03 10:02:01 server CRON[2250]: pam_unix(cron:session): session opened for user root
```

Explanation:

* `-n 50` limits the output to the last 50 log lines.
* Useful for checking recent errors or recent service activity.
* You can change `50` to any number, such as `100` or `200`.

Follow logs live:

```bash
journalctl -f
```

This command follows logs in real time. New log entries appear automatically as they are written to the journal. It works similarly to `tail -f`.

Example output:

```text
May 03 10:05:12 server sshd[2401]: Failed password for invalid user test from 203.0.113.10
May 03 10:05:15 server sshd[2401]: Connection closed by invalid user test 203.0.113.10
May 03 10:05:20 server nginx[2410]: 192.168.1.25 - - "GET / HTTP/1.1" 200
```

Explanation:

* Shows new log entries as they happen.
* Useful for live debugging.
* Commonly used while restarting a service or reproducing an issue.
* Press `Ctrl + C` to stop following logs.

View logs since boot:

```bash
journalctl -b
```

This command displays logs from the current system boot only. It filters out logs from previous boots and shows what has happened since the machine last started.

Example output:

```text
May 03 08:00:01 server kernel: Linux version 6.8.0
May 03 08:00:04 server systemd[1]: Starting system initialization...
May 03 08:00:15 server systemd[1]: Started ssh.service - OpenSSH server daemon
```

Explanation:

* `-b` means current boot.
* Useful for investigating startup problems.
* Helps separate current issues from older historical logs.
* Often used after a reboot or crash.

View previous boot:

```bash
journalctl -b -1
```

This command shows logs from the previous boot. It is useful when the system crashed, rebooted unexpectedly, or had an issue before the current startup.

Example output:

```text
May 02 22:41:03 server kernel: Out of memory: Killed process 1884
May 02 22:41:10 server systemd[1]: nginx.service: Failed with result 'exit-code'
May 02 22:42:01 server systemd[1]: Reached target Reboot
```

Explanation:

* `-b -1` means one boot before the current boot.
* Useful for checking why a system restarted.
* Helps troubleshoot crashes, failed shutdowns, and boot loops.
* `journalctl --list-boots` can be used to see available boot records.

View logs from the last hour:

```bash
journalctl --since "1 hour ago"
```

This command displays logs generated during the last hour. It is helpful when an issue happened recently and you do not want to search through older logs.

Example output:

```text
May 03 09:12:44 server docker[1805]: Container web_app started
May 03 09:25:10 server nginx[1921]: connect() failed while connecting to upstream
May 03 09:58:31 server sshd[2150]: Accepted password for deploy from 192.168.1.30
```

Explanation:

* `--since` filters logs by start time.
* `"1 hour ago"` is a relative time expression.
* Useful for recent troubleshooting.
* Other examples include `"10 minutes ago"` or `"yesterday"`.

View logs from a time range:

```bash
journalctl --since "2026-05-03 09:00" --until "2026-05-03 10:00"
```

This command displays logs between a specific start time and end time. It is useful when you know exactly when a problem occurred and want to inspect only that period.

Example output:

```text
May 03 09:05:14 server nginx[1602]: 502 Bad Gateway while reading response header from upstream
May 03 09:20:44 server postgresql[1710]: checkpoint complete
May 03 09:45:02 server systemd[1]: Started cleanup temporary files
```

Explanation:

* `--since` defines the beginning of the time range.
* `--until` defines the end of the time range.
* Useful for incident investigation.
* Time format should be clear and consistent, such as `YYYY-MM-DD HH:MM`.

#### Filter by Service

```bash
journalctl -u ssh.service
journalctl -u nginx.service
journalctl -u docker.service
journalctl -u postgresql.service
```

These commands display logs for specific systemd services. Filtering by service is one of the most common ways to use `journalctl` because it removes unrelated system messages and focuses only on the service you are troubleshooting.

Example output:

```text
May 03 10:12:01 server sshd[2501]: Server listening on 0.0.0.0 port 22
May 03 10:12:08 server sshd[2510]: Accepted publickey for admin from 192.168.1.20
May 03 10:12:10 server sshd[2510]: pam_unix(sshd:session): session opened for user admin
```

Explanation:

* `-u` filters logs by systemd unit name.
* Service names usually end in `.service`.
* Useful for debugging one service at a time.
* Common examples include `ssh.service`, `nginx.service`, `docker.service`, and `postgresql.service`.

Follow one service live:

```bash
journalctl -u nginx.service -f
```

This command follows only the logs from `nginx.service` in real time. It is useful when testing configuration changes, watching requests, or troubleshooting live service behavior.

Example output:

```text
May 03 10:20:01 server nginx[2701]: 192.168.1.50 - - "GET /api/status HTTP/1.1" 200
May 03 10:20:08 server nginx[2701]: 192.168.1.51 - - "POST /login HTTP/1.1" 302
May 03 10:20:12 server nginx[2701]: connect() failed while connecting to upstream
```

Explanation:

* `-u nginx.service` filters logs to Nginx only.
* `-f` follows new log entries live.
* Useful during reloads, restarts, and active testing.
* Press `Ctrl + C` to stop.

Show only recent logs for a service:

```bash
journalctl -u nginx.service -n 100
```

This command displays the most recent 100 log entries for `nginx.service`. It is useful when you want recent service logs without following them live.

Example output:

```text
May 03 10:30:05 server nginx[2801]: signal process started
May 03 10:30:06 server systemd[1]: Reloaded nginx.service - A high performance web server
May 03 10:31:10 server nginx[2801]: 192.168.1.70 - - "GET /health HTTP/1.1" 200
```

Explanation:

* `-u nginx.service` limits logs to the Nginx service.
* `-n 100` shows the last 100 entries.
* Useful for quick service checks.
* You can increase or decrease the number depending on how much history you need.

#### Filter by Severity

```bash
journalctl -p err
```

Shows errors and anything more severe.

This command filters logs by priority level. The `err` level shows error messages and more severe messages such as critical, alert, and emergency logs. It is useful when you want to quickly find serious problems without reading informational logs.

Example output:

```text
May 03 10:40:11 server nginx[3001]: connect() failed while connecting to upstream
May 03 10:41:03 server kernel: EXT4-fs error on device sda1
May 03 10:42:18 server systemd[1]: docker.service: Failed with result 'exit-code'
```

Explanation:

* `-p err` shows priority level `err` and anything more severe.
* Useful for finding failures quickly.
* Less noisy than viewing all logs.
* Can be combined with `-u` to filter errors for a specific service.

Priority levels:

| Name    | Code | Meaning                   |
| ------- | ---- | ------------------------- |
| emerg   | 0    | System unusable           |
| alert   | 1    | Immediate action required |
| crit    | 2    | Critical condition        |
| err     | 3    | Error                     |
| warning | 4    | Warning                   |
| notice  | 5    | Normal but important      |
| info    | 6    | Informational             |
| debug   | 7    | Debug messages            |

Examples:

```bash
journalctl -p warning
```

This command shows warning messages and anything more severe. It is useful when you want to see potential problems before they become errors.

Example output:

```text
May 03 10:50:01 server nginx[3100]: conflicting server name ignored
May 03 10:51:22 server kernel: CPU temperature above threshold
May 03 10:52:05 server systemd[1]: service restart operation timed out
```

Explanation:

* Shows `warning`, `err`, `crit`, `alert`, and `emerg` messages.
* Good for proactive troubleshooting.
* More detailed than `-p err`.
* May include warnings that are not service-breaking.

```bash
journalctl -p err -u ssh.service
```

This command shows only error-level and more severe logs for the SSH service. It is useful when troubleshooting failed SSH logins, SSH service failures, or authentication problems.

Example output:

```text
May 03 11:00:12 server sshd[3301]: error: kex_exchange_identification: client sent invalid protocol identifier
May 03 11:01:44 server sshd[3310]: fatal: Timeout before authentication
May 03 11:03:01 server sshd[3322]: error: PAM: Authentication failure for illegal user test
```

Explanation:

* `-p err` filters by error severity.
* `-u ssh.service` limits logs to SSH.
* Useful for authentication and connection troubleshooting.
* Reduces noise from normal SSH login messages.

```bash
journalctl -p debug -u myapp.service
```

This command shows debug-level logs for `myapp.service`. Since `debug` is the lowest priority level, this may include very detailed messages depending on how the service logs its output.

Example output:

```text
May 03 11:10:01 server myapp[3500]: DEBUG Loading configuration from /etc/myapp/config.yml
May 03 11:10:02 server myapp[3500]: DEBUG Database connection pool initialized
May 03 11:10:03 server myapp[3500]: INFO Application started successfully
```

Explanation:

* `-p debug` includes debug logs and all higher-priority messages.
* Useful during development or deep troubleshooting.
* Can produce very verbose output.
* Best combined with `-u` to avoid too much unrelated output.

#### Journal Output Formats

Normal output:

```bash
journalctl -u nginx
```

This command shows logs for the Nginx service using the default journal output format. The default format is readable and suitable for most manual troubleshooting tasks.

Example output:

```text
May 03 11:20:01 server nginx[3700]: 192.168.1.80 - - "GET / HTTP/1.1" 200
May 03 11:20:05 server nginx[3700]: 192.168.1.81 - - "GET /favicon.ico HTTP/1.1" 404
May 03 11:20:10 server systemd[1]: Reloaded nginx.service - A high performance web server
```

Explanation:

* Displays service logs in the standard human-readable format.
* Good for day-to-day troubleshooting.
* Shows timestamp, hostname, process name, process ID, and message.
* Easy to read directly in the terminal.

Short ISO timestamps:

```bash
journalctl -u nginx -o short-iso
```

This command shows Nginx logs with ISO-style timestamps. This format is useful when you need clearer timestamps, especially for comparing logs across systems or matching logs with external monitoring tools.

Example output:

```text
2026-05-03T11:25:01+0200 server nginx[3800]: 192.168.1.90 - - "GET / HTTP/1.1" 200
2026-05-03T11:25:03+0200 server nginx[3800]: 192.168.1.91 - - "POST /api/login HTTP/1.1" 401
2026-05-03T11:25:08+0200 server nginx[3800]: upstream timed out while reading response header
```

Explanation:

* `-o short-iso` changes the output format.
* Shows timestamps in ISO-style format.
* Useful for log correlation.
* Easier to sort, compare, and copy into reports.

Verbose metadata:

```bash
journalctl -u nginx -o verbose
```

This command shows detailed metadata for each journal entry. It includes fields such as systemd unit name, process ID, executable path, hostname, priority, and other internal journal fields.

Example output:

```text
MESSAGE=192.168.1.90 - - "GET / HTTP/1.1" 200
_PID=3800
_UID=33
_GID=33
_SYSTEMD_UNIT=nginx.service
_COMM=nginx
_HOSTNAME=server
PRIORITY=6
```

Explanation:

* `-o verbose` shows detailed journal fields.
* Useful for advanced debugging.
* Helps identify exact processes, units, users, and priorities.
* More detailed than normal output and less convenient for quick reading.

JSON output:

```bash
journalctl -u nginx -o json
```

This command outputs each journal entry as a single JSON object. It is useful when logs need to be processed by scripts, command-line tools, or log aggregation systems.

Example output:

```json
{"MESSAGE":"192.168.1.90 - - \"GET / HTTP/1.1\" 200","_PID":"3800","_SYSTEMD_UNIT":"nginx.service","PRIORITY":"6","_HOSTNAME":"server"}
{"MESSAGE":"upstream timed out while reading response header","_PID":"3800","_SYSTEMD_UNIT":"nginx.service","PRIORITY":"3","_HOSTNAME":"server"}
```

Explanation:

* `-o json` prints logs as JSON.
* Each log entry appears on one line.
* Useful for parsing with tools such as `jq`.
* Good for automation, scripts, and log pipelines.

Pretty JSON:

```bash
journalctl -u nginx -o json-pretty
```

This command outputs journal entries as formatted JSON. It is easier for humans to read than normal JSON output because fields are split across multiple lines with indentation.

Example output:

```json
{
  "MESSAGE" : "192.168.1.90 - - \"GET / HTTP/1.1\" 200",
  "_PID" : "3800",
  "_SYSTEMD_UNIT" : "nginx.service",
  "PRIORITY" : "6",
  "_HOSTNAME" : "server"
}
```

Explanation:

* `-o json-pretty` formats JSON across multiple lines.
* Easier to inspect manually than compact JSON.
* Useful when reviewing metadata-rich log entries.
* Less convenient for line-based log processing than `-o json`.

This is useful when feeding logs into scripts or log aggregation systems. JSON formats allow tools to read fields such as service name, priority, process ID, hostname, and message without relying on text parsing. For quick manual troubleshooting, normal or short output is usually easier to read. For automation and structured logging workflows, JSON output is usually better.

### Linux Logs by System Layer

A useful way to understand logs is by layers.

| Layer              | Components                                              |
|--------------------|----------------------------------------------------------|
| Application Layer  | Python apps, nginx, Apache, PostgreSQL, Docker apps     |
| Service Layer      | systemd services, cron, SSH, NetworkManager             |
| OS Layer           | package manager, sudo, auth, syslog                     |
| Kernel Layer       | drivers, hardware, memory, disk, CPU, networking        |
| Boot Layer         | bootloader, initramfs, systemd startup                  |

#### Kernel Logs

Kernel logs are useful for debugging:

* hardware
* drivers
* network interfaces
* USB devices
* disks
* memory errors
* CPU warnings
* filesystem problems

Kernel logs come from the Linux kernel rather than from normal user-space applications. They are especially useful when troubleshooting low-level system problems, such as a disk failing, a network card disconnecting, a USB device not being detected, a driver crashing, or the system reporting CPU or memory warnings.

Commands:

```bash
dmesg
```

This command displays messages from the kernel ring buffer. These messages usually include boot messages, device detection, driver messages, hardware warnings, and kernel-level errors.

Example output:

```text
[    0.000000] Linux version 6.8.0-31-generic
[    1.245011] usb 1-1: new high-speed USB device number 2 using xhci_hcd
[    2.884310] eth0: renamed from enp0s3
[   15.902144] EXT4-fs (sda1): mounted filesystem
```

Explanation:

* Shows kernel messages stored in the kernel ring buffer.
* Useful for checking hardware and driver events.
* Timestamps are shown as seconds since boot.
* Output may be cleared after reboot or overwritten on busy systems.

```bash
dmesg -T
```

This command displays kernel messages with human-readable timestamps. Instead of showing only seconds since boot, it converts timestamps into normal date and time format.

Example output:

```text
[Sun May  3 09:01:10 2026] Linux version 6.8.0-31-generic
[Sun May  3 09:01:12 2026] usb 1-1: new high-speed USB device number 2 using xhci_hcd
[Sun May  3 09:01:15 2026] eth0: renamed from enp0s3
[Sun May  3 09:02:01 2026] EXT4-fs (sda1): mounted filesystem
```

Explanation:

* `-T` shows readable timestamps.
* Easier to match kernel events with incidents.
* Useful when checking when a device disconnected or an error happened.
* Timestamp conversion may be less accurate if the system clock changed after boot.

```bash
journalctl -k
```

This command displays kernel messages from the systemd journal. It is similar to `dmesg`, but it reads kernel logs from the journal instead of only the kernel ring buffer.

Example output:

```text
May 03 09:01:10 server kernel: Linux version 6.8.0-31-generic
May 03 09:01:12 server kernel: usb 1-1: new high-speed USB device number 2 using xhci_hcd
May 03 09:01:15 server kernel: eth0: renamed from enp0s3
May 03 09:02:01 server kernel: EXT4-fs (sda1): mounted filesystem
```

Explanation:

* `-k` shows kernel messages from the journal.
* Uses normal journal timestamps.
* Can include persisted kernel logs from previous boots if journal persistence is enabled.
* Useful when you want kernel logs with `journalctl` filtering options.

```bash
journalctl -k -b
```

This command displays kernel messages from the current boot only. It is useful when troubleshooting hardware, driver, or boot-related issues from the current running session.

Example output:

```text
May 03 09:01:10 server kernel: Linux version 6.8.0-31-generic
May 03 09:01:13 server kernel: ACPI: bus type USB registered
May 03 09:01:18 server kernel: e1000e 0000:00:19.0 eth0: NIC Link is Up
May 03 09:04:44 server kernel: EXT4-fs (sda1): re-mounted filesystem
```

Explanation:

* `-k` filters journal entries to kernel messages.
* `-b` limits output to the current boot.
* Useful for checking startup and hardware initialization messages.
* Helps avoid mixing current kernel messages with older boot logs.

Examples:

```bash
dmesg | grep -i error
```

This command searches kernel messages for the word `error`, ignoring letter case. It is useful for quickly finding kernel-level failures.

Example output:

```text
[ 1234.442100] EXT4-fs error (device sda1): ext4_find_entry: inode read error
[ 1240.112901] blk_update_request: I/O error, dev sda, sector 884120
[ 1244.650331] usb 2-1: device descriptor read/64, error -71
```

Explanation:

* `grep -i error` searches for `error`, `Error`, or `ERROR`.
* Useful for finding disk, USB, filesystem, and driver errors.
* May miss problems that use words like `failed`, `timeout`, or `reset`.
* For broader searches, also check `fail`, `warn`, and `timeout`.

```bash
dmesg | grep -i usb
```

This command filters kernel messages related to USB devices. It is useful when checking whether a USB drive, keyboard, network adapter, or other USB device was detected correctly.

Example output:

```text
[    1.245011] usb 1-1: new high-speed USB device number 2 using xhci_hcd
[    1.601233] usb 1-1: New USB device found, idVendor=0781, idProduct=5567
[    1.604811] usb-storage 1-1:1.0: USB Mass Storage device detected
```

Explanation:

* Shows USB detection and driver messages.
* Useful when a USB device is not appearing.
* Can show device resets, disconnects, and descriptor errors.
* Helpful for troubleshooting external drives and USB adapters.

```bash
dmesg | grep -i eth
```

This command searches kernel messages for Ethernet-related entries. It is useful when checking network interface detection, link state changes, and network driver messages.

Example output:

```text
[    2.884310] eth0: renamed from enp0s3
[   45.812001] e1000e 0000:00:19.0 eth0: NIC Link is Up 1000 Mbps Full Duplex
[  300.441221] eth0: Link is Down
```

Explanation:

* Searches for messages containing `eth`.
* Useful for Ethernet interface troubleshooting.
* Can show whether the network link is up or down.
* Some systems use names like `enp0s3`, `ens160`, or `eno1` instead of `eth0`.

```bash
journalctl -k -p warning
```

This command shows kernel warning messages and anything more severe. It is useful when you want to focus on kernel problems without reading normal informational messages.

Example output:

```text
May 03 10:12:44 server kernel: CPU0: Core temperature above threshold
May 03 10:13:02 server kernel: blk_update_request: I/O error, dev sda, sector 884120
May 03 10:13:10 server kernel: EXT4-fs warning (device sda1): mounting fs with errors
```

Explanation:

* `-k` filters logs to kernel messages.
* `-p warning` shows warnings, errors, critical, alert, and emergency messages.
* Useful for finding serious hardware or kernel issues quickly.
* Can be combined with `-b` to show warnings from the current boot only.

Sample kernel log:

```text
[12345.678901] eth0: Link is Down
[12346.123456] EXT4-fs error: I/O error while writing superblock
[12347.222222] CPU0: Core temperature above threshold
```

This sample shows three different kernel-level problems. The first line indicates a network interface link problem, the second line indicates a filesystem or disk write problem, and the third line indicates a CPU temperature warning.

Interpretation:

```text
eth0 Link is Down        → network interface disconnected
EXT4-fs error            → filesystem or disk issue
temperature threshold    → cooling or hardware problem
```

Explanation:

* `eth0 Link is Down` usually means the network cable was unplugged, the virtual interface disconnected, or the switch port went down.
* `EXT4-fs error` usually points to filesystem corruption, disk I/O errors, storage problems, or an unsafe shutdown.
* `I/O error while writing superblock` is serious because the superblock contains important filesystem metadata.
* `CPU temperature above threshold` means the CPU is getting too hot and may throttle performance or shut down to protect hardware.
* Repeated disk, filesystem, or temperature messages should be investigated immediately.

#### Authentication Logs

Authentication logs record:

- SSH login attempts
- sudo usage
- failed passwords
- user sessions
- PAM authentication

Ubuntu/Debian:

```bash
sudo less /var/log/auth.log
```

RHEL-based systems:

```bash
sudo less /var/log/secure
```

Using journald:

```bash
journalctl -u ssh.service
journalctl _COMM=sshd
```

Common searches:

```bash
sudo grep "Failed password" /var/log/auth.log
sudo grep "Accepted password" /var/log/auth.log
sudo grep "sudo" /var/log/auth.log
sudo grep "session opened" /var/log/auth.log
```

Example:

```text
May 03 11:00:01 server sshd[23456]: Failed password for invalid user admin from 203.0.113.10 port 54323 ssh2
```

Breakdown:

```text
Failed password       → login failed
invalid user admin    → account does not exist
203.0.113.10          → source IP
sshd                  → SSH daemon
```

#### Systemd Service Logs

Most services managed by systemd can be debugged with:

```bash
systemctl status service-name
journalctl -u service-name
```

Example:

```bash
systemctl status nginx
journalctl -u nginx
journalctl -u nginx -f
```

Useful pattern:

```bash
sudo systemctl restart nginx
journalctl -u nginx -n 50 --no-pager
```

This lets you restart a service and immediately inspect the most recent logs.

#### Cron Logs

Cron logs scheduled jobs.

Depending on distro, cron logs may be in:

```bash
/var/log/syslog
/var/log/cron
journalctl -u cron
journalctl -u crond
```

Examples:

```bash
grep CRON /var/log/syslog
journalctl -u cron
```

Sample:

```text
May 03 12:00:01 server CRON[4567]: (root) CMD (/usr/local/bin/backup.sh)
```

This means cron started the script.

It does **not** guarantee the script succeeded.

For proper script debugging, the script itself should log success and failure.

#### Package Manager Logs

Useful when asking:

```text
What changed recently?
Was a package upgraded?
Did an update break something?
```

Debian/Ubuntu:

```bash
less /var/log/dpkg.log
less /var/log/apt/history.log
less /var/log/apt/term.log
```

Examples:

```bash
grep "install " /var/log/dpkg.log
grep "upgrade " /var/log/dpkg.log
grep nginx /var/log/apt/history.log
```

RHEL/Fedora:

```bash
less /var/log/dnf.log
less /var/log/yum.log
rpm -qa --last
```

#### Web Server Logs

##### Nginx

Common files:

```bash
/var/log/nginx/access.log
/var/log/nginx/error.log
```

Access log example:

```text
192.168.1.50 - - [03/May/2026:13:00:01 +0200] "GET /index.html HTTP/1.1" 200 612
```

Meaning:

```text
192.168.1.50    → client IP
GET /index.html → requested path
200             → HTTP status code
612             → bytes sent
```

Error log example:

```text
2026/05/03 13:01:22 [error] 1234#1234: *55 connect() failed while connecting to upstream
```

This often means nginx cannot reach the backend app.

Useful commands:

```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo grep " 500 " /var/log/nginx/access.log
sudo grep "connect() failed" /var/log/nginx/error.log
```

##### Apache

Common files:

```bash
/var/log/apache2/access.log
/var/log/apache2/error.log
```

or:

```bash
/var/log/httpd/access_log
/var/log/httpd/error_log
```

#### Database Logs

PostgreSQL logs may be in:

```bash
/var/log/postgresql/
journalctl -u postgresql
```

MySQL/MariaDB logs may be in:

```bash
/var/log/mysql/
journalctl -u mysql
journalctl -u mariadb
```

Common things to search:

```bash
grep -i error /var/log/postgresql/*.log
grep -i "connection refused" /var/log/mysql/error.log
journalctl -u postgresql -p err
```

#### Docker Logs

Docker has its own logging path.

View container logs:

```bash
docker logs container_name
docker logs -f container_name
docker logs --tail 100 container_name
docker logs --since 1h container_name
```

Docker service logs:

```bash
journalctl -u docker
```

Docker Compose logs:

```bash
docker compose logs
docker compose logs -f
docker compose logs api
docker compose logs --tail 100
```

Common Docker debugging flow:

```bash
docker ps
docker ps -a
docker logs container_name
docker inspect container_name
journalctl -u docker
```

### Creating Logs from Python Applications

Python applications should not rely only on `print()`.

Use the built-in `logging` module.

#### Basic Python Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger("myapp")

logger.info("Application started")
logger.warning("Disk space is getting low")
logger.error("Database connection failed")
```

Example output:

```text
2026-05-03 14:00:01 INFO myapp: Application started
2026-05-03 14:00:02 WARNING myapp: Disk space is getting low
2026-05-03 14:00:03 ERROR myapp: Database connection failed
```

#### Log to a File

```python
import logging

logging.basicConfig(
    filename="/var/log/myapp.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s [%(process)d]: %(message)s"
)

logger = logging.getLogger("myapp")

logger.info("Server started")
logger.error("Could not connect to database")
```

Important:

```text
The application user must have permission to write to the log file.
```

Example:

```bash
sudo touch /var/log/myapp.log
sudo chown myappuser:myappuser /var/log/myapp.log
```

#### Log to Console for systemd

If your Python app runs as a systemd service, logging to stdout/stderr is often best.

Python app:

```python
import logging
import sys

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Application started")
logger.error("Something failed")
```

Systemd service:

```ini
[Unit]
Description=My Python App
After=network.target

[Service]
User=myappuser
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then logs can be viewed with:

```bash
journalctl -u myapp.service
journalctl -u myapp.service -f
```

Flow:

```text
Python stdout/stderr
        |
        v
systemd service manager
        |
        v
systemd-journald
        |
        v
journalctl -u myapp.service
```

#### Python Rotating File Logs

For standalone apps, you can rotate logs from inside Python.

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "/var/log/myapp.log",
    maxBytes=5_000_000,
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("App started")
logger.warning("Something looks suspicious")
logger.error("Something failed")
```

This creates files like:

```text
/var/log/myapp.log
/var/log/myapp.log.1
/var/log/myapp.log.2
/var/log/myapp.log.3
```

Use this when the app owns its logs.

Use `logrotate` when Linux should manage the log files externally.

#### Python Timed Rotating Logs

Rotate every day:

```python
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    "/var/log/myapp.log",
    when="midnight",
    interval=1,
    backupCount=14
)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Daily rotating logger started")
```

Result:

```text
myapp.log
myapp.log.2026-05-01
myapp.log.2026-05-02
myapp.log.2026-05-03
```

#### Python JSON Logs

JSON logs are easier for machines to parse.

```python
import logging
import json
import sys
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "process": record.process,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

logger.info("Application started")
```

Example output:

```json
{
  "timestamp": "2026-05-03T12:00:01+00:00",
  "level": "INFO",
  "logger": "myapp",
  "message": "Application started",
  "module": "app",
  "line": 31,
  "process": 1234
}
```

JSON logs are good for:

```text
Loki
Elasticsearch
OpenSearch
Splunk
Fluent Bit
Vector
Logstash
custom Python parsers
```

#### Python Logging Exceptions Properly

Bad:

```python
try:
    1 / 0
except Exception as e:
    logger.error(f"Error: {e}")
```

Better:

```python
try:
    1 / 0
except Exception:
    logger.exception("Unexpected calculation error")
```

`logger.exception()` includes the traceback.

Example:

```text
ERROR myapp: Unexpected calculation error
Traceback (most recent call last):
  File "app.py", line 10, in <module>
    1 / 0
ZeroDivisionError: division by zero
```

Tracebacks are extremely important for debugging.

#### Python App Logging to Syslog

You can send Python logs to syslog.

```python
import logging
from logging.handlers import SysLogHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

handler = SysLogHandler(address="/dev/log")
formatter = logging.Formatter("myapp: %(levelname)s %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Application started")
logger.error("Database connection failed")
```

Then check:

```bash
journalctl | grep myapp
grep myapp /var/log/syslog
```

### Creating Logs from Shell Scripts

#### Using `logger`

The `logger` command sends messages to syslog/journald.

Simple example:

```bash
logger "Backup completed successfully"
```

With tag:

```bash
logger -t backup_script "Backup completed successfully"
```

With severity:

```bash
logger -t backup_script -p local0.info "Backup started"
logger -t backup_script -p local0.err "Backup failed"
```

Example script:

```bash
#!/bin/bash

SOURCE="/data"
DEST="/backup"

logger -t backup_script -p local0.info "Backup started"

if rsync -a "$SOURCE" "$DEST"; then
    logger -t backup_script -p local0.info "Backup completed successfully"
else
    logger -t backup_script -p local0.err "Backup failed"
    exit 1
fi
```

View logs:

```bash
journalctl -t backup_script
grep backup_script /var/log/syslog
```

### Rsyslog

`rsyslog` is a powerful syslog daemon used to:

- receive logs
- filter logs
- write logs to files
- forward logs to remote servers
- split logs by facility/severity/program

Basic flow:

```text
Application / Kernel / Service
            |
            v
        journald
            |
            v
        rsyslog
            |
     +------+------+
     |             |
     v             v
 /var/log/syslog   Remote log server
```

#### Rsyslog Rule Format

Classic format:

```text
facility.priority    action
```

Example:

```text
authpriv.*           /var/log/auth.log
kern.*               /var/log/kern.log
mail.info            /var/log/mail.info
*.err                /var/log/errors.log
```

Facilities:

| Facility | Meaning                  |
| -------- | ------------------------ |
| auth     | Authentication           |
| authpriv | Private auth messages    |
| cron     | Cron jobs                |
| daemon   | System daemons           |
| kern     | Kernel messages          |
| mail     | Mail system              |
| syslog   | Syslog internal messages |
| user     | User-level messages      |
| local0-7 | Custom use               |

Priorities:

```text
debug < info < notice < warning < err < crit < alert < emerg
```

#### Custom Rsyslog Rule

Create:

```bash
sudo nano /etc/rsyslog.d/30-myapp.conf
```

Example:

```text
if $programname == 'myapp' then /var/log/myapp.log
& stop
```

Restart rsyslog:

```bash
sudo systemctl restart rsyslog
```

Test it:

```bash
logger -t myapp "Hello from myapp"
cat /var/log/myapp.log
```

#### Remote Logging with Rsyslog

##### Server

Enable TCP receiver:

```text
module(load="imtcp")
input(type="imtcp" port="514")
```

Store logs by hostname:

```text
template(name="RemoteLogs" type="string" string="/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log")
*.* ?RemoteLogs
```

Restart:

```bash
sudo systemctl restart rsyslog
```

##### Client

Send logs to server:

```text
*.* @@logserver.example.com:514
```

`@` means UDP.

`@@` means TCP.

Restart:

```bash
sudo systemctl restart rsyslog
```

Architecture:

```text
+-----------+       TCP 514       +----------------+
| server01  | ------------------> | logserver      |
| server02  | ------------------> | /var/log/remote|
| server03  | ------------------> |                |
+-----------+                     +----------------+
```

### Log Housekeeping

Logs grow forever unless managed.

Housekeeping means:

- rotate old logs
- compress old logs
- delete expired logs
- limit disk usage
- vacuum journal files
- archive important logs

There are two major housekeeping systems:

| System           | Manages                               |
|------------------|----------------------------------------|
| logrotate        | Plain text logs in /var/log            |
| journald config  | systemd journal size and retention     |

#### Logrotate

`logrotate` manages traditional log files.

Config locations:

```bash
/etc/logrotate.conf
/etc/logrotate.d/
```

View configs:

```bash
cat /etc/logrotate.conf
ls /etc/logrotate.d/
cat /etc/logrotate.d/nginx
cat /etc/logrotate.d/rsyslog
```

Example config:

```text
/var/log/myapp.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 myappuser adm
    postrotate
        systemctl reload myapp.service > /dev/null 2>&1 || true
    endscript
}
```

Meaning:

```text
daily          rotate every day
rotate 14      keep 14 old logs
compress       gzip old logs
delaycompress  wait one cycle before compression
missingok      do not error if file is missing
notifempty     do not rotate empty logs
create         create a new file with permissions/owner/group
postrotate     run command after rotation
```

#### Check Logrotate Status

Logrotate state file:

```bash
cat /var/lib/logrotate/status
```

Debug logrotate without changing files:

```bash
sudo logrotate -d /etc/logrotate.conf
```

Force rotation:

```bash
sudo logrotate -f /etc/logrotate.conf
```

Force one config:

```bash
sudo logrotate -f /etc/logrotate.d/nginx
```

Check rotated files:

```bash
ls -lh /var/log/syslog*
ls -lh /var/log/nginx/*
```

Example:

```text
/var/log/syslog
/var/log/syslog.1
/var/log/syslog.2.gz
/var/log/syslog.3.gz
```

#### How Logrotate Runs Automatically

On many systems, logrotate is run by a systemd timer:

```bash
systemctl status logrotate.timer
systemctl list-timers | grep logrotate
```

Or by cron:

```bash
ls /etc/cron.daily/
cat /etc/cron.daily/logrotate
```

Useful check:

```bash
systemctl status logrotate.service
journalctl -u logrotate.service
```

#### Journald Housekeeping

Check journal disk usage:

```bash
journalctl --disk-usage
```

Vacuum old journal logs by size:

```bash
sudo journalctl --vacuum-size=1G
```

Vacuum by time:

```bash
sudo journalctl --vacuum-time=14d
```

Vacuum by number of files:

```bash
sudo journalctl --vacuum-files=10
```

Config file:

```bash
/etc/systemd/journald.conf
```

Common settings:

```ini
[Journal]
Storage=persistent
SystemMaxUse=1G
SystemKeepFree=2G
MaxRetentionSec=1month
Compress=yes
```

Restart journald after changes:

```bash
sudo systemctl restart systemd-journald
```

#### Persistent vs Volatile Journals

Volatile journal:

```text
/run/log/journal
```

Lost after reboot.

Persistent journal:

```text
/var/log/journal
```

Survives reboot.

Enable persistent journal:

```bash
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald
```

Check:

```bash
ls -ld /var/log/journal
journalctl --list-boots
```

### Quickly Searching and Parsing Logs

This is where practical debugging happens.

#### Basic Tools

| Tool       | Use                                |
| ---------- | ---------------------------------- |
| less       | Read large files interactively     |
| tail       | Show last lines / follow live logs |
| grep       | Search text                        |
| awk        | Extract columns / summarize        |
| sed        | Transform/filter text              |
| cut        | Extract fields                     |
| sort       | Sort results                       |
| uniq       | Count repeated lines               |
| wc         | Count lines                        |
| jq         | Parse JSON logs                    |
| journalctl | Query systemd journal              |
| zgrep      | Search compressed .gz logs         |
| lnav       | Interactive log viewer             |

#### Fast Examples

Follow a file live:

```bash
tail -f /var/log/syslog
```

Follow multiple files:

```bash
tail -f /var/log/syslog /var/log/auth.log
```

Search for errors:

```bash
grep -i error /var/log/syslog
```

Search compressed rotated logs:

```bash
zgrep -i error /var/log/syslog.*.gz
```

Search current and rotated logs:

```bash
grep -i error /var/log/syslog /var/log/syslog.1
zgrep -i error /var/log/syslog.*.gz
```

Count failed SSH attempts by IP:

```bash
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr
```

Find top requested URLs in nginx access log:

```bash
awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head
```

Find top HTTP status codes:

```bash
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -nr
```

Find 500 errors:

```bash
awk '$9 >= 500 {print}' /var/log/nginx/access.log
```

#### Using `journalctl` for Fast Filtering

Errors from current boot:

```bash
journalctl -b -p err
```

Warnings and errors from nginx:

```bash
journalctl -u nginx -p warning
```

Logs since 10 minutes ago:

```bash
journalctl --since "10 minutes ago"
```

Logs for one executable:

```bash
journalctl _COMM=sshd
```

Logs for one PID:

```bash
journalctl _PID=1234
```

Kernel logs from current boot:

```bash
journalctl -k -b
```

Show logs without pager:

```bash
journalctl -u nginx --no-pager
```

#### JSON Log Parsing with `jq`

Example JSON log:

```json
{"timestamp":"2026-05-03T12:00:00Z","level":"ERROR","service":"api","message":"database timeout"}
```

Show only errors:

```bash
jq 'select(.level == "ERROR")' app.log
```

Print timestamp and message:

```bash
jq -r 'select(.level == "ERROR") | "\(.timestamp) \(.message)"' app.log
```

Count by level:

```bash
jq -r '.level' app.log | sort | uniq -c
```

#### `lnav`

`lnav` is an interactive log viewer that can understand many log formats.

Install:

```bash
sudo apt install lnav
```

Open logs:

```bash
sudo lnav /var/log/syslog /var/log/auth.log
```

Open all nginx logs:

```bash
sudo lnav /var/log/nginx/*.log
```

Benefits:

- colored logs
- automatic timestamp detection
- search
- filtering
- SQL-like queries
- multiple files together

#### Gathering Logs Together

For troubleshooting, it is often useful to collect logs into one bundle.

Example:

```bash
mkdir -p debug-logs

journalctl -b > debug-logs/journal-current-boot.log
journalctl -p err > debug-logs/journal-errors.log
dmesg -T > debug-logs/dmesg.log
systemctl status nginx > debug-logs/nginx-status.txt
journalctl -u nginx > debug-logs/nginx-journal.log
cp /var/log/nginx/error.log debug-logs/

tar -czf debug-logs.tar.gz debug-logs
```

Result:

```text
debug-logs.tar.gz
```

You can send this to another admin or attach it to a bug report.

### Centralized Log Collection

For one server, local logs may be enough.

For many servers, centralized logging is better.

```text
+-----------+       +-----------+
| app01     |       | app02     |
+-----+-----+       +-----+-----+
      |                   |
      v                   v
+-------------------------------+
|      Log Collector            |
| rsyslog / Fluent Bit / Vector |
+---------------+---------------+
                |
                v
+-------------------------------+
| Storage / Search              |
| Loki / Elasticsearch / Splunk |
+-------------------------------+
                |
                v
+-------------------------------+
| Dashboard / Alerts            |
| Grafana / Kibana / SIEM       |
+-------------------------------+
```

Common tools:

| Tool          | Purpose                                       |
| ------------- | --------------------------------------------- |
| rsyslog       | Classic syslog forwarding and routing         |
| syslog-ng     | Alternative syslog daemon                     |
| Fluent Bit    | Lightweight log collector/forwarder           |
| Fluentd       | Heavier log collector/processor               |
| Vector        | Fast log/event pipeline                       |
| Logstash      | Processing pipeline for Elastic/OpenSearch    |
| Filebeat      | Ships log files to Elastic/OpenSearch         |
| Promtail      | Ships logs to Loki                            |
| Loki          | Log storage/query system by Grafana ecosystem |
| Elasticsearch | Search/index log storage                      |
| OpenSearch    | Open-source Elasticsearch alternative         |
| Splunk        | Commercial log analytics platform             |
| Grafana       | Dashboards for logs and metrics               |
| Kibana        | Elasticsearch visualization UI                |

### Debugging with Logs: Practical Playbooks

#### Service Will Not Start

Example: nginx fails.

Step 1:

```bash
systemctl status nginx
```

Step 2:

```bash
journalctl -u nginx -n 100 --no-pager
```

Step 3:

```bash
sudo nginx -t
```

Step 4:

```bash
sudo tail -n 100 /var/log/nginx/error.log
```

Flow:

```text
Service failed
     |
     v
systemctl status
     |
     v
journalctl -u service
     |
     v
application-specific config test
     |
     v
application-specific error log
```

#### SSH Login Problems

Check SSH service:

```bash
systemctl status ssh
journalctl -u ssh
```

Check auth logs:

```bash
sudo tail -f /var/log/auth.log
```

Search failures:

```bash
sudo grep "Failed password" /var/log/auth.log
```

Search accepted logins:

```bash
sudo grep "Accepted" /var/log/auth.log
```

Common causes:

- wrong password
- wrong username
- SSH key permission problem
- firewall blocking port
- PermitRootLogin disabled
- PasswordAuthentication disabled
- fail2ban blocking IP

#### Disk Full Because of Logs

Check disk:

```bash
df -h
```

Find largest log directories:

```bash
sudo du -sh /var/log/* | sort -h
```

Find huge log files:

```bash
sudo find /var/log -type f -size +100M -exec ls -lh {} \;
```

Check journal size:

```bash
journalctl --disk-usage
```

Clean journal safely:

```bash
sudo journalctl --vacuum-size=1G
```

Force logrotate:

```bash
sudo logrotate -f /etc/logrotate.conf
```

Do not blindly delete active logs.

Safer truncate if needed:

```bash
sudo truncate -s 0 /var/log/huge.log
```

#### Web App Returns 502 / 503 / 504

Check nginx:

```bash
sudo tail -f /var/log/nginx/error.log
```

Check backend service:

```bash
systemctl status myapp
journalctl -u myapp -n 100
```

Check port listening:

```bash
ss -tulpn
```

Check app logs:

```bash
journalctl -u myapp -f
```

Common meaning:

```text
502 Bad Gateway      nginx cannot talk to backend
503 Service Unavailable backend unavailable or overloaded
504 Gateway Timeout backend too slow or unreachable
```

#### System Rebooted Unexpectedly

List boots:

```bash
journalctl --list-boots
```

View previous boot errors:

```bash
journalctl -b -1 -p err
```

View previous boot kernel messages:

```bash
journalctl -k -b -1
```

Search shutdown/reboot messages:

```bash
journalctl -b -1 | grep -i "shutdown\|reboot\|panic\|oom\|killed"
```

Check for OOM killer:

```bash
journalctl -k | grep -i "out of memory\|oom"
```

### Security-Focused Log Examples

#### Failed SSH Attempts

```bash
sudo grep "Failed password" /var/log/auth.log
```

Count by source IP:

```bash
sudo grep "Failed password" /var/log/auth.log \
  | awk '{print $(NF-3)}' \
  | sort \
  | uniq -c \
  | sort -nr
```

#### Sudo Usage

```bash
sudo grep "sudo" /var/log/auth.log
```

Example:

```text
May 03 14:00:01 server sudo: alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/usr/bin/apt update
```

Meaning:

```text
alice used sudo
from terminal pts/0
while in /home/alice
to run apt update as root
```

#### Fail2ban Logs

Common locations:

```bash
/var/log/fail2ban.log
journalctl -u fail2ban
```

Commands:

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

### Best Practices

#### For Linux Admins

- Use journalctl for systemd services.
- Use /var/log for traditional text logs.
- Check service-specific logs.
- Know your distro differences.
- Use logrotate.
- Check journal disk usage.
- Centralize logs for multiple servers.
- Do not delete logs blindly.
- Secure log permissions.

#### For Application Developers

- Use structured logging.
- Include timestamps.
- Include severity levels.
- Include service name.
- Include request IDs where possible.
- Log exceptions with tracebacks.
- Avoid logging secrets.
- Send logs to stdout when running under systemd or containers.
- Use JSON logs for production systems.

#### What Not to Log

Avoid logging:

- passwords
- API keys
- private tokens
- session cookies
- credit card numbers
- personal data unless required
- SSH private keys
- database credentials

Bad:

```text
User login failed with password hunter2
```

Better:

```text
User login failed for username alice from 203.0.113.10
```

### Quick Command Cheat Sheet

#### General

```bash
tail -f /var/log/syslog
less /var/log/syslog
grep -i error /var/log/syslog
zgrep -i error /var/log/syslog.*.gz
```

#### Journald

```bash
journalctl
journalctl -n 100
journalctl -f
journalctl -b
journalctl -b -1
journalctl -p err
journalctl -u nginx
journalctl -u nginx -f
journalctl --since "1 hour ago"
journalctl --disk-usage
```

#### Kernel

```bash
dmesg
dmesg -T
journalctl -k
journalctl -k -b
```

#### Services

```bash
systemctl status nginx
journalctl -u nginx -n 100
systemctl restart nginx
```

#### Auth

```bash
grep "Failed password" /var/log/auth.log
grep "sudo" /var/log/auth.log
journalctl _COMM=sshd
```

#### Logrotate

```bash
cat /etc/logrotate.conf
ls /etc/logrotate.d/
cat /var/lib/logrotate/status
sudo logrotate -d /etc/logrotate.conf
sudo logrotate -f /etc/logrotate.conf
```

#### Disk Usage

```bash
df -h
du -sh /var/log/*
find /var/log -type f -size +100M -exec ls -lh {} \;
journalctl --disk-usage
```

### Best Practices

- Regular log analysis should be automated using tools like `Logwatch` or `Splunk` to enhance efficiency and reduce manual oversight.
- It is important to set up alerts for critical events, which can be configured using tools such as `Nagios` or `Prometheus` to ensure rapid response to incidents.
- To secure log storage, access control should be enforced by restricting log file permissions to authorized personnel only, ensuring that sensitive data remains protected.
- Encrypting log data, especially during transmission over networks, is crucial for preventing unauthorized access and maintaining confidentiality.
- Implementing log retention policies is necessary to ensure compliance with legal requirements, especially for industries with strict data retention mandates.
- Proper disk space management is essential when storing logs, requiring a balance between keeping historical data for analysis and ensuring that storage resources are not overwhelmed.
- Centralized logging solutions offer significant advantages by simplifying log management across multiple servers, reducing complexity and improving oversight.
- Platforms like the ELK Stack (Elasticsearch, Logstash, Kibana) should be utilized to provide robust search capabilities and visualization tools for more effective log analysis.
- Regular reviews of logging configurations are necessary to ensure that the system is capturing all relevant data and that no important events are missed.
- Keeping logging software updated is vital for benefiting from the latest security patches and new features, reducing the risk of vulnerabilities in the system.

### Challenges

1. Discuss the importance of logging in system administration, including its role in maintaining system health, identifying issues, and assisting with security auditing. Provide examples of how logging helps in daily administration tasks and long-term system monitoring.
2. Research and describe Journald, its functions, and its advantages over traditional text-file-based logging systems. Explain how Journald works with systemd, highlighting features like binary storage, structured logging, and how it simplifies log management for modern systems.
3. Explain how Rsyslog works and describe its configuration process, including how to set up centralized logging. Discuss severity levels, how they categorize log messages, and how they can be used to filter specific types of messages based on their importance or urgency.
4. Use the `logger` command to create custom messages in the system logs. Experiment with different flags, such as specifying the facility or severity level, and explain how `logger` can be used to add entries manually or from within scripts for testing or informational purposes.
5. Configure and use `logrotate` to automate log file management. Set up a basic configuration to rotate, compress, and delete log files on a schedule, and discuss how `logrotate` helps prevent logs from consuming excessive disk space. Explain the importance of log rotation in production systems.
6. Research common log file formats, such as text-based, JSON, and binary formats, and compare their structures. Discuss the benefits and drawbacks of each format, considering factors like readability, compatibility with log analysis tools, and efficiency for storage and search.
7. Set up and use log filters to selectively include or exclude specific log messages. Use either Rsyslog or Journald, and create a rule that filters messages based on criteria such as facility, severity level, or keywords. Document how filtering helps reduce noise in the logs and improves readability.
8. Utilize log analysis tools like `grep`, `journalctl`, or `awk` to extract meaningful information from log files. Perform tasks such as searching for specific events, identifying patterns, and generating summary reports. Explain how log analysis helps administrators identify issues and monitor system health.
9. Outline best practices for managing logs in a production environment. Discuss strategies for log retention, log security, and ensuring reliability and availability of log files. Include recommendations on how to securely store and transmit logs, especially for compliance purposes. Also describe common logging-related issues, such as missing logs, log file corruption, or disk space running out due to log growth, and explain steps for diagnosing and resolving each problem.
10. If you delete an application’s log file on a production server, could that cause the application to stop functioning?
