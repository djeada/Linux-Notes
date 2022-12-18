## Introduction to Mounting and Unmounting on Linux

In Linux, you must mount file systems, disks, DVDs, and USB drives before you can access them. The mount and umount commands are used to mount and unmount file systems, respectively. This article provides an overview of how to use these commands and some common scenarios for mounting and unmounting file systems in Linux.

## Verifying That a Drive is Visible

Before attempting to mount a drive, it is important to verify that it is visible to the system. You can use the `fdisk -l` command to list all accessible disks, including both mounted and unmounted drives.

## Mounting File Systems

To mount a file system, use the `mount -t file_system_type source_location target_location` command, where `file_system_type` is the type of file system being mounted (e.g. ext4), `source_location` is the location of the file system (e.g. /dev/sdb1), and `target_location` is the directory where the file system will be mounted (e.g. /mnt/shared).

If you are unsure of the file system type, you can use the `mount -a source_location target_location` command, which will automatically detect the file system type. For example:

```
mount -a /dev/sdb1 /mnt/shared
```

To view all currently mounted file systems, you can use the mount command without any parameters. The same information can also be found in the `/etc/mtab` file, which can be viewed using the `cat /etc/mtab` command.

## Mounting at System Startup

By default, mounted disks will be lost when the system is rebooted. To remount a file system at system startup, you can add an entry to the `/etc/fstab` file. Each entry should contain the device, mount point, file system type, options, dump frequency, and fsck order, separated by tabs or spaces. For example:

```
#device        mountpoint     fstype    options     dump   fsck
/dev/sdb1      /mnt/shared    ext4      defaults    0      1
```

To verify that the fstab settings have been properly applied, you can use the `mount -a` command.

## Mounting an ISO Image

You may want to mount an ISO image as if it were a DVD on your optical drive. To do this, use the `mount -o loop filename.iso mount_point` command, where `filename.iso` is the name of the ISO image and `mount_point` is the directory where it will be mounted. For example:

```
mount -o loop myfiles.iso /mnt/iso
```

<h1>Verify that the drive is visible</h1>
Use the following command to list all accessible disks, including mounted and unmounted drives: 

```bash
fdisk -l
```

## Unmounting File Systems

To unmount a file system, use the umount source_location command. If the source location is currently in use, the command will fail. To unmount the file system, you can try killing the process using the lsof command to determine the process ID, or you can use the `umount -l source_location` command to perform a "lazy" unmount.

For example, to determine the process ID of a process that is preventing you from unmounting a file system, you can use the following command:

```
lsof | grep target_location
```

If a process with the ID 3528 appears, then you can use the following command to kill it:

```
kill 3528
```

Then, you can retry the `unmount` command. If nothing else works, you can use the `umount -l source_location` command to perform a "lazy" unmount. This will unmount the file system as soon as it is no longer in use, but it may result in data loss or corruption if processes are still accessing the file system.

It is important to properly unmount file systems to ensure that all data is properly saved and to prevent data loss or corruption. Be cautious when using the umount command, and make sure to use it only when it is safe to do so.

## Challenges

1. What command is used to list all accessible disks, including both mounted and unmounted drives, on a Linux system?
1. How do you mount a file system in Linux? What are the required parameters for the mount command?
1. How do you view all currently mounted file systems in Linux?
1. How do you mount a file system at system startup in Linux? What file do you need to modify, and what information should be included in each entry?
1. How do you mount an ISO image as if it were a DVD on your optical drive in Linux?
1. What command is used to unmount a file system in Linux? What should you do if the source location is currently in use?
1. What is a "lazy" unmount, and when might it be used? What are the potential consequences of using a lazy unmount?
1. What is the importance of properly unmounting file systems in Linux? What can happen if you do not properly unmount a file system?
