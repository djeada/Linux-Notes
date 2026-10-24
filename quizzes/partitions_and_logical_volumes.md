# Partitions and Logical Volumes Quiz

Notes: [Partitions](../notes/partitions.md), [Logical Volume Management](../notes/logical_volume_management.md)

Check your understanding of MBR and GPT partitioning, partitioning tools, and LVM physical volumes, volume groups, logical volumes and snapshots.

#### Q. What is a disk partition?

* [ ] A directory that has its own permissions
* [x] A section of a disk that the OS can manage independently, with its own filesystem
* [ ] A copy of the disk kept for recovery
* [ ] A file that stores swap space

> **Explanation:** A partition is a region of a physical disk recorded in the partition table. Each one can be formatted with its own filesystem and mounted separately, or used for swap.

#### Q. On a shared server, two projects store data in `/srv/projA` and `/srv/projB` on the same filesystem. What stops one project from filling the disk for both?

* [x] Nothing, unless the directories are on separate partitions or logical volumes, or quotas are used
* [ ] Directory permissions automatically limit each directory's capacity
* [ ] Linux reserves an equal share of space for each top-level directory
* [ ] The `/srv` directory is limited to half of the disk by default

> **Explanation:** Directories on one filesystem share its free space. Permissions control who can access files, not how much space they use; capacity is isolated by separate partitions or LVs, or limited with quotas.

#### Q. How many primary partitions can an MBR partition table hold?

* [ ] 2
* [x] 4
* [ ] 16
* [ ] 128

> **Explanation:** MBR has room for four primary entries. To get more partitions, one of them can be an extended partition holding logical partitions. 128 is GPT's default entry count.

#### Q. What is the purpose of an extended partition on an MBR disk?

* [ ] It stores the boot loader
* [ ] It holds a backup copy of the partition table
* [x] It acts as a container for logical partitions, working around the four-partition limit
* [ ] It extends a filesystem across two disks

> **Explanation:** An extended partition takes one of the four primary slots and does not hold a normal filesystem itself. Logical partitions are created inside it, and only one extended partition is allowed per disk.

#### Q. An MBR disk already has three primary partitions and an extended partition. What number does `fdisk` give the first logical partition?

* [ ] 4
* [x] 5
* [ ] 1
* [ ] 0

> **Explanation:** Numbers 1 to 4 are reserved for primary and extended entries, so logical partitions always start at 5, for example `/dev/sda5`.

#### Q. What happens when you delete an extended partition that contains logical partitions?

* [ ] The logical partitions become primary partitions
* [ ] Only the empty space in it is freed
* [x] All logical partitions inside it are removed too
* [ ] The operation is refused until you convert the disk to GPT

> **Explanation:** Logical partitions are defined inside the extended partition, so removing the container removes them as well. Back up their data before doing this.

#### Q. You want to use the full capacity of a new 4 TB disk as one partition. Why should you choose GPT over MBR?

* [ ] MBR cannot hold Linux filesystems
* [x] MBR is limited to about 2 TB disks (with 512-byte sectors), while GPT supports far larger disks
* [ ] GPT partitions are formatted automatically
* [ ] MBR allows only one partition on disks over 1 TB

> **Explanation:** MBR stores sector addresses in 32-bit fields, which caps it at about 2 TB with 512-byte sectors. GPT removes that limit and also supports many partitions without extended partitions.

#### Q. Which feature makes GPT more robust than MBR?

* [ ] It encrypts the partition table
* [x] It stores a backup partition table and protects it with CRC32 checksums
* [ ] It keeps the partition table in RAM
* [ ] It mirrors every partition to a second disk

> **Explanation:** GPT keeps a primary table at the start of the disk and a backup at the end, both with checksums, so corruption can be detected and repaired. MBR has one unprotected copy in the first sector.

#### Q. On an MBR disk booted by legacy BIOS, what does marking a primary partition as "active" (the boot flag) mean?

* [ ] The partition is currently mounted
* [ ] The partition holds the swap area
* [ ] The partition is encrypted
* [x] It is the partition the firmware's boot code should boot from

> **Explanation:** The boot flag, toggled with `a` in `fdisk`, tells MBR boot code which partition to start. Extended partitions cannot be booted directly.

#### Q. When converting a BIOS-booted disk from MBR to GPT, what does GRUB need on the GPT disk?

* [ ] An extended partition
* [x] A small BIOS boot partition (type code `ef02` in `gdisk`)
* [ ] A FAT32 partition larger than 1 GB
* [ ] A logical partition numbered 5

> **Explanation:** GPT does not guarantee the post-MBR gap that GRUB uses on MBR disks, so a tiny BIOS boot partition holds GRUB's core image. After writing the table, reinstall GRUB with `grub-install`.

#### Q. What does the device name `/dev/sdb` refer to?

* [ ] The second partition on the first disk
* [x] The second SCSI or SATA disk
* [ ] The second virtual disk in KVM
* [ ] The boot partition

> **Explanation:** The letter after `sd` identifies the disk: `a` is the first, `b` the second. Partitions add a number, as in `/dev/sda2`, and KVM virtual disks use `/dev/vdX`.

#### Q. Which device name refers to the second partition on the second SATA disk?

* [ ] `/dev/sda2`
* [ ] `/dev/sdb1`
* [x] `/dev/sdb2`
* [ ] `/dev/sd2b`

> **Explanation:** `sdb` is the second disk and the trailing `2` is the partition number. `/dev/sda2` is the second partition of the first disk.

#### Q. Which device name refers to the first partition on the first NVMe disk?

* [ ] `/dev/nvme0n1`
* [ ] `/dev/sda1`
* [ ] `/dev/nvme1`
* [x] `/dev/nvme0n1p1`

> **Explanation:** NVMe names are controller, namespace and then `p` plus the partition number. `/dev/nvme0n1` is the whole disk.

#### Q. You attach a new SATA disk and it appears as `/dev/sdc`. After you create one partition on it, what is that partition called?

* [ ] `/dev/sdc0`
* [x] `/dev/sdc1`
* [ ] `/dev/sdca`
* [ ] `/dev/sdc-p1`

> **Explanation:** Partition numbers start at 1, so the first partition on `/dev/sdc` is `/dev/sdc1`. The `p` separator is only used when the disk name ends in a digit, such as NVMe.

#### Q. Which command lists disks and their partitions as a tree, with sizes and mount points?

* [ ] `df -h`
* [ ] `mount`
* [x] `lsblk`
* [ ] `du -h`

> **Explanation:** `lsblk` shows every block device, including unmounted partitions and LVM volumes, with `TYPE` and `MOUNTPOINT` columns. `df` lists only mounted filesystems.

#### Q. What does this `lsblk` output tell you?

```text
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0   500G  0 disk
├─sda1   8:1    0    50G  0 part /
└─sda2   8:2    0    50G  0 part /home
```

* [ ] The disk is full
* [ ] `/home` is 500G in size
* [x] About 400G of the disk is not allocated to any partition
* [ ] `sda2` is the boot partition

> **Explanation:** The disk is 500G and its two partitions use 100G, so roughly 400G is unallocated and available for new partitions. `lsblk` does not print free space directly; you infer it.

#### Q. Inside `fdisk`, which command saves your partition changes to the disk and exits?

* [ ] `q`
* [ ] `p`
* [ ] `n`
* [x] `w`

> **Explanation:** `fdisk` keeps changes in memory until you press `w`. `q` quits without saving, which is a safe way to back out, `p` prints the table and `n` creates a partition.

#### Q. While creating a partition in `fdisk`, what should you enter at the "Last sector" prompt to make it 50 GiB?

* [ ] `50G`
* [x] `+50G`
* [ ] `-50G`
* [ ] `50000`

> **Explanation:** A leading `+` gives a size relative to the first sector. A bare number is read as an absolute sector, so `50000` would end the partition at sector 50000, making it only about 23 MiB.

#### Q. Which partitioning tool was designed specifically for GPT disks?

* [x] `gdisk`
* [ ] `fdisk`
* [ ] `lsblk`
* [ ] `resize2fs`

> **Explanation:** `gdisk` is the GPT counterpart of `fdisk`, with commands such as `o` to create a new GPT. Modern `fdisk` also handles GPT, but it started as an MBR tool; `lsblk` and `resize2fs` do not edit partition tables.

#### Q. You just created `/dev/sdb1` with `fdisk`. What must you do before you can store files on it?

* [ ] Nothing, it can be mounted immediately
* [ ] Run `lvcreate` on it
* [ ] Mark it as active
* [x] Create a filesystem on it, for example `mkfs.ext4 /dev/sdb1`

> **Explanation:** A new partition is just raw space. A filesystem must be created on it before it can be mounted and used for files.

#### Q. What does deleting a partition with `fdisk` actually do?

* [ ] Securely overwrites all data in that area
* [ ] Moves the data to the neighbouring partition
* [x] Removes its entry from the partition table and marks the area as free
* [ ] Converts it into unformatted swap space

> **Explanation:** Deletion only removes the table entry. Old data may still be on disk until it is overwritten, so it is not a secure erase, and you should back up anything you need first.

#### Q. You need to shrink the ext4 filesystem on `/dev/sda1` and its partition. In what order should you work?

* [ ] Shrink the partition with `fdisk`, then run `resize2fs`
* [x] Back up, unmount, shrink the filesystem with `resize2fs`, then shrink the partition
* [ ] Run `resize2fs` while mounted, then reboot
* [ ] Delete the partition and run `mkfs.ext4` with a smaller size

> **Explanation:** The filesystem must already fit inside the smaller space before the partition is cut down; doing it the other way round destroys data. When growing, reverse the order: enlarge the partition, then run `resize2fs`.

#### Q. You enlarged the partition `/dev/sda1` into free space. Which command makes its ext4 filesystem use the new space?

* [ ] `fsck -f /dev/sda1`
* [ ] `mkfs.ext4 /dev/sda1`
* [x] `resize2fs /dev/sda1`
* [ ] `tune2fs -l /dev/sda1`

> **Explanation:** Without a size argument, `resize2fs` grows the filesystem to fill its partition. `mkfs.ext4` would erase the data, and `tune2fs -l` only prints superblock information.

#### Q. A partitioning tool reports "Partition in use" when you try to change `/dev/sda1`. What is the usual fix?

* [x] Unmount the partition and close programs using it
* [ ] Run `mkfs` on the partition first
* [ ] Convert the disk to GPT
* [ ] Add the partition to `/etc/fstab`

> **Explanation:** A mounted partition cannot safely be resized or deleted. Unmount it with `umount`, or for system partitions work from a live USB.

#### Q. In what order are the three LVM layers built, from the disk upward?

* [ ] Logical volume, volume group, physical volume
* [x] Physical volume, volume group, logical volume
* [ ] Volume group, physical volume, logical volume
* [ ] Physical volume, logical volume, volume group

> **Explanation:** Disks or partitions become physical volumes, PVs are pooled into a volume group, and logical volumes are carved from the VG. A filesystem then goes on the LV.

#### Q. What is an LVM physical volume (PV)?

* [ ] A logical volume that has been mounted
* [ ] A snapshot of a volume group
* [x] A disk or partition initialized with `pvcreate` for use by LVM
* [ ] The filesystem created on a logical volume

> **Explanation:** A PV is a device such as `/dev/sdb` or `/dev/sdc1` labeled for LVM. It is not mounted directly; it contributes its space to a volume group.

#### Q. What is an LVM volume group (VG)?

* [ ] A group of users allowed to manage LVM
* [x] A storage pool made from one or more physical volumes
* [ ] A single partition on one disk
* [ ] A list of mounted logical volumes

> **Explanation:** A VG combines the capacity of its PVs, so its size is the sum of theirs. Logical volumes are allocated from that pool.

#### Q. Which statement about an LVM logical volume (LV) is true?

* [ ] It must be the same size as one physical disk
* [ ] It can only be used for swap
* [ ] It is a type of extended partition
* [x] It can be formatted and mounted like a partition, and can span several disks in the VG

> **Explanation:** An LV behaves like a partition to the rest of the system, but it is allocated from the VG's pool, so it can use space from several PVs and be resized later.

#### Q. You have two blank disks, `/dev/sdb` and `/dev/sdc`, and want to start building LVM on them. Which command comes first?

* [x] `sudo pvcreate /dev/sdb /dev/sdc`
* [ ] `sudo lvcreate -L 20G -n data TEST`
* [ ] `sudo mkfs.ext4 /dev/sdb`
* [ ] `sudo vgextend TEST /dev/sdc`

> **Explanation:** The devices must be initialized as PVs before they can join a volume group with `vgcreate`. LVs come after the VG, and the filesystem goes on the LV, not on the raw disk.

#### Q. Which command adds the physical volume `/dev/sdd` to the existing volume group `TEST`?

* [ ] `sudo vgcreate TEST /dev/sdd`
* [ ] `sudo pvcreate TEST /dev/sdd`
* [x] `sudo vgextend TEST /dev/sdd`
* [ ] `sudo lvextend TEST /dev/sdd`

> **Explanation:** `vgextend` grows a VG by adding PVs. `vgcreate` would try to make a new group, and `lvextend` resizes logical volumes, not groups.

#### Q. Which command creates a 20 GB logical volume named `vol_name_1` in the volume group `TEST`?

* [ ] `sudo lvcreate -n 20G -L vol_name_1 TEST`
* [ ] `sudo vgcreate -L 20G -n vol_name_1 TEST`
* [ ] `sudo lvcreate TEST vol_name_1 20G`
* [x] `sudo lvcreate -L 20G -n vol_name_1 TEST`

> **Explanation:** `-L` sets the size and `-n` the name, followed by the VG. The new LV appears as `/dev/TEST/vol_name_1`.

#### Q. How are `/dev/TEST/vol_name_1` and `/dev/mapper/TEST-vol_name_1` related?

* [ ] The first is the LV and the second is its snapshot
* [ ] The first is a PV and the second is the VG
* [x] They are two names for the same logical volume
* [ ] The second is a backup copy of the first

> **Explanation:** LVM creates both paths for every LV: `/dev/VG/LV` and the device-mapper name `/dev/mapper/VG-LV`. Either can be used with `mkfs`, `mount` or `/etc/fstab`.

#### Q. What is the difference between `lvextend -L +10G /dev/TEST/data` and `lvextend -L 10G /dev/TEST/data`?

* [ ] There is no difference
* [ ] `+10G` also resizes the filesystem, while `10G` does not
* [ ] `+10G` uses a new disk, while `10G` uses free space in the VG
* [x] `+10G` adds 10 GB to the current size, while `10G` sets the total size to 10 GB

> **Explanation:** A leading `+` is relative. Without it the value is the target size, which `lvextend` refuses if it is smaller than the current size. Filesystem resizing is controlled by `-r`.

#### Q. After `sudo lvextend -L +10G /dev/TEST/vol_name_1`, `df -h` still shows the old size. What is missing?

* [ ] A reboot to reload the partition table
* [ ] Running `vgextend` on the volume group
* [x] Growing the filesystem, for example with `resize2fs`, or using `lvextend -r`
* [ ] Recreating the filesystem with `mkfs.ext4`

> **Explanation:** `lvextend` enlarges only the block device. The filesystem on it must be grown too; `-r` does both steps in one command.

#### Q. A filesystem on an LV is 100% full and `vgs` shows `VFree` as 0. What must you do before you can extend the LV?

* [ ] Run `lvextend -r` anyway, since it allocates space automatically
* [x] Add storage with `pvcreate` and `vgextend`, or free space in the VG
* [ ] Run `vgchange -ay`
* [ ] Create a snapshot of the LV

> **Explanation:** An LV can only grow into free extents in its VG. When `VFree` is 0, add a new PV to the group or remove or shrink other LVs first.

#### Q. In `pvs` output, what does the `PFree` column show?

* [ ] The space used by snapshots
* [ ] The size of the largest LV on that disk
* [ ] The number of free partitions on the disk
* [x] The unallocated space remaining on that physical volume

> **Explanation:** `PSize` is the PV's total size and `PFree` is how much of it no LV uses yet. The volume group equivalent in `vgs` is `VFree`.

#### Q. What is the correct order for safely shrinking an ext4 filesystem on a logical volume?

* [ ] `lvreduce`, then `resize2fs`, then `e2fsck`
* [ ] `lvreduce` while mounted, then reboot
* [x] Unmount, `e2fsck -f`, `resize2fs` to the new size, then `lvreduce`
* [ ] `resize2fs`, then `lvreduce`, both while mounted

> **Explanation:** The filesystem must be checked and shrunk to fit before the LV is reduced; reducing the LV first cuts off data. Back up beforehand and remount and verify afterwards.

#### Q. Why can't you shrink a logical volume that holds an XFS filesystem in the usual way?

* [x] XFS can be grown, even online, but cannot be shrunk in place
* [ ] XFS cannot be used on LVM
* [ ] XFS is read-only once created
* [ ] XFS needs `vgreduce` instead of `lvreduce`

> **Explanation:** XFS supports growing but has no shrink operation. To get a smaller XFS volume you must back up, recreate the filesystem and restore.

#### Q. What happens to the space of a logical volume after `lvremove /dev/TEST/vol_name_1`?

* [ ] It is lost until the disk is repartitioned
* [x] It returns to the volume group as free space
* [ ] It is moved to a snapshot automatically
* [ ] It becomes a new physical volume

> **Explanation:** Removing an LV frees its extents in the VG, which `vgs` shows as `VFree`. Unmount the LV first, and remember its data is gone.

#### Q. How does an LVM snapshot preserve the original state of a logical volume?

* [ ] It copies the whole LV when the snapshot is created
* [x] It uses copy-on-write, keeping old blocks only as they change on the origin
* [ ] It compresses the origin LV into a file
* [ ] It mirrors all writes to a second disk

> **Explanation:** A new snapshot is nearly empty. When a block on the origin is about to change, the old block is saved into the snapshot, so it only needs space for changed data.

#### Q. Which command creates a 1 GB snapshot named `snap1` of `/dev/TEST/vol_name_1`?

* [ ] `sudo lvextend -s 1G snap1 /dev/TEST/vol_name_1`
* [ ] `sudo lvconvert --merge /dev/TEST/vol_name_1 snap1`
* [x] `sudo lvcreate -L 1G -s -n snap1 /dev/TEST/vol_name_1`
* [ ] `sudo vgcreate -s snap1 /dev/TEST/vol_name_1`

> **Explanation:** `lvcreate -s` makes a snapshot of the origin LV, with `-L` reserving space for changed blocks. `lvconvert --merge` is used later to roll back to a snapshot.

#### Q. In `lvs` output, a snapshot's `Data%` reaches 100%. What does that mean?

* [ ] The origin LV is full
* [ ] The snapshot has been merged automatically
* [x] The snapshot ran out of space and is no longer valid
* [ ] The snapshot is ready to be mounted

> **Explanation:** Once the snapshot's space is used up by changed blocks, it can no longer represent the earlier state and becomes invalid. Extend or remove snapshots before they fill, and do not keep them longer than needed.

#### Q. A risky upgrade broke the data on `/dev/TEST/vol_name_1`, which has the snapshot `snap1`. Which command rolls the LV back to the snapshot?

* [ ] `sudo lvremove /dev/TEST/snap1`
* [x] `sudo lvconvert --merge /dev/TEST/snap1`
* [ ] `sudo lvextend -r /dev/TEST/snap1`
* [ ] `sudo vgchange -ay /dev/TEST/snap1`

> **Explanation:** Merging writes the snapshot's preserved state back into the origin. If the origin is in use, the merge happens at the next activation, so unmount it first.

#### Q. Why are LVM snapshots not a replacement for real backups?

* [ ] Snapshots cannot be mounted
* [ ] Snapshots are deleted at every reboot
* [ ] Snapshots only store file names, not data
* [x] Snapshots live on the same storage, so a disk failure can destroy them along with the origin

> **Explanation:** A snapshot depends on the origin LV and sits in the same volume group. Keep separate backups on other storage for disaster recovery.

#### Q. After booting a rescue system, `lvs` lists your logical volumes but they cannot be mounted because they are inactive. Which command activates them?

* [ ] `sudo pvcreate -a`
* [ ] `sudo lvextend -ay`
* [ ] `sudo mount -a`
* [x] `sudo vgchange -ay`

> **Explanation:** `vgchange -ay` activates all logical volumes in all volume groups, creating their device nodes. Check with `lsblk` afterwards, then mount them.

#### Q. Why must you be careful running `pvcreate /dev/sdb`?

* [ ] It immediately mounts the disk
* [x] It writes LVM metadata to the disk and destroys any data already on it
* [ ] It removes the disk from all volume groups
* [ ] It changes the disk's device name

> **Explanation:** `pvcreate` initializes the device for LVM, overwriting what was there. Confirm the device with `lsblk` before running it.

#### Q. In a typical Linux server layout that uses LVM, which part is usually kept as a plain partition rather than a logical volume?

* [ ] `/home`
* [ ] `/var`
* [ ] `/`
* [x] The EFI system partition

> **Explanation:** Firmware must read the EFI system partition (and often `/boot`) directly, without LVM support, so they stay plain partitions. `/`, `/home` and `/var` benefit from LVM's resizing.
