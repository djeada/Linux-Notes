## Mounting and Unmounting

Mounting is the process of making a file system, disk, DVD, or USB drive accessible to the operating system so that you can read and write data on it. In Linux, you need to mount these devices before using them.

Unmounting is the process of disconnecting a mounted file system from the operating system. This should be done before physically disconnecting a device to prevent data loss or corruption.

Use the `mount` and `umount` commands to mount and unmount file systems.

```
+-------------------------------------+        +--------------------------------------+
|          Operating System           |        |            File System              |
|          (Linux Environment)        |        | (e.g., Disk, DVD, USB Drive)        |
+-------------------------------------+        +--------------------------------------+
        | ^                                         | ^
        | | Mounting                                | | Data Access
        | | (make accessible)                       | | (read/write)
        | |                                         | |
        v |                                         v |
+-------------------------------------+        +--------------------------------------+
|            mount command            | <----> |           Mounted State             |
+-------------------------------------+        +--------------------------------------+
        | ^                                         | ^
        | | Unmounting                              | | Data Protection
        | | (disconnect safely)                     | | (prevent loss/corruption)
        | |                                         | |
        v |                                         v |
+-------------------------------------+        +--------------------------------------+
|           umount command            | <----> |          Unmounted State            |
+-------------------------------------+        +--------------------------------------+
```
 
## Verifying Drive Visibility

When working with different drives on a Linux-based system, it's important to verify whether these drives are visible to the operating system. Checking drive visibility helps confirm that the drive is properly connected and recognized by the system, which is a prerequisite for actions like mounting or partitioning.

Drive visibility indicates that the system can interact with the drive, access its metadata, and perform operations such as reading or writing data.

One common method to check drive visibility is by using the `fdisk` command, which provides various disk management tasks. When used with the `-l` option, `fdisk` lists all the accessible disk drives, regardless of their mount status. 

Here is the command:

```bash
sudo fdisk -l
```

You need superuser or root privileges to execute this command, hence the sudo prefix.

The output will display a list of all the disk drives, their partitions, and relevant details like size, type, and partition scheme. Drives are usually named in the format of `/dev/sdX` or `/dev/nvmeXnY`, where X and Y are letters or numbers corresponding to the drive and partition number respectively.

If the drive you're interested in appears in this list, it means it's visible to the operating system and ready for further operations like mounting.

However, keep in mind that visibility doesn't necessarily mean the drive is in a healthy state. Tools like `smartctl` from the smartmontools package can be used for checking drive health and SMART (Self-Monitoring, Analysis, and Reporting Technology) status.

## Mounting File Systems

Mounting a file system is an essential process in Linux, making the file system or a storage device (like a hard disk, CD-ROM, or USB drive) accessible for reading and writing data. Once a file system is mounted, it's integrated into the system's directory tree and can be accessed from the assigned mount point (a directory on your system).

```
 File System /dev/sdb1
         |
         |  mount /dev/sdb1 /mnt/mydrive
         |
         v
 +-------------------------------+
 |  Linux System's Directory Tree |
 |                               |
 |   /                           |
 |   ├── home                    |
 |   ├── var                     |
 |   ├── etc                     |
 |   ├── ...                     |
 |   ├── mnt                     |
 |   │   ├── ...                 |
 |   │   ├── mydrive  <----------|------ Mounted here
 |   │   ├── ...                 |
 |   ├── ...                     |
 +-------------------------------+
```

### How to Mount a File System

The basic syntax for mounting a file system in Linux is as follows:

```bash
mount -t file_system_type source_location target_location
```

- `file_system_type`: This is the type of file system you are trying to mount. Common types include ext2, ext3, ext4 (standard Linux file systems), FAT32 (common for USB drives), NTFS (Windows file systems), and others.

- `source_location`: This is the identifier of the device you want to mount, typically in the form of /dev/sdXN or /dev/nvmeXnY where X and Y are letters or numbers identifying the drive and partition number, respectively.

- `target_location`: This is the mount point, i.e., the directory where you want the file system to be accessible. For instance, /mnt/shared.

For example, to mount an ext4 file system located at `/dev/sdb1` to the `/mnt/shared` directory, you would use:

```bash
mount -t ext4 /dev/sdb1 /mnt/shared
```

If you are unsure of the file system type, you can omit the -t option and Linux will attempt to determine the type automatically:

```bash
mount /dev/sdb1 /mnt/shared
```

### Viewing All Mounted File Systems

To see a list of all currently mounted file systems, you can use the mount command with no parameters. This command will output information about all mounted file systems including their type, mount point, and mount options:

```bash
mount
```

Example Output:

```
/dev/sda1 on / type ext4 (rw,relatime,data=ordered)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
/dev/sdb1 on /mnt/external type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,errors=remount-ro)
```

Output Explanation:

- `/dev/sda1`, `tmpfs`, `/dev/sdb1` - These are the device names or identifiers.
- `/`, `/dev/shm`, `/mnt/external` - These are the directories where the file systems are mounted.
- `ext4`, `tmpfs`, `vfat` - This indicates the type of file system.
- `(rw,relatime,data=ordered)`, etc. - These are options used while mounting, like read-write mode, permissions, etc.

### Visualization of Mounting

**Initial Filesystem Structure:**

```
/
├── bin
├── etc
├── home
│   ├── alice
│   └── bob
├── usr
└── var
```

**Mounting a New Device at `/mnt/backup`:**

1. **Before Mounting:**

```
/
├── bin
├── etc
├── home
│   ├── alice
│   └── bob
├── mnt
│   └── backup (empty directory)
├── usr
└── var
```

2. **Mount Command:**

```bash
sudo mount /dev/sdb1 /mnt/backup
```

- **`/dev/sdb1`**: Device file representing the storage device.
- **`/mnt/backup`**: Mount point.

3. **After Mounting:**

```
/
├── bin
├── etc
├── home
│   ├── alice
│   └── bob
├── mnt
│   └── backup
│       ├── documents
│       ├── photos
│       └── music
├── usr
└── var
```

**Explanation:**

- **Mount Point `/mnt/backup`**: The contents of `/dev/sdb1` are now accessible under `/mnt/backup`.
- **Accessing Files**: Users can navigate to `/mnt/backup` and interact with files as part of the directory tree.

### The Mounting Process Flow

```
+-----------------------+
|     Storage Device    |
|    (/dev/sdb1)        |
+-----------+-----------+
            |
            | Mount Command
            v
+-----------------------+
|   Kernel's VFS Layer  |
|  (Virtual Filesystem) |
+-----------+-----------+
            |
            | Mounts the Filesystem
            v
+----------------------------+
|   Directory Tree           |
| (Mount Point: /mnt/backup) |
+----------------------------+
```

### Mounting Types

- **Manual Mounting**: Using the `mount` command.
- **Automatic Mounting**:
  - **At Boot**: Specified in `/etc/fstab`.
  - **On Demand**: Using automount daemons.

### `/etc/fstab` File

Defines filesystems to be mounted at boot time.

**Sample Entry:**

```
/dev/sdb1   /mnt/backup   ext4    defaults    0   2
```

- **Fields Explained**:
  1. **Device**: `/dev/sdb1`
  2. **Mount Point**: `/mnt/backup`
  3. **Filesystem Type**: `ext4`
  4. **Options**: `defaults`
  5. **Dump**: `0` (backup utility dump)
  6. **Pass**: `2` (fsck order)



## Unmounting File Systems

Unmounting a file system is the process of detaching it from the system's directory tree. Once a file system is unmounted, files cannot be accessed from that file system until it is mounted again.

This is an essential process because it ensures that all pending read/write operations are completed and all data cached in memory is written to disk. This helps prevent potential data loss or corruption.

### How to Unmount a File System

To unmount a file system, you use the `umount` command followed by the mount point or the device name:

```bash
umount /mnt/shared
```

In this command, /mnt/shared is the mount point of the file system. This command will disconnect the file system from the directory tree.

### Troubleshooting Unmounting Issues

Sometimes, you may encounter an error message indicating that the device is busy when you try to unmount a file system. This typically means some processes are still using the file system, preventing it from being unmounted.

To find out which processes are using the file system, you can use the `lsof` command (short for "list of open files") and filter the results with grep:

```bash
lsof | grep /mnt/shared
```

This command will list all processes currently accessing /mnt/shared. If a process appears with, for example, the ID 3528, you can stop this process with the kill command:

```bash
kill 3528
```

Then, you can retry the umount command.

### Lazy Unmounting

If you still can't unmount the file system, you can use a "lazy" unmount with the -l option. This tells the system to unmount the file system as soon as it is not busy:

```bash
umount -l /mnt/shared
```

This is a powerful option and should be used with caution. When used, it might appear as if files have been unmounted, but in reality, their unmounting is only deferred until they are no longer in use.

## Mounting an ISO Image

An ISO image is a disk image of an optical disc. In other words, it is a file that contains the exact contents, including the file system, of an optical disc such as a CD, DVD, or Blu-ray Disc. ISO images are often used for archival purposes, distribution of media, or for creating a backup copy of a disc.

In Linux, you can mount an ISO image to make its contents accessible just as you would with a physical disc.

```
  ISO File (file.iso)
         |
         |  mount -o loop file.iso /mnt/iso
         |
         v
+-------------------------------+
|  Linux System's Directory Tree |
|                               |
|   /                           |
|   ├── home                    |
|   ├── var                     |
|   ├── etc                     |
|   ├── ...                     |
|   ├── mnt                     |
|   │   ├── ...                 |
|   │   ├── iso  <--------------|------ Mounted here
|   │   ├── ...                 |
|   ├── ...                     |
+-------------------------------+
```

### How to Mount an ISO Image

The process of mounting an ISO image is a bit different from mounting physical devices. The `loop` device is a pseudo-device that makes a file accessible as a block device, and it's used to mount files like ISO images that contain a file system within them.

Here's the general command for mounting an ISO image:

```bash
mount -o loop file.iso /mnt/iso
```

In this command:

- `-o loop` instructs the mount command to use the loop device, making the ISO file accessible as a block device.
- `file.iso` is the ISO file you want to mount. Replace this with your actual file name.
- `/mnt/iso` is the directory where you want the ISO contents to be accessible (known as the mount point). You need to create this directory if it doesn't exist. Replace /mnt/iso with your actual directory.

For example, to mount an ISO image called image.iso in the current directory to the mount point /mnt/iso, you would use:

```bash
mount -o loop image.iso /mnt/iso
```

### Checking the Contents of the ISO Image

After the ISO image is mounted, you can navigate to the mount point and inspect its contents just like a regular directory. For instance:

```bash
cd /mnt/iso
ls
```

This command will display the list of files and directories stored in the ISO image.

Remember to unmount the ISO image once you're done with it using the umount command followed by the mount point:

```bash
umount /mnt/iso
```

## Challenges

I. Recognize Devices

- Plug a USB drive into your system.
- Use the `fdisk -l` command to recognize the device name of the USB drive.

II. Manual Mounting

- Create a new directory under `/mnt`.
- Mount your USB drive to this new directory.

III. Accessing Mounted Files

- Navigate to the mount point of your USB drive.
- Create, read, and delete a file in this directory.

IV. Unmounting

- Unmount the USB drive from the directory you previously mounted it to.
- Confirm that the device has been unmounted successfully.

V. Create a Virtual Disk File

- Create a new file in your home directory using the `dd` command. This file will simulate a new disk drive.
- Format this file with an `ext4` filesystem using the `mkfs.ext4` command.
- Mount this virtual disk file to a directory in your system.
