## System Startup Process

What happens between the time you push the power button and the time you see the login prompt?

```
[1] Power On
       │
       ▼
+--------------------------------+
| [2] BIOS / UEFI                |
|  • Load firmware from NVRAM    |
|  • Run POST (Power-On Self Test) |
+--------------------------------+
       │
       ▼
+--------------------------------+
| [3] Device Detection           |
|  • Enumerate CPU, RAM, disks   |
|  • Initialize bus controllers  |
+--------------------------------+
       │
       ▼
+--------------------------------+
| [4] Boot-Device Selection      |
|  • UEFI Boot Manager or MBR    |
|  • Choose EFI partition or MBR |
+--------------------------------+
       │
       ▼
+--------------------------------+
| [5] Bootloader (GRUB2 / LILO)  |
|  • Read /boot/grub2/grub.cfg   |
|  • Display menu (timeout/user) |
|  • Load:                       |
|     – vmlinuz-<version> (kernel) |
|     – initramfs-<version>.img  |
|     – Kernel cmdline args      |
+--------------------------------+
       │
       ▼
+-------------------------------------------------+
| [6] Linux Kernel + Initramfs                   |
|  • Decompress & relocate kernel image           |
|  • Mount initramfs (dracut/busybox)             |
|  • Load early userspace tools & modules (.ko)  |
|  • Probe hardware & mount real root FS         |
|  • pivot_root/switch_root → exec /sbin/init    |
+-------------------------------------------------+
       │
       ▼
+-------------------------------------------------+
| [7] systemd (PID 1)                             |
|  • Execute /usr/lib/systemd/systemd             |
|  • Read default.target → resolves into         |
|      multi-user.target →                       |
|        ├─ sysinit.target  (fsck, sysctl, kmod)  |
|        ├─ basic.target    (journald, udev)      |
|        └─ multi-user.target                     |
|            ├─ getty@.service (login prompts)    |
|            ├─ sshd.service                      |
|            └─ network-online.target             |
|    [opt] graphical.target → display-manager     |
+-------------------------------------------------+
       │
       ▼
+-------------------------------------------------+
| [8] User‐Space Initialization                   |
|  • systemd-login (logind)                       |
|  • Shell startup: /etc/profile, ~/.bashrc       |
|  • GUI login manager (gdm/kdm/xdm)              |
|  → Finally: users can log in & start sessions   |
+-------------------------------------------------+
```

### Bootup Process

The bootup process is the ordered set of steps a computer follows after power-on, moving from firmware control to a fully running operating system. At a high level it consists of:

1. **Power-On Self-Test (POST)**
2. **Boot-loader discovery and first-stage execution**
3. **Second-stage boot loader / firmware boot manager**
4. **Kernel (and initramfs) loading**
5. **PID 1 initialization (SysV init or systemd)**
6. **Multi-user state (runlevels / targets)**

#### Power-On Self-Test (POST)

When power is applied the system firmware—either classic **BIOS** or modern **UEFI (Unified Extensible Firmware Interface)**—executes POST. POST verifies CPU registers, firmware integrity, system RAM, basic chipset functions, and often attached devices such as GPUs. Many firmwares emit diagnostic beep codes or on-screen messages if errors are found; fatal errors halt the boot process so that subsequent stages are never reached.

#### Boot Loader Execution

After a successful POST the firmware locates a bootable **device** according to its configured boot order.

**On BIOS systems**

* The firmware reads the **first 512-byte sector** (Master Boot Record) of the selected disk into memory location 0x7C00 and jumps to it.
* This sector contains a *very small* first-stage loader (≤ 446 bytes) whose only job is to locate and load a more capable second-stage loader.

**On UEFI systems**

* There is *no* 512-byte MBR loader requirement. Instead, the firmware reads the FAT32-formatted **EFI System Partition (ESP)**, loads the configured `*.efi` executable (e.g. `\EFI\Microsoft\Boot\bootmgfw.efi`, `\EFI\debian\grubx64.efi`, or a **shim** in Secure Boot scenarios) and transfers control to it.
* Boot order entries are stored in NVRAM and edited with tools such as `efibootmgr`.

To modify the boot sequence you usually press **Esc, F2, F10, F12 or Del** during POST; the key varies by vendor.

**Types of Firmware and First-Stage Code**

| Firmware Model                 | First-Stage Location               | Notes                                                                                     |
| ------------------------------ | ---------------------------------- | ----------------------------------------------------------------------------------------- |
| **BIOS**                       | First 446 bytes of the disk’s MBR  | Limited space; must chain-load a second-stage loader (GRUB Legacy, LILO, Syslinux, etc.). |
| **UEFI (without Secure Boot)** | EFI executable on ESP              | Can load GRUB 2, systemd-boot, rEFInd, or the kernel directly.                            |
| **UEFI (with Secure Boot)**    | Microsoft-signed **shim** → GRUB 2 | shim validates GRUB’s signature before handing off.                                       |

Most modern x86 machines ship with UEFI; legacy BIOS mode is often still available for compatibility.

### Master Boot Record (MBR)

The **MBR** is the first sector (LBA 0) of a traditional BIOS disk. By convention it is **512 bytes** and contains:

* **446 bytes** – first-stage boot loader machine code
* **64 bytes** – primary partition table (four 16-byte entries)
* **2 bytes** – signature `0x55 AA` used by firmware to validate the read

> **GPT note** – On GUID Partition Table disks a *protective* MBR is still present for legacy tools, but real partition metadata lives in GPT headers and tables beyond LBA 0.

```
                    Computer Starts
                         |
                         v
              +---------------------+
              |     BIOS / UEFI     |
              +---------------------+
                         |
                (if BIOS) Reads MBR
                         v
              +---------------------+
              |   Master Boot       |
              |       Record        |
              +---------------------+
                         |
      +------------------+------------------+
      |  First-Stage     |  Partition Table |
      |   Loader (446B)  |   (4 entries)    |
      +------------------+------------------+
                         |
                0x55AA Signature Check
                         v
              +---------------------+
              |  Second-Stage Boot  |
              |      Loader         |
              +---------------------+
```

### Second-Stage Boot Loader

The full-featured second stage (or, on UEFI, the firmware boot manager itself) understands filesystems and can present a menu.

**GRUB Legacy vs GRUB 2**

|                    | **GRUB Legacy**                             | **GRUB 2**                                         |
| ------------------ | ------------------------------------------- | -------------------------------------------------- |
| Main files         | `stage1`, `stage2`, `menu.lst`, `grub.conf` | `/boot/grub/grub.cfg` *(generated)*                |
| Editing config     | Manual edit                                 | Edit `/etc/default/grub` + `grub-mkconfig`         |
| Filesystem support | ext2/3, iso9660 (limited)                   | ext2-4, btrfs, xfs, ZFS, LVM, LUKS…                |
| ISO/USB live boot  | No (patches existed)                        | Native `loopback` / `search --file`                |
| Menu visibility    | Always shown                                | Hidden unless **Esc/Shift** pressed (configurable) |

Other popular loaders include **systemd-boot** (formerly `gummiboot`), **rEFInd**, and **LILO/Syslinux** on legacy systems.

### Kernel Initialization

Once the loader selects a kernel it usually loads:

1. **Kernel image** (`vmlinuz-*`)
2. **initramfs / initrd** – a compressed cpio archive that holds early-boot userspace and drivers needed to find the real root filesystem.

After decompression the kernel:

* Enables paging, sets up memory management and CPU scheduling.
* Initializes built-in and **modules** (`/lib/modules/$(uname -r)/`) drivers.
* Mounts the root filesystem specified by the loader or by `root=` kernel parameter.
* Executes **PID 1**:
* **`/sbin/init`** on SysV-init systems
* **`/usr/lib/systemd/systemd`** on the vast majority of modern distributions
* Alternatives such as **OpenRC**, **runit**, **s6-rc**, etc.

### Init Process

`init` (or `systemd`) is the *root of the user-space process tree*.

* **SysV-init** consults `/etc/inittab` and launches scripts in `/etc/rc.d/rc*.d/`.
* **systemd** reads declarative **unit files** in `/usr/lib/systemd/` and `/etc/systemd/`.

### Runlevels

(Only relevant to SysV-init or distributions that still provide compatibility.)

| Runlevel | Traditional Meaning (Red Hat / Debian)\*           |
| -------- | -------------------------------------------------- |
| 0        | Halt / power-off                                   |
| 1        | Single-user (rescue)                               |
| 2        | Multi-user (Debian: full network; Red Hat: unused) |
| 3        | Multi-user, networking, no GUI                     |
| 4        | Undefined / custom                                 |
| 5        | Multi-user + graphical login                       |
| 6        | Reboot                                             |

Runlevel semantics vary slightly across families. Use `runlevel` to query, `telinit <N>` to switch, and edit `/etc/inittab` to change the default (if SysV-init is in use).

```bash
# Show current and previous runlevel
runlevel
# Switch to runlevel 3
sudo telinit 3
```

### Targets (systemd)

`systemd` replaces runlevels with **targets**, which can aggregate any number of services (units).

| Target              | Approx. Runlevel | Purpose                                           |
| ------------------- | ---------------- | ------------------------------------------------- |
| `poweroff.target`   | 0                | Power-off                                         |
| `rescue.target`     | 1                | Single-user (basic services)                      |
| `emergency.target`  | —                | Root shell, minimal mounts (stricter than rescue) |
| `multi-user.target` | 2/3              | Text-mode multi-user                              |
| `graphical.target`  | 5                | GUI login manager + multi-user                    |
| `reboot.target`     | 6                | Reboot                                            |

```bash
# Show active targets
systemctl list-units --type=target --state=active
# Switch to graphical target
sudo systemctl isolate graphical.target
# Query / set default target
systemctl get-default
sudo systemctl set-default multi-user.target
```

Symbolic links keep backward compatibility:

```bash
ls -l /usr/lib/systemd/system/runlevel*.target
```

### Kernel Panic

A **kernel panic** is an unrecoverable fault detected by the kernel (NULL pointer dereference, unhandled IRQ, corrupted stack, etc.). When it occurs the kernel prints a *panic stack trace*, optionally dumps memory to disk (kdump / crashkernel), and halts or reboots according to `kernel.panic` sysctl.

**Common causes**

* **Hardware:** defective RAM, overheating CPU, failing storage controller.
* **Software:** buggy kernel module, out-of-tree driver, mis-compiled custom kernel.
* **Filesystem:** unrecoverable journal corruption, I/O errors on root FS.

**Recovery steps**

1. **Single-user / rescue mode** – add `single` or `systemd.unit=rescue.target` to the kernel command line.
2. **Examine logs** – review last lines of `dmesg`, `/var/log/kern.log`, or crash dumps.
3. **Hardware tests** – run `memtest86+`, manufacturer disk diagnostics, or swap suspected components.
4. **Live USB** – chroot into the installation to reinstall kernels or roll back updates.
5. **Backups** – maintain verified backups so that a full reinstall remains a quick option if necessary.

### System Management Commands

In Linux, several command-line utilities allow you to manage your system effectively. Here are some of the most commonly used commands.

#### Managing the Hostname

A hostname is a unique name that identifies a system within a network. It's essential for communication in a network environment as it differentiates one machine from another.

Viewing the hostname: Use the `hostname` command to print the current hostname of the system:

```bash
hostname
```

Setting the hostname: In SystemD-based systems, you can change the hostname using the hostnamectl command. Alternatively, you can manually modify the /etc/hostname file.

``` bash
hostnamectl set-hostname your_new_name
```

#### Checking System Uptime

The uptime command is used to check how long the system has been running without rebooting. It also displays the current time, number of logged-in users, and system load averages over the last 1, 5, and 15 minutes.

```bash
uptime
```

#### Rebooting the System

Immediate reboot: Use the reboot command or systemctl reboot to restart the system immediately.

```bash
# Using reboot
reboot

# Using systemctl
systemctl reboot
```

Scheduled reboot: To reboot at a specific time, use the shutdown command with the -r option followed by the time in minutes. For instance, to reboot in 5 minutes:

```bash
shutdown -r +5
```

#### Shutting Down the System

Immediate shutdown: The system can be shut down immediately using the shutdown now command or systemctl poweroff.

```bash
# Using shutdown
shutdown now

# Using systemctl
systemctl poweroff
```

Scheduled shutdown: A shutdown can be scheduled at a specific time using the shutdown command with the -h option followed by the time in minutes. For example, to shut down the system in 30 minutes:

```bash
shutdown -h +30
```

Understanding and correctly using these commands can be incredibly beneficial when managing Linux-based systems. It allows users to maintain control over their systems, schedule tasks, and keep track of their system's status.

### Recovering the Root Password

If you forget the root password on your Linux system, you can recover it by following these steps. We will interrupt the boot process to gain access to a shell, then change the root password.

1. **Reboot the machine.** Start by restarting your computer. You can do this with the `reboot` command or by manually turning it off and on again.

2. **Interrupt the boot process.** During the boot process, you'll see the Grub bootloader screen. This is where you select which kernel you want to boot. Interrupt this by pressing any key before the timer runs out.

3. **Edit the boot options.** Highlight the kernel you want to boot and press `e` to edit the boot options.

4. **Modify the kernel parameters.** In the kernel parameters line (usually starting with `linux16` or `linux`), navigate to the end and add `rd.break` which interrupts the boot process before control is passed from the initramfs to the actual kernel. Press `Ctrl-x` or `F10` to continue booting.

5. **Gain write access to the system root.** After booting, you'll be in an emergency shell. The system root is mounted as read-only. Remount it as read-write with the following command: 

```bash
mount -o remount,rw /sysroot
```

6. **Change to the system root directory**. Use the chroot command to change the apparent root directory to /sysroot:

```bash
chroot /sysroot
```

7. **Change the root password**. You are now in a position to change the root password. Use the passwd command and follow the prompts to enter a new root password.

8. **Update SELinux parameters**. If your system uses SELinux, you need to update the SELinux parameters. Run the following command to ensure the context labels are reset on the filesystem:

```bash
touch /.autorelabel
```

9. **Exit and reboot**. Finally, type exit twice. The first exit will leave the chroot environment, and the second will continue the boot process. Your system will then reboot and you should be able to log in with the new root password.

### Challenges

1. Use the `reboot` command to restart your system, then use the `uptime` command to confirm the restart by observing the system uptime. Discuss how the `uptime` command can help you monitor system stability and determine when the system was last rebooted.
2. Check the current hostname of your system with the `hostname` command, then change it using `hostnamectl set-hostname new_hostname`. Verify the change by running `hostname` again. Discuss the significance of hostname settings, particularly for networked environments where unique identification is necessary.
3. Simulate a scenario where you've lost the root password by opening a new terminal or SSH session where you are not logged in as root. Follow the appropriate steps to reset the root password and reboot the system. Verify that you can log in with the new password. Explain the importance of password recovery skills for system administrators.
4. Research kernel panic scenarios and describe the steps you would take to diagnose and resolve a kernel panic. Although not recommended to simulate a kernel panic on a production system, document the commands and troubleshooting techniques used for resolving kernel panics, such as reviewing logs or booting into recovery mode.
5. Check your current system runlevel or target using `runlevel` on init-based systems or `systemctl get-default` on systemd-based systems. Change the runlevel (for init) or switch targets (for systemd), and confirm that the change was successful. Explain the differences between runlevels and targets and their roles in controlling system state.
6. Schedule a system shutdown with the `shutdown` command (e.g., `shutdown +10` to schedule a shutdown in 10 minutes), then cancel it before it takes effect using `shutdown -c`. Practice scheduling a reboot in a similar way, and explain how to manage scheduled tasks effectively to prevent unintended system downtime.
7. Use the `systemctl list-timers` command to view all active timers on your system. Identify which services are associated with each timer and discuss the role of timers in automating system maintenance tasks, such as updates or backups, on a scheduled basis.
8. Modify the timezone of your system using `timedatectl set-timezone` followed by the appropriate timezone (e.g., `America/New_York`). Verify the change with `timedatectl` and discuss how setting the correct timezone is essential for accurate logging and scheduling, especially on servers used by teams in different geographic locations.
9. Set up a recurring system maintenance task using `cron`. For example, configure a cron job that runs a simple script every day at midnight, such as creating a backup of a directory. Verify that the cron job is functioning by checking the output or logs. Discuss the importance of cron in automating routine maintenance tasks.
10. Use `journalctl` to view system logs from the most recent boot, filtering the logs to show only critical or error messages. Explain how analyzing boot logs can help you troubleshoot startup issues and identify potential system problems early.
