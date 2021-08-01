<h2>df</h2>
The <i>df</i> command shows hard drive partitions, optical drives and other storage devices are mounted, their file system type and disk usage.

```bash
df -hT
```

<h2>du</h2>
The <i>du</i> command is used to determine the amount of disk usage for a directory.

```bash
du -x / | sort -nr | head -20
```

<h2>lsof</h2>

The <i>lsof</i> command stands for List Of Open Files and provides information to determine which files are opened by which process.

```bash
sudo lsof | less
```

To check which process running on port 8080, use:

```bash
lsof -i :8080
```
