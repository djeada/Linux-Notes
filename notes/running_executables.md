## How the Linux Kernel Executes Programs

We'll explore the inner workings of the Linux kernel, focusing on how it loads and executes binaries. We'll dive into the `execve` system call, build a custom kernel, and use debugging tools to see the execution process in action. Whether you're a seasoned developer or just curious about operating systems, this walkthrough aims to shed light on the fascinating journey from a command to a running program.

### The Role of the `execve` System Call

At the heart of program execution in Linux lies the `execve` system call. This function is responsible for replacing the current process image with a new one, effectively running a new program within the same process. When you run a command in the terminal, `execve` is the mechanism that makes it happen.

In C, the function signature of `execve` is:

```c
int execve(const char *pathname, char *const argv[], char *const envp[]);
```

Let's break down the parameters:

- The path to the executable file you want to run.
- An array of argument strings passed to the new program.
- An array of environment variables for the new program.

When a program calls `execve`, the kernel loads the specified executable into memory, sets up the new environment, and starts executing the program from its entry point. The original process is overwritten, but it retains its process ID, which is why `execve` doesn't create a new process but transforms the existing one.

### Observing `execve` in Action with `strace`

To see how `execve` operates under the hood, we can use a tool called `strace`. This utility traces system calls made by a program, allowing us to observe interactions with the kernel.

For example, if we want to see how the `ls` command is executed, we can run:

```bash
strace -e execve ls
```

The `-e execve` option tells `strace` to filter and display only `execve` system calls. When you run this command, you'll see output showing which executables are being invoked, along with the arguments and environment variables. This simple exercise reveals the essential role `execve` plays in running even the most basic commands.

### Building a Custom Linux Kernel

To truly understand how the kernel executes programs, we can build our own version of the Linux kernel. This allows us to customize it for debugging and explore its internals.

#### Cloning the Kernel Source Code

Start by cloning the official Linux kernel repository:

```bash
git clone https://github.com/torvalds/linux.git
```
This command downloads the entire kernel source code into a directory named `linux`. Navigate into this directory:

```bash
cd linux
```

#### Configuring the Kernel

Before compiling, we need to configure the kernel to suit our needs. We can generate a default configuration as a starting point:

```bash
make defconfig
```
This command creates a standard configuration file based on your system's architecture.

#### Customizing for Debugging

To make debugging easier and reduce compilation time, we'll adjust some settings:

I. **Disable Address Space Layout Randomization (KASLR)**: KASLR randomizes the memory address where the kernel is loaded, which can complicate debugging. To disable it:

- Run `make menuconfig` to open the configuration menu.
- Navigate to **Processor type and features**.
- Uncheck **Randomize the address of the kernel image (KASLR)**.

II. **Streamline the Kernel**: Disabling unnecessary features speeds up compilation and simplifies debugging.

- Uncheck **Virtualization** in its respective section.
- Uncheck **Enable loadable module support**.
- Uncheck **Networking support**.

III. **Enable Debugging Options**: These settings provide valuable information when debugging.

- Enable **Compile the kernel with debug info**.
- Enable **Provide GDB scripts for kernel debugging**.
- kernel debugger**.
After making these changes, save your configuration and exit the menu.

#### Compiling the Kernel

Now we're ready to compile the kernel:

```bash
make -j$(nproc)
```

The `-j$(nproc)` option tells `make` to use all available CPU cores, speeding up the process. Compiling the kernel can take some time, so feel free to take a break while it builds.

Once compilation is complete, generate the GDB scripts:

```bash
make scripts_gdb
```

These scripts help GDB (the GNU Debugger) understand kernel data structures during debugging sessions.

### Creating an Initramfs with Custom Programs

An initramfs (initial RAM filesystem) is a simple filesystem loaded into memory during the boot process. We'll create one containing a statically linked shell and a sample program to test our custom kernel.

#### Building a Statically Linked Shell

First, we'll build a minimal shell to use as the initial process:

I. **Download BusyBox**: BusyBox combines tiny versions of many common UNIX utilities into a single small executable.

```bash
wget https://busybox.net/downloads/busybox-1.35.0.tar.bz2
tar -xjf busybox-1.35.0.tar.bz2
cd busybox-1.35.0
```

II. **Configure for Static Linking**:

```bash
make defconfig
```

Then, edit the `.config` file or run:

```bash
make menuconfig
```

Under **BusyBox Settings**, ensure **Build BusyBox as a static binary (no shared libs)** is enabled.

III. **Compile BusyBox**:

```bash
make -j$(nproc)
```

IV. **Install BusyBox**:

```bash
make install
```

This installs BusyBox into a `_install` directory.

#### Preparing the Initramfs

Create a directory to hold the initramfs contents:

```bash
mkdir -p ../initramfs/{bin,sbin,etc,proc,sys,usr/{bin,sbin}}
```

Copy BusyBox into the initramfs:

```bash
cp -r _install/* ../initramfs/
```

Create a simple `init` script that the kernel will execute first:

```bash
cat > ../initramfs/init << 'EOF'

#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
echo "Welcome to the custom initramfs shell!"
exec /bin/sh

EOF
```

Make the script executable:

```bash
chmod +x ../initramfs/init
```

#### Adding a Sample Program

Let's create a simple C program to test:

```bash
cat > ../initramfs/hello.c << 'EOF'

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
  printf("Hello from the custom kernel!\n");
  return 0;
}

EOF
```

Compile the program statically:

```bash
gcc -static -o ../initramfs/bin/hello ../initramfs/hello.c
```

#### Creating the Initramfs Archive

Finally, create the initramfs cpio archive:

```bash
cd ../initramfs
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
cd ..
```

This command finds all files in the initramfs directory, creates a cpio archive in the `newc` format, and compresses it with gzip.

### Booting the Custom Kernel with QEMU

Now that we have a custom kernel and initramfs, we can boot them using QEMU, an open-source emulator that supports virtualization.

#### Starting QEMU

Run the following command:

```bash
qemu-system-x86_64 \
-kernel linux/arch/x86/boot/bzImage \
-initrd initramfs.cpio.gz \
-append "console=ttyS0" \
-nographic \
-s -S
```

Here's what the options mean:

- Specifies the path to the kernel image.
- Specifies the initramfs archive.
- Directs kernel messages to the serial console.
- Disables graphical output; everything goes to the terminal.
- Starts QEMU with GDB debugging enabled and pauses execution at startup.

With these options, QEMU waits for a debugger to connect before starting the kernel.

### Debugging the Kernel with GDB

Now we can connect GDB to QEMU to debug the kernel.

#### Connecting GDB

In a new terminal window, navigate to the kernel source directory and start GDB:

```bash
gdb linux/vmlinux
```

Within GDB, connect to QEMU:

```gdb
(gdb) target remote :1234
```

The kernel is now paused and ready for debugging.

#### Setting Breakpoints

Let's set a breakpoint at the `do_execve` function:

```gdb
(gdb) break do_execve
```

Then, continue execution:

```gdb
(gdb) continue
```

Switch back to the QEMU terminal. The kernel should now boot and drop into our custom shell.

### Observing Program Execution

In the QEMU shell, run our sample program:

```bash
./hello
```

Because we set a breakpoint at `do_execve`, GDB will pause execution when the kernel attempts to execute `hello`.

#### Stepping Through `do_execve`

Back in GDB, we can step through the `do_execve` function to observe how the kernel handles the execution request:

```gdb
(gdb) step
```

As you step through, pay attention to how the kernel prepares the binary for execution, including loading the executable, setting up memory spaces, and initializing the process environment.

#### Inspecting Variables

We can inspect variables and structures to understand the state of the kernel. For example, to view the binary parameters:

```gdb
(gdb) print *bprm
```

This displays the contents of the `linux_binprm` structure, which holds information about the binary being executed.

### Understanding Binary Format Handling

The kernel supports multiple binary formats (like ELF, scripts, etc.). It determines how to execute a file based on its format.

#### Exploring `search_binary_handler`

The function `search_binary_handler` is responsible for finding the appropriate handler for the binary:

```gdb
(gdb) break search_binary_handler
(gdb) continue
```

When the breakpoint hits, you can examine the available handlers:

```gdb
(gdb) print fmt->name
```

By continuing execution and checking the handler's name, you can see how the kernel selects the ELF handler for our compiled program.

### Loading the ELF Binary

Once the ELF handler is selected, the kernel uses `load_elf_binary` to load the executable.

#### Stepping into `load_elf_binary`

Continue stepping through the code:

```gdb
(gdb) step
```

Within `load_elf_binary`, the kernel reads the ELF header, sets up memory mappings, and prepares the process for execution.

#### Checking the ELF Header

You can examine the ELF header:

```gdb
(gdb) print elf_ex.e_ident
```

This should display the magic numbers identifying the file as an ELF executable.

### Starting the Program

After loading the binary, the kernel sets up the initial CPU state and starts the program.

#### Examining `start_thread`

The `start_thread` function sets the instruction pointer and stack pointer for the new process:

```gdb
(gdb) step
```

Check the instruction pointer:

```gdb
(gdb) print/x regs->ip
```

This address should correspond to the entry point of our `hello` program.

#### Verifying the Entry Point

To confirm, you can check the entry point in the compiled binary:

```bash
readelf -h hello
```

Look for the **Entry point address** and compare it to the instruction pointer value from GDB.

### Resuming Execution

Once the setup is complete, we can allow the program to run:

```gdb
(gdb) continue
```

Switch back to the QEMU terminal. You should see the message from our program:

```
Hello from the custom kernel!
```

This indicates that the kernel successfully executed our program.
