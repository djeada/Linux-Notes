# System Startup Process

What happens between the time you push the power button and the time you see the login prompt?

## 1. Bootup Process

The bootup process is a sequence of events that occurs when you power on a computer. It involves several stages including POST, boot loader execution, loading and initializing the operating system.

### 1.1 Power-On Self-Test (POST)

When a computer is powered on, the BIOS or UEFI (Unified Extensible Firmware Interface) performs a Power-On Self-Test (POST). This test checks the integrity of the hardware components and ensures that everything is functioning correctly. In case of any errors, POST halts the boot process and sends out an error message.

### 1.2 Boot Loader Execution

After successfully passing POST, BIOS/UEFI locates the bootable device. It then searches for, loads, and executes the first-stage boot loader. This boot loader is responsible for transitioning the computer from firmware services to the actual operating system. To modify the boot sequence, you may need to press a specific key (like F12 or F2) during this stage.

**Types of First-Stage Boot Loaders**

There are two primary types of first-stage boot loaders: 

- **BIOS**: Basic Input Output System, an older version of the firmware.
- **UEFI**: Unified Extensible Firmware Interface, a more recent version with improved functionality and security.

Most computers either have BIOS or UEFI, not both.

## 2. Master Boot Record (MBR)

The Master Boot Record is the first sector of a bootable disk (e.g., /dev/sda or /dev/hda). It's typically 512 bytes in size and comprises:

- **Boot Loader Information**: Code to load the second-stage boot loader.
- **Partition Table Information**: Defines the organization of the disk into partitions.
- **MBR Validation Check**: A magic number for error checking.

## 3. Second-Stage Boot Loader

This stage takes over after the first stage. One of the most common second-stage boot loaders is GRUB (Grand Unified Bootloader). GRUB allows users to choose which kernel image should be executed and displays a splash screen.

In addition, GRUB understands file system layouts and can load modules, such as those for USB or graphics card support, into the kernel. The newer version of GRUB is GRUB2.

|     | GRUB | GRUB2 |
| --- | ---- | ----- |
| **Version** | Legacy | Newer Version |
| **Configuration Files** | menu.lst, grub.conf | /boot/grub/grub.cfg |
| **Ease of Modification** | More Difficult | Customize with /etc/default/grub |
| **Live Boot Environments** | No Support | Can Boot from ISO or USB |
| **Boot Menu Display** | Usually Displays on Boot | Hidden Boot Menu (Hold down SHIFT during boot) |

### 4. Kernel Initialization

After the bootloader has completed its tasks, the kernel is loaded and executed. The kernel plays a central role in managing the computer's resources, and is essentially the heart of the operating system. In a Linux system, the kernel is highly modular and efficient, adding to its flexibility and performance.

**Kernel Tasks**

- **Mounts the Root File System**: The kernel mounts the root filesystem to gain access to the entire filesystem hierarchy.
- **Executes Init Process**: The kernel then executes the init process (`/sbin/init`), which is typically run as a daemon with Process ID (PID) 1.
- **Loads Modules**: The kernel has access to all modules loaded into it, such as those for USB support or graphics cards. These modules are not part of the static kernel and are usually placed at `/lib/modules/`.

### 5. Init Process

The init process, short for 'initialization', is the first process that starts on a Linux system. Init runs as a daemon with PID 1, marking the commencement of the user-space system.

**Responsibilities of the Init Process**

- **Determines the Runlevel**: The init process selects the runlevel, which defines the state in which the system will operate.
- **Loads Startup Programs**: The init process reads the configuration file (`/etc/inittab`) to determine which programs should be loaded at startup.

### 6. Runlevel

The runlevel is a system mode that defines the services and processes that the system should run. Each runlevel corresponds to a different state of the machine, from halted state to single-user mode, to full multi-user with GUI and networking. 

| Runlevel | Description |
| --- | --- |
| 0 | Halt, shutting down the system |
| 1 | Single-user mode, usually for system maintenance |
| 2 | Multiuser, without NFS (network file system) |
| 3 | Full multiuser mode, with networking |
| 4 | Unused |
| 5 | Multiuser mode with GUI |
| 6 | Reboot, restarting the system |

**Interacting with Runlevels**

You can display the current runlevel using the `runlevel` command:

```bash
runlevel
```

To switch to a different runlevel, for example runlevel 3, use the telinit command:

```bash
telinit 3
```
To set a default runlevel, you need to edit the /etc/inittab file. For example, to set runlevel 3 as the default, find and replace the following line:

```bash
id:3:initdefault:
```

Remember to be cautious when editing this file, as incorrect settings can prevent your system from booting correctly.

### 7. Targets (SystemD)

In Linux distributions that utilize `SystemD`, the concept of `runlevels` has been replaced by `targets`. Targets represent different states that the system can be in, and each target is associated with a specific set of services and units that are started or stopped to reach that state. This allows for more flexibility and control over the system's operational mode.

| Target | Equivalent Runlevel | Description |
| --- | --- | --- |
| `poweroff.target` | Runlevel 0 | Halt, shutting down the system |
| `rescue.target` | Runlevel 1 | Single-user mode, usually for system maintenance |
| `emergency.target` | Special | Similar to rescue.target, but mounts the minimum number of file systems read-only |
| `multi-user.target` | Runlevel 3 | Multiuser mode, without GUI |
| `graphical.target` | Runlevel 5 | Multiuser mode with GUI |
| `reboot.target` | Runlevel 6 | Reboot, restarting the system |

If you are using a `SystemD`-based distribution, the following command will list the symbolic links between the old runlevel targets and the new SystemD targets:

```bash
ls -l /usr/lib/systemd/system/runlevel*.target
```

This will produce output similar to the following, showing how each runlevel is mapped to a corresponding SystemD target:

```bash
/usr/lib/systemd/system/runlevel0.target -> poweroff.target
/usr/lib/systemd/system/runlevel1.target -> rescue.target
/usr/lib/systemd/system/runlevel2.target -> multi-user.target
/usr/lib/systemd/system/runlevel3.target -> multi-user.target
/usr/lib/systemd/system/runlevel4.target -> multi-user.target
/usr/lib/systemd/system/runlevel5.target -> graphical.target
/usr/lib/systemd/system/runlevel6.target -> reboot.target
```

### Interacting with SystemD Targets

You can display the current active target with the following command:

```bash
systemctl list-units --type target --state active
```

To change to a different target, use the systemctl isolate command. For example, to switch to multi-user.target, use:

```bash
systemctl isolate multi-user.target
```

You can display the default target (the target that the system boots into by default) with this command:

```bash
systemctl get-default
```

And you can set a new default target with the systemctl set-default command. For instance, to make multi-user.target the default, use:

```bash
systemctl set-default multi-user.target
```

Once the services and units associated with the chosen target have been started, the system is ready for use. At this point, the login prompt is displayed, marking the end of the boot process.

## Understanding Kernel Panic

A Kernel panic is a fatal error condition detected by the Linux kernel, triggering a state where the operating system cannot continue to function safely. It is equivalent to a system crash, and its causes are varied, ranging from hardware malfunctions and software bugs to potential security vulnerabilities. When a Kernel panic occurs, the system typically prints an error message, dumps the kernel memory for post-mortem debugging, and then either waits for a reboot or attempts an automatic reboot depending on the kernel settings.

**Potential Causes of Kernel Panic**

- **Hardware Errors**: Faulty or incompatible hardware, such as RAM or hard drive, can often lead to a kernel panic. A common cause is bad memory modules.
- **Software Errors**: Kernel panic can also be triggered by software errors, such as bugs in the kernel itself, or problematic device drivers.
- **File System Corruption**: Corrupted file systems can cause the kernel to panic, particularly if the damage affects critical system files.

**Handling Kernel Panic**

- **Single User Mode**: If the root cause of the kernel panic isn't immediately clear, booting the system in single-user mode can be helpful. This mode allows you to access the system with root privileges, enabling you to run diagnostic commands and check system logs that might hint at the source of the problem.
- **Hardware Diagnostics**: If the kernel panic is potentially caused by a hardware issue, diagnostic software can be used to test various hardware components. If a faulty component is identified, replacement or repair may be necessary.
- **Live CD/USB**: If the system cannot boot normally due to kernel panic, booting from a live CD or USB stick is a good option. This provides a way to access the file system and potentially fix the issue or at least recover valuable data.
- **Rescue Mode/Bootable System Repair Tools**: Some distributions offer rescue modes or bootable system repair tools to diagnose and fix issues causing kernel panics. These tools can be invaluable for identifying and rectifying system problems.
- **Backup**: Regularly backing up your system is always a good practice. In case of severe issues like kernel panic, a reliable backup can save significant time and effort, providing a fallback point to restore the system.

## Essential System Management Commands

In Linux, several command-line utilities allow you to manage your system effectively. Here are some of the most commonly used commands.

### Managing the Hostname

A hostname is a unique name that identifies a system within a network. It's essential for communication in a network environment as it differentiates one machine from another.

Viewing the hostname: Use the `hostname` command to print the current hostname of the system:

```bash
hostname
```

Setting the hostname: In SystemD-based systems, you can change the hostname using the hostnamectl command. Alternatively, you can manually modify the /etc/hostname file.

``` bash
hostnamectl set-hostname your_new_name
```

### Checking System Uptime

The uptime command is used to check how long the system has been running without rebooting. It also displays the current time, number of logged-in users, and system load averages over the last 1, 5, and 15 minutes.

```bash
uptime
```

### Rebooting the System

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

### Shutting Down the System

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

## Recovering the Root Password

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

## Challenges

1. **Reboot your system:**
    - Use the `reboot` command to restart your system. 
    - Check the output of the `uptime` command to verify that the system has been restarted. 
    - You should see the system uptime is very short, indicating a recent restart.

2. **Change your system's hostname:**
    - First, check the current hostname using the `hostname` command.
    - Use the `hostnamectl set-hostname your_new_name` command to rename your server, replacing `your_new_name` with the new name you want to assign.
    - Run the `hostname` command again to confirm that the operation was successful. The name displayed should match the new name you assigned.

3. **Recover the root password:**
    - Without logging out of your current session, simulate a situation where you've lost the root password by opening a new terminal session or SSH connection where you aren't logged in as root.
    - Follow the steps provided in the "Recovering the Root Password" section above to reset the root password.
    - After rebooting, ensure that you can successfully log in with the new root password.

4. **Practice handling kernel panic:**
    - Although simulating a kernel panic scenario isn't recommended on a production machine, understanding the steps needed to resolve a kernel panic is valuable.
    - Review the "Kernel panic" section and take note of the steps you would take to diagnose and resolve a kernel panic.

5. **Manage system runlevels/targets:**
    - Check your current runlevel or target.
    - If you are using an init-based system, try changing the runlevel and verify the change.
    - If you are using a systemd-based system, try switching between targets and confirm that the change took effect.
    - Remember to switch back to your default runlevel or target after you've completed the challenge.

6. **Schedule system tasks:**
    - Try to schedule a system shutdown using the `shutdown` command, then cancel it before it takes effect.
    - Do the same with a system reboot.
    - Remember: make sure to cancel these tasks if you are doing this on a production machine, to avoid unwanted system downtime.
