## Disk Usage Management

The ability to manage and monitor disk usage is crucial when maintaining Linux systems. Disk usage is often checked when diagnosing system issues, planning for future storage requirements, or cleaning up unused files and directories.

## Understanding the df command

The `df` (disk filesystem) command provides insights into the filesystems of your machine. It details the total size, space used, space available, and percentage of space used. To display these statistics in a human-readable format, using standard units like KB, MB, GB, use the `-h` (human-readable) option.

For instance, executing `df -h` would yield an output similar to the following:

| Filesystem | Size | Used | Available | Use% | Mounted on |
| --- | --- | --- | --- | --- | --- |
| /dev/sda1 | 2.00T | 1.00T | 1.00T | 50% | / |
| /dev/sda2 | 2.00T | 1.00T | 1.00T | 50% | /boot |

This output details the following:

* `Filesystem`: This column lists the name of each filesystem.
* `Size`: This depicts the total size of each filesystem.
* `Used`: This indicates the space used within each filesystem.
* `Available`: This shows the remaining space within each filesystem.
* `Use%`: This highlights the percentage of total space used in each filesystem.
* `Mounted on`: This tells you the mount point of each filesystem, which is where the filesystem is accessible in the system's directory structure.

## Diving into the du command

The `du` (disk usage) command is used to estimate the space used by given files or directories. The `-h` option can be used for human-readable output, while the `-s` option can be used to provide a summarized result for directories. For instance, executing `du -sh .` will display the total size of the current directory in a human-readable format.

If you want to identify the top 10 largest directories starting from the root directory (`/`), you could use the following command:

```bash
du -x / | sort -nr | head -10
```

Here's an example of what the output might look like:

```
10485760    /usr
5120000     /var
2097152     /lib
1024000     /opt
524288      /boot
256000      /home
128000      /bin
64000       /sbin
32000       /etc
16000       /tmp
```

In this command, `du -x /` estimates the size of each directory in the root filesystem. `sort -nr` sorts these estimates in numerical order and reverses the output to display the largest sizes first. Finally, `head -10` truncates the output to only the top 10 lines, thereby showing the 10 largest directories.

## The ncdu Command

For a more visual representation of disk usage, you might consider using `ncdu` (NCurses Disk Usage). `ncdu` is a ncurses-based tool that provides a fast and easy-to-use interface to find out what directories are using your disk space. If it's not pre-installed, you can easily install it using your package manager, such as `apt` or `yum`. 

The command `ncdu -x /` will start at the root directory (`/`) and present an interactive interface where you can browse directories and see their sizes.

An example output might look like this in a non-interactive, textual representation:

```
ncdu 1.15 ~ Use the arrow keys to navigate, press ? for help
--- / -----------------------------------------------------------------------
    4.6 GiB [##########] /usr
    2.1 GiB [####      ] /var
  600.0 MiB [#         ] /lib
  500.0 MiB [#         ] /opt
  400.0 MiB [          ] /boot
  300.0 MiB [          ] /sbin
  200.0 MiB [          ] /bin
  100.0 MiB [          ] /etc
   50.0 MiB [          ] /tmp
   20.0 MiB [          ] /home
   10.0 MiB [          ] /root
    5.0 MiB [          ] /run
    1.0 MiB [          ] /srv
    0.5 MiB [          ] /dev
    0.1 MiB [          ] /mnt
    0.0 MiB [          ] /proc
    0.0 MiB [          ] /sys
 Total disk usage: 8.8 GiB  Apparent size: 8.8 GiB  Items: 123456
```

## Cleaning Up Disk Space

Once you've identified what's using your disk space, the next step is often to free up space. Here are a few strategies:

1. **Remove Unnecessary Packages and Dependencies**: Over time, your system may accumulate packages that are no longer needed. These can be safely removed to free up space. On a Debian-based system like Ubuntu, you can use `apt-get autoremove` to remove unnecessary packages.

2. **Clear Package Manager Cache**: Most package managers store package files in a cache that can take up a lot of space. For example, to clear the cache in a system using `apt`, use the command `apt-get clean`.

3. **Find and Remove Large Files**: You can use the `find` command to locate files over a certain size and then decide if they need to be kept. For example, `find / -type f -size +100M` will find files larger than 100 MB.

4. **Use a Disk Cleanup Utility**: Tools like `bleachbit` can be used to clean up various types of unnecessary files, like cache, cookies, internet history, temporary files, log files, and so on.

5. **Archive and Compress Less Used Data**: If there are directories or files not accessed frequently, consider compressing them to save space. Tools like `tar`, `gzip`, `bzip2` can be used for this.

## Automating Disk Usage Checks

For ongoing disk usage monitoring, consider setting up automated tasks. For instance, you can schedule a cron job that runs `df` and `du` at regular intervals and sends reports via email or logs them for later review.

Monitoring disk usage proactively can prevent potential issues related to low disk space, such as application errors, slow performance, or system crashes.

### Bash Script Example for Disk Usage Monitoring

```bash
#!/bin/bash

# Script to monitor disk usage and report

# Set the path for the log file
LOG_FILE="/var/log/disk_usage_report.log"

# Get disk usage with df
echo "Disk Usage Report - $(date)" >> "$LOG_FILE"
echo "---------------------------------" >> "$LOG_FILE"
df -h >> "$LOG_FILE"

# Get top 10 directories consuming space
echo "" >> "$LOG_FILE"
echo "Top 10 Directories by Size:" >> "$LOG_FILE"
du -x / | sort -nr | head -10 >> "$LOG_FILE"

# Optionally, you can send this log via email instead of writing to a file
# For email, you can use: mail -s "Disk Usage Report" recipient@example.com < "$LOG_FILE"

# End of script
```

- Save it as `disk_usage_monitor.sh`.
- If you prefer to move the script to a standard location for cron jobs and set it up with a single command, you can use a system directory like `/etc/cron.daily`. This directory is used for scripts that should be run daily by the system's cron daemon. Here's how you can do it:

```bash
sudo chmod +x /path/to/disk_usage_monitor.sh && sudo mv /path/to/disk_usage_monitor.sh /etc/cron.daily/
```

## Challenges

1. Display the free space available on the root filesystem (`/`).
2. For each mounted filesystem, show the percentage of space used.
3. Provide information about all filesystems, including those that are not currently mounted.
4. Determine the size of the directory you're currently in.
5. Check and report the size of the `/home` directory.
6. Identify the 10 largest directories in the system.
7. Track and report the amount of data being written to the disk in real-time.
8. Locate individual files that are taking up the most space on the disk.
9. Take snapshots of disk usage at different times and compare them to identify growth trends.
10. Break down disk usage statistics by the types of files (e.g., `.txt`, `.jpg`, `.log`).
