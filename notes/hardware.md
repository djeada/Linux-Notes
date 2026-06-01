## Hardware on Linux

Linux is well known for running on a wide range of hardware. It can run on laptops, desktops, servers, embedded systems, routers, single-board computers, virtual machines, and high-performance clusters.

Linux supports this variety because the kernel is modular. Hardware support can be built directly into the kernel or added through loadable kernel modules, often called drivers.

At a high level, Linux hardware management looks like this:

```text id="jc73u6"
Hardware device
      |
      v
Kernel driver
      |
      v
Device file, interface, or subsystem
      |
      v
User-space tools and applications
```

For example, a storage device may appear as `/dev/sda`, a network card may appear as `eth0` or `enp0s3`, and a USB keyboard may appear through the input subsystem.

The main idea is:

- Linux detects hardware.
- The kernel assigns a driver.
- The device becomes available to the system.
- User-space tools inspect, configure, or use it.

### Hardware Compatibility

Linux supports many hardware devices, but support depends on drivers.

Some hardware works immediately because the driver is already included in the Linux kernel. Other hardware may require extra firmware, vendor drivers, or newer kernel versions.

Hardware support is usually best when:

- the manufacturer provides Linux support
- the device uses a common chipset
- the driver is included in the kernel
- the distribution includes required firmware
- the hardware has been available long enough for mature support

Hardware support can be more difficult when:

- the device is very new
- the manufacturer provides no documentation
- the driver is proprietary
- firmware is missing
- the hardware uses unusual or unsupported chipsets

Common areas where driver issues may appear include:

- Wi-Fi adapters
- Bluetooth adapters
- graphics cards
- webcams
- fingerprint readers
- special function keys
- touchpads
- audio devices
- new storage controllers

### Hardware Architecture Support

Linux can run on many CPU architectures.

Common architectures include:

- x86_64 / AMD64
- ARM / ARM64
- PowerPC
- MIPS
- SPARC
- RISC-V

The most common architecture for laptops, desktops, and servers is usually `x86_64`.

ARM and ARM64 are common in phones, embedded systems, Raspberry Pi boards, cloud servers, and low-power devices.

RISC-V is an emerging open hardware architecture.

To check the current system architecture:

```bash id="dfh7la"
uname -m
```

Example output:

```text id="z0lqxk"
x86_64
```

To see more CPU architecture information:

```bash id="m5zpfw"
lscpu
```

### Hardware as Files

Linux follows the Unix idea that many system resources can be represented as files.

Hardware devices are often represented under:

```text id="env1ma"
/dev
```

The `/dev` directory contains device files.

These files are special interfaces to hardware or kernel features.

```text id="o7zt5z"
+-------------------+
| User command      |
| cat, dd, program  |
+-------------------+
          |
          v
+-------------------+
| Device file       |
| /dev/sda          |
| /dev/null         |
| /dev/input/event0 |
+-------------------+
          |
          v
+-------------------+
| Kernel driver     |
+-------------------+
          |
          v
+-------------------+
| Hardware / kernel |
+-------------------+
```

### Types of Device Files

There are three common categories to know.

- block devices
- character devices
- special virtual devices

### Block Devices

Block devices transfer data in blocks.

Examples include:

- /dev/sda
- /dev/sdb
- /dev/nvme0n1
- /dev/loop0

These usually represent disks, partitions, SSDs, NVMe drives, USB storage, and loop devices.

To list block devices:

```bash id="jeom3r"
lsblk
```

Example output:

```text id="n83phz"
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0 238.5G  0 disk
├─sda1   8:1    0   512M  0 part /boot/efi
├─sda2   8:2    0     1G  0 part /boot
└─sda3   8:3    0   237G  0 part /
sr0     11:0    1  1024M  0 rom
```

Interpretation:

- sda is a disk
- sda1, sda2, and sda3 are partitions
- sr0 is an optical drive
- MOUNTPOINTS shows where partitions are mounted

### Character Devices

Character devices transfer data as a stream of characters or bytes.

Examples include:

- /dev/tty
- /dev/ttyS0
- /dev/input/event0
- /dev/random
- /dev/urandom

Character devices are common for terminals, serial ports, input devices, and random number sources.

To inspect a device file:

```bash id="v8zpqc"
ls -l /dev/null /dev/sda
```

Example output:

```text id="pu5306"
crw-rw-rw- 1 root root 1, 3 Jun  1 10:00 /dev/null
brw-rw---- 1 root disk 8, 0 Jun  1 10:00 /dev/sda
```

Interpretation:

- c at the start means character device
- b at the start means block device

### Special Devices

Linux has special virtual devices that are not normal hardware.

Examples:

- /dev/null
- /dev/zero
- /dev/random
- /dev/urandom

`/dev/null` discards anything written to it.

Example:

```bash id="d9z0vs"
echo "discard this" > /dev/null
```

`/dev/zero` produces endless zero bytes.

Example:

```bash id="aj50dr"
head -c 16 /dev/zero | xxd
```

`/dev/random` and `/dev/urandom` provide random data.

### Device Permissions

Device files have normal Linux permissions.

Example:

```bash id="t68tjm"
ls -l /dev/sda
```

Example output:

```text id="etzpbf"
brw-rw---- 1 root disk 8, 0 Jun  1 10:00 /dev/sda
```

Interpretation:

- root owns the device
- the disk group has access
- normal users may not access it directly

This is why many hardware commands require `sudo`.

### udev

`udev` is the Linux device manager.

It creates device files dynamically when hardware appears and removes them when hardware disappears.

For example, when you plug in a USB drive, the kernel detects it, then `udev` creates device entries such as:

- /dev/sdb
- /dev/sdb1

The basic flow is:

```text id="m6yfh5"
Hardware event
      |
      v
Kernel detects device
      |
      v
udev receives event
      |
      v
Device file is created or updated
      |
      v
System can use the device
```

`udev` can also apply permissions, create symlinks, and trigger rules.

### Gathering Hardware Information

Linux provides many tools for identifying hardware.

The most useful commands are:

- lspci     PCI devices
- lsusb     USB devices
- lscpu     CPU information
- lsblk     block devices
- lshw      full hardware summary
- dmesg     kernel hardware messages
- udevadm   udev events and device information

### PCI Devices with `lspci`

PCI devices include graphics cards, network cards, storage controllers, sound cards, and many motherboard components.

Run:

```bash id="yof2e7"
lspci
```

For more detail:

```bash id="k6ir1q"
lspci -vvv
```

To show which driver is handling each device:

```bash id="xqdy0p"
lspci -k
```

Example output:

```text id="w2zu3u"
00:1f.2 SATA controller: Intel Corporation 8 Series SATA Controller
        Kernel driver in use: ahci
        Kernel modules: ahci

01:00.0 VGA compatible controller: NVIDIA Corporation GP107M
        Kernel driver in use: nvidia
        Kernel modules: nvidiafb, nouveau, nvidia_drm, nvidia
```

Interpretation:

- The SATA controller is using the ahci driver.
- The NVIDIA GPU is using the nvidia driver.
- Available possible modules are also shown.

This is useful when checking whether the correct driver is loaded.

### USB Devices with `lsusb`

USB devices include webcams, keyboards, mice, flash drives, Bluetooth adapters, printers, and external storage.

Run:

```bash id="i7q9go"
lsusb
```

Verbose output:

```bash id="jglyvs"
lsusb -v
```

Example output:

```text id="h7l2p2"
Bus 002 Device 003: ID 0bda:5689 Realtek Semiconductor Corp. Integrated Webcam
```

Interpretation:

- Bus 002 Device 003 identifies where the device is connected.
- 0bda:5689 is the vendor ID and product ID.
- Realtek Integrated Webcam is the detected device.

Vendor and product IDs are useful when searching for driver information.

### CPU Information with `lscpu`

Run:

```bash id="y4rs4q"
lscpu
```

Example output:

```text id="k103am"
Architecture:            x86_64
CPU(s):                  8
Thread(s) per core:      2
Core(s) per socket:      4
Socket(s):               1
Vendor ID:               GenuineIntel
Model name:              Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
```

Interpretation:

- The system is x86_64.
- It has 8 logical CPUs.
- There are 4 physical cores with 2 threads per core.

This helps understand CPU capacity and architecture.

### Storage Devices with `lsblk`

Run:

```bash id="cecxci"
lsblk
```

More useful filesystem view:

```bash id="jrxert"
lsblk -f
```

Example output:

```text id="dhkbf0"
NAME   FSTYPE LABEL UUID                                 MOUNTPOINTS
sda
├─sda1 vfat         1111-2222                            /boot/efi
├─sda2 ext4         aaaa-bbbb                            /boot
└─sda3 ext4         cccc-dddd                            /
```

Interpretation:

- sda is the disk.
- sda1 is a vfat EFI partition.
- sda2 and sda3 are ext4 partitions.
- sda3 is mounted as the root filesystem.

### Full Hardware Summary with `lshw`

Run:

```bash id="mdipd3"
sudo lshw -short
```

Example output:

```text id="dfzvuq"
H/W path        Device      Class          Description
======================================================
/0                          system         Latitude 5480
/0/4                        processor      Intel Core i5-7200U
/0/1c                       memory         8GiB System Memory
/0/100/14                   bus            USB 3.0 xHCI Controller
/0/100/1d/0     wlp2s0      network        Wireless 8265 / 8275
```

Interpretation:

- The system model is shown.
- The CPU, memory, USB controller, and wireless adapter are listed.
- The wireless device is associated with interface wlp2s0.

`lshw` is useful when you want a broad inventory of the system.

### Kernel Messages with `dmesg`

`dmesg` shows kernel messages, including hardware detection and errors.

Show recent messages:

```bash id="eksuzr"
dmesg | tail -50
```

With readable timestamps:

```bash id="dyjxth"
dmesg -T | tail -50
```

Example after plugging in a USB drive:

```text id="cg61kw"
[Mon Jun  1 10:15:01 2026] usb 1-1: new high-speed USB device number 3 using xhci_hcd
[Mon Jun  1 10:15:01 2026] usb 1-1: Product: Ultra USB 3.0
[Mon Jun  1 10:15:02 2026] sd 6:0:0:0: [sdb] 60062500 512-byte logical blocks
[Mon Jun  1 10:15:02 2026]  sdb: sdb1
[Mon Jun  1 10:15:02 2026] sd 6:0:0:0: [sdb] Attached SCSI removable disk
```

Interpretation:

- The USB device was detected.
- The kernel identified it as a storage device.
- It was assigned the disk name sdb.
- It has one partition, sdb1.

`dmesg` is one of the first tools to use when hardware is not detected correctly.

### Watching Hardware Events with `udevadm`

To watch hardware events live:

```bash id="l6hk6f"
sudo udevadm monitor --environment --udev
```

Example output:

```text id="y3l0pc"
UDEV  [456.789123] add /devices/pci0000:00/.../usb1/1-1 (usb)
ACTION=add
DEVNAME=/dev/bus/usb/001/003
ID_BUS=usb
ID_MODEL=Ultra_USB_3.0
ID_VENDOR=SanDisk
```

Interpretation:

- udev saw a USB device being added.
- The action is add.
- The device vendor and model were detected.

This is helpful when debugging device rules or checking whether the system notices hardware changes.

### Monitoring Hardware Performance

Hardware monitoring helps identify whether the system is overloaded, overheating, waiting on disk, running out of memory, or experiencing network problems.

Useful tools include:

- top
- htop
- vmstat
- iostat
- ss
- sensors
- glances
- nmon

### CPU and Process Monitoring with `top` and `htop`

Run:

```bash id="rnyk97"
top
```

or:

```bash id="x7e6te"
htop
```

Example `top` output:

```text id="rfa7mg"
%Cpu(s): 25.0 us,  5.0 sy, 65.0 id,  5.0 wa
MiB Mem :  16384.0 total, 8192.0 used, 2048.0 free, 6144.0 buff/cache

PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM COMMAND
5678 user      20   0 2625488   1.2g   9456 S 100.0  7.5 process_name
```

Interpretation:

- process_name is using one full CPU core.
- CPU idle is still 65%, so the whole system is not fully CPU-saturated.
- I/O wait is 5%, which is not very high.

Important fields:

- %CPU   CPU usage by process
- %MEM   memory usage by process
- RES    resident memory actually used in RAM
- S      process state
- wa     CPU time spent waiting on I/O

### System Overview with `vmstat`

Run:

```bash id="vpknsm"
vmstat 5
```

This prints system statistics every 5 seconds.

Example output:

```text id="uhvw5p"
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 823456  23456 345678    0    0     1     2  300  500  5  1 93  1  0
```

Interpretation:

- r = 1 means one process is waiting to run.
- b = 0 means no blocked processes.
- si and so are 0, so the system is not swapping.
- wa = 1 means little time is spent waiting on disk I/O.

Important fields:

- r    runnable processes
- b    blocked processes
- si   swap in
- so   swap out
- bi   blocks read from disk
- bo   blocks written to disk
- us   user CPU
- sy   system CPU
- id   idle CPU
- wa   I/O wait

### Disk Monitoring with `iostat`

Run:

```bash id="ogb1kc"
iostat -xz 1
```

Example output:

```text id="met1f2"
avg-cpu:  %user %nice %system %iowait %steal %idle
           2.00  0.00    1.00    0.50   0.00 96.50

Device            r/s     w/s    rkB/s   wkB/s  await  aqu-sz  %util
sda              1.00    2.00    50.00  100.00   2.20    0.01   0.15
```

Interpretation:

- sda is barely used.
- %util is low.
- await is low.
- There is no disk bottleneck in this sample.

Important fields:

- r/s       reads per second
- w/s       writes per second
- rkB/s     kilobytes read per second
- wkB/s     kilobytes written per second
- await     average request wait time
- aqu-sz    average queue size
- %util     device utilization

### Network Sockets with `ss`

The older tool is `netstat`, but modern Linux systems usually prefer `ss`.

Show listening TCP and UDP ports:

```bash id="w8cjra"
ss -tulnp
```

Example output:

```text id="hq92qa"
Netid State  Local Address:Port  Peer Address:Port Process
tcp   LISTEN 0.0.0.0:22          0.0.0.0:*         users:(("sshd",pid=1234,fd=3))
tcp   LISTEN 0.0.0.0:80          0.0.0.0:*         users:(("nginx",pid=5678,fd=6))
```

Interpretation:

- SSH is listening on port 22.
- Nginx is listening on port 80.
- Both are listening on all IPv4 interfaces.

This is useful for checking which services are reachable over the network.

### Temperature and Fan Monitoring with `sensors`

Install sensors tools if needed:

```bash id="e7qi96"
sudo apt install lm-sensors
```

Detect available sensors:

```bash id="ex73ia"
sudo sensors-detect
```

Then run:

```bash id="k0d4x2"
sensors
```

Example output:

```text id="yn35ur"
coretemp-isa-0000
Package id 0:  +55.0°C  (high = +80.0°C, crit = +100.0°C)
Core 0:        +54.0°C  (high = +80.0°C, crit = +100.0°C)
Core 1:        +53.0°C  (high = +80.0°C, crit = +100.0°C)
```

Interpretation:

- CPU package temperature is 55°C.
- The high threshold is 80°C.
- The critical threshold is 100°C.
- The system is warm but not overheating.

High temperatures can cause throttling, instability, shutdowns, or long-term hardware damage.

### All-in-One Monitoring with `glances`

Run:

```bash id="uelawz"
glances
```

`glances` shows CPU, memory, disk, network, sensors, and processes in one interface.

It is useful when you want a quick overall view of system health.

### Interactive Monitoring with `nmon`

Run:

```bash id="gf17c6"
nmon
```

Common keys:

- c   CPU
- m   memory
- d   disk
- n   network
- t   top processes

`nmon` is useful for focused performance monitoring.

### Configuring Hardware

Linux includes tools for configuring different hardware types.

Examples include:

- hdparm     SATA/IDE disk parameters
- sdparm     SCSI/SATA device parameters
- xrandr     display settings on X11
- alsamixer  interactive sound mixer
- amixer     scriptable sound mixer
- ip         network interface configuration
- iwconfig   older wireless configuration tool
- rfkill     block or unblock wireless devices

### Disk Information with `hdparm`

Run:

```bash id="jzrlag"
sudo hdparm -I /dev/sda
```

Example output:

```text id="uf9o5h"
/dev/sda:

Model Number:       Samsung SSD 860 EVO 500GB
Serial Number:      S3Z9NB0K123456X
Firmware Revision:  RVT02B6Q
Transport:          Serial, ATA8-AST, SATA III
Logical Sector size:   512 bytes
Physical Sector size:  512 bytes
device size with M = 1000*1000: 500107 MBytes
```

Interpretation:

- The disk model and firmware are shown.
- The disk uses SATA.
- The reported capacity is about 500 GB.
- Sector size information can matter for alignment and performance.

Be careful with `hdparm` write-related options. Some options can affect data safety.

### SCSI Device Parameters with `sdparm`

Run:

```bash id="amri08"
sudo sdparm --all /dev/sdb
```

Example output:

```text id="o5yk6f"
Caching (SBC) mode page:
  WCE   Write Cache Enable: 1
  RCD   Read Cache Disable: 0
```

Interpretation:

- Write cache is enabled.
- Read cache is not disabled.

Storage cache settings can affect performance and data safety.

### Display Configuration with `xrandr`

On X11 systems, use:

```bash id="xdc0ym"
xrandr
```

Set a display mode:

```bash id="r1d5du"
xrandr --output HDMI-1 --mode 1920x1080 --rate 60 --primary
```

Example output:

```text id="zrsj8g"
HDMI-1 connected primary 1920x1080+0+0
1920x1080     60.00*+  59.94
1680x1050     59.88
```

Interpretation:

- HDMI-1 is connected.
- 1920x1080 at 60 Hz is active.
- The display is set as primary.

Note that Wayland-based desktop environments may use different tools or graphical settings panels.

### Sound with `alsamixer` and `amixer`

Interactive mixer:

```bash id="w5s8sf"
alsamixer
```

Useful keys:

- Arrow keys   adjust volume
- M            mute or unmute
- F6           select sound card
- Esc          exit

Scriptable commands:

```bash id="k8anzc"
amixer set Master unmute
amixer set Master 75%
```

Example output:

```text id="q9gjvs"
Simple mixer control 'Master',0
Front Left: Playback 49152 [75%] [on]
Front Right: Playback 49152 [75%] [on]
```

Interpretation:

- Master volume is set to 75%.
- Both left and right channels are unmuted.

### Network Interface Configuration with `ip`

Show network interfaces:

```bash id="odexff"
ip addr show
```

Bring an interface up:

```bash id="snxv89"
sudo ip link set eth0 up
```

Example output:

```text id="fv4zzh"
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 state DOWN
    link/ether 00:0a:95:9d:68:16
```

Interpretation:

- The interface is administratively UP.
- NO-CARRIER means no physical link is detected.
- For Ethernet, this may mean cable disconnected or switch port inactive.

### Wireless Devices with `rfkill`

Check wireless block status:

```bash id="lto0hf"
rfkill list
```

Example output:

```text id="myir1e"
0: phy0: Wireless LAN
    Soft blocked: no
    Hard blocked: no
1: hci0: Bluetooth
    Soft blocked: yes
    Hard blocked: no
```

Interpretation:

- Wi-Fi is not blocked.
- Bluetooth is blocked by software.
- There is no hardware block.

Unblock Bluetooth:

```bash id="sagysd"
rfkill unblock bluetooth
```

A hard block usually means a physical switch, BIOS setting, or firmware-level block.

### Drivers and Kernel Modules

Linux drivers are often kernel modules.

A module can be loaded, unloaded, inspected, or configured.

Useful commands include:

- lsmod
- modprobe
- modprobe -r
- modinfo
- insmod
- rmmod

### Listing Loaded Modules with `lsmod`

Run:

```bash id="axqwfg"
lsmod
```

Search for a module:

```bash id="xvnp7e"
lsmod | grep e1000e
```

Example output:

```text id="n6nrk9"
e1000e                245760  0
intel_cstate           20480  0
```

Interpretation:

- e1000e is loaded.
- It uses memory in the kernel.
- The final column shows how many other modules or devices are using it.

### Loading a Module with `modprobe`

Load a module:

```bash id="b2vs3e"
sudo modprobe e1000e
```

`modprobe` is preferred because it handles dependencies automatically.

### Removing a Module

Unload a module:

```bash id="oohcjd"
sudo modprobe -r e1000e
```

This may fail if the module is currently in use.

Example:

```text id="qcx99q"
modprobe: FATAL: Module e1000e is in use.
```

Interpretation:

- A device or another module is still using e1000e.
- You cannot safely remove it until it is no longer needed.

### Inspecting Module Information with `modinfo`

Run:

```bash id="jd6dxw"
modinfo e1000e
```

Example output:

```text id="gqrj4j"
filename:    /lib/modules/6.x/kernel/drivers/net/ethernet/intel/e1000e/e1000e.ko
version:     3.2.6-k
license:     GPL
description: Intel(R) PRO/1000 Network Driver
author:      Intel Corporation
```

Interpretation:

- This module is an Intel network driver.
- The file path shows where the module lives.
- The license and version are shown.

### Module Configuration

Module options can be configured under:

```text id="sdr0ts"
/etc/modprobe.d/
```

Example:

```bash id="hq7l7v"
echo "options e1000e InterruptThrottleRate=3000" | sudo tee /etc/modprobe.d/e1000e.conf
```

This applies an option when the module loads.

Configuration changes may require unloading and reloading the module or rebooting.

### Blacklisting a Module

If a module causes problems or conflicts with another driver, it can be blacklisted.

Example:

```bash id="a928kv"
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
```

This prevents the open-source NVIDIA `nouveau` driver from loading.

After changing early boot driver behavior, you may need:

```bash id="fgtuik"
sudo update-initramfs -u
sudo reboot
```

Blacklisting should be done carefully. If you blacklist the wrong driver, hardware may stop working.

### Graphics Drivers

Graphics drivers are important for desktop performance, external displays, GPU compute, and hardware acceleration.

Common GPU vendors include:

- Intel
- AMD
- NVIDIA

Intel and AMD usually work well with open-source drivers included in Linux distributions.

NVIDIA may use either the open-source `nouveau` driver or the proprietary NVIDIA driver.

### NVIDIA

On Ubuntu systems, you can inspect recommended drivers with:

```bash id="q2y29s"
ubuntu-drivers devices
```

Install a driver:

```bash id="yvduge"
sudo apt install nvidia-driver-470
```

Check status:

```bash id="t4wzgv"
nvidia-smi
```

Example output:

```text id="f9bgki"
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.57.02    Driver Version: 470.57.02    CUDA Version: 11.4     |
| GPU  Name            Temp    Memory-Usage        GPU-Util                   |
|  0   GeForce GTX1050  35C     200MiB / 4040MiB    2%                         |
+-----------------------------------------------------------------------------+
```

Interpretation:

- The NVIDIA driver is installed and working.
- The GPU is detected.
- Temperature, memory usage, and GPU utilization are visible.

### AMD

AMD GPUs often use the open-source `amdgpu` driver.

Check GPU:

```bash id="subbdw"
lspci | grep -E 'VGA|3D|Display'
```

Example output:

```text id="vqvnd5"
01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 10
```

Check driver:

```bash id="kmnpch"
lspci -k | grep -A3 -E 'VGA|3D|Display'
```

Example:

```text id="lekx5w"
Kernel driver in use: amdgpu
Kernel modules: amdgpu
```

Interpretation:

- The AMD GPU is using the amdgpu kernel driver.

### Hardware Troubleshooting Workflow

Hardware troubleshooting works best when done systematically.

A good order is:

1. Identify the hardware
2. Check whether the kernel detected it
3. Check which driver is in use
4. Check logs for errors
5. Check device permissions and configuration
6. Monitor resource usage
7. Test the hardware under controlled load
8. Update kernel, firmware, or drivers if needed
9. Compare with a live USB environment
10. Consider physical failure if problems persist

### Step 1: Identify the Hardware

Use:

```bash id="w34lcf"
lspci
lsusb
lsblk
lscpu
sudo lshw -short
```

This answers:

- What hardware does the system see?
- What model is it?
- What bus is it connected to?
- Is it storage, network, USB, graphics, or something else?

### Step 2: Check Kernel Detection

Use:

```bash id="co2nar"
dmesg -T | tail -100
```

Search for errors:

```bash id="d4zk39"
dmesg -T | grep -iE 'error|fail|warn|timeout|reset'
```

Example output:

```text id="vx9jwr"
[Mon Jun  1 10:20:01 2026] ata1.00: failed command: READ FPDMA QUEUED
[Mon Jun  1 10:20:01 2026] ata1.00: error: { UNC }
```

Interpretation:

- The disk reported an unreadable sector or read error.
- This may indicate disk damage or storage reliability problems.
- Back up important data immediately.

### Step 3: Verify Driver Loading

Use:

```bash id="vkguc3"
lspci -k
```

Look for:

- Kernel driver in use
- Kernel modules

If no driver is in use, the device may not function properly.

### Step 4: Check System Logs

Depending on the distribution, check:

```bash id="a76tgd"
sudo less /var/log/syslog
sudo less /var/log/kern.log
sudo journalctl -k
```

With systemd, kernel logs can be viewed using:

```bash id="avw9x6"
journalctl -k -b
```

Search for errors:

```bash id="jk5xnr"
journalctl -k -b | grep -iE 'error|fail|warn|timeout|reset'
```

### Step 5: Check Disk Health

Install SMART tools:

```bash id="a3msuw"
sudo apt install smartmontools
```

Check health:

```bash id="dxs2w0"
sudo smartctl -H /dev/sda
```

Example output:

```text id="taqdrj"
SMART overall-health self-assessment test result: PASSED
```

Interpretation:

- The disk reports that its overall SMART health check passed.
- This does not guarantee the disk is perfect, but it is a good sign.

Detailed check:

```bash id="a54gh7"
sudo smartctl -a /dev/sda
```

Warning signs include:

- Reallocated_Sector_Ct increasing
- Current_Pending_Sector greater than 0
- Offline_Uncorrectable greater than 0
- SMART overall-health FAILED
- many CRC errors

### Step 6: Test Memory

Memory problems can cause crashes, corrupted files, random application failures, and kernel panics.

Use Memtest86+ from boot media or the boot menu when available.

General interpretation:

- No errors after multiple passes is a good sign.
- Any memory error is serious.
- Faulty RAM should usually be replaced.

### Step 7: Stress Test CPU

Install:

```bash id="gwfwe3"
sudo apt install stress-ng
```

Run a CPU stress test:

```bash id="xh8kdc"
stress-ng --cpu 4 --timeout 60s
```

Example output:

```text id="ihn74e"
stress-ng: info: setting to a timeout of 60 seconds
stress-ng: info: dispatching hogs: 4 cpu
stress-ng: info: successful run completed in 60.00s
```

Interpretation:

- The CPU completed the stress test without crashing.
- If the system freezes, overheats, or powers off, investigate cooling, power, or hardware stability.

### Step 8: Check Physical Connections

Some hardware problems are physical.

Check:

- loose USB cable
- bad USB port
- loose SATA cable
- failing power supply
- unseated RAM
- unseated GPU
- dust buildup
- fan failure
- overheating

Safety rules:

- Power off before opening the computer.
- Unplug power before touching internal components.
- Use anti-static precautions.
- Do not open power supplies.
- Back up important data before hardware work.

### Scenario 1: Simulate a USB Hardware Event and Inspect It

Practice detecting a hardware change using `dmesg`, `lsusb`, `lsblk`, and `udevadm`.

#### Simulation

Plug in a USB flash drive.

In another terminal, watch udev events:

```bash id="p6e11i"
sudo udevadm monitor --environment --udev
```

Then plug in the USB device.

#### Check with `dmesg`

```bash id="oed2sm"
dmesg -T | tail -30
```

Example output:

```text id="ok5hk2"
[Mon Jun  1 10:15:01 2026] usb 1-1: new high-speed USB device number 3 using xhci_hcd
[Mon Jun  1 10:15:01 2026] usb 1-1: Product: Ultra USB 3.0
[Mon Jun  1 10:15:02 2026] sd 6:0:0:0: [sdb] 60062500 512-byte logical blocks
[Mon Jun  1 10:15:02 2026]  sdb: sdb1
```

#### Check with `lsusb`

```bash id="brtgp8"
lsusb
```

Example output:

```text id="l3ks65"
Bus 001 Device 003: ID 0781:5591 SanDisk Corp. Ultra USB 3.0
```

#### Check with `lsblk`

```bash id="v06tus"
lsblk
```

Example output:

```text id="s5t6qb"
NAME   SIZE TYPE MOUNTPOINTS
sda   238G disk
└─sda1 238G part /
sdb    29G disk
└─sdb1 29G part
```

Interpretation:

- dmesg shows the kernel detected the device.
- lsusb shows the USB identity.
- lsblk shows the storage device and partition.
- The USB drive appeared as /dev/sdb with partition /dev/sdb1.

If `lsusb` sees the device but `lsblk` does not, the USB device may not be a storage device, or the storage driver may not have attached properly.

### Scenario 2: Simulate a CPU Bottleneck

Create controlled CPU pressure and verify it with `top`, `htop`, and `vmstat`.

#### Simulate the Bottleneck

```bash id="tazxro"
stress-ng --cpu 4 --timeout 60s
```

This starts four CPU workers for 60 seconds.

#### Check with `top`

```bash id="g8mqre"
top
```

Example output:

```text id="jncw6p"
%Cpu(s): 95.0 us,  4.0 sy,  0.0 ni,  1.0 id,  0.0 wa

PID USER      PR  NI  S  %CPU COMMAND
4321 user      20   0  R 399.0 stress-ng-cpu
```

Interpretation:

- CPU user time is very high.
- Idle time is very low.
- stress-ng is consuming about four CPU cores.
- This is a CPU bottleneck, not a disk bottleneck.

#### Check with `vmstat`

```bash id="da3nz0"
vmstat 1
```

Example output:

```text id="ctge11"
r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
5  0      0 800000  20000 500000    0    0     0     1 3000 6000 95  4  1  0  0
```

Interpretation:

- r is high because processes are waiting for CPU.
- wa is 0, so the system is not waiting on disk.
- The bottleneck is CPU saturation.

### Scenario 3: Simulate Memory Pressure

Create memory pressure and observe it with `free`, `vmstat`, and `top`.

#### Simulate the Bottleneck

Use a conservative test first:

```bash id="m51fzk"
stress-ng --vm 2 --vm-bytes 70% --timeout 60s
```

This uses memory workers for 60 seconds.

#### Check with `free`

```bash id="ii01qm"
free -h
```

Example output:

```text id="enqw12"
               total        used        free      shared  buff/cache   available
Mem:            8.0G        6.7G        300M        100M        1.0G        900M
Swap:           2.0G        300M        1.7G
```

Interpretation:

- Most RAM is used.
- Available memory is low.
- Swap is being used.
- The system may become slower if swapping increases.

#### Check with `vmstat`

```bash id="egcc12"
vmstat 1
```

Example output:

```text id="qs1jhr"
r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
2  1 400000 100000  20000 200000  500  800  2000 4000 2000 5000 40 10 35 15  0
```

Interpretation:

- si and so are nonzero, so the system is swapping.
- wa is elevated because swap uses disk.
- The root problem is memory pressure, even though disk I/O is also visible.

### Scenario 4: Simulate Disk I/O Pressure

Create disk activity and verify it with `iostat` and `iotop`.

#### Simulate the Bottleneck

Install tools if needed:

```bash id="x0ojyk"
sudo apt install fio sysstat iotop
```

Run a safe file-based write test:

```bash id="e2kc4h"
mkdir -p ~/hardware-lab

fio --name=write-test \
    --directory=~/hardware-lab \
    --size=1G \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --runtime=60 \
    --time_based
```

#### Check with `iostat`

```bash id="jc9b0d"
iostat -xz 1
```

Example output:

```text id="yfbkdr"
Device            r/s     w/s     rkB/s     wkB/s   await  aqu-sz  %util
sda              0.00  350.00      0.00  350000.0   32.50   10.20  99.60
```

Interpretation:

- w/s and wkB/s are high.
- await is elevated.
- aqu-sz shows queueing.
- %util is near 100%.
- The disk is saturated by writes.

#### Check with `iotop`

```bash id="f27w8v"
sudo iotop -o
```

Example output:

```text id="n01dka"
Total DISK WRITE: 340.00 M/s
TID  PRIO USER DISK READ DISK WRITE IO> COMMAND
5221 be/4 user 0.00 B/s  338.00 M/s 92% fio --name=write-test
```

Interpretation:

- fio is the process generating disk pressure.
- The bottleneck is caused by heavy disk writes.

### Scenario 5: Simulate a Network Interface State Change Safely

Practice interface inspection without disabling your real network connection.

Instead of bringing down a real interface, create a dummy interface.

#### Create a Dummy Interface

```bash id="kmjjdc"
sudo modprobe dummy
sudo ip link add dummy0 type dummy
sudo ip link set dummy0 up
```

#### Check with `ip`

```bash id="lvxtb3"
ip link show dummy0
```

Example output:

```text id="lhhr6v"
10: dummy0: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 state UNKNOWN mode DEFAULT
    link/ether 9a:42:cc:10:22:33 brd ff:ff:ff:ff:ff:ff
```

Interpretation:

- dummy0 exists.
- It is administratively UP.
- It is a virtual interface, so state may show UNKNOWN.

#### Bring It Down

```bash id="iwxdgc"
sudo ip link set dummy0 down
```

Check again:

```bash id="rvuo8o"
ip link show dummy0
```

Example output:

```text id="ozwz2l"
10: dummy0: <BROADCAST,NOARP> mtu 1500 state DOWN mode DEFAULT
```

Interpretation:

- The interface is now down.
- This simulates an interface state change safely.

#### Clean Up

```bash id="mt9qfo"
sudo ip link delete dummy0
```

### Scenario 6: Simulate a Missing or Blocked Wireless Device

Understand `rfkill` output and wireless blocking.

#### Check Current State

```bash id="utlwrc"
rfkill list
```

Example output:

```text id="lh1qgo"
0: phy0: Wireless LAN
    Soft blocked: no
    Hard blocked: no
1: hci0: Bluetooth
    Soft blocked: yes
    Hard blocked: no
```

Interpretation:

- Wi-Fi is usable.
- Bluetooth is blocked by software.
- Bluetooth can be unblocked with rfkill.

#### Unblock Bluetooth

```bash id="p2hf3m"
rfkill unblock bluetooth
```

Check again:

```bash id="jpqzmr"
rfkill list
```

Example output:

```text id="jitqf4"
1: hci0: Bluetooth
    Soft blocked: no
    Hard blocked: no
```

Interpretation:

- The Bluetooth software block was removed.
- If hard blocked were yes, software could not fix it.

### Scenario 7: Simulate Overheating Risk Under CPU Load

Observe how CPU load affects temperature.

#### Start Temperature Monitoring

In one terminal:

```bash id="onrlkz"
watch -n 1 sensors
```

Example idle output:

```text id="w0lsko"
Package id 0:  +45.0°C  (high = +80.0°C, crit = +100.0°C)
Core 0:        +44.0°C
Core 1:        +43.0°C
```

#### Apply CPU Load

In another terminal:

```bash id="owro40"
stress-ng --cpu 4 --timeout 60s
```

Example loaded output:

```text id="b2dfv6"
Package id 0:  +78.0°C  (high = +80.0°C, crit = +100.0°C)
Core 0:        +79.0°C
Core 1:        +77.0°C
```

Interpretation:

- Temperature rose under CPU load.
- The package is close to the high threshold.
- If temperature reaches critical levels or the system throttles, check cooling.

Possible fixes:

- clean dust
- check fans
- improve airflow
- replace thermal paste
- reduce overclocking
- check laptop power profile

### Scenario 8: Simulate a Driver Investigation

Identify which driver is handling a device.

#### Choose a Device

Run:

```bash id="u2akgo"
lspci
```

Example:

```text id="qtfojs"
00:1f.6 Ethernet controller: Intel Corporation Ethernet Connection I219-LM
```

#### Check Driver

```bash id="saxgy9"
lspci -k -s 00:1f.6
```

Example output:

```text id="h6emxn"
00:1f.6 Ethernet controller: Intel Corporation Ethernet Connection I219-LM
        Kernel driver in use: e1000e
        Kernel modules: e1000e
```

#### Inspect Module

```bash id="s8nr33"
modinfo e1000e | head
```

Example output:

```text id="dixduo"
filename:    /lib/modules/6.x/kernel/drivers/net/ethernet/intel/e1000e/e1000e.ko
description: Intel(R) PRO/1000 Network Driver
license:     GPL
```

Interpretation:

- The Ethernet controller is using the e1000e driver.
- The module exists on disk.
- The driver appears to be correctly loaded.

If no kernel driver is in use, investigate missing firmware, unsupported hardware, or kernel version issues.

### Scenario 9: Simulate a Log-Based Hardware Investigation

Use logs to identify hardware-like errors.

#### Search Kernel Logs

```bash id="l9s1px"
journalctl -k -b | grep -iE 'error|fail|warn|timeout|reset'
```

Example output:

```text id="m9jfsd"
Jun 01 10:20:01 host kernel: usb 1-1: USB disconnect, device number 2
Jun 01 10:20:05 host kernel: ata1.00: failed command: READ FPDMA QUEUED
Jun 01 10:20:05 host kernel: ata1.00: error: { UNC }
```

Interpretation:

- The USB disconnect may indicate a removed device or flaky USB connection.
- The ATA read failure is more serious and may indicate disk problems.
- The next step is to check disk health with smartctl.

#### Follow Up with SMART

```bash id="cr5qi0"
sudo smartctl -a /dev/sda
```

Look for:

- Reallocated_Sector_Ct
- Current_Pending_Sector
- Offline_Uncorrectable
- UDMA_CRC_Error_Count

Interpretation:

- Sector-related errors may indicate failing media.
- CRC errors may indicate cable or connection problems.
- Back up important data before deeper testing.

### Common Hardware Problems and Fixes

#### Device Not Detected

Check:

```bash id="ab99pc"
lsusb
lspci
dmesg -T | tail -50
journalctl -k -b
```

Possible causes:

- bad cable
- bad port
- missing driver
- missing firmware
- hardware disabled in BIOS
- device failure
- unsupported hardware

### Device Detected but Not Working

Check:

```bash id="qwko97"
lspci -k
lsmod
modinfo modulename
dmesg -T | grep -i firmware
```

Possible causes:

- wrong driver
- driver conflict
- missing firmware
- permissions issue
- device blocked by rfkill
- service not running

### Disk Errors

Check:

```bash id="j63w9m"
dmesg -T | grep -iE 'ata|nvme|I/O error|reset|timeout'
sudo smartctl -a /dev/sda
```

Possible fixes:

- back up immediately
- replace failing disk
- check cables
- check power
- update firmware if appropriate
- restore from backup if data is corrupted

### Overheating

Check:

```bash id="xb13ak"
sensors
watch -n 1 sensors
```

Symptoms:

- fans loud
- system slows down
- sudden shutdowns
- CPU frequency drops
- high temperature readings

Possible fixes:

- clean dust
- improve airflow
- check fans
- replace thermal paste
- reduce load
- repair cooling system

### Network Hardware Problems

Check:

```bash id="y8ky5b"
ip link
lspci -k | grep -A3 -i ethernet
dmesg -T | grep -iE 'firmware|link|eth|wlan|wifi'
rfkill list
```

Possible causes:

- cable disconnected
- Wi-Fi blocked
- missing firmware
- wrong driver
- bad switch port
- interface administratively down

### Audio Problems

Check:

```bash id="y5gpqn"
alsamixer
amixer
aplay -l
```

Common causes:

- muted channel
- wrong output device
- low volume
- missing driver
- PulseAudio or PipeWire issue

### Display Problems

Check:

```bash id="enyewt"
xrandr
lspci -k | grep -A3 -E 'VGA|3D|Display'
journalctl -k -b | grep -iE 'drm|nvidia|amdgpu|i915'
```

Common causes:

- wrong display mode
- driver issue
- unsupported refresh rate
- GPU driver conflict
- bad cable or adapter

### Safe Hardware Troubleshooting Rules

- Back up important data before risky troubleshooting.
- Do not run destructive disk commands on unknown devices.
- Do not remove kernel modules used by active hardware unless you understand the risk.
- Be careful restarting networking over SSH.
- Power off before touching internal components.
- Use anti-static precautions.
- Check logs before guessing.
- Change one thing at a time.
- Record what you changed.

### Useful Command Summary

Hardware inventory:

```bash id="rdq19k"
lspci
lspci -k
lsusb
lscpu
lsblk
lsblk -f
sudo lshw -short
```

Kernel and device events:

```bash id="elfe7o"
dmesg -T | tail -50
journalctl -k -b
sudo udevadm monitor --environment --udev
```

Monitoring:

```bash id="tug0tl"
top
htop
vmstat 1
iostat -xz 1
ss -tulnp
sensors
glances
nmon
```

Drivers:

```bash id="nq6ifp"
lsmod
modinfo modulename
sudo modprobe modulename
sudo modprobe -r modulename
```

Storage health:

```bash id="jxo2ef"
sudo smartctl -H /dev/sda
sudo smartctl -a /dev/sda
```

Network and wireless:

```bash id="xu1nqb"
ip addr show
ip link show
rfkill list
```

Audio and display:

```bash id="sizlnd"
alsamixer
amixer
xrandr
```

### Challenges

1. Use `lspci`, `lsusb`, and `lsblk` to identify hardware connected to your system. For each device, write what it appears to be and what role it serves.
2. Use `lscpu` to identify your CPU architecture, number of logical CPUs, cores per socket, and threads per core.
3. Use `lspci -k` to choose a PCI device and identify the kernel driver currently handling it.
4. Plug in a USB device, then use `dmesg`, `lsusb`, `lsblk`, and `udevadm monitor` to observe the detection process.
5. Use `ls -l /dev/null /dev/zero /dev/sda` to compare character and block devices.
6. Use `top` or `htop` to identify the most CPU-intensive process on your system.
7. Use `free -h` and `vmstat 1` to inspect memory usage, available memory, and swap activity.
8. Use `sensors` to check CPU temperature. Then run a short CPU stress test and observe how temperature changes.
9. Use `smartctl` to check disk health, if SMART is supported by your storage device.
10. Create a dummy network interface, bring it up and down, inspect it with `ip link`, and then delete it.
