## What is a kernel?

A kernel is the central component of an operating system that manages the hardware and software resources of a computer. It is responsible for controlling the CPU, allocating memory, accessing data, and scheduling processes. The kernel is the first software to run when a computer starts up and is loaded into protected memory to prevent it from being rewritten by other programs. The functionality of the kernel can be extended by adding modules to it, allowing users to fine-tune their kernel settings.

## Kernel architecture

There are several types of kernel architectures, including monolithic, microkernel, and hybrid. The Linux kernel is a monolithic kernel, similar to the UNIX system. Monolithic kernels include not only the CPU, memory, and interprocess communication (IPC) functions, but also device drivers, system server calls, and file system management. The Linux kernel is shared between different Linux distributions.
Differences from other UNIX kernels

* Linux allows kernel modules to be loaded dynamically.
* Linux has an object-oriented device model that includes device classes, hot-pluggable events, and a user-space device file system.
* Linux supports symmetrical multiprocessing.
* Linux is both open-source and free.
* Linux does not include certain basic Unix features that are deemed "poorly conceived" by kernel engineers.
* Linux has built-in preemption.
* Linux does not distinguish between threads and regular processes.

## Components of the Linux kernel

* A system call interface (SCI) is an overlay that enables function calls from user space into the kernel. This interface may be specific to the architecture.
* Process management is responsible for the execution of processes, also known as threads in the kernel, which represent individual virtualizations of the processor.
* Memory management involves techniques for managing available memory, as well as hardware capabilities for physical and virtual mappings. Linux also includes swap space.
* The virtual file system provides a standard interface abstraction for file systems, serving as a bridge between the system call interface and the file systems provided by the kernel.
* The network stack is a tiered architecture based on protocols.
* Device drivers make specific hardware devices operational and make up a significant portion of the Linux kernel's source code.
* Architecture-dependent code is dependent on the architecture on which it operates and must take the architectural design into account for proper functioning and efficiency.


## Monitoring the kernel

* The dmesg command (alternatively `journalctl --dmesg`) allows users to view the kernel ring buffer. The kernel ring buffer holds information such as device driver initialization messages, hardware messages, and kernel module messages.
* The `/proc` directory, also known as the `/proc` filesystem, contains a hierarchical set of special files that reflect the current state of the kernel, allowing users and programs to see what the kernel sees.
* The `uname` command provides users with important system information. The following flags can be used with uname:

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
The boot procedures (BIOS or UEFI, MBR, and GRUB) complete system startup by loading the kernel into memory and connecting it to the initial ramdisk (initrd or initramfs), after which systemd is launched.

After the kernel is loaded into memory and connected to the initial ramdisk (initrd or initramfs), the startup process continues with the launch of systemd.

1. Systemd initializes the system and loads system services.
1. Systemd activates all enabled target units. Target units are high-level units that group together related services and are used to boot the system into a particular state.
1. Systemd starts the default target unit, which is typically the graphical user interface (GUI) for desktop environments or a command-line interface for servers.

The startup process can be customized by modifying the target units and system services that are activated during boot. This can be done through the use of systemd configuration files, which are written in a declarative language and control the behavior of systemd and the services it manages.

## Kernel modules
Kernel modules are pieces of code that can be loaded and unloaded into the kernel at runtime, without the need to recompile the kernel. They provide additional functionality to the kernel and are used to support a wide range of hardware and software devices.

To work with kernel modules, you can use the following commands:

* `lsmod`: This command lists all currently loaded kernel modules.
* `modprobe`: This command loads a kernel module into the kernel.
* `rmmod`: This command unloads a kernel module from the kernel.
* `depmod`: This command generates a list of dependencies for all installed kernel modules.
* `dkms`: This command is used to manage DKMS-controlled kernel modules. It can be used to install, remove, and build kernel modules.

## DKMS

The Dynamic Kernel Module Support (DKMS) is a system that allows kernel modules to be automatically rebuilt when a new kernel is installed. This is useful because it allows kernel modules to be used across different kernels without the need to manually rebuild them each time a new kernel is installed.

To use DKMS, you need to have the dkms package installed on your system. 

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
