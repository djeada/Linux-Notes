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
