#### Q. What type of partition is used to store data and can be directly accessed by the system?

* [ ] Extended Partition
* [ ] Logical Partition
* [x] Primary Partition
* [ ] Volume Group
* [ ] Logical Volume

#### Q. How many primary partitions can be created on a hard drive using a traditional MBR partition scheme?

* [ ] 2
* [x] 4
* [ ] 6
* [ ] 8
* [ ] 16

#### Q. Which type of partition acts as a container for logical partitions?

* [ ] Primary Partition
* [ ] Logical Partition
* [x] Extended Partition
* [ ] Volume Group
* [ ] Physical Volume

#### Q. When an extended partition is created, what does it directly store?

* [ ] Data
* [ ] File Systems
* [x] Logical Partitions
* [ ] Boot Information
* [ ] Operating Systems

#### Q. What is the main advantage of using logical partitions?

* [ ] They automatically back up data.
* [ ] They increase the speed of data transfer.
* [ ] They provide additional protection for system files.
* [x] They allow for creating more than four partitions on a system.
* [ ] They improve the system’s boot time.

#### Q. In a Logical Volume Management (LVM) setup, what is a logical volume?

* [ ] A type of extended partition.
* [ ] A physical hard drive used in the volume group.
* [x] A virtual partition that is created within a volume group.
* [ ] A primary partition that has been converted to a secondary partition.
* [ ] A component that holds data temporarily.

#### Q. What component in LVM holds the physical storage devices?

* [ ] Logical Volume
* [ ] Volume Group
* [x] Physical Volume
* [ ] File System
* [ ] Logical Partition

#### Q. What happens to the logical volumes when a volume group is removed in LVM?

* [ ] They are automatically converted to primary partitions.
* [ ] They become part of a new volume group.
* [x] They are deleted, and data may be lost unless backed up.
* [ ] They are reformatted with a new file system.
* [ ] They are merged into a single volume.

#### Q. Which method is used to format a primary partition?

* [ ] Partition Table
* [ ] Logical Volume Manager
* [x] File System (e.g., NTFS, FAT32, ext4)
* [ ] Boot Manager
* [ ] Disk Cleanup Tool

#### Q. What does marking a primary partition as "active" indicate?

* [ ] It is used for storing backup files.
* [ ] It is part of an extended partition.
* [x] It contains the operating system that the computer should boot from.
* [ ] It is a placeholder for logical partitions.
* [ ] It has been encrypted for security.

#### Q. What is a volume group in LVM?

* [ ] A single physical hard drive.
* [ ] A type of extended partition.
* [x] A collection of physical volumes that are grouped together.
* [ ] A virtual partition within an extended partition.
* [ ] A file system used to manage data.

#### Q. What is the purpose of a physical volume in LVM?

* [ ] To act as a virtual partition within a volume group.
* [x] To provide physical storage space that is used in volume groups.
* [ ] To format partitions with a file system.
* [ ] To hold data temporarily before it is backed up.
* [ ] To serve as a backup for logical volumes.

#### Q. Which LVM component is responsible for creating and managing logical volumes?

* [ ] Volume Group
* [ ] Physical Volume
* [x] Logical Volume Manager (LVM)
* [ ] Partition Table
* [ ] File System

#### Q. What command in LVM is used to extend an existing logical volume?

* [ ] lvremove
* [ ] lvcreate
* [ ] lvdisplay
* [x] lvextend
* [ ] lvsnapshot

#### Q. How is a logical volume formatted?

* [ ] By converting it to a primary partition.
* [ ] By using the Disk Management tool in Windows.
* [ ] By creating a new volume group.
* [x] By applying a file system to it.
* [ ] By removing the volume group it belongs to.

#### Q. What is the benefit of using logical volumes over physical partitions?

* [ ] They are faster in terms of data transfer speed.
* [ ] They automatically back up data.
* [ ] They provide physical separation of data.
* [x] They allow for dynamic resizing and flexible management of storage.
* [ ] They improve system boot time.

#### Q. What must you do before removing a volume group in LVM?

* [ ] Convert all logical volumes to physical partitions.
* [ ] Backup all data from the logical volumes.
* [x] Remove or move all logical volumes from the volume group.
* [ ] Format all logical volumes with a new file system.
* [ ] Increase the size of the physical volumes.

#### Q. What is the maximum number of primary partitions that can be created on a hard drive using the MBR (Master Boot Record) partition scheme?

* [ ] 2
* [x] 4
* [ ] 6
* [ ] 8
* [ ] 16

#### Q. How much of the hard drive’s space is used by an extended partition in the MBR partition scheme?

* [ ] It takes up the entire drive.
* [x] It takes up a portion of the drive’s space and is not directly usable for data storage.
* [ ] It uses exactly half of the drive’s space.
* [ ] It uses all the space except for one primary partition slot.
* [ ] It is equal to the size of the logical partitions created within it.

#### Q. In an LVM setup, what is the relationship between a physical volume and a volume group?

* [ ] A physical volume is a virtual partition within a volume group.
* [ ] A volume group is a logical volume created from physical volumes.
* [x] A physical volume is a physical storage device that is included in a volume group.
* [ ] A volume group is a type of extended partition used to manage physical volumes.
* [ ] A physical volume is a collection of volume groups.

#### Q. What must be true about the total size of logical volumes in relation to the size of the physical volumes in LVM?

* [ ] The total size of logical volumes can exceed the size of physical volumes.
* [ ] The total size of logical volumes must exactly match the size of physical volumes.
* [x] The total size of logical volumes must be less than or equal to the combined size of physical volumes in the volume group.
* [ ] The total size of logical volumes must be double the size of physical volumes.
* [ ] The size of logical volumes is independent of the size of physical volumes.

#### Q. When creating a new partition, what should you ensure about the partition size in relation to the total drive capacity?

* [ ] The partition size can be larger than the total drive capacity.
* [x] The partition size must be less than or equal to the total drive capacity.
* [ ] The partition size must be exactly half of the total drive capacity.
* [ ] The partition size must be exactly the same as the total drive capacity.
* [ ] The partition size does not need to match the drive capacity.

#### Q. What is the effect of removing a primary partition from a hard drive?

* [ ] The data in the primary partition is preserved.
* [ ] The primary partition is converted to an extended partition.
* [x] The data in the primary partition is typically lost unless backed up, and the space becomes unallocated.
* [ ] The primary partition is merged with the extended partition.
* [ ] The data is automatically restored to a new partition.

#### Q. In LVM, what happens to the physical volume space when logical volumes are removed?

* [ ] The physical volume space is automatically resized.
* [ ] The space is converted into a new file system.
* [x] The space is reclaimed and can be used for other logical volumes or left unallocated.
* [ ] The physical volume is deleted.
* [ ] The space is locked and cannot be reused.

#### Q. What must be done before creating a new logical volume in LVM?

* [ ] Ensure that the total size of logical volumes is greater than the physical volume size.
* [ ] Format the physical volume with a new file system.
* [x] Create a volume group that includes the physical volumes.
* [ ] Delete existing logical volumes.
* [ ] Convert physical volumes into primary partitions.

#### Q. What is the maximum number of logical volumes that can be created within a single volume group in LVM?

* [ ] 4
* [ ] 16
* [ ] 64
* [ ] 256
* [x] There is no fixed limit; it depends on the system's resources and configuration.

#### Q. When resizing a logical volume in LVM, what must be considered?

* [ ] The size of the logical volume must be reduced to be less than the physical volume.
* [ ] The total size of logical volumes must always be equal to the size of the volume group.
* [ ] The physical volume size must be resized before resizing the logical volume.
* [x] The volume group must have sufficient free space to accommodate the resizing.
* [ ] The volume group size must be reduced to match the size of the logical volume.

#### Q. What is a common technique used to span a logical volume across multiple physical disks?

* [x] Logical Volume Management (LVM)
* [ ] Network File System (NFS)
* [ ] Partition Table
* [ ] File Allocation Table (FAT)
* [ ] Extended Partition

#### Q. In LVM, what term describes the process of combining multiple physical volumes into a volume group?

* [ ] Striping
* [x] Aggregation
* [ ] Mirroring
* [ ] Partitioning
* [ ] Fragmentation

#### Q. Which storage configuration provides data striping across multiple disks for improved read/write performance?

* [x] RAID 0
* [ ] RAID 1
* [ ] RAID 5
* [ ] RAID 10
* [ ] RAID 6

#### Q. What is the primary advantage of using RAID 5 in a multi-disk configuration?

* [ ] Increased write speed
* [ ] Mirrored data for redundancy
* [x] Balanced performance and redundancy with distributed parity
* [ ] Simplified storage management
* [ ] Highest capacity utilization

#### Q. When using LVM to manage logical volumes across multiple physical disks, what should be considered regarding space allocation?

* [ ] The total size of logical volumes must be less than the size of each individual physical volume.
* [ ] Logical volumes can exceed the size of the physical volumes they span.
* [x] The total size of logical volumes should not exceed the combined size of all physical volumes in the volume group.
* [ ] Each physical volume must be the same size.
* [ ] Logical volumes must be resized to match the size of the smallest physical volume.

#### Q. How does Network File System (NFS) interact with multiple physical disks on a server?

* [ ] NFS directly manages physical disks and partitions them.
* [x] NFS provides network access to files stored on the server's disks but does not manage the disks themselves.
* [ ] NFS aggregates multiple disks into a single network file system.
* [ ] NFS automatically mirrors data across multiple disks.
* [ ] NFS handles RAID configurations for physical disks.

#### Q. What is a key benefit of using NFS for file sharing across multiple servers?

* [ ] It increases physical disk performance.
* [ ] It simplifies RAID configuration.
* [x] It allows for centralized access and management of files across different servers.
* [ ] It directly combines storage capacity from multiple servers.
* [ ] It manages the logical volume resizing automatically.

#### Q. In a multi-server environment, how can storage be effectively managed to ensure high availability?

* [ ] By using a single NFS server with local disks.
* [ ] By configuring RAID 0 across all servers.
* [x] By implementing a clustered file system or distributed storage system that provides redundancy.
* [ ] By manually syncing files between servers.
* [ ] By using only physical disks without network access.

#### Q. What is a clustered file system and how does it relate to multi-server setups?

* [ ] A system that manages physical disks independently on each server.
* [ ] A file system that provides local storage for each server.
* [x] A file system designed to allow multiple servers to access the same storage as if it were local, providing high availability and redundancy.
* [ ] A system that exclusively uses NFS for file sharing.
* [ ] A method for partitioning physical disks across servers.

#### Q. When setting up a distributed storage system across multiple physical disks and servers, what is a critical consideration?

* [ ] Ensuring each disk is formatted with the same file system.
* [ ] The total storage capacity must be the same on all servers.
* [x] Properly managing data redundancy, load balancing, and network connectivity to avoid bottlenecks and ensure reliability.
* [ ] All disks must be of the same physical size.
* [ ] Each server should be configured with identical hardware specifications.

#### Q. What is the primary purpose of using Logical Volume Manager (LVM) in a multi-disk setup?

* [ ] To create and manage partitions on each disk individually.
* [ ] To directly handle network traffic and file sharing.
* [x] To abstract and aggregate multiple physical disks into flexible logical volumes, allowing dynamic resizing and management.
* [ ] To perform RAID operations on a single disk.
* [ ] To manage NFS configurations.

#### Q. What is a disk sector (logical block)?

* [ ] A physical platter on the disk
* [x] The smallest addressable unit of storage on a disk
* [ ] The partition table entry
* [ ] The filesystem metadata area
* [ ] A special cache area on SSDs

#### Q. How is a disk partition defined?

* [ ] By filesystem type only
* [ ] By mount point only
* [x] By a start block and an end block on the disk
* [ ] By a unique device letter or name
* [ ] By partition label alone

#### Q. How are physical disks numbered in Windows?

* [ ] Disk A, Disk B, Disk C
* [x] Disk 0, Disk 1, Disk 2
* [ ] Disk C, Disk D, Disk E
* [ ] Disk 1, Disk 2, Disk 3
* [ ] Disk A:, Disk B:, Disk C:

#### Q. In Linux, which device name corresponds to the second SCSI disk?

* [x] `/dev/sdb`
* [ ] `/dev/sda2`
* [ ] `/dev/hdb`
* [ ] `/dev/nda`
* [ ] `/dev/vdb`

#### Q. How does Windows mount partitions?

* [ ] As directory paths under `/mnt/`
* [x] As drive letters (e.g. C:, D:)
* [ ] Using `fstab` entries
* [ ] By labeling volumes only
* [ ] By UUIDs in the registry

#### Q. Which Linux command lists all block devices and their partitions?

* [x] `lsblk`
* [ ] `mount`
* [ ] `df -h`
* [ ] `fdisk -l`
* [ ] `du`

#### Q. Can partitions on the same disk use different file systems?

* [ ] No, they must all match
* [x] Yes, each partition can be formatted independently
* [ ] Only if the disk is GPT
* [ ] Only on Windows
* [ ] Only on Linux

#### Q. If you see paths `/home/user1` and `/var/log` on Linux, could they be on different partitions?

* [ ] No, Linux uses a single root partition
* [x] Yes, each directory can be a separate mount point
* [ ] Only if `/etc/fstab` is misconfigured
* [ ] Only on enterprise distributions
* [ ] Only when using LVM

#### Q. You attach a new SCSI disk to Linux; it appears as `/dev/sdc`. What is the first partition likely named?

* [ ] `/dev/sdc0`
* [x] `/dev/sdc1`
* [ ] `/dev/sdca`
* [ ] `/dev/sdc01`
* [ ] `/dev/sdc-m1`

#### Q. Why is understanding partition and mount differences between Windows and Linux important?

* [x] It ensures you correctly locate and manage data across systems
* [ ] It only matters for SSDs, not HDDs
* [ ] It lets you convert NTFS to ext4 on the fly
* [ ] It’s only required for network shares
* [ ] It avoids using drive letters on Linux
