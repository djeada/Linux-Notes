## Standards for the layout of partition tables 

When configuring a hard drive, you have two options: 
* MBR (Master Boot Record)
* GPT (GUID Partition Table)

To see which one you are using, use:
 
```bash
gdisk -l 
```

## MBR

* In March 1983, IBM PC DOS 2.0 included MBR.
* MBR is made up of three parts: master boot code, a partition table for the disk, and disk signature. 
* It saves its data on the disk's first sector. 
* MBR only supports disks up to 2TB in capacity and can store a maximum of four primary partition entries.

## GPT

* It's newer and more advanced than MBR. It does all its predecessor can do and more.
* GUID Partition Tables, is a format that differs from MBR in that it allows more than 2 TB and up to 128 partitions.
* GPT is made up of a Protective MBR and additionally maintains cyclic redundancy check (CRC) values to ensure the integrity of its data.
* To use it you must activate the UEFI in your system's BIOS settings.

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

## Creating and destroying partitions
You can use fdisk to create both MBR and GPT partitions. However it is adviced to used gdisk for GPT partitions, which has similar interface.

To view all disk partitions, use:

```bash
fdisk -l
```

To create a /dev/sda partition, use:  

```bash
fdisk /dev/sda
```

Type n to access the creation menu.
You will be asked to select the kind of partition. For a primary partition, use p, and for an extended or logical partition, use e.

To remove a /dev/sda partition, use:  

```bash
fdisk /dev/sda
```

Type d to access the deletion menu.

After you've set up your partitions, you must create a filesystem to make your disk usable!
