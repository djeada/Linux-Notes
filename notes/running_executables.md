## How the Linux Kernel Executes Programs

When you type a command such as:

```bash
ls
```

a lot happens behind the scenes.

The shell does not directly “become” `ls` by itself. Instead, it asks the Linux kernel to execute the program. The main system call involved is:

```c
execve()
```

The `execve` system call replaces the current process image with a new program.

That means the process keeps the same process ID, but its memory, code, stack, arguments, and environment are replaced with those of the new program.

A simple view looks like this:

```text
Before execve:

Process PID 1234
+----------------------+
| Program: shell       |
| Code: /bin/bash      |
| Args: bash           |
| Env: PATH=...        |
+----------------------+

execve("/bin/ls", ["ls"], envp)

After execve:

Process PID 1234
+----------------------+
| Program: ls          |
| Code: /bin/ls        |
| Args: ls             |
| Env: PATH=...        |
+----------------------+
```

The process did not get a new PID. It became a different program.

### Big Picture

Program execution usually involves several layers.

```text
User types command
        |
        v
Shell parses command
        |
        v
Shell usually calls fork()
        |
        v
Child process calls execve()
        |
        v
Kernel loads executable
        |
        v
Kernel sets up memory, stack, arguments, environment
        |
        v
Program starts running
```

For a normal shell command, the shell usually uses both:

- fork()    create a child process
- execve()  replace the child with the requested program

This is why the shell survives after running a command.

If the shell directly called `execve("ls", ...)` without forking first, the shell itself would be replaced by `ls`.

### The `execve` System Call

The C function signature is:

```c
int execve(const char *pathname, char *const argv[], char *const envp[]);
```

The arguments are:

- pathname   path to the program to execute
- argv       argument vector passed to the new program
- envp       environment variables passed to the new program

Example:

```c
execve("/bin/ls", ["ls", "-l", "/tmp", NULL], envp);
```

This asks the kernel to run:

```bash
/bin/ls -l /tmp
```

The new program receives:

```text
argv[0] = "ls"
argv[1] = "-l"
argv[2] = "/tmp"
```

Environment variables such as `PATH`, `HOME`, `USER`, and `LANG` can also be passed to the new program.

### Important Property of `execve`

`execve` does not create a new process.

It transforms the current process.

- fork() creates a new process.
- execve() replaces the current process image.

This distinction is very important.

```text
Shell
 |
 | fork()
 v
Child process
 |
 | execve("/bin/ls")
 v
ls process
```

The shell remains alive because it forked first. The child becomes `ls`.

### What the Kernel Does During `execve`

When a process calls `execve`, the kernel performs several steps.

1. Validate the executable path
2. Check permissions
3. Open the file
4. Identify the binary format
5. Load the program into memory
6. Set up a new virtual address space
7. Set up stack, arguments, and environment
8. Configure registers
9. Start execution at the program entry point

A simplified kernel-side flow looks like this:

```text
execve()
   |
   v
do_execveat_common()
   |
   v
prepare binary parameters
   |
   v
search_binary_handler()
   |
   +--> ELF executable      -> load_elf_binary()
   |
   +--> script with #!      -> load_script()
   |
   +--> other binary format -> matching handler
   |
   v
set up memory mappings
   |
   v
set up stack and registers
   |
   v
jump to program entry point
```

Function names can vary slightly between kernel versions. On many modern kernels, useful functions to inspect include:

- do_execveat_common
- bprm_execve
- search_binary_handler
- load_elf_binary
- start_thread

### Observing `execve` with `strace`

The easiest way to observe program execution is with `strace`.

Run:

```bash
strace -e execve ls
```

Example output:

```text
execve("/usr/bin/ls", ["ls"], 0x7ffc8e0a9b10 /* 45 vars */) = 0
```

Interpretation:

- The program /usr/bin/ls was executed.
- argv contained one argument: "ls".
- The process received environment variables.
- The return value is 0 in the trace because exec succeeded.

Normally, a successful `execve` does not return to the old program. If `execve` returns, it usually means it failed.

Example failure:

```bash
strace -e execve /no/such/program
```

Example output:

```text
execve("/no/such/program", ["/no/such/program"], 0x7ffd...) = -1 ENOENT (No such file or directory)
```

Interpretation:

- The kernel could not find the requested executable.
- ENOENT means the file or path does not exist.

### `execve` and the Shell

When you run:

```bash
ls -l
```

the shell usually searches your `PATH` to find `ls`.

If `PATH` includes:

```text
/usr/local/bin:/usr/bin:/bin
```

the shell may find:

```text
/usr/bin/ls
```

Then it runs something conceptually like:

```c
fork();
execve("/usr/bin/ls", ["ls", "-l", NULL], envp);
```

The kernel does not search `PATH` for `execve`.

Important distinction:

- The shell searches PATH.
- execve needs a pathname.

Some higher-level functions, such as `execvp`, do search `PATH`, but they are library functions. They eventually call `execve`.

### Executing Scripts

Not every executable file is a compiled binary.

A script may begin with a shebang line:

```bash
#!/bin/sh
```

Example script:

```bash
#!/bin/sh
echo "Hello from script"
```

When the kernel sees the `#!` line, it uses the interpreter.

```text
Script file:
./hello.sh

First line:
#!/bin/sh

Kernel executes:
/bin/sh ./hello.sh
```

The flow looks like this:

```text
execve("./hello.sh")
        |
        v
Kernel sees #!/bin/sh
        |
        v
Kernel executes interpreter
        |
        v
execve("/bin/sh", ["/bin/sh", "./hello.sh"], envp)
```

This is why the interpreter path must be valid.

If the shebang points to a missing interpreter, the script fails even if the script itself exists.

### Executable Permissions

For `execve` to work, permissions matter.

Check a file:

```bash
ls -l ./hello
```

Example:

```text
-rwxr-xr-x 1 user user 16000 Jun 1 12:00 hello
```

The `x` bits mean the file is executable.

If a file is not executable:

```text
-rw-r--r-- 1 user user 16000 Jun 1 12:00 hello
```

running it may fail:

```bash
./hello
```

Example output:

```text
bash: ./hello: Permission denied
```

Fix:

```bash
chmod +x ./hello
```

### Binary Formats

Linux can execute several types of files through binary format handlers.

Common examples:

- ELF binaries
- scripts with shebang lines
- miscellaneous registered binary formats through binfmt_misc

Most compiled Linux programs use the ELF format.

ELF stands for Executable and Linkable Format.

To inspect a binary:

```bash
file /bin/ls
```

Example output:

```text
/bin/ls: ELF 64-bit LSB pie executable, x86-64, dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2
```

Interpretation:

- /bin/ls is an ELF executable.
- It is for x86-64.
- It is dynamically linked.
- It uses a dynamic linker.

### ELF Loading

For ELF binaries, the kernel uses the ELF loader.

A simplified ELF loading flow:

```text
Kernel opens executable
        |
        v
Reads ELF header
        |
        v
Checks architecture and format
        |
        v
Maps program segments into memory
        |
        v
Sets up stack with argv, envp, auxiliary vector
        |
        v
Sets instruction pointer to entry point
        |
        v
Program begins execution
```

To inspect the ELF header:

```bash
readelf -h /bin/ls
```

Example output:

```text
ELF Header:
  Class:                             ELF64
  Machine:                           Advanced Micro Devices X86-64
  Entry point address:               0x61d0
```

Interpretation:

- The binary is a 64-bit ELF file.
- It targets x86-64.
- The entry point is the address where execution begins.

### Static and Dynamic Linking

Programs can be statically linked or dynamically linked.

- Static linking:
  library code is included inside the executable

- Dynamic linking:
  the executable depends on shared libraries at runtime

### Static Linking

A statically linked binary contains the library code it needs.

Compile statically:

```bash
gcc -static -o hello-static hello.c
```

Check it:

```bash
file hello-static
```

Example output:

```text
hello-static: ELF 64-bit LSB executable, x86-64, statically linked
```

Run:

```bash
ldd hello-static
```

Example output:

```text
not a dynamic executable
```

Interpretation:

- The binary does not need the dynamic linker to load shared libraries.
- Most required code is inside the executable.

Static binaries are useful for initramfs environments because they do not need many external libraries.

### Dynamic Linking

Most normal Linux programs are dynamically linked.

A dynamically linked program depends on shared libraries such as:

- libc.so.6
- libpthread.so
- libm.so

The kernel loads the executable and notices that it needs an interpreter, commonly:

```text
/lib64/ld-linux-x86-64.so.2
```

or on Debian/Ubuntu systems:

```text
/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
```

Then the dynamic linker loads the shared libraries.

```text
Executable
    |
    v
Kernel sees dynamic linker path
    |
    v
Dynamic linker starts
    |
    v
Shared libraries are loaded
    |
    v
Program main() begins
```

Diagram:

```text
+-------------------+       +-------------------+       +-------------------+
| Executable        | ----> | Dynamic Linker    | ----> | Shared Libraries  |
| ./myapp           |       | ld-linux...       |       | libc.so.6, etc.   |
+-------------------+       +-------------------+       +-------------------+
```

### Inspecting Shared Libraries with `ldd`

Use:

```bash
ldd /usr/bin/ls
```

Example output:

```text
linux-vdso.so.1 (0x00007ffc12345000)
libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
/lib64/ld-linux-x86-64.so.2
```

Interpretation:

- /usr/bin/ls depends on shared libraries.
- The dynamic linker found the libraries on the system.

If a library is missing, `ldd` may show:

```text
libexample.so => not found
```

That means the program may fail to start.

### Library Search Paths

The dynamic linker searches for libraries using several sources.

Common places include:

- RPATH or RUNPATH embedded in the executable
- LD_LIBRARY_PATH environment variable
- /etc/ld.so.cache
- /lib
- /usr/lib
- /lib64
- /usr/lib64
- distribution-specific library directories

The flow is roughly:

```text
Program needs libexample.so
        |
        v
Dynamic linker checks configured search paths
        |
        v
If found, library is loaded
        |
        v
If not found, program fails
```

### `ldconfig`

The `ldconfig` command updates the shared library cache.

The cache is stored at:

```text
/etc/ld.so.cache
```

To update it:

```bash
sudo ldconfig
```

To add a custom library directory:

```bash
echo "/opt/myapp/lib" | sudo tee /etc/ld.so.conf.d/myapp.conf
sudo ldconfig
```

Check whether a library is known:

```bash
ldconfig -p | grep mylib
```

### `LD_LIBRARY_PATH`

`LD_LIBRARY_PATH` temporarily adds directories to the library search path.

Example:

```bash
export LD_LIBRARY_PATH=/opt/myapp/lib:$LD_LIBRARY_PATH
./myapp
```

This is useful for testing and development.

However, it can cause version conflicts if used carelessly.

A good rule is:

- Use LD_LIBRARY_PATH for temporary testing.
- Use ldconfig or proper packaging for stable system-wide configuration.

### Building a Custom Kernel for Learning

Building a custom kernel is a useful way to understand how Linux executes programs internally.

This is a lab activity. It should be done in a virtual machine, containerized build environment, or disposable test system.

Do not replace the kernel on an important machine unless you understand kernel recovery.

### Kernel Source

Clone the kernel source:

```bash
git clone https://github.com/torvalds/linux.git
cd linux
```

Create a default configuration:

```bash
make defconfig
```

This creates a `.config` file for your architecture.

### Debug-Friendly Kernel Configuration

For kernel debugging, useful settings include:

- debug symbols
- GDB scripts
- kernel debugging options
- disabled KASLR
- simplified feature set

Open the configuration menu:

```bash
make menuconfig
```

Useful options to consider:

- Enable debug info
- Enable GDB scripts
- Disable KASLR
- Enable kernel debugger options if needed
- Reduce unneeded drivers or features for faster builds

KASLR means Kernel Address Space Layout Randomization. It randomizes where the kernel is loaded in memory.

For debugging, disabling KASLR makes addresses easier to understand.

### Compiling the Kernel

Build with all CPU cores:

```bash
make -j$(nproc)
```

Build GDB helper scripts:

```bash
make scripts_gdb
```

The uncompressed debug kernel image is usually:

```text
vmlinux
```

The bootable compressed kernel image on x86 is usually:

```text
arch/x86/boot/bzImage
```

### Initramfs

An initramfs is an initial RAM filesystem loaded by the kernel during boot.

It provides a minimal user-space environment before the real root filesystem is mounted.

For a kernel execution lab, an initramfs can contain:

- a shell
- basic utilities
- test programs
- an init script

The kernel starts the first user-space process, usually:

```text
/init
```

inside the initramfs.

### BusyBox

BusyBox provides many small Unix utilities in one binary.

It is commonly used in initramfs labs.

Download and extract:

```bash
wget https://busybox.net/downloads/busybox-1.35.0.tar.bz2
tar -xjf busybox-1.35.0.tar.bz2
cd busybox-1.35.0
```

Configure:

```bash
make defconfig
make menuconfig
```

Enable:

- Build BusyBox as a static binary

Build:

```bash
make -j$(nproc)
make install
```

This creates:

```text
_install/
```

containing BusyBox and utility symlinks.

### Creating a Minimal Initramfs

Create directories:

```bash
mkdir -p ../initramfs/{bin,sbin,etc,proc,sys,usr/{bin,sbin}}
```

Copy BusyBox files:

```bash
cp -r _install/* ../initramfs/
```

Create `/init`:

```bash
cat > ../initramfs/init << 'EOF'
#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
echo "Welcome to the custom initramfs shell!"
exec /bin/sh
EOF
```

Make it executable:

```bash
chmod +x ../initramfs/init
```

Important note:

- /init must be executable.
- If /init is missing or not executable, the kernel may panic because it cannot start user space.

### Adding a Test Program

Create a small C program:

```bash
cat > ../initramfs/hello.c << 'EOF'
#include <stdio.h>

int main(void) {
    printf("Hello from the custom kernel!\n");
    return 0;
}
EOF
```

Compile it statically:

```bash
gcc -static -o ../initramfs/bin/hello ../initramfs/hello.c
```

Check:

```bash
file ../initramfs/bin/hello
```

Expected output includes:

```text
statically linked
```

This matters because the minimal initramfs may not contain shared libraries.

### Creating the Initramfs Archive

From inside the initramfs directory:

```bash
cd ../initramfs
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
cd ..
```

This creates:

```text
initramfs.cpio.gz
```

The kernel can load this archive as its initial filesystem.

### Booting with QEMU

QEMU can boot the custom kernel without replacing your real system kernel.

Run:

```bash
qemu-system-x86_64 \
  -kernel linux/arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0" \
  -nographic \
  -s -S
```

Option meanings:

- -kernel    kernel image to boot
- -initrd    initramfs archive
- -append    kernel command-line arguments
- console=ttyS0 sends output to serial console
- -nographic uses terminal instead of graphical display
- -s starts a GDB server on TCP port 1234
- -S pauses CPU at startup until GDB continues execution

The `-s -S` options are useful for debugging.

### Debugging with GDB

In another terminal:

```bash
gdb linux/vmlinux
```

Connect to QEMU:

```gdb
target remote :1234
```

The kernel is paused.

Useful setup:

```gdb
set pagination off
```

Set a breakpoint.

Depending on kernel version, try:

```gdb
break do_execveat_common
```

or:

```gdb
break bprm_execve
```

or search for relevant symbols:

```gdb
info functions execve
info functions search_binary_handler
```

Continue:

```gdb
continue
```

When you run a program inside QEMU, the breakpoint should trigger during execution.

### Binary Handler Selection

The kernel uses binary handlers to decide how to execute a file.

The important function is commonly:

```text
search_binary_handler
```

It checks available handlers and selects the right one.

Examples:

- ELF binary       -> load_elf_binary
- script with #!   -> script handler
- other formats    -> other registered handlers

Set a breakpoint:

```gdb
break search_binary_handler
continue
```

When it stops, inspect the execution path.

For ELF binaries, another useful breakpoint is:

```gdb
break load_elf_binary
continue
```

### Program Entry Point

After loading the binary, the kernel prepares CPU registers so execution begins at the program entry point.

On x86-64, the instruction pointer register controls the next instruction to execute.

In kernel debugging, you may inspect something like:

```gdb
print/x regs->ip
```

The exact register structure and symbol names can vary by kernel version and architecture.

Compare with:

```bash
readelf -h hello
```

Look for:

```text
Entry point address
```

Interpretation:

- The ELF entry point is where execution begins.
- The kernel sets the process state so the CPU starts there.

### Scenario 1: Observe `execve` for a Normal Command

#### Goal

See the system call used to execute a program.

#### Simulate

```bash
strace -e execve ls
```

#### Example Output

```text
execve("/usr/bin/ls", ["ls"], 0x7ffc8e0a9b10 /* 45 vars */) = 0
```

#### Interpretation

- The ls command was executed using execve.
- The path was /usr/bin/ls.
- The argument list contained "ls".
- The process received environment variables.

#### Real Use

Use this when you want to confirm which executable is actually being run.

### Scenario 2: Show That `execve` Replaces the Current Process

#### Goal

Demonstrate that `execve` does not create a new PID.

#### Create Program

```bash
cat > exec-demo.c << 'EOF'
#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("Before execve: PID=%d\n", getpid());

    char *argv[] = {"/bin/echo", "Hello after execve", NULL};
    char *envp[] = {NULL};

    execve("/bin/echo", argv, envp);

    perror("execve failed");
    return 1;
}
EOF
```

Compile:

```bash
gcc -o exec-demo exec-demo.c
```

Run:

```bash
./exec-demo
```

#### Example Output

```text
Before execve: PID=8123
Hello after execve
```

#### Interpretation

- The program printed its PID before execve.
- Then it was replaced by /bin/echo.
- The original program did not continue after successful execve.

The line after `execve` only runs if `execve` fails.

### Scenario 3: Observe a Script Shebang

#### Goal

See how executing a script causes the interpreter to run.

#### Create Script

```bash
cat > hello-script.sh << 'EOF'
#!/bin/sh
echo "hello from script"
EOF

chmod +x hello-script.sh
```

Trace it:

```bash
strace -e execve ./hello-script.sh
```

#### Example Output

```text
execve("./hello-script.sh", ["./hello-script.sh"], 0x7ffc...) = 0
hello from script
```

Depending on tracing options and shell behavior, you may also observe `/bin/sh` being involved.

#### Interpretation

- The kernel sees the shebang line.
- The script is executed through /bin/sh.
- The script itself is not native machine code.

#### Failure Case

Change the shebang to a missing interpreter:

```bash
cat > bad-script.sh << 'EOF'
#!/no/such/interpreter
echo "this will not run"
EOF

chmod +x bad-script.sh
./bad-script.sh
```

Example output:

```text
bash: ./bad-script.sh: cannot execute: required file not found
```

Interpretation:

- The script exists.
- The interpreter in the shebang does not exist.
- Execution fails because the kernel cannot start the interpreter.

### Scenario 4: Compare Static and Dynamic Binaries

#### Goal

Understand the difference between static and dynamic linking.

#### Create Program

```bash
cat > hello.c << 'EOF'
#include <stdio.h>

int main(void) {
    puts("hello");
    return 0;
}
EOF
```

Compile dynamically:

```bash
gcc -o hello-dynamic hello.c
```

Compile statically:

```bash
gcc -static -o hello-static hello.c
```

Check:

```bash
file hello-dynamic hello-static
```

#### Example Output

```text
hello-dynamic: ELF 64-bit LSB pie executable, x86-64, dynamically linked
hello-static:  ELF 64-bit LSB executable, x86-64, statically linked
```

Run `ldd`:

```bash
ldd hello-dynamic
ldd hello-static
```

#### Example Output

```text
linux-vdso.so.1
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
/lib64/ld-linux-x86-64.so.2

not a dynamic executable
```

#### Interpretation

- The dynamic binary depends on shared libraries.
- The static binary contains the needed library code.
- The static binary is more suitable for minimal initramfs labs.

### Scenario 5: Diagnose a Missing Shared Library

#### Goal

Practice identifying why a dynamically linked program fails to start.

#### Simulate Conceptually

If a program depends on a missing library, running `ldd` may show:

```bash
ldd ./myapp
```

Example output:

```text
libexample.so => not found
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
```

#### Interpretation

- The program requires libexample.so.
- The dynamic linker cannot find it.
- The program will likely fail at startup.

#### Fix Options

Temporary development fix:

```bash
export LD_LIBRARY_PATH=/opt/myapp/lib:$LD_LIBRARY_PATH
./myapp
```

System-wide fix:

```bash
echo "/opt/myapp/lib" | sudo tee /etc/ld.so.conf.d/myapp.conf
sudo ldconfig
```

Verify:

```bash
ldconfig -p | grep libexample
```

### Scenario 6: Boot a Minimal Initramfs and Run a Static Program

#### Goal

Verify that a custom kernel can start a minimal user space and execute a test program.

#### Simulate

Boot QEMU:

```bash
qemu-system-x86_64 \
  -kernel linux/arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0" \
  -nographic
```

Inside QEMU, run:

```bash
/bin/hello
```

#### Example Output

```text
Welcome to the custom initramfs shell!
/ # /bin/hello
Hello from the custom kernel!
```

#### Interpretation

- The kernel booted successfully.
- The initramfs /init script ran.
- The shell started.
- The test program executed successfully.

This confirms that the kernel can load and execute a user-space ELF program.

### Scenario 7: Break on Kernel Exec Path with GDB

#### Goal

Observe the kernel execution path when a program runs.

#### Start QEMU Paused

```bash
qemu-system-x86_64 \
  -kernel linux/arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0" \
  -nographic \
  -s -S
```

#### Connect GDB

```bash
gdb linux/vmlinux
```

Inside GDB:

```gdb
target remote :1234
set pagination off
info functions execve
break do_execveat_common
continue
```

If the symbol is unavailable, try:

```gdb
break bprm_execve
break search_binary_handler
break load_elf_binary
```

#### Trigger Exec

Inside QEMU:

```bash
/bin/hello
```

#### Example GDB Output

```text
Breakpoint 1, do_execveat_common (...)
```

#### Interpretation

- The kernel reached the exec path.
- The program execution request entered kernel code.
- You can now step through the loading process.

### Scenario 8: Observe ELF Handler Selection

#### Goal

Watch the kernel choose the correct binary format handler.

#### GDB Breakpoints

```gdb
break search_binary_handler
break load_elf_binary
continue
```

Run inside QEMU:

```bash
/bin/hello
```

#### Example Interpretation

- search_binary_handler is called.
- The kernel checks available binary handlers.
- For the hello program, the ELF handler is selected.
- load_elf_binary handles the executable.

This shows how Linux supports multiple executable formats.

### Scenario 9: Compare ELF Entry Point with Kernel Register Setup

#### Goal

Connect the ELF entry point to where execution begins.

#### Check Entry Point

Inside the build host:

```bash
readelf -h initramfs/bin/hello
```

Example output:

```text
Entry point address:               0x401530
```

#### Inspect in GDB

Near the end of ELF loading, inspect the instruction pointer setup.

Example:

```gdb
print/x regs->ip
```

Example output:

```text
$1 = 0x401530
```

#### Interpretation

- The ELF header says execution begins at 0x401530.
- The kernel prepared the process so the CPU begins at that address.

Exact addresses and structures may vary depending on architecture, compiler, static vs dynamic linking, and kernel version.

### Scenario 10: Trace Dynamic Linker Involvement

#### Goal

Understand that dynamically linked programs involve the dynamic linker.

#### Check a Normal Binary

```bash
file /bin/ls
```

Example:

```text
/bin/ls: ELF 64-bit LSB pie executable, x86-64, dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2
```

Inspect program headers:

```bash
readelf -l /bin/ls | grep interpreter
```

Example output:

```text
[Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
```

#### Interpretation

- The executable asks the kernel to start the dynamic linker.
- The dynamic linker loads required shared libraries.
- Then the program begins normal execution.

This is why dynamically linked binaries need the correct linker and libraries to exist in the runtime environment.

### Common Problems and Fixes

#### Problem: Permission Denied

Example:

```text
bash: ./hello: Permission denied
```

Check:

```bash
ls -l ./hello
```

Fix:

```bash
chmod +x ./hello
```

Interpretation:

```text
The file exists, but it is not executable.
```

### Problem: No Such File or Directory

Example:

```text
bash: ./hello: No such file or directory
```

Possible causes:

- file path is wrong
- interpreter is missing
- dynamic linker is missing
- required runtime path is missing

Check:

```bash
ls -l ./hello
file ./hello
readelf -l ./hello | grep interpreter
ldd ./hello
```

If `file` shows a dynamic interpreter that does not exist, the binary cannot start.

### Problem: Missing Shared Library

Example:

```text
error while loading shared libraries: libexample.so: cannot open shared object file
```

Check:

```bash
ldd ./myapp
```

Fix:

```bash
export LD_LIBRARY_PATH=/path/to/lib:$LD_LIBRARY_PATH
```

or:

```bash
echo "/path/to/lib" | sudo tee /etc/ld.so.conf.d/myapp.conf
sudo ldconfig
```

### Problem: Initramfs Kernel Panic

Example:

```text
Kernel panic - not syncing: No working init found
```

Possible causes:

- /init missing
- /init not executable
- /init has wrong shebang
- shell interpreter missing
- BusyBox not copied correctly
- initramfs archive created incorrectly

Check initramfs contents:

```bash
mkdir /tmp/initramfs-check
cd /tmp/initramfs-check
zcat /path/to/initramfs.cpio.gz | cpio -idmv
ls -l init
file bin/busybox
```

Fix:

```bash
chmod +x init
```

Make sure `/bin/sh` exists.

### Problem: GDB Breakpoint Does Not Work

Possible causes:

- function name changed in this kernel version
- debug symbols are missing
- KASLR is enabled
- wrong vmlinux file is loaded
- kernel was optimized in a way that changes symbol visibility

Check symbols:

```gdb
info functions execve
info functions binary_handler
info functions load_elf
```

Make sure GDB uses:

```text
linux/vmlinux
```

not only the compressed `bzImage`.

### Useful Command Summary

Observe execution:

```bash
strace -e execve ls
strace -f -e execve bash -c 'ls | wc -l'
```

Inspect binaries:

```bash
file ./program
readelf -h ./program
readelf -l ./program
ldd ./program
```

Compile test programs:

```bash
gcc -o hello hello.c
gcc -static -o hello-static hello.c
```

Library cache:

```bash
sudo ldconfig
ldconfig -p | grep library
```

Kernel build:

```bash
git clone https://github.com/torvalds/linux.git
cd linux
make defconfig
make menuconfig
make -j$(nproc)
make scripts_gdb
```

Initramfs archive:

```bash
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
```

QEMU boot:

```bash
qemu-system-x86_64 \
  -kernel linux/arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0" \
  -nographic
```

QEMU with GDB:

```bash
qemu-system-x86_64 \
  -kernel linux/arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0" \
  -nographic \
  -s -S
```

GDB:

```gdb
target remote :1234
break do_execveat_common
break search_binary_handler
break load_elf_binary
continue
```

### Safe Lab Rules

Kernel and QEMU labs can be complex. Use a safe environment.

- Use a virtual machine or disposable lab system.
- Do not replace your main system kernel.
- Keep build directories organized.
- Use static binaries in minimal initramfs environments.
- Disable KASLR for easier debugging.
- Expect kernel function names to vary by version.
- Document the kernel version you are using.

### Practical Challenges

1. Run `strace -e execve ls` and explain the output.
2. Write a small C program that calls `execve("/bin/echo", ...)`. Confirm that the original program does not continue after a successful `execve`.
3. Create a script with a valid shebang and trace its execution. Then create a script with a broken shebang and explain the error.
4. Compile the same `hello.c` program dynamically and statically. Compare `file` and `ldd` output.
5. Use `readelf -h` to find the entry point of a compiled program.
6. Use `readelf -l` to find the dynamic linker requested by a dynamically linked binary.
7. Build a minimal initramfs with BusyBox and a static `hello` program.
8. Boot a custom kernel and initramfs with QEMU.
9. Attach GDB to QEMU and set breakpoints in the exec path.
10. Write a short report explaining the path from typing a command in the shell to the kernel loading and starting the executable.

Once QEMU is waiting for a debugger connection, open another terminal, navigate to your kernel source, and run `gdb vmlinux`. In GDB, do `target remote :1234` and then `continue`. Describe what you see on the QEMU console and why you’re dropped into your initramfs shell.
