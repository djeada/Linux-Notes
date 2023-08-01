## Mounting and Unmounting

Mounting is the process of making a file system, disk, DVD, or USB drive accessible to the operating system so that you can read and write data on it. In Linux, you need to mount these devices before using them.

Unmounting is the process of disconnecting a mounted file system from the operating system. This should be done before physically disconnecting a device to prevent data loss or corruption.

Use the `mount` and `umount` commands to mount and unmount file systems.
 
## Check if a Drive is Visible

We check if a drive is visible to make sure the operating system can see and interact with it. This helps confirm the drive is connected and ready for mounting.

Use the `fdisk -l` command to list all accessible disks, including mounted and unmounted drives.

## Mounting File Systems

To mount a file system, use this command: `mount -t file_system_type source_location target_location`.

* File systems: `ext2, `ext3`, `ext4`, `FAT32`, `NTFS`, and more.
* Source location: the device identifier (e.g., `/dev/sdb1`).
* Target location: the folder where the file system will be accessible (e.g., `/mnt/shared`).

If you don't know the file system type, use this command: `mount -a source_location target_location`.

To see all mounted file systems, use the `mount` command with no parameters.

## Mounting at Startup

`/etc/fstab` is a configuration file that lists file systems and their mount points. It helps the operating system know which file systems to mount automatically during startup.

To mount a file system at startup, add an entry to the `/etc/fstab` file.

Example:

```
#device        mountpoint     fstype    options     dump   fsck
/dev/sdb1      /mnt/shared    ext4      defaults    0      1
```

To check if fstab settings are correct, use the `mount -a` command.

## Mounting an ISO Image

An ISO image is a file that contains the contents of an optical disc, like a CD or DVD. 

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
