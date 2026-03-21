## Inotify

Inotify is a Linux kernel subsystem that provides a mechanism for monitoring file system events. It allows applications to watch files and directories for changes such as creation, deletion, modification, and access. Rather than repeatedly polling the file system to detect changes, inotify delivers event notifications directly to user-space programs, making it both efficient and responsive.

System administrators, developers, and DevOps engineers rely on inotify for tasks ranging from live log monitoring and automated backup triggers to build-system watchers and security auditing. The kernel-level integration means inotify imposes minimal overhead, even when watching large numbers of files.

### How Inotify Works

```
+------------------------------------------------------------------+
|                      Inotify Workflow Overview                   |
+------------------------------------------------------------------+
         │
         ▼
+--------------------------------------+       +----------------------------------+
|       User-Space Application         |       |        Kernel (VFS Layer)        |
|   (Creates inotify instance and      |       |  (Tracks watched inodes and      |
|    adds watches on files/dirs)       |       |   generates events on changes)   |
+--------------------------------------+       +----------------------------------+
         │                                                      │
         │   inotify_init() / inotify_add_watch()               │
         --------------------------------------------------------
                                       |
                                       ▼
                         +-------------------------------+
                         |     Inotify File Descriptor   |
                         |   (Readable via read()/poll() |
                         |    when events are queued)     |
                         +-------------------------------+
                                       │
                                       │ Kernel queues inotify_event
                                       │ structs as changes happen
                                       ▼
                         +---------------------------------+
                         |   Application Reads Events      |
                         | (Processes each event and acts) |
                         +---------------------------------+
```

- An application begins by calling `inotify_init()` to create an inotify instance, which returns a **file descriptor** used for all subsequent operations.
- Watches are added with `inotify_add_watch()`, specifying a **path** and a bitmask of event types to monitor (e.g., `IN_MODIFY`, `IN_CREATE`, `IN_DELETE`).
- When a watched event occurs, the kernel places an `inotify_event` structure on the inotify file descriptor's **read queue**.
- The application retrieves events by calling `read()` on the file descriptor, or uses `poll()`/`select()`/`epoll()` to **wait** for events without busy-looping.
- Each event contains the **watch descriptor**, the event **mask**, an optional **cookie** for pairing rename events, and the **filename** when the watch is on a directory.
- A watch can be removed with `inotify_rm_watch()`, and closing the inotify file descriptor **cleans up** all associated watches automatically.

### Event Types

Inotify can watch for a variety of file system events. The table below lists the most commonly used event masks.

| Event Mask      | Description                                                          |
|-----------------|----------------------------------------------------------------------|
| `IN_ACCESS`     | File was accessed (read).                                            |
| `IN_MODIFY`     | File was modified (write).                                           |
| `IN_ATTRIB`     | Metadata changed (permissions, timestamps, extended attributes).     |
| `IN_CLOSE_WRITE`| File opened for writing was closed.                                  |
| `IN_CLOSE_NOWRITE`| File opened read-only was closed.                                 |
| `IN_OPEN`       | File was opened.                                                     |
| `IN_MOVED_FROM` | File was moved out of the watched directory.                         |
| `IN_MOVED_TO`   | File was moved into the watched directory.                           |
| `IN_CREATE`     | File or directory was created in the watched directory.              |
| `IN_DELETE`     | File or directory was deleted from the watched directory.            |
| `IN_DELETE_SELF` | Watched file or directory itself was deleted.                       |
| `IN_MOVE_SELF`  | Watched file or directory itself was moved.                          |

Convenience masks combine related events for common use cases:

| Convenience Mask | Equivalent Events                                              |
|------------------|----------------------------------------------------------------|
| `IN_CLOSE`       | `IN_CLOSE_WRITE` \| `IN_CLOSE_NOWRITE`                        |
| `IN_MOVE`        | `IN_MOVED_FROM` \| `IN_MOVED_TO`                               |
| `IN_ALL_EVENTS`  | All of the above events combined.                              |

### Using inotifywait and inotifywatch

The `inotify-tools` package provides two command-line utilities that expose the inotify API without writing any code.

#### Installing inotify-tools

On Debian/Ubuntu-based systems:

```bash
sudo apt install inotify-tools
```

On Red Hat/Fedora-based systems:

```bash
sudo dnf install inotify-tools
```

On Arch Linux:

```bash
sudo pacman -S inotify-tools
```

#### inotifywait

`inotifywait` blocks until one or more inotify events occur on the specified files or directories. It is the most commonly used tool for scripting file-system triggers.

I. Watch a single file for modification:

```bash
inotifywait -e modify /var/log/syslog
```

When `/var/log/syslog` is written to, the command prints the event and exits:

```
/var/log/syslog MODIFY
```

II. Continuously monitor a directory for any changes:

```bash
inotifywait -m -r /home/user/projects
```

The `-m` flag keeps the watcher running (monitor mode) and `-r` watches all subdirectories recursively. Sample output as files change:

```
/home/user/projects/ CREATE main.c
/home/user/projects/ MODIFY main.c
/home/user/projects/ CLOSE_WRITE,CLOSE main.c
/home/user/projects/build/ CREATE output.o
```

III. Watch for specific events with a custom output format:

```bash
inotifywait -m -r -e create -e delete --format '%T %w%f %e' --timefmt '%Y-%m-%d %H:%M:%S' /etc
```

This monitors `/etc` for file creation and deletion, printing a timestamped log:

```
2025-03-21 10:15:42 /etc/nginx/sites-enabled/mysite CREATE
2025-03-21 10:16:03 /etc/nginx/sites-enabled/oldsite DELETE
```

#### inotifywatch

`inotifywatch` collects file system event statistics over a period of time, rather than printing individual events. This is useful for profiling which files or directories see the most activity.

I. Gather statistics for 60 seconds on a directory:

```bash
inotifywatch -t 60 -r /var/log
```

After 60 seconds, it prints a summary table:

```
total  access  modify  close_write  open  filename
45     12      8       8            17    /var/log/
22     5       6       6            5     /var/log/nginx/
9      3       2       2            2     /var/log/auth.log
```

II. Focus on specific event types:

```bash
inotifywatch -t 30 -e modify -e create /home/user/uploads
```

### Practical Shell Script Examples

Inotify is especially powerful when combined with shell scripts to automate responses to file system changes.

#### Automated Backup on File Change

This script watches a directory and copies any modified or newly created file to a backup location:

```bash
#!/bin/bash
WATCH_DIR="/home/user/documents"
BACKUP_DIR="/home/user/backups"

inotifywait -m -r -e close_write -e moved_to --format '%w%f' "$WATCH_DIR" |
while read -r FILE; do
    RELATIVE="${FILE#$WATCH_DIR/}"
    mkdir -p "$BACKUP_DIR/$(dirname "$RELATIVE")"
    cp "$FILE" "$BACKUP_DIR/$RELATIVE"
    echo "Backed up: $RELATIVE"
done
```

- The script uses `close_write` to trigger only after a file has been completely written and closed.
- The `moved_to` event catches files moved into the directory.
- `--format '%w%f'` outputs the full path of the affected file for easy processing.

#### Log Watcher with Alert

This script monitors a log file for error messages and sends a notification:

```bash
#!/bin/bash
LOG_FILE="/var/log/application.log"

inotifywait -m -e modify --format '%w%f' "$LOG_FILE" |
while read -r FILE; do
    if tail -n 1 "$FILE" | grep -qi "error"; then
        echo "ERROR detected in $FILE at $(date)" >> /var/log/alert.log
    fi
done
```

### The Inotify C API

For applications that need tighter integration, the inotify system calls are available directly in C.

```
+------------------------------------------+
|           inotify C API Flow             |
+------------------------------------------+
|                                          |
|  1. fd = inotify_init()                  |
|        │                                 |
|        ▼                                 |
|  2. wd = inotify_add_watch(fd,           |
|           "/path", IN_MODIFY | IN_CREATE)|
|        │                                 |
|        ▼                                 |
|  3. read(fd, buf, BUF_LEN)              |
|        │                                 |
|        ▼                                 |
|  4. Process inotify_event structs        |
|     from buf                             |
|        │                                 |
|        ▼                                 |
|  5. inotify_rm_watch(fd, wd)            |
|     close(fd)                            |
+------------------------------------------+
```

A minimal C program that watches a directory:

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/inotify.h>

#define BUF_LEN (10 * (sizeof(struct inotify_event) + 256))

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <path>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int fd = inotify_init();
    if (fd == -1) {
        perror("inotify_init");
        exit(EXIT_FAILURE);
    }

    int wd = inotify_add_watch(fd, argv[1], IN_CREATE | IN_DELETE | IN_MODIFY);
    if (wd == -1) {
        perror("inotify_add_watch");
        exit(EXIT_FAILURE);
    }

    printf("Watching %s for changes...\n", argv[1]);

    char buf[BUF_LEN];
    for (;;) {
        ssize_t len = read(fd, buf, BUF_LEN);
        if (len <= 0) {
            perror("read");
            exit(EXIT_FAILURE);
        }

        char *ptr = buf;
        while (ptr < buf + len) {
            struct inotify_event *event = (struct inotify_event *)ptr;
            if (event->mask & IN_CREATE) printf("CREATED: %s\n", event->name);
            if (event->mask & IN_DELETE) printf("DELETED: %s\n", event->name);
            if (event->mask & IN_MODIFY) printf("MODIFIED: %s\n", event->name);
            ptr += sizeof(struct inotify_event) + event->len;
        }
    }

    inotify_rm_watch(fd, wd);
    close(fd);
    return 0;
}
```

### Kernel Limits and Tuning

Inotify operates within kernel-imposed limits that control resource usage. These limits can be viewed and adjusted through `/proc/sys/fs/inotify/`.

| Parameter                          | Description                                                     | Default |
|------------------------------------|-----------------------------------------------------------------|---------|
| `max_user_instances`               | Maximum number of inotify instances per user.                   | 128     |
| `max_user_watches`                 | Maximum number of watches per user across all instances.        | 65536   |
| `max_queued_events`                | Maximum number of events queued before events start being dropped. | 16384   |

I. View the current watch limit:

```bash
cat /proc/sys/fs/inotify/max_user_watches
```

II. Temporarily increase the watch limit:

```bash
sudo sysctl fs.inotify.max_user_watches=524288
```

III. Make the change persistent across reboots by adding to `/etc/sysctl.conf`:

```bash
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

Applications that monitor many files (such as IDEs, build tools, or file-syncing utilities) may require increasing `max_user_watches`. The kernel allocates approximately 1 KB of kernel memory per watch on 64-bit systems, so setting the limit to 524288 uses roughly 512 MB of memory.

### Inotify vs Alternatives

| Feature                  | Inotify                          | fanotify                          | dnotify (legacy)              |
|--------------------------|----------------------------------|-----------------------------------|-------------------------------|
| Granularity              | File and directory level         | Filesystem-wide or mount-point    | Directory level only          |
| Recursive watching       | Not built-in (requires manual)   | Mark entire mount points          | Not supported                 |
| Permission decisions     | No                               | Yes (allow/deny file access)      | No                            |
| Event detail             | Rich (path, mask, cookie)        | Rich (includes file descriptor)   | Signal-based, limited info    |
| Kernel version required  | 2.6.13+                          | 2.6.37+                           | 2.4+                          |
| Typical use case         | File watchers, build tools       | Antivirus, access control         | Legacy applications           |

- **Inotify** is the standard choice for monitoring individual files and directories with fine-grained event information. Most user-space tools and frameworks (e.g., `inotifywait`, Node.js `fs.watch`, Python `watchdog`) are built on it.
- **fanotify** is suited for system-wide monitoring and access-control decisions, commonly used by antivirus software and security tools.
- **dnotify** is the predecessor to inotify and is considered obsolete. It required holding open file descriptors on watched directories and delivered events via signals, making it cumbersome and limited.

### Common Use Cases

- **Build systems** such as `make`, `webpack`, and `cargo` use inotify to detect source file changes and trigger automatic rebuilds.
- **File synchronization** tools like `rsync`-based watchers and `lsyncd` use inotify to detect changes and replicate them to remote servers in near real-time.
- **Log monitoring** is simplified with inotify because utilities can react to new log entries the moment they are written rather than polling at intervals.
- **Security auditing** benefits from inotify by allowing administrators to watch critical configuration files (e.g., `/etc/passwd`, `/etc/shadow`) for unauthorized modifications.
- **Development environments** including IDEs and text editors use inotify to refresh file listings and detect external modifications to open files.
- **Containerized workloads** and orchestration tools watch configuration files for hot-reload without restarting services.

### Challenges

1. Install `inotify-tools` on your system and use `inotifywait` to monitor your home directory for any file creation events. Create a few files and observe the output.
2. Write a shell script that uses `inotifywait` in monitor mode to watch a directory and log every modification event with a timestamp to a log file.
3. Use `inotifywatch` to gather file system event statistics on `/tmp` for two minutes, then analyze which event types occurred most frequently.
4. Investigate the current inotify kernel limits on your system by reading the values in `/proc/sys/fs/inotify/`. Explain what each parameter controls and when you might need to increase them.
5. Create a shell script that watches a directory for new files and automatically moves any file with a `.tmp` extension to a designated cleanup folder.
6. Monitor `/etc` for any changes using `inotifywait` with recursive mode. Make a small configuration change and verify that inotify reports it correctly.
7. Write a C program using the inotify API that watches a directory and prints a message whenever a file is created, modified, or deleted.
8. Compare the behavior of `inotifywait` when watching a single file versus a directory. Explain the differences in event reporting and the role of the filename field in `inotify_event`.
9. Set up two terminal sessions: in one, run an `inotifywait` monitor on a directory, and in the other, perform operations such as creating, renaming, and deleting files. Observe how rename events use the `cookie` field to pair `IN_MOVED_FROM` and `IN_MOVED_TO`.
10. Research the limitations of inotify with respect to recursive directory watching and high watch counts. Propose a strategy for monitoring a large project tree with thousands of subdirectories while staying within kernel limits.
