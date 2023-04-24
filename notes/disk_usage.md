## Linux Disk Usage Management Guide

Learn the basics of `df` and `du` commands for checking disk usage, finding large files and directories, and freeing up disk space. Also, get tips to optimize disk space usage and avoid running out of space.

## The df command

`df` command shows information about filesystems, including total size, space used, space available, and percentage of space used. Use `-h` option for human-readable output.

For example, `df -h` displays:

| Filesystem | Size | Used | Available | Use% | Mounted on |
| --- | --- | --- | --- | --- | --- |
| /dev/sda1 | 2.00T | 1.00T | 1.00T | 100% | / |
| /dev/sda2 | 2.00T | 1.00T | 1.00T | 100% | /boot |

Table shows:

* Filesystem: filesystem name.
* Size: total filesystem size.
* Used: space used on filesystem.
* Available: space available on filesystem.
* Use%: percentage of space used on filesystem.
* Mounted on: filesystem mount point.

## The du command

`du` command shows disk usage of a file or directory. Use `-h` option for human-readable output, and `-s` option to summarize results. For example, `du -sh .` shows the total size of the current directory.

To find the 10 largest directories, use:

```bash
du -x / | sort -nr | head -10
```

This scans the root directory (`/`), sorts results by size in descending order, and shows the top 10 results.

## Challenges

1. Show free space available on a specific filesystem, like the root filesystem (`/`).
2. Display percentage of space used for each mounted filesystem.
3. Show information about all filesystems, including unmounted ones.
4. Check the size of the current directory.
5. Check the size of the `/home` directory.
6. Find the 10 largest directories in the system.
