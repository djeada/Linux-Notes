<h1>Verify that the drive is visible</h1>
Use the following command to list all accessible disks, including mounted and unmounted drives: 

```bash
fdisk -l
```

<h1>Mount command</h1>

On Linux you have to mount partitions, file systems, dvds, usb drives before you can use them.
The procedure for utilizing the mount command is quite simple.

When no parameters are specified, mount will display all mounted file systems:

```bash
mount
```

The same information may be found in /etc/mtab:

```bash
cat /etc/mtab
```

<h1>Mounting a file system</h1>

To mount a file system, use the following commands:

```bash
mount -t file_system_type source_location target_location
```

The file system type must be the same as what is specified in source location.

```bash
mount -t ext4 /dev/sdb1 /mnt/shared
```

Option -a will find the file system type for you!

mount -a source_location target_location

```bash
mount -a /dev/sdb1 /mnt/shared
```

Now drive is available for use under /mnt/shared directory.

<h1>Mounting at system startup</h1>

Mounted disks will be lost when the system is rebooted. Add the following line to the /etc/fstab file to remount on system startup: 
 
```
#device        mountpoint     fstype    options     dump   fsck
/dev/sdb1      /mnt/shared    ext4      defaults    0      1
```

Be cautious while using this file, since it has the potential to cause your system to fail to boot!

Verify that the fstab settings were appropriately added by using the following command: 

```bash
mount -a
```

<h1>Mounting an iso image </h1>

Why? You may then use it as if it were a DVD on your optical drive.

mount -o loop filename.iso mount_point

```bash
mount -o loop myfiles.iso /mnt/iso
```

<h1>Unmounting</h1>

To unmount, use the following commands:

```bash
unmount source_location
```

When the source location is busy (someone is using it), the command will fail!

To minimize damage, find the busy process, kill it, and then unmount the drive. We may use lsof to determine the ids of processes that are preventing us from unmounting the drive: 

```bash
lsof | grep target_location
```

If a process with the id 3528 appears, then use: 

```bash
kill 3528
```

Retry unmounting. If nothing else works, the last resort is lazy unmounting:

```bash
umount -l target_location
```
