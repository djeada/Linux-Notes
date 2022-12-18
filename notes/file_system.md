## Types of files in a UNIX filesystem

UNIX systems use a hierarchical filesystem to store and organize files. A file can be classified based on its purpose or how it is stored in the filesystem.

### Classification based on purpose

1. Ordinary files: These contain text, data, and code information. They cannot contain other files or directories. Unlike other operating systems, UNIX filenames do not have a name and an extension.

1. Directories: In Linux, files are organized into directories (similar to folders in Windows). The root directory is simply referred to as `/`. Users' files are stored in their home directories, which are located in `/home/`. For example, `/home/adam/` is the home directory for the user adam.

1. Devices: UNIX allows hardware devices to be accessed like regular files to provide applications with easy access to hardware devices. In UNIX, there are two types of devices: block-oriented devices that transfer data in blocks (e.g., hard drives) and character-oriented devices that transmit data byte by byte (e.g., modems and terminals).

1. Links: A link is a reference to another file. There are two types of links: hard links and soft links. A hard link to a file is indistinguishable from the file itself. A soft link (also known as a symbolic link) is an indirect pointer or shortcut to a file. A soft link is created as a directory file entry with a pathname.

### Classification based on storage

Another way to classify files in a UNIX file system is based on how they are stored in the file system.

1. Regular files: These are files that are directly placed in the file system. They can contain text, data, or code information. They can not contain other files or directories within them.
1. Virtual files: These are not actual files, but rather interfaces to other programs or the kernel itself. Examples of virtual files include `/proc` and `/sys`.
1. Remote files: These are files from a remote Network File System (NFS) server that has been mounted on the file system. The user can access these files as if they were stored locally on the system.

### Classification based on visibility

Files can also be classified based on their visibility in the file system. There are three main categories:

1. Visible files: These are the files that are normally visible when you list the contents of a directory.
1. Hidden files: These are files that are not normally visible when you list the contents of a directory. These files have a period (`.`) as the first character in their filename, and are usually used for storing configuration or system files.

## File names 
Unlike Windows, Linux distinguishes between upper and lower case letters in file names.
That is, the file names "Test," "TEST," and "test" all refer to different files. 

## Directory structure

In Linux, everything is organized within the root directory (/). Even if you have multiple hard drives or SSDs, their storage will be contained within the root directory. The following is a list of some of the important directories you may encounter in a Linux system:

| Directory | Description |
| --- | --- |
| `/` | root directory |
| `/bin` | low-level system utilities (like `bash`, `cat` or `ls`) |
| `/usr/bin` | system utilities for normal users |
| `/sbin` | system utilities for superusers |
| `/lib` | low-level system utility program libraries |
| `/usr/lib` | library programs for higher-level user programs |
| `/tmp` | storage for temporary files (removed after 10 days) |
| `/home` | Each user's home directory has personal file space. Each directory is named after the user's login. |
| `/etc` | configuration files for programs and packages |
| `/dev` | info about hardware devices (disks, webcams, keyboards etc.) |
| `/var` | variable data specfic to the system, files that are expected to grow (like info about crashed processes). |
| `/root` | root user home directory |
| `/boot` | files needed for the boot up process |
| `/media` and `/mnt` | other mounted devices (like USB stick) |
| `/proc` | ino about every process on the system |

## Special directory names 

There are several special directory names that have specific meaning in a UNIX file system:

1. `./` refers to the current directory
1. `../` refers to the directory one level above the current directory
1. `~/` refers to the user's home directory

## File system types

A file system is a way of organizing and storing data on a storage device, such as a hard drive or USB drive.

There are several types of file systems that are used on Linux systems:

1. Second Extended File System (`ext2`): This is the most widely used file system on Linux systems. It is simple and efficient, but does not support advanced features such as journaling or encryption.
1. Third Extended File System (`ext3`): This file system is an improvement on the ext2 file system, adding support for journaling. This means that the file system keeps track of all changes made to the file system, which can help to recover the file system in the event of a crash.
1. Fourth Extended File System (`ext4`): This file system is an improvement on the ext3 file system, adding support for larger file sizes and larger file systems. It also has improved performance and reliability.
1. Journaling File System (`JFS`): This file system was developed by IBM and is designed for large file systems. It has a number of advanced features, including journaling, which helps to improve the reliability of the file system.
1.  Network File System (`NFS`): This file system allows a Linux system to access files on a remote server over a network connection. It is commonly used to share files between systems on a local network.
1. Virtual File System (`VFS`): This is not a file system in the traditional sense, but rather a layer that sits between the operating system and the file system. It allows different file systems to be used by the operating system, regardless of the underlying hardware.
1. File Allocation Table (`FAT`): This file system is commonly used on USB drives and other removable storage devices. It is a simple file system that is supported by most operating systems, including Linux.
1. New Technology File System (`NTFS`): This file system is commonly used on Windows systems. It can be accessed and used on Linux systems, but it is not a native file system.
1.  `ResiserFS`: This file system is designed for use on large file systems, and is known for its good performance and reliability. It is often used on servers and other systems with large amounts of data.

## Creating a File System
You can use the `mkfs` command to create a new file system on a storage device.

Let's say `/dev/sdb` is a disk with defined partitions but no data stored on it. To check the disk information and partitions, you can use the `fdisk` command:

```
fdisk -l /dev/sdb 
```

Assume the following partitions exist on `/dev/sdb`: `/dev/sdb1`, `/dev/sdb2`, `/dev/sdb3`. To create an `ext4` file system on each of them, use the `mkfs` command as follows:

```
mkfs -t ext4 /dev/sdb1
mkfs -t ext4 /dev/sdb2
mkfs -t ext4 /dev/sdb3
```

Here is an example of how to create a new ext4 file system on a device:

1. First, determine the device you want to create the file system on. You can use the lsblk command to list all available block devices and their corresponding device names.

2. Unmount the device, if it is already mounted. You can use the umount command to unmount a device, followed by the device name. For example: `umount /dev/sda1`

3. Use the mkfs command to create the file system. For example: `mkfs.ext4 /dev/sda1`

4. Mount the new file system. You can use the mount command to mount the file system, followed by the device name and the mount point (a directory where the file system will be accessible). For example: `mount /dev/sda1 /mnt/new_fs`

Note that there are many different file system options available in Linux, and the specific options and syntax for the mkfs command may vary depending on the file system you are creating. Consult the documentation for the specific file system you are using for more information.

## Challenges

1. What is the root directory in Linux?
1. Does the file `/bin/echo` exist on your system? If so, how does it relate to the `echo` command?
1. Use `/dev/random` or `/dev/urandom` to create a file with 100 lines of random chars.
1. Can you explain the purpose of the `/bin` and `/sbin` directories? 
1. What is the purpose of the `/usr/bin` directory in a Linux system?
1. What is the difference between character and block device drivers in UNIX? Can we use `ls`  to determine which group the device belongs to?
1. Can you deduce your CPU's model from the contents of `/proc/cpuinfo`? 
1. What hidden files may be found in the `/root` directory? 
1. What command can you use to create a new file system in Linux?
1. How do you check the disk information and partitions on a device in Linux?
1. How do you mount a file system in Linux?
