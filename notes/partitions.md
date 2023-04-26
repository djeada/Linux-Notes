## Partitioning disks

Partitioning a disk means dividing the disk into smaller areas called partitions. Each partition can store different types of data or provide extra storage. There are two main partition tables: MBR (Master Boot Record) and GPT (GUID Partition Table).

### MBR (Master Boot Record)

MBR is the older partition table format, used on most computers. It started in March 1983 with IBM PC DOS 2.0. MBR has three parts: the main boot code, a partition table for the disk, and a disk signature. MBR stores its data in the first sector of the disk. It supports disks up to 2TB and can have up to four primary partitions.

### GPT (GUID Partition Table)

GPT is a newer and better partition table format than MBR. It supports disks larger than 2TB and up to 128 partitions. GPT has a Protective MBR and also checks (CRC) values to make sure its data is correct. To use GPT, you must enable UEFI in your computer's BIOS settings.

## Common disk names

The first two-three letters mean the device type:

* /dev/sda - a hard drive using the SCSI/SATA driver. Both physical servers and virtual machines use it.
* /dev/hda - the older IDE disk device type.
* /dev/vda - a disk in a kvm virtual machine using the virtio disk driver. 
* /dev/xvda - a disk in a xen virtual machine using the xen virtual disk driver.

The last letter tells the device order, and the numbers tell how many partitions the device has, starting with zero:

* /dev/sda2 is the second (2) partition on your first (a) SATA disk.
* /dev/sdc1 is the first (1) partition on your third (c) SATA disk.
* /dev/hdb3 is the third (3) partition of the second (b) IDE hard drive.

## Looking at partition tables

To look at a disk's partition table, use the gdisk or fdisk command. The gdisk command is for GPT partitions, while fdisk can be used for MBR and GPT partitions. To see all disk partitions, use:

```
fdisk -l
```

## Making partitions

To make a partition on a disk, use the fdisk or gdisk command. To make a partition on the /dev/sda disk using fdisk, use:

```
fdisk /dev/sda
```

Press `n` to get to the partition creation menu. You will choose the type of partition (primary or extended). For a primary partition, use `p`, and for an extended or logical partition, use `e`.

To make a partition on the `/dev/sda` disk using `gdisk`, use:

```
gdisk /dev/sda
```

1. Make a new partition by pressing `n`.

2. Choose if you want to create a primary or logical partition by pressing `p` or `l`.

3. Choose the partition number by typing a number from 1 to 128.

4. Type the starting and ending sectors for the partition, or press enter to use the default values.

5. Choose a partition type by pressing `t` and entering the type code or type name.

6. Type `w` to save the changes to the disk and leave `gdisk`.

Note: If you are making a partition on a disk that already has partitions, you might need to delete or resize existing partitions before making the new one. To delete a partition, use the d command in gdisk, and to resize a partition, use the n command to make a new partition in the size you want, then delete the old partition.

## Changing MBR to GPT using gdisk

Sometimes you might want to change a disk from one partition table format to another. For example, you might have an MBR disk and want to change it to GPT, or be done using tools like gdisk or parted.

To change an MBR disk to GPT using `gdisk`, follow these steps:

1. First, check the current partition table of the disk using `gdisk -l /dev/sda`
2. Backup the current partition table by making a copy using `sgdisk -b /dev/sda`
3. Now, run `gdisk /dev/sda` to open the `gdisk` tool for the `/dev/sda` disk
4. Press `x` to enter the experts menu and then `z` to remove the GPT data structures on the disk
5. Press `y` when asked to confirm that you want to destroy the GPT data structures
6. Press `n` to create a new GPT data structure on the disk
7. Press `y` when asked to confirm 
8. Now, you can create the partitions on the disk as needed using the `n` command in the main menu
9. When you are done creating the partitions, press `w` to save the changes to the disk
10. Restart the system and check the partition table using `gdisk -l /dev/sda` to make sure the conversion was successful

## Challenges

1. What is the difference between MBR and GPT partition tables?
2. How do you see all disk partitions in Linux?
3. How do you make a new partition using fdisk?
4. What is the difference between primary and extended partitions?
5. How do you delete a partition using fdisk?
6. What is the reason for creating a filesystem on a disk?
7. Can you change an MBR partition table to a GPT partition table and the other way around? If so, how?
8. What do the first two or three letters of common disk names mean?
9. What do the last letter and numbers of common disk names mean?
10. What is the biggest capacity of a disk that can be partitioned with MBR and GPT, respectively?
