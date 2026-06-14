## System Startup Process

The system startup process is everything that happens between pressing the power button and reaching a usable login prompt or graphical desktop.

At a high level, startup moves through several layers:

```text id="p4f7p1"
Power on
   |
   v
Firmware: BIOS or UEFI
   |
   v
Boot device selection
   |
   v
Bootloader
   |
   v
Linux kernel
   |
   v
initramfs
   |
   v
real root filesystem
   |
   v
PID 1: systemd or init
   |
   v
services, login prompts, network, GUI
```

A more detailed boot flow looks like this:

```text id="x94trb"
[1] Power On
       |
       v
+----------------------------------+
| [2] BIOS / UEFI                  |
|  - Run POST                      |
|  - Initialize firmware settings  |
|  - Detect basic hardware         |
+----------------------------------+
       |
       v
+----------------------------------+
| [3] Device Detection             |
|  - CPU, RAM, disks               |
|  - Bus controllers               |
|  - Bootable devices              |
+----------------------------------+
       |
       v
+----------------------------------+
| [4] Boot Device Selection        |
|  - BIOS reads MBR                |
|  - UEFI loads EFI executable     |
+----------------------------------+
       |
       v
+----------------------------------+
| [5] Bootloader                   |
|  - GRUB, systemd-boot, rEFInd    |
|  - Select kernel                 |
|  - Load kernel and initramfs     |
|  - Pass kernel command line      |
+----------------------------------+
       |
       v
+----------------------------------+
| [6] Linux Kernel + Initramfs     |
|  - Decompress kernel             |
|  - Initialize memory and drivers |
|  - Mount initramfs               |
|  - Find real root filesystem     |
|  - switch_root to real system    |
+----------------------------------+
       |
       v
+----------------------------------+
| [7] PID 1                        |
|  - systemd or init               |
|  - Start targets/runlevels       |
|  - Start services                |
+----------------------------------+
       |
       v
+----------------------------------+
| [8] User Space Ready             |
|  - login prompt                  |
|  - SSH                           |
|  - graphical login manager       |
|  - user sessions                 |
+----------------------------------+
```

The important idea is:

```text id="zx8hqb"
Startup is a chain.
If one stage fails, the next stage may never begin.
```

### Bootup Process

The bootup process is the ordered set of steps a computer follows after power-on until the operating system is running.

The major stages are:

1. POST
2. Firmware boot selection
3. Bootloader execution
4. Kernel loading
5. Initramfs execution
6. Real root filesystem mount
7. PID 1 startup
8. Services and login sessions

Each stage has a different responsibility.

- Firmware finds something bootable.
- Bootloader loads the kernel.
- Kernel starts the operating system.
- Initramfs finds the real root filesystem.
- PID 1 starts user-space services.

### POST: Power-On Self-Test

POST stands for Power-On Self-Test.

It is performed by system firmware, either BIOS or UEFI.

POST checks basic hardware before the operating system starts.

Common checks include:

- CPU initialization
- RAM detection
- firmware integrity
- basic chipset functions
- keyboard or display initialization
- storage controller detection
- GPU initialization

If POST fails, the operating system usually never starts.

Symptoms of POST failure may include:

- beep codes
- diagnostic LEDs
- blank screen
- firmware error message
- system powers on then shuts off

Common causes include:

- bad RAM
- loose GPU
- failed motherboard
- overheating
- power supply problems
- firmware corruption

### BIOS vs UEFI

BIOS and UEFI are firmware interfaces.

They both start the boot process, but they work differently.

### BIOS Boot

On BIOS systems, the firmware reads the first sector of the selected disk.

That first sector is the Master Boot Record, or MBR.

```text id="z3onrm"
BIOS
 |
 v
Read first 512 bytes of disk
 |
 v
Execute first-stage boot code
 |
 v
Load second-stage bootloader
```

The first-stage code is tiny, so it usually only knows how to find and load a larger bootloader.

### UEFI Boot

On UEFI systems, the firmware reads boot entries from NVRAM.

It then loads an EFI executable from the EFI System Partition, also called ESP.

```text id="mlqfdd"
UEFI firmware
     |
     v
Read NVRAM boot entry
     |
     v
Open EFI System Partition
     |
     v
Load .efi boot program
     |
     v
Run GRUB, systemd-boot, rEFInd, shim, or another loader
```

Common EFI boot files include:

- `\EFI\debian\grubx64.efi`
- `\EFI\ubuntu\shimx64.efi`
- `\EFI\Microsoft\Boot\bootmgfw.efi`

With Secure Boot, the firmware may load a signed shim first. The shim then validates and loads the next bootloader.

### MBR

MBR stands for Master Boot Record.

It is the first sector of a traditional BIOS disk.

It is usually 512 bytes.

```text id="ldxzec"
+--------------------------------------+
| Master Boot Record, 512 bytes        |
+----------------------+---------------+
| 446 bytes            | boot code     |
| 64 bytes             | partition tbl |
| 2 bytes              | 0x55AA sig    |
+----------------------+---------------+
```

The MBR contains:

- first-stage bootloader code
- traditional partition table
- boot signature

On GPT disks, a protective MBR may still exist, but the real partition information is stored in GPT structures.

### GPT and EFI System Partition

Modern systems usually use GPT with UEFI.

GPT stands for GUID Partition Table.

UEFI systems usually boot from an EFI System Partition.

The ESP is typically:

- FAT32 formatted
- mounted at /boot/efi
- contains .efi bootloader files

Check EFI partition:

```bash id="wxzllh"
lsblk -f
```

Example output:

```text id="j339dv"
NAME   FSTYPE LABEL UUID                                 MOUNTPOINTS
sda
├─sda1 vfat         1111-2222                            /boot/efi
├─sda2 ext4         aaaa-bbbb                            /boot
└─sda3 ext4         cccc-dddd                            /
```

Interpretation:

```text id="dnzhle"
sda1 is a vfat partition mounted at /boot/efi.
This is likely the EFI System Partition.
```

### Boot Device Selection

Firmware chooses a boot device based on boot order.

Common boot devices include:

- internal SSD
- NVMe drive
- USB drive
- network PXE boot
- optical media
- external disk

To change the boot order, users usually press a firmware key during startup.

Common keys include:

- `Esc`
- `F2`
- `F10`
- `F12`
- `Del`

The exact key depends on the system vendor.

On UEFI systems, boot entries can often be viewed from Linux using:

```bash id="i7vlyx"
sudo efibootmgr
```

Example output:

```text id="gxv4ga"
BootCurrent: 0002
BootOrder: 0002,0001,0000
Boot0000* Windows Boot Manager
Boot0001* UEFI USB Drive
Boot0002* debian
```

Interpretation:

```text id="q7mzup"
The current boot entry is debian.
The firmware tries debian first, then USB, then Windows.
```

### Bootloader

The bootloader loads the Linux kernel and initramfs into memory.

Common bootloaders include:

- GRUB 2
- systemd-boot
- `rEFInd`
- `LILO`
- Syslinux

The most common Linux bootloader is GRUB 2.

The bootloader usually provides:

- boot menu
- kernel selection
- recovery entries
- kernel command-line editing
- initramfs loading
- chainloading another OS

### GRUB 2

GRUB 2 can read filesystems, display menus, load kernels, load initramfs images, and pass kernel parameters.

Important files include:

- `/boot/grub/grub.cfg`
- `/etc/default/grub`
- `/etc/grub.d/`

On some Red Hat-based systems:

```text id="ls93d4"
/boot/grub2/grub.cfg
```

Important note:

```text id="sj02b7"
Do not usually edit grub.cfg directly.
Edit /etc/default/grub or files under /etc/grub.d, then regenerate the configuration.
```

Common regeneration commands:

Debian/Ubuntu:

```bash id="m4x7al"
sudo update-grub
```

Generic GRUB command:

```bash id="rfwrve"
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

Red Hat-style systems may use:

```bash id="kp5z67"
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

### Kernel Image and Initramfs

The bootloader normally loads two important files:

- `vmlinuz-*` — compressed Linux kernel image
- `initramfs-*` — early userspace image

Example:

```bash id="uyy4ri"
ls -lh /boot
```

Example output:

```text id="smcn1i"
-rw-r--r-- 1 root root  12M vmlinuz-6.8.0
-rw-r--r-- 1 root root  45M initramfs-6.8.0.img
-rw-r--r-- 1 root root 200K config-6.8.0
```

Interpretation:

```text id="pkn2qi"
The kernel image is vmlinuz-6.8.0.
The initramfs image contains early boot tools and drivers.
```

### Kernel Command Line

The bootloader passes parameters to the kernel.

View the current kernel command line:

```bash id="u7sjn8"
cat /proc/cmdline
```

Example output:

```text id="wrum9x"
BOOT_IMAGE=/vmlinuz-6.8.0 root=UUID=abcd-1234 ro quiet splash
```

Important parameters:

- `root=UUID=...` — real root filesystem
- `ro` — initially mount root read-only
- `quiet` — reduce boot messages
- `systemd.unit=rescue.target` — boot into rescue mode
- `rd.break` — break into initramfs emergency shell
- `single` — single-user style boot

### Kernel Initialization

After the bootloader transfers control, the kernel begins initialization.

The kernel:

- decompresses itself
- sets up memory management
- initializes CPU features
- starts scheduler
- initializes device drivers
- mounts initramfs
- detects hardware
- loads needed modules
- finds the real root filesystem
- starts PID 1

A simplified flow:

```text id="rgqlpo"
Kernel image starts
       |
       v
Initialize CPU and memory
       |
       v
Initialize drivers
       |
       v
Mount initramfs
       |
       v
Find real root filesystem
       |
       v
switch_root or pivot_root
       |
       v
Start /sbin/init or systemd
```

### Initramfs

Initramfs stands for initial RAM filesystem.

It is a temporary filesystem loaded into memory during early boot.

It contains tools and drivers needed before the real root filesystem is available.

Initramfs may contain:

- storage drivers
- filesystem drivers
- LVM tools
- RAID tools
- encryption tools
- network boot tools
- busybox or dracut tools
- early boot scripts

Initramfs is especially important when the root filesystem is on:

- `LVM`
- encrypted disk
- software RAID
- network storage
- special storage controller

If initramfs cannot find or mount the real root filesystem, boot may fail.

### switch_root and pivot_root

After initramfs finds and mounts the real root filesystem, the system must move from the temporary root to the real root.

This is commonly done with:

```text id="f8i23x"
switch_root
```

or historically:

```text id="rk66g4"
pivot_root
```

Conceptual flow:

```text id="s3c8wg"
Temporary initramfs root
        |
        v
Mount real root filesystem
        |
        v
Switch to real root
        |
        v
Run real /sbin/init or systemd
```

### PID 1

PID 1 is the first user-space process.

On most modern Linux systems, PID 1 is systemd.

Check PID 1:

```bash id="lcjzjy"
ps -p 1 -o pid,comm,args
```

Example output:

```text id="v25fic"
PID COMMAND ARGS
1   systemd /usr/lib/systemd/systemd
```

Interpretation:

```text id="kqhj54"
systemd is PID 1.
It is responsible for starting and supervising user-space services.
```

On older systems, PID 1 may be:

```text id="khbnaj"
init
```

or alternatives such as:

- `OpenRC`
- runit
- s6

### SysV Init

SysV init is an older initialization system.

It uses:

- `/etc/inittab`
- `/etc/init.d/`
- `/etc/rc.d/`

SysV init organizes system states using runlevels.

Commands include:

```bash id="hp8e72"
runlevel
sudo telinit 3
```

SysV init is less common on modern mainstream distributions but still appears in older systems and compatibility layers.

### systemd

systemd is the dominant init system on many modern Linux distributions.

It manages:

- services
- targets
- mounts
- devices
- timers
- sockets
- logging through journald
- dependency ordering
- parallel startup

systemd uses unit files.

Common unit types include:

- `.service`
- `.target`
- `.mount`
- `.socket`
- `.timer`
- `.device`

### systemd Startup Flow

systemd starts units according to dependencies.

A simplified target flow:

```text id="eq8i0e"
default.target
      |
      v
multi-user.target or graphical.target
      |
      +--> sysinit.target
      |       fsck, sysctl, modules, udev
      |
      +--> basic.target
      |       journald, sockets, basic services
      |
      +--> multi-user services
              sshd, cron, networking, getty
```

If the system boots to a GUI, `graphical.target` includes display-manager services.

```text id="r2o62l"
graphical.target
      |
      v
multi-user.target
      |
      v
display-manager.service
      |
      v
graphical login screen
```

### Runlevels

Runlevels are the traditional SysV way to represent system state.

- 0 — halt or power off
- 1 — single-user or rescue
- 2 — multi-user, distro-specific
- 3 — multi-user with networking, no GUI
- 4 — custom or unused
- 5 — multi-user with GUI
- 6 — reboot

Runlevel meaning can vary between distributions.

Check runlevel:

```bash id="zrtu9o"
runlevel
```

Example output:

```text id="bgtgij"
N 5
```

Interpretation:

```text id="mutq9z"
There was no previous runlevel.
The current runlevel is 5.
```

### systemd Targets

systemd replaces runlevels with targets.

Common targets:

- `poweroff.target` — power off
- `rescue.target` — basic rescue mode
- `emergency.target` — very minimal emergency shell
- `multi-user.target` — text-mode multi-user system
- `graphical.target` — graphical login and multi-user services
- `reboot.target` — reboot

Approximate mapping:

- `runlevel 0` → `poweroff.target`
- `runlevel 1` → `rescue.target`
- `runlevel 3` → `multi-user.target`
- `runlevel 5` → `graphical.target`
- `runlevel 6` → `reboot.target`

Check default target:

```bash id="hi1zhb"
systemctl get-default
```

Example:

```text id="ss95c8"
graphical.target
```

Set default target:

```bash id="cbyoxj"
sudo systemctl set-default multi-user.target
```

Switch target immediately:

```bash id="3moclj"
sudo systemctl isolate multi-user.target
```

Important:

```text id="qmxfc8"
set-default changes future boots.
isolate changes the current running state.
```

### Login Prompts and User Sessions

After startup reaches the appropriate target, login services become available.

Text login prompts are usually provided by:

```text id="asxzi9"
getty@.service
```

Example:

```bash id="ko35no"
systemctl status getty@tty1.service
```

SSH login is usually provided by:

```text id="ro7pfu"
sshd.service
```

Graphical login is provided by a display manager, such as:

- gdm
- sddm
- lightdm
- xdm

User sessions may load shell startup files such as:

- `/etc/profile`
- `~/.bash_profile`
- `~/.bashrc`

### Boot Logs

Boot logs are essential for diagnosing startup problems.

View logs from the current boot:

```bash id="a62vyn"
journalctl -b
```

Show only errors from current boot:

```bash id="r9xbbc"
journalctl -b -p err
```

Show previous boot:

```bash id="rf3ot3"
journalctl -b -1
```

Show kernel messages:

```bash id="v755aj"
journalctl -k -b
```

Example:

```text id="s5dwxy"
Jun 01 10:00:05 host systemd[1]: Started OpenSSH server daemon.
Jun 01 10:00:08 host kernel: EXT4-fs (sda3): mounted filesystem with ordered data mode.
```

Interpretation:

```text id="aw3nh3"
systemd started sshd.
The kernel mounted the root filesystem successfully.
```

### Boot Performance Tools

systemd includes tools for measuring boot performance.

Show total boot time:

```bash id="dvbzoy"
systemd-analyze
```

Example output:

```text id="h1qpq3"
Startup finished in 4.123s (kernel) + 12.456s (userspace) = 16.579s
graphical.target reached after 12.200s in userspace.
```

Interpretation:

```text id="dedcdg"
The kernel stage took about 4.1 seconds.
User-space services took about 12.5 seconds.
The graphical target was reached after about 12.2 seconds.
```

Show slow services:

```bash id="mvvctw"
systemd-analyze blame
```

Example output:

```text id="jp1zjg"
12.000s slow-demo.service
 3.500s NetworkManager-wait-online.service
 1.200s sshd.service
```

Interpretation:

```text id="di6l0y"
slow-demo.service took the most time.
NetworkManager wait-online also contributed to boot delay.
```

Show dependency chain:

```bash id="b2o4nb"
systemd-analyze critical-chain
```

This helps identify services that delay the boot path.

### Kernel Panic

A kernel panic is an unrecoverable kernel error.

When it happens, the kernel cannot safely continue.

Symptoms may include:

- panic message on console
- stack trace
- system freeze
- automatic reboot
- failure to mount root filesystem

Common causes:

- bad RAM
- failing disk
- buggy kernel module
- broken storage driver
- filesystem corruption
- bad kernel update
- misconfigured custom kernel

Example panic message:

```text id="x3d5tn"
Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)
```

Interpretation:

```text id="a0ff8c"
The kernel could not mount the root filesystem.
Possible causes include wrong root= parameter, missing initramfs driver, bad disk, or filesystem problem.
```

### Kernel Panic Recovery Workflow

When diagnosing a panic:

1. Photograph or capture the panic message.
2. Boot an older kernel from GRUB if available.
3. Boot rescue mode or live USB.
4. Check storage and filesystem health.
5. Check recent kernel or driver updates.
6. Review logs from previous boot.
7. Rebuild initramfs if storage drivers are missing.
8. Test RAM and hardware if errors persist.

Useful commands after booting rescue or a working kernel:

```bash id="kfk1p3"
journalctl -b -1 -p err
journalctl -k -b -1
dmesg -T
lsblk -f
blkid
fsck
```

### Basic System Management Commands

### Hostname

View hostname:

```bash id="vcy4my"
hostname
```

Set hostname on systemd systems:

```bash id="qdxo0j"
sudo hostnamectl set-hostname server01
```

Verify:

```bash id="pd936q"
hostnamectl
```

Example output:

```text id="nkf1pg"
Static hostname: server01
Operating System: Ubuntu
Kernel: Linux 6.8.0
Architecture: x86-64
```

Interpretation:

```text id="py0kyo"
The system hostname is server01.
This name identifies the machine on the network and in logs.
```

### Uptime

Check uptime:

```bash id="xjcs94"
uptime
```

Example output:

```text id="b1nsnl"
15:20:10 up 3 days,  4:12,  2 users,  load average: 0.10, 0.20, 0.18
```

Interpretation:

```text id="h4geqj"
The system has been running for 3 days and 4 hours.
Two users are logged in.
Load average is low.
```

Uptime helps confirm whether a reboot happened recently.

### Reboot

Reboot immediately:

```bash id="ls9map"
sudo reboot
```

or:

```bash id="d417sx"
sudo systemctl reboot
```

Schedule reboot in 5 minutes:

```bash id="u7jm8s"
sudo shutdown -r +5
```

Cancel scheduled shutdown or reboot:

```bash id="l7twmd"
sudo shutdown -c
```

### Shutdown

Shutdown immediately:

```bash id="xb0lpt"
sudo shutdown now
```

or:

```bash id="synk22"
sudo systemctl poweroff
```

Schedule shutdown in 30 minutes:

```bash id="soxn5f"
sudo shutdown -h +30
```

Broadcast message example:

```bash id="en66d5"
sudo shutdown -h +30 "System maintenance in 30 minutes"
```

### Timezone

Show time settings:

```bash id="dsgip4"
timedatectl
```

List timezones:

```bash id="b6sc70"
timedatectl list-timezones
```

Set timezone:

```bash id="k2d1fj"
sudo timedatectl set-timezone Europe/Berlin
```

Verify:

```bash id="f1a0go"
timedatectl
```

Correct timezone matters for:

- logs
- cron jobs
- systemd timers
- security investigations
- scheduled maintenance
- distributed systems

### Root Password Recovery

Root password recovery is a sensitive administrative procedure.

Only perform it on systems you own or are authorized to administer.

A common Red Hat-style recovery method uses:

```text id="fpqif8"
rd.break
```

This breaks into initramfs before the real root filesystem is fully started.

General flow:

1. Reboot.
2. Open GRUB menu.
3. Edit kernel command line.
4. Add rd.break.
5. Boot into emergency shell.
6. Remount sysroot read-write.
7. chroot into /sysroot.
8. Change password.
9. Trigger SELinux relabel if needed.
10. Reboot.

Commands after reaching the emergency shell:

```bash id="rsbgu9"
mount -o remount,rw /sysroot
chroot /sysroot
passwd root
touch /.autorelabel
exit
exit
```

Interpretation:

```text id="r4n5jx"
The root filesystem is remounted writable.
chroot makes /sysroot behave like /.
passwd changes the root password.
.autorelabel tells SELinux to relabel files on next boot.
```

On Debian/Ubuntu systems, recovery may use GRUB recovery mode or `init=/bin/bash` depending on setup.

### Scenario 1: Measure Boot Time and Find Slow Services

#### Goal

Identify what slowed down the boot process.

#### Simulate a Boot Delay

Create a test service that sleeps during boot:

```bash id="r732tc"
sudo tee /etc/systemd/system/slow-demo.service > /dev/null <<'EOF'
[Unit]
Description=Slow Boot Demo Service

[Service]
Type=oneshot
ExecStart=/bin/sleep 20

[Install]
WantedBy=multi-user.target
EOF
```

Enable it:

```bash id="csh81m"
sudo systemctl daemon-reload
sudo systemctl enable slow-demo.service
```

Reboot:

```bash id="qbehlk"
sudo systemctl reboot
```

#### Check with `systemd-analyze`

After reboot:

```bash id="tjy0tj"
systemd-analyze
```

Example output:

```text id="wk2kdl"
Startup finished in 3.800s (kernel) + 25.400s (userspace) = 29.200s
multi-user.target reached after 25.100s in userspace.
```

#### Check Slow Services

```bash id="pupmma"
systemd-analyze blame | head
```

Example output:

```text id="yy6b4w"
20.010s slow-demo.service
 3.400s NetworkManager-wait-online.service
 1.100s sshd.service
```

#### Interpretation

```text id="m2p2od"
The boot delay is mostly caused by slow-demo.service.
The kernel was not the main bottleneck.
The userspace service startup path was delayed.
```

#### Cleanup

```bash id="pej7mp"
sudo systemctl disable --now slow-demo.service
sudo rm -f /etc/systemd/system/slow-demo.service
sudo systemctl daemon-reload
```

### Scenario 2: Diagnose a Failed Service During Boot

#### Goal

Simulate a service that fails during boot and diagnose it.

#### Create a Broken Service

```bash id="g9voos"
sudo tee /etc/systemd/system/broken-boot.service > /dev/null <<'EOF'
[Unit]
Description=Broken Boot Demo Service

[Service]
Type=oneshot
ExecStart=/not/a/real/command

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start:

```bash id="e80zry"
sudo systemctl daemon-reload
sudo systemctl enable broken-boot.service
sudo systemctl start broken-boot.service
```

#### Check Failed Units

```bash id="wsj8n7"
systemctl --failed
```

Example output:

```text id="vkczio"
UNIT                 LOAD   ACTIVE SUB    DESCRIPTION
broken-boot.service  loaded failed failed Broken Boot Demo Service
```

#### Check Status

```bash id="y2fe05"
systemctl status broken-boot.service
```

Example output:

```text id="b7kxxp"
Active: failed (Result: exit-code)
Process: 1300 ExecStart=/not/a/real/command (code=exited, status=203/EXEC)
```

#### Check Logs

```bash id="rhwb7l"
journalctl -u broken-boot.service -b
```

Example output:

```text id="v1fd1y"
Failed to locate executable /not/a/real/command
Failed at step EXEC spawning /not/a/real/command: No such file or directory
```

#### Interpretation

```text id="dmvfzk"
The service failed because ExecStart points to a missing executable.
This is not a kernel or bootloader problem.
It is a systemd unit configuration problem.
```

#### Cleanup

```bash id="v8oxuf"
sudo systemctl disable broken-boot.service
sudo rm -f /etc/systemd/system/broken-boot.service
sudo systemctl daemon-reload
sudo systemctl reset-failed
```

### Scenario 3: Simulate Wrong Default Target

#### Goal

Understand the difference between text-mode and graphical boot.

#### Check Current Default Target

```bash id="wdx09z"
systemctl get-default
```

Example:

```text id="xnpwed"
graphical.target
```

#### Change Future Boots to Text Mode

```bash id="xoffg7"
sudo systemctl set-default multi-user.target
```

Reboot:

```bash id="lb3r6q"
sudo reboot
```

#### Check After Boot

```bash id="tolv9c"
systemctl get-default
systemctl list-units --type=target --state=active
```

Example output:

```text id="mz0s9l"
multi-user.target
```

#### Interpretation

```text id="tmz15v"
The system is configured to boot into text-mode multi-user state.
A graphical login manager may not start automatically.
```

#### Restore Graphical Boot

```bash id="rxabgf"
sudo systemctl set-default graphical.target
sudo systemctl isolate graphical.target
```

### Scenario 4: Boot into Rescue Target

#### Goal

Practice entering a limited maintenance environment.

#### Temporary Boot Method

At GRUB, edit the kernel command line and add:

```text id="sbsfd0"
systemd.unit=rescue.target
```

Boot with the edited entry.

#### Runtime Method

From a running system:

```bash id="eov6me"
sudo systemctl isolate rescue.target
```

#### Check

```bash id="kjcv5t"
systemctl list-units --type=target --state=active
```

Example output:

```text id="g6h0lm"
rescue.target loaded active active Rescue Mode
```

#### Interpretation

```text id="ndpyo0"
The system is in rescue mode.
Only essential services are running.
This mode is useful for maintenance and repair.
```

#### Return to Normal Target

```bash id="keknkw"
sudo systemctl isolate multi-user.target
```

or for GUI:

```bash id="uh6gsb"
sudo systemctl isolate graphical.target
```

### Scenario 5: Diagnose a Boot Problem from Logs

#### Goal

Use journal logs to find errors from the current or previous boot.

#### Check Current Boot Errors

```bash id="xsu55c"
journalctl -b -p err
```

Example output:

```text id="sem6y0"
Jun 01 10:05:01 host systemd[1]: failed-demo.service: Failed with result 'exit-code'.
Jun 01 10:05:01 host kernel: ata1.00: failed command: READ FPDMA QUEUED
```

#### Interpretation

```text id="sy2xml"
One service failed.
The kernel also reported a disk-related error.
The service failure and disk error should be investigated separately.
```

#### Check Previous Boot

```bash id="kjs5ws"
journalctl -b -1 -p err
```

Interpretation:

```text id="xtzl72"
Previous boot logs help diagnose failures that happened before the last reboot.
```

### Scenario 6: Simulate and Cancel Scheduled Shutdown

#### Goal

Practice scheduling and canceling shutdowns safely.

#### Schedule Shutdown

```bash id="qojyki"
sudo shutdown -h +10 "Test shutdown in 10 minutes"
```

Example broadcast:

```text id="rgyhvs"
Broadcast message from root:
The system is going down for poweroff in 10 minutes!
```

#### Cancel It

```bash id="v27fur"
sudo shutdown -c
```

#### Interpretation

```text id="oq3yuk"
The shutdown was scheduled.
shutdown -c canceled it before it happened.
This is useful during maintenance planning.
```

#### Schedule Reboot

```bash id="ql27hh"
sudo shutdown -r +5 "Test reboot in 5 minutes"
```

Cancel:

```bash id="b4rklz"
sudo shutdown -c
```

### Scenario 7: Verify a Reboot with Uptime

#### Goal

Confirm that a system actually restarted.

#### Before Reboot

```bash id="k373fp"
uptime
```

Example:

```text id="pmvy42"
up 14 days, 3:21
```

Reboot:

```bash id="hamhxs"
sudo systemctl reboot
```

After reboot:

```bash id="dxkbxd"
uptime
```

Example:

```text id="k2lojr"
up 2 min
```

#### Interpretation

```text id="r55dh3"
The uptime reset from 14 days to 2 minutes.
This confirms the system rebooted.
```

### Scenario 8: Investigate Kernel Panic: Root Filesystem Not Found

#### Goal

Understand a common boot panic pattern.

#### Simulated Symptom

Console shows:

```text id="l9vn9d"
Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)
```

#### Check from Rescue Environment

Boot from an older kernel, rescue mode, or live USB.

Check disks:

```bash id="bayya4"
lsblk -f
blkid
```

Example:

```text id="mq5br6"
NAME   FSTYPE UUID       MOUNTPOINTS
sda1   vfat   1111-2222  /boot/efi
sda2   ext4   aaaa-bbbb  /boot
sda3   ext4   cccc-dddd  /
```

Check kernel command line from bootloader configuration:

```bash id="uc7qd3"
grep -R "root=" /boot/grub* /boot/loader 2>/dev/null
```

Example problem:

```text id="suuohk"
root=UUID=wrong-uuid
```

#### Interpretation

```text id="mdsq4f"
The kernel was told to mount a root filesystem UUID that does not exist.
Fix GRUB configuration or filesystem UUID references.
```

#### Possible Fixes

- correct root= UUID
- rebuild GRUB configuration
- rebuild initramfs
- check disk health
- restore missing storage drivers

### Scenario 9: Recover Root Password in a Lab VM

#### Goal

Practice emergency administrative recovery.

#### GRUB Step

At GRUB, edit the kernel entry and add:

```text id="j5ebxn"
rd.break
```

Boot with Ctrl-X or F10.

#### Emergency Shell Commands

```bash id="nnpzyc"
mount -o remount,rw /sysroot
chroot /sysroot
passwd root
touch /.autorelabel
exit
exit
```

#### Example Output

```text id="u9fox9"
Changing password for user root.
New password:
Retype new password:
passwd: all authentication tokens updated successfully.
```

#### Interpretation

```text id="p39e4d"
The root password was changed.
SELinux relabeling was requested for the next boot.
The system should reboot and allow login with the new password.
```

#### Safety Note

```text id="ws7jct"
This is for authorized recovery only.
Physical or console access to a machine often means administrative control is possible.
Protect servers with disk encryption, firmware passwords, and cloud access controls where appropriate.
```

### Scenario 10: Inspect systemd Timers During Startup Maintenance

#### Goal

Understand scheduled system maintenance managed by systemd.

#### Check Timers

```bash id="khbsx3"
systemctl list-timers --all
```

Example output:

```text id="x1a9yj"
NEXT                        LEFT    LAST                        PASSED UNIT                         ACTIVATES
Mon 2026-06-15 00:00:00     8h      Sun 2026-06-14 00:00:00     16h    logrotate.timer              logrotate.service
Mon 2026-06-15 06:00:00     14h     Sun 2026-06-14 06:00:00     10h    apt-daily.timer               apt-daily.service
```

#### Interpretation

```text id="s7f26m"
logrotate.timer activates logrotate.service.
apt-daily.timer activates apt-daily.service.
Timers are systemd's scheduled task mechanism, similar in purpose to cron.
```

### Scenario 11: Set and Verify Timezone

#### Goal

Ensure logs and schedules use the correct local time.

#### Check

```bash id="ki86qm"
timedatectl
```

Example output:

```text id="fdbfai"
Time zone: UTC (UTC, +0000)
System clock synchronized: yes
```

#### Change

```bash id="hqwby8"
sudo timedatectl set-timezone Europe/Berlin
```

#### Verify

```bash id="qtq4dj"
timedatectl
```

Example output:

```text id="l6kxm7"
Time zone: Europe/Berlin (CEST, +0200)
System clock synchronized: yes
```

#### Interpretation

```text id="x1owfd"
The system timezone is now Europe/Berlin.
Logs, cron jobs, and timers will use this timezone unless configured otherwise.
```

### Scenario 12: Create a Simple Cron Maintenance Task

#### Goal

Use cron for scheduled maintenance.

#### Create a Backup Script

```bash id="p9otcd"
mkdir -p ~/maintenance-demo
cat > ~/maintenance-demo/backup-demo.sh <<'EOF'
#!/bin/bash
mkdir -p "$HOME/maintenance-demo/backups"
tar -czf "$HOME/maintenance-demo/backups/home-backup-$(date +%F).tar.gz" "$HOME/maintenance-demo" 2>/dev/null
EOF

chmod +x ~/maintenance-demo/backup-demo.sh
```

#### Add Cron Job

Edit crontab:

```bash id="ghr3d0"
crontab -e
```

Add:

```text id="ufjjg2"
0 0 * * * /home/user/maintenance-demo/backup-demo.sh
```

#### Interpretation

```text id="krv0s4"
The script runs every day at midnight.
Cron is useful for recurring maintenance tasks.
```

#### Verify Cron Service

```bash id="k4sfo5"
systemctl status cron
```

or on some systems:

```bash id="lgcoft"
systemctl status crond
```

### Common Startup Problems and Fixes

#### Problem: System Boots Slowly

Check:

```bash id="vxfaj9"
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
journalctl -b -p warning
```

Common causes:

- slow service
- network wait timeout
- failed mount
- disk issue
- DNS delay
- bad dependency ordering

### Problem: Service Fails at Boot

Check:

```bash id="zxjdk1"
systemctl --failed
systemctl status service-name
journalctl -u service-name -b
```

Common causes:

- missing executable
- bad config
- wrong permissions
- missing dependency
- port conflict
- filesystem not mounted yet

### Problem: Boot Drops to Emergency Mode

Check:

```bash id="sf4psr"
journalctl -xb
systemctl --failed
mount -a
cat /etc/fstab
lsblk -f
```

Common causes:

- bad /etc/fstab entry
- missing disk
- wrong UUID
- filesystem check failure
- root filesystem issue

A common fix for optional disks is adding:

```text id="dwvzog"
nofail
```

to the `/etc/fstab` options, if appropriate.

### Problem: GRUB Menu Does Not Show

Try during boot:

- hold Shift on BIOS systems
- press Esc on many UEFI systems

Also check GRUB configuration:

```bash id="mhdizk"
grep GRUB_TIMEOUT /etc/default/grub
```

### Problem: Kernel Panic After Update

Try:

- boot older kernel from GRUB
- boot rescue mode
- check journal from previous boot
- rebuild initramfs
- reinstall known-good kernel
- check third-party kernel modules

Commands:

```bash id="hz6sj1"
journalctl -b -1 -p err
ls /boot
uname -r
```

### Useful Command Summary

Boot and firmware:

```bash id="br2c8u"
sudo efibootmgr
lsblk -f
cat /proc/cmdline
ls -lh /boot
```

systemd boot state:

```bash id="or2ic8"
ps -p 1 -o pid,comm,args
systemctl get-default
systemctl list-units --type=target --state=active
systemctl --failed
```

Boot performance:

```bash id="hy7anf"
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
```

Logs:

```bash id="krnw1i"
journalctl -b
journalctl -b -p err
journalctl -k -b
journalctl -b -1
```

Targets:

```bash id="xjjvx6"
sudo systemctl isolate multi-user.target
sudo systemctl isolate graphical.target
sudo systemctl set-default multi-user.target
sudo systemctl set-default graphical.target
```

System management:

```bash id="gg7tpd"
hostname
hostnamectl
uptime
sudo reboot
sudo systemctl reboot
sudo shutdown -r +5
sudo shutdown -h +30
sudo shutdown -c
timedatectl
```

Timers and cron:

```bash id="swyh8o"
systemctl list-timers --all
crontab -e
crontab -l
```

### Safe Lab Cleanup

Remove slow demo service:

```bash id="pez11t"
sudo systemctl disable --now slow-demo.service 2>/dev/null
sudo rm -f /etc/systemd/system/slow-demo.service
```

Remove broken boot service:

```bash id="d223j8"
sudo systemctl disable --now broken-boot.service 2>/dev/null
sudo rm -f /etc/systemd/system/broken-boot.service
```

Reload systemd:

```bash id="zw5jhh"
sudo systemctl daemon-reload
sudo systemctl reset-failed
```

Return to graphical target if needed:

```bash id="nhdoye"
sudo systemctl set-default graphical.target
sudo systemctl isolate graphical.target
```

Cancel scheduled shutdown if one exists:

```bash id="uo9x3g"
sudo shutdown -c
```

### Challenges

1. Reboot a lab system, then use `uptime` to confirm that the reboot happened.
2. Check your hostname with `hostname`, change it with `hostnamectl`, and verify the result.
3. Use `systemd-analyze`, `systemd-analyze blame`, and `systemd-analyze critical-chain` to identify slow boot components.
4. Create a slow demo service that sleeps for 20 seconds during boot. Reboot, measure the delay, then remove the service.
5. Create a broken systemd service, start it, inspect `systemctl --failed`, read its logs, and fix or remove it.
6. Check your default systemd target. Switch between `multi-user.target` and `graphical.target` on a lab machine.
7. Schedule a shutdown in 10 minutes, then cancel it with `shutdown -c`.
8. Use `journalctl -b -p err` to review errors from the current boot.
9. Use `systemctl list-timers --all` to identify scheduled maintenance tasks and the services they activate.
10. Practice root password recovery only in a lab VM. Document the GRUB parameter used, commands run, and why SELinux relabeling may be needed.
11. Research a kernel panic message and write a diagnosis plan that includes logs, hardware checks, older kernel boot, rescue mode, and backups.
12. Set the timezone with `timedatectl`, verify it, and explain why timezone correctness matters for logs and scheduled tasks.
