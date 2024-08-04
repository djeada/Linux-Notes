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

You can perform the following operations with partitions:

- You can **create** new partitions if there is sufficient physical space available on the disk.
- **Deleting** a partition will remove all data stored within that partition, so it is important to back up any important information before performing this operation.
- **Resizing** a partition involves either **shrinking** or **growing** it, depending on your needs and available unallocated space on the disk.
- When resizing partitions, be aware that the **file system** may need to be adjusted to match the new partition size, and this operation may require additional tools or steps to complete successfully.

### Relationship between Physical Disks and Partitions 

The relationship between physical disks (like hard drives or SSDs) and partitions is managed through a device naming convention and a series of abstractions that allow the operating system to handle storage efficiently. Physical disks are the actual hardware components where data is stored. They can be hard disk drives (HDDs), solid-state drives (SSDs), or other storage devices. These disks are identified by device names such as `/dev/sda`, `/dev/sdb`, etc.

```
+-------------------+
| Physical Disk 1  |
|    (/dev/sda)     |
|                   |
|  +-------------+  |
|  | Partition 1 |  |
|  | (/dev/sda1) |  |
|  +-------------+  |
|  | Partition 2 |  |
|  | (/dev/sda2) |  |
|  +-------------+  |
+-------------------+

+-------------------+
| Physical Disk 2  |
|    (/dev/sdb)     |
|                   |
|  +-------------+  |
|  | Partition 1 |  |
|  | (/dev/sdb1) |  |
|  +-------------+  |
|  | Partition 2 |  |
|  | (/dev/sdb2) |  |
|  +-------------+  |
+-------------------+

+-------------------+
| Physical Disk 3  |
|    (/dev/sdc)     |
|                   |
|  +-------------+  |
|  | Partition 1 |  |
|  | (/dev/sdc1) |  |
|  +-------------+  |
|  | Partition 2 |  |
|  | (/dev/sdc2) |  |
|  +-------------+  |
+-------------------+
```

Partitions are divisions of a physical disk, each of which can be formatted with a file system and used for different purposes. Each partition is also represented as a device file but with an additional number indicating the partition:

- `/dev/sda1` refers to the first partition on the first disk (`/dev/sda`).
- `/dev/sda2` refers to the second partition on the first disk, and so forth.

### Common Disk Naming Conventions

Disk names typically follow a specific naming pattern to indicate the type of device, its order, and its partitions. Here's a breakdown:

#### I Device Type Indicators

The first few letters of the disk name indicate the type of device:

- **`/dev/sdX`**: Represents a hard drive using the SCSI or SATA interface. Commonly used in physical servers and virtual machines.
- **`/dev/hdX`**: Refers to an older IDE disk. This type is less common in modern systems.
- **`/dev/vdX`**: Indicates a disk in a KVM (Kernel-based Virtual Machine) using the virtio disk driver.
- **`/dev/xvdX`**: Represents a disk in a Xen virtual machine using the Xen virtual disk driver.

#### II Device Order

The last letter before any numbers denotes the order of the device:

- **`/dev/sda`**: The first SCSI/SATA disk.
- **`/dev/sdb`**: The second SCSI/SATA disk.
- **`/dev/hda`**: The first IDE disk.
- **`/dev/hdb`**: The second IDE disk.

#### III Partition Number

Numbers following the device identifier indicate the partition index:

- **`/dev/sda1`**: The first partition on the first SATA disk.
- **`/dev/sdc2`**: The second partition on the third SATA disk.
- **`/dev/hdb3`**: The third partition on the second IDE disk.

#### Additional Remarks

- Modern systems predominantly use the `/dev/sdX` naming convention due to the widespread adoption of SATA interfaces.
- In virtualized environments, `/dev/vdX` and `/dev/xvdX` are commonly used, depending on the virtualization technology.

This naming convention helps to identify and manage disks and partitions in various systems and environments efficiently.

### Partition Types

### Primary Partitions

- **Primary** partitions are one of the basic types of partitions on a hard drive. They are used to store **data** and can be directly accessed by the system.
- When a **primary partition** is created, it is given a specific portion of the hard drive's **storage space** and can be formatted with a file system such as **NTFS**, **FAT32**, or **ext4**. This process involves initializing the partition, setting a file system, and making it ready for data storage.
- Upon creation, one of the primary partitions can be marked as "**active**," indicating that it contains the operating system that the computer should **boot** from.
- If a primary partition is **removed**, the data within that partition is typically lost unless **backed up**. The space occupied by the partition becomes **unallocated**, and it can be reused to create a new partition. The removal process involves deleting the partition table entry and possibly wiping the data, depending on the tools and methods used.

#### Extended Partitions

- An **extended partition** is a special type of partition that acts as a **container** for logical partitions, used when more than four partitions are needed on a system.
- When an extended partition is created, it occupies one of the four primary partition slots but does not directly hold **data**. Instead, it provides a framework within which **logical partitions** can be created. The creation process involves defining the size and boundaries of the extended partition, which can then be subdivided into logical partitions.
- The creation of an extended partition allows for greater **flexibility** in partitioning schemes, as multiple logical partitions can be set up within it, effectively bypassing the limit of four primary partitions.
- Removing an extended partition results in the loss of all **logical partitions** contained within it. The process of removal includes deleting the partition table entry for the extended partition and all its associated logical partitions. The freed space becomes **unallocated** and available for new partitions.

#### Logical Partitions

- **Logical partitions** are subdivisions within an extended partition. They function similarly to primary partitions in that they can store **data** and be formatted with a file system.
- When a logical partition is created, it is defined within the space of an extended partition. The process involves setting up a specific area within the extended partition, formatting it with a file system, and preparing it for **data storage**.
- Logical partitions allow users to create more than four partitions on a system, providing additional **organizational** options for different types of data or multiple **operating systems**.
- Removing a logical partition involves deleting its partition table entry within the extended partition. The data in the logical partition is lost unless **backed up**. The space occupied by the deleted logical partition becomes **unallocated** within the extended partition and can be reused for new logical partitions.

### MBR and GPT

- **MBR** is the older partition table format, used on most computers. It started in March 1983 with IBM PC DOS 2.0. MBR has three parts: the main boot code, a partition table for the disk, and a disk signature. MBR stores its data in the first sector of the disk. It supports disks up to 2TB and can have up to four primary partitions.
- **GPT** is a newer and better partition table format than MBR. It supports disks larger than 2TB and up to 128 partitions. GPT has a Protective MBR and also checks (CRC) values to make sure its data is correct. To use GPT, you must enable UEFI in your computer's BIOS settings.

Below is a table comparing both formats:

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

### Looking at partition tables

To look at a disk's partition table, use the gdisk or `fdisk` command. The `gdisk` command is for GPT partitions, while `fdisk` can be used for both MBR and GPT partitions. To see all disk partitions, use:

```
fdisk -l
```

Here's an example of what this output might look like:

```
Disk /dev/sda: 500 GiB, 536870912000 bytes, 1048576000 sectors
Disk model: Samsung SSD 860
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 2F3C4D5E-6F7A-4B8B-9C7D-2E1F12345678

Device        Start        End   Sectors   Size Type
/dev/sda1      2048     534527    532480   260M EFI System
/dev/sda2    534528    1050623    515096   251M Linux filesystem
/dev/sda3   1050624  209715199 208664576  99.5G Linux filesystem
/dev/sda4 209715200  419430399 209715200   100G Linux filesystem
/dev/sda5 419430400 1048575967 628145568 299.5G Linux filesystem
```

Explanation:

- The system currently has five partitions, which are labeled as `/dev/sda1` through `/dev/sda5`.
- The disk uses the GPT partitioning scheme, which supports more than four primary partitions and is suitable for disks larger than **2 TB**.
- The first partition, `/dev/sda1`, is an EFI System Partition and is **260M** in size. This partition is typically used to store the bootloader and related files necessary for booting the operating system.
- The second partition, `/dev/sda2`, is a Linux filesystem partition with a size of **251M**. This might be used for a small dedicated function, such as a `/boot` partition.
- The third partition, `/dev/sda3`, is also a Linux filesystem partition and has a size of **99.5G**. This could be the primary partition used for the operating system and user data.
- The fourth partition, `/dev/sda4`, is another Linux filesystem partition with a size of **100G**. It might be used for storing additional data or another operating system.
- The fifth partition, `/dev/sda5`, is the largest, with a size of **299.5G**, and is also a Linux filesystem. This partition could be used for extensive data storage or other applications.
- The total size of all the partitions combined is approximately **499.511 GiB**. This value is slightly less than the total physical disk size due to the space reserved for partition tables and alignment overhead.
- The physical disk, identified as `/dev/sda`, has a total size of **500 GiB**, which corresponds to **536870912000** bytes.
- The difference between the total physical disk size and the sum of all partition sizes is minimal, indicating efficient use of disk space with only minor overhead.
- Since the disk uses GPT, it supports creating additional partitions beyond the existing five. GPT allows for up to **128 partitions** on most systems, far exceeding the four primary partitions limitation of MBR.
- Options for managing partitions include resizing existing partitions if there is unallocated space or if certain partitions can be shrunk to make room for others.
- New partitions can be created using the unallocated space on the disk, if available, using command-line tools like `fdisk`, `gdisk`, or graphical utilities such as `GParted`.
- It is possible to change the type of an existing partition, for example, converting a Linux filesystem partition to a swap partition, depending on system requirements.

### Managing Disk Partitions 

To manage disk partitions in Linux, you can use tools like `fdisk`, `parted`, or `lsblk`. Here's a guide on how to handle the tasks you've mentioned, with examples and explanations:

#### Checking Partition Types

To differentiate between primary, extended, and logical partitions, we need to check for the partition number and consider that extended partitions are typically numbered within 1-4 but are treated separately from primary partitions. Here's a command that will list all the partitions on your system along with their types:

```bash
lsblk -o NAME,TYPE | awk '
$2 == "part" {
    if ($1 ~ /[1-4]$/) {
        if ($1 ~ /[0-9]p[0-9]$/) {
            part_type = "primary"
        } else {
            part_type = "extended"
        }
    } else {
        part_type = "logical"
    }
    print "/dev/" $1, part_type
}'
```

Example output:

```
/dev/├─sda1 primary
/dev/└─sda2 primary
```

To determine whether a specific partition is primary, extended, or logical, you can use the following script. This script takes a partition path (like `/dev/sda1`) and outputs its type:

```bash
partition_path="/dev/sda1"  # Replace with user-provided partition path
lsblk -no TYPE $partition_path | awk '
/part/ {
    if ("'"$partition_path"'" ~ /[0-9]p?[1-4]$/) {
        if ("'"$partition_path"'" ~ /[0-9]p[1-4]$/) {
            print "primary"
        } else {
            print "extended"
        }
    } else if ("'"$partition_path"'" ~ /[0-9]p?[5-9][0-9]*$/) {
        print "logical"
    } else {
        print "unknown"
    }
}'
```

Replace `/dev/sda1` with the specific partition path the user provides. The script will output "primary," "extended," or "logical" accordingly.

#### Checking Free Space

To check how much free space is available on the disk run `sudo parted /dev/sda print free`.

Example output:

```
Model: ATA Disk (scsi)
Disk /dev/sda: 500GB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags: 

Number  Start   End     Size    File system  Name                  Flags
        17,4kB  1049kB  1031kB  Free Space
 1      1049kB  538MB   537MB   fat32        EFI System Partition  boot, esp
 2      538MB   500GB   500GB   ext4
        500GB   500GB   1056kB  Free Space
```

The `Free Space` line indicates unallocated space. In this case **1056kB**.

#### Creating a New Partition

Let's assume we currently have the following primary partitions: `/dev/sda1` and `/dev/sda2`. We want to create a new partition layout with /dev/sda3 as a primary partition, `/dev/sda4` as an extended partition, and `/dev/sda5` through `/dev/sda7` as logical partitions within the extended partition. To accomplish this, you can use partitioning tools such as `parted`, `fdisk`, or `gdisk`. Below are the steps for each tool:

##### Using `parted`

I. Start `parted`

```bash
sudo parted /dev/sda
```

II. Create the Third Primary Partition (`/dev/sda3`)**

```bash
(parted) mkpart primary ext4 40GiB 60GiB
```

- This creates `/dev/sda3` as a primary partition of type ext4, starting at 40GiB and ending at 60GiB. Adjust the sizes as needed.
- There should be confirmation of the partition creation.

III. Create the Extended Partition (`/dev/sda4`)

```bash
(parted) mkpart extended 60GiB 100%
```

- This creates `/dev/sda4` as an extended partition, starting at 60GiB and occupying the rest of the disk.
- There should be confirmation of the extended partition creation.

IV. Create Logical Partitions (`/dev/sda5`, `/dev/sda6`, `/dev/sda7`)

```bash
(parted) mkpart logical ext4 60GiB 70GiB
(parted) mkpart logical ext4 70GiB 80GiB
(parted) mkpart logical ext4 80GiB 90GiB
```

- This creates logical partitions `/dev/sda5`, `/dev/sda6`, and `/dev/sda7` within the extended partition, each with 10GiB of space.
- There should be confirmation for each logical partition creation.

V. Exit `parted`

```bash
(parted) quit
```

##### Using `fdisk`

I. Start `fdisk`

```bash
sudo fdisk /dev/sda
```

II. Create the Third Primary Partition (`/dev/sda3`)

```bash
Command (m for help): n
```

- Select `primary` and choose partition number `3`.
- There should be a prompt to enter the start and end sectors.
- Define Start and End for `/dev/sda3`
  - Start: +40G
  - End: +60G
- There should be confirmation of `/dev/sda3` creation.

III. Create the Extended Partition (`/dev/sda4`)**

```bash
Command (m for help): n
```

- Select `extended` and choose partition number `4`.
- There should be a prompt to enter the start and end sectors.

- Define Start and End for `/dev/sda4`
  - Start: +60G
  - End: (use default or specify end manually, e.g., 100G for the entire disk)
- There should be confirmation of `/dev/sda4` creation.

IV. Create Logical Partitions (`/dev/sda5`, `/dev/sda6`, `/dev/sda7`)

```bash
Command (m for help): n
```

- Select `logical` and create each partition one by one.
- Define Start and End for `/dev/sda5`
  - Start: +60G
  - End: +70G
- Define Start and End for `/dev/sda6`
  - Start: +70G
  - End: +80G
- Define Start and End for `/dev/sda7`
  - Start: +80G
  - End: +90G
- There should be confirmation of each logical partition creation.

V. Write Changes

```bash
Command (m for help): w
```

- Writes the changes to the disk and exits `fdisk`.

##### Using `gdisk`

I. Start `gdisk`

```bash
sudo gdisk /dev/sda
```

II. Create the Third Primary Partition (`/dev/sda3`)

```bash
Command (? for help): n
```

- Follow prompts to set partition number `3`, starting sector, and ending sector.
- Example Input:
  - Partition number: 3
  - First sector: +40G
  - Last sector: +60G
- There should be confirmation of `/dev/sda3` creation.

III. Create the Extended Partition (`/dev/sda4`)**

```bash
Command (? for help): n
```

- Follow prompts to set partition number `4`, starting sector, and ending sector.
- Example Input:
  - Partition number: 4
  - First sector: +60G
  - Last sector: +100G (or end of disk)
- There should be confirmation of `/dev/sda4` creation.

IV. Create Logical Partitions (`/dev/sda5`, `/dev/sda6`, `/dev/sda7`)

```bash
Command (? for help): n
```

- Follow prompts to create logical partitions within the extended partition.
- Example Input:
  - `/dev/sda5`: +60G to +70G
  - `/dev/sda6`: +70G to +80G
  - `/dev/sda7`: +80G to +90G
- There should be confirmation of each logical partition creation.

V. Write Changes

```bash
Command (? for help): w
```

This writes changes to disk and exits `gdisk`.

#### Resizing Partitions

Resizing partitions involves either expanding or shrinking an existing partition. This can be done using tools like `parted`, `fdisk`, and `gdisk`, though some tools are better suited for certain tasks. Here are the detailed steps and considerations for each tool:

##### Using `parted`

I. Start `parted`

```bash
sudo parted /dev/sda
```

II. Check Partition Table

```bash
(parted) print
```

This lists all partitions and their details.

III. Resize Partition

```bash
(parted) resizepart PARTITION_NUMBER END
```

- `PARTITION_NUMBER` is the number of the partition to resize, and `END` specifies the new end point (e.g., `50GiB`).
- To resize `/dev/sda3` to end at 50GiB: `(parted) resizepart 3 50GiB`
- Confirm the resizing action. If the new size is smaller than the used space, `parted` will issue a warning or error.

IV. Exit `parted`

```bash
(parted) quit
```

##### Using `fdisk`

**Note:** `fdisk` does not support resizing partitions directly. You need to delete the partition and recreate it with the new size. This can be risky and should be done with caution.

I. Start `fdisk`

```bash
sudo fdisk /dev/sda
```

II. List Partitions

```bash
Command (m for help): p
```

This displays the current partition table.

III. Delete the Partition

```bash
Command (m for help): d
```

- Enter the number of the partition you want to delete.
- This deletes the specified partition. This action does not delete the data but removes the partition table entry.

IV. Recreate the Partition with New Size

```bash
Command (m for help): n
```

- Follow prompts to create a new partition, specifying the new start and end sectors.
- If recreating `/dev/sda3`:
  - Start: Same as the previous start sector
  - End: New desired end sector

V. Write Changes

```bash
Command (m for help): w
```

This writes the new partition table and exits `fdisk`.

VI. Resize Filesystem (if needed)

After resizing the partition, you may need to resize the filesystem to fill the new partition size using tools like `resize2fs` for ext4 filesystems.

##### Using `gdisk`

I. Start `gdisk`**

```bash
sudo gdisk /dev/sda
```

II. List Partitions

```bash
Command (? for help): p
```

This lists current partitions.

III. Delete the Partition

```bash
Command (? for help): d
```

- Enter the partition number to delete.
- This deletes the specified partition entry.

IV. Recreate the Partition with New Size

```bash
Command (? for help): n
```

- Follow prompts to recreate the partition with the desired new size.
- Recreate `/dev/sda3` with a different end sector.
- Confirm the creation of the new partition.

V. Write Changes

```bash
Command (? for help): w
```

This writes changes to disk and exits `gdisk`.

VI. Resize Filesystem (if needed)

Use appropriate filesystem tools (e.g., `resize2fs`) to resize the filesystem to fit the new partition size.

#### Removing Partitions

Removing partitions is a critical task that should be done carefully to avoid data loss. The process varies slightly depending on the tool you use (`parted`, `fdisk`, or `gdisk`). Below are the instructions for each tool, along with notes on the expected outputs.

##### Using `parted`

I. Start `parted`

```bash
sudo parted /dev/sda
```

II. Check Partition Table

```bash
(parted) print
```

This lists all partitions and their details.

III. Remove Partition

```bash
(parted) rm PARTITION_NUMBER
```

- Replace `PARTITION_NUMBER` with the number of the partition you want to delete (e.g., `3` for `/dev/sda3`).
- To remove `/dev/sda3`: `(parted) rm 3`
- There should be confirmation that the partition has been removed.

IV. Exit `parted`

```bash
(parted) quit
```

##### Using `fdisk`

I. Start `fdisk`

```bash
sudo fdisk /dev/sda
```

II. List Partitions

```bash
Command (m for help): p
```

This displays the current partition table.

III. Delete Partition

```bash
Command (m for help): d
```

- Enter the number of the partition you want to delete.
- To delete `/dev/sda3`, use `Partition number: 3`
- Confirm the deletion of the partition.

IV. Write Changes

```bash
Command (m for help): w
```

This writes the changes to the partition table and exits `fdisk`.

##### Using `gdisk`

I. Start `gdisk`

```bash
sudo gdisk /dev/sda
```

II. List Partitions

```bash
Command (? for help): p
```

This lists the current partitions.

III. Delete Partition

```bash
Command (? for help): d
```

- Enter the partition number to delete.
- To delete `/dev/sda3`, use `Partition number: 3`
- There should be confirmation of the partition deletion.

IV. Write Changes

```bash
Command (? for help): w
```

This writes the changes to the disk and exits `gdisk`.

#### Changing MBR to GPT using gdisk

Sometimes, there's a need to change a disk from one partition table format to another. For instance, converting an MBR disk to a GPT format can be done using tools like `gdisk` or `parted`. Here's how to do it with `gdisk`:
### Steps to Repartition a Disk Using gdisk with Expected Outputs

- To **check the current partition table**, use the command `gdisk -l /dev/sda`. The expected output will list the current partitions, including details such as partition number, start and end sectors, size, and type. For example:

```
GPT fdisk (gdisk) version 1.0.6

Partition table scan:
MBR: protective
BSD: not present
APM: not present
GPT: present

Found valid GPT with protective MBR; using GPT.
Disk /dev/sda: 20971520 sectors, 10.0 GiB
Logical sector size: 512 bytes
Disk identifier (GUID): B7D5F9E3-3A74-4F56-B0D7-FB65DE571EC7
Partition table holds up to 128 entries
First usable sector is 34, last usable sector is 20971486
Partitions will be aligned on 2048-sector boundaries
Total free space is 10265 sectors (5.0 MiB)

Number  Start (sector)    End (sector)  Size       Code  Name
 1          2048         20951039   10.0 GiB    8300  Linux filesystem
```

- **Backing up the current partition table** is essential and can be done with `sgdisk -b /backup/path/partition-table-backup /dev/sda`. A backup file should be created at the specified path, like `/backup/path/partition-table-backup`. This action does not produce a direct console output but ensures a backup is available for recovery.

- To **start gdisk for disk management**, execute `gdisk /dev/sda`. The initial prompt will indicate readiness for commands:

```
GPT fdisk (gdisk) version 1.0.6

Type device filename, or press <Enter> to exit: /dev/sda
Command (? for help):
```

- Access the **experts menu** by pressing 'x' at the prompt, which changes to:

```
Expert command (? for help):
```

- **Removing the GPT data structures** involves pressing 'z' in the experts menu. This action prompts:

```
About to wipe out GPT on /dev/sda. Proceed? (Y/N):
```

Confirm with 'y', then decide on blanking out the MBR:

```
Blank out MBR? (Y/N): 
```

After confirming with 'y', the result will be:

```
GPT data structures destroyed! You may now partition the disk using the 'n' command.
```

- **Creating a new GPT data structure** requires pressing 'n' and confirming the action:

```
Expert command (? for help): n

Creating new GPT data structure
Confirm creation of a new GPT by pressing 'y': Y
```

The system will acknowledge:

```
GPT data structures created successfully.
```

- During **partition creation**, use the 'n' command to define each partition. The prompt guides through the process:

```
Command (? for help): n
Partition number (1-128, default 1): 1
First sector (34-20971486, default = 2048) or {+-}size{KMGTP}:
Last sector (2048-20971486, default = 20971486) or {+-}size{KMGTP}: +1G
Current type is 'Linux filesystem'
Hex code or GUID (L to show codes, Enter = 8300): 
```

After defining the partitions, the prompt returns to:

```
Command (? for help):
```

- To **save changes and exit gdisk**, press 'w'. The command confirms the write operation:

```
Do you want to proceed? (Y/N): Y
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING PARTITIONS!!

Do you want to proceed? (Y/N): Y

OK; writing new GUID partition table (GPT) to /dev/sda.
The operation has completed successfully.
```

- **Verifying the new partition table** after a system restart can be done with `gdisk -l /dev/sda`. The output should reflect the newly created partitions, similar to:

```
GPT fdisk (gdisk) version 1.0.6

Partition table scan:
MBR: protective
BSD: not present
APM: not present
GPT: present

Found valid GPT with protective MBR; using GPT.
Disk /dev/sda: 20971520 sectors, 10.0 GiB
Logical sector size: 512 bytes
Disk identifier (GUID): 12345678-1234-1234-1234-1234567890AB
Partition table holds up to 128 entries
First usable sector is 34, last usable sector is 20971486
Partitions will be aligned on 2048-sector boundaries
Total free space is 1048576 sectors (512.0 MiB)

Number  Start (sector)    End (sector)  Size       Code  Name
 1          2048           2099199   1.0 GiB    8300  Linux filesystem
 2       2099200          20971519   9.0 GiB    8300  Linux filesystem
```

This output confirms that the new partitions are correctly set up.

🔴 Caution:

- It's crucial to back up any important data before proceeding with this operation, as changing the partition table format can lead to data loss.
- Ensure that your system supports GPT and UEFI (if you're planning to boot from the disk), as older systems with BIOS may not support GPT.

#### Important Notes

- **Backup Data** before modifying disk partitions to prevent data loss, as altering partitions can sometimes lead to accidental loss of important information.
- When managing disk partitions, **Resizing and Deleting Partitions** may be necessary if existing partitions occupy the space needed for new ones. To delete a partition, use the `d` command in tools like `gdisk` or `fdisk`. For resizing, you might need to create a new partition with the desired size using the `n` command and then delete the old partition.
- The **Partition Types** you select depend on specific needs, such as using a Linux filesystem or creating a swap space. Each partition type is identified by a unique code or identifier that defines its purpose and structure.
- **Administrative Privileges** are typically required when using partitioning tools, as these actions need root access. Therefore, commands are often prefixed with `sudo` to grant the necessary permissions.

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
