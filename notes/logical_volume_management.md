## Partitions and Volumes

Storage media such as DVDs, USB sticks, hard disk drives (HDDs), and solid state drives (SSDs) can all be partitioned. Partitions are defined in the partition table and allow a single storage device to be used for multiple purposes.

A volume is a single accessible storage area with a single file system. While a partition is contained to a single disk, a disk can have one or more partitions. Additionally, a volume may span multiple disks.
Logical Volume Manager (LVM)

The Logical Volume Manager (LVM) is a tool for managing disk storage space in Linux systems. It allows you to create logical volumes that can be easily resized, relocated, and added to, providing flexibility and the ability to add capacity to your system without the need for physical disk expansion. LVM also allows for the creation of volume snapshots, which can be useful for creating backups.

However, LVM does add some complexity to the setup process and requires additional kernel support. In some cases, repair images may not work with LVM-based systems.

## LVM Components

LVM is made up of several components: physical volumes, volume groups, and logical volumes. Physical volumes are actual disk storage devices, such as HDDs or SSDs. Volume groups are collections of physical volumes that can be treated as a single entity. Logical volumes are the storage areas within volume groups that can be formatted with a file system and mounted.


## Creating LVM Volumes

To create LVM volumes, you need to perform the following steps:

1. Create physical volumes: Use the pvcreate command to define physical volumes on disks. For example:

```bash
pvcreate /dev/sdb
pvcreate /dev/sdc
pvcreate /dev/sdd
```

2. Define volume groups: Use the vgcreate command to create a volume group and add physical volumes to it. For example:


```bash
vgcreate TEST /dev/sdb
vgextend TEST /dev/sdc /dev/sdd
```

3. Create logical volumes: Use the lvcreate command to create logical volumes within a volume group. For example:

```bash
lvcreate -L 20G -n vol_name_1 TEST
lvcreate -L 12G -n vol_name_2 TEST
```

4. Create a file system on the logical volume: Use the mkfs command to create a file system on the logical volume. For example:

```bash
mkfs -t ext4 /dev/TEST/vol_name_1
```

5. Mount the logical volume: Use the mount command to mount the logical volume to a desired mounting point. For example:

```bash
mount -t ext4 /dev/TEST/vol_name_1 /mounting_point
```

## Challenges

1. How to reduce the size of an LVM partition? Hint: Keep in mind that you can only reduce the size of an LVM partition if there is enough free space within the logical volume to allow for the reduction. You should also make sure to back up any important data on the partition before attempting to resize it.
