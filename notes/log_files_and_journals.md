## Log files and journals
Logging is an essential component of system administration on Linux systems. With the right logging tools and techniques, you can keep track of crucial events, troubleshoot problems, and ensure the seamless operation of your system. There are numerous logging methods available on Linux, including text files, `Journald`, and `Rsyslog`, each with its own unique set of advantages and limitations.

## Types of logging

There are several types of logging methods that can be used on a Linux system:

* `Text files`: This is a basic method of logging, in which information is stored in plain text files. The sysadmin has complete control over what is stored in these files, and can choose to store any type of information that they wish.

* `Journald`: This logging method is utilized by systemd-based systems. It stores information about the boot procedure, services, and the kernel in binary files. These files are not meant to be preserved for long periods of time, as they are designed to be rotated out and deleted when no longer needed.

* `Rsyslog:` This logging system redirects different log files to the `/var/log` directory. These logs are persistent, meaning they are meant to be stored and kept for longer periods of time.

## Log files at /var/log
Log files are essential for the successful administration of any Linux system, as they contain information on the system's health, including any system or application problems. While programs can store their log files in any location they choose, the majority of Linux system log files are located in the `/var/log` directory.

If you list the files in the /var/log directory, you will see that there are many Linux system log files:

* `syslog`: This file contains messages relating to the kernel, apps, and more in a centralized logging system (syslog). It is also often used as the consolidated log file for all Linux computers in a data center.
* `auth.log`: This file contains information on authentication failures and successes.
* `messages`: This file contains general system messages of all types.

## Rsyslog
Rsyslog is a high-performance system for log processing. It has a modular design, excellent performance, and strong security features. While it started as a simple syslogd, rsyslog has evolved into a logging tool that is capable of receiving input from a variety of sources, modifying it, and sending the output to a variety of destinations.

The primary configuration file for rsyslog can be found at: `/etc/rsyslog.conf`. However, be warned that editing this file can be complex, as it has its own scripting language.

### Severity levels

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

## Logger
Logger is a command-line utility used to add logs to the local `/var/log/syslog` file or a remote syslog server. It provides several options for adding logs, including the ability to select the priority, specify a remote system, and define the syslog port. 

For more information on logger, you can use the man pages:

```
man logger
```

A simple example of using logger is:

```
logger "An example of log message"
```

To send a log message to a remote server using logger, you can use the following command:

```
logger -n 192.168.10.27 -P 1420 "An example of log message"
```

Here, the `-n` flag specifies the IP address of the remote syslog server, and the `-P` flag specifies the port number.

## Logrotate

Logrotate is a system tool that automates the process of rotating and compressing log files. Log files can potentially consume all available disk space on a system if they are not rotated, compressed, and pruned on a regular basis.

To check the version of logrotate installed on your system, you can use the following command:

```
logrotate --version
```

## Journald for systemd based systems

Journald is responsible for event logging on systemd-based systems. It records events from log files, kernel messages, and other sources.

To display the man pages for journald, you can use the following command:

```
man systemd-journald
```

By default, journald is volatile, meaning that its logs are not stored persistently. To make journald persistent, you can uncomment the following line in the configuration file: `'# Storage=auto'`. This file can be found at: `/etc/systemd/journald.conf`.

To display the last 10 lines of journald logs, you can use the following command:

```
journalctl -n
```

To display the last 10 lines of journald logs and follow them as they are added in real-time, you can use the following command:

```
journalctl -f
```

To display the short status of a specific service, you can use the following command:

```
systemctl status sshd
```

To display journald logs by priority, you can use the following command:

```
journalctl -p err
```

This will display only logs with a priority of "err" or higher. You can also use other priority levels, such as "warning" or "notice", to filter the logs displayed.

## Conclusion

In this article, we covered several types of logging methods that can be used on a Linux system, including text files, journald, and rsyslog. We also looked at log files located in the `/var/log` directory and discussed the tools logrotate and logger, which can be used to manage and manipulate log files. Finally, we looked at journald, the event logging system used on systemd-based systems. Understanding how logging works on a Linux system is essential for effective system administration and troubleshooting.

## Challenges

1. What is logging and why is it important?
1. What is `Journald` and how does it differ from traditional logging systems?
1. What is `Rsyslog` and how does it work?
1. How can you use the logger command to send messages to the system logs?
1. How can you configure log rotation to manage the size of log files?
1. What are some common log file formats, and how do they differ from each other?
1. How can you use log filters to selectively include or exclude certain log messages?
1. How can you use log analysis tools to extract useful information from log files?
1. What are some best practices for managing and maintaining logs in a production environment?
1. How can you troubleshoot issues related to logging on a Linux system?
