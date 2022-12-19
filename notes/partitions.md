## Partitioning disks

Partitioning a disk is the process of dividing the disk into multiple storage areas, known as partitions. Each partition can be used to store different types of data or to provide additional storage space. There are two main types of partition tables: MBR (Master Boot Record) and GPT (GUID Partition Table).

### MBR (Master Boot Record)

MBR is the traditional partition table format used on most computers. It was first introduced in March 1983 with IBM PC DOS 2.0. MBR consists of three main parts: the master boot code, a partition table for the disk, and a disk signature. MBR stores its data on the first sector of the disk. It supports disks up to 2TB in capacity and can store a maximum of four primary partition entries.

### GPT (GUID Partition Table)

GPT is a newer and more advanced partition table format than MBR. It supports disks larger than 2TB and up to 128 partitions. GPT is made up of a Protective MBR and also maintains cyclic redundancy check (CRC) values to ensure the integrity of its data. To use GPT, you must enable the UEFI in your system's BIOS settings.

## Common disk names

The first two-three letters refer to the device type:

* /dev/sda - a hard drive that use the SCSI/SATA driver. Both physical servers and virtual machines use it.
* /dev/hda - the legacy IDE disk device type.
* /dev/vda - a disk in a kvm virtual machine using the virtio disk driver. 
* /dev/xvda - a disk in a xen virtual machine that use the xen virtual disk driver.

The last letter denotes the device order (it may alternatively be the last two), and the digits denote the number of partitions the device has, beginning with zero:

* /dev/sda2 is the second (2) partition on your initial (a) SATA disk.
* /dev/sdc1 is the first (1) partition on your third (c) SATA disk.
* /dev/hdb3 is the third (3) partition of the second (b) IDE hard drive.

## Viewing partition tables

To view the partition table of a disk, you can use the gdisk or fdisk command. The gdisk command is specifically for GPT partitions, while fdisk can be used for both MBR and GPT partitions. To view all disk partitions, use:

```
fdisk -l
```

## Creating partitions

To create a partition on a disk, you can use the fdisk or gdisk command. To create a partition on the /dev/sda disk using fdisk, use:

```
fdisk /dev/sda
```

Press `n` to access the partition creation menu. You will be asked to select the type of partition (primary or extended). For a primary partition, use `p`, and for an extended or logical partition, use `e`.

To create a partition on the `/dev/sda` disk using `gdisk`, use:

```
gdisk /dev/sda
```

1. Create a new partition by pressing `n`.

2. Choose whether you want to create a primary or logical partition by pressing `p` or l, respectively.

3. Choose the partition number by typing in a number from 1 to 128.

4. Enter the starting and ending sectors for the partition, or press enter to use the default values.

5. Choose a partition type by pressing `t` and entering the type code or type name.

6. Type `w` to write the changes to the disk and exit `gdisk`.

Note: If you are creating a partition on a disk that already has partitions, you may need to delete or resize existing partitions before creating the new one. To delete a partition, use the d command in gdisk, and to resize a partition, use the n command to create a new partition in the desired size, then delete the old partition.

## Converting MBR to GPT using gdisk

There are times when you might want to convert a disk from one partition table format to another. For example, you might have an MBR disk and want to convert it to GPT, or vice versa. This can be done using certain tools such as gdisk or parted.

To convert an MBR disk to GPT using `gdisk`, follow these steps:

1. First, check the current partition table of the disk using `gdisk -l /dev/sda`
1. Backup the current partition table by creating a copy of it using `sgdisk -b /dev/sda`
1. Now, run `gdisk /dev/sda` to open the `gdisk` tool for the `/dev/sda` disk
1. Press `x` to enter the experts menu and then `z` to zap the GPT data structures on the disk
1. Press `y` when prompted to confirm that you want to destroy the GPT data structures
1. Press `n` to create a new GPT data structure on the disk
1. Press `y` when prompted to confirm 
1. Now, you can create the partitions on the disk as needed using the `n` command in the main menu
1. When you are done creating the partitions, press `w` to write the changes to the disk
1. Reboot the system and check the partition table using `gdisk -l /dev/sda` to confirm that the conversion was successful

## Challenges

1. What is the difference between MBR and GPT partition tables?
1. How do you view all disk partitions in Linux?
1. How do you create a new partition using fdisk?
1. What is the difference between primary and extended partitions?
1. How do you delete a partition using fdisk?
1. What is the purpose of creating a filesystem on a disk?
1. Can you convert an MBR partition table to a GPT partition table and vice versa? If so, how?
1. What do the first two or three letters of common disk names represent?
1. What do the last letter and digits of common disk names represent?
1. What is the maximum capacity of a disk that can be partitioned with MBR and GPT, respectively?
