## Disk usage
The `df` and `du` commands are useful tools for monitoring and managing disk usage on a Linux system.

## The df command

The `df` command displays information about the filesystems on a system, including the total size, the amount of space used, the amount of space available, and the percentage of space used. The `-h` option can be used to display the output in a human-readable format, making it easier to interpret the results.

For example, the command `df -h` would display the information shown in the table below.

| Filesystem | Size | Used | Available | Use% | Mounted on |
| --- | --- | --- | --- | --- | --- |
| /dev/sda1 | 2.00T | 1.00T | 1.00T | 100% | / |
| /dev/sda2 | 2.00T | 1.00T | 1.00T | 100% | /boot |
| /dev/sda3 | 2.00T | 1.00T | 1.00T | 100% | /home |
| /dev/sda4 | 2.00T | 1.00T | 1.00T | 100% | /mnt/backup |
| /dev/sda5 | 2.00T | 1.00T | 1.00T | 100% | /mnt/home |
| /dev/sda6 | 2.00T | 1.00T | 1.00T | 100% | /mnt/media |

The table shows the following information for each filesystem:

* Filesystem: the name of the filesystem.
* Size: the total size of the filesystem.
* Used: the amount of space used on the filesystem.
* Available: the amount of space available on the filesystem.
* Use%: the percentage of space used on the filesystem.
* Mounted on: the mount point for the filesystem.

## The du command

The `du` command, on the other hand, displays the disk usage of a specific file or directory. The `-h` option can be used to display the output in a human-readable format, and the `-s` option can be used to summarize the results. For example, the command `du -sh .`  will display the total size of the current directory in a human-readable format.

To find the 10 largest directories in the entire system, you can use the following command: 

```bash
du -x / | sort -nr | head -10
```

This will recursively scan the root directory (`/`) and sort the results in descending order based on size, then display the top 10 results.

## Challenges

1. Display the amount of free space available on a specific filesystem, such as the root filesystem (`/`).
1. Show the percentage of space used for each mounted filesystem.
1. Display information about all available filesystems, including those that are not currently mounted.
1. Check the size of the current directory.
1. Check the size of the `/home` directory.
1. Find the 10 largest directories in the entire system.
