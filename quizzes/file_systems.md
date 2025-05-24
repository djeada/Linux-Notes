#### Q. Which command creates an ext4 filesystem on `/dev/sdb1`?

* [ ] `mkfs -t ext3 /dev/sdb1`
* [ ] `mkfs.ext4 -o /dev/sdb1`
* [x] `mkfs.ext4 /dev/sdb1`
* [ ] `mkfs.ext4 -f /mount/sdb1`
* [ ] `format ext4 /dev/sdb1`

#### Q. In `/etc/fstab`, what does the third field specify?

* [ ] The filesystem UUID
* [x] The mount point
* [ ] Mount options
* [ ] Dump/pass order
* [ ] Filesystem type

#### Q. What is an inode in a Linux filesystem?

* [ ] A special file that holds swap space
* [ ] The superblock backup area
* [x] A data structure storing metadata about a file
* [ ] The journal log of filesystem changes
* [ ] A symbolic link to the file’s data blocks

#### Q. Which mount option disables updating the file access time?

* [ ] `nosuid`
* [ ] `nodev`
* [x] `noatime`
* [ ] `ro`
* [ ] `sync`

#### Q. How do you repair a corrupted ext4 filesystem on `/dev/sda2`?

* [ ] `fsck.ext4 /mount/sda2`
* [x] `fsck.ext4 -y /dev/sda2`
* [ ] `e2fsck /mount/sda2`
* [ ] `tune2fs -r /dev/sda2`
* [ ] `mkfs.ext4 -r /dev/sda2`

#### Q. Which of these is a journaling filesystem?

* [ ] FAT32
* [ ] NTFS
* [x] XFS
* [ ] ISO9660
* [ ] UDF

#### Q. To mount a filesystem by its UUID, which command format is correct?

* [ ] `mount /dev/disk/by-label/UUID-1234 /mnt`
* [x] `mount UUID=1234-abcd /mnt`
* [ ] `mount -t ext4 1234-abcd /mnt`
* [ ] `mount /mnt UUID=1234-abcd`
* [ ] `mount /dev/sdb1 /mnt --uuid`

#### Q. Which command mounts the partition `/dev/sdb2` (ext4) on the directory `/data`?

* [ ] `mount /dev/sdb2 /data -t ext4`
* [x] `mount -t ext4 /dev/sdb2 /data`
* [ ] `mount /data /dev/sdb2 -t ext4`
* [ ] `mount -o ext4 /data /dev/sdb2`
* [ ] `mount /dev/sdb2 ext4 /data`

#### Q. Where do you define persistent (automatic) mounts so they survive reboot?

* [ ] `/etc/mtab`
* [ ] `/proc/mounts`
* [x] `/etc/fstab`
* [ ] `/etc/exports`
* [ ] `/etc/auto.master`

#### Q. In `/etc/fstab`, which field (by position) specifies mount options?

* [ ] 1st field
* [ ] 2nd field
* [ ] 3rd field
* [x] 4th field
* [ ] 5th field

#### Q. Which mount option makes a filesystem read-only?

* [ ] `noexec`
* [ ] `nosuid`
* [x] `ro`
* [ ] `rw`
* [ ] `nodev`

#### Q. What command causes the system to (re)mount all filesystems listed in `/etc/fstab`?

* [ ] `mount --all`
* [x] `mount -a`
* [ ] `mount --reload`
* [ ] `mount --fstab`
* [ ] `mount --enable`

#### Q. How do you create a bind-mount of `/var/log` onto `/mnt/logs`?

* [ ] `mount --loop /var/log /mnt/logs`
* [x] `mount --bind /var/log /mnt/logs`
* [ ] `mount -t bind /var/log /mnt/logs`
* [ ] `mount -o loop /var/log /mnt/logs`
* [ ] `mount -o dirbind /var/log /mnt/logs`

#### Q. Which command unmounts `/mnt/data` but only when it’s no longer busy (lazy unmount)?

* [ ] `umount -f /mnt/data`
* [x] `umount -l /mnt/data`
* [ ] `umount /mnt/data --lazy`
* [ ] `umount -a /mnt/data`
* [ ] `umount --detach /mnt/data`

#### Q. Which utility displays currently mounted filesystems in a tree view?

* [ ] `mount --tree`
* [ ] `df --tree`
* [x] `findmnt`
* [ ] `lsblk -t`
* [ ] `blkid --tree`

#### Q. To mount a `tmpfs` of size 512 MB at `/mnt/tmp`, which command is correct?

* [ ] `mount -t tmpfs tmpfs /mnt/tmp size=512M`
* [x] `mount -t tmpfs -o size=512M tmpfs /mnt/tmp`
* [ ] `mount tmpfs /mnt/tmp -o 512M`
* [ ] `mount -o tmpfs,size=512M /mnt/tmp`
* [ ] `mount -t tmpfs /mnt/tmp -L 512M`

#### Q. Which service handles dynamic on-demand automounting via `/etc/auto.*` maps?

* [ ] `autofs`
* [ ] `systemd-automount`
* [ ] `autohome`
* [x] `autofs`
* [ ] `automountd`

#### Q. Which file lists directories to be shared via NFS on the server?

* [ ] `/etc/hosts.allow`
* [ ] `/etc/exports.conf`
* [x] `/etc/exports`
* [ ] `/etc/nfs.conf`
* [ ] `/etc/exports.d/nfs.exports`

#### Q. What command applies changes made in `/etc/exports` without restarting the NFS service?

* [ ] `systemctl restart nfs-server`
* [ ] `exportfs --reload-all`
* [ ] `exportfs -arv`
* [x] `exportfs -ra`
* [ ] `exportfs --update`

#### Q. By default, which port does the NFS server listen on for NFSv3?

* [ ] TCP/2049 only
* [ ] UDP/111 only
* [ ] TCP/20048
* [x] TCP/2049 and uses portmapper on 111
* [ ] UDP/2049

#### Q. Which mount option on the client makes file writes synchronous (i.e., safe but slower)?

* [ ] `soft`
* [ ] `intr`
* [x] `sync`
* [ ] `bg`
* [ ] `noexec`

#### Q. How do you mount an NFS export `server:/export/home` on `/mnt/home`?

* [ ] `mount nfs server:/export/home /mnt/home`
* [ ] `mount -t nfs4 server:/export/home /mnt/home`
* [x] `mount -t nfs server:/export/home /mnt/home`
* [ ] `mount.nfs /export/home /mnt/home`
* [ ] `mount.nfs4 server:/export/home /mnt/home`

#### Q. Which utility shows currently mounted clients on an NFS server?

* [ ] `showmount -e`
* [x] `showmount -a`
* [ ] `rpcinfo -p`
* [ ] `nfsstat -s`
* [ ] `exportfs -v`

#### Q. What does the `no_root_squash` option in `/etc/exports` do?

* [ ] Allows root on the server to map to root on the client
* [x] Allows root on the client to act as root on exported share
* [ ] Disables UID mapping entirely
* [ ] Prevents any root access to the share
* [ ] Enables root to change squash options

#### Q. Which protocol does NFSv4 use by default for locking and state management?

* [ ] NLM (Network Lock Manager)
* [ ] statd over RPCBIND
* [x] Built-in stateful protocol over TCP/2049
* [ ] LDAP
* [ ] HTTP

#### Q. In `/etc/fstab`, which option ensures an NFS mount retries indefinitely until the server is available?

* [ ] `soft`
* [ ] `timeo=0`
* [x] `hard`
* [ ] `nolock`
* [ ] `noauto`

#### Q. What is a common symptom of a “stale file handle” error on NFS clients?

* [ ] Authentication failures when mounting
* [ ] Files always appearing with zero size
* [x] “Stale file handle” messages when accessing files after server reboot or export change
* [ ] Inability to resolve hostnames
* [ ] Kernel panic on file operations

#### Q. What does the `tune2fs -l /dev/sdb1` command display?

* [ ] Live I/O statistics for the filesystem
* [ ] The on-disk block allocation map
* [x] Filesystem superblock parameters and labels
* [ ] A list of files in the root directory
* [ ] Current mount options in use

#### Q. Which filesystem is case-sensitive but not case-preserving?

* [ ] NTFS
* [x] UDF
* [ ] ext4
* [ ] XFS
* [ ] VFAT

#### Q. What does enabling quotas on a filesystem allow you to do?

* [ ] Encrypt user data at rest
* [ ] Automatically back up changed files
* [ ] Mount the filesystem read-only
* [x] Limit disk usage per user or group
* [ ] Convert the filesystem to read-write compression
