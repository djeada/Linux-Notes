# Logs and Journals Quiz

Notes: [Log Files and Journals](../notes/log_files_and_journals.md), [Inotify](../notes/inotify.md)

Check your understanding of `journalctl` filtering, journald storage, rsyslog and `/var/log`, logrotate, syslog priorities and inotify file watching.

#### Q. Which command shows only the log entries of `nginx.service` from the current boot?

* [ ] `journalctl -u nginx.service -f`
* [x] `journalctl -u nginx.service -b`
* [ ] `journalctl -b -1 nginx.service`
* [ ] `journalctl -k -u nginx.service`

> **Explanation:** `-u` filters by unit and `-b` with no argument limits output to the current boot; both filters apply together. `-b -1` would select the previous boot, `-f` follows new entries, and `-k` selects kernel messages.

#### Q. You run the commands below. What does the last one print?

```bash
logger -t qz -p local0.notice "notice msg"
logger -t qz -p local0.err    "err msg"
logger -t qz -p user.debug    "debug msg"
journalctl -t qz -p err -o cat
```

* [ ] `notice msg` and `err msg`
* [ ] `err msg` and `debug msg`
* [x] `err msg` only
* [ ] All three messages

> **Explanation:** `-p err` shows priority 3 (`err`) and everything more severe (0 to 2); `notice` is 5 and `debug` is 7, so both are hidden. `-t qz` selects by syslog identifier, and `-o cat` prints only the message text.

#### Q. A script logs with `logger -t backup "done"`, giving no `-p` option. Which command still shows that entry?

* [ ] `journalctl -t backup -p warning`
* [ ] `journalctl -t backup -p err`
* [ ] `journalctl -t backup -p crit`
* [x] `journalctl -t backup -p notice`

> **Explanation:** `logger` uses `user.notice` by default, which is priority 5. A `-p` filter shows its level and all more severe ones, so `notice` (or a less severe level such as `info`) includes it, while `warning` (4) and above do not.

#### Q. Which command shows only messages of priority `warning` and `err`, leaving out `crit`, `alert` and `emerg`?

* [x] `journalctl -p warning..err`
* [ ] `journalctl -p warning`
* [ ] `journalctl -p err -p warning`
* [ ] `journalctl -p 4,3`

> **Explanation:** `-p` takes either one level, which means "this or more severe", or a range `FROM..TO` (names or numbers 0 to 7). `-p warning` alone would also include priorities 0 to 2.

#### Q. Which messages does `journalctl -p 4` show?

* [ ] Only messages with priority exactly `warning`
* [x] `warning` messages and anything more severe
* [ ] `warning` messages and anything less severe
* [ ] The last four journal entries

> **Explanation:** Syslog priorities run from 0 (`emerg`) to 7 (`debug`), and 4 is `warning`. A single `-p` value selects that level and all lower numbers, so 0 to 4 here. Use `-n 4` to limit the number of entries.

#### Q. Which command shows the last 10 lines of nginx's logs and then keeps printing new entries as they arrive?

* [ ] `journalctl -u nginx -n 10`
* [ ] `journalctl -u nginx -e`
* [x] `journalctl -u nginx -f`
* [ ] `journalctl -u nginx -r`

> **Explanation:** `-f` (follow) implies `-n 10` and then waits for new entries, like `tail -f`; stop it with `Ctrl+C`. `-n` alone exits after printing, `-e` jumps to the end in the pager, and `-r` shows newest entries first.

#### Q. Which command shows journal entries from the last 30 minutes?

* [x] `journalctl --since "30 min ago"`
* [ ] `journalctl -n 30`
* [ ] `journalctl -b -30`
* [ ] `journalctl --until "30 min ago"`

> **Explanation:** `--since` and `--until` accept relative times like `"1 hour ago"`, words like `today` or `yesterday`, and dates like `"2026-05-03 09:00"`. `-n 30` limits the count, and `--until` would show everything older than 30 minutes.

#### Q. A server with a persistent journal rebooted unexpectedly. Which command shows the kernel messages from the boot before the current one?

* [ ] `journalctl -k`
* [ ] `dmesg -T`
* [x] `journalctl -k -b -1`
* [ ] `journalctl -b`

> **Explanation:** `-k` selects kernel messages and implies `-b`, so on its own it shows only the current boot; `-b -1` selects the previous one. `dmesg` reads the kernel ring buffer, which starts empty at every boot.

#### Q. What does `journalctl _COMM=sshd _COMM=sudo` show?

* [x] Entries from either `sshd` or `sudo`
* [ ] Only entries that match both names at once, so nothing
* [ ] Only `sudo` entries, because the last match wins
* [ ] An error, because a field may be given only once

> **Explanation:** Matches on the same field are combined with OR, while matches on different fields, such as `_COMM=sshd _PID=1234`, are combined with AND. Options like `-u` or `-b` add further AND filters.

#### Q. Which command shows the journal entries written by process ID 1234?

* [ ] `journalctl -p 1234`
* [ ] `journalctl -u 1234`
* [x] `journalctl _PID=1234`
* [ ] `journalctl -n 1234`

> **Explanation:** A `FIELD=value` argument matches a journal field; `_PID`, `_COMM`, `_UID` and `_SYSTEMD_UNIT` are common. `-o verbose` shows all fields of each entry. `-p` filters by priority, and `-n` limits the number of lines.

#### Q. Why does `journalctl -u nginx.service` also show lines from `systemd[1]`, such as `Started nginx.service`?

* [ ] systemd relays every nginx message under its own name
* [x] `-u` also matches the messages systemd logs about that unit
* [ ] nginx runs inside PID 1, so its messages carry systemd's name
* [ ] The output also includes every message written by PID 1

> **Explanation:** For each unit, `-u` adds a match for `_SYSTEMD_UNIT=` plus matches for messages from systemd and coredumps about that unit. That is why start, stop and failure messages appear next to the service's own output.

#### Q. A backup script logs with `logger -t backup_script "Backup started"`. Which command finds those entries?

* [ ] `journalctl -u backup_script`
* [x] `journalctl -t backup_script`
* [ ] `journalctl -k backup_script`
* [ ] `journalctl -p backup_script`

> **Explanation:** `logger -t` sets the syslog identifier, and `journalctl -t` filters on it. `-u` filters by systemd unit, and a script run from a shell or cron is not a unit named `backup_script`.

#### Q. You need to feed journal entries to `jq`, one JSON object per line. Which output option do you use?

* [ ] `-o json-pretty`
* [ ] `-o verbose`
* [ ] `-o short-iso`
* [x] `-o json`

> **Explanation:** `-o json` writes each entry as a single-line JSON object with fields such as `MESSAGE`, `PRIORITY` and `_SYSTEMD_UNIT`. `json-pretty` spreads each object over many lines, which is easier to read but awkward for line-based tools.

#### Q. `Storage=` is unset in `journald.conf`, so it defaults to `auto`. `/var/log/journal` does not exist. What happens to the journal at reboot?

* [x] It is lost, because journald keeps it only in `/run/log/journal` in memory
* [ ] It is copied to `/var/log/syslog` and the binary files are removed
* [ ] It survives, because `auto` always creates `/var/log/journal`
* [ ] It is saved compressed in `/boot`

> **Explanation:** `auto` stores the journal persistently only if `/var/log/journal` exists; otherwise it uses volatile storage under `/run`. `journalctl -b -1` then has no earlier boot to show. A separate rsyslog may still keep text logs.

#### Q. `Storage=auto` is in effect. Which change makes the journal survive reboots?

* [ ] Set `Compress=yes` in `/etc/systemd/journald.conf`
* [x] Create `/var/log/journal` and restart `systemd-journald`
* [ ] Create `/run/log/journal` and restart `systemd-journald`
* [ ] Set `ForwardToSyslog=yes` in `/etc/systemd/journald.conf`

> **Explanation:** With `auto`, the existence of `/var/log/journal` switches journald to persistent storage. Setting `Storage=persistent` also works. `/run` is a tmpfs, and forwarding to syslog only feeds the text logs.

#### Q. `sudo journalctl --vacuum-size=100M` completes, but `journalctl --disk-usage` still reports 300M. What is the likely reason?

* [ ] The size is in kilobytes, so the limit was 100 GiB
* [ ] Vacuuming applies only after `systemd-journald` restarts
* [x] Vacuuming removes only archived files; the active journal files still count
* [ ] `--disk-usage` also counts the rsyslog files in `/var/log`

> **Explanation:** `--vacuum-size`, `--vacuum-time` and `--vacuum-files` never delete active journal files. Run `journalctl --rotate --vacuum-size=100M` to archive the active files first.

#### Q. Which setting permanently caps the disk space used by the persistent journal?

* [x] `SystemMaxUse=` in `/etc/systemd/journald.conf`
* [ ] `RuntimeMaxUse=` in `/etc/systemd/journald.conf`
* [ ] `rotate 4` in `/etc/logrotate.d/journal`
* [ ] `MaxLevelStore=` in `/etc/systemd/journald.conf`

> **Explanation:** `SystemMaxUse=` limits the journal in `/var/log/journal`, while `RuntimeMaxUse=` limits the volatile one in `/run/log/journal`. logrotate does not manage the binary journal. `--vacuum-*` options are one-off clean-ups.

#### Q. On Ubuntu, failed SSH logins appear in `/var/log/auth.log` but not in `/var/log/syslog`. Given the rsyslog rules below, why?

```text
auth,authpriv.*              /var/log/auth.log
*.*;auth,authpriv.none       -/var/log/syslog
```

* [ ] `syslog` receives only kernel messages
* [x] The second rule matches everything except the `auth` and `authpriv` facilities
* [ ] rsyslog writes each message to the first matching file only
* [ ] sshd writes `auth.log` itself, bypassing rsyslog

> **Explanation:** In a selector list separated by `;`, later selectors override earlier ones, and `none` excludes a facility. The first rule sends those facilities to `auth.log`. On RHEL the equivalent files are `/var/log/secure` and `/var/log/messages`.

#### Q. On a RHEL or Fedora system with rsyslog, which files usually hold the general system log and the authentication log?

* [ ] `/var/log/syslog` and `/var/log/auth.log`
* [ ] `/var/log/kern.log` and `/var/log/sudo.log`
* [ ] `/var/log/journal` and `/var/log/lastlog`
* [x] `/var/log/messages` and `/var/log/secure`

> **Explanation:** Red Hat-style systems use `messages` and `secure`, while Debian and Ubuntu use `syslog` and `auth.log`. `/var/log/journal` holds the binary journal, read with `journalctl`.

#### Q. Which rsyslog rule writes mail messages of priority `info` only, without the more severe levels?

* [ ] `mail.info     /var/log/mail.info`
* [x] `mail.=info    /var/log/mail.info`
* [ ] `mail.!info    /var/log/mail.info`
* [ ] `mail.*        /var/log/mail.info`

> **Explanation:** A plain priority such as `mail.info` matches that level and everything more severe. The `=` prefix selects exactly one level, `!` excludes levels, and `*` matches all priorities.

#### Q. In an rsyslog client rule such as `*.* @@logserver.example.com:514`, what does `@@` mean?

* [x] Forward over TCP
* [ ] Forward over UDP
* [ ] Forward over TLS only
* [ ] Forward to two servers

> **Explanation:** A single `@` forwards over UDP and `@@` over plain TCP, which is more reliable than UDP but still unencrypted. Encryption needs extra TLS configuration on both sides.

#### Q. What does the `& stop` line do in this rsyslog file?

```text
if $programname == 'myapp' then /var/log/myapp.log
& stop
```

* [ ] It stops rsyslog after the first message from `myapp` has been written
* [ ] It stops the `myapp` process when it logs too many messages
* [ ] It closes and reopens `/var/log/myapp.log` after each write
* [x] It discards the matched messages after writing them, so later rules skip them

> **Explanation:** `&` applies another action to the same filter, and `stop` ends processing for those messages. Without it, `myapp` lines would also reach later rules, such as the one writing `/var/log/syslog`.

#### Q. `logrotate -f` is run four times on `app.log`, which gets new lines before each run, with the config below. Which old logs exist afterwards?

```text
/var/log/app.log {
    rotate 2
    compress
    delaycompress
}
```

* [x] `app.log.1` and `app.log.2.gz`
* [ ] `app.log.1.gz` and `app.log.2.gz`
* [ ] `app.log.1`, `app.log.2` and `app.log.3`
* [ ] `app.log.1.gz` to `app.log.4.gz`

> **Explanation:** `rotate 2` keeps two old logs and deletes older ones. `delaycompress` leaves the newest rotated file uncompressed until the next cycle, so a program still writing to it is not cut off.

#### Q. An app opens `app.log` once at start-up and never reopens it. logrotate rotates the file with `create` and no `postrotate` script. What happens next?

* [ ] The app writes to the new `app.log`, because the path is the same
* [ ] The app crashes because its log file was deleted
* [x] The app keeps writing into `app.log.1`, and the new `app.log` stays empty
* [ ] logrotate waits until the app closes the file

> **Explanation:** Renaming does not change the open file descriptor, so writes follow the inode now called `app.log.1`. Add a `postrotate` command that tells the app to reopen its log (reload or signal), or use `copytruncate`.

#### Q. What is the trade-off of the logrotate option `copytruncate`?

* [ ] It needs twice the inodes, so it fails on most filesystems
* [x] Lines written between the copy and the truncate can be lost
* [ ] It cannot be combined with `compress`
* [ ] It sends `SIGHUP` to every process that has the file open

> **Explanation:** `copytruncate` copies the log and then truncates the original in place, so writers keep the same file and need no restart. Data logged in the short gap between the two steps is lost, and `create` has no effect.

#### Q. Which command shows what logrotate would do with your configuration, without rotating anything?

* [ ] `sudo logrotate -f /etc/logrotate.conf`
* [ ] `sudo logrotate -s /etc/logrotate.conf`
* [x] `sudo logrotate -d /etc/logrotate.conf`
* [ ] `sudo logrotate -m /etc/logrotate.conf`

> **Explanation:** `-d` (debug) implies verbose output and makes no changes to logs or the state file. `-f` forces a rotation even if it is not due, `-s` names a state file, and `-m` sets a mail command.

#### Q. On Ubuntu 24.04, what normally runs logrotate once a day?

* [ ] A long-running `logrotated` daemon
* [ ] `systemd-journald`, after each journal rotation
* [ ] rsyslog, when it receives `SIGHUP`
* [x] `logrotate.timer`, which starts `logrotate.service`

> **Explanation:** The timer has `OnCalendar=daily` and `Persistent=true`; check it with `systemctl list-timers | grep logrotate`. Older systems run it from `/etc/cron.daily/logrotate`. Its state is kept in `/var/lib/logrotate/status`.

#### Q. `/var/log` is full. You run `rm /var/log/huge.log`, but `df` shows no free space gained. Why?

* [x] A process still holds the file open, so its blocks are not freed yet
* [ ] `rm` moves files from `/var/log` to a trash directory first
* [ ] `df` only updates after the journal is rotated
* [ ] The file was a hard link to the journal

> **Explanation:** Deleting removes the name, but the inode lives on while any process holds it open; `ls -l /proc/<pid>/fd` shows it as `(deleted)`. Truncate active logs with `truncate -s 0` or restart the writer instead.

#### Q. You run the command below on the line that follows it. What does it print?

```bash
awk '{print $(NF-3)}' <<< 'May 03 11:00:01 server sshd[23456]: Failed password for invalid user admin from 203.0.113.10 port 54323 ssh2'
```

* [ ] `54323`
* [ ] `from`
* [x] `203.0.113.10`
* [ ] `port`

> **Explanation:** `NF` is the number of fields, so `$NF` is `ssh2`, `$(NF-1)` is `54323`, `$(NF-2)` is `port` and `$(NF-3)` is the IP. Counting from the end works whether the user name is one word or `invalid user admin`.

#### Q. You watch a directory with `inotifywait -m /w` and run `echo hi > /w/f`, where `f` did not exist. Which event sequence is printed?

* [ ] `MODIFY f`, then `CREATE f`
* [ ] `CREATE f` only
* [ ] `OPEN f`, `CREATE f`, `CLOSE_NOWRITE,CLOSE f`
* [x] `CREATE f`, `OPEN f`, `MODIFY f`, `CLOSE_WRITE,CLOSE f`

> **Explanation:** The shell creates and opens the file, writes to it, then closes it. Each step is a separate inotify event; `CLOSE_WRITE` marks the close of a file that was open for writing.

#### Q. A script must process each uploaded file once, after the upload has finished writing it. Which event should `inotifywait` wait for?

* [ ] `-e modify`
* [ ] `-e create`
* [x] `-e close_write`
* [ ] `-e open`

> **Explanation:** `modify` fires for every write, so a large file triggers many events, and `create` fires before any data arrives. `close_write` fires once, when a writer closes the file; add `moved_to` for files moved in.

#### Q. While watching `/w`, you run `mv /w/f /w/g`. Which events does inotify report?

* [x] `MOVED_FROM f` and `MOVED_TO g`, linked by the same cookie
* [ ] `DELETE f` followed by `CREATE g` for the new name
* [ ] `MODIFY f` followed by `ATTRIB g` for the new name
* [ ] `MOVE_SELF f`, because the file itself was moved

> **Explanation:** A rename inside a watched directory produces two events with the same `cookie` field, which lets a program pair the old and new names. `MOVE_SELF` is reported only when the watched item itself is moved.

#### Q. You run `inotifywait -m /etc/app.conf` and edit the file with `sed -i`. After a `DELETE_SELF` event, later changes to the file are not reported. Why?

* [ ] `sed -i` turns off inotify for the files it edits in place
* [ ] inotifywait reports only the first change made to any watched file
* [ ] The event queue overflowed, so the kernel removed the watch
* [x] `sed -i` writes a new file and renames it over the old one, so the watched inode is gone

> **Explanation:** A watch belongs to an inode, not a path. Editors and `sed -i` often replace the file, so the old inode is deleted and its watch removed. Watch the directory instead and filter on the file name.

#### Q. `inotifywait -m /w` is running. A program creates `/w/sub/z`, where `/w/sub` is an existing subdirectory. What is printed?

* [ ] `/w/ CREATE sub/z`
* [x] No event at all
* [ ] `/w/ MODIFY sub`
* [ ] `/w/sub/ CREATE z`

> **Explanation:** A directory watch covers only its direct entries; kernel inotify watches are not recursive. `inotifywait -r` adds one watch per subdirectory, which can hit `fs.inotify.max_user_watches` on large trees.

#### Q. `inotifywait -r -m /srv/data` fails on a large tree, reporting that the inotify watch limit was reached. Which change fixes this?

* [ ] Raise `ulimit -n` for the shell
* [ ] Raise `fs.file-max` with `sysctl`
* [ ] Remount `/srv/data` with `noatime`
* [x] Raise `fs.inotify.max_user_watches` with `sysctl`

> **Explanation:** Each watched directory uses one watch, and the per-user limit is in `/proc/sys/fs/inotify/max_user_watches`. Put the new value in a file under `/etc/sysctl.d/` to keep it after reboot.

#### Q. A watcher reads an `IN_Q_OVERFLOW` event. What should it do?

* [ ] Nothing; the kernel resends the lost events later
* [ ] Restart the machine to clear the queue
* [ ] Lower `max_user_watches` so fewer events are queued
* [x] Rescan the watched paths, because some events were dropped

> **Explanation:** When more than `max_queued_events` events are waiting, the kernel drops new ones and queues one overflow event. The program can no longer trust its view, so it must rebuild its state from the filesystem.

#### Q. A scanner must be able to stop a program from opening a file until the file has been checked. Which kernel interface supports that?

* [ ] inotify, using `IN_OPEN`
* [x] fanotify, using permission events
* [ ] dnotify, using signals
* [ ] inotify, using `IN_ACCESS`

> **Explanation:** inotify only reports events after they happen. fanotify can mark whole mounts or filesystems and ask a user-space program to allow or deny an access, which is why antivirus tools use it.
