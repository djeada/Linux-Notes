## Files and Filesystems

In Unix, files and filesystems are fundamental components of the operating system's structure. A file is a collection of data stored on disk, which can include anything from text documents and images to executable programs. Files are organized within directories in a hierarchical structure, allowing for efficient data management and retrieval.

A filesystem, on the other hand, is a method and data structure that the operating system uses to manage files on a disk or partition. It provides a way to store, retrieve, and organize files, supporting features like file permissions, links, and metadata. Common Unix filesystems include ext4, XFS, and Btrfs, each offering different capabilities and optimizations. Understanding these concepts is essential for managing data and system resources effectively in a Unix environment.

### Types of Files in a UNIX Filesystem

Unix and Unix-like systems, including Linux, organize files in a hierarchical structure called a filesystem. Files can be classified based on their purpose, storage method, and visibility.

#### Classification Based on Purpose

1. **Ordinary files** are the most common type, containing text, data, or program code. They cannot contain other files or directories.
2. **Directory files** function as folders to organize other files, with the root directory (`/`) being the top-level directory of the entire filesystem. Users' files are usually stored in their respective home directories, such as `/home/adam/`.
3. **Device files** represent hardware devices as if they were files. Block-oriented devices, like hard drives, transfer data in large blocks, whereas character-oriented devices, such as keyboards or modems, handle data one byte at a time.
4. **Link files** serve as references to other files. Hard links are essentially duplicates of the original file and behave identically, while soft links (or symbolic links) act as indirect pointers to a file or directory, similar to shortcuts in Windows.

The `file` command in Linux is a powerful tool that helps identify and classify these file types by analyzing their content and structure. Below are insights on how the `file` command interprets and reports on these various classifications:

| **Classification**  | **file Command Example**                   | **file Command Output Example**                                                   | **Explanation**                                                                 |
|---------------------|--------------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **Text Files**      | `file document.txt`                        | `document.txt: ASCII text`                                                        | The `file` command detects text encoding (e.g., ASCII, UTF-8) or identifies binary format for executables. |
| **Binary Files**    | `file program`                             | `program: ELF 64-bit LSB executable, x86-64, dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2` | Provides detailed information about binary files, including architecture and format. |
| **Directory Files** | `file /home/user`                          | `/home/user: directory`                                                           | Identified as a "directory". Contains pointers to other files and directories. |
| **Block Devices**   | `file /dev/sda`                            | `/dev/sda: block special`                                                         | The `file` command distinguishes between block devices (e.g., "block special") and character devices (e.g., "character special"). |
| **Character Devices** | `file /dev/tty`                          | `/dev/tty: character special`                                                     | Useful for identifying the type of device a file represents. |
| **Symbolic Links**  | `file /usr/bin/python`                     | `/usr/bin/python: symbolic link to /usr/bin/python3.8`                            | Symbolic links are reported with their target file or directory. |
| **Hard Links**      | `file hardlinkfile`                        | (Output identical to the original file)                                           | Hard links are identical to the original file in the `file` command output. |


#### Classification Based on Storage

1. **Regular files** contain text, data, or program code and are stored directly in the file system.
2. **Virtual files** provide an interface to other programs or the kernel. They do not contain traditional data but rather information about processes and system parameters, typically found in directories like `/proc` and `/sys`.
3. **Remote files** are stored on a remote Network File System (NFS) server. They can be accessed and manipulated as if they were stored locally.

The table below provides the most effective commands for identifying each type of file based on their specific attributes and locations:

| **Classification**  | **Command Example**                       | **Command Output Example**                                                                 | **Explanation**                                                                 |
|---------------------|-------------------------------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **Regular Files**   | `file document.txt`                       | `document.txt: ASCII text`                                                                 | The `file` command detects the type of content in regular files, such as text, binary, or executable.              |
| **Virtual Files**   | `stat /proc/cpuinfo`                      | `File: /proc/cpuinfo\nSize: 0\tBlocks: 0\tIO Block: 4096   regular file\nDevice: 0,5\tInode: 4026532255` | The `stat` command shows a typical file size of 0, located in `/proc` or `/sys`, indicating it's a virtual file. |
| **Remote Files**    | `df -T /mnt/nfs/remote_file`              | `Filesystem     Type 1K-blocks     Used Available Use% Mounted on\nnfsserver:/export  nfs    1024000   102400    924000   10% /mnt/nfs` | The `df -T` command displays the filesystem type as `nfs`, identifying it as a remote file on an NFS server.  |

#### Classification Based on Visibility

1. **Visible files** are displayed when you list the contents of a directory using commands like `ls`.
2. **Hidden files** are not displayed in a standard directory listing. They start with a period (`.`) and typically store configuration data or system files. They can be revealed using the `ls -a` command.

#### Note About File Names

Filenames are case-sensitive. This means the operating system treats "Test," "TEST," and "test" as different files. Also, most file types in Linux are determined by file content and not by the file extension, unlike systems like Windows.

#### Special Directory Names 

In a filesystem, certain directory names have special meanings that simplify navigation and file management:

1. The `./` notation refers to the current directory, meaning the directory where you are presently located. It is commonly used when executing a script or a program located in the current directory. For instance, if you have a script named `script.sh` in the current directory, you can run it using `./script.sh`. This tells the system to look for `script.sh` in the current directory.
2. The `../` notation refers to the parent directory, which is the directory one level up from the current directory in the filesystem hierarchy. It is useful for navigating upwards in the directory structure. For example, if you are in `/home/user/Documents` and you use `cd ../`, you will move up to `/home/user`.
3. The `~/` notation is a shorthand for the current user's home directory. The home directory is a personal space allocated to a user where personal files and settings are stored. For example, `~/Documents` would refer to the `Documents` directory within the home directory of the current user. This is especially useful for referencing files and directories in a user's home space without needing to specify the full path.

These notations provide a convenient way to navigate and manage files and directories efficiently in a command-line environment. They are particularly useful in scripting and automation tasks, where paths need to be specified dynamically or relative to the current context.

### Directory Structure

Linux organizes everything within a single directory hierarchy that starts with the root directory (`/`). 

```
/
├── bin
├── boot
├── dev
├── etc
│   ├── network
│   └── ssh
├── home
│   └── [user]
│       ├── Documents
│       ├── Downloads
│       ├── Music
│       ├── Pictures
│       ├── Videos
│       └── Desktop
├── lib
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── sbin
├── srv
├── sys
├── tmp
├── usr
│   ├── bin
│   ├── include
│   ├── lib
│   ├── local
│   └── share
└── var
    ├── cache
    ├── lib
    ├── local
    ├── lock
    ├── log
    └── tmp
```

Key directories within the Linux file system include:

| Directory       | Description |
| --------------- | ----------- |
| `/`             | The root directory: the starting point of the file system hierarchy, all other directories branch off from here. |
| `/bin`          | Essential low-level system utilities, executable by all users. |
| `/usr/bin`      | A place for user commands and applications typically used after the system boot process. |
| `/sbin`         | Contains system binaries crucial for booting, restoring, recovering, and/or repairing the system, supplementing the binaries in `/bin`. |
| `/lib`          | Contains shared libraries essential for the binaries found in `/bin` and `/sbin`. |
| `/usr/lib`      | Libraries necessary for `/usr/bin` binaries and applications. |
| `/tmp`          | A directory for storing temporary files, which are usually cleared at each reboot. |
| `/home`         | The home ground for personal directories of each user, where they can store their personal files. |
| `/etc`          | A repository for system-wide configuration files and scripts utilized during the boot process. |
| `/dev`          | A space hosting device nodes that correspond to hardware devices connected to the system. |
| `/var`          | Manages variable data such as system logs, mail and printer spool directories, alongside transient and temporary files. |
| `/root`         | Serves as the home directory for the root (superuser) account, distinct from the root directory (`/`). |
| `/boot`         | Stores files vital for the boot process, including the Linux kernel and the boot loader. |
| `/media` and `/mnt` | Serve as mount points for file systems and removable devices like CDs, USB drives, etc. |

### File System Types

A file system is a method of organizing, storing, and retrieving data on a storage device, like a hard drive, SSD, or USB drive. It manages the available space on the device, keeping track of which sectors belong to which files and directories.

Several types of file systems can be used on Linux systems, each designed with specific use-cases and features:

1. **`ext2` (Second Extended Filesystem)** is one of the first file systems specifically designed for Linux. It is simple and efficient but lacks advanced features like journaling or encryption.
2. **`ext3` (Third Extended Filesystem)** is an improved version of `ext2` with added support for journaling, which helps protect against data loss by keeping a log of changes that are yet to be committed to the file system.
3. **`ext4` (Fourth Extended Filesystem)** is currently the default Linux file system. It supports larger file sizes and file systems, has improved performance and reliability, and includes features like delayed allocation and journal checksumming.
4. **`JFS` (Journaled File System)** was originally developed by IBM for its own operating systems. It is designed to handle large file systems efficiently and features journaling.
5. **`NFS` (Network File System)** is not a file system for storing data on disk but rather a protocol that allows a system to access files over a network as if they were on its local hard drive.
6. **`VFS` (Virtual File System)** is a software layer in the kernel that provides a common interface to various file systems, allowing the operating system to access and manage different types of file systems uniformly.
7. **`FAT` (File Allocation Table)** is an old and simple file system common on removable storage devices and used by most operating systems, making it a good choice for interoperability.
8. **`NTFS` (New Technology File System)** is the standard file system of Windows NT and its later versions, such as Windows 2000, XP, Server 2003, Server 2008, Vista, and 7. It can be accessed on Linux but is not native, so it may lack full functionality.
9. **`ReiserFS` (Reiser File System)** is a general-purpose, journaled computer file system known for good performance and reliability. It efficiently handles a large number of small files and is often used on servers.
10. **`Btrfs` (B-tree File System)** is a copy-on-write (CoW) file system for Linux aimed at implementing advanced features with a focus on fault tolerance, repair, and easy administration. It provides features like snapshots, subvolumes, and built-in RAID.
11. **`XFS`** is a high-performance journaling file system created by Silicon Graphics, Inc. It is particularly proficient at parallel I/O, making it a good choice for applications that involve large files and require high-performance I/O.

| Category                     | ext2                       | ext3                        | ext4                        | JFS                        | NFS                        | VFS                        | FAT                        | NTFS                       | ReiserFS                   | Btrfs                      | XFS                        |
|------------------------------|----------------------------|-----------------------------|-----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|
| **Design Purpose**           | Simple Linux file system   | Improved ext2 with journaling | Default Linux file system  | Large file systems         | Network file access        | Common interface for FS    | Removable storage          | Windows file system        | Small files, servers       | Advanced Linux features    | High-performance, large files |
| **Journaling**               | No                         | Yes                         | Yes                         | Yes                        | N/A (protocol)             | N/A                        | No                         | Yes                        | Yes                        | Yes                        | Yes                        |
| **Performance**              | Efficient for small FS     | Better than ext2            | Better than ext3            | High efficiency            | Depends on network         | N/A                        | Simple, lower performance  | Good, Windows optimized    | Good for small files       | Good, advanced features    | Excellent, parallel I/O    |
| **Maximum File/FS Size**     | Smaller than ext3/4        | Larger than ext2            | Very large                  | Very large                 | N/A                        | N/A                        | Limited by design          | Very large                 | Large                      | Very large                 | Very large                 |
| **Suitability**              | Basic, older Linux systems | General Linux use           | Modern Linux systems        | Enterprise, large data     | Network environments       | Kernel-level operations    | Wide compatibility         | Windows environments       | Server use                 | Linux, advanced use        | Large file handling        |
| **Encryption Support**       | No                         | No                          | Yes (since 4.1)             | No                         | N/A                        | N/A                        | No                         | Yes                        | No                         | Yes                        | No                         |
| **Data Recovery**            | Harder                     | Easier than ext2            | Easier than ext3            | Good                       | Depends on implementation  | N/A                        | Simpler but riskier        | Good                       | Good                       | Very good                  | Good                       |
| **Use in Large Servers**     | Less common                | Common                      | Very common                 | Yes                        | Yes, for shared storage    | N/A                        | Less common                | Less common                | Yes                        | Yes                        | Yes                        |
| **Use in Personal Devices**  | Less common                | Less common                 | Common                      | Less common                | Less common                | N/A                        | Very common                | Common in Windows          | Less common                | Growing                    | Less common                |

### Creating a File System

Creating a new file system on a storage device in Linux is a fundamental task that involves several critical steps. This guide will walk you through the process, from identifying the device to mounting the new file system. Each step includes specific commands and detailed explanations to ensure a successful setup.

I. Identifying the Device

Before you can create a file system, you need to identify the correct storage device. This is crucial to avoid accidentally formatting the wrong device, which could lead to data loss. The `lsblk` command is used to list all available block devices, displaying useful information such as device names, sizes, types, and current mount points.

To list the devices, execute:

```bash
lsblk
```

Example Output:

```
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0  500G  0 disk 
├─sda1   8:1    0  250G  0 part /
├─sda2   8:2    0  249G  0 part /home
└─sda3   8:3    0    1G  0 part [SWAP]
sdb      8:16   0  100G  0 disk 
└─sdb1   8:17   0  100G  0 part /mnt/backup
```

In this output, `sda` and `sdb` are physical drives, while `sda1`, `sda2`, and `sda3` are partitions on `sda`. You need to select the correct device (`sdb` in this case) for creating a new file system.

II. Unmounting the Device (if applicable)

If the device you want to format is already mounted, it must be unmounted. This step is necessary because a file system cannot be modified while it is in use. To unmount a device, use the `umount` command followed by the device's mount point or name.

For instance, to unmount `/dev/sdb1`, you would use:

```bash
umount /mnt/backup
```

Alternatively, you can unmount by specifying the device:

```bash
umount /dev/sdb1
```

III. Creating the File System

With the device unmounted, you can now create the new file system. The `mkfs` (make file system) command is used for this purpose, followed by the type of file system you want to create and the device name. Common file system types include:

- `ext4`: A widely-used, robust file system suitable for most use cases.
- `ext3`: An older version of ext4, with journaling for improved reliability.
- `xfs`: Known for high performance, particularly with large files.
- `btrfs`: A newer file system with advanced features like snapshotting and self-healing.

To create an `ext4` file system on `/dev/sdb1`, the command is:

```bash
mkfs.ext4 /dev/sdb1
```

The command can take a few moments, depending on the size of the device. You may also use additional options with `mkfs` to specify features like block size, volume label, and more.

IV. Mounting the New File System

Once the file system is created, you need to mount it to make it accessible. The `mount` command is used for this purpose. You must specify both the device and the desired mount point, which can be an existing directory or a new one created for this purpose.

To mount the new file system on `/dev/sdb1` to `/mnt/new_fs`, you would do the following:

1. Create a new mount point if it doesn't exist:

```bash
mkdir -p /mnt/new_fs
```

2. Mount the device:

```bash
mount /dev/sdb1 /mnt/new_fs
```

After mounting, you can verify that the device is mounted correctly by using the `df -h` or `lsblk` commands, which will list mounted file systems along with their details.

#### Additional Considerations

- To ensure that the file system mounts automatically at boot, you need to add an entry in the `/etc/fstab` file. This file contains information about the file systems and their mount points.
- Regular maintenance of the file system, such as checking for errors with `fsck`, is recommended to ensure data integrity.
- Always backup important data before formatting any storage device to prevent accidental data loss.

### Challenges

1. Can you explain what the root directory is in Linux? How is it different from the root user's home directory?
2. In the context of the `echo` command in Linux, what is the relationship between `/bin/echo` and typing `echo` at the shell prompt?
3. Using `/dev/random` or `/dev/urandom`, how would you create a file filled with 100 lines of random characters? Can you write a shell command to do this?
4. What is the purpose of the `/bin` and `/sbin` directories in a Linux system? Can you list some of the files you would typically find in these directories and briefly describe what they do?
5. In a Linux system, what is the purpose of `/usr/bin`? What kind of files are typically stored in this directory and why?
6. Can you explain the difference between character and block device drivers in UNIX? Can the `ls` command be used to determine whether a device file represents a character device or a block device? If so, how?
7. By looking at the contents of `/proc/cpuinfo`, can you determine the model of your CPU? What command would you use to display this file's contents?
8. What hidden files might you expect to find in the `/root` directory? Why might these files be hidden?
9. What command can you use to create a new file system in Linux? What options does this command typically have, and how are they used?
10. How can you check disk information and partitions on a device in Linux? Please write down the command you would use and briefly explain its output.
11. What steps and commands would you use to mount a file system in Linux? Please provide an example command and explain what it does.
