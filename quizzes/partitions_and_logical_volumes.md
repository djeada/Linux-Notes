# Partitions and Logical Volumes Quiz

Notes: [Partitions](../notes/partitions.md), [Logical Volume Management](../notes/logical_volume_management.md)

Check your understanding of MBR and GPT partitioning, partitioning tools, and LVM physical volumes, volume groups, logical volumes and snapshots.

#### Q. What is a disk partition?

* [x] A region of a disk, defined in its partition table, used as a separate block device
* [ ] A directory tree that the kernel gives its own permissions and quota
* [ ] A full copy of the disk that is kept for recovery
* [ ] A special file in `/dev` that stores swap space

> **Explanation:** A partition is a range of sectors described by the partition table, such as `/dev/sda1`. It can hold its own filesystem, swap or an LVM physical volume, and is managed independently of the other partitions.

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

* [ ] It stores the boot loader code and the boot flag
* [ ] It holds a backup copy of the primary partition table
* [x] It acts as a container for logical partitions, working around the four-partition limit
* [ ] It lets one filesystem extend across two physical disks

> **Explanation:** An extended partition takes one of the four primary slots and does not hold a normal filesystem itself. Logical partitions are created inside it, and only one extended partition is allowed per disk.

#### Q. An MBR disk already has three primary partitions and an extended partition. What number does `fdisk` give the first logical partition?

* [ ] 4
* [x] 5
* [ ] 1
* [ ] 0

> **Explanation:** Numbers 1 to 4 are reserved for primary and extended entries, so on Linux logical partitions always start at 5, for example `/dev/sda5`, even when fewer than four primaries exist.

#### Q. What happens when you delete an extended partition that contains logical partitions?

* [ ] The logical partitions become primary partitions
* [ ] Only the empty space in it is freed
* [x] All logical partitions inside it are removed too
* [ ] The operation is refused until you convert the disk to GPT

> **Explanation:** Logical partitions are defined inside the extended partition, so removing the container removes them as well. Back up their data before doing this.

#### Q. You want to use the full capacity of a new 4 TB disk as one partition. Why should you choose GPT over MBR?

* [ ] MBR partitions cannot hold ext4 or other Linux filesystems
* [x] MBR can address only 2 TiB with 512-byte sectors; GPT has no such practical limit
* [ ] GPT partitions are formatted automatically when they are created
* [ ] MBR allows only one partition on any disk larger than 1 TB

> **Explanation:** MBR stores sector addresses in 32-bit fields, capping it at 2 TiB with 512-byte sectors; `fdisk` warns that a DOS table cannot use the rest. GPT removes that limit and needs no extended partitions.

#### Q. Which feature makes GPT more robust than MBR?

* [x] It stores a backup partition table and protects it with CRC32 checksums
* [ ] It encrypts the partition table so it cannot be altered
* [ ] It keeps a copy of the partition table in firmware memory
* [ ] It mirrors every partition onto a second disk automatically

> **Explanation:** GPT keeps a primary header and table at the start of the disk and a backup at the end, both with checksums. If the main header is damaged, `gdisk` reports a CRC error and loads the backup.

#### Q. `gdisk -l` on a GPT disk reports `MBR: protective`. What is the protective MBR for?

* [ ] It holds a second copy of the GPT partition entries
* [ ] It lets the disk keep four primary MBR partitions alongside GPT
* [x] It marks the whole disk as in use so MBR-only tools do not treat it as empty
* [ ] It stores the UEFI boot loader

> **Explanation:** Sector 0 of a GPT disk holds an MBR with a single entry of type `0xEE` covering the disk. Old tools then see one unknown partition instead of free space they might overwrite.

#### Q. On an MBR disk booted by legacy BIOS, what does marking a primary partition as "active" (the boot flag) mean?

* [ ] The partition is currently mounted by the running system
* [ ] The partition holds the swap area used during boot
* [ ] The partition is encrypted and needs a passphrase at boot
* [x] It marks the partition whose boot sector generic MBR boot code should load

> **Explanation:** The boot flag, toggled with `a` in `fdisk`, is read by classic MBR boot code to choose which partition to start. Boot loaders such as GRUB installed in the MBR usually ignore it.

#### Q. When converting a BIOS-booted disk from MBR to GPT, what does GRUB need on the GPT disk?

* [x] A small BIOS boot partition (type code `ef02` in `gdisk`)
* [ ] An extended partition to hold GRUB's files
* [ ] A FAT32 partition of at least 1 GB at the end of the disk
* [ ] A logical partition numbered 5 for the boot code

> **Explanation:** On GPT the sectors after the MBR hold the GPT header and table, so GRUB cannot rely on that gap; a tiny BIOS boot partition holds its core image. After writing the table, reinstall GRUB with `grub-install`.

#### Q. You open an MBR disk whose only partition runs to the last sector. `gdisk` converts it in memory, but `w` aborts with the message below. What is the problem?

```text
Warning! Secondary partition table overlaps the last partition by
33 blocks!
You will need to delete this partition or resize it in another utility.
Aborting write of new partition table.
```

* [ ] The disk is larger than 2 TiB, which MBR cannot convert
* [ ] The partition is still mounted, so its sectors are locked
* [ ] `gdisk` cannot convert MBR disks and `fdisk` must be used
* [x] GPT needs the last 33 sectors for its backup table; shrink the partition first

> **Explanation:** The backup GPT header and entries live at the end of the disk. Shrink the filesystem and partition by at least that much before converting.

#### Q. A KVM virtual machine using virtio disks shows `vda` and `vdb` in `lsblk`. What are they?

* [ ] Volume groups created by LVM
* [ ] Partitions on the first disk
* [ ] Old IDE disks
* [x] The first and second virtual disks

> **Explanation:** Virtio disks in KVM guests are named `/dev/vdX`, just as SCSI/SATA disks are `/dev/sdX`; Xen guests use `/dev/xvdX` and old IDE disks `/dev/hdX`. Partitions add a number, as in `/dev/vda1`.

#### Q. Which device name refers to the second partition on the second SATA disk?

* [x] `/dev/sdb2`
* [ ] `/dev/sda2`
* [ ] `/dev/sdb1`
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

* [ ] The disk is full because both partitions are mounted
* [ ] `/home` is 500G in size because it is on `sda`
* [x] About 400G of the disk is not allocated to any partition
* [ ] `sda2` is the boot partition, since it is listed last

> **Explanation:** The disk is 500G and its two partitions use 100G, so roughly 400G is unallocated and available for new partitions. `lsblk` does not print free space directly; you infer it.

#### Q. Which command shows the unallocated regions of `/dev/sda` together with its partitions?

* [x] `sudo parted /dev/sda print free`
* [ ] `lsblk -f /dev/sda`
* [ ] `sudo blkid /dev/sda`
* [ ] `df -h /dev/sda`

> **Explanation:** `print free` adds "Free Space" rows with their start, end and size. `lsblk -f` and `blkid` show filesystems and UUIDs, and `df` reports usage of mounted filesystems only.

#### Q. `sudo fdisk -l /dev/sdb` prints `Disklabel type: dos`. What does that mean?

* [x] The disk uses an MBR partition table
* [ ] The disk is formatted with a FAT filesystem
* [ ] The disk can only be read by DOS or Windows
* [ ] The disk uses GPT with a legacy boot flag

> **Explanation:** `fdisk` calls the MBR format "dos" (and `parted` calls it "msdos"). A GPT disk shows `Disklabel type: gpt`; the label says nothing about the filesystems inside the partitions.

#### Q. Inside `fdisk`, which command saves your partition changes to the disk and exits?

* [ ] `q`
* [ ] `p`
* [ ] `n`
* [x] `w`

> **Explanation:** `fdisk` keeps changes in memory until you press `w`. `q` quits without saving, which is a safe way to back out, `p` prints the table and `n` creates a partition.

#### Q. While creating a partition in `fdisk` (util-linux 2.39), what should you enter at the "Last sector" prompt to make it 50 GiB?

* [ ] `50G`
* [x] `+50G`
* [ ] `-50G`
* [ ] `50000`

> **Explanation:** A leading `+` gives a size from the first sector. `-50G` instead leaves 50 GiB free at the end, `50000` is an absolute sector (about 23 MiB here), and `50G` without a sign is rejected as out of range.

#### Q. Which partitioning tool was designed specifically for GPT disks?

* [x] `gdisk`
* [ ] `fdisk`
* [ ] `lsblk`
* [ ] `resize2fs`

> **Explanation:** `gdisk` is the GPT counterpart of `fdisk`, with commands such as `o` to create a new GPT. Modern `fdisk` also handles GPT, but it started as an MBR tool; `lsblk` and `resize2fs` do not edit partition tables.

#### Q. You just created `/dev/sdb1` with `fdisk`. What must you do before you can store files on it?

* [x] Create a filesystem on it, for example `mkfs.ext4 /dev/sdb1`
* [ ] Nothing, it can be mounted immediately with `mount`
* [ ] Run `lvcreate` on it to make it usable
* [ ] Mark it as active with the `a` command in `fdisk`

> **Explanation:** A new partition is just raw space. A filesystem must be created on it before it can be mounted and used for files.

#### Q. You run `sudo parted -s /dev/sdb mklabel gpt mkpart data ext4 1MiB 100%`. Can you now mount `/dev/sdb1` as ext4?

* [ ] Yes, the `ext4` argument made `mkpart` format the partition
* [x] No, `ext4` is only a type hint; you still need `mkfs.ext4 /dev/sdb1`
* [ ] Yes, but only after running `resize2fs` to fill the partition
* [ ] No, GPT partitions cannot hold ext4, only FAT32 or XFS

> **Explanation:** The `fs-type` argument of `mkpart` sets the partition type and creates no filesystem, so `blkid` finds nothing on it. Note that `mklabel` also replaces any existing partition table.

#### Q. What does deleting a partition with `fdisk` actually do?

* [ ] Securely overwrites all data in that area with zeros
* [ ] Moves its data into the neighbouring partition first
* [x] Removes its entry from the partition table and marks the area as free
* [ ] Converts the area into unformatted swap space

> **Explanation:** Deletion only removes the table entry. Old data may still be on disk until it is overwritten, so it is not a secure erase, and you should back up anything you need first.

#### Q. To grow `/dev/sdb1` with `fdisk`, you delete it and create a larger partition 1. `fdisk` then reports "Partition #1 contains a ext4 signature". What must you get right to keep the data?

* [ ] Start the new partition at the next free sector and remove the signature
* [ ] Choose a different partition number so the old one is not overwritten
* [ ] Run `mkfs.ext4` on the new partition before writing the table
* [x] Start it at exactly the same first sector and keep the signature

> **Explanation:** The filesystem begins at the old start sector, so the new entry must start there and only end later. Removing the signature erases the ext4 magic, so the filesystem is no longer recognized. After `w`, run `resize2fs`.

#### Q. You need to shrink the ext4 filesystem on `/dev/sda1` and its partition. In what order should you work?

* [x] Back up, unmount, shrink the filesystem with `resize2fs`, then shrink the partition
* [ ] Shrink the partition with `fdisk`, then run `resize2fs`
* [ ] Run `resize2fs` while mounted, then reboot
* [ ] Delete the partition and run `mkfs.ext4` with a smaller size

> **Explanation:** The filesystem must already fit inside the smaller space before the partition is cut down; doing it the other way round destroys data. ext4 can only be shrunk unmounted. When growing, reverse the order.

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

#### Q. What does the final `2` in this `/etc/fstab` line mean?

```text
UUID=3f1c8a2e-5b7d-4c11-9e0a-2d6f8b1c4e77  /mnt/data  ext4  defaults  0  2
```

* [ ] Wait two seconds after boot before mounting the filesystem
* [ ] Keep two backup copies of the filesystem with `dump`
* [ ] The filesystem is on the second partition of its disk
* [x] `fsck` checks it at boot after the root filesystem, which uses `1`

> **Explanation:** The sixth field is `fs_passno`: `1` for root, `2` for other filesystems, `0` for no check. The fifth field (`0`) is the old `dump` flag. Test new entries with `sudo mount -a` before rebooting.

#### Q. Why do `/etc/fstab` entries usually use `UUID=` instead of names like `/dev/sdb1`?

* [x] Names like `/dev/sdb1` can change between boots, while the UUID stays the same
* [ ] UUIDs let the kernel mount the filesystem faster at boot
* [ ] Plain device names like `/dev/sdb1` are rejected in `/etc/fstab`
* [ ] The UUID entry makes the filesystem encrypted at rest

> **Explanation:** The UUID is stored in the filesystem itself, so it identifies the same filesystem wherever the disk appears. Find it with `blkid` or `lsblk -f`.

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

> **Explanation:** A VG combines the capacity of its PVs, so its size is roughly the sum of theirs minus a little metadata. Logical volumes are allocated from that pool.

#### Q. Which statement about an LVM logical volume (LV) is true?

* [ ] It must be exactly the same size as one of the physical disks
* [ ] It can only be used for swap, not for regular filesystems
* [ ] It is a type of extended partition stored in the MBR
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

#### Q. Which command creates a 20 GiB logical volume named `vol_name_1` in the volume group `TEST`?

* [ ] `sudo lvcreate -n 20G -L vol_name_1 TEST`
* [ ] `sudo vgcreate -L 20G -n vol_name_1 TEST`
* [ ] `sudo lvcreate TEST vol_name_1 20G`
* [x] `sudo lvcreate -L 20G -n vol_name_1 TEST`

> **Explanation:** `-L` sets the size (LVM's `G` means GiB) and `-n` the name, followed by the VG. The new LV appears as `/dev/TEST/vol_name_1`.

#### Q. How are `/dev/TEST/vol_name_1` and `/dev/mapper/TEST-vol_name_1` related?

* [ ] The first is the LV and the second is its snapshot
* [ ] The first is a PV and the second is the VG
* [x] They are two names for the same logical volume
* [ ] The second is a backup copy of the first

> **Explanation:** Both point to the same device-mapper device. LVM documents `/dev/VG/LV` as the stable name for scripts, because the `/dev/mapper` format is meant for internal use and escapes some characters.

#### Q. An Ubuntu server shows the device `/dev/mapper/ubuntu--vg-ubuntu--lv`. What are the volume group and logical volume names?

* [ ] VG `ubuntu`, LV `vg-ubuntu--lv`
* [ ] VG `ubuntu--vg`, LV `ubuntu--lv`
* [x] VG `ubuntu-vg`, LV `ubuntu-lv`
* [ ] VG `ubuntu-vg-ubuntu`, LV `lv`

> **Explanation:** In `/dev/mapper` names a single hyphen separates VG from LV, and hyphens inside the names are doubled. `dmsetup splitname` decodes it, and `/dev/ubuntu-vg/ubuntu-lv` is the same device.

#### Q. What is the difference between `lvextend -L +10G /dev/TEST/data` and `lvextend -L 10G /dev/TEST/data`?

* [ ] There is no difference
* [ ] `+10G` also resizes the filesystem, while `10G` does not
* [ ] `+10G` uses a new disk, while `10G` uses free space in the VG
* [x] `+10G` adds 10 GiB to the current size, while `10G` sets the total size to 10 GiB

> **Explanation:** A leading `+` is relative. Without it the value is the target size, which `lvextend` refuses if it is not larger than the current size. Filesystem resizing is controlled by `-r`.

#### Q. After `sudo lvextend -L +10G /dev/TEST/vol_name_1`, `df -h` still shows the old size. What is missing?

* [ ] A reboot, so the kernel reloads the partition table
* [ ] Running `vgextend` so the volume group grows too
* [x] Growing the filesystem, for example with `resize2fs`, or using `lvextend -r`
* [ ] Recreating the filesystem with `mkfs.ext4` at the new size

> **Explanation:** `lvextend` enlarges only the block device. The filesystem on it must be grown too; `-r` does both steps in one command.

#### Q. A filesystem on an LV is 100% full and `vgs` shows `VFree` as 0. What must you do before you can extend the LV?

* [x] Add storage with `pvcreate` and `vgextend`, or free space in the VG
* [ ] Run `lvextend -r` anyway, since it allocates space automatically
* [ ] Run `vgchange -ay`
* [ ] Create a snapshot of the LV

> **Explanation:** An LV can only grow into free extents in its VG. When `VFree` is 0, add a new PV to the group or remove or shrink other LVs first.

#### Q. In a VG with the default 4 MiB extent size, `lvextend` fails with the message below. About how much free space does the VG have?

```text
Insufficient free space: 1280 extents needed, but only 129 available
```

* [ ] 129 MiB
* [x] 516 MiB
* [ ] 1280 MiB
* [ ] 5 GiB

> **Explanation:** LVM allocates in physical extents, so the free space is $129 \times 4\ \text{MiB} = 516\ \text{MiB}$. The request needed $1280 \times 4\ \text{MiB} = 5\ \text{GiB}$, which is what `-L +5G` asks for.

#### Q. In `pvs` output, what does the `PFree` column show?

* [ ] The space used by snapshots
* [ ] The size of the largest LV on that disk
* [ ] The number of free partitions on the disk
* [x] The unallocated space remaining on that physical volume

> **Explanation:** `PSize` is the PV's total size and `PFree` is how much of it no LV uses yet. The volume group equivalent in `vgs` is `VFree`.

#### Q. `lvs` shows the attribute string `-wi-ao----` for the LV `data`. What does the `o` in the sixth position mean?

* [ ] The LV is the origin of a snapshot and cannot be removed
* [x] The device is open, for example because its filesystem is mounted
* [ ] The LV is owned by root and other users cannot open it
* [ ] The LV is offline and must be activated before use

> **Explanation:** In `lv_attr`, position 5 `a` means active and position 6 `o` means open. An origin LV is shown by an `o` in the first position instead, as in `owi-a-s---`.

#### Q. What is the correct order for safely shrinking an ext4 filesystem on a logical volume?

* [ ] `lvreduce`, then `resize2fs`, then `e2fsck`
* [ ] `lvreduce` while mounted, then reboot
* [x] Unmount, `e2fsck -f`, `resize2fs` to the new size, then `lvreduce`
* [ ] `resize2fs`, then `lvreduce`, both while mounted

> **Explanation:** The filesystem must be checked and shrunk to fit before the LV is reduced; reducing the LV first cuts off data. `lvreduce -r` performs the filesystem step for you. Back up beforehand.

#### Q. Why can't you shrink a logical volume that holds an XFS filesystem in the usual way?

* [x] XFS can be grown, and only while mounted, but has no general way to shrink
* [ ] XFS cannot be placed on LVM logical volumes at all
* [ ] XFS becomes read-only once it has been created
* [ ] XFS must be shrunk with `vgreduce` instead of `lvreduce`

> **Explanation:** `xfs_growfs` enlarges a mounted XFS filesystem, but XFS offers no normal shrink operation. To get a smaller XFS volume you back up, recreate the filesystem and restore.

#### Q. What happens to the space of a logical volume after `lvremove /dev/TEST/vol_name_1`?

* [ ] It is lost until the disk is repartitioned
* [x] It returns to the volume group as free space
* [ ] It is moved to a snapshot automatically
* [ ] It becomes a new physical volume

> **Explanation:** Removing an LV frees its extents in the VG, which `vgs` shows as `VFree`. Unmount the LV first, and remember its data is gone.

#### Q. You want to take the disk `/dev/sdb` out of the volume group `TEST` while its LVs stay online. Which sequence works, assuming the other PVs have enough free space?

* [ ] `lvremove` every LV, then `pvremove /dev/sdb`
* [x] `pvmove /dev/sdb`, then `vgreduce TEST /dev/sdb`
* [ ] `vgreduce TEST /dev/sdb`, then `pvmove /dev/sdb`
* [ ] `pvremove /dev/sdb`, then `vgextend TEST`

> **Explanation:** `pvmove` relocates the allocated extents to other PVs in the VG while the LVs stay in use. Only an empty PV can be removed with `vgreduce`, after which `pvremove` can wipe its label.

#### Q. You are dismantling a lab LVM setup with one LV on one VG. In what order do you remove the pieces after unmounting?

* [x] `lvremove`, `vgremove`, `pvremove`
* [ ] `pvremove`, `vgremove`, `lvremove`
* [ ] `vgremove`, `lvremove`, `pvremove`
* [ ] `lvremove`, `pvremove`, `vgremove`

> **Explanation:** Teardown reverses creation: remove the LVs, then the now-empty VG, then the LVM labels on the PVs. `pvremove` normally refuses a PV that still belongs to a VG.

#### Q. How does an LVM snapshot preserve the original state of a logical volume?

* [ ] It copies the whole LV when the snapshot is created
* [x] It uses copy-on-write, keeping old blocks only as they change on the origin
* [ ] It compresses the origin LV into a file
* [ ] It mirrors all writes to a second disk

> **Explanation:** A new snapshot is nearly empty. When a block on the origin is about to change, the old block is saved into the snapshot, so it only needs space for changed data.

#### Q. Which command creates a 1 GiB snapshot named `snap1` of `/dev/TEST/vol_name_1`?

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

> **Explanation:** Once the snapshot's space is used up by changed blocks, it can no longer represent the earlier state and is marked invalid (`I` in its attributes). The origin LV keeps working.

#### Q. A snapshot you still need shows `Data%` at 85% and the origin keeps changing. What should you do?

* [ ] Run `lvreduce` on the origin to slow down changes
* [ ] Run `resize2fs` on the snapshot
* [ ] Nothing, LVM deletes old blocks from the snapshot when it fills
* [x] Give it more COW space with `lvextend -L +1G` on the snapshot LV

> **Explanation:** Extending a copy-on-write snapshot adds room for changed blocks, and automatic extension can be configured. Size snapshots for the writes you expect and remove them when done.

#### Q. To test snapshot exhaustion, you run `fallocate -l 200M bigfile` on the ext4 origin of a 50 MiB snapshot, but the snapshot's `Data%` barely moves. Why?

* [x] `fallocate` reserves blocks as unwritten extents without writing data, so few origin blocks change
* [ ] Snapshots only record changes to files that existed when the snapshot was created
* [ ] ext4 writes new files into the snapshot instead of the origin
* [ ] `Data%` is only updated after the origin is unmounted

> **Explanation:** A COW snapshot fills only when blocks on the origin are overwritten. `fallocate` updates a little metadata; writing real data, for example with `dd if=/dev/urandom ... conv=fsync`, fills the snapshot.

#### Q. A risky upgrade broke the data on `/dev/TEST/vol_name_1`, which has the snapshot `snap1`. Which command rolls the LV back to the snapshot?

* [ ] `sudo lvremove /dev/TEST/snap1`
* [x] `sudo lvconvert --merge /dev/TEST/snap1`
* [ ] `sudo lvextend -r /dev/TEST/snap1`
* [ ] `sudo vgchange -ay /dev/TEST/snap1`

> **Explanation:** Merging writes the snapshot's preserved state back into the origin and then removes the snapshot. If the origin or snapshot is open, the merge waits until both are closed and the LV is next activated, so unmount first.

#### Q. Why are LVM snapshots not a replacement for real backups?

* [ ] Snapshots cannot be mounted, so files cannot be restored
* [ ] Snapshots are deleted automatically at every reboot
* [ ] Snapshots only store file names and metadata, not data
* [x] Snapshots live in the same VG as the origin, so a disk failure can destroy both

> **Explanation:** A snapshot depends on the origin LV and sits in the same volume group. Keep separate backups on other storage for disaster recovery.

#### Q. After booting a rescue system, `lvs` lists your logical volumes but they cannot be mounted because they are inactive. Which command activates them?

* [ ] `sudo pvcreate -a`
* [ ] `sudo lvextend -ay`
* [ ] `sudo mount -a`
* [x] `sudo vgchange -ay`

> **Explanation:** `vgchange -ay` activates all logical volumes in all volume groups, creating their device nodes. Check with `lsblk` afterwards, then mount them.

#### Q. Why must you be careful running `pvcreate /dev/sdb`?

* [ ] It immediately mounts the disk under `/dev/mapper`
* [x] It overwrites the start of the disk, wiping its partition table or filesystem
* [ ] It removes the disk from every volume group it belongs to
* [ ] It renames the disk's device node to an LVM name

> **Explanation:** `pvcreate` initializes the device for LVM, overwriting what was at its start; `-f` or `-y` suppress its confirmation prompts. Confirm the device with `lsblk` before running it.

#### Q. In a typical Linux server layout that uses LVM, which part is usually kept as a plain partition rather than a logical volume?

* [ ] `/home`
* [ ] `/var`
* [ ] `/`
* [x] The EFI system partition

> **Explanation:** Firmware must read the EFI system partition (and often `/boot`) directly, without LVM support, so they stay plain partitions. `/`, `/home` and `/var` benefit from LVM's resizing.
