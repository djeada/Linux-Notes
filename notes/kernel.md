## Linux Kernel

We will now delve deeply into the Linux kernel to understand its role in the operating system, where it resides on your system, and how kernel modules function. We will also explore how to download and examine the Linux kernel source code, and discuss the various configuration options available within it. The goal is to provide you with a comprehensive understanding of this critical component of the operating system—not necessarily to enable you to compile your own custom kernel, but to appreciate what the kernel does and how it operates.

TODO:
- compare various kernel versions

### What is the Linux Kernel?

The **Linux kernel** is the core component of the Linux operating system. According to [Wikipedia](https://en.wikipedia.org/wiki/Linux_kernel):

> *The Linux kernel is a computer program that manages input/output requests from software and translates them into data processing instructions for the CPU and other electronic components of a computer.*

In simpler terms, the kernel acts as a bridge between software applications and the hardware of a computer. It handles critical tasks such as:

- Allocating and deallocating memory spaces.
- Scheduling processes and threads.
- Facilitating communication between hardware and software.
- Providing an interface for user applications to interact with the system securely.

### The Role of the Kernel in the System

Think of the kernel as the **director** or **manager** of all system operations at the lowest level. It is responsible for:

- Directly interacting with the CPU, memory, and peripheral devices.
- Allocating system resources such as CPU time, memory space, and input/output bandwidth.
- Providing a uniform interface for software applications to interact with various hardware components without needing to know the hardware details.

Without the kernel, applications would have to manage hardware interactions themselves, leading to complexity and potential instability.

### Understanding Kernel Space and User Space

In operating systems like Linux, the concepts of **kernel space** and **user space** are fundamental. They represent two separate areas of memory used for different purposes, ensuring the system's stability and security by controlling how processes interact with hardware and core system functions.

```
+--------------------------------------------------+
|                   User Space                     |
|                                                  |
|  +--------------------------------------------+  |
|  |            User Applications               |  |
|  |                                            |  |
|  |  +---------+   +---------+   +---------+   |  |
|  |  |  App 1  |   |  App 2  |   |  App 3  |   |  |
|  |  +---------+   +---------+   +---------+   |  |
|  |                                            |  |
|  +--------------------------------------------+  |
|                                                  |
+--------------------------------------------------+
|                   Kernel Space                   |
|                                                  |
|  +--------------------------------------------+  |
|  |           Operating System Kernel          |  |
|  |                                            |  |
|  |  +---------+  +----------+  +-----------+  |  |
|  |  | Memory  |  | Scheduler |  |  Drivers |  |  |
|  |  | Manager |  |          |  |           |  |  |
|  |  +---------+  +----------+  +-----------+  |  |
|  |                                            |  |
|  +--------------------------------------------+  |
|                                                  |
+--------------------------------------------------+
|                  Hardware Layer                  |
|                                                  |
|  +--------------------------------------------+  |
|  |                Physical Hardware           |  |
|  +--------------------------------------------+  |
|                                                  |
+--------------------------------------------------+
```

- In a computer system, the **user space** is a designated area where user applications operate, providing a level of isolation from critical system components.
- Applications in user space are assigned their own **memory space**, which enhances security by preventing interference between individual applications.
- The **kernel space** is reserved for the operating system kernel, which has direct access to system resources and hardware, enabling it to manage tasks like memory allocation, process scheduling, and hardware communication.
- Operating in kernel space requires **higher privileges**, which ensures that only trusted components have control over fundamental system functions.
- At the base of the system lies the **hardware layer**, comprising physical components like the CPU, memory, and various peripheral devices, which together form the foundation of the computing environment.
- The hardware layer interfaces with the kernel through **drivers**, which are software modules that translate hardware functionality into commands the kernel can understand.
- Between user space and kernel space, there exists a **system call interface** that allows applications to request services from the kernel, such as file access or network communication.
- **Security measures** are implemented to maintain separation between user space and kernel space, preventing malicious software from gaining unauthorized kernel access.
- The **memory management unit** (MMU) plays a crucial role in maintaining this separation by translating virtual memory addresses used by applications into physical addresses on the hardware.
- Applications running in user space cannot directly access hardware components; they must rely on **API calls** to communicate with the kernel, which then interacts with the hardware on their behalf.
- The **virtual memory** system enables applications to perceive a consistent memory structure, regardless of the actual physical memory arrangement, thereby simplifying programming and enhancing efficiency.
- **Interrupt handling** is a vital function within the kernel, allowing it to respond promptly to hardware events, such as input from peripherals or errors in processing.
- Kernel space is commonly divided into **modules** that handle specific functions like device management, networking, and filesystem operations, allowing for a modular and adaptable system architecture.
- **User privileges** in user space are limited compared to those in kernel space, ensuring that applications cannot perform actions that could compromise system stability or security.
- The **protection ring model** is often employed, with user space operating in a lower-privileged ring, while kernel space functions within a more privileged ring, reducing the risk of accidental or malicious interference.

#### Detailed Memory Layout

```
+------------------------+ 0xFFFFFFFF (Highest Address)
|      Kernel Space      |
|  (Shared among all     |
|   processes)           |
+------------------------+ 0xC0000000 (On 32-bit systems)
|                        |
|                        |
|                        |
|      User Space        |
|  (Per-process virtual  |
|   memory space)        |
|                        |
|                        |
+------------------------+ 0x00000000 (Lowest Address)
```

**User Space Memory**:

- Each process has its own user space memory.
- Cannot access other processes' memory or kernel memory.

**Kernel Space Memory**:

- Shared among all processes.
- Only accessible when the processor is in kernel mode.

#### Visualization of System Call

```
User Space:
+-----------------+
|  User App       |
|  Calls read()   |
+--------+--------+
   |
   v
Kernel Space:
+-----------------+
|  System Call    |
|  Handler        |
+--------+--------+
   |
   v
+-----------------+
|  Filesystem     |
|  Driver         |
+--------+--------+
   |
   v
Hardware Layer:
+-----------------+
|  Disk Hardware  |
+-----------------+
```

### Locating the Kernel on Your System

The kernel and its related files reside in the `/boot` directory on a Linux system. This directory contains essential components needed during the boot process.

To view the contents of the `/boot` directory, open a terminal and run:

```bash
ls /boot
```

You may see output similar to:

```
config-5.4.0-42-generic
initrd.img-5.4.0-42-generic
vmlinuz-5.4.0-42-generic
System.map-5.4.0-42-generic
```

- `vmlinuz-5.4.0-42-generic` is the compressed Linux kernel executable.
- `initrd.img` is initial RAM disk image used during boot.
- `config-` and `System.map-` are configuration and symbol map files for the kernel.

#### Understanding Multiple Kernels

It's common to have multiple kernels installed on your system. This provides flexibility and safety:

- If a new kernel update causes issues, you can boot into an older, stable kernel.
- Developers may need to test software against different kernel versions.
- Some hardware may require specific kernel versions.

Listing available kernels:

```bash
ls /boot/vmlinuz*
```

Example output:

```
/boot/vmlinuz-5.4.0-40-generic
/boot/vmlinuz-5.4.0-42-generic
```

#### Selecting a Kernel at Boot Time

The bootloader, typically **GRUB2** (GRand Unified Bootloader version 2) in modern Linux distributions, allows you to select which kernel to boot.

**To select a kernel at boot time:**

1. Restart your computer.
2. Hold down the `Shift` key (for BIOS systems) or press `Esc` repeatedly (for UEFI systems) during startup to access the GRUB menu.
3. Navigate the GRUB menu using arrow keys to select `Advanced options for Ubuntu` or similar.
4. Choose the desired kernel from the list of installed kernels.

**Note:** Modifying GRUB configurations can be complex and may affect system boot. Always proceed with caution.

### Kernel Modules

Kernel modules are pieces of code that can be loaded and unloaded into the kernel at runtime. They extend the functionality of the kernel without the need to reboot the system.

**Examples of kernel modules include:**

- **Device drivers** facilitate communication between the operating system and various hardware components, enabling devices like network cards, USB peripherals, and graphics cards to function correctly within the system.
- To ensure compatibility across diverse storage formats, **file system drivers** provide support for various file systems, including NTFS, FAT, and ext4, allowing the operating system to read and write data to different types of storage media.
- **System calls** offer a structured way for applications to request specific functionalities from the operating system, such as file manipulation, memory allocation, and network communication, enhancing the interaction between user applications and the kernel.

#### Viewing Loaded Modules

To see which modules are currently loaded into the kernel, use the `lsmod` command:

```bash
lsmod
```

The output will list modules with their sizes and usage counts:

```
Module                  Size  Used by
snd_hda_codec_realtek   94208  1
snd_hda_codec_generic   77824  1 snd_hda_codec_realtek
uvcvideo               102400  0
videobuf2_vmalloc      16384  1 uvcvideo
```

#### The `/lib/modules` Directory

Kernel modules are stored in the `/lib/modules/<kernel-version>` directory. Each kernel version has its own set of modules.

To list modules for a specific kernel:

```bash
ls /lib/modules/$(uname -r)
```

This directory contains subdirectories and files that represent various modules and their dependencies.

### Exploring the Kernel Source Code

The official source code for the Linux kernel is available at [kernel.org](https://www.kernel.org/).

**To download the kernel source code:**

1. **Visit [kernel.org](https://www.kernel.org/)**
2. **Identify the Latest Stable Kernel**: Look for the latest stable release, e.g., `5.8.12`.
3. **Download the Source Archive**: Click on the `.tar.xz` link to download the compressed source code.

Alternatively, from the terminal:

```bash
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.8.12.tar.xz
```

#### Extracting the Source Code

After downloading, extract the source code using the `tar` command:

```bash
tar -xf linux-5.8.12.tar.xz
```

This will create a directory named `linux-5.8.12`.

#### Navigating the Source Tree

Change into the source directory:

```bash
cd linux-5.8.12
```

List the contents:

```bash
ls
```

Key directories include:

| Directory       | Description                            |
|-----------------|----------------------------------------|
| `arch/`         | Architecture-specific code.            |
| `drivers/`      | Device driver source code.             |
| `fs/`           | File system implementations.           |
| `include/`      | Header files.                          |
| `kernel/`       | Core kernel code.                      |
| `net/`          | Networking stack code.                 |
| `Documentation/`| Documentation for various kernel components. |

#### Examining Drivers and Modules

**Example: Exploring Network Drivers**

Navigate to the network drivers directory:

```bash
cd drivers/net
ls
```

You will see directories for different types of network devices, such as:

| Directory   | Description               |
|-------------|---------------------------|
| `ethernet/` | Ethernet drivers.         |
| `wireless/` | Wireless network drivers. |
| `usb/`      | USB network drivers.      |

**Viewing a Specific Driver**

For example, to view the source code for a Realtek Ethernet driver:

```bash
cd ethernet/realtek
ls
```

Files like `r8169.c` represent the source code for specific drivers.

You can examine the code using a text editor:

```bash
less r8169.c
```

**Note:** Understanding kernel source code requires knowledge of the C programming language and kernel development practices.

### Configuring the Kernel

Before configuring the kernel, ensure that you have the necessary tools installed.

**Install Required Packages on Ubuntu/Debian:**

```bash
sudo apt-get install build-essential libncurses-dev bison flex libssl-dev libelf-dev
```

| Package            | Description                                        |
|--------------------|----------------------------------------------------|
| `build-essential`  | Provides essential tools like `gcc` and `make`.    |
| `libncurses-dev`   | Needed for the menu configuration interface.       |
| `bison` and `flex` | Required for parsing during the build process.     |
| `libssl-dev`       | Provides SSL libraries.                            |
| `libelf-dev`       | ELF object file access library.                    |

#### Using `make menuconfig`

`make menuconfig` is a terminal-based configuration utility that allows you to configure the kernel options via a text-based menu.

**Steps:**

I. Navigate to the Kernel Source Directory:

```bash
cd linux-5.8.12
```

II. Run the Configuration Utility:

```bash
make menuconfig
```

This will display a menu with various categories:

- General setup
- Platform options
- Processor type and features
- Power management options
- Bus options
- Executable file formats
- Networking support
- Device drivers
- File systems
- Security options

#### Understanding Kernel Configuration Options

**Navigating the Menu:**

| Key         | Description                              |
|-------------|------------------------------------------|
| Arrow Keys  | Move up and down the menu.               |
| Enter       | Select a menu item or enter a submenu.   |
| Spacebar    | Toggle selections.                       |

**Configuration Symbols:**

| Symbol | Description                           |
|--------|---------------------------------------|
| `[*]`  | Feature is built into the kernel.     |
| `[ ]`  | Feature is not included.              |
| `<M>`  | Feature is built as a loadable module.|

**Example: Configuring File System Support**

I. **Select `File systems`**:

```bash
File systems  --->
```

II. **View Supported File Systems**:

- Second extended fs support (ext2)
- Third extended fs support (ext3)
- Fourth extended fs support (ext4)
- FAT file system support
- NTFS file system support

III. **Enabling NTFS Support**:

- Press `Spacebar` to select **NTFS file system support**
- Note that write support may be experimental.

**Example: Enabling a Device Driver as a Module**

I. Navigate to `Device Drivers`:

```bash
Device Drivers  --->
```

II. Select a Device Category (e.g., `Network device support`):

```bash
Network device support  --->
```

III. Choose a Specific Driver:

- Locate the driver for your hardware.
- Press `M` to compile it as a module.

#### Key aspects of `sysctl`

`sysctl` is a utility that allows for querying and modifying kernel parameters at runtime. These parameters control various aspects of the operating system's behavior, such as networking, process limits, security settings, and more. It is commonly used by system administrators to fine-tune the performance and behavior of the system without needing to reboot.

- The kernel manages hardware and software interactions on a system, and these interactions are governed by kernel parameters. For example, parameters can control how much memory a process can use or how networking functions are handled.
- Kernel parameters are usually found in the `/proc/sys/` directory. Each parameter is represented as a file that can be read or modified using the `sysctl` command.

**Usage:**

I. View current kernel parameters:

```bash
sysctl -a
```

This command will list all kernel parameters and their current values.

II. View a specific kernel parameter:

```bash
sysctl net.ipv4.ip_forward
```

This will display the value of the `net.ipv4.ip_forward` parameter, which controls whether the system can act as a router by forwarding network packets.

III. Modify a kernel parameter temporarily:

```bash
sysctl -w net.ipv4.ip_forward=1
```

This command will enable IP forwarding, but the change will only last until the system is rebooted.

IV. Make changes permanent:

To make changes permanent, you need to add the parameter to the `/etc/sysctl.conf` file (or in newer systems, files in `/etc/sysctl.d/`):

```
net.ipv4.ip_forward = 1
```

After editing the configuration file, you can apply the changes without rebooting using:

```bash
sysctl -p
```

Here are some common scenarios where `sysctl` is used, with relevant examples and explanations for each:

##### Adjust TCP Buffer Sizes (Network Performance Tuning)

You want to optimize the network performance, especially for high-bandwidth or high-latency environments, by adjusting TCP buffer sizes.

```bash
sysctl -w net.core.rmem_max=16777216  # Max receive buffer size
sysctl -w net.core.wmem_max=16777216  # Max send buffer size
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"  # Receive buffer settings
sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"  # Send buffer settings
```

**Permanent Configuration:**

```
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
```

Adjusting TCP buffer sizes can significantly impact network performance, particularly for high-latency links like satellite or intercontinental connections.

##### Reduce Swap Usage (Memory Management)

You want to reduce swap usage to improve performance for systems with enough RAM by adjusting how aggressively the system uses swap space.

```bash
sysctl -w vm.swappiness=10
```

**Permanent Configuration:**

```
vm.swappiness = 10
```

`vm.swappiness` controls how likely the kernel is to swap memory pages to disk. A lower value (0-10) means the system will prioritize using RAM before swapping, which is helpful for performance on systems with sufficient memory.

##### Enable Kernel Address Space Layout Randomization (Security)

You want to enhance system security by enabling address space layout randomization (ASLR), which helps prevent certain types of attacks.

```bash
sysctl -w kernel.randomize_va_space=2
```

**Permanent Configuration:**

```
kernel.randomize_va_space = 2
```

ASLR randomizes the memory addresses used by system processes, making it harder for attackers to exploit memory corruption vulnerabilities. Setting `kernel.randomize_va_space` to 2 fully enables it.

##### Increase Maximum Number of Open File Descriptors (Process Management)

You need to increase the maximum number of file descriptors a process can open, which is important for applications handling many simultaneous connections (e.g., web servers).

```bash
sysctl -w fs.file-max=100000
```

**Permanent Configuration:**

```
fs.file-max = 100000
```

This setting increases the limit on the total number of file descriptors the kernel can allocate. Useful for optimizing servers under heavy load.

##### Increase Shared Memory Limits (For Databases)

You are tuning a database (e.g., PostgreSQL) that relies on shared memory, and you need to increase the shared memory limits.

```bash
sysctl -w kernel.shmmax=68719476736  # Set maximum size of a single shared memory segment
sysctl -w kernel.shmall=4294967296    # Set total amount of shared memory (in pages)
```

**Permanent Configuration:**

```
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
```

These parameters configure how much shared memory can be allocated by the system, which is critical for database systems that use shared memory for caching and buffers.

##### Disable ICMP Redirect Acceptance (Security)

To enhance network security, you want to disable the system’s acceptance of ICMP redirects, which can be used maliciously to alter routing tables.

```bash
sysctl -w net.ipv4.conf.all.accept_redirects=0
sysctl -w net.ipv4.conf.default.accept_redirects=0
```

**Permanent Configuration:**

```
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
```

Disabling ICMP redirects ensures that malicious users cannot alter the routing table by sending false ICMP redirect messages. It is a common practice to harden system security.

##### Control TCP SYN Cookies (DDoS Mitigation)

You want to enable SYN cookies to protect against SYN flood attacks, a type of denial-of-service (DoS) attack.

```bash
sysctl -w net.ipv4.tcp_syncookies=1
```

**Permanent Configuration:**

```
net.ipv4.tcp_syncookies = 1
```

SYN cookies help mitigate SYN flood attacks by ensuring that the kernel doesn't allocate resources to half-open TCP connections during an attack. Instead, it uses cryptographic cookies to validate connection requests.

#### The Importance of Kernel Configuration

Proper kernel configuration is crucial:

- Including only necessary components can streamline the kernel.
- Ensuring that all hardware devices are supported by the kernel.
- Disabling unnecessary features can reduce the attack surface.

Caution: Incorrect configuration may result in an unbootable system. It's advisable to:

- Save the current working configuration.
- Use virtual machines or non-critical systems for testing.

### Compiling and Installing the Kernel

After configuring the kernel, you can proceed to compile it.

**Compile the Kernel and Modules:**

```bash
make -j$(nproc)
```

Options:

- `-j$(nproc)` utilizes all available CPU cores for faster compilation.

**Note**: The compilation process may take considerable time depending on system resources.

#### Installing Modules and the Kernel

**Install Kernel Modules:**

```bash
sudo make modules_install
```

This installs the kernel modules to `/lib/modules/<kernel-version>`.

**Install the Kernel:**

```bash
sudo make install
```

This installs:

| File           | Description                                  |
|----------------|----------------------------------------------|
| Kernel Image   | `/boot/vmlinuz-<kernel-version>`             |
| System Map     | `/boot/System.map-<kernel-version>`          |
| Configuration  | `/boot/config-<kernel-version>`              |

#### Updating the Bootloader

After installing the new kernel, update the bootloader to recognize it.

**For GRUB2:**

```bash
sudo update-grub
```

This scans for all available kernels and updates `/boot/grub/grub.cfg`.

**Verify the New Kernel Entry:**

```bash
grep menuentry /boot/grub/grub.cfg
```

Look for an entry corresponding to your new kernel version.

### Challenges

1. Download the latest Linux kernel source code from the official repository. Configure and compile it for a specific system. Document the steps and choices made during configuration.
2. Develop a simple kernel module, such as a 'Hello World' module. Load and unload it from your Linux kernel, and inspect the system log to verify its functioning.
3. Tune a Linux kernel for enhanced performance on a specific hardware setup. Modify parameters such as scheduler settings, file system support, and networking options. Benchmark the system before and after the optimization.
4. Find on the internet a kernel patch (for a bug fix or improvement) and apply it to your kernel source. Re-compile and test the kernel to ensure the patch functions as expected.
5. Simulate a kernel panic using tools or commands (like `sysrq` trigger). Capture and analyze the output to understand the cause of the panic and how to recover from such situations.
6. Create a custom kernel configuration for a specific use case, like a gaming system, server, or embedded device. Tailor features and modules for the chosen application, and explain your configuration choices.
7. Write a script to automate the deployment of a newly compiled kernel, including copying it to the `/boot` directory, updating the boot loader configuration, and rebooting the system.
8. Use the `git bisect` tool to identify a regression in the kernel. Document the process of finding the offending commit in the kernel source.
9. Configure and compile a real-time Linux kernel. Test its real-time capabilities with appropriate benchmarks or tools, and discuss the implications and challenges of using a real-time kernel.
10. Explore kernel security modules like SELinux or AppArmor. Set up a module, create custom security policies, and test their effectiveness in enhancing system security.
