# Boot concepts

What happens in Linux between the time you push the power button and the time you see the login prompt? 

## Boot process

### BIOS

* Basic input output system.
* Checks the integrity of the system.
* The boot loader program is searched for, loaded, and executed.
* To alter the boot sequence, hit a specific key (F12 or F2) during BIOS startup.

### BIOS vs UEFI

* What is the difference? Which one should we support?
* Both serve as the middle man between hardware and the OS.
* UEFI is newer program.
* Usually you have either BIOS or UEFI (Unified Extensible Firmware Interface).

### MBR

* Master boot record.
* First sector of bootable disk (/dev/sda or /dev/hda).
* < 512 bytes.
* Primary boot loader info.
* Partition table info.
* Mbr validation check. 

### GRUB

This is hwo the computer transitions from BIOS to the actual OS.

* Grand unified bootloader.
* Chooses which kernel image should be executed.
* Displays the splash screen.
* Has knowledge of the file system.
* Newer version is GRUB2.

| GRUB | GRUB2 |
| ----------- | ----------- |
| Legacy | Newer version |
| menu.lst, grub.conf | /boot/grub/grub.cfg |
| difficult to modify | customize with /etc/default/grub |
| no live boot envrioments | can boot from ISO or USB |
| boot menu usually displays ons boot | hidden boot menu (on boot, hold down SHIFT) |

### Kernel

The Linux kernel is efficient because it is modular.

* Kernel is started from GRUB.
* The files responsible for this part are called <code>vmlinux</code> or <code>vmlinuz</code>. Those are static files found on <code>/boot/</code>.
* Mounts the root file system.
* Executes init: /sbin/init.
* Then it has access to all modules loaded into the kernel (such as usb or video card).
* Modules are not part of the static kernel, they are usually placed at <code>/lib/modules/</code>.

### Init

On Linux, init (short for initialization) is the program that starts all other processes. It is typically run as a daemon with PID 1. 

* Chooses the run level.
* Configuration file: /etc/inittab.
* What programs will be loaded on startup.

### Run level

Executes program for the current run level.

| Run level | Description |
| --- | --- |
| 0 | halt |
| 1 | single user mode |
| 2 | multiuser, without nfs |
| 3 | full multiuser mode |
| 4 | unused |
| 5 | X11 |
| 6 | reboot |

## Kernel panic

* If nothing was changed on the system, one of the hardware components might be defective.
* If you recently updated the kernel, you can restore to a previous version. On the upgrade, Linux automatically backs up the old kernel. 

## Useful Commands

### Hostname

You may change the system hostname on a systemd-based operating system by manually changing /etc/hostname file or using:

```bash
hostnamectl set-hostname your_new_name
```

### Uptime

```bash
uptime
```

### Reboot

Reboot system with systemctl:

```bash
systemctl reboot
```

To restart in 5 minutes, use the <i>shutdown</i> command:

```bash
shutdown -r +5
```

### Shutdown

To power off inmmediately, use the <i>shutdown</i> command:

```bash
shutdown now
```

To power off with systemctl, use:

```bash
systemctl poweroff
```

## Recover the root password

1. reboot the machine
1. interrupt grub process typing any key
1. press 'e' to edit the kernel that you want to init
1. locate 'linux16' line and add at the end of the line 'rd.break' and press Ctrl-x
1. the sysroot is mounted as read only filesystem, remount with rw filesystem
1. mount -o remount,rw /sysroot
1. chroot /sysroot
1. use passwd command to change the password
1. touch /.autorelabel
1. exit

## Challenges

1. Run the <i>reboot</i> command. Use the <i>uptime</i> command to ensure that your server was restarted.
1. Use <i>hostnamectl set-hostname</i> to rename your server. Run, <i>hostname</i>, to confirm that the operation was successful.
1. While the machine is booting up, interupt the process and change the root password.
1. Recover the root password.
