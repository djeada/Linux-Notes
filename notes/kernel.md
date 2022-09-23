## What is kernel?
Operating systems have kernels that manage the CPU hardware, allocate memory, access data and schedule processes. 
They also execute programs and protect them from each other. As soon as a computer starts up, it is the first software to run. 
In order to prevent the kernel's most essential code from being rewritten by other programs running in the operating system, it is loaded into protected memory regions. The kernel's functionality can be expanded by adding modules to it. As a result, by activating or removing modules, a user may fine-tune their kernel settings. This amount of granular control is one of the many reasons why Linux is so popular.

## Kernel Architecture
A kernel might be monolithic, microkernel, or hybrid in nature (like the OS X and Windows 11). The Linux kernel is a single monolithic computer operating system kernel that is similar to the UNIX system.  Unlike the microkernel, the monolithic kernel includes not only the Central Processing Unit, memory, and IPC, but also device drivers, system server calls, and file system administration. This Linux kernel is shared between Linux Distributions.

## Differences from other UNIX kernels

* Kernel modules can be loaded dynamically in Linux.
* Linux includes an object-oriented device model that includes device classes, hot-pluggable events, and a user-space device file-system.
* Linux supports symmetrical multiprocessors.
* Linux is both open source and free.
* Some basic Unix features are ignored by Linux because they are deemed "poorly conceived" by kernel engineers.
* Preemption is built into the Linux kernel.
* The Linux kernel does not distinguish between threads and regular processes.

## Components of Linux kernel

* A system call interface (SCI) is a thin overlay that allows function calls from user space into the kernel. This interface may be architecture-specific.
* Process management is primarily responsible for the execution of procedures. These are known as threads in a kernel and represent an individual virtualization of the specific processor.
* Memory management; for efficiency, memory is handled in what are known as pages. Linux contains techniques for managing available memory as well as hardware capabilities for physical and virtual mappings. There is also swap space available.
* Virtual file system provides a standard interface abstraction for file systems. It acts as a bridge between the system call interface and the file systems provided by the kernel.
* The network stack is built as a tiered architecture based on the protocols.
* Device drivers make a specific hardware device operational, make up a substantial portion of the source code in the Linux kernel. Tutorial on Device Drivers
* Architecture-dependent code; those parts that rely on the architecture on which they operate and, as a result, must take the architectural design into account for proper functioning and efficiency.

## Monitoring kernel

* <i>dmesg</i> (alternatively <i>journalctl --dmesg</i>) allows to see kernel ring buffer. The kernel ring buffer holds information such as device driver initialization messages, hardware messages, and kernel module messages.
* The /proc/ directory, commonly known as the <i>/proc filesystem</i>, includes a hierarchical set of special files that reflect the current state of the kernel, allowing programs and users to see what the kernel sees.
* <i>uname</i>  provides users with important system information.

| Flag | Description |
| --- | --- |
| <i>-s</i> | kernel name |
| <i>-r</i> | kernel release |
| <i>-v</i> | kernel version |
| <i>-m</i> | machine architecture |
| <i>-p</i> | processor architecture |

## Startup process
The boot procedures (BIOS or UEFI, MBR, and GRUB) complete system startup by loading the kernel into memory and connecting it to the initial ramdisk (initrd or initramfs), after which systemd is launched.

The startup procedures then take up the baton and complete the operating system's setup. 

1. The kernel probes accessible hardware at boot.
2. When a hardware component is detected, the systemd-udevd process loads the appropriate driver and makes the hardware device available.
3. systemd-udevd examines the rules files in /usr/lib/udev/rules.d to determine how the deives are initialized. These are the udev rules files given by the system and should not be changed.
4. After processing the system-supplied udev rules files, systemd-udevd searches the /etc/udev/rules.d directory for any custom rules that may be present.
5. As a consequence, the appropriate kernel modules are automatically loaded, and information about the kernel modules and associated hardware is written to the sysfs file system, which is mounted in the /sys directory.

## Working with kernel modules

* <i>lsmod</i> shows all currently used modules.
* <i>modinfo module_name</i> displays info about a specific kernel module.
* <i>modprobe module_name</i> loads specified module (-r flag is used to unload a module).

## DKMS

Let us imagine a following scenario: you just bought some hardware part for your PC like graphics card or WIFI adapter and after plugining it in you find out that it is not recognised by your system. You have to now look for a drivers for that hardware. 

* One option is to download the official source code of the device driver, compile it against the kernel and the install and activated it. 
* If you are lucky everything will work fine till the next kernel update. You will then have to manually repeat the process.
* Another option is to use DKMS (dynamic kernel module support). It will automatically re-build kernel modules on kernel upgrade.
* Additionally it is good to notice that many hardware vendors already distribute their hardware's device driver as a DKMS packages.

### Installation

On Debian based systems:

sudo apt install dkms

On Arch based systems:

