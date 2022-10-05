<h2>Partition vs volume</h2>

Storage media (DVDs, USB sticks, HDDs, SSDs) may all be partitioned, and these partitions are defined in the partition table.

A volume is a single accessible storage area with a single file system. 

* A partition is contained to a single disk.
* A disk can have one or more partitions.
* A volume may span multiple disks.

<h2>LVM</h2>

Pros:
* Flexibility. Can relocate space between volumes while the system is running without effort.
* Possibility to add capacity.
* Allows volume snapshots which are useful for backups.

Cons:
* Added complexity in setup.
* More kernel support is required, thus some repair images may fail.

<h2>LVM Components</h2>

Physical Volumes -> Volume Group -> Logical Volume 1, Logical Volume 2...

<h2>Creating LVM Volumes</h2>

1. Create physcial volumes
2. Define volume groups
3. Create logical volumes

Clearing a disk's partition table

```bash
dd if=/dev/zero of=/dev/sdb bs=512 count=1
```

Defining LVM physical volumes

```bash
pvcreate /dev/sdb
pvcreate /dev/sdc
pvcreate /dev/sdd
```

Show all currently defined physical volumes:

```bash
pvscan -v
```

Creating a volume group:

```bash
vgcreate TEST /dev/sdb
vgextend TEST /dev/sdc /dev/sdd
```

Defining logical volumes:

```bash
lvcreate -L 20G -n vol_name_1 TEST
lvcreate -L 12G -n vol_name_2 TEST
```

Create a file system on the logical volume:

```bash
mkfs -t ext4 /dev/TEST/vol_name_1
```

Mount the logical volume:

```bash
mount -t ext4 /dev/TEST/vol_name_1 mounting_point
```

## Challenges

1. How to reduce the size of LVM partition?
