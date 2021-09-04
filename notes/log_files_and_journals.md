<h1>log files</h1>
Log files are essential for successful administration of any sort of Linux system, since they include information on the system's health, such as any system or application problems. In spite of the fact that programs can place their log files wherever they like, the majority of Linux system log files are located in /var/log.

If you list files located at /var/log, you'll see that there are a lot of Linux system log files:

* syslog: You'll find messages relating to your kernel, apps, and more in  centralized logging system (syslog). It is used also as the consolidated log file for all Linux computers in a data center.
* auth.log: contains authentication failures and successes
* messages: contains general system messages of all types

<h1>journald for systemd based systems</h1>

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
