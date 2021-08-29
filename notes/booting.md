What Linux does between the moment you press the power button and the time the login prompt appears?

<h2>BIOS</h2>

* Basic input output system.
* Checks the integrity of the system.
* The boot loader program is searched for, loaded, and executed.
* To alter the boot sequence, hit a specific key (F12 or F2) during BIOS startup.

<h2>MBR</h2>

* Master boot record.
* First sector of bootable disk (/dev/sda or /dev/hda).
* < 512 bytes.
* Primary boot loader info.
* Partition table info.
* Mbr validation check. 

<h2>GRUB</h2>

* Grand unified bootloader.
* Chooses which kernel image should be executed.
* Displays the splash screen.
* Has knowledge of the file system.
* Configuration file: /boot/grub/grub.cfg

<h2>Kernel</h2>

* Mounts the root file system.
* Executes init: /sbin/init

<h2>Init</h2>

* Chooses run level
* Configuration file: /etc/inittab
* What programs will be loaded on startup.

<h2>Run level</h2>

* executes program for the current run level

| Run level | Description |
| --- | --- |
| 0 | halt |
| 1 | single user mode |
| 2 | multiuser, without nfs |
| 3 | full multiuser mode |
| 4 | unused |
| 5 | X11 |
| 6 | reboot |

<h2>Hostname</h2>
You may change the system hostname on a systemd-based operating system by manually changing /etc/hostname.

<h2>Uptime</h2>
uptime

<h2>Reboot</h2>
Reboot system with systemctl:

```bash
systemctl reboot
```

To restart in 5 minutes, use the <i>shutdown</i> command:

```bash
shutdown -r +5
```

<h2>Shutdown</h2>

To power off inmmediately, use the <i>shutdown</i> command:

```bash
shutdown now
```

To power off with systemctl, use:

```bash
systemctl poweroff
```

<h2>Recover root password</h2>

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
