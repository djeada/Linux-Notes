## Types of files in a UNIX filesystem

UNIX systems organize files in a hierarchical structure. Files can be classified by purpose, storage, or visibility.

### Purpose-based classification

1. Ordinary files: Contain text, data, or code. They can't hold other files or directories.
2. Directories: Like folders, used to organize files. Root directory (`/`) is the top-level directory. Users' files are in their home directories (e.g., `/home/adam/`).
3. Devices: Represent hardware devices as files. Block-oriented devices (e.g., hard drives) transfer data in blocks, while character-oriented devices (e.g., modems) transfer data byte by byte.
4. Links: References to other files. Hard links are indistinguishable from the original file, while soft links (symbolic links) are indirect pointers to a file.

### Storage-based classification

1. Regular files: Contain text, data, or code and are stored directly in the file system.
2. Virtual files: Interfaces to other programs or the kernel (e.g., `/proc` and `/sys`).
3. Remote files: Files from a remote Network File System (NFS) server, accessible as if stored locally.

### Visibility-based classification

1. Visible files: Seen when listing a directory's contents.
2. Hidden files: Not seen when listing a directory's contents. They start with a period (`.`) and store configuration or system files.

## File names 
Linux is case-sensitive, treating "Test," "TEST," and "test" as different files.

## Directory structure

Linux organizes everything within the root directory (`/`). Important directories include:

| Directory | Description |
| --- | --- |
| `/bin` | Low-level system utilities |
| `/usr/bin` | System utilities for normal users |
| `/sbin` | System utilities for superusers |
| `/lib` | Low-level system utility program libraries |
| `/usr/lib` | Library programs for higher-level user programs |
| `/tmp` | Temporary files storage (removed after 10 days) |
| `/home` | Home directories for users |
| `/etc` | Configuration files |
| `/dev` | Hardware device info |
| `/var` | Variable data specific to the system |
| `/root` | Root user home directory |
| `/boot` | Boot up process files |
| `/media` and `/mnt` | Mounted devices |

## Special directory names 

There are several special directory names that have specific meaning in a UNIX file system:

1. `./` refers to the current directory.
2. `../` refers to the directory above the current directory.
3. `~/` refers to the user's home directory.

## File system types

A file system is a way of organizing and storing data on a storage device, such as a hard drive or USB drive.

There are several types of file systems that are used on Linux systems:

1. `ext2`: Simple and efficient but lacks advanced features like journaling or encryption.
2. `ext3`: Adds support for journaling.
3. `ext4`: Supports larger file sizes and file systems, improved performance and reliability.
4. `JFS`: Designed for large file systems with advanced features like journaling.
5. `NFS`: Access remote server files over a network connection.
6. `VFS`: A layer between OS and file system for handling different file systems.
7. `FAT`: Common on USB drives and removable storage devices.
8. `NTFS`: Used on Windows systems, can be accessed on Linux but not native.
9. `ReiserFS`: Good performance and reliability, often used on servers.

## Creating a File System
To create a new file system on a storage device in Linux, follow these steps:

1. **Determine the device**: Use `lsblk` to list all available block devices and their names. This will help you identify the device you want to format.

2. **Unmount the device (if mounted)**: Before creating a new file system, you must unmount the device if it's already mounted. Use `umount` followed by the device name (e.g. `umount /dev/sda1`).

3. **Create the file system**: Use `mkfs` followed by the type and device name (e.g. `mkfs.ext4 /dev/sda1`). There are different file system types available such as `ext4`, `ext3`, `ext2`, `xfs`, and `btrfs`. The choice depends on your needs and preferences. `ext4` is the most common and recommended for general use.

4. **Mount the new file system**: Use `mount` followed by the device name and mount point (e.g. `mount /dev/sda1 /mnt/new_fs`). Choose an appropriate mount point or create a new directory for the mount point if needed.

Example with a disk `/dev/sdb` and partitions `/dev/sdb1`, `/dev/sdb2`, `/dev/sdb3`:

- Check disk information and partitions: `fdisk -l /dev/sdb`
- Create `ext4` file system on each partition:

```
mkfs -t ext4 /dev/sdb1
mkfs -t ext4 /dev/sdb2
mkfs -t ext4 /dev/sdb3
```

Remember that you can replace `ext4` with any other supported file system type according to your needs. Always make sure to backup any important data before creating a new file system, as this process will erase the data on the target device.

## Challenges

1. What is the root directory in Linux?
2. How does `/bin/echo` relate to the `echo` command?
3. Create a file with 100 lines of random characters using `/dev/random` or `/dev/urandom`.
4. Explain the purpose of `/bin` and `/sbin` directories.
5. What is the purpose of `/usr/bin` in a Linux system?
6. What is the difference between character and block device drivers in UNIX? Can `ls` determine the device
7. Can you deduce your CPU's model from the contents of `/proc/cpuinfo`? 
8. What hidden files may be found in the `/root` directory? 
9. What command can you use to create a new file system in Linux?
10. How do you check the disk information and partitions on a device in Linux?
11. How do you mount a file system in Linux?
