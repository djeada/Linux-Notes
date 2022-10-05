## The df command

Monitoring disk usage is a common task for Linux systems administrators. The <code>df</code> command can be used to display disk usage information. You can use the <code>-h</code> option to display output in a human-readable format.

| Filesystem | Size | Used | Available | Use% | Mounted on |
| --- | --- | --- | --- | --- | --- |
| /dev/sda1 | 2.00T | 1.00T | 1.00T | 100% | / |
| /dev/sda2 | 2.00T | 1.00T | 1.00T | 100% | /boot |
| /dev/sda3 | 2.00T | 1.00T | 1.00T | 100% | /home |
| /dev/sda4 | 2.00T | 1.00T | 1.00T | 100% | /mnt/backup |
| /dev/sda5 | 2.00T | 1.00T | 1.00T | 100% | /mnt/home |
| /dev/sda6 | 2.00T | 1.00T | 1.00T | 100% | /mnt/media |

It basically comes down to showing the following information:

* How much disk space has already been used?
* How much of it is still free to use?
* What filesystems are currently mounted?

## The du command

The <code>du</code> command displays the disk usage of a file or directory. The <code>-h</code> option can be used to display output in a human-readable format. The <code>-s</code> option can be used to summarize the results. 

```bash
du -sh .
```
To find the 10 largest directories in the entire system, use:

```bash
du -x / | sort -nr | head -10
```

## Challenges

1. Display the size of the current directory.
2. Display the size of the `/home` directory.
3. Find the 10 largest directories in the entire system.
