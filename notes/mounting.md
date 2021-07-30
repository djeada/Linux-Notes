On Linux you have to mount partitions, file systems, dvds, usb drives before you can use them.

<h2>Mount command</h2>

The procedure for utilizing the mount command is quite simple.

When no parameters are specified, mount will display all mounted file systems:

```bash
mount
```

The same information may be found in /etc/mtab:

```bash
cat /etc/mtab
```

<h2>Mounting a file system</h2>

To mount a file system, use the following syntax:

mount -t file_system_type source_location target_location

The file system type must be the same as what is specified in source location.

```bash
mount -t ext4 /dev/sdb1 /mnt/shared
```

Option -a will find the file system type for you!

mount -a source_location target_location

```bash
mount -a /dev/sdb1 /mnt/shared
```

<h2> Mounting an iso image </h2>

Why? You may then use it as if it were a DVD on your optical drive.

mount -o loop filename.iso mount_point

```bash
mount -o loop myfiles.iso /mnt/iso
```

<h2>Unmounting</h2>

To unmount, use the following syntax:

```bash
unmount source_location
```

When the source location is busy (someone is using it), the command will fail!

