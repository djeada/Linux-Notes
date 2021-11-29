

<h1>The df command</h1>
Monitoring disk usage is a common task for Linux systems administrators. The <code>df</code> command can be used to display disk usage information. You can use the <code>-h</code> option to display output in a human-readable format.

| Filesystem | Size | Used | Available | Use% | Mounted on |
| --- | --- | --- | --- | --- | --- |
| /dev/sda1 | 2.00T | 1.00T | 1.00T | 100% | / |
| /dev/sda2 | 2.00T | 1.00T | 1.00T | 100% | /boot |
| /dev/sda3 | 2.00T | 1.00T | 1.00T | 100% | /home |
| /dev/sda4 | 2.00T | 1.00T | 1.00T | 100% | /mnt/backup |
| /dev/sda5 | 2.00T | 1.00T | 1.00T | 100% | /mnt/home |
| /dev/sda6 | 2.00T | 1.00T | 1.00T | 100% | /mnt/media |

The <code>df</code> command can also be used to display the disk usage of a specific file or directory.

```bash
df -h /home
```

<h1>The du command</h1>

The <code>du</code> command displays the disk usage of a file or directory. The <code>-h</code> option can be used to display output in a human-readable format. The <code>-s</code> option can be used to summarize the results. 

```bash
du -sh .
```
To find the 10 largest directories in the entire system, use:

```bash
du -x / | sort -nr | head -10
```

<h1>Challenges</h1>

1. Display the disk usage of the current directory.
2. Display the disk usage of the /home directory.
3. Find the 10 largest directories in the entire system.
