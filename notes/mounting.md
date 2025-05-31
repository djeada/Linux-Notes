## Mounting and Unmounting

If you come from a Windows world, the idea of mounting might sound strange at first, since Linux handles storage devices and filesystems quite differently. In Linux, "mounting" is the process of making a storage device (such as a hard disk partition, USB drive, or network share) accessible within the filesystem hierarchy. Here’s a brief overview:

**What Can Be Mounted:**

- Hard disk partitions, SSDs, optical drives, and USB flash drives.  
- Shares via NFS (Network File System) or SMB/CIFS (used by Windows shares).  
- Special pseudo-filesystems like `/proc`, `/sys`, and `/dev` that provide interface access to system resources.

**Mandatory vs. Optional Mounting:**  

- Some filesystems must be mounted for the system to function properly. For example, root (`/`), `/proc`, `/sys`, and `/dev` are mounted at boot time by the system.
- External drives, additional partitions, and remote shares can be mounted manually by the user when needed or configured to auto-mount based on system settings.

**System vs. Manual Mounting on Distros like Ubuntu:**

- Ubuntu and similar distributions use *automatic mounting* for essential filesystems during boot. The `/etc/fstab` file contains entries that help the system decide which filesystems to mount at startup and with what options. Modern desktop environments also auto-mount removable media when they are connected.
- Users may *manually mount* devices that aren’t auto-mounted using the `mount` command. This is common for transient devices or non-standard partition layouts, and for troubleshooting or accessing specific partitions without permanent configuration changes.

### Understanding Mounting

Mounting is the process of making a file system accessible at a certain point in the Linux directory tree. When you mount a device, you're telling the operating system to attach the file system on that device to a specific directory, known as a mount point. This action integrates the device's file system with the existing directory structure, allowing you to read and write data to it as if it were just another directory on your system.

Imagine the Linux directory tree as a large, interconnected network of folders. By mounting a new device, you're effectively adding a new branch to this tree. This new branch can be accessed and navigated just like any other part of the tree.

```
Linux Directory Tree Before Mounting:

/
├── bin
├── etc
├── home
│   ├── user
├── usr
└── var

Linux Directory Tree After Mounting /dev/sdb1 at /mnt/external:

/
├── bin
├── etc
├── home
│   ├── user
├── mnt
│   └── external  <-- Mounted device /dev/sdb1
│       ├── documents
│       ├── photos
│       └── videos
├── usr
└── var
```

In this diagram, `/dev/sdb1` is a storage device (like a USB drive), and `/mnt/external` is the directory where it's mounted. After mounting, the contents of the device appear under `/mnt/external`.

### The Mount Command

To mount a file system, you use the `mount` command. This command attaches the file system found on a device to the directory tree at the specified mount point.

**Basic Syntax:**

```bash
mount [OPTIONS] <DEVICE> <MOUNT_POINT>
```

- `<DEVICE>` is the device file representing the storage device, such as `/dev/sdb1` for a specific partition.
- `<MOUNT_POINT>` is the directory where you want to access the contents of the device, like `/mnt/external`.

**Common Options (`[OPTIONS]`):** 

- `-t <filesystem_type>` lets you specify the filesystem type, like `ext4` for Linux filesystems or `ntfs` for Windows filesystems. If you don’t specify this, `mount` will try to detect the filesystem type automatically.
- `-o <options>` allows you to pass specific options. For example, `ro` mounts the device as read-only, while `rw` makes it read-write. You can also use `noexec` to prevent files on the device from being executed or `uid=<user_id>` to set the ownership. 

**Example:**

Suppose you have a USB drive at `/dev/sdb1` that you want to mount at `/mnt/external`. Here's how you can do it:

I. **Create a Mount Point:**

First, create the directory if it doesn't exist:

```bash
sudo mkdir -p /mnt/external
```

II. **Mount the Device:**

```bash
sudo mount /dev/sdb1 /mnt/external
```

This command mounts the device `/dev/sdb1` to the directory `/mnt/external`.

**Understanding the Output:**

After mounting, you can verify that the device is mounted by using the `mount` command without any arguments:

```bash
mount
```

This will display a list of all mounted file systems. Look for an entry like:

```
/dev/sdb1 on /mnt/external type ext4 (rw,relatime)
```

Breaking down the command:

- `/dev/sdb1` is the device that's mounted.
- `on /mnt/external` is the mount point.
- `type ext4` is the file system type.
- `(rw,relatime)` are mount options indicating it's read-write with relatime updates.

### Understanding Unmounting

Unmounting is the process of detaching a mounted file system from the directory tree. Before physically disconnecting a device, you should always unmount it to ensure that all data has been written to the device and to prevent data corruption.

Think of unmounting as safely removing a book from a library shelf. You ensure that no one is reading or writing notes in it before you take it away.

### The Umount Command

To unmount a file system, you use the `umount` command (note there's no 'n' in 'umount').

**Basic Syntax:**
Of course! Here’s a clear explanation for unmounting a device:

**Basic Syntax:**

```bash
umount [OPTIONS] <MOUNT_POINT or DEVICE>
```

- `<MOUNT_POINT>` or `<DEVICE>` specifies what you want to unmount. You can provide the directory where the device is mounted (e.g., `/mnt/external`) or the device itself (e.g., `/dev/sdb1`).

**Common Options (`[OPTIONS]`):**

- `-l` (Lazy unmount) allows the unmounting process to complete after the device is no longer in use. This is helpful if a process is currently accessing the device, as it will unmount once that process finishes.
- `-f` (Force unmount) forces the device to unmount, even if it’s currently in use. Use this with caution, as it can lead to data corruption if the device is actively writing or reading data.

**Example:**

To unmount the device we mounted earlier:

```bash
sudo umount /mnt/external
```

**Handling Common Issues:**

Sometimes, you might encounter an error like:

```
umount: /mnt/external: target is busy.
```

This means that a process is still using the file system. To find out which processes are causing this, you can use:

```bash
sudo lsof +f -- /mnt/external
```

This command lists open files on the file system. The output will look something like:

```
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
bash     1234 user  cwd    DIR   8,17     4096    2 /mnt/external
```

Below is a table explaining meaning of each field:

| **Field**   | **Description**                                                                                                     |
|-------------|---------------------------------------------------------------------------------------------------------------------|
| `COMMAND`   | The name of the command or process that opened the file.                                                            |
| `PID`       | The Process ID of the command or process.                                                                           |
| `USER`      | The user who owns the process that opened the file.                                                                 |
| `FD`        | The file descriptor (e.g., `cwd` for current directory, `rtd` for root, `txt` for code, `mem` for memory).          |
| `TYPE`      | The type of file, such as `REG` (regular file), `DIR` (directory), `CHR` (character device), `FIFO` (pipe), etc.    |
| `DEVICE`    | The device number (major and minor) for the file.                                                                   |
| `SIZE/OFF`  | The size of the file or the file offset.                                                                            |
| `NODE`      | The file's inode number.                                                                                            |
| `NAME`      | The name or path of the file being accessed.                                                                        |

To resolve the issue, you can close the application or navigate out of the directory in any terminal sessions. If necessary, you can terminate the process using:

```bash
sudo kill 1234
```

### Verifying Drive Visibility

Before mounting a device, it's important to verify that the operating system recognizes it. This ensures that the device is properly connected and ready for use.

**Using fdisk to List Devices:**

The `fdisk -l` command lists all the disk partitions on the system.

```bash
sudo fdisk -l
```

**Sample Output:**

```
Disk /dev/sda: 256 GB
...
Disk /dev/sdb: 32 GB
Device     Boot Start       End   Sectors  Size Id Type
/dev/sdb1        2048  62521343  62519296 29.8G 83 Linux
```

- The disk named `/dev/sdb` is configured with a **total capacity** of 32 GB, which can be used for various storage purposes.
- Within this disk, there exists a **partition** labeled `/dev/sdb1`, allowing for segmented storage allocation.
- This **partition** possesses a specific size, which may occupy the entire disk space or just a portion, depending on how it was set up.
- The **type** of the `/dev/sdb1` partition typically indicates its intended usage, such as **Linux** or **swap** partition, which defines how the system interacts with it. 

### Mounting File Systems with Specific Types

Sometimes, you may need to specify the file system type when mounting, especially if it's not a standard type or if the system doesn't auto-detect it.

**Example: Mounting a NTFS File System**

Suppose you have an external hard drive formatted with the NTFS file system (common with Windows). You can mount it using:

```bash
sudo mount -t ntfs /dev/sdb1 /mnt/external
```

Breaking down the command:

- `-t ntfs` specifies the file system type as NTFS.

### Using the /etc/fstab File for Persistent Mounts

The `/etc/fstab` file contains information about file systems and mount points. By adding an entry here, you can configure the system to automatically mount a device at boot.

**Example Entry:**

```
/dev/sdb1   /mnt/external   ext4    defaults    0   2
```

Below is a table explaining each field in the entry:

| **Field**            | **Description**                                                                                   |
|----------------------|---------------------------------------------------------------------------------------------------|
| **Device**           | `/dev/sdb1` – the device file or partition being mounted.                                         |
| **Mount Point**      | `/mnt/external` – the directory where the device is mounted.                                      |
| **File System Type** | `ext4` – the type of file system on the device.                                                   |
| **Options**          | `defaults` – standard mount options (e.g., read-write, async).                                    |
| **Dump**             | `0` – indicates if the partition should be backed up by the `dump` utility (`0` = no).            |
| **Pass**             | `2` – the fsck order during boot (`1` for root filesystem, `2` for other filesystems, `0` for no check). |

**Mounting All File Systems in fstab:**

After editing `/etc/fstab`, you can mount all file systems listed there using:

```bash
sudo mount -a
```

### Mounting ISO Images

An ISO image is a single file that contains the complete content and structure of a CD/DVD. You can mount an ISO file to access its contents without burning it to a physical disc.

**Mounting an ISO File:**

Suppose you have an ISO file named `ubuntu.iso` and you want to mount it at `/mnt/iso`.

I. Create a Mount Point:

```bash
sudo mkdir -p /mnt/iso
```

II. Mount the ISO:

```bash
sudo mount -o loop ubuntu.iso /mnt/iso
```

Breaking down the command:

- `-o` uses a loop device, allowing you to mount a file as a block device.

**Accessing the ISO Contents:**

Navigate to the mount point:

```bash
cd /mnt/iso
ls
```

You'll see the files and directories contained within the ISO image.

### Unmounting the ISO Image

When you're done, unmount the ISO to free up the loop device:

```bash
sudo umount /mnt/iso
```

### Visualizing the Mounting Process

Here's an ASCII diagram to help visualize how mounting integrates a device into the directory tree:

```
Before Mounting:

/
├── bin
├── etc
├── home
│   ├── user
├── mnt
├── usr
└── var

After Mounting /dev/sdb1 at /mnt/external:

/
├── bin
├── etc
├── home
│   ├── user
├── mnt
│   └── external
│       ├── data
│       └── projects
├── usr
└── var
```

### The Mounting Workflow

I. Verify Device Visibility:

Use `sudo fdisk -l` to list all devices and ensure your device is recognized.

II. Create a Mount Point:

If necessary, create a directory to serve as the mount point.

```bash
sudo mkdir /mnt/external
```

III. Mount the Device:

```bash
sudo mount /dev/sdb1 /mnt/external
```

IV. Access Files:

Navigate to `/mnt/external` to access the device's files.

V. Unmount When Done:

```bash
sudo umount /mnt/external
```

### Ensuring Data Integrity

- To avoid **data loss**, always unmount devices before physically removing them, as this allows the operating system to finalize any pending write operations.
- Since the operating system often **caches** write operations, data may not be written to the device immediately, so unmounting ensures all data has been properly saved.
- When you **unmount** a device, it confirms that all read and write processes have concluded, making it safe to remove the device without risking corruption.
- Failing to **unmount** a device before removing it can lead to incomplete data transfers and, consequently, corrupted files.

### Automating Mounting with udev Rules

- Advanced users can set up **udev rules** to automate the mounting process whenever a device is connected, enhancing ease of access.
- Creating **custom rules** in the `/etc/udev/rules.d/` directory enables automatic actions based on device characteristics, like USB device type or specific serial numbers.
- With **udev** rules, frequently used devices can be automatically mounted at a predefined location, reducing repetitive manual mounting steps.
- This automation can improve **workflow efficiency** and minimize errors, especially if you regularly work with multiple external devices.

#### Example: Auto-Mount USB Drive with udev

I. **Identify the Device**:

- First, connect the USB drive to your system and identify it using the `lsblk` or `dmesg` command.
- Find the device's **UUID** (Universally Unique Identifier) with the `blkid` command. This is necessary for ensuring that the rule applies to this specific device.

```bash
sudo blkid /dev/sdX1
```

II. **Create the udev Rule**:

- Open or create a new file in `/etc/udev/rules.d/`, for example, `99-usb-mount.rules`.
- Add the following rule, which will automatically mount the USB drive to a specified directory whenever it’s connected:

```bash
ACTION=="add", KERNEL=="sdX1", SUBSYSTEM=="block", ENV{ID_FS_UUID}=="your-uuid-here", RUN+="/bin/mkdir -p /media/my_usb && /bin/mount /dev/sdX1 /media/my_usb"
```

Replace **sdX1** with your specific device identifier, and **your-uuid-here** with the UUID of the device you found in the previous step.

In this rule:

- `ACTION=="add"` specifies that the rule should apply when the device is **added**.
- `KERNEL=="sdX1"` matches the specific device you want to auto-mount.
- `SUBSYSTEM=="block"` indicates that this rule applies to **block devices**, like hard drives or USB drives.
- `ENV{ID_FS_UUID}=="your-uuid-here"` ensures the rule matches the **exact device** based on its UUID.
- `RUN+="/bin/mkdir -p /media/my_usb && /bin/mount /dev/sdX1 /media/my_usb"` defines the action, which is to create the mount directory if it doesn’t exist and mount the device to that directory.

III. **Reload udev Rules**:

After saving the file, reload the **udev** rules with the following command:

```bash
sudo udevadm control --reload-rules
```
   
Then, to test the new rule, **disconnect** and **reconnect** your USB drive.

IV. **Remove Rules**:

If the drive is **removed**, you may want to create a separate rule to **unmount** it automatically:

```bash
ACTION=="remove", KERNEL=="sdX1", SUBSYSTEM=="block", ENV{ID_FS_UUID}=="your-uuid-here", RUN+="/bin/umount /media/my_usb"
```

By adding this **removal rule**, the device will be safely unmounted from the `/media/my_usb` directory whenever it is disconnected, helping to prevent **data corruption**.

### Troubleshooting Mounting Issues

- If you encounter a **"Permission Denied"** error, confirm that you have the necessary user permissions, or try using the `sudo` command for elevated access.
- When the system reports an **"Unknown File System Type"** error, you may need to install additional software packages, such as `ntfs-3g`, which provides support for NTFS file systems on Linux.
- A **"Device is Busy"** message indicates that files or processes are currently using the device; use commands like `lsof` or `fuser` to identify and close them before attempting to unmount.
- For devices that won’t unmount due to **active processes**, ending those processes can clear the device for proper unmounting, ensuring data integrity.

### Challenges

1. Plug a USB drive into your system and use `lsblk` and `fdisk -l` to identify the device name and partition details. Discuss how device names are assigned and explain the difference between physical devices and partitions.
2. Create a new directory under `/mnt` or `/media`, and mount your USB drive to this directory using the `mount` command. Describe the purpose of mount points and how they provide access to external storage devices on Linux.
3. Navigate to the mount point of the USB drive and perform basic file operations—create, read, edit, and delete a file. Discuss how mounting makes files accessible and how permissions might affect file access on mounted devices.
4. What happens if you mount a USB drive onto an existing non-empty directory? Is this allowed, and if so, what happens to the directory’s original contents?
5. Create a virtual disk file in your home directory using the `dd` command, specifying its size and location. Discuss how virtual disk files can simulate actual disks and their potential uses in testing and development.
6. Format the virtual disk file with an `ext4` filesystem using `mkfs.ext4`. Explain the significance of different filesystem types and why choosing an appropriate filesystem is important for specific use cases.
7. Mount the formatted virtual disk file to a directory under `/mnt`, just as you would a physical device. Discuss the concept of loopback devices and how they allow files to be mounted as if they were physical disks.
8. Investigate the differences between temporary and persistent mounting by adding an entry for your USB drive or virtual disk in `/etc/fstab`. Explain how persistent mounts work and the benefits of configuring automatic mounts for commonly used devices.
9. Explore permissions on the mounted USB drive by changing the ownership and permissions of files on it. Discuss how Linux handles permissions for different users on mounted devices and the implications for shared drives.
10. Create a script that automatically mounts and unmounts the USB drive upon insertion and removal, utilizing `udev` rules for automation. Explain how `udev` helps manage device events in Linux and the advantages of automated mounting for frequently used external devices.
