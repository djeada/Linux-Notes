## Disk Partitions, Volumes, and LVM

Storage devices such as HDDs, SSDs, USB drives, and virtual disks provide raw space. Before that space can be used conveniently, it usually needs to be divided, organized, formatted, and mounted.

Linux storage can be understood in layers.

```text id="0cdghx"
Physical disk
    |
    v
Partition
    |
    v
Filesystem
    |
    v
Mount point
    |
    v
Usable files and directories
```

With LVM, there are extra layers that make storage more flexible.

```text id="i9g5w5"
Physical disk or partition
    |
    v
Physical Volume, PV
    |
    v
Volume Group, VG
    |
    v
Logical Volume, LV
    |
    v
Filesystem
    |
    v
Mount point
```

The main idea is that normal partitions are relatively fixed, while LVM gives you a flexible storage pool that can be expanded, resized, and organized more easily.

### Partitions

A partition is a section of a storage device.

A physical disk can be divided into multiple partitions. Each partition can be used for a different purpose.

For example, a disk might contain:

```text id="vcg6dp"
/boot       boot files
/           root filesystem
/home       user files
swap        swap space
```

A simple partition layout might look like this:

```text id="mkpsql"
Disk: /dev/sda
+-------------+----------------+----------------+
| /dev/sda1   | /dev/sda2      | /dev/sda3      |
| /boot       | /              | /home          |
| 1G          | 40G            | 200G           |
+-------------+----------------+----------------+
```

Partitions are useful because they separate storage into independent regions. This can help with organization, booting, security, backups, and system recovery.

### Partition Tables

A partition table describes how a disk is divided into partitions.

The two most common partition table types are:

```text id="o5mj7h"
MBR
GPT
```

MBR is older. GPT is newer and more common on modern systems.

### MBR Partitions

MBR stands for Master Boot Record.

MBR has an important limitation: it supports only four primary partitions.

To work around this, MBR uses extended and logical partitions.

```text id="24naqi"
MBR Disk
+-------------+-------------+-------------------------------+
| Primary 1   | Primary 2   | Extended Partition            |
|             |             | +----------+ +-------------+  |
|             |             | | Logical  | | Logical     |  |
|             |             | | Part 1   | | Part 2      |  |
|             |             | +----------+ +-------------+  |
+-------------+-------------+-------------------------------+
```

The extended partition is a container. It does not directly hold a filesystem in the normal way. Instead, it contains logical partitions.

Important point:

```text id="4gca51"
Primary, extended, and logical partitions are mainly MBR concepts.
```

### GPT Partitions

GPT stands for GUID Partition Table.

GPT is the modern partitioning scheme. It avoids many MBR limitations.

With GPT:

* No need for extended partitions
* No need for logical partitions
* Supports many partitions
* Better support for large disks
* More robust partition metadata

A GPT disk looks simpler conceptually:

```text id="5g14j7"
GPT Disk
+-------------+-------------+-------------+-------------+
| Partition 1 | Partition 2 | Partition 3 | Partition 4 |
+-------------+-------------+-------------+-------------+
```

On modern Linux systems, GPT is usually preferred unless there is a specific compatibility reason to use MBR.

### Volumes

A volume is a usable storage area that can contain a filesystem.

A volume may be a simple partition, such as:

```text id="1bka8y"
/dev/sda1
```

or it may be a logical volume created by LVM, such as:

```text id="p4eqkv"
/dev/vg_data/lv_home
```

The important difference is that a partition is tied directly to a section of one disk, while a logical volume can be created from a flexible storage pool.

### Partition vs Volume

A partition is a physical division of a disk.

A volume is a usable storage unit that usually contains a filesystem.

A simple partition-based setup looks like this:

```text id="qxj8yp"
Disk
 |
 +--> Partition
        |
        +--> Filesystem
               |
               +--> Mount point
```

An LVM-based setup looks like this:

```text id="lyc3ci"
Disk or partition
 |
 +--> Physical Volume
        |
        +--> Volume Group
               |
               +--> Logical Volume
                      |
                      +--> Filesystem
                             |
                             +--> Mount point
```

In everyday use, both a partition and a logical volume can be formatted and mounted.

The difference is in how flexible they are to manage.

### Why Use LVM?

LVM stands for Logical Volume Manager.

LVM allows Linux systems to manage storage more flexibly than traditional partitions.

With LVM, you can:

* Combine multiple disks into one storage pool
* Create logical volumes from that pool
* Extend logical volumes when more space is needed
* Reduce some logical volumes carefully
* Move data between disks
* Create snapshots
* Add new disks to existing storage
* Manage storage using meaningful names

For example, instead of being locked into a fixed `/home` partition size, you could create a logical volume for `/home` and expand it later if users need more space.

### LVM Big Picture

LVM has three main layers:

```text id="t88t39"
Physical Volume, PV
Volume Group, VG
Logical Volume, LV
```

A physical volume is a disk or partition prepared for LVM.

A volume group is a pool of storage made from one or more physical volumes.

A logical volume is a usable storage unit created inside a volume group.

```text id="qjgo5p"
|-----------------|     |-----------------|     |-----------------|
| Physical Volume |     | Physical Volume |     | Physical Volume |
| PV: /dev/sdb    |     | PV: /dev/sdc    |     | PV: /dev/sdd    |
| Size: 50G       |     | Size: 100G      |     | Size: 150G      |
|-----------------|     |-----------------|     |-----------------|
        |                       |                       |
        +-----------------------+-----------------------+
                                |
                                v
|------------------------------------------------------------------|
|                      Volume Group: TEST                          |
|                        Total Size: 300G                          |
|                                                                  |
|  |------------------|     |------------------|                   |
|  | Logical Volume   |     | Logical Volume   |   Free Space      |
|  | vol_name_1       |     | vol_name_2       |   30G             |
|  | Size: 180G       |     | Size: 90G        |                   |
|  |------------------|     |------------------|                   |
|                                                                  |
|------------------------------------------------------------------|
```

This means:

* `/dev/sdb`, `/dev/sdc`, and `/dev/sdd` are physical volumes
* They are combined into a volume group named `TEST`
* Logical volumes are created from space inside `TEST`
* Unused space remains available for future expansion

### Physical Volumes

A physical volume, or PV, is a disk or partition initialized for use by LVM.

Examples:

```text id="3cyrh2"
/dev/sdb
/dev/sdc1
/dev/nvme1n1p3
```

A PV is not normally mounted directly. Instead, it becomes part of a volume group.

To create a physical volume:

```bash id="nu316t"
sudo pvcreate /dev/sdb
```

To view physical volumes:

```bash id="gj0cxr"
sudo pvs
```

Example output:

```text id="za6lbx"
PV         VG      Fmt  Attr PSize   PFree
/dev/sdb   TEST    lvm2 a--   50.00g  0
/dev/sdc   TEST    lvm2 a--  100.00g 10.00g
/dev/sdd   TEST    lvm2 a--  150.00g 20.00g
```

Interpretation:

| Field     | Description                    |
| --------- | ------------------------------ |
| **PV**    | Physical volume device         |
| **VG**    | Volume group the PV belongs to |
| **PSize** | Total size of the PV           |
| **PFree** | Unused space on that PV        |

### Volume Groups

A volume group, or VG, is a storage pool made from one or more physical volumes.

Example:

```text id="m6cq7o"
TEST
```

A VG combines the capacity of all physical volumes assigned to it.

To create a volume group:

```bash id="pn0z5s"
sudo vgcreate TEST /dev/sdb
```

To add more physical volumes to an existing volume group:

```bash id="08y4yx"
sudo vgextend TEST /dev/sdc /dev/sdd
```

To view volume groups:

```bash id="km21ed"
sudo vgs
```

Example output:

```text id="pyui0x"
VG     #PV #LV #SN Attr   VSize    VFree
TEST     3   2   0 wz--n- 300.00g  30.00g
```

Interpretation:

| Field     | Description                             |
| --------- | --------------------------------------- |
| **#PV**   | Number of physical volumes in the group |
| **#LV**   | Number of logical volumes in the group  |
| **VSize** | Total size of the volume group          |
| **VFree** | Unused space still available            |

The `VFree` value is important. It tells you how much space is available for new logical volumes or for extending existing ones.

### Logical Volumes

A logical volume, or LV, is the usable storage area created inside a volume group.

It behaves much like a partition. You can format it, mount it, and store files on it.

Examples:

```text id="u3qj80"
/dev/TEST/vol_name_1
/dev/mapper/TEST-vol_name_1
```

Both paths usually refer to the same logical volume.

To create a logical volume:

```bash id="s90apv"
sudo lvcreate -L 20G -n vol_name_1 TEST
```

This creates a 20 GB logical volume named `vol_name_1` inside the volume group `TEST`.

To view logical volumes:

```bash id="j2wq5w"
sudo lvs
```

Example output:

```text id="ijxuao"
LV          VG    Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
vol_name_1  TEST  -wi-a----- 180.00g
vol_name_2  TEST  -wi-a-----  90.00g
```

Interpretation:

| Field     | Description         |
| --------- | ------------------- |
| **LV**    | Logical volume name |
| **VG**    | Volume group name   |
| **LSize** | Logical volume size |
| **Attr**  | Volume attributes   |

### Filesystems on Logical Volumes

A logical volume is not ready for normal file storage until it has a filesystem.

For example, to create an ext4 filesystem:

```bash id="r9f5st"
sudo mkfs.ext4 /dev/TEST/vol_name_1
```

Then create a mount point:

```bash id="qjr6ul"
sudo mkdir -p /mnt/mydata
```

Mount it:

```bash id="1bd3v0"
sudo mount /dev/TEST/vol_name_1 /mnt/mydata
```

Check it:

```bash id="of75xj"
df -h /mnt/mydata
```

Example output:

```text id="c2vwf8"
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/TEST-vol_name_1    20G   24K   19G   1% /mnt/mydata
```

Interpretation:

```text id="s7swty"
The logical volume is formatted, mounted, and usable.
Files written to /mnt/mydata are stored on the LV.
```

### LVM Naming

LVM names usually follow this pattern:

```text id="c8fztx"
/dev/VOLUME_GROUP/LOGICAL_VOLUME
```

Example:

```text id="js0tgy"
/dev/TEST/vol_name_1
```

Linux may also show the same LV under `/dev/mapper`:

```text id="pyfv2n"
/dev/mapper/TEST-vol_name_1
```

Both refer to the same logical volume.

### Basic LVM Creation Workflow

A full LVM setup usually follows this order:

1. Identify disks or partitions
2. Create physical volumes
3. Create a volume group
4. Create logical volumes
5. Create filesystems
6. Create mount points
7. Mount logical volumes
8. Optionally configure /etc/fstab

Example:

```bash id="t8u1ps"
sudo pvcreate /dev/sdb /dev/sdc /dev/sdd
sudo vgcreate TEST /dev/sdb
sudo vgextend TEST /dev/sdc /dev/sdd

sudo lvcreate -L 20G -n vol_name_1 TEST
sudo lvcreate -L 12G -n vol_name_2 TEST

sudo mkfs.ext4 /dev/TEST/vol_name_1
sudo mkdir -p /mnt/vol1
sudo mount /dev/TEST/vol_name_1 /mnt/vol1
```

### Extending a Logical Volume

One of the biggest advantages of LVM is that logical volumes can be extended.

If the volume group has free space, you can increase an LV size.

Example:

```bash id="vz5bqk"
sudo lvextend -L +10G /dev/TEST/vol_name_1
```

This adds 10 GB to the logical volume.

However, the filesystem also needs to be expanded.

For ext4:

```bash id="ve7wh0"
sudo resize2fs /dev/TEST/vol_name_1
```

A more convenient method is to use `-r`, which resizes the filesystem automatically:

```bash id="njys9d"
sudo lvextend -r -L +10G /dev/TEST/vol_name_1
```

This is often safer and simpler because it handles both steps:

```text id="ynm3xj"
extend LV
resize filesystem
```

### Reducing a Logical Volume

Reducing a logical volume is more dangerous than extending it.

If done incorrectly, it can destroy data.

The safe order for ext4 is:

1. Back up important data
2. Unmount the filesystem
3. Check the filesystem
4. Shrink the filesystem
5. Shrink the logical volume
6. Mount again
7. Verify data

Example:

```bash id="r6m3qk"
sudo umount /dev/TEST/vol_name_1
sudo e2fsck -f /dev/TEST/vol_name_1
sudo resize2fs /dev/TEST/vol_name_1 15G
sudo lvreduce -L 15G /dev/TEST/vol_name_1
sudo mount /dev/TEST/vol_name_1 /mnt/vol1
```

Important warning:

```text id="kljxcr"
Do not reduce an LV before reducing the filesystem.
The filesystem must fit inside the smaller LV.
```

For some filesystems, such as XFS, shrinking is not supported. XFS can be grown online but not shrunk in place.

### Deleting a Logical Volume

To delete a logical volume, first unmount it.

```bash id="lz3cao"
sudo umount /mnt/vol1
```

Then remove it:

```bash id="f74ok8"
sudo lvremove /dev/TEST/vol_name_1
```

LVM will ask for confirmation.

After removal, the space returns to the volume group as free space.

Check with:

```bash id="hf682z"
sudo vgs
```

### LVM Snapshots

An LVM snapshot captures the state of a logical volume at a point in time.

Snapshots are useful for:

* Temporary backups
* Consistent backup windows
* Testing risky changes
* Rollback scenarios
* Capturing a filesystem state before updates

A snapshot does not immediately copy all data. Instead, it uses copy-on-write behavior. When data changes on the original LV, the snapshot keeps the old blocks so it can preserve the earlier state.

```text id="ghg06l"
Original LV before snapshot
        |
        v
Snapshot created
        |
        v
Changes happen on original LV
        |
        v
Snapshot preserves old data blocks
```

Create a snapshot:

```bash id="t6nf0v"
sudo lvcreate -L 1G -s -n snap_vol_name_1 /dev/TEST/vol_name_1
```

This creates a 1 GB snapshot named `snap_vol_name_1`.

View snapshots:

```bash id="swwppg"
sudo lvs
```

Example output:

```text id="bqskbg"
LV               VG    Attr       LSize  Origin      Data%
snap_vol_name_1  TEST  swi-a-s---  1.00g vol_name_1  12.00
vol_name_1       TEST  owi-a-s--- 20.00g
```

Interpretation:

* `snap_vol_name_1` is a snapshot of `vol_name_1`
* `Data%` shows how much of the snapshot space is used
* If `Data%` reaches `100%`, the snapshot becomes invalid

### Restoring from a Snapshot

To merge a snapshot back into the original logical volume:

```bash id="lmqcrk"
sudo lvconvert --merge /dev/TEST/snap_vol_name_1
```

The merge may happen immediately or at the next activation, depending on whether the origin volume is active.

A common safe workflow is:

* Create snapshot
* Make changes
* If changes are bad, unmount original LV
* Merge snapshot
* Reactivate LV
* Mount again

Snapshots are useful, but they are not a full backup replacement. If the disk fails, snapshots on the same disk may be lost too.

### Persistent Mounting with `/etc/fstab`

If you want an LV mounted automatically at boot, add it to `/etc/fstab`.

Example:

```text id="chccnp"
/dev/TEST/vol_name_1   /mnt/vol1   ext4   defaults   0   2
```

A more robust option is to use a UUID.

Find the UUID:

```bash id="o1d33n"
sudo blkid /dev/TEST/vol_name_1
```

Example:

```text id="j8yyrg"
/dev/TEST/vol_name_1: UUID="1111-2222" TYPE="ext4"
```

Then use:

```text id="brmwfk"
UUID=1111-2222   /mnt/vol1   ext4   defaults   0   2
```

Test `/etc/fstab` before rebooting:

```bash id="nq1p58"
sudo mount -a
```

### Partition Types Compared

Primary partition:

- traditional partition type, especially on MBR disks
- can contain a filesystem or bootable OS files
- MBR supports up to 4 primary partitions

Extended partition:

- MBR-only container used to work around the 4-partition limit
- does not directly store normal data
- contains logical partitions

Logical partition:

- created inside an extended partition on MBR disks
- can contain a filesystem
- used when more than 4 partitions are needed

LVM logical volume:

- flexible virtual storage unit created inside a volume group
- can be resized more easily
- can span multiple disks through the volume group
- supports snapshots and advanced management

Modern note:

```text id="pbxug1"
On GPT disks, primary/extended/logical partition limits are mostly not relevant.
GPT supports many normal partitions without extended partitions.
```

### When to Use Partitions vs LVM

Use normal partitions when:

* The layout is simple
* The system is small
* You do not need resizing flexibility
* You want easier recovery with minimal layers
* You are creating simple boot or EFI partitions

Use LVM when:

* Storage may grow later
* You need flexible resizing
* You want to combine disks into a pool
* You want snapshots
* You manage servers or virtual machines
* You want meaningful volume names

A common Linux server layout might use both:

```text id="e1i8fk"
/boot      normal partition
/boot/efi  EFI system partition
/          LVM logical volume
/home      LVM logical volume
/var       LVM logical volume
```

### Useful LVM Commands

| Command     | Description                         |
| ----------- | ----------------------------------- |
| `pvs`       | Show physical volumes               |
| `pvdisplay` | Detailed physical volume info       |
| `vgs`       | Show volume groups                  |
| `vgdisplay` | Detailed volume group info          |
| `lvs`       | Show logical volumes                |
| `lvdisplay` | Detailed logical volume info        |
| `lsblk`     | Show block devices and mount points |
| `lsblk -f`  | Show filesystems and UUIDs          |
| `df -h`     | Show mounted filesystem usage       |
| `blkid`     | Show UUID and filesystem type       |

Creation commands:

* `pvcreate /dev/sdb`
* `vgcreate TEST /dev/sdb`
* `vgextend TEST /dev/sdc`
* `lvcreate -L 20G -n vol_name_1 TEST`
* `mkfs.ext4 /dev/TEST/vol_name_1`
* `mount /dev/TEST/vol_name_1 /mnt/vol1`

Resize commands:

```bash id="rhvt1x"
lvextend -r -L +10G /dev/TEST/vol_name_1
resize2fs /dev/TEST/vol_name_1
lvreduce -L 15G /dev/TEST/vol_name_1
```

Snapshot commands:

```bash id="u7lwx1"
lvcreate -L 1G -s -n snap_vol_name_1 /dev/TEST/vol_name_1
lvconvert --merge /dev/TEST/snap_vol_name_1
```

Removal commands:

```bash id="mhcy2x"
umount /mnt/vol1
lvremove /dev/TEST/vol_name_1
vgremove TEST
pvremove /dev/sdb
```

### Safe LVM Lab Setup Using Loopback Disks

The following lab simulates disks using regular files.

This is safer than practicing on real disks because it avoids accidentally destroying real data.

Important warning:

* These commands still use `sudo` and create block devices
* Run them only on a test machine or lab VM
* Carefully copy device names
* Do not use real disks such as `/dev/sda` unless you intend to erase them

### Scenario 1: Create a Complete LVM Setup in a Lab

#### Goal

Simulate three disks, create LVM physical volumes, combine them into one volume group, create a logical volume, format it, mount it, and verify that it works.

#### Step 1: Create Test Disk Files

```bash id="yzevim"
mkdir -p ~/lvm-lab

truncate -s 1G ~/lvm-lab/disk1.img
truncate -s 1G ~/lvm-lab/disk2.img
truncate -s 1G ~/lvm-lab/disk3.img
```

These files act like fake disks.

#### Step 2: Attach Files as Loop Devices

```bash id="ki12af"
sudo losetup --find --show ~/lvm-lab/disk1.img
sudo losetup --find --show ~/lvm-lab/disk2.img
sudo losetup --find --show ~/lvm-lab/disk3.img
```

Example output:

```text id="b6s88b"
/dev/loop10
/dev/loop11
/dev/loop12
```

Interpretation:

* The files are now visible as block devices
* In this example, the fake disks are `/dev/loop10`, `/dev/loop11`, and `/dev/loop12`
* Your device numbers may be different

#### Step 3: Create Physical Volumes

```bash id="kusq9g"
sudo pvcreate /dev/loop10 /dev/loop11 /dev/loop12
```

Example output:

```text id="s5pq5g"
Physical volume "/dev/loop10" successfully created.
Physical volume "/dev/loop11" successfully created.
Physical volume "/dev/loop12" successfully created.
```

Check:

```bash id="ckqgft"
sudo pvs
```

Example output:

```text id="e0rmtg"
PV           VG  Fmt  Attr PSize    PFree
/dev/loop10      lvm2 ---  1024.00m 1024.00m
/dev/loop11      lvm2 ---  1024.00m 1024.00m
/dev/loop12      lvm2 ---  1024.00m 1024.00m
```

Interpretation:

```text id="sxv540"
The loop devices are prepared for LVM.
They are not yet part of a volume group.
```

#### Step 4: Create a Volume Group

```bash id="h0vcaq"
sudo vgcreate lab_vg /dev/loop10 /dev/loop11
```

Example output:

```text id="rhw6pq"
Volume group "lab_vg" successfully created
```

Check:

```bash id="mqo2bi"
sudo vgs
```

Example output:

```text id="cdgcdl"
VG      #PV #LV #SN Attr   VSize  VFree
lab_vg    2   0   0 wz--n- 1.99g  1.99g
```

Interpretation:

```text id="xyk339"
Two 1 GB loop disks are combined into one volume group.
The volume group has about 2 GB of usable space.
```

#### Step 5: Create a Logical Volume

```bash id="dh42zw"
sudo lvcreate -L 1G -n data lab_vg
```

Example output:

```text id="sjtfpx"
Logical volume "data" created.
```

Check:

```bash id="a3r36b"
sudo lvs
```

Example output:

```text id="rawh1k"
LV    VG      Attr       LSize Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
data  lab_vg  -wi-a----- 1.00g
```

Interpretation:

```text id="o4fcfh"
A 1 GB logical volume named data now exists inside lab_vg.
```

#### Step 6: Create a Filesystem

```bash id="qopjkl"
sudo mkfs.ext4 /dev/lab_vg/data
```

Example output:

```text id="knq2qw"
Creating filesystem with 262144 4k blocks and 65536 inodes
Filesystem UUID: 12345678-abcd-1234-abcd-123456789abc
```

Interpretation:

```text id="d0nafn"
The logical volume now contains an ext4 filesystem.
It can be mounted and used for files.
```

#### Step 7: Mount the Logical Volume

```bash id="wlng4f"
sudo mkdir -p /mnt/lvmlab
sudo mount /dev/lab_vg/data /mnt/lvmlab
```

Check:

```bash id="gwjwgc"
df -h /mnt/lvmlab
```

Example output:

```text id="nasnlw"
Filesystem               Size  Used Avail Use% Mounted on
/dev/mapper/lab_vg-data  974M   24K  907M   1% /mnt/lvmlab
```

Interpretation:

```text id="c761po"
The logical volume is mounted and usable.
Files placed in /mnt/lvmlab are stored on the LVM logical volume.
```

### Scenario 2: Simulate a Full Filesystem and Fix It with LVM

#### Goal

Simulate a common storage bottleneck: a mounted filesystem is almost full, but the volume group still has free space.

This is one of the best practical use cases for LVM.

#### Step 1: Fill the Filesystem

```bash id="p3t9iq"
sudo fallocate -l 850M /mnt/lvmlab/bigfile
```

Check usage:

```bash id="sioih0"
df -h /mnt/lvmlab
```

Example output:

```text id="m42d61"
Filesystem               Size  Used Avail Use% Mounted on
/dev/mapper/lab_vg-data  974M  851M   58M  94% /mnt/lvmlab
```

Interpretation:

```text id="p6l0xo"
The filesystem is almost full.
Applications writing to /mnt/lvmlab may fail soon.
```

#### Step 2: Check Whether the Volume Group Has Free Space

```bash id="fgg7q7"
sudo vgs
```

Example output:

```text id="pjnb1v"
VG      #PV #LV #SN Attr   VSize  VFree
lab_vg    2   1   0 wz--n- 1.99g  1016.00m
```

Interpretation:

* The filesystem is almost full, but the volume group has about 1 GB free
* This means the logical volume can be extended

#### Step 3: Extend the Logical Volume and Filesystem

Use `-r` to resize the filesystem at the same time:

```bash id="lrn5li"
sudo lvextend -r -L +500M /dev/lab_vg/data
```

Example output:

```text id="j6u4k6"
Size of logical volume lab_vg/data changed from 1.00 GiB to 1.49 GiB.
Logical volume lab_vg/data successfully resized.
resize2fs 1.46.5
The filesystem is now 390144 blocks long.
```

#### Step 4: Verify the Result

```bash id="fzi9sx"
df -h /mnt/lvmlab
```

Example output:

```text id="o6pccr"
Filesystem               Size  Used Avail Use% Mounted on
/dev/mapper/lab_vg-data  1.5G  851M  542M  62% /mnt/lvmlab
```

Interpretation:

* The logical volume grew
* The filesystem grew
* The mount point now has more free space
* The capacity bottleneck is resolved

### Scenario 3: Simulate “No Space Left in Volume Group”

#### Goal

Show what happens when the filesystem needs more space but the volume group does not have enough free space.

#### Step 1: Try to Extend Too Much

```bash id="s2fwzq"
sudo lvextend -r -L +5G /dev/lab_vg/data
```

Example output:

```text id="grs1zn"
Insufficient free space: 1280 extents needed, but only 129 available
```

Interpretation:

* The logical volume cannot be extended because the volume group does not have enough free space
* This is not a filesystem problem
* This is a volume group capacity problem

#### Step 2: Confirm with `vgs`

```bash id="b9e1ek"
sudo vgs
```

Example output:

```text id="n84sk8"
VG      #PV #LV #SN Attr   VSize  VFree
lab_vg    2   1   0 wz--n- 1.99g  516.00m
```

Interpretation:

```text id="h5q06a"
Only about 516 MB is free in the volume group.
A 5 GB extension is impossible without adding more storage.
```

#### Step 3: Add Another Physical Volume

Earlier, `/dev/loop12` was prepared as a PV but not added to the VG.

Add it now:

```bash id="co3fbr"
sudo vgextend lab_vg /dev/loop12
```

Example output:

```text id="phu3q8"
Volume group "lab_vg" successfully extended
```

Check:

```bash id="fi91hr"
sudo vgs
```

Example output:

```text id="g6pz3f"
VG      #PV #LV #SN Attr   VSize  VFree
lab_vg    3   1   0 wz--n- 2.99g  1.51g
```

Interpretation:

* The volume group now includes another physical volume
* Free space increased
* The LV can now be extended further

#### Step 4: Extend Again

```bash id="funt08"
sudo lvextend -r -L +1G /dev/lab_vg/data
```

Check:

```bash id="l5a0pp"
df -h /mnt/lvmlab
```

Example output:

```text id="alr6z3"
Filesystem               Size  Used Avail Use% Mounted on
/dev/mapper/lab_vg-data  2.5G  851M  1.6G  35% /mnt/lvmlab
```

Interpretation:

* Adding a PV increased VG capacity
* The LV and filesystem were extended
* The filesystem now has enough free space

### Scenario 4: Simulate and Inspect LVM Layers

#### Goal

Use LVM tools to understand the relationship between PVs, VGs, LVs, filesystems, and mount points.

#### Check Block Devices

```bash id="xzq9hx"
lsblk
```

Example output:

```text id="z5ic26"
NAME              SIZE TYPE MOUNTPOINT
loop10              1G loop
└─lab_vg-data     2.5G lvm  /mnt/lvmlab
loop11              1G loop
└─lab_vg-data     2.5G lvm  /mnt/lvmlab
loop12              1G loop
└─lab_vg-data     2.5G lvm  /mnt/lvmlab
```

Interpretation:

* The logical volume data is built from space in the volume group
* The volume group is backed by multiple loop devices
* The logical volume is mounted at `/mnt/lvmlab`

#### Check Physical Volumes

```bash id="g37vc1"
sudo pvs
```

Example output:

```text id="tvh324"
PV           VG      Fmt  Attr PSize    PFree
/dev/loop10  lab_vg  lvm2 a--  1020.00m    0
/dev/loop11  lab_vg  lvm2 a--  1020.00m    0
/dev/loop12  lab_vg  lvm2 a--  1020.00m  500.00m
```

Interpretation:

```text id="e1bbv3"
All three loop devices are physical volumes.
Some free space remains on /dev/loop12.
```

#### Check Volume Group

```bash id="we2efe"
sudo vgs
```

Example output:

```text id="gt72ug"
VG      #PV #LV #SN Attr   VSize  VFree
lab_vg    3   1   0 wz--n- 2.99g 500.00m
```

Interpretation:

* The volume group contains 3 PVs and 1 LV
* It still has 500 MB free

#### Check Logical Volume

```bash id="yik0bu"
sudo lvs
```

Example output:

```text id="hg2slr"
LV    VG      Attr       LSize Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
data  lab_vg  -wi-ao---- 2.50g
```

Interpretation:

* The data LV is 2.5 GB
* The `o` attribute indicates it is open, meaning it is active and mounted or in use

### Scenario 5: Create a Snapshot Before a Risky Change

#### Goal

Create a snapshot, make a risky change, and understand how the snapshot protects the earlier state.

#### Step 1: Create a Test File

```bash id="v8gmxq"
echo "original version" | sudo tee /mnt/lvmlab/example.txt
cat /mnt/lvmlab/example.txt
```

Example output:

```text id="ysn4sx"
original version
```

#### Step 2: Create a Snapshot

```bash id="oudohe"
sudo lvcreate -L 200M -s -n data_snap /dev/lab_vg/data
```

Example output:

```text id="ro6ozs"
Logical volume "data_snap" created.
```

Check:

```bash id="p8j1sr"
sudo lvs
```

Example output:

```text id="x1583m"
LV        VG      Attr       LSize   Origin Data%
data      lab_vg  owi-aos---   2.50g
data_snap lab_vg  swi-a-s--- 200.00m data   0.01
```

Interpretation:

* `data_snap` is a snapshot of `data`
* It preserves the original state at the time the snapshot was created

#### Step 3: Make a Risky Change

```bash id="o79sl6"
echo "bad change" | sudo tee /mnt/lvmlab/example.txt
cat /mnt/lvmlab/example.txt
```

Example output:

```text id="tbrrqw"
bad change
```

#### Step 4: Inspect Snapshot Usage

```bash id="l25jps"
sudo lvs
```

Example output:

```text id="f4rdwr"
LV        VG      Attr       LSize   Origin Data%
data      lab_vg  owi-aos---   2.50g
data_snap lab_vg  swi-a-s--- 200.00m data   1.25
```

Interpretation:

* The snapshot is using some space because the original LV changed after the snapshot was created
* If `Data%` reaches `100%`, the snapshot becomes invalid

#### Step 5: Restore by Merging the Snapshot

Unmount the filesystem first:

```bash id="zq8sgf"
cd ~
sudo umount /mnt/lvmlab
```

Merge the snapshot:

```bash id="sdc56f"
sudo lvconvert --merge /dev/lab_vg/data_snap
```

Example output:

```text id="o63qma"
Merging of volume lab_vg/data_snap started.
lab_vg/data: Merged: 100.00%
```

Reactivate if needed:

```bash id="lwhwdt"
sudo lvchange -ay /dev/lab_vg/data
```

Mount again:

```bash id="kxkrxw"
sudo mount /dev/lab_vg/data /mnt/lvmlab
cat /mnt/lvmlab/example.txt
```

Expected output:

```text id="veakyq"
original version
```

Interpretation:

* The snapshot merge restored the LV to the earlier state
* The risky change was undone

### Scenario 6: Simulate Snapshot Space Exhaustion

Show why snapshot size matters.

Snapshots need enough space to store changed blocks. If too much changes after the snapshot is created, the snapshot can fill up and become unusable.

#### Step 1: Create a Small Snapshot

```bash id="d9kf9c"
sudo lvcreate -L 50M -s -n small_snap /dev/lab_vg/data
```

#### Step 2: Write Enough Data to the Original LV

```bash id="n9yplc"
sudo fallocate -l 200M /mnt/lvmlab/change-after-snapshot.bin
```

#### Step 3: Check Snapshot Usage

```bash id="a4j6mu"
sudo lvs
```

Example output:

```text id="fzq79o"
LV          VG      Attr       LSize  Origin Data%
data        lab_vg  owi-aos--- 2.50g
small_snap  lab_vg  swi-a-s--- 50.00m data   100.00
```

Interpretation:

* The snapshot is full
* A full snapshot may become invalid
* This means the snapshot can no longer reliably represent the original point-in-time state

#### Lesson

* Snapshot size must be chosen based on how much data may change while the snapshot exists
* Snapshots should usually be temporary

### Scenario 7: Clean Up the LVM Lab

Remove the test LVM setup safely.

#### Step 1: Unmount

```bash id="bfdmo5"
cd ~
sudo umount /mnt/lvmlab
```

#### Step 2: Remove Snapshots if Any Remain

```bash id="k4umtu"
sudo lvs
sudo lvremove /dev/lab_vg/small_snap
```

Only remove snapshots that exist.

#### Step 3: Remove the Logical Volume

```bash id="m4k756"
sudo lvremove /dev/lab_vg/data
```

Example output:

```text id="lex1ar"
Do you really want to remove active logical volume lab_vg/data? [y/n]: y
Logical volume "data" successfully removed.
```

#### Step 4: Remove the Volume Group

```bash id="dvj00j"
sudo vgremove lab_vg
```

#### Step 5: Remove Physical Volume Labels

```bash id="rjyd5g"
sudo pvremove /dev/loop10 /dev/loop11 /dev/loop12
```

#### Step 6: Detach Loop Devices

```bash id="qfx2sx"
sudo losetup -d /dev/loop10
sudo losetup -d /dev/loop11
sudo losetup -d /dev/loop12
```

#### Step 7: Delete Test Files

```bash id="q7bpte"
rm -rf ~/lvm-lab
sudo rmdir /mnt/lvmlab
```

Check:

```bash id="j19yhv"
lsblk
```

Interpretation:

```text id="mjaffu"
The test loop devices, LVM objects, mount point, and files have been removed.
The lab environment is cleaned up.
```

### Common LVM Troubleshooting

#### Problem: Filesystem Is Full

Symptoms:

```text id="st2n11"
applications cannot write files
df -h shows 100% usage
"No space left on device"
```

Check:

```bash id="gaz0f1"
df -h
sudo vgs
sudo lvs
```

Interpretation:

* If `df` is full but `VFree` exists in `vgs`, extend the LV
* If `df` is full and `VFree` is `0`, add storage or delete/move data

Fix if VG has free space:

```bash id="u2f1zc"
sudo lvextend -r -L +10G /dev/VG_NAME/LV_NAME
```

#### Problem: Volume Group Has No Free Space

Symptoms:

```text id="mne6vr"
lvextend fails
error mentions insufficient free extents
vgs shows VFree as 0
```

Check:

```bash id="gzd4mn"
sudo vgs
sudo pvs
```

Fix:

```bash id="rhup74"
sudo pvcreate /dev/newdisk
sudo vgextend VG_NAME /dev/newdisk
sudo lvextend -r -L +10G /dev/VG_NAME/LV_NAME
```

#### Problem: Logical Volume Exists but Is Not Mounted

Check:

```bash id="bq530x"
sudo lvs
lsblk
findmnt
```

If the LV exists but is not mounted, mount it:

```bash id="doa2re"
sudo mkdir -p /mnt/data
sudo mount /dev/VG_NAME/LV_NAME /mnt/data
```

#### Problem: LVM Devices Not Active

Sometimes LVM volumes exist but are inactive.

Check:

```bash id="akq2bd"
sudo lvs
```

Activate all volume groups:

```bash id="x5zkhp"
sudo vgchange -ay
```

Then check again:

```bash id="kb9h3x"
lsblk
```

#### Problem: Snapshot Is Full

Check:

```bash id="ycm6un"
sudo lvs
```

If snapshot `Data%` is near 100%, it is at risk.

Fix options:

* Remove the snapshot if no longer needed
* Extend the snapshot if possible
* Merge it if rollback is needed
* Avoid keeping snapshots too long

Remove snapshot:

```bash id="kx3887"
sudo lvremove /dev/VG_NAME/SNAPSHOT_NAME
```

### LVM Safety Rules

* Always back up important data before resizing
* Extending is usually safer than reducing
* Do not reduce an LV before shrinking the filesystem
* Use `lvextend -r` when possible
* Check `df -h`, `lvs`, `vgs`, and `pvs` before making changes
* Do not run `pvcreate` on a disk containing data you want to keep
* Snapshots are useful, but they are not full backups
* Test `/etc/fstab` changes with `mount -a` before rebooting

### Challenges

1. Describe the process of reducing the size of an LVM partition. Explain the precautions to take, such as ensuring adequate free space and backing up any critical data on the partition. Outline the commands you would use, including how to first resize the filesystem before reducing the logical volume itself.
2. Explain how to extend an LVM partition to utilize more free space within the volume group. Describe the process and commands required to first extend the logical volume and then resize the filesystem to use the additional space.
3. Describe the process of taking a snapshot of an LVM logical volume, including the reasons why snapshots are useful (such as for backups or testing changes). Provide the commands needed to create a snapshot and explain how to restore data from a snapshot if needed.
4. Detail the steps required to remove a logical volume from an LVM setup. Describe the commands needed for each step and discuss precautions to ensure data safety before, during, and after the removal process, such as unmounting the volume and backing up important data.
5. Explain the steps for adding a new physical disk to an existing volume group in an LVM setup. Describe the process, including the commands to initialize the disk as a physical volume, add it to the volume group, and verify the volume group has expanded.
6. Research and describe the concept of striping in LVM, including how striping can improve read and write performance by distributing data across multiple physical volumes. Explain the process of setting up a striped logical volume and the commands needed to specify the stripe size.
7. Describe how to monitor the status of your LVM setup, including checking for available free space, the health of logical volumes, and the status of volume groups. List the commands you would use, such as `lvdisplay`, `vgdisplay`, and `pvdisplay`, and explain the key information each command provides.
8. Compare a RAID setup with and without LVM. Discuss the benefits that LVM adds to a RAID environment, such as simplified management, easier resizing of logical volumes, and flexibility in adding storage. Provide examples of how LVM complements RAID setups.
9. Describe the process for moving data from one physical volume to another within an LVM setup, using the `pvmove` command. Explain why this might be necessary, such as for hardware maintenance or upgrading storage, and outline the steps to ensure data remains accessible throughout the move.
10. Research the LVM caching feature, which allows you to use a faster disk (such as an SSD) as a cache for a slower logical volume. Describe how this setup can improve performance, and provide an outline of the commands needed to set up an LVM cache.
