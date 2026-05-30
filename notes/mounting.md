## Mounting and Unmounting

In Linux, mounting is the process of making a filesystem available somewhere inside the main directory tree.

This can feel unusual if you come from Windows. In Windows, storage devices usually appear as separate drive letters, such as:

```text
C:\
D:\
E:\
```

Linux works differently. Linux has one main directory tree that starts at:

```text
/
```

Storage devices, partitions, USB drives, ISO files, and network shares are attached somewhere inside that tree.

For example, a USB drive might be mounted at:

```text
/mnt/external
```

or:

```text
/media/user/USB_DRIVE
```

Once mounted, the device looks like an ordinary directory. You can use commands such as `cd`, `ls`, `cp`, `mv`, and `rm` to work with its files.

### What Can Be Mounted

Many different things can be mounted in Linux.

Common examples include:

- hard disk partitions
- SSD partitions
- USB flash drives
- external hard drives
- CD/DVD/ISO images
- network shares
- special system filesystems

Network filesystems can also be mounted, such as:

```text
NFS        common on Unix/Linux networks
SMB/CIFS   common for Windows file shares
```

Linux also mounts special pseudo-filesystems that do not represent normal storage devices. These include:

```text
/proc
/sys
/dev
/run
```

These provide information about processes, hardware, devices, and runtime system state.

### Required and Optional Mounts

Some filesystems are required for the system to work.

For example:

```text
/       root filesystem
/proc   process and kernel information
/sys    hardware and kernel information
/dev    device files
```

These are usually mounted automatically during boot.

Other filesystems are optional. These include USB drives, extra partitions, external disks, ISO images, and network shares.

Optional filesystems may be mounted manually by the user or automatically by the desktop environment.

### Mounting on Desktop Linux

On desktop distributions such as Ubuntu, Fedora, or Linux Mint, removable devices are often mounted automatically.

For example, when you plug in a USB drive, the file manager may automatically mount it under something like:

```text
/media/username/USB_NAME
```

This is convenient for normal desktop use.

Manual mounting is still useful when:

- a device is not auto-mounted
- you are working on a server
- you are troubleshooting
- you want a custom mount point
- you are mounting an ISO file
- you are mounting a network share
- you need specific mount options

### Understanding Mounting

Mounting attaches a filesystem to a directory.

That directory is called a mount point.

Before mounting, the directory is just an ordinary directory. After mounting, the contents of the mounted filesystem appear there.

```text
Linux Directory Tree Before Mounting:

/
├── bin
├── etc
├── home
│   └── user
├── mnt
├── usr
└── var
```

Now suppose a USB drive partition is available as:

```text
/dev/sdb1
```

and we mount it at:

```text
/mnt/external
```

After mounting, the tree may look like this:

```text
Linux Directory Tree After Mounting /dev/sdb1 at /mnt/external:

/
├── bin
├── etc
├── home
│   └── user
├── mnt
│   └── external  <-- Mounted device /dev/sdb1
│       ├── documents
│       ├── photos
│       └── videos
├── usr
└── var
```

The files are physically stored on `/dev/sdb1`, but they are accessed through `/mnt/external`.

A simple way to remember this is:

```text
Device or filesystem + mount point = accessible files
```

### Important Mounting Idea

Mounting does not copy files into the mount point.

It simply makes the filesystem visible at that location.

For example:

```bash
sudo mount /dev/sdb1 /mnt/external
```

does not copy the USB drive into `/mnt/external`.

It attaches the filesystem on `/dev/sdb1` so that its contents can be accessed through `/mnt/external`.

### Mount Points

A mount point is a directory where a filesystem is attached.

Common mount point locations include:

```text
/mnt        traditional temporary mount location
/media      common location for removable media
/backup     custom mount point for backup drives
/data       custom mount point for data disks
```

For example:

```text
/mnt/external
/mnt/iso
/media/usb
/data
/backup
```

A mount point should usually be empty before mounting.

If the directory already contains files, those files are not deleted, but they become hidden while another filesystem is mounted on top of that directory.

Example:

```text
Before mounting:
/mnt/external contains oldfile.txt

After mounting /dev/sdb1 at /mnt/external:
/mnt/external shows the USB drive contents

After unmounting:
/mnt/external shows oldfile.txt again
```

This can confuse beginners, so it is best to use an empty directory as the mount point.

### Device Names

Linux represents storage devices using files under:

```text
/dev
```

Examples:

```text
/dev/sda      first disk
/dev/sda1     first partition on first disk
/dev/sdb      second disk
/dev/sdb1     first partition on second disk
/dev/nvme0n1  NVMe disk
/dev/nvme0n1p1 first partition on NVMe disk
```

A USB drive might appear as:

```text
/dev/sdb
```

and its first partition might appear as:

```text
/dev/sdb1
```

However, device names can change after rebooting or reconnecting hardware. For persistent configuration, it is usually better to use a UUID instead of a device name.

### Checking Which Devices Exist

Before mounting a device, first check whether Linux can see it.

Useful commands include:

```bash
lsblk
```

```bash
sudo fdisk -l
```

```bash
blkid
```

The `lsblk` command is often the easiest for beginners.

Example:

```bash
lsblk
```

Example output:

```text
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0 256.0G  0 disk
├─sda1   8:1    0   512M  0 part /boot
└─sda2   8:2    0 255.5G  0 part /
sdb      8:16   1  32.0G  0 disk
└─sdb1   8:17   1  32.0G  0 part
```

This shows that `/dev/sdb1` exists but is not currently mounted.

The `fdisk -l` command gives more detailed partition information:

```bash
sudo fdisk -l
```

Example output:

```text
Disk /dev/sdb: 32 GB
Device     Boot Start       End   Sectors  Size Id Type
/dev/sdb1        2048  62521343  62519296 29.8G 83 Linux
```

This means:

```text
/dev/sdb   is the disk
/dev/sdb1  is a partition on that disk
29.8G      is the partition size
Linux      is the partition type
```

The partition is usually what you mount, not the whole disk.

So you usually mount:

```text
/dev/sdb1
```

not:

```text
/dev/sdb
```

### The `mount` Command

The `mount` command attaches a filesystem to a mount point.

Basic syntax:

```bash
mount [OPTIONS] DEVICE MOUNT_POINT
```

Example:

```bash
sudo mount /dev/sdb1 /mnt/external
```

This means:

```text
Mount the filesystem on /dev/sdb1 at /mnt/external.
```

The general workflow is:

```text
Find the device
      |
      v
Create a mount point
      |
      v
Mount the device
      |
      v
Access files through the mount point
```

### Basic Manual Mount Example

Suppose a USB drive partition is available as:

```text
/dev/sdb1
```

and you want to access it at:

```text
/mnt/external
```

First, create the mount point:

```bash
sudo mkdir -p /mnt/external
```

Then mount the device:

```bash
sudo mount /dev/sdb1 /mnt/external
```

Now list the files:

```bash
ls /mnt/external
```

You can also move into the mounted filesystem:

```bash
cd /mnt/external
```

### Verifying Mounted Filesystems

To see mounted filesystems, you can run:

```bash
mount
```

However, the output can be long.

A cleaner command is:

```bash
findmnt
```

To check one mount point:

```bash
findmnt /mnt/external
```

Example output:

```text
TARGET        SOURCE    FSTYPE OPTIONS
/mnt/external /dev/sdb1 ext4   rw,relatime
```

This means:

|             | Description          |
| ----------- | -------------------- |
| **TARGET**  | Where it is mounted  |
| **SOURCE**  | Device being mounted |
| **FSTYPE**  | Filesystem type      |
| **OPTIONS** | Mount options        |


You can also use:

```bash
df -h
```

This shows mounted filesystems and available space in a human-readable format.

### Understanding Mount Output

A mount entry might look like this:

```text
/dev/sdb1 on /mnt/external type ext4 (rw,relatime)
```

Breaking it down:

```text
/dev/sdb1        device
/mnt/external    mount point
ext4             filesystem type
rw               read-write
relatime         access-time update behavior
```

The `rw` option means the filesystem is mounted read-write.

A read-only mount would show:

```text
ro
```

### Filesystem Types

A filesystem type describes how data is organized on the device.

Common filesystem types include:

| Filesystem  | Description                                    |
| ----------- | ---------------------------------------------- |
| **ext4**    | Common Linux filesystem                        |
| **xfs**     | Common on servers                              |
| **btrfs**   | Modern Linux filesystem with advanced features |
| **vfat**    | FAT32, common for USB drives                   |
| **exfat**   | Common for large USB drives and SD cards       |
| **ntfs**    | Common Windows filesystem                      |
| **iso9660** | CD/DVD ISO filesystem                          |
| **nfs**     | Network File System                            |
| **cifs**    | Windows/Samba network share                    |

Usually Linux can detect the filesystem automatically.

If needed, you can specify it manually with `-t`.

Example:

```bash
sudo mount -t ext4 /dev/sdb1 /mnt/external
```

For an NTFS drive:

```bash
sudo mount -t ntfs3 /dev/sdb1 /mnt/external
```

On some systems, especially older ones, NTFS support may use `ntfs-3g`:

```bash
sudo mount -t ntfs-3g /dev/sdb1 /mnt/external
```

If you get an error about an unknown filesystem type, you may need to install support for that filesystem.

### Mount Options

Mount options control how the filesystem is mounted.

Options are passed with `-o`.

Example:

```bash
sudo mount -o ro /dev/sdb1 /mnt/external
```

This mounts the filesystem as read-only.

Common options include:

| Option       | Description                                            |
| ------------ | ------------------------------------------------------ |
| **ro**       | Read-only                                              |
| **rw**       | Read-write                                             |
| **noexec**   | Do not allow execution of programs from the filesystem |
| **nosuid**   | Ignore set-user-ID and set-group-ID bits               |
| **nodev**    | Do not interpret device files                          |
| **uid=1000** | Set file owner for filesystems without Unix ownership  |
| **gid=1000** | Set group owner                                        |
| **defaults** | Use default options                                    |

Examples:

```bash
sudo mount -o ro /dev/sdb1 /mnt/external
```

```bash
sudo mount -o noexec,nosuid,nodev /dev/sdb1 /mnt/external
```

Read-only mounting is useful when you want to inspect a disk without accidentally changing it.

### Unmounting

Unmounting detaches a mounted filesystem from the directory tree.

The command is:

```bash
umount
```

Notice the spelling:

```text
umount
```

not:

```text
unmount
```

To unmount a filesystem, use either the mount point or the device.

Example using the mount point:

```bash
sudo umount /mnt/external
```

Example using the device:

```bash
sudo umount /dev/sdb1
```

After unmounting, the files from the device are no longer visible at the mount point.

### Why Unmounting Matters

You should unmount removable storage before physically removing it.

Linux often caches writes. This means that when you copy a file to a USB drive, the command may finish before all data has actually been written to the physical device.

Unmounting makes sure pending writes are completed.

The safe workflow is:

```text
Copy files
    |
    v
Unmount the device
    |
    v
Wait for command to finish
    |
    v
Physically remove the device
```

If you unplug a device without unmounting it, you may cause:

- corrupted files
- incomplete writes
- damaged filesystem metadata
- lost data

### The `sync` Command

The `sync` command asks Linux to flush cached writes to storage.

```bash
sync
```

This can be useful before unmounting removable media.

However, `sync` is not a replacement for `umount`.

A safer sequence is:

```bash
sync
sudo umount /mnt/external
```

### Handling “Target Is Busy”

Sometimes unmounting fails with an error like:

```text
umount: /mnt/external: target is busy
```

This means something is still using the mounted filesystem.

Common causes include:

- a terminal is currently inside the mount point
- a file is open in an editor
- a program is reading or writing files there
- a shell process has that directory as its current working directory

For example, if your terminal is currently in:

```text
/mnt/external
```

then unmounting may fail.

Move out of the directory:

```bash
cd ~
```

Then try again:

```bash
sudo umount /mnt/external
```

### Finding Processes Using a Mount

To see which processes are using a mount point, use `lsof`:

```bash
sudo lsof +f -- /mnt/external
```

Example output:

```text
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
bash     1234 user  cwd    DIR   8,17     4096    2 /mnt/external
```

This means a Bash process with PID `1234` has its current working directory inside `/mnt/external`.

The most important fields are:

| Field       | Description                  |
| ----------- | ---------------------------- |
| **COMMAND** | Process name                 |
| **PID**     | Process ID                   |
| **USER**    | User running the process     |
| **FD**      | File descriptor              |
| **NAME**    | File or directory being used |

Another useful command is:

```bash
sudo fuser -vm /mnt/external
```

To close the issue, first try to close the application or move the terminal out of the directory.

If needed, terminate the process:

```bash
sudo kill 1234
```

Use `kill` carefully. Terminating a process that is writing data may cause data loss.

### Lazy and Forced Unmounts

The `umount` command has advanced options.

Lazy unmount:

```bash
sudo umount -l /mnt/external
```

The `-l` option detaches the filesystem now and cleans it up after it is no longer busy.

Forced unmount:

```bash
sudo umount -f /mnt/external
```

The `-f` option forces the unmount.

Forced unmounts should be used carefully, especially for local disks, because they can risk data corruption.

A good rule is:

- Normal unmount first.
- Find and close processes if busy.
- Use lazy or forced unmount only when you understand the risk.

#### Mounting with a Specific Filesystem Type

Sometimes Linux does not automatically detect the filesystem type, or you want to be explicit.

Example for ext4:

```bash
sudo mount -t ext4 /dev/sdb1 /mnt/external
```

Example for NTFS:

```bash
sudo mount -t ntfs3 /dev/sdb1 /mnt/external
```

Example for FAT32:

```bash
sudo mount -t vfat /dev/sdb1 /mnt/external
```

Example for exFAT:

```bash
sudo mount -t exfat /dev/sdb1 /mnt/external
```

If mounting fails, check the filesystem type with:

```bash
lsblk -f
```

or:

```bash
sudo blkid /dev/sdb1
```

Example:

```text
/dev/sdb1: UUID="ABCD-1234" TYPE="exfat" LABEL="MYUSB"
```

### Mounting ISO Images

An ISO image is a file that contains the contents of a CD, DVD, or installation image.

For example:

```text
ubuntu.iso
```

You can mount an ISO file without burning it to a disc.

First create a mount point:

```bash
sudo mkdir -p /mnt/iso
```

Then mount the ISO:

```bash
sudo mount -o loop ubuntu.iso /mnt/iso
```

The `loop` option lets Linux treat a regular file as if it were a block device.

After mounting, view the files:

```bash
ls /mnt/iso
```

When finished, unmount it:

```bash
sudo umount /mnt/iso
```

The workflow looks like this:

```text
ubuntu.iso file
      |
      v
loop device
      |
      v
mounted at /mnt/iso
      |
      v
contents become accessible
```

### Mounting Network Shares

Network shares can also be mounted.

Two common types are:

```text
NFS      common between Linux/Unix systems
CIFS     used for Windows/Samba shares
```

Example NFS mount:

```bash
sudo mount -t nfs server:/export/data /mnt/data
```

Example CIFS mount:

```bash
sudo mount -t cifs //server/share /mnt/share -o username=myuser
```

Network mounts are common for shared storage, home directories, backups, and file servers.

For persistent network mounts, `/etc/fstab` or systemd mount units are often used.

### Persistent Mounts with `/etc/fstab`

Manual mounts disappear after reboot.

To mount a filesystem automatically at boot, configure it in:

```text
/etc/fstab
```

The file contains one filesystem per line.

Example:

```text
/dev/sdb1   /mnt/external   ext4    defaults    0   2
```

The fields are:

| Field           | Value           |
| --------------- | --------------- |
| **Device**      | `/dev/sdb1`     |
| **Mount point** | `/mnt/external` |
| **Filesystem**  | `ext4`          |
| **Options**     | `defaults`      |
| **Dump**        | `0`             |
| **fsck pass**   | `2`             |

The last two fields are older but still important:

```text
0   do not use dump backup
2   check this filesystem after the root filesystem
```

The root filesystem usually has pass value `1`.

Other local Linux filesystems often use `2`.

Filesystems that should not be checked at boot often use `0`.

### Prefer UUIDs in `/etc/fstab`

Device names such as `/dev/sdb1` can change.

For example, today a USB drive may be:

```text
/dev/sdb1
```

but after reboot it may become:

```text
/dev/sdc1
```

To avoid this problem, use a UUID.

Find the UUID:

```bash
sudo blkid /dev/sdb1
```

Example:

```text
/dev/sdb1: UUID="1234-ABCD" TYPE="ext4"
```

Then use the UUID in `/etc/fstab`:

```text
UUID=1234-ABCD   /mnt/external   ext4   defaults   0   2
```

This is more reliable than using `/dev/sdb1`.

### Testing `/etc/fstab`

After editing `/etc/fstab`, do not reboot immediately.

First test it with:

```bash
sudo mount -a
```

This attempts to mount everything listed in `/etc/fstab`.

If there is an error, fix it before rebooting.

A bad `/etc/fstab` entry can cause boot problems, especially if it refers to an unavailable device without safe options.

For removable or optional drives, consider options such as:

```text
nofail
x-systemd.automount
```

Example:

```text
UUID=1234-ABCD   /mnt/external   ext4   defaults,nofail   0   2
```

The `nofail` option allows the system to continue booting even if the device is not present.

## Visualizing the Mounting Process

Before mounting:

```text
/
├── bin
├── etc
├── home
│   └── user
├── mnt
├── usr
└── var
```

After mounting `/dev/sdb1` at `/mnt/external`:

```text
/
├── bin
├── etc
├── home
│   └── user
├── mnt
│   └── external
│       ├── data
│       └── projects
├── usr
└── var
```

The mounted filesystem becomes part of the normal directory tree.

You do not access it through a separate drive letter. You access it through the mount point.

### Typical Mounting Workflow

A safe manual mounting workflow looks like this:

1. Connect the device
2. Identify the device name
3. Check the filesystem type
4. Create a mount point
5. Mount the filesystem
6. Access the files
7. Unmount when finished
8. Remove the device

Commands:

```bash
lsblk -f
```

```bash
sudo mkdir -p /mnt/external
```

```bash
sudo mount /dev/sdb1 /mnt/external
```

```bash
ls /mnt/external
```

```bash
sudo umount /mnt/external
```

### Data Integrity

Always unmount removable filesystems before unplugging them.

This matters because Linux may delay writes for performance.

For example, copying a file may appear to finish quickly, but some data may still be waiting in memory.

Unmounting ensures that:

```text
pending writes are completed
open files are closed
filesystem metadata is updated
the device is safe to remove
```

This reduces the chance of corruption or data loss.

### Automounting

Many desktop systems already automount removable drives.

For servers or custom setups, there are several ways to automate mounting:

```text
/etc/fstab
systemd mount units
systemd automount units
udev rules
desktop environment automounting
autofs
```

For most users, `/etc/fstab` is the best starting point.

For advanced users, `udev` can run actions when hardware appears or disappears.

### Automating Mounting with `udev`

`udev` manages device events in Linux.

It can detect when a USB drive is connected and run a command or script.

However, using `udev` directly for mounting can be tricky. Long commands with shell features such as `&&` may not work as expected unless run through a script or shell.

A cleaner approach is to have a `udev` rule call a script.

First, identify the device UUID:

```bash
sudo blkid /dev/sdX1
```

Example:

```text
/dev/sdX1: UUID="1234-ABCD" TYPE="ext4"
```

Create a script:

```bash
sudo nano /usr/local/sbin/mount-my-usb.sh
```

Example script:

```bash
#!/bin/sh
mkdir -p /media/my_usb
mount UUID=1234-ABCD /media/my_usb
```

Make it executable:

```bash
sudo chmod +x /usr/local/sbin/mount-my-usb.sh
```

Then create a `udev` rule:

```bash
sudo nano /etc/udev/rules.d/99-usb-mount.rules
```

Example rule:

```text
ACTION=="add", SUBSYSTEM=="block", ENV{ID_FS_UUID}=="1234-ABCD", RUN+="/usr/local/sbin/mount-my-usb.sh"
```

Reload rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Then unplug and reconnect the device to test.

For many real systems, `systemd` automounts or desktop automounting are easier and more reliable than custom `udev` mounting rules.

### Troubleshooting Mounting Problems

#### Problem: Permission Denied

Example:

```text
mount: permission denied
```

Possible causes:

- you forgot sudo
- the mount point permissions are restricted
- the filesystem permissions do not allow access
- security policy is blocking the mount

Try:

```bash
sudo mount /dev/sdb1 /mnt/external
```

If the mount succeeds but your user cannot write to the mounted filesystem, check ownership and permissions.

For Linux filesystems such as ext4, use:

```bash
ls -ld /mnt/external
```

For FAT, exFAT, or NTFS filesystems, ownership may need to be controlled with mount options such as `uid` and `gid`.

Example:

```bash
sudo mount -o uid=1000,gid=1000 /dev/sdb1 /mnt/external
```

#### Problem: Unknown Filesystem Type

Example:

```text
mount: unknown filesystem type 'exfat'
```

Possible causes:

- missing filesystem driver
- wrong filesystem type specified
- damaged filesystem

Check the type:

```bash
lsblk -f
```

or:

```bash
sudo blkid /dev/sdb1
```

Then install the needed support package if necessary.

For example, NTFS or exFAT support may require additional packages on some systems.

#### Problem: Target Is Busy

Example:

```text
umount: /mnt/external: target is busy
```

Find processes using it:

```bash
sudo lsof +f -- /mnt/external
```

or:

```bash
sudo fuser -vm /mnt/external
```

Then close the program, move out of the directory, or stop the process.

Common fix:

```bash
cd ~
sudo umount /mnt/external
```

#### Problem: Device Not Found

Example:

```text
mount: /dev/sdb1 does not exist
```

Check devices:

```bash
lsblk
```

Possible causes:

- device not plugged in
- wrong device name
- kernel has not detected it yet
- bad cable or port
- device name changed

Check recent kernel messages:

```bash
dmesg | tail
```

#### Problem: Bad `/etc/fstab` Entry

If `mount -a` fails, inspect `/etc/fstab`.

Common mistakes include:

- wrong UUID
- wrong filesystem type
- missing mount point directory
- bad mount options
- incorrect spacing

Create the mount point if missing:

```bash
sudo mkdir -p /mnt/external
```

Then test again:

```bash
sudo mount -a
```

### Challenges

1. Plug a USB drive into your system and use `lsblk` and `fdisk -l` to identify the device name and partition details. Discuss how device names are assigned and explain the difference between physical devices and partitions.
2. Create a new directory under `/mnt` or `/media`, and mount your USB drive to this directory using the `mount` command. Describe the purpose of mount points and how they provide access to external storage devices on Linux.
3. Navigate to the mount point of the USB drive and perform basic file operations—create, read, edit, and delete a file. Discuss how mounting makes files accessible and how permissions might affect file access on mounted devices.
4. What happens if you mount a USB drive onto an existing non-empty directory? Is this allowed, and if so, what happens to the directory’s original contents?
5. Create a virtual disk file in your home directory using the `dd` command, specifying its size and location. Discuss how virtual disk files can simulate actual disks and their potential uses in testing and development.
6. Format the virtual disk file with an `ext4` filesystem using `mkfs.ext4`. Explain the significance of different filesystem types and why choosing an appropriate filesystem is important for specific use cases.
7. Mount the formatted virtual disk file to a directory under `/mnt`, just as you would a physical device. Discuss the concept of loopback devices and how they allow files to be mounted as if they were physical disks.
8. Investigate the differences between temporary and persistent mounting by adding an entry for your USB drive or virtual disk in `/etc/fstab`. Explain how persistent mounts work and the benefits of configuring automatic mounts for commonly used devices.
9. Explore permissions on the mounted USB drive by changing the ownership and permissions of files on it. Discuss how Linux handles permissions for different users on mounted devices and the implications for shared drives.
10. Create a script that automatically mounts and unmounts the USB drive upon insertion and removal, utilizing `udev` rules for automation. Explain how `udev` helps manage device events in Linux and the advantages of automated mounting for frequently used external devices.
