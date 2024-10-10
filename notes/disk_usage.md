## Disk Usage Management

The ability to manage and monitor disk usage comes handy when maintaining servers. Disk usage is often checked when diagnosing system issues, planning for future storage requirements, or cleaning up unused files and directories.

### Understanding the df command

The `df` (disk filesystem) command provides information about the filesystems on your machine. It shows details such as total size, used space, available space, and the percentage of space used. To display these statistics in a human-readable format, using units like KB, MB, or GB, you can use the `-h` (human-readable) option.

For example, executing `df -h` might produce an output like the following:

| Filesystem | Size | Used | Available | Use% | Mounted on |
| --- | --- | --- | --- | --- | --- |
| /dev/sda1 | 2.0T | 1.0T | 1.0T | 50% | / |
| /dev/sda2 | 500G | 200G | 300G | 40% | /boot |

This output provides the following information:

* `Filesystem`: The name of each filesystem.
* `Size`: The total size of each filesystem.
* `Used`: The amount of space that has been used within each filesystem.
* `Available`: The remaining free space within each filesystem.
* `Use%`: The percentage of total space that has been used in each filesystem.
* `Mounted on`: The mount point of each filesystem, indicating where it is accessible within the system's directory structure.

### Exploring the `du` Command

The `du` (disk usage) command is used to estimate the space occupied by files or directories. To display the output in a human-readable format, you can use the `-h` option. The `-s` option provides a summarized result for directories. For example, running `du -sh .` will show the total size of the current directory in a human-readable format.

To find the top 10 largest directories starting from the root directory (`/`), you can use the following command:

```bash
du -x / | sort -nr | head -10
```

An example output might look like this:

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

In this command:

- `du -x /` calculates the size of each directory within the root filesystem.
- `sort -nr` sorts these sizes in descending numerical order.
- `head -10` limits the output to the top 10 largest directories.

This command sequence helps you quickly identify the directories consuming the most space on your system.

To further improve the speed of the `du` command, especially when dealing with many subdirectories, you can use `xargs -P` to parallelize the processing. This approach takes advantage of multiple CPU cores, allowing `du` to run on multiple directories simultaneously. Additionally, combining it with `awk` can help format the output more cleanly.

Here’s an enhanced example that finds the top 10 largest directories and uses `xargs` to speed up the process:

```bash
find / -maxdepth 1 -type d | xargs -I{} -P 4 du -sh {} 2>/dev/null | sort -hr | head -10 | awk '{printf "%-10s %s\n", $1, $2}'
```

Explanation:

I. `find / -maxdepth 1 -type d`: This command finds all directories at the root level (`/`), limiting the search to the top-level directories only (`-maxdepth 1`).

II. `xargs -I{} -P 4 du -sh {} 2>/dev/null`: 

- `xargs` takes the output of `find` and passes each directory to the `du` command.
- `-I{}` is used to specify the replacement string `{}` for the directory name.
- `-P 4` specifies that up to 4 `du` processes can run in parallel, leveraging multiple cores for faster execution.
- `du -sh {}` calculates the size of each directory in a human-readable format.
- `2>/dev/null` suppresses any error messages, such as permission denied errors.

III. `sort -hr`: Sorts the output in human-readable format and in reverse order, so the largest directories come first.

IV. `head -10`: Limits the output to the top 10 largest directories.

V. `awk '{printf "%-10s %s\n", $1, $2}'`: Formats the output, ensuring the size and directory name align neatly. The `%-10s` ensures the size column has a fixed width, making the output more readable.

By using `xargs -P`, you can significantly reduce the time it takes to compute the disk usage of directories, especially on systems with many directories and multiple CPU cores. This method effectively utilizes system resources to perform the operation more efficiently.

### The `ncdu` Command

For a more visual and interactive representation of disk usage, you can use `ncdu` (NCurses Disk Usage). `ncdu` is a ncurses-based tool that provides a user-friendly interface to quickly assess which directories are consuming the most disk space. If it is not already installed, you can install it via your package manager, such as `apt` for Debian-based systems or `yum` for Red Hat-based systems.

Running the command `ncdu -x /` will start the program at the root directory (`/`) and present an interactive interface. Here, you can navigate through directories using arrow keys and view their sizes, making it easier to identify space hogs.

Here’s an example of what the output might look like in a non-interactive, textual representation:

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

In this output:

- The bar `[##########]` visually represents the proportion of disk space used by each directory.
- The size of each directory is displayed, making it easy to compare.
- The total disk usage and apparent size are summarized at the bottom, along with the total number of items analyzed.

`ncdu` is especially useful for quickly finding large directories and files, thanks to its intuitive interface. The ability to easily navigate through directories makes it a powerful tool for managing disk space on your system.

### Cleaning Up Disk Space

Once you've identified what's using your disk space, the next step is often to free up space. Here are a few strategies:

- Removing unnecessary packages and dependencies is an effective way to free up disk space. Over time, systems can accumulate outdated or unused packages, which can be safely removed. For instance, on a Debian-based system like Ubuntu, the `apt-get autoremove` command can help clean out these unused packages.
- Clearing the package manager cache can also reclaim significant disk space. Package managers often store downloaded packages in a cache, which can grow large over time. On systems using `apt`, you can use the `apt clean` command to clear the cache.
- Finding and removing large files is another strategy. The `find` command can be utilized to search for files exceeding a certain size, enabling users to review and decide if those files should be deleted. For example, `find / -type f -size +100M` will list files larger than 100 MB.
- Using a disk cleanup utility can automate the process of deleting various unnecessary files. Tools like `bleachbit` can efficiently remove temporary files, cache, cookies, internet history, and log files, helping to free up space.
- Archiving and compressing less frequently used data can also save space. Files and directories that are rarely accessed can be compressed using tools like `tar`, `gzip`, or `bzip2`, reducing their size and freeing up more disk space.

### Automating Disk Usage Checks

For ongoing disk usage monitoring, consider setting up automated tasks. For instance, you can schedule a cron job that runs `df` and `du` at regular intervals and sends reports via email or logs them for later review.

Monitoring disk usage proactively can prevent potential issues related to low disk space, such as application errors, slow performance, or system crashes.

#### Bash Script Example for Disk Usage Monitoring

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

### Challenges

1. Explain the concept of filesystems and mount points, and then display the available free space on the root filesystem (`/`). Discuss why monitoring free space on the root is crucial for system stability.
2. List all currently mounted filesystems and calculate the percentage of space used on each. Explain the importance of monitoring multiple filesystems, especially in systems with separate partitions for critical directories like `/var`, `/home`, or `/boot`.
3. Identify all filesystems configured on the system, whether mounted or not, and display relevant information such as filesystem type, size, and last mount point. Discuss the purpose of different filesystem types and reasons they might not be mounted.
4. Calculate the total size of the directory you’re in, including all files and subdirectories. Discuss recursive disk usage and the impact of nested directories on storage.
5. Provide a breakdown of disk space usage within the `/home` directory for each user. Discuss the significance of managing space within `/home` and how it affects individual user accounts.
6. List the top 10 directories consuming the most disk space across the entire system. Explain how these large directories can affect disk performance and the importance of periodically checking them.
7. Track data being written to the disk in real-time for a set period, displaying a summary of write activity. Discuss the reasons behind tracking disk write activity, including potential implications for system performance and health.
8. Identify individual files that occupy the most space on the disk. Discuss strategies for managing large files and how deleting or relocating these files can reclaim disk space.
9. Take snapshots of disk usage at two different times and compare them to identify any significant changes or trends. Discuss the importance of historical data in predicting future disk space needs and planning for expansion or cleanup.
10. Analyze disk usage by categorizing files based on their extensions (e.g., `.txt`, `.jpg`, `.log`). Explain how file type classification can help in identifying disk space hogs and in organizing cleanup strategies.
