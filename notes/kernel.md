## What is a kernel?

A kernel is the main piece of a computer's system that handles the computer's parts and programs. It takes care of the computer's brain, sets aside memory, gets information, and organizes tasks. The kernel is the first thing to work when a computer turns on and is kept safe so other things can't mess with it. You can put extra pieces into the kernel to change how it works.

## Kernel architecture

There are different ways to build a kernel, like monolithic, microkernel, and hybrid. The Linux kernel is a monolithic one, similar to the UNIX system. Monolithic kernels have parts for the computer's brain, memory, and talking between tasks. They also handle things like devices, system requests, and file organization. The Linux kernel is used in different versions of Linux.

### Differences from other UNIX kernels

* Linux allows kernel modules to be loaded dynamically.
* Linux has an object-oriented device model that includes device classes, hot-pluggable events, and a user-space device file system.
* Linux supports symmetrical multiprocessing.
* Linux is both open-source and free.
* Linux does not include certain basic Unix features that are deemed "poorly conceived" by kernel engineers.
* Linux has built-in preemption.
* Linux does not distinguish between threads and regular processes.

## Components of the Linux kernel

* System call interface (SCI): An overlay that enables function calls from user space into the kernel.
* Process management: Manages the execution of processes or threads in the kernel, which represent individual virtualizations of the processor.
* Memory management: Manages available memory, physical and virtual mappings, and swap space.
* Virtual file system: Provides a standard interface abstraction for file systems.
* Network stack: A tiered architecture based on protocols.
* Device drivers: Make specific hardware devices operational.
* Architecture-dependent code: Code that depends on the architecture it operates on.

## Monitoring the kernel

* Use `dmesg` or `journalctl --dmesg` to view the kernel ring buffer.
* The `/proc` directory contains special files that reflect the current state of the kernel.
* Use the `uname` command to get important system information, like kernel version.

The following flags can be used with `uname`:

| Flag | Description |
| ---- | ----------- |
| `-s` | kernel name |
| `-r` | kernel release |
| `-v` | kernel version |
| `-m` | machine architecture |
| `-p` | processor architecture |

For example to check the current kernel version, use the following command:

```
uname -a
```
## Startup process

1. BIOS or UEFI, MBR, and GRUB complete system startup by loading the kernel into memory and connecting it to the initial ramdisk (initrd or initramfs).
1. Systemd initializes the system and loads system services.
1. Systemd activates all enabled target units, which are high-level units that group together related services.
1. Systemd starts the default target unit, typically a GUI for desktop environments or a command-line interface for servers.

## Kernel modules
Kernel modules are small chunks of code that you can insert or take out from the kernel while the computer is running, without having to modify the core kernel code. These modules extend the kernel's capabilities, allowing it to communicate with a wide variety of hardware and software devices more effectively.

To interact with kernel modules and manage them, you can use a set of specific commands designed for this purpose:

* `lsmod`: This command lists all currently loaded kernel modules.
* `modprobe`: This command loads a kernel module into the kernel.
* `rmmod`: This command unloads a kernel module from the kernel.
* `depmod`: This command generates a list of dependencies for all installed kernel modules.
* `dkms`: This command is used to manage DKMS-controlled kernel modules. It can be used to install, remove, and build kernel modules.

## DKMS
The Dynamic Kernel Module Support (DKMS) is a way to help kernel modules work with new kernels when they are added to the computer. This is helpful because you don't need to build the modules again every time you get a new kernel.

To use DKMS, you need to have the dkms package on your computer.

On Debian based systems:

```
sudo apt install dkms
```

On Arch based systems:

```
sudo pacman -S dkms
```

You can then use the dkms command to manage kernel modules that are controlled by DKMS. For example, to install a kernel module using DKMS, you can use the following command:

```
dkms install <module_name>
```

To remove a kernel module using DKMS, you can use the following command:

```
dkms remove <module_name> --all
```

To build a kernel module using DKMS, you can use the following command:

```
dkms build <module_name>
```

By working with kernel modules and DKMS, you can easily manage the additional functionality provided by kernel modules and ensure that they are properly rebuilt when a new kernel is installed.

## Challenges

1. What is the primary function of the kernel in an operating system?
1. How is the Linux kernel different from microkernel and hybrid kernels?
1. What is a kernel module and how is it used in the Linux kernel?
1. What is the purpose of DKMS and how is it used to manage kernel modules in Linux?
1. How does the startup process work in a Linux system, and what role does systemd play in this process?
1. What is the `/proc` filesystem and how is it used to monitor the kernel?
1. How can you check the current kernel version on a Linux system?
1. What is the difference between a thread and a regular process in the Linux kernel?
1. How can you load and unload a kernel module in Linux using the `modprobe` and `rmmod` commands, respectively?
1. How can you build a kernel module using DKMS?
