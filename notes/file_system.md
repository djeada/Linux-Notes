## Types of files stored in UNIX filesystem
  
One way to classify the files is by their purpose: 

1. Ordinary files: Text, data, and code information can all be found in ordinary files. 
  Files and folders can not be contained within other files or directories. 
  Unlike other operating systems, UNIX filenames do not have a name and an extension .

1. Directories: In Linux, files are arranged into directories (analogous to folders in Windows). 
  The root directory is simply referred to as `/`.
  Users' files are stored in their home folders, which are located in `/home/.` For instance, `/home/adam/.`

1. Devices: To provide applications simple access to hardware devices, UNIX permits them to be utilized in the same manner that regular files are. In UNIX, there are two sorts of devices: block-oriented devices that transport data in blocks (e.g., hard drives) and character-oriented devices that send data byte by byte (e.g. modems and terminals).

1. Links: A link is a reference to another file. There are two kinds of links: hard links and soft links. A hard link to a file is indistinguishable from the file itself. A soft link (also known as a symbolic link) is an indirect pointer or shortcut to a file. A soft link is created as a directory file entry with a pathname.

Another approach is to categorize them according to how they are stored in the file system: 

* Files that are directly placed in the file system.
* Virtual files that are not files but rather interfaces to other programs or kernel itself (/proc and /sys).
* Files from a remote NFS server that has been mounted on the file system. 

### Special directory names 

* “./” is a reference to the current directory;
* “../” is a reference  to the directory one level above the current directory; 
* “~/” is a reference  to your home directory.

### File names 
Unlike Windows, Linux distinguishes between upper and lower case letters in file names.
That is, the file names "Test," "TEST," and "test" all refer to different files. 

### Hidden files 
Hidden files have filenames that begin with “.” (period). 
These are generally system files that do not appear when you list the contents of a directory. 

### Permissions
Files are given `permissions` that specify who has access to them and what kind of access they have.
The three most basic forms of access are read, write, and execute. 
You can read the content of a file (e.g., make your own copy) if you have read access. 
You can remove, edit, or replace files with write access.
Execute access is necessary to run programs or access the contents of folders.

## UNIX Directory Structure

Everything in Linux is located in the root directory. Even if you have many hard disks or SSDs, their storage will be stacked under the root directory. 

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
| `/var` | variable data specfic to the system |
| `/root` | root user home directory |
| `/boot` | files needed for the boot up process |
| `/media` and `/mnt` | other mounted devices (like USB stick) |
| `/proc` | ino about every process on the system |

## File system types

### Second Extended File System (ext2)

* Maximum file size: 2 TB
* Maximum volume size: 4 TB
* File name size: 255 characters
* Supports: POSIX permissions and compression
* If a system shuts down unexpectedly, it takes an EXTREMELY LONG TIME to recover.

### Second Extended File System (ext3)

* Does everything ext2 does (you can upgrade 2 to 3).
* It comes with a journal (before making a transaction it will describe it in the journal and mark it as incomplete). It is a lifesaver.
* Security over slightly slower I/O actions.

### Fourth Extended File System (ext4)

* Maximum file size: 16 TB
* Maximum volume size: 1 exabyte
* Maximum number of files: 4 billion
* Maximum file name length: 255 characters
* Uses journaling.

### Reiser File System 

* Maximum file size: 8 TB
* Maximum volume size: 16 TB
* Faster than ext2 and ext3.
* Uses journaling.

### XFS

* Older.
* Used to be the only option for big drives.
* Still used by CentOS.

### DOS (windows world)

* ntfs
* vfat
* fat32
* linux can read and write to those file systems

## Creating a file system
Let's say `/dev/sdb` is a disk  with defined partitions but no data stored on it.

To check the disk info and partitions, use:

```bash
fdisk -l /dev/sdb 
```

Assume the following partition exists on `/dev/sdb`: `/dev/sdb1`, `/dev/sdb2`, `/dev/sdb3`.

To create ext4 file system on each of them, use:

```bash
mkfs -t ext4 /dev/sdb1
mkfs -t ext4 /dev/sdb2
mkfs -t ext4 /dev/sdb3
```

## Challenges

1. Does the file `/bin/echo` exist on your system? If so, how does it relate to the `echo` command?
1. Use `/dev/random` or `/dev/urandom` to create a file with 100 lines of random chars.
1. Can you explain the purpose of the `/bin` and `/sbin` directories? 
1. What is the difference between character and block device drivers in UNIX? Can we use `ls`  to determine which group the device belongs to?
1. Can you deduce your CPU's model from the contents of `/proc/cpuinfo`? 
1. What hidden files may be found in the `/root` directory? 
