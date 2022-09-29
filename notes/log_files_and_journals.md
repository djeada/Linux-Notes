<h1>Types of logging</h1>

1. Keeping information in text files. The sysadmin has complete control over what is stored.
2. Journald - utilized by systemd-based systems. Binaries containing info about the boot procedure, services, and the kernel. Those files aren't preserved.
3. Rsyslog - redirects different log files to /var/log. Those logs are persistent.

<h1>Log files at /var/log</h1>
Log files are essential for successful administration of any sort of Linux system, since they include information on the system's health, such as any system or application problems. In spite of the fact that programs can place their log files wherever they like, the majority of Linux system log files are located in /var/log.

If you list files located at /var/log, you'll see that there are a lot of Linux system log files:

* syslog: You'll find messages relating to your kernel, apps, and more in  centralized logging system (syslog). It is used also as the consolidated log file for all Linux computers in a data center.
* auth.log: contains authentication failures and successes
* messages: contains general system messages of all types

<h1>Rsyslog</h1>
Rsyslog is a rocket-fast system for log processing.

Its characteristics include a modular design, great performance, and strong security features.

While it began as a simple syslogd, rsyslog has evolved into a logging ninja, capable of receiving inputs from a variety of sources, modifying them, and sending the outputs to a variety of destinations. 

The primary configuration file should be located at: /etc/rsyslog.conf. Be warned that editing this file is not as simple as it appears.
It has its own scripting language. 

<h2>Severity levels:</h2>	

| Code | Severity |  Description |
| --- | --- | --- |
| 0 | emerg | system is unusable |
| 1 | alert | action must be taken immediately |
| 2 | crit | critical conditions |
| 3 |  error | error conditions |
| 4 |  warning | warning conditions |
| 5 |  notice | normal but significant condition |
| 6 |  info | informational messages |
| 7 |  debug | debug-level messages |

<h1>Logger</h1>
Logger is a command-line utility used to add logs to the local /var/log/syslog file or a remote syslog server.
For adding logs, logger gives several choices such as selecting priority, specifying a remote system, and specifically defining the syslog port. 
More information may be found at:

```bash
man logger
```

A simple example:

```bash
logger "An example of log message"
```

To send a log message to a remote server, do the following: 

```bash
logger -n 192.168.10.27 -P 1420 "An example of log message"
```

<h1>Logrotate</h1>

Logrotate is a system tool that automates log file rotation and compression.
Log files might potentially absorb all available disk space on a system if they were not rotated, compressed, and pruned on a regular basis. 

```bash
logrotate --version
```

<h1>Journald for systemd based systems</h1>

<i>journald</i> is in charge of event logging. It records events from log files, kernel messages, etc.

Display man pages about <i>journald</i>:

```bash
man systemd-journald
```

<i>journald</i> is volatile by default; to make it persistent, uncomment the following line: '# Storage=auto'. 

```bash
vim /etc/systemd/journald.conf
```

To display the last 10 lines of <i>journalctl</i>, use:

```bash
journalctl -n
```

To display the last 10 lines of <i>journalctl</i> and follow, use:

```bash
journalctl -f
```

To display the short status os specific service, use:

```bash
systemctl status sshd
```

To display see <i>journalctl</i> messages by priority, use:

```bash
journalctl -p info
```

To see <i>journalctl</i> messages that occurred after a certain time, use:

```bash
journalctl --since yesterday
```

To display information about the boot process:

```bash
systemd-analyze
```

## SNMP 

* Simple network management protocol
* Mainly used for pulling data from devices (some can have no storage like cameras)

