## Introduction to Mounting and Unmounting

In Linux, you need to mount file systems, disks, DVDs, and USB drives before using them. Use the `mount` and `umount` commands to mount and unmount file systems.

## Check if a Drive is Visible

Use the `fdisk -l` command to list all accessible disks, including mounted and unmounted drives.

## Mounting File Systems

To mount a file system, use this command: `mount -t file_system_type source_location target_location`.

If you don't know the file system type, use this command: `mount -a source_location target_location`.

To see all mounted file systems, use the `mount` command with no parameters.

## Mounting at Startup

To mount a file system at startup, add an entry to the `/etc/fstab` file.

Example:

```
#device        mountpoint     fstype    options     dump   fsck
/dev/sdb1      /mnt/shared    ext4      defaults    0      1
```

To check if fstab settings are correct, use the `mount -a` command.

## Mounting at System Startup

By default, mounted disks will be lost when the system is rebooted. To remount a file system at system startup, you can add an entry to the `/etc/fstab` file. Each entry should contain the device, mount point, file system type, options, dump frequency, and fsck order, separated by tabs or spaces. For example:

```
#device        mountpoint     fstype    options     dump   fsck
/dev/sdb1      /mnt/shared    ext4      defaults    0      1
```

To verify that the fstab settings have been properly applied, you can use the `mount -a` command.

## Mounting an ISO Image

Use this command to mount an ISO image: `mount -o loop filename.iso mount_point`.

## Unmounting File Systems
To unmount a file system, use the `umount source_location` command. If the source location is in use, try killing the process using `lsof | grep target_location` to find the process ID, or use the `umount -l source_location` command for a "lazy" unmount.

```
umount /mnt/shared
```

Find the process ID preventing unmounting:

```
lsof | grep /mnt/shared
```

If a process with ID 3528 appears, kill it:

```
kill 3528
```

Retry the `umount` command, or use a "lazy" unmount:

```
umount /mnt/shared
umount -l /mnt/shared
```

Be careful when using the umount command to prevent data loss or corruption.

## Challenges

1. Use the `fdisk -l` command to list all accessible disks.
2. Use the `mount -t file_system_type source_location target_location` command to mount a file system.
3. Use the `mount` command with no parameters to view mounted file systems.
4. Add an entry to the `/etc/fstab` file to mount a file system at startup.
5. Use the `mount -o loop filename.iso mount_point` command to mount an ISO image.
6. Use the `umount source_location` command to unmount a file system. Kill the process or use "lazy" unmount if the source location is in use.
7. A "lazy" unmount unmounts the file system when it's not in use but might cause data loss or corruption.
8. Properly unmounting file systems prevents data loss and corruption.
