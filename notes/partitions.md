## Partitioning disks

Partitioning a disk means dividing the disk into smaller areas called partitions. Each partition can store different types of data or provide extra storage. There are two main partition tables: MBR (Master Boot Record) and GPT (GUID Partition Table).

```
+------------------+------------------+------------------+-----------------+-----------------+
| Partition        | /dev/sda1        | /dev/sda2        | /dev/sda3       | Free Space      |
+------------------+------------------+------------------+-----------------+-----------------+
| Filesystem       | ext4             | ext4             | swap            |                 |
+------------------+------------------+------------------+-----------------+                 |
| Mount Point      | /                | /home            |                 |                 |
+------------------+------------------+------------------+-----------------+                 |
| Size             | 50GB             | 100GB            | 8GB             | 42GB            |
+------------------+------------------+------------------+-----------------+-----------------+
```

### MBR (Master Boot Record)

MBR is the older partition table format, used on most computers. It started in March 1983 with IBM PC DOS 2.0. MBR has three parts: the main boot code, a partition table for the disk, and a disk signature. MBR stores its data in the first sector of the disk. It supports disks up to 2TB and can have up to four primary partitions.

### GPT (GUID Partition Table)

GPT is a newer and better partition table format than MBR. It supports disks larger than 2TB and up to 128 partitions. GPT has a Protective MBR and also checks (CRC) values to make sure its data is correct. To use GPT, you must enable UEFI in your computer's BIOS settings.

| Feature        | GPT (GUID Partition Table)                 | MBR (Master Boot Record)           |
|----------------|--------------------------------------------|------------------------------------|
| **Maximum Partition Size** | 18.8 million TB (with 512B sector size) | 2 TB (with 512B sector size)       |
| **Maximum Number of Partitions** | 128 partitions per disk (typically)   | 4 primary partitions per disk     |
| **Data Recovery** | Stores multiple copies of the partitioning and boot data across the disk for resilience. | Stores only one copy of the partitioning and boot data at the beginning of the disk, making it more prone to data loss. |
| **Compatibility** | Supported by newer operating systems and modern hardware (UEFI). | Universally compatible with all operating systems and BIOS. |
| **Boot Process** | Works with UEFI (Unified Extensible Firmware Interface) which is a modern method of booting. | Works with BIOS (Basic Input/Output System) which is traditional and older. |
| **Partition Scheme** | Uses globally unique identifiers (GUIDs) for partitions. | Uses a traditional partition table. |
| **Advantages** | Higher limits on partition sizes and counts, better data resilience, required for modern hardware (like larger hard drives). | Universal compatibility, simplicity, and well-tested over time. |
| **Disadvantages** | Not compatible with older systems that only support BIOS. | Limited partition size and count, less resilient against data corruption. |

### Common disk names

The first two-three letters mean the device type:

- `/dev/sda`: This represents a hard drive using the SCSI or SATA interface driver. It's commonly used in both physical servers and virtual machines.
- `/dev/hda`: Refers to the older IDE disk device type. This was more common in older systems and is less frequently seen in modern setups.
- `/dev/vda`: Indicates a disk in a KVM (Kernel-based Virtual Machine) virtual machine using the virtio disk driver.
- `/dev/xvda`: Represents a disk in a Xen virtual machine using the Xen virtual disk driver.

The last letter tells the device order, and the numbers tell how many partitions the device has, starting with zero:

I. The last letter (before any numbers) shows the order of the device. 

For example:

- `a` in `/dev/sda` indicates it's the first SCSI/SATA disk.
- `b` in `/dev/hdb` shows it's the second IDE disk.

II. The numbers denote the partition index on the device, starting from 1. 

For example:

- `/dev/sda2` is the second partition (`2`) on the first SATA disk (`sda`).
- `/dev/sdc1` refers to the first partition (`1`) on the third SATA disk (`sdc`).
- `/dev/hdb3` is the third partition (`3`) on the second IDE hard drive (`hdb`).

Note:

- Modern systems predominantly use the `/dev/sdX` naming convention due to the shift towards SATA interfaces.
- In virtualized environments, `/dev/vdX` and `/dev/xvdX` are more common, depending on the virtualization technology used.

### Looking at partition tables

To look at a disk's partition table, use the gdisk or fdisk command. The gdisk command is for GPT partitions, while fdisk can be used for MBR and GPT partitions. To see all disk partitions, use:

```
fdisk -l
```

Here's an example of what this output might look like:

```
Disk /dev/sda: 240.0 GB, 240057409536 bytes, 468862128 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: gpt

Device       Start       End   Sectors  Size Type
/dev/sda1     2048   1050623   1048576  512M EFI System
/dev/sda2  1050624 468862127 467811504  223G Linux filesystem

Disk /dev/sdb: 1.0 TB, 1000204886016 bytes, 1953525168 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: mbr

Device       Start       End   Sectors  Size Type
/dev/sdb1     2048 1953525167 1953523120 931.5G Linux filesystem
```

Explanation:

- *Disk Information*: Provides details about each disk (`/dev/sda`, `/dev/sdb`, etc.), including size, sector information, and disk label type (GPT or MBR).
- *Partition Information*: For each disk, it lists all partitions, their start and end sectors, total sectors, size, and type (e.g., EFI System, Linux filesystem).
    
### Making Partitions on a Disk

Creating partitions on a disk allows you to logically divide it into segments, each of which can be used independently. This can be done using either the `fdisk` or `gdisk` command in Linux, depending on whether your disk uses MBR (Master Boot Record) or GPT (GUID Partition Table) partitioning scheme, respectively.

#### MBR Partitioning

To partition a disk (e.g., `/dev/sda`) with `fdisk`:
1. Start `fdisk`: `fdisk /dev/sda`.
2. To create a new partition, press `n`. You'll then be prompted to choose between creating a primary (`p`) or an extended (`e`) partition. Most use cases will require a primary partition.
3. Specify the partition size by entering the starting and ending sectors. You can press Enter to accept the default values.
4. Optionally, set the partition type by pressing `t` and entering the type code.
5. To save the changes and exit `fdisk`, press `w`.

#### GPT Partitioning

For disks with GPT, use `gdisk`:
1. Open `gdisk` on your target disk: `gdisk /dev/sda`.
2. Create a new partition by pressing `n`. 
3. Choose the partition number (1 to 128).
4. Enter the starting and ending sectors, or press Enter to use defaults.
5. Set the partition type by pressing `t` and entering the type code or name.
6. Write the changes to disk and exit by pressing `w`.

#### Important Notes

- **Backup Data** before modifying disk partitions to prevent data loss, as altering partitions can sometimes lead to accidental loss of important information.
- When managing disk partitions, **Resizing and Deleting Partitions** may be necessary if existing partitions occupy the space needed for new ones. To delete a partition, use the `d` command in tools like `gdisk` or `fdisk`. For resizing, you might need to create a new partition with the desired size using the `n` command and then delete the old partition.
- The **Partition Types** you select depend on specific needs, such as using a Linux filesystem or creating a swap space. Each partition type is identified by a unique code or identifier that defines its purpose and structure.
- **Administrative Privileges** are typically required when using partitioning tools, as these actions need root access. Therefore, commands are often prefixed with `sudo` to grant the necessary permissions.

### Changing MBR to GPT using gdisk

Sometimes, there's a need to change a disk from one partition table format to another. For instance, converting an MBR disk to a GPT format can be done using tools like `gdisk` or `parted`. Here's how to do it with `gdisk`:

1. First, check the current partition table of the disk: `gdisk -l /dev/sda`.
2. Backup the current partition table: `sgdisk -b /dev/sda`.
3. Run `gdisk` for the disk: `gdisk /dev/sda`.
4. In `gdisk`, press `x` to enter the experts menu.
5. Then, press `z` to zap (remove) the GPT data structures on the disk.
6. Confirm the action by pressing `y` when prompted about destroying the GPT data structures.
7. Press `n` to create a new GPT data structure on the disk.
8. Confirm the creation of a new empty GPT by pressing `y`.
9. Create the required partitions by using the `n` command in the main menu.
10. After partitioning, save the changes and exit `gdisk` by pressing `w`.
11. Restart the system to ensure all changes take effect.
12. Verify the new partition table: `gdisk -l /dev/sda`.

🔴 Caution:

- It's crucial to back up any important data before proceeding with this operation, as changing the partition table format can lead to data loss.
- Ensure that your system supports GPT and UEFI (if you're planning to boot from the disk), as older systems with BIOS may not support GPT.

### Challenges

1. What are the key differences in terms of capacity, partition limits, and compatibility between MBR (Master Boot Record) and GPT (GUID Partition Table) partition tables?
2. How can you list all the disk partitions on a Linux system?
3. What are the steps to create a new partition on a disk using the `fdisk` command?
4. What distinguishes primary partitions from extended partitions?
5. How can you delete an existing partition using the `fdisk` command?
6. Why is it necessary to create a filesystem on a disk partition?
7. Is it possible to convert a disk from an MBR partition table to a GPT partition table and vice versa? If yes, how can this be achieved?
8. What do the first two or three letters in common disk names (like `/dev/sda`, `/dev/hda`) signify?
9. What information is conveyed by the last letter and the numbers in common disk names (e.g., `/dev/sda1`, `/dev/sdc2`)?
10. What is the largest capacity of a disk that can be effectively partitioned using MBR and GPT partition tables, respectively?
