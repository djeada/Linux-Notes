## Log Files, Journals, and Logging Systems

Understanding how logging works in Linux is like learning the language your system uses to communicate. Logs are the detailed records that your system keeps about its activities, and they are invaluable for troubleshooting, monitoring performance, and ensuring security. Let's embark on a journey to demystify log files, journals, and the various logging systems used in Linux.

### What Is a Log?

A **log** is a record of events produced by an operating system, application, service, script, device, or security component.

Logs answer questions like:

```text
What happened?
When did it happen?
Who or what caused it?
Was it normal, suspicious, or broken?
Where should I look next?
```

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

```text
+-------------------+-------------------------------------------------------+
| System            | Purpose                                               |
|-------------------|-------------------------------------------------------|
| journald          | Collects structured logs from systemd, kernel, apps   |
| journalctl        | Reads and filters journald logs                       |
| rsyslog           | Routes logs into text files or remote log servers     |
| /var/log          | Directory where many plain-text logs live             |
| logrotate         | Rotates, compresses, and deletes old text logs        |
| logger            | Sends custom log messages from shell scripts          |
| dmesg             | Reads kernel ring buffer messages                     |
+-------------------+-------------------------------------------------------+
```

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

```bash
cat
less
tail
grep
awk
sed
```

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
+-----------+------------+----------------+----------------+
|                        |                |                |
| systemd services       | kernel         | applications   | stdout/stderr |
| nginx.service          | hardware       | custom apps    | service logs  |
+------------------------+----------------+----------------+
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

View newest logs:

```bash
journalctl -n 50
```

Follow logs live:

```bash
journalctl -f
```

View logs since boot:

```bash
journalctl -b
```

View previous boot:

```bash
journalctl -b -1
```

View logs from the last hour:

```bash
journalctl --since "1 hour ago"
```

View logs from a time range:

```bash
journalctl --since "2026-05-03 09:00" --until "2026-05-03 10:00"
```

#### Filter by Service

```bash
journalctl -u ssh.service
journalctl -u nginx.service
journalctl -u docker.service
journalctl -u postgresql.service
```

Follow one service live:

```bash
journalctl -u nginx.service -f
```

Show only recent logs for a service:

```bash
journalctl -u nginx.service -n 100
```

#### Filter by Severity

```bash
journalctl -p err
```

Shows errors and anything more severe.

Priority levels:

```text
+----------+------+------------------------------+
| Name     | Code | Meaning                      |
|----------|------|------------------------------|
| emerg    | 0    | System unusable              |
| alert    | 1    | Immediate action required    |
| crit     | 2    | Critical condition           |
| err      | 3    | Error                        |
| warning  | 4    | Warning                      |
| notice   | 5    | Normal but important         |
| info     | 6    | Informational                |
| debug    | 7    | Debug messages               |
+----------+------+------------------------------+
```

Examples:

```bash
journalctl -p warning
journalctl -p err -u ssh.service
journalctl -p debug -u myapp.service
```

#### Journal Output Formats

Normal output:

```bash
journalctl -u nginx
```

Short ISO timestamps:

```bash
journalctl -u nginx -o short-iso
```

Verbose metadata:

```bash
journalctl -u nginx -o verbose
```

JSON output:

```bash
journalctl -u nginx -o json
```

Pretty JSON:

```bash
journalctl -u nginx -o json-pretty
```

This is useful when feeding logs into scripts or log aggregation systems.

### Linux Logs by System Layer

A useful way to understand logs is by layers.

```text
+------------------------------------------------------+
| Application Layer                                    |
| Python apps, nginx, Apache, PostgreSQL, Docker apps  |
+------------------------------------------------------+
| Service Layer                                        |
| systemd services, cron, SSH, NetworkManager          |
+------------------------------------------------------+
| OS Layer                                             |
| package manager, sudo, auth, syslog                  |
+------------------------------------------------------+
| Kernel Layer                                         |
| drivers, hardware, memory, disk, CPU, networking     |
+------------------------------------------------------+
| Boot Layer                                           |
| bootloader, initramfs, systemd startup               |
+------------------------------------------------------+
```

#### Kernel Logs

Kernel logs are useful for debugging:

```text
hardware
drivers
network interfaces
USB devices
disks
memory errors
CPU warnings
filesystem problems
```

Commands:

```bash
dmesg
dmesg -T
journalctl -k
journalctl -k -b
```

Examples:

```bash
dmesg | grep -i error
dmesg | grep -i usb
dmesg | grep -i eth
journalctl -k -p warning
```

Sample kernel log:

```text
[12345.678901] eth0: Link is Down
[12346.123456] EXT4-fs error: I/O error while writing superblock
[12347.222222] CPU0: Core temperature above threshold
```

Interpretation:

```text
eth0 Link is Down        → network interface disconnected
EXT4-fs error            → filesystem or disk issue
temperature threshold    → cooling or hardware problem
```

#### Authentication Logs

Authentication logs record:

```text
SSH login attempts
sudo usage
failed passwords
user sessions
PAM authentication
```

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

#### 6.7 Database Logs

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

## Using `logger`

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

```text
receive logs
filter logs
write logs to files
forward logs to remote servers
split logs by facility/severity/program
```

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

```text
+----------+---------------------------+
| Facility | Meaning                   |
|----------|---------------------------|
| auth     | Authentication            |
| authpriv | Private auth messages     |
| cron     | Cron jobs                 |
| daemon   | System daemons            |
| kern     | Kernel messages           |
| mail     | Mail system               |
| syslog   | Syslog internal messages  |
| user     | User-level messages       |
| local0-7 | Custom use                |
+----------+---------------------------+
```

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

```text
rotate old logs
compress old logs
delete expired logs
limit disk usage
vacuum journal files
archive important logs
```

There are two major housekeeping systems:

```text
+------------------+----------------------------------------+
| System           | Manages                                |
|------------------|----------------------------------------|
| logrotate        | Plain text logs in /var/log             |
| journald config  | systemd journal size and retention      |
+------------------+----------------------------------------+
```

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

```text
+---------+------------------------------------------------+
| Tool    | Use                                            |
|---------|------------------------------------------------|
| less    | Read large files interactively                 |
| tail    | Show last lines / follow live logs             |
| grep    | Search text                                    |
| awk     | Extract columns / summarize                    |
| sed     | Transform/filter text                          |
| cut     | Extract fields                                 |
| sort    | Sort results                                   |
| uniq    | Count repeated lines                           |
| wc      | Count lines                                    |
| jq      | Parse JSON logs                                |
| journalctl | Query systemd journal                       |
| zgrep   | Search compressed .gz logs                     |
| lnav    | Interactive log viewer                         |
+---------+------------------------------------------------+
```

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

```text
colored logs
automatic timestamp detection
search
filtering
SQL-like queries
multiple files together
```

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

```text
+----------------+--------------------------------------------------+
| Tool           | Purpose                                          |
|----------------|--------------------------------------------------|
| rsyslog        | Classic syslog forwarding and routing            |
| syslog-ng      | Alternative syslog daemon                        |
| Fluent Bit     | Lightweight log collector/forwarder              |
| Fluentd        | Heavier log collector/processor                  |
| Vector         | Fast log/event pipeline                          |
| Logstash       | Processing pipeline for Elastic/OpenSearch       |
| Filebeat       | Ships log files to Elastic/OpenSearch            |
| Promtail       | Ships logs to Loki                               |
| Loki           | Log storage/query system by Grafana ecosystem    |
| Elasticsearch  | Search/index log storage                         |
| OpenSearch     | Open-source Elasticsearch alternative            |
| Splunk         | Commercial log analytics platform                |
| Grafana        | Dashboards for logs and metrics                  |
| Kibana         | Elasticsearch visualization UI                   |
+----------------+--------------------------------------------------+
```

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

```text
wrong password
wrong username
SSH key permission problem
firewall blocking port
PermitRootLogin disabled
PasswordAuthentication disabled
fail2ban blocking IP
```

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

```text
Use journalctl for systemd services.
Use /var/log for traditional text logs.
Check service-specific logs.
Know your distro differences.
Use logrotate.
Check journal disk usage.
Centralize logs for multiple servers.
Do not delete logs blindly.
Secure log permissions.
```

#### For Application Developers

```text
Use structured logging.
Include timestamps.
Include severity levels.
Include service name.
Include request IDs where possible.
Log exceptions with tracebacks.
Avoid logging secrets.
Send logs to stdout when running under systemd or containers.
Use JSON logs for production systems.
```

#### What Not to Log

Avoid logging:

```text
passwords
API keys
private tokens
session cookies
credit card numbers
personal data unless required
SSH private keys
database credentials
```

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
