# System startup concepts

What happens between the time you push the power button and the time you see the login prompt?

## Bootup process

### First-stage boot loader

When a computer is turned on, the BIOS (Basic Input Output System) performs a power-on self-test (POST) to check the integrity of the system. The BIOS then searches for, loads, and executes the boot loader program. The boot loader is responsible for transitioning the computer from BIOS to the actual operating system.

To alter the boot sequence, you may need to press a specific key (such as F12 or F2) during BIOS startup.

There are two main types of first-stage boot loaders: BIOS and UEFI (Unified Extensible Firmware Interface). BIOS is the older boot loader program, while UEFI is the newer version. Most computers have either BIOS or UEFI, but not both.

### MBR

The Master Boot Record (MBR) is the first sector of a bootable disk (such as /dev/sda or /dev/hda). It is typically 512 bytes in size and contains:

* Primary boot loader information.
* Partition table information.
* An MBR validation check.
    
### Second-stage boot loader

One of the most common second-stage boot loaders is GRUB (Grand Unified Bootloader). GRUB allows the user to choose which kernel image should be executed and displays a splash screen. It also has knowledge of the file system and is able to load modules, such as those for USB or video card support, into the kernel. The newer version of GRUB is called GRUB2.

| GRUB | GRUB2 |
| ----------- | ----------- |
| Legacy | Newer version |
| menu.lst, grub.conf | /boot/grub/grub.cfg |
| difficult to modify | customize with /etc/default/grub |
| no live boot envrioments | can boot from ISO or USB |
| boot menu usually displays ons boot | hidden boot menu (on boot, hold down SHIFT) |

### Kernel

Once the boot loader has finished its job, the kernel is loaded and executed. The kernel is responsible for mounting the root file system and starting the init process, which is typically run as a daemon with PID 1. Init is responsible for choosing the run level and starting the programs associated with that run level.

The Linux kernel is efficient because it is modular.

* Mounts the root file system.
* Executes init: `/sbin/init`.
* Then it has access to all modules loaded into the kernel (such as usb or video card).
* Modules are not part of the static kernel, they are usually placed at `/lib/modules/`.

### Init

Init (short for initialization) is the first process that starts on a Linux system. It is usually run as a daemon with Process ID (PID) 1 and is responsible for:

* Choosing the runlevel.
* Reading the configuration file (/etc/inittab) to determine which programs should be loaded on startup.

### Runlevel

A run level is a system mode that determines the type of system being used (e.g. graphical, standalone network). The user can switch between run levels and set the default run level. The available run levels differ between distributions. Common ones include:

| Runlevel | Description |
| --- | --- |
| 0 | halt |
| 1 | single user mode |
| 2 | multiuser, without nfs (network) |
| 3 | full multiuser mode (with network) |
| 4 | unused |
| 5 | multiuser gui |
| 6 | reboot |

To display the current runlevel, use:

```bash
runlevel
```

To switch runlevel to number 3, use:

```bash
telinit 3
```

To set the default, you have to edit `/etc/inittab`. For example, if you want to make number 3 your default, you must find and replace the following line: 

    id:3:initdefault:

### Targets

In `SystemD`-based distributions, `targets` replace `runlevels`.. Targets represent different states that the system can be in, and each target has a set of associated programs that are started or stopped to achieve that state. 

| Target type | Runlevel |
| --- | --- |
| `poweroff.target` | runlevel 0 |
| `rescue.target` | runlevel 1 |
| `emergency.target` | runlevel 2 |
| `multi-user.target` | runlevel 3 |
| `graphical.target` | runlevel 5 |
| `reboot.target` | runlevel 6 |

If you're using one of those distributions, try the following command: 

```bash
ls -ll /usr/lib/systemd/system/runlevel*.target
```

You should get output similar to the following:

    /usr/lib/systemd/system/runlevel0.target -> poweroff.target
    /usr/lib/systemd/system/runlevel1.target -> rescue.target
    /usr/lib/systemd/system/runlevel2.target -> multi-user.target
    /usr/lib/systemd/system/runlevel3.target -> multi-user.target
    /usr/lib/systemd/system/runlevel4.target -> multi-user.target
    /usr/lib/systemd/system/runlevel5.target -> graphical.target
    /usr/lib/systemd/system/runlevel6.target -> reboot.target
    
`runlevel.target` files are soft-links to `SystemD` files. 

To display the current target, use:

```bash
systemctl list-units --type target | egrep "eme|res|gra|mul" | head -1
```

To switch the target to `multi-user.target`, use: 

```bash
systemctl isolate multi-user
```

To display the default target, use:

```bash
systemctl get-default
```

To set the default target to `multi-user.target`, use: 

```bash
systemctl set-default multi-user.target
```

Once the programs associated with the chosen run level or target have been started, the system is ready for use and the login prompt is displayed.

## Kernel panic
Kernel panic is a state of the operating system when it is unable to function properly, due to an unexpected and critical error in the kernel. This error can be caused by a variety of factors, such as a hardware malfunction, a software bug, or a security vulnerability.

* If you are not sure what caused the kernel panic, you can try booting the system in single user mode. This will allow you to access the system and run commands as the root user. You can then try to identify the cause of the kernel panic and fix it.
* If the kernel panic is caused by a hardware issue, you may need to replace the faulty component.
* If you are unable to boot the system at all due to a kernel panic, you may need to boot from a live CD or USB and try to fix the issue from there. You can also try booting into rescue mode or using a bootable system repair tool to diagnose and fix the issue.
* It is always a good idea to keep a backup of your system in case of a kernel panic or other issues. This can save you time and effort in the event that you need to restore your system. 


## Useful commands

The following commands can be useful when managing your system.

### Hostname

The hostname is a unique name that identifies your system on a network. You may change the system hostname on a SystemD-based operating system by manually changing `/etc/hostname` file or using:

```
hostnamectl set-hostname your_new_name
```

To view the current hostname of the system, use:

```
hostname
```

### Uptime

The `uptime` command displays the amount of time that the system has been running. It shows the current time, how long the system has been up, how many users are currently logged in, and the system load averages for the past 1, 5, and 15 minutes.

```
uptime
```

### Reboot

To reboot the system, you can use the `reboot` command or the `systemctl reboot` command.

```
# reboot command
reboot

# systemctl reboot command
systemctl reboot
```

To schedule a reboot at a specific time, use the `shutdown` command with the `-r` flag and specify the time in minutes. For example, to reboot in 5 minutes, use the following command:

```
shutdown -r +5
```

### Shutdown

To shut down the system, you can use the `shutdown` command or the `systemctl poweroff` command.

```
# shutdown command
shutdown now

# systemctl poweroff command
systemctl poweroff
```

To schedule a shutdown at a specific time, use the shutdown command with the `-h` flag and specify the time in minutes. For example, to shut down in 30 minutes, use the following command:

```
shutdown -h +30
```

## Recover the root password

1. Reboot the machine.
1. During the boot process, interrupt the Grub process by pressing any key.
1. Press `e` to edit the kernel that you want to initialize.
1. Locate the `linux16` line and add `rd.break` at the end of the line. Press `Ctrl-x` to continue booting.
1. The sysroot will be mounted as a read-only filesystem. Use the following command to remount it with read-write permissions: `mount -o remount,rw /sysroot`
1. Change into the sysroot filesystem with the `chroot /sysroot` command.
1. Use the `passwd` command to change the root password.
1. Run the command `touch /.autorelabel` to reset the SELinux context labels on the filesystem.
1. Exit the chroot environment with the `exit` command.

## Challenges

1. Run the `reboot` command to restart your server. You can use the `uptime` command to verify that the machine has been restarted.
1. Use the `hostnamectl set-hostname` command to rename your server. You can then use the `hostname` command to confirm that the operation was successful.
1. Recover the root password.
