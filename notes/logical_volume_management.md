## Partitions and Volumes

Picture storage devices like DVDs, USBs, and various hard drives (HDDs and SSDs, for example) as cakes that can be sliced into smaller pieces. These slices are known as partitions, and they help organize the storage device into sections for different uses, like keeping various file types or running multiple operating systems. The way these partitions are arranged is like a table you'd use to keep track of everything.

Now, think of a volume as a section on a bookshelf, each with its own way of organizing files, or a file system. It's like having a separate spot on the shelf for different genres of books. While a partition is restricted to just one disk, that disk can have multiple partitions. For example, you might have a hard drive split into three parts: one for your operating system, another for your documents, and a third for your multimedia files.

In contrast, a volume can span across several disks, similar to connecting multiple bookshelves to make more room for your books. This can be helpful when you need extra space for certain files, like large video files, and want to spread the storage across multiple devices.

## Logical Volume Manager (LVM)

The Logical Volume Manager (LVM) is a tool for managing disk storage in Linux systems. It lets you create logical volumes that can be easily changed in size, moved, and added to. This gives flexibility and lets you add storage to your system without needing more physical disks. LVM also allows for making volume snapshots, which can be useful for making backups.

But, LVM does make the setup process more complex and needs extra support from the kernel. In some cases, repair images might not work with LVM-based systems.

## LVM Components

LVM has several parts:

* physical volumes,
* volume groups,
* logical volumes.

Physical volumes are actual storage devices, like HDDs or SSDs. Volume groups are groups of physical volumes that can be treated as one thing. Logical volumes are the storage areas within volume groups that can be given a file system and mounted.

## Creating LVM Volumes

To create LVM volumes, follow these steps:

1. Make physical volumes: Use the `pvcreate` command to make physical volumes on disks. For example:

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
2. How do you extend an LVM partition to use more free space within the volume group? What command(s) would you use?
3. Explain the process of taking a snapshot of an LVM logical volume. Why might this be useful, and how can you create and restore from a snapshot?
4. How do you remove a logical volume from an LVM setup? What are the necessary steps to ensure data safety?
5. How do you add a new physical disk to an existing volume group? Describe the process, including the commands required.
6. Explain the concept of striping in LVM. What is its purpose, and how can you set up a striped logical volume?
7. How can you monitor the status of your LVM setup, including checking for available free space, the status of logical volumes, and the status of volume groups?
8. In a RAID setup, what are the differences between using LVM and not using LVM? What benefits does LVM provide in a RAID environment?
