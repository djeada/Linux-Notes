## Partitioning Disks

Partitioning a disk involves dividing a physical storage device into separate, manageable sections called partitions. Each partition functions as an independent disk within the operating system, allowing for better organization, multi-boot setups, or separation of system files from user data. The two main partition table formats used to define how these partitions are structured on the disk are the Master Boot Record (MBR) and the GUID Partition Table (GPT).

Imagine your disk as a bookshelf divided into compartments:

```
+------------------+------------------+------------------+------------------+
|   Compartment 1  |   Compartment 2  |   Compartment 3  |   Free Space     |
|   (/dev/sda1)    |   (/dev/sda2)    |   (/dev/sda3)    |                  |
+------------------+------------------+------------------+------------------+
|    50 GB         |    100 GB        |     8 GB         |     42 GB        |
|    ext4          |    ext4          |     swap         |                  |
|    Mounted at /  |    Mounted at    |                  |                  |
|                  |      /home       |                  |                  |
+------------------+------------------+------------------+------------------+
```

In this illustration, the disk `/dev/sda` is divided into three partitions with varying sizes and purposes, and there's remaining free space available for future use.

In real-world scenarios, this setup could serve multiple purposes. For instance, different partitions might use different file systems tailored to their roles. A common choice is to use ext4 for both system files (`/`) and user data (`/home`), while swap space supports memory management.

Another practical use is on a shared server where several developers work. Here, each developer might get a separate partition or directory. This way, one developer's work won’t use up space meant for another, preventing conflicts and accidental data overwrites. The free space on the disk offers room for future expansion or for creating new partitions as project needs evolve.

### Basic Partition Operations

Several operations can be performed on disk partitions:

- If unallocated space exists on the disk, new partitions can be created to store data, install additional operating systems, or organize files.
- Removing a partition frees up space on the disk but also erases all data within that partition. It's essential to back up any important information before deletion.
- Adjusting the size of existing partitions can help optimize disk space usage. This may involve expanding a partition into adjacent free space or shrinking it to make room for new partitions.
- After creating a partition, it must be formatted with a filesystem (e.g., ext4, NTFS) to store files. Formatting prepares the partition for data storage.

### Relationship Between Physical Disks and Partitions

A physical disk is the actual hardware component that stores data. Partitions are logical divisions within this disk, allowing the operating system to manage different areas separately. Each partition can be treated as an independent disk with its own filesystem and mount point.

Visual representation:

```
+-------------------+
|   Physical Disk   |
|     (/dev/sda)    |
|                   |
|  +-------------+  |
|  | Partition 1 |  |
|  | (/dev/sda1) |  |
|  +-------------+  |
|  | Partition 2 |  |
|  | (/dev/sda2) |  |
|  +-------------+  |
|  | Partition 3 |  |
|  | (/dev/sda3) |  |
|  +-------------+  |
+-------------------+
```

Each partition is a segment of the physical disk that can be managed independently, formatted with different filesystems, and mounted at different points in the directory tree.

### Disk Naming Conventions

In Linux, disks and partitions are named using specific conventions to identify the device type, order, and partition number.

**Device Type Indicators**:

- `/dev/sdX` represents SCSI or SATA disks. The 'X' is a letter starting from 'a' for the first disk, 'b' for the second, and so on.
- `/dev/hdX` refers to older IDE disks.
- `/dev/vdX` denotes virtual disks in KVM environments.
- `/dev/xvdX` indicates virtual disks in Xen virtualization.

**Partition Numbers**:

Partitions are numbered starting from 1. For example, `/dev/sda1` is the first partition on the first disk.

Examples:

- The device **/dev/sda** refers to the system’s **first disk**, typically used for the primary operating system or main storage.
- **/dev/sdb** represents the **second disk**, which might be used for additional storage, backups, or separate partitions.
- Located on the first disk, **/dev/sda1** is the **first partition**, often reserved for essential system files or boot-related data.
- The **second partition** on the second disk is labeled **/dev/sdb2**, and it may be used for secondary storage, user files, or specific applications.

### Types of Partitions

#### Primary Partitions

Primary partitions are the main partitions on a disk. On an MBR-partitioned disk, you can have up to four primary partitions. These partitions are used to boot operating systems or store data.

**Creating a Primary Partition**:

- Use a partitioning tool like `fdisk` or `parted`.
- Allocate a portion of the disk's storage to the partition.
- Format the partition with a filesystem (e.g., `ext4`).

Example using `fdisk` to create a primary partition:

```bash
sudo fdisk /dev/sda
```

Inside `fdisk`:

```
Command (m for help): n
Partition type:
   p   primary (1 primary, 0 extended, 3 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-1048575999, default 2048): [Press Enter]
Last sector, +sectors or +size{K,M,G,T,P}: +50G
Created a new partition 1 of type 'Linux' and of size 50 GiB.
```

- A new primary Linux partition was created with a size of 50 GiB.
- It was assigned as partition number 1.
- The partition starts at the default first sector, which is 2048.

**Formatting the Partition**:

```bash
sudo mkfs.ext4 /dev/sda1
```

This action prepares the partition for use by creating an **ext4** filesystem structure on it.
  
#### Extended and Logical Partitions

Extended partitions are a workaround for the MBR limitation of four primary partitions. An extended partition acts as a container for logical partitions, allowing you to create more than four partitions on a disk.

**Creating an Extended Partition**:

Inside `fdisk`:

```
Command (m for help): n
Partition type:
   p   primary (3 primary, 1 extended, 0 free)
   e   extended
Select (default p): e
Partition number (1-4, default 4): 4
First sector (some value): [Press Enter]
Last sector, +sectors or +size{K,M,G,T,P}: [Press Enter to use remaining space]
Created a new extended partition 4.
```

- A new extended partition was created and labeled as partition number 4.
- Since there were already three primary partitions, the extended type (`e`) was selected.
- The first sector was set to the default by pressing Enter.
- The last sector was also set to default by pressing Enter, allowing the partition to use all remaining available space.

**Creating Logical Partitions Within the Extended Partition**:

```
Command (m for help): n
All primary partitions are in use
Adding logical partition 5
First sector (some value): [Press Enter]
Last sector, +sectors or +size{K,M,G,T,P}: +20G
Created a new logical partition 5 of type 'Linux' and of size 20 GiB.
```

- Since all primary partitions were already in use, a new logical partition was added.
- The partition was assigned as logical partition number 5.
- The first sector was set to the default by pressing Enter.
- The size of the partition was specified as 20 GiB by entering `+20G`.
- A new 20 GiB Linux logical partition, labeled as partition 5, was successfully created.

Repeat the process for additional logical partitions.

#### Comparison

Here's a comprehensive comparison of different partition types:

| **Feature**          | **Primary Partition**                                                             | **Extended Partition**                                                          | **Logical Partition**                                                             |
|----------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| **Definition**       | A main partition that can host an operating system or data directly.              | A special type of partition that acts as a container for logical partitions.    | A partition within an extended partition used to store data.                       |
| **Maximum Number**   | Up to 4 primary partitions per disk under MBR.                                    | Only 1 extended partition per disk under MBR (counts as one of the 4 primary).  | Numerous logical partitions can exist within the extended partition (limited by OS). |
| **Purpose**          | Used to install operating systems or store data directly.                         | Provides a way to bypass the limit of 4 primary partitions by containing logical partitions. | Allows the creation of additional partitions beyond the primary limit for organizing data. |
| **Bootability**      | Can be marked as active to boot an operating system (on MBR systems).             | Cannot be used to boot directly; it's a container.                              | Generally not bootable, but can be configured with bootloaders in some cases.       |
| **Storage Location** | Entries stored directly in the partition table within the MBR or GPT.             | Defined in the partition table but contains an extended boot record (EBR) for logical partitions. | Defined within EBRs linked in a chain inside the extended partition.               |
| **Limitations**      | Limited to 4 per disk under MBR (no limit under GPT).                             | Only one extended partition allowed per disk under MBR.                         | Number limited by available space and operating system constraints.                 |
| **Use Cases**        | Ideal for systems requiring multiple operating systems or separate data areas.    | Necessary when more than 4 partitions are needed on an MBR disk.                | Useful for organizing data into separate partitions beyond the primary partition limit. |
| **Deletion Impact**  | Deleting removes the partition and all its data.                                  | Deleting removes the extended partition and all contained logical partitions.   | Deleting removes only the specific logical partition and its data.                  |

### Partition Table Formats: MBR vs. GPT

Partition table formats are  organize data on storage devices, enabling the system to locate, identify, and manage different partitions on a disk. Two of the most widely used partition table formats are the Master Boot Record (MBR) and the GUID Partition Table (GPT). Each format comes with its own structure, limitations, and features, which affect how storage devices can be utilized and managed. While MBR is an older format, widely compatible across various operating systems, GPT is a newer standard designed to address the limitations of MBR, offering greater flexibility and scalability for modern storage needs.

#### Master Boot Record (MBR)

The Master Boot Record is the original partition table format, introduced in the 1980s, which has been the standard for decades. Located in the first sector of a storage device, the MBR holds the boot loader and information about the disk's partitions. However, MBR has some notable limitations: it supports a maximum disk size of 2 TB and can only create up to four primary partitions. For users needing more partitions, an extended partition must be created to hold additional logical partitions. Despite these limitations, MBR's simplicity and broad compatibility with older systems make it a popular choice for users and devices that do not require large storage capacities or numerous partitions.

#### GUID Partition Table (GPT)

The GUID Partition Table was developed as a modern replacement for MBR, overcoming many of its restrictions. GPT is part of the Unified Extensible Firmware Interface (UEFI) standard and supports much larger disks, theoretically up to 9.4 zettabytes, with practically unlimited partition counts. Each partition in GPT is identified by a globally unique identifier (GUID), enhancing flexibility and reducing the likelihood of partition-related conflicts. Additionally, GPT maintains multiple copies of its partition table for improved data redundancy and recovery, making it more reliable than MBR. GPT has become the preferred choice for newer systems, particularly those requiring large storage capacities or more than four partitions, and is increasingly supported by most modern operating systems.

Comparison Table:

| Feature                    | MBR                            | GPT                                |
|----------------------------|--------------------------------|------------------------------------|
| Max Disk Size              | 2 TB                           | 9.4 ZB                             |
| Max Partitions             | 4 primary partitions           | 128 partitions (default)           |
| Data Redundancy            | No                             | Yes (multiple partition tables)    |
| Error Checking             | None                           | CRC32 checksums                    |
| Boot Mode                  | BIOS                           | UEFI                               |
| Compatibility              | Older systems                  | Modern systems                     |

### Operations in `gdisk` and `fdisk`

Both `gdisk` and `fdisk` are powerful command-line tools used for disk partitioning, `gdisk` is designed for GPT disks, while `fdisk` traditionally works with MBR disks but now supports GPT as well. Below is a table summarizing the key operations available in each tool.

#### `gdisk` Operations

| **Command** | **Description**                                          |
|-------------|----------------------------------------------------------|
| `p`         | Display the current partition table.                     |
| `n`         | Create a new partition.                                  |
| `d`         | Delete a partition.                                      |
| `t`         | Change a partition's type code.                          |
| `l`         | List known partition types.                              |
| `w`         | Write changes to disk and exit.                          |
| `q`         | Quit without saving changes.                             |
| `x`         | Enter expert mode for advanced options.                  |
| `?`         | Display help information.                                |
| `i`         | Show detailed information about a partition.             |
| `o`         | Create a new empty GUID partition table (GPT).           |
| `r`         | Enter recovery and transformation mode.                  |

#### `fdisk` Operations

| **Command** | **Description**                                          |
|-------------|----------------------------------------------------------|
| `p`         | Display the partition table.                             |
| `n`         | Add a new partition.                                     |
| `d`         | Delete a partition.                                      |
| `t`         | Change a partition's system ID (type).                   |
| `l`         | List known partition types.                              |
| `w`         | Write changes to disk and exit.                          |
| `q`         | Quit without saving changes.                             |
| `m`         | Display help menu.                                       |
| `a`         | Toggle a bootable flag on a partition.                   |
| `v`         | Verify the partition table for errors.                   |
| `x`         | Enter expert mode for advanced options.                  |
| `g`         | Create a new empty GPT partition table.                  |

### Managing Disk Partitions

#### Viewing Partition Tables

To inspect the partition table of a disk, we use previously introduced tools `fdisk`, `parted`, or `gdisk`.

##### Using `fdisk`

```bash
sudo fdisk -l /dev/sda
```

Example output:

```
Disk /dev/sda: 500 GiB, 536870912000 bytes, 1048576000 sectors
Disk model: ST500DM002-1BD14
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
Disklabel type: dos
Disk identifier: 0x12345678

Device     Boot   Start        End    Sectors   Size Id Type
/dev/sda1          2048  104857599 104855552    50G 83 Linux
/dev/sda2     104857600 209715199 104857600    50G 83 Linux
```

- The disk `/dev/sda` is 500 GiB in size.
- It uses the `dos` partition table format (MBR).
- There are two primary partitions: `/dev/sda1` and `/dev/sda2`.

##### Using `parted`

`parted` is another tool that can be used to inspect the partition table, particularly helpful for both MBR and GPT partition tables. 

To view the partition table with `parted`, use the following command:

```bash
sudo parted /dev/sda print
```

Example output:

```
Model: ATA ST500DM002-1BD14 (scsi)
Disk /dev/sda: 500GB
Sector size (logical/physical): 512B/4096B
Partition Table: msdos
Disk Flags: 

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  50.0GB  50.0GB  primary  ext4
 2      50.0GB  100GB   50.0GB  primary  ext4
```

- Here, the disk `/dev/sda` is 500GB.
- It uses the `msdos` partition table format.
- There are two primary partitions listed, each formatted with the `ext4` filesystem.

##### Using `gdisk`

`gdisk` is a tool similar to `fdisk` but designed specifically for GPT partition tables. It’s particularly useful for disks larger than 2 TB or when using UEFI-based systems.

To view the partition table with `gdisk`, use the following command:

```bash
sudo gdisk -l /dev/sda
```

Example output:

```
GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: not present
  BSD: not present
  APM: not present
  GPT: present

Disk /dev/sda: 1048576000 sectors, 500.0 GiB
Logical sector size: 512 bytes
Disk identifier (GUID): D2AC4D27-567A-4E2B-8A6F-3BC66E42DAF7
Partition table holds up to 128 entries
First usable sector is 34, last usable sector is 1048575966
Partitions will be aligned on 2048-sector boundaries

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048        104857599   50.0 GiB    8300  Linux filesystem
   2       104857600       209715199   50.0 GiB    8300  Linux filesystem
```

- This disk `/dev/sda` is formatted with a GPT partition table.
- There are two partitions, each assigned the Linux filesystem type.
- The disk can accommodate up to 128 partitions and supports large disks (over 2 TB). 

#### Checking Free Space

To check for unallocated space on a disk—space that hasn’t been assigned to any partition—you can use tools like `fdisk`, `parted`, and `lsblk`. These utilities show information about partitions and any remaining unallocated space on the disk.

##### Using `fdisk`

With `fdisk`, you can view both existing partitions and unallocated space. When you use `fdisk -l`, it lists the partitions on the disk, and at the end, any unallocated space will be noted.

```bash
sudo fdisk -l /dev/sda
```

Example output:

```
Disk /dev/sda: 500 GiB, 536870912000 bytes, 1048576000 sectors
Disk model: ST500DM002-1BD14
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
Disklabel type: dos
Disk identifier: 0x12345678

Device     Boot   Start        End    Sectors   Size Id Type
/dev/sda1          2048  104857599 104855552    50G 83 Linux
/dev/sda2     104857600 209715199 104857600    50G 83 Linux

Disk /dev/sda has 400 GiB of unallocated space.
```

- This shows that `/dev/sda` has 500 GB in total, with two partitions, and it indicates unallocated space.
- You can see that the remainder of the disk (400 GB) is unallocated.

##### Using `parted`

`parted` also displays unallocated space, making it a useful tool to confirm if your disk has unused space.

```bash
sudo parted /dev/sda print free
```

Example output:

```
Model: ATA ST500DM002-1BD14 (scsi)
Disk /dev/sda: 500GB
Sector size (logical/physical): 512B/4096B
Partition Table: msdos
Disk Flags: 

Number  Start   End     Size    Type     File system  Flags
        0.00B  1049kB  1049kB            Free Space
 1      1049kB  50.0GB  50.0GB  primary  ext4
 2      50.0GB  100GB   50.0GB  primary  ext4
        100GB   500GB   400GB            Free Space
```

- The `print free` option in `parted` shows both allocated and unallocated space.
- This example shows 400 GB of free space starting from 100 GB to the end of the disk.

##### Using `lsblk`

`lsblk` doesn’t directly show unallocated space, but by listing only mounted filesystems and partitions, it indirectly indicates where unallocated space might be found on a disk.

```bash
lsblk
```

Example output:

```
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0   500G  0 disk 
├─sda1   8:1    0    50G  0 part /
└─sda2   8:2    0    50G  0 part /home
```

- Here, `lsblk` shows that `/dev/sda` has a total size of 500 GB.
- With only 100 GB used across two partitions, we can infer that the remaining space (400 GB) is unallocated. 

#### Creating a New Partition

Here’s how to create a new partition on `/dev/sda`:

##### Using `fdisk`

I. Open `fdisk`:

```bash
sudo fdisk /dev/sda
```

II. List Current Partitions:

Once in `fdisk`, type `p` and press Enter to view the current partition table.

III. Create a New Partition:

- Type `n` to create a new partition.
- `p` for a primary partition.
- `e` for an extended partition (if you need more than four primary partitions on an MBR disk).
- Specify the partition number if prompted (you can usually press Enter to select the next available number).
- Choose the starting sector (press Enter to accept the default starting position).
- Specify the size by entering `+size`, for example, `+50G` for a 50 GB partition.

IV. Write the Changes:

Type `w` to write the changes to the disk and exit `fdisk`.

V. Verify the New Partition:

Use `lsblk` or `sudo fdisk -l` to confirm that the new partition has been created.

##### Using `parted`

I. Open `parted`:

```bash
sudo parted /dev/sda
```

II. Set Disk Label (Optional):


```bash
mklabel gpt
```

III. Create the Partition:

```bash
mkpart primary ext4 100GB 150GB
```

This creates a primary partition formatted as `ext4` starting at 100 GB and ending at 150 GB.

IV. Type `quit` to exit `parted`.

V. Format the Partition (Optional):

```bash
sudo mkfs.ext4 /dev/sda3
```

##### Using `gdisk`

I. Open `gdisk`:

```bash
sudo gdisk /dev/sda
```

II. Create a New Partition:

- In `gdisk`, type `n` to create a new partition.
- Specify the partition number (or press Enter to select the next available).
- Choose the starting sector and size, similar to `fdisk`.
- Assign a partition type code if needed (e.g., `8300` for Linux filesystems).

III. Write the Changes:

Type `w` to write the changes to the disk and exit `gdisk`.

After creating the partition, you may need to format it and add it to `/etc/fstab` for automatic mounting on boot. To format it, you can use a command such as:

```bash
sudo mkfs.ext4 /dev/sda3
```

To mount it immediately, create a mount point and mount the partition:

```bash
sudo mkdir /mnt/newpartition
sudo mount /dev/sda3 /mnt/newpartition
```

#### Resizing Partitions

Resizing partitions involves careful steps to avoid data loss.

##### Shrinking a Partition

- Before making any changes, it’s essential to create a **backup** of important data to prevent potential data loss.
- To shrink the filesystem, utilize **tools** specific to the filesystem type; for example, `resize2fs` is suitable for **ext4** filesystems.

```bash
sudo resize2fs /dev/sda1 40G
```

Following the filesystem shrink, use **partition** management tools such as `fdisk` or `parted` to modify the partition size.

```bash
sudo fdisk /dev/sda
```

Inside `fdisk`, you will need to **delete** the existing partition and recreate it, specifying the new, smaller size and ensuring it starts at the **same sector** as the original.

##### Expanding a Partition

- To increase the partition size, adjust the **partition** to encompass additional available space using `fdisk` or `parted`.
- After resizing the partition, use filesystem tools like **resize2fs** to expand the filesystem to fill the entire resized partition.

```bash
sudo resize2fs /dev/sda1
```

**General Tips for Partition Resizing**:

- Always **verify** that the new partition size is accurate before applying changes, as incorrect sizing can lead to **data loss** or corruption.
- It's advisable to **unmount** the partition (if possible) prior to resizing operations to avoid potential **errors**.
- After resizing, use the **fsck** (filesystem check) tool to check the filesystem's **integrity**, ensuring it operates correctly.

```bash
sudo fsck /dev/sda1
```

**Post-Resize Checks**:

- Run a **health check** on the disk and partition after resizing to confirm everything is functioning as expected.
- If the partition is used by the **operating system**, it may be necessary to **reboot** for changes to take effect fully.

#### Deleting Partitions

Here’s how to delete a partition, for example, `/dev/sda3`:

##### Using `fdisk` to Delete a Partition

I. Open `fdisk`:

```bash
sudo fdisk /dev/sda
```

II. List Partitions:

Type `p` and press Enter to view the current partitions and identify the one you want to delete.

III. Delete the Partition:

- Type `d` to delete a partition.
- You will be prompted to enter the partition number. Enter the number of the partition you wish to delete (e.g., `3` for `/dev/sda3`).
- If you only have one partition, it will delete that automatically.

IV. Write the Changes:

Type `w` to write the changes and exit `fdisk`. This action removes the partition from the partition table.

V. Verify the Deletion:

Use `lsblk` or `sudo fdisk -l` to confirm the partition has been deleted.

##### Using `parted` to Delete a Partition

I. Open `parted`:

```bash
sudo parted /dev/sda
```

II. List Partitions:

Type `print` to view the partition table and locate the partition you want to delete.

III. Delete the Partition:

```bash
rm 3
```

IV. Quit `parted`:

- Type `quit` to exit `parted`.
V. Verify the Deletion:
- Use `lsblk` or `sudo parted /dev/sda print` to ensure the partition is removed.

##### Using `gdisk` to Delete a Partition

I. Open `gdisk`:

```bash
sudo gdisk /dev/sda
```

II. Delete the Partition:

- Type `d` and press Enter to delete a partition.
- Enter the partition number you want to delete (e.g., `3` for `/dev/sda3`).

III. Write the Changes:

Type `w` to write the changes to the disk and exit `gdisk`. Confirm the changes when prompted.

IV. Verify the Deletion:

Use `lsblk` or `sudo gdisk -l /dev/sda` to confirm the partition has been removed.

**Note:** Deleting a partition will remove all data on that partition. Make sure to back up any important data before proceeding with the deletion process.

### Practical Examples and Commands

#### Listing All Disks and Partitions

The `lsblk` command provides a detailed overview of all block devices, including disks and partitions, and their mount points.

```bash
lsblk -o NAME,MAJ:MIN,RM,SIZE,RO,TYPE,MOUNTPOINT
```

Example output:

```
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0 465.8G  0 disk
├─sda1   8:1    0    50G  0 part /
├─sda2   8:2    0    50G  0 part /home
└─sda3   8:3    0   100G  0 part /data
```

Here, each disk and partition is displayed with its size, type, and mount point. `sda` is the primary disk, with `sda1`, `sda2`, and `sda3` as its partitions.

#### Formatting and Mounting a New Partition

After creating a new partition, such as `/dev/sda3`, you need to format it and then mount it to make it accessible.

**Formatting**:

```bash
sudo mkfs.ext4 /dev/sda3
```

This command formats the partition `/dev/sda3` with the `ext4` filesystem. Ensure you’ve chosen the correct filesystem for your needs (e.g., `ext4`, `xfs`, etc.).

**Creating a Mount Point**:

```bash
sudo mkdir /mnt/data
```

This creates a directory (`/mnt/data`) where the partition will be mounted, allowing access to its contents from that location.

**Mounting the Partition**:

```bash
sudo mount /dev/sda3 /mnt/data
```

Mounting attaches the `/dev/sda3` partition to the `/mnt/data` directory, making it accessible as part of the file system.

**Verifying the Mount**:

```bash
df -h | grep sda3
```

Example output:

```
/dev/sda3       99G   60M   94G   1% /mnt/data
```

The `df -h` command provides details about the mounted partition, showing the used and available space. The output confirms that `/dev/sda3` is mounted on `/mnt/data`.

#### Adding the Partition to `/etc/fstab`

To ensure that the partition mounts automatically at boot, add an entry to the `/etc/fstab` file. This file defines how disk partitions, block devices, and remote filesystems are mounted.

**Get the UUID**:

```bash
sudo blkid /dev/sda3
```

Example output:

```
/dev/sda3: UUID="abcd-1234" TYPE="ext4" PARTUUID="12345678-03"
```

The `blkid` command displays the UUID for each partition. UUIDs are unique identifiers for partitions, making them more reliable than device names, as device names can change between boots.

**Edit `/etc/fstab`**:

```bash
sudo nano /etc/fstab
```

This opens the `/etc/fstab` file in a text editor (like `nano`). You can add an entry for the new partition to ensure it mounts automatically at boot.

Add the following line:

```
UUID=abcd-1234   /mnt/data   ext4   defaults   0   2
```

- `UUID=abcd-1234` specifies the UUID for the partition.
- `/mnt/data` is the directory where the partition will be mounted.
- `ext4` specifies the filesystem type.
- `defaults` are mount options (e.g., read/write permissions).
- `0` is a flag for whether the partition should be dumped (typically set to `0`).
- `2` sets the order for filesystem checks at boot, where `2` means it will be checked after the root filesystem.

After saving and exiting, you can run `sudo mount -a` to apply changes immediately.
### Changing MBR to GPT Using gdisk

Converting a disk's partition table from the Master Boot Record (MBR) format to the GUID Partition Table (GPT) can unlock new capabilities, such as supporting disks larger than 2 terabytes and allowing more than four primary partitions. The `gdisk` utility is a powerful tool that facilitates this conversion while aiming to preserve your existing data. In this comprehensive guide, we'll walk through the process of changing an MBR partition table to GPT using `gdisk`, providing detailed explanations and interpretations at each step.

#### Preparing for the Conversion

Converting from MBR to GPT is a significant operation that can potentially lead to data loss if not done carefully. Proper preparation is crucial.

- Before making any changes, back up all important data on the disk. While `gdisk` is designed to convert partition tables without losing data, unexpected issues can occur.
- Ensure that your system's firmware (BIOS/UEFI) supports GPT. Most modern systems with UEFI firmware can boot from GPT disks. Older BIOS systems may require additional steps, like creating a BIOS boot partition.

#### Step 1: Examine the Current Partition Table

Start by inspecting the existing partition table to understand the current disk layout.

```bash
sudo gdisk -l /dev/sda
```

**Example Output:**

```
GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: MBR only
  BSD: not present
  APM: not present
  GPT: not present

Found valid MBR with protective or hybrid GPT; converting MBR to GPT format in memory.
This operation may not preserve existing partitions.

Disk /dev/sda: 20971520 sectors, 10.0 GiB
Sector size (logical/physical): 512 bytes / 512 bytes
Disk identifier (GUID): FFFFEEEE-DDDD-CCCC-BBBB-AAAA99998888
Partition table holds up to 128 entries
First usable sector is 34, last usable sector is 20971486
Total free space is 0 sectors (0 bytes)

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048        20971519   10.0 GiB    0700  Microsoft basic data
```

- The disk `/dev/sda` currently uses the MBR partitioning scheme.
- There's one primary partition occupying the entire disk.
- `gdisk` is ready to convert the MBR partition table to GPT in memory.

#### Step 2: Launch gdisk Interactive Mode

Run `gdisk` to interactively convert the partition table.

```bash
sudo gdisk /dev/sda
```

**Example Output:**

```
GPT fdisk (gdisk) version 1.0.5

Type 'help' or '?' to view a list of commands.

Command (? for help):
```

- You've entered `gdisk`'s interactive prompt.
- You can now issue commands to modify the partition table.

#### Step 3: Review the Existing Partition Table

Before making changes, it's wise to review the current partitions.

At the `gdisk` prompt, type:

```
p
```

**Example Output:**

```
Disk /dev/sda: 20971520 sectors, 10.0 GiB
Sector size (logical/physical): 512 bytes / 512 bytes
Disk identifier (GUID): A1B2C3D4-E5F6-7890-1234-56789ABCDEF0
Partition table holds up to 128 entries

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048        20971519   10.0 GiB    0700  Microsoft basic data
```

- Confirms the presence of a single partition spanning the entire disk.
- The partition code `0700` indicates a Microsoft basic data partition.

#### Step 4: Write the New GPT Partition Table

To apply the GPT format, write the changes to the disk.

At the `gdisk` prompt, type:

```
w
```

**Example Output:**

```
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING PARTITIONS!!

Do you want to proceed? (Y/N): y
```

- `gdisk` warns that writing the GPT data will overwrite the existing MBR partition table.
- Typing `y` confirms that you want to proceed.

After confirmation, you should see:

```
OK; writing new GUID partition table (GPT) to /dev/sda.
The operation has completed successfully.
```

- The new GPT partition table has been successfully written to the disk.
- You can now exit `gdisk`.

#### Step 5: Verify the Conversion

Confirm that the disk now uses the GPT partitioning scheme.

```bash
sudo gdisk -l /dev/sda
```

**Example Output:**

```
GPT fdisk (gdisk) version 1.0.5

Disk /dev/sda: 20971520 sectors, 10.0 GiB
Sector size (logical/physical): 512 bytes / 512 bytes
Disk identifier (GUID): B123C456-D789-0E12-3456-7890ABCDEF12
Partition table holds up to 128 entries

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048        20971519   10.0 GiB    8300  Linux filesystem
```

- The disk now has a GPT partition table.
- The existing partition is preserved and recognized as a GPT partition.
- The partition code `8300` indicates a Linux filesystem.

#### Step 6: Adjust Partition Types (If Necessary)

Depending on your system, you may need to adjust the partition type codes.

At the `gdisk` prompt, type:

```
t
```

You'll be prompted to enter the partition number:

```
Partition number (1-1): 1
```

Then enter the new hex code:

```
Hex code or GUID (L to show codes, Enter = 8300): 8300
```

- Ensures that the partition type is set correctly for your operating system.
- You can list available codes by typing `L` at the prompt.

#### Step 7: Create a BIOS Boot Partition (For BIOS Systems)

If your system uses BIOS (not UEFI), you'll need a BIOS boot partition to boot from a GPT disk.

At the `gdisk` prompt, create a new partition:

```
n
```

**Example Input:**

| Option            | Action                                            |
|-------------------|---------------------------------------------------|
| Partition Number  | Press Enter to accept the default.                |
| First Sector      | Press Enter to accept the default.                |
| Last Sector       | `+1M` (creates a 1 MB partition).                 |
| Hex Code          | `ef02` (BIOS boot partition).                     |

**Example Output:**

```
Command (? for help): n
Partition number (2-128, default 2): [Press Enter]
First sector (34-2047, default = 34) or {+-}size{KMGTP}: [Press Enter]
Last sector (2048-2047, default = 2047) or {+-}size{KMGTP}: +1M
Current type is 'Linux filesystem'
Hex code or GUID (L to show codes, Enter = 8300): ef02
Changed type of partition to 'BIOS boot partition'
```

- A small BIOS boot partition is created at the beginning of the disk.
- This partition is required for GRUB to boot from a GPT disk on BIOS systems.

#### Step 8: Write Changes and Exit gdisk

Save the changes to the disk.

At the `gdisk` prompt, type:

```
w
```

Confirm when prompted:

```
Do you want to proceed? (Y/N): y
```

**Example Output:**

```
OK; writing new GUID partition table (GPT) to /dev/sda.
The operation has completed successfully.
```

#### Step 9: Reinstall the Bootloader

Since the partition table has changed, you need to reinstall the bootloader.

For GRUB on BIOS systems:

```bash
sudo grub-install /dev/sda
```

**Example Output:**

```
Installing for i386-pc platform.
Installation finished. No error reported.
```

- GRUB is reinstalled to work with the new GPT partition table.
- No errors indicate a successful installation.

#### Step 10: Update the Filesystem Table (fstab)

Ensure that the `/etc/fstab` file references the correct partitions.

Use `blkid` to find the new UUIDs:

```bash
sudo blkid
```

Update `/etc/fstab` accordingly.

#### Step 11: Reboot and Test

Reboot the system to verify that everything works correctly.

```bash
sudo reboot
```

- If the system boots without issues, the conversion was successful.
- If problems occur, you may need to troubleshoot bootloader configurations.

#### Visual Representation of the Conversion

To better understand the process, here's a simplified visual:

Before Conversion (MBR):

```
+-----------------------+
|       MBR Disk        |
|-----------------------|
| MBR Partition Table   |
|                       |
| +-------------------+ |
| |   /dev/sda1       | |
| |   Primary         | |
| |   Linux           | |
| +-------------------+ |
|                       |
+-----------------------+
```

After Conversion (GPT):

```
+-----------------------+
|       GPT Disk        |
|-----------------------|
| GPT Partition Table   |
|                       |
| +-------------------+ |
| |   /dev/sda1       | |
| |   Linux Filesystem| |
| +-------------------+ |
| +-------------------+ |
| |   /dev/sda2       | |
| |   BIOS Boot Part. | |
| +-------------------+ |
|                       |
+-----------------------+
```

- The disk now uses GPT, with the original partition preserved.
- A new BIOS boot partition is added for bootloader compatibility.

### Safety Precautions

- Always back up important data before making changes.
- Unmount partitions before resizing or deleting.
- For system partitions, use a live CD/USB to make changes.
- Verify commands and parameters to avoid mistakes.
- Ensure you're familiar with the tools and steps involved.

### Common Errors and Troubleshooting

#### Error: "Partition in Use"

- The **cause** of this error is usually that the partition is mounted or actively in use by the system. 
- To resolve this, unmount the partition by running:

```bash
sudo umount /dev/sda1
```

It’s also advisable to **close** any applications or services currently using the partition, as they can prevent the partition from unmounting properly.

#### Error: "No Free Sectors Available"

This error generally occurs when there is **no unallocated space** left on the disk. To address this, you can either shrink existing partitions to **create free space** or, if needed, upgrade to a larger disk or use additional storage to accommodate the expansion.

#### Error: "Filesystem Check Required"

- Filesystem inconsistencies after resizing can prompt this error.
- To fix it, run a **filesystem check and repair** with the following command:

```bash
sudo fsck -f /dev/sda1
```

This command performs a comprehensive **scan and repair** of the filesystem, helping to restore it to a consistent state after any partition resizing activities.

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
