# File Systems Quiz

Notes: [File Systems](../notes/file_system.md), [Mounting](../notes/mounting.md), [NFS](../notes/nfs.md)

Check your understanding of filesystem types, the directory hierarchy, mounting, `/etc/fstab` and NFS.

#### Q. Which command creates an ext4 filesystem on the partition `/dev/sdb1`?

* [ ] `mkfs -t ext3 /dev/sdb1`
* [x] `mkfs.ext4 /dev/sdb1`
* [ ] `mkfs.ext4 /mnt/sdb1`
* [ ] `format ext4 /dev/sdb1`

> **Explanation:** `mkfs.ext4` takes the block device, not a mount point. `mkfs -t ext3` would build the wrong filesystem type, and `format` is not a Linux command.

#### Q. What happens to the existing files on `/dev/sdb1` when you run `mkfs.ext4 /dev/sdb1`?

* [ ] They are converted to the ext4 format
* [ ] They are moved to a `lost+found` directory
* [x] They are lost, because a new empty filesystem replaces the old one
* [ ] They are kept, because `mkfs` only writes free space

> **Explanation:** Creating a filesystem writes fresh metadata (superblock, inode tables, journal) over the old structures, so existing data is no longer reachable. Back up first and double-check the device name.

#### Q. Which command sets the label `mydata` on an existing ext4 filesystem without reformatting it?

* [ ] `mkfs.ext4 -L mydata /dev/sdb1`
* [ ] `blkid -L mydata`
* [x] `e2label /dev/sdb1 mydata`
* [ ] `findmnt -L mydata`

> **Explanation:** `e2label` changes the label in place, and running it with only the device prints the current label. `mkfs.ext4 -L` sets a label but also wipes the filesystem, and `blkid -L` looks a device up by label.

#### Q. In the `/etc/fstab` line below, which value is the mount options field?

```text
/dev/sdb1   /mnt/external   ext4    defaults    0   2
```

* [ ] `ext4`
* [ ] `/mnt/external`
* [x] `defaults`
* [ ] `2`

> **Explanation:** The fields are device, mount point, filesystem type, options, dump and fsck pass. `defaults` is the standard set of options such as read-write.

#### Q. In the `/etc/fstab` line below, what does the final `2` mean?

```text
UUID=1234-ABCD   /mnt/mydata   ext4   defaults   0   2
```

* [ ] Mount the filesystem two seconds after boot
* [ ] Keep two backup copies with `dump`
* [x] Check the filesystem with `fsck` after the root filesystem
* [ ] Allow two retries if mounting fails

> **Explanation:** The sixth field is the fsck pass order: `1` is usually the root filesystem, `2` means check after root, and `0` means do not check. The fifth field, `0` here, disables `dump` backups.

#### Q. Why is `UUID=...` usually preferred over `/dev/sdb1` in `/etc/fstab`?

* [ ] UUIDs make the filesystem mount faster
* [x] Device names such as `/dev/sdb1` can change between boots, but a filesystem's UUID does not
* [ ] Only UUIDs work with ext4
* [ ] UUIDs encrypt the mount

> **Explanation:** Adding or removing disks can renumber `/dev/sdX` names, causing the wrong device to mount or a boot failure. The UUID identifies the filesystem itself.

#### Q. Which command prints the UUID and filesystem type of `/dev/sdb1`?

* [x] `blkid /dev/sdb1`
* [ ] `df -h /dev/sdb1`
* [ ] `e2label /dev/sdb1`
* [ ] `fdisk -l /dev/sdb1`

> **Explanation:** `blkid` reads the filesystem signature and prints `UUID=` and `TYPE=`. `e2label` shows only the label, `df` shows usage and `fdisk -l` shows partition layout. `lsblk -f` is another way to see UUIDs.

#### Q. Which command mounts the filesystem with UUID `1234-abcd` on `/mnt`?

* [x] `mount UUID=1234-abcd /mnt`
* [ ] `mount /mnt UUID=1234-abcd`
* [ ] `mount -t ext4 1234-abcd /mnt`
* [ ] `mount /dev/1234-abcd /mnt`

> **Explanation:** `mount` accepts `UUID=` (or `LABEL=`) as the source, followed by the mount point. A bare UUID is treated as a path and fails.

#### Q. You just added a line to `/etc/fstab`. What should you run before rebooting to catch mistakes?

* [ ] `sync`
* [x] `sudo mount -a`
* [ ] `sudo umount -a`
* [ ] `sudo fsck /etc/fstab`

> **Explanation:** `mount -a` tries to mount everything listed in `/etc/fstab`, so a typo shows up now instead of breaking the next boot. `fsck` checks filesystems, not configuration files.

#### Q. Which `/etc/fstab` option lets the system finish booting even if a listed external drive is not connected?

* [ ] `noauto,rw`
* [ ] `ro`
* [x] `nofail`
* [ ] `sync`

> **Explanation:** `nofail` tells the boot process not to treat a missing device as an error. It is recommended for removable or optional disks, often combined with `x-systemd.automount`.

#### Q. Which mount option stops the kernel from updating a file's access time every time it is read?

* [ ] `nosuid`
* [ ] `nodev`
* [x] `noatime`
* [ ] `sync`

> **Explanation:** `noatime` skips access-time updates, reducing writes on busy filesystems. `nosuid` and `nodev` are security options, and `sync` makes writes synchronous.

#### Q. You need to inspect a disk from a damaged system without any risk of changing it. Which mount command is appropriate?

* [ ] `sudo mount -o rw /dev/sdb1 /mnt/external`
* [x] `sudo mount -o ro /dev/sdb1 /mnt/external`
* [ ] `sudo mount -o noexec /dev/sdb1 /mnt/external`
* [ ] `sudo mount -o remount /dev/sdb1 /mnt/external`

> **Explanation:** `ro` mounts the filesystem read-only, so nothing can be written. `noexec` blocks running programs but still allows writes.

#### Q. What does the `noexec` mount option do?

* [ ] Makes the filesystem read-only
* [x] Prevents programs on the filesystem from being executed directly
* [ ] Ignores device files on the filesystem
* [ ] Hides executable files from directory listings

> **Explanation:** With `noexec`, binaries stored on that filesystem cannot be run, which is useful for removable media or `/tmp`. Files can still be read and written.

#### Q. What does the `nosuid` mount option do?

* [x] Ignores set-user-ID and set-group-ID bits on files in that filesystem
* [ ] Prevents users other than root from mounting it
* [ ] Removes all user ownership information
* [ ] Disables symbolic links

> **Explanation:** With `nosuid`, a setuid program on that filesystem runs with the caller's own privileges, so a planted setuid-root binary cannot be used to gain root.

#### Q. The root filesystem was mounted read-only during recovery. Which command makes it writable without rebooting?

* [ ] `mount -a /`
* [ ] `umount -l /`
* [ ] `mount --bind / /`
* [x] `mount -o remount,rw /`

> **Explanation:** `remount` changes the options of an already-mounted filesystem in place, here switching it to read-write. Unmounting `/` on a running system is not an option.

#### Q. Which command makes the contents of the image file `ubuntu.iso` browsable at `/mnt/iso`?

* [ ] `sudo mount --bind ubuntu.iso /mnt/iso`
* [ ] `sudo cp ubuntu.iso /mnt/iso`
* [x] `sudo mount -o loop ubuntu.iso /mnt/iso`
* [ ] `sudo tar -xf ubuntu.iso /mnt/iso`

> **Explanation:** The `loop` option attaches the regular file to a loop device so it can be mounted like a disk. A bind mount only mirrors existing directories, and copying the file does not expose its contents.

#### Q. Which command makes the existing directory `/var/log` also accessible at `/mnt/logs`?

* [ ] `mount -o loop /var/log /mnt/logs`
* [x] `mount --bind /var/log /mnt/logs`
* [ ] `mount -t tmpfs /var/log /mnt/logs`
* [ ] `mount -o remount /var/log /mnt/logs`

> **Explanation:** A bind mount attaches an existing directory tree at a second location. `loop` is for image files, and a tmpfs mount would create an empty in-memory filesystem.

#### Q. The directory `/mnt/external` contains `oldfile.txt`. What happens to it when you mount `/dev/sdb1` on `/mnt/external`?

* [ ] It is deleted
* [ ] It is copied onto the USB drive
* [x] It is hidden until the filesystem is unmounted
* [ ] It appears alongside the USB drive's files

> **Explanation:** Mounting places the new filesystem over the directory, hiding the original contents without touching them. They reappear after `umount`, which is why empty mount points are recommended.

#### Q. `sudo umount /mnt/external` fails with "target is busy". What is a common cause?

* [ ] The filesystem has errors that need `fsck`
* [x] A shell or program has its current directory or an open file inside `/mnt/external`
* [ ] The device was mounted with `nofail`
* [ ] The command must be spelled `unmount`

> **Explanation:** The kernel will not detach a filesystem that is in use. `cd` out of the mount point or close the program, then try again.

#### Q. Which command shows which processes are using the mount at `/mnt/external`?

* [ ] `findmnt /mnt/external`
* [ ] `df -h /mnt/external`
* [x] `sudo fuser -vm /mnt/external`
* [ ] `lsblk /mnt/external`

> **Explanation:** `fuser -vm` lists processes with files or working directories on that filesystem; `lsof +f -- /mnt/external` gives similar output. `findmnt` and `df` describe the mount itself, not its users.

#### Q. What does `umount -l /mnt/external` do?

* [ ] Lists processes that keep the mount busy
* [x] Detaches the mount point now and finishes cleanup once it is no longer busy
* [ ] Forces the unmount and kills processes using it
* [ ] Unmounts every filesystem listed in `/etc/fstab`

> **Explanation:** A lazy unmount removes the filesystem from the directory tree immediately and releases it once the last user finishes. Prefer a normal unmount after closing the users when you can.

#### Q. Why should you unmount a USB drive before unplugging it?

* [ ] Unmounting erases temporary files from the drive
* [x] Linux caches writes, and unmounting ensures they are written to the device
* [ ] The drive cannot be detected again otherwise
* [ ] Unmounting checks the drive for viruses

> **Explanation:** A copy may finish while data still sits in the page cache. `umount` flushes pending writes and closes the filesystem cleanly; `sync` flushes too but does not replace unmounting.

#### Q. Which utility lists mounted filesystems as a tree with their sources, types and options?

* [ ] `blkid`
* [x] `findmnt`
* [ ] `fdisk -l`
* [ ] `du -h`

> **Explanation:** `findmnt` shows the mount hierarchy, and `findmnt /mnt/point` checks a single mount. `blkid` reports filesystem signatures and `fdisk -l` shows partition tables.

#### Q. What should you do before running `fsck` to repair the ext4 filesystem on `/dev/sdb1`?

* [ ] Mount it read-write so changes can be saved
* [ ] Run `mkfs.ext4` to reset its metadata
* [ ] Delete its `lost+found` directory
* [x] Unmount it

> **Explanation:** Repairing a mounted filesystem can corrupt it further because the kernel is changing it at the same time. Unmount first, or for the root filesystem use a rescue or live environment.

#### Q. What does `tune2fs -l /dev/sdb1` display?

* [ ] Live I/O statistics for the device
* [ ] The files in the filesystem's root directory
* [x] The filesystem's superblock information, such as block count, inode count, UUID and features
* [ ] The current mount options

> **Explanation:** `-l` lists superblock contents for ext2, ext3 and ext4. Mount options are shown by `findmnt`, and I/O statistics by tools such as `iostat`.

#### Q. Which command converts an existing ext2 filesystem to ext3 by adding a journal?

* [x] `tune2fs -O has_journal /dev/sdb1`
* [ ] `mkfs.ext3 /dev/sdb1`
* [ ] `resize2fs -j /dev/sdb1`
* [ ] `e2label /dev/sdb1 ext3`

> **Explanation:** `tune2fs -O has_journal` enables the journal feature in place, keeping the data. `mkfs.ext3` would create a new, empty filesystem.

#### Q. Which filesystem added journaling to the ext family for the first time?

* [ ] ext2
* [x] ext3
* [ ] ext4
* [ ] FAT32

> **Explanation:** ext3 is ext2 plus a journal, which records pending changes so the filesystem can recover quickly after a crash. ext4 kept journaling and added larger limits and extents.

#### Q. Which Linux filesystem uses copy-on-write and natively supports snapshots and subvolumes?

* [ ] ext4
* [ ] XFS
* [x] Btrfs
* [ ] FAT32

> **Explanation:** Btrfs writes changed data to new locations instead of overwriting, which makes cheap snapshots possible. ext4 and XFS are journaling filesystems without built-in snapshots.

#### Q. Which filesystem, originally developed by Silicon Graphics, is known for high performance with large files and parallel I/O?

* [ ] ext3
* [ ] ReiserFS
* [ ] JFS
* [x] XFS

> **Explanation:** XFS was created by SGI and scales well under concurrent workloads. JFS came from IBM and ReiserFS is a historical filesystem known for handling many small files.

#### Q. What is the role of the Virtual File System (VFS) in the Linux kernel?

* [ ] It stores files in RAM instead of on disk
* [ ] It shares files with other machines over the network
* [x] It gives programs one common interface for working with many different filesystem types
* [ ] It encrypts data before it reaches the disk

> **Explanation:** The VFS layer translates system calls like `open` and `read` into operations for ext4, XFS, NFS and others, so applications do not need filesystem-specific code.

#### Q. Copying a 6 GB video to a USB stick fails, although the stick has plenty of free space. The stick is most likely formatted with which filesystem?

* [x] FAT32
* [ ] exFAT
* [ ] ext4
* [ ] NTFS

> **Explanation:** FAT32 limits individual files to 4 GiB minus 1 byte. exFAT, NTFS and ext4 all support much larger files.

#### Q. A program needs temporary files that survive a reboot. Which directory is intended for that?

* [ ] `/tmp`
* [x] `/var/tmp`
* [ ] `/run`
* [ ] `/proc`

> **Explanation:** `/tmp` is commonly cleared at boot and `/run` holds volatile runtime data, while `/var/tmp` is meant to persist between reboots. `/proc` is a kernel pseudo filesystem.

#### Q. Where should an administrator install a program compiled from source so it does not clash with distribution-managed packages?

* [ ] `/usr/bin`
* [x] `/usr/local/bin`
* [ ] `/bin`
* [ ] `/etc`

> **Explanation:** The package manager owns `/usr/bin` and `/bin`. `/usr/local` (or `/opt`) is reserved for locally installed software, and `/etc` is for configuration, not binaries.

#### Q. Why should you never store persistent files in `/proc` or `/sys`?

* [ ] They are mounted read-only for all users
* [ ] They are backed up and overwritten every night
* [ ] They are encrypted with a per-boot key
* [x] They are pseudo filesystems generated by the kernel, with no data stored on disk

> **Explanation:** `/proc` and `/sys` expose live kernel and process state. Their contents are created on the fly and disappear at shutdown.

#### Q. How do block device files differ from character device files under `/dev`?

* [ ] Block devices are virtual, while character devices are physical hardware
* [x] Block devices transfer data in blocks (such as disks), while character devices handle a stream of bytes (such as terminals)
* [ ] Block devices can only be read by root, while character devices can be read by anyone
* [ ] Block devices hold directories, while character devices hold files

> **Explanation:** Disks like `/dev/sda` are block devices accessed in fixed-size chunks. Keyboards, terminals and serial ports are character devices; `ls -l` marks them with `b` and `c`.

#### Q. Which file on an NFS server defines which directories are shared and which clients may access them?

* [ ] `/etc/fstab`
* [ ] `/etc/hosts.allow`
* [x] `/etc/exports`
* [ ] `/etc/idmapd.conf`

> **Explanation:** Each line in `/etc/exports` names a directory followed by the allowed clients and options, such as `/opt/shared 192.168.1.0/24(rw,sync,root_squash)`. Clients use `/etc/fstab` to mount shares.

#### Q. After editing `/etc/exports`, which command applies the changes without restarting the NFS service?

* [ ] `sudo exportfs -u`
* [ ] `sudo exportfs -v`
* [ ] `showmount -e localhost`
* [x] `sudo exportfs -r`

> **Explanation:** `exportfs -r` re-reads `/etc/exports` and syncs the active export table. `-v` only displays current exports and `-u` unexports a directory.

#### Q. What does the `root_squash` export option do?

* [ ] Gives client root full root access to the export
* [ ] Prevents the server's root user from reading the export
* [ ] Forces all client users to log in as root
* [x] Maps requests from root on the client to an anonymous unprivileged user

> **Explanation:** With `root_squash`, UID 0 on a client becomes `nobody` (or `nfsnobody`) on the server. `no_root_squash` disables this protection and should be avoided unless truly needed.

#### Q. Which export option maps every client user, not just root, to the anonymous user?

* [ ] `no_root_squash`
* [x] `all_squash`
* [ ] `no_subtree_check`
* [ ] `async`

> **Explanation:** `all_squash` makes all access use one server-side identity, which can be chosen with `anonuid` and `anongid`. It suits simple public drop-box shares.

#### Q. What does the `sync` option in `/etc/exports` mean?

* [ ] The client caches all writes locally
* [x] The server commits changes to storage before replying to the client
* [ ] Exports are re-read every minute
* [ ] The export is mirrored to a second server

> **Explanation:** `sync` is the safe choice: a reply means the data is stored. `async` replies earlier for speed but can lose data if the server crashes.

#### Q. Why is NFSv4 generally easier to put behind a firewall than NFSv3?

* [ ] It uses UDP only
* [ ] It needs no open ports at all
* [x] It uses a single main TCP port, 2049
* [ ] It runs over HTTPS on port 443

> **Explanation:** NFSv4 is a stateful protocol that carries everything over TCP port 2049. NFSv3 relies on extra services such as rpcbind on port 111 and mountd, often on varying ports.

#### Q. Which command mounts the export `/opt/shared` from the server `192.168.1.100` on `/mnt/nfs_shared`?

* [ ] `sudo mount -t nfs /mnt/nfs_shared 192.168.1.100:/opt/shared`
* [x] `sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared`
* [ ] `sudo mount -t nfs 192.168.1.100 /opt/shared /mnt/nfs_shared`
* [ ] `sudo mount --bind 192.168.1.100:/opt/shared /mnt/nfs_shared`

> **Explanation:** The source is written `server:/path`, followed by the local mount point. Reversing them or splitting the host from the path makes `mount` fail, and a bind mount only works with local directories.

#### Q. From a client, which command lists the directories that the NFS server `192.168.1.100` advertises?

* [ ] `exportfs -v 192.168.1.100`
* [x] `showmount -e 192.168.1.100`
* [ ] `findmnt 192.168.1.100`
* [ ] `nfsidmap -l 192.168.1.100`

> **Explanation:** `showmount -e` queries the server's export list (most useful with NFSv3-style services). `exportfs` runs on the server itself, and `findmnt` shows local mounts.

#### Q. A laptop has an NFS share in `/etc/fstab` and hangs at boot when away from the office network. Which options fix this?

* [ ] `defaults,sync`
* [ ] `ro,noatime`
* [ ] `hard,intr`
* [x] `_netdev,nofail,x-systemd.automount`

> **Explanation:** `_netdev` marks the mount as network-dependent, `nofail` stops a missing server from failing the boot, and `x-systemd.automount` mounts the share on first access instead of at boot.

#### Q. User alice has UID 1000 on an NFS client but UID 2000 on the server. Why does she get "Permission denied" on her own files in the share?

* [ ] NFS ignores file permissions for non-root users
* [ ] The server always maps users to `nobody`
* [x] NFS sends the numeric UID 1000, which the server does not treat as alice
* [ ] Usernames longer than four characters are not supported

> **Explanation:** With traditional NFS authentication, ownership checks use numeric UIDs and GIDs. Keep them consistent through central identity management such as LDAP, or assign matching IDs manually.

#### Q. Files on an NFSv4 mount show the owner `nobody` even though the UIDs match. What is a likely cause?

* [ ] The export uses `sync`
* [x] The NFSv4 ID-mapping domain in `/etc/idmapd.conf` differs between client and server
* [ ] The client mounted the share with `noatime`
* [ ] The server's disk is full

> **Explanation:** NFSv4 maps names using a domain; if the client and server domains differ, names cannot be mapped and owners appear as `nobody` or `4294967294`. Squash options can produce the same symptom.

#### Q. A client shows "Stale file handle" after the server's exported directory was renamed and recreated. How do you fix it on the client?

* [ ] Run `exportfs -r` on the client
* [x] Leave the directory, then unmount and remount the share
* [ ] Run `fsck` on the NFS mount point
* [ ] Delete and recreate the local mount point directory

> **Explanation:** The client still holds references to the old directory objects. Remounting obtains fresh handles; use `fuser -vm` or `lsof` if the unmount reports that the target is busy.
