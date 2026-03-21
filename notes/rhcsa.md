## RHCSA (Red Hat Certified System Administrator)

The Red Hat Certified System Administrator (RHCSA) certification is one of the most respected credentials in the Linux world. Unlike exams where you pick answers from a list, RHCSA is entirely performance-based — you sit in front of a live Red Hat Enterprise Linux system and complete real tasks within a time limit. If you can pass it, employers know you can actually do the work.

This guide walks through the exam objectives, key concepts you need to master, and practical exercises to build the skills that get tested.

### Exam Details at a Glance

| Detail | Information |
|--------|-------------|
| **Exam Code** | EX200 |
| **Format** | Performance-based (hands-on tasks on a live system) |
| **Duration** | 2.5 hours |
| **Number of Tasks** | Typically 10–15 tasks |
| **Passing Score** | 210 out of 300 (70%) |
| **Cost** | Approximately $500 USD |
| **Prerequisites** | None required, but RHCSA-level experience recommended |
| **Validity** | 3 years |
| **Based On** | Red Hat Enterprise Linux 9 (current version) |

### Exam Objectives Overview

Red Hat publishes official exam objectives that change with each RHEL version. The following covers the major domains:

```
RHCSA Exam Domains
├── Understand and Use Essential Tools
│   ├── Access shell prompts and issue commands
│   ├── Use input/output redirection
│   ├── Use grep and regular expressions
│   ├── Access remote systems using SSH
│   ├── Log in and switch users
│   ├── Archive, compress, unpack, and decompress files
│   ├── Create and edit text files
│   ├── Create, delete, copy, and move files and directories
│   └── Create hard and soft links
├── Create Simple Shell Scripts
│   ├── Conditionals (if/then, case)
│   ├── Loops (for, while)
│   ├── Process script inputs ($1, $2, etc.)
│   └── Process output of shell commands within a script
├── Operate Running Systems
│   ├── Boot, reboot, and shut down normally
│   ├── Boot into different targets manually
│   ├── Interrupt boot process to gain access (reset root password)
│   ├── Identify CPU/memory-intensive processes and kill them
│   ├── Adjust process scheduling
│   ├── Manage tuning profiles
│   ├── Locate and interpret system log files
│   └── Preserve system journals
├── Configure Local Storage
│   ├── List, create, delete partitions (MBR and GPT)
│   ├── Create and remove physical volumes
│   ├── Assign physical volumes to volume groups
│   ├── Create and delete logical volumes
│   ├── Configure systems to mount file systems at boot
│   ├── Configure and manage swap space
│   ├── Create and configure file systems (ext4, xfs)
│   └── Mount and unmount network file systems (NFS)
├── Create and Configure File Systems
│   ├── Create, mount, unmount, and use ext4 and xfs
│   ├── Mount and unmount network file systems (NFS, CIFS)
│   ├── Configure autofs
│   ├── Extend existing logical volumes
│   └── Create and configure set-GID directories
├── Deploy, Configure, and Maintain Systems
│   ├── Schedule tasks using cron and at
│   ├── Start and stop services, configure services to start at boot
│   ├── Configure systems to boot into a specific target
│   ├── Install and update software packages
│   ├── Modify the system bootloader
│   └── Configure time service clients
├── Manage Basic Networking
│   ├── Configure IPv4 and IPv6 addresses
│   ├── Configure hostname resolution
│   ├── Configure network services to start at boot
│   └── Restrict network access using firewalld
├── Manage Users and Groups
│   ├── Create, delete, and modify local user accounts
│   ├── Change passwords and adjust password aging
│   ├── Create, delete, and modify local groups
│   ├── Configure superuser access
│   └── Configure key-based authentication for SSH
├── Manage Security
│   ├── Configure firewall settings using firewalld
│   ├── Manage default file permissions
│   ├── Configure SELinux modes (enforcing, permissive, disabled)
│   ├── List and identify SELinux file and process contexts
│   ├── Restore default file contexts
│   ├── Manage SELinux port labels
│   ├── Use boolean settings to modify SELinux policy
│   └── Diagnose and address routine SELinux policy violations
└── Manage Containers
    ├── Find and retrieve container images
    ├── Inspect container images
    ├── Perform container management (run, start, stop, list, inspect, remove)
    ├── Run a service inside a container
    ├── Configure a container to start automatically as a systemd service
    └── Attach persistent storage to a container
```

### Essential Tools

This section covers the foundational commands and techniques you need. Everything else builds on these skills.

#### Working with Files and Directories

You should be able to perform these operations without hesitation:

```bash
# Create a directory structure
mkdir -p /home/user/project/{docs,src,bin}

# Copy files preserving permissions and ownership
cp -a /source/dir /destination/

# Create hard and soft links
ln /path/to/original /path/to/hardlink
ln -s /path/to/original /path/to/symlink

# Find files by various criteria
find / -name "*.conf" -type f 2>/dev/null
find /home -user student -size +1M
find /var -mtime -7 -name "*.log"
```

#### Input/Output Redirection and Pipes

Redirection shows up in nearly every exam task, even when it's not the main objective:

```bash
# Redirect stdout and stderr separately
command > output.txt 2> errors.txt

# Redirect both to the same file
command &> all_output.txt

# Append instead of overwrite
command >> output.txt 2>&1

# Use pipes to chain commands
ps aux | grep httpd | grep -v grep
cat /etc/passwd | cut -d: -f1 | sort
```

#### Using grep and Regular Expressions

```bash
# Search for a pattern in files
grep "failed" /var/log/secure

# Case-insensitive search
grep -i "error" /var/log/messages

# Show line numbers
grep -n "root" /etc/passwd

# Use extended regular expressions
grep -E "^(root|admin)" /etc/passwd

# Recursive search through directories
grep -r "ServerName" /etc/httpd/
```

#### Archiving and Compression

```bash
# Create a compressed tar archive
tar czf archive.tar.gz /path/to/directory

# Extract a tar archive
tar xzf archive.tar.gz

# List contents without extracting
tar tzf archive.tar.gz

# Create with bzip2 compression
tar cjf archive.tar.bz2 /path/to/directory

# Extract to a specific directory
tar xzf archive.tar.gz -C /target/directory
```

### Operating Running Systems

#### Changing Boot Targets

The exam often asks you to configure the system to boot into a specific target:

```bash
# Check current default target
systemctl get-default

# Set default target to multi-user (no GUI)
systemctl set-default multi-user.target

# Set default target to graphical
systemctl set-default graphical.target

# Switch to a different target immediately
systemctl isolate rescue.target
```

#### Resetting the Root Password

This is a classic RHCSA task. You need to know the exact steps because you won't have internet access during the exam:

```
Step-by-step root password reset:

1. Reboot the system
2. At the GRUB menu, press 'e' to edit the boot entry
3. Find the line starting with 'linux' 
4. Append: rd.break
5. Press Ctrl+X to boot
6. At the switch_root prompt:

   mount -o remount,rw /sysroot
   chroot /sysroot
   passwd root
   touch /.autorelabel
   exit
   exit

7. System reboots with new root password
```

The `touch /.autorelabel` step is critical when SELinux is enforcing — without it, the password change won't stick because the SELinux context on `/etc/shadow` will be wrong.

#### Managing Processes

```bash
# Find processes consuming the most CPU
top -bn1 | head -20

# Kill a process by PID
kill -9 <PID>

# Find and kill a process by name (find PID first)
ps aux | grep "process_name"
kill <PID>

# Change process priority
nice -n 10 command
renice -n 5 -p <PID>
```

### Configuring Local Storage

#### Partitioning with fdisk and gdisk

```bash
# List existing partitions
lsblk
fdisk -l

# Create a new partition (interactive)
fdisk /dev/sdb
# n (new), p (primary), accept defaults or set size, w (write)

# For GPT partitions
gdisk /dev/sdb
```

#### LVM (Logical Volume Management)

LVM tasks appear on almost every RHCSA exam. Know these commands cold:

```bash
# Create a physical volume
pvcreate /dev/sdb1

# Create a volume group
vgcreate myvg /dev/sdb1

# Create a logical volume (500MB)
lvcreate -L 500M -n mylv myvg

# Format the logical volume
mkfs.xfs /dev/myvg/mylv

# Mount it
mkdir /mnt/mydata
mount /dev/myvg/mylv /mnt/mydata

# Make it persistent in /etc/fstab
echo "/dev/myvg/mylv /mnt/mydata xfs defaults 0 0" >> /etc/fstab

# Extend a logical volume and resize the filesystem
lvextend -L +200M /dev/myvg/mylv
xfs_growfs /mnt/mydata          # for xfs
# or
resize2fs /dev/myvg/mylv        # for ext4
```

#### Swap Space

```bash
# Create a swap partition or file
dd if=/dev/zero of=/swapfile bs=1M count=512
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Make persistent
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab

# Verify
swapon --show
free -h
```

### Managing Users and Groups

```bash
# Create a user with specific UID and home directory
useradd -u 1500 -d /home/jsmith -s /bin/bash jsmith

# Set password
passwd jsmith

# Create a group
groupadd developers

# Add user to supplementary group
usermod -aG developers jsmith

# Configure password aging
chage -M 90 -W 7 -I 14 jsmith

# View password aging info
chage -l jsmith

# Configure sudo access
visudo
# Add: jsmith ALL=(ALL) NOPASSWD: ALL
```

### Managing Security

#### SELinux

SELinux questions are guaranteed on the RHCSA. Many candidates fail because they don't practice this enough:

```bash
# Check current SELinux mode
getenforce
sestatus

# Set SELinux to enforcing
setenforce 1

# Make permanent (survives reboot)
# Edit /etc/selinux/config and set SELINUX=enforcing

# View file contexts
ls -Z /var/www/html/

# Restore default context
restorecon -Rv /var/www/html/

# Change file context
semanage fcontext -a -t httpd_sys_content_t "/custom/path(/.*)?"
restorecon -Rv /custom/path

# Manage SELinux ports
semanage port -a -t http_port_t -p tcp 8888
semanage port -l | grep http

# Toggle SELinux booleans
getsebool -a | grep httpd
setsebool -P httpd_enable_homedirs on

# Troubleshoot SELinux denials
ausearch -m AVC -ts recent
sealert -a /var/log/audit/audit.log
```

#### Firewall Configuration

```bash
# Check firewall status
firewall-cmd --state

# List current rules
firewall-cmd --list-all

# Add a service permanently
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https

# Add a specific port
firewall-cmd --permanent --add-port=8080/tcp

# Reload to apply changes
firewall-cmd --reload

# Verify changes
firewall-cmd --list-all
```

### Networking

```bash
# View current network configuration
ip addr show
ip route show

# Configure a static IP using nmcli
nmcli con mod "System eth0" ipv4.addresses 192.168.1.100/24
nmcli con mod "System eth0" ipv4.gateway 192.168.1.1
nmcli con mod "System eth0" ipv4.dns "8.8.8.8 8.8.4.4"
nmcli con mod "System eth0" ipv4.method manual
nmcli con up "System eth0"

# Configure hostname
hostnamectl set-hostname server1.example.com

# Configure hostname resolution
# Edit /etc/hosts for local resolution
echo "192.168.1.50 server2.example.com server2" >> /etc/hosts
```

### Scheduling Tasks

```bash
# Create a cron job for user
crontab -e
# Add: 0 2 * * * /usr/local/bin/backup.sh

# Create a cron job that runs every 15 minutes
# */15 * * * * /path/to/script.sh

# Schedule a one-time task with at
at 3:00 PM
# at> /usr/local/bin/maintenance.sh
# at> Ctrl+D

# Manage systemd timers (modern alternative)
systemctl list-timers
```

### Managing Containers

Container management is a newer addition to the RHCSA objectives (RHEL 9):

```bash
# Log in to a container registry
podman login registry.redhat.io

# Search for images
podman search httpd

# Pull an image
podman pull registry.redhat.io/rhel9/httpd-24

# Run a container
podman run -d --name myweb -p 8080:8080 registry.redhat.io/rhel9/httpd-24

# List running containers
podman ps

# Inspect a container
podman inspect myweb

# Create a systemd service for a container (rootless)
mkdir -p ~/.config/systemd/user/
cd ~/.config/systemd/user/
podman generate systemd --name myweb --files --new
systemctl --user daemon-reload
systemctl --user enable container-myweb.service
systemctl --user start container-myweb.service

# Attach persistent storage
podman run -d --name myweb -v /host/data:/var/www/html:Z registry.redhat.io/rhel9/httpd-24
```

The `:Z` flag at the end of the volume mount tells podman to apply the correct SELinux context to the mounted directory. Forgetting this is a common mistake when SELinux is in enforcing mode.

### Practice Makes Perfect

#### Start Here (Beginner)

1. **Set up your lab:**
   - Install Rocky Linux or AlmaLinux in a virtual machine (these are free RHEL-compatible distributions that closely match the exam environment; avoid CentOS Stream as it's a rolling release that may differ from stable RHEL)
   - Give it two virtual disks (one for the OS, one for practice partitioning)
   - Allocate at least 2GB RAM

2. **Master the basics:**
   - Create users, groups, and set passwords without looking at notes
   - Practice file operations (copy, move, link, find) until they're automatic
   - Set up SSH key-based authentication between two VMs

#### Next Level (Intermediate)

3. **Storage tasks:**
   - Create partitions, physical volumes, volume groups, and logical volumes
   - Extend logical volumes and resize filesystems
   - Configure `/etc/fstab` entries and verify with `mount -a`
   - Set up swap space using both partitions and files

4. **Service management:**
   - Install and configure Apache (`httpd`)
   - Configure it to start at boot with `systemctl enable`
   - Open the correct firewall ports
   - Fix SELinux contexts for custom document roots

#### Advanced Challenges

5. **Full scenario practice:**
   - Reset the root password using the `rd.break` method
   - Configure a container to run as a systemd service
   - Set up autofs for NFS mounts
   - Configure network interfaces using `nmcli`

6. **Timed practice exam:**
   - Set a 2.5-hour timer
   - Work through all the tasks you can create from the exam objectives
   - Use only `man` pages and `--help` for reference
   - Reboot your VM at the end to verify persistence

<details>
<summary>Click for hints and tips</summary>

**Critical things that must survive a reboot:**
- `/etc/fstab` entries (use `mount -a` to test before rebooting)
- Firewall rules (always use `--permanent` flag then `--reload`)
- SELinux settings (use `-P` flag with `setsebool`)
- Systemd service enablement (`systemctl enable`)
- Network configuration changes made persistent via `nmcli`

**Time management during the exam:**
- Quickly read through all tasks first
- Do easy tasks first to bank points
- Don't spend more than 15 minutes on any single task
- If stuck, move on and come back later
- Save 10 minutes at the end to verify persistence

**Common pitfalls:**
- Forgetting `restorecon` after changing SELinux file contexts
- Using `firewall-cmd` without `--permanent`
- Not testing `/etc/fstab` with `mount -a` before rebooting
- Missing the `:Z` flag on container volume mounts with SELinux
- Not running `systemctl daemon-reload` after modifying unit files

</details>

### What's Next?

After passing the RHCSA, consider these paths:

- [RHCE Preparation](https://www.redhat.com/en/services/certification/rhce) — Focuses on Ansible automation and advanced system administration
- [Linux Certification Overview](./linux_certification_overview.md) — Compare other certification options
- [LFCS Certification Guide](./lfcs.md) — See how the Linux Foundation certification compares

### Helpful Resources

#### Official Red Hat Resources

- [RHCSA Exam Page (EX200)](https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam) — Official exam details and registration
- [RHCSA Exam Objectives](https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam?section=objectives) — Current exam objectives
- [Red Hat Training](https://www.redhat.com/en/services/training-and-certification) — Official courses (RH124, RH134)

#### Related Notes in This Repository

- [SELinux](./selinux.md) — Deep dive into SELinux configuration and troubleshooting
- [Logical Volume Management](./logical_volume_management.md) — Comprehensive LVM guide
- [Managing Users](./managing_users.md) — User and group administration
- [Firewall](./firewall.md) — Firewall configuration with firewalld
- [Services](./services.md) — Systemd service management
- [Networking](./networking.md) — Network configuration fundamentals

---

**Ready to start studying?** Set up your practice lab first, then work through each exam objective systematically. The [Linux Certification Overview](./linux_certification_overview.md) can help you confirm that RHCSA is the right choice for your career goals.

### Challenges

1. Set up a practice lab by installing a Red Hat-based distribution (such as CentOS Stream, Rocky Linux, or AlmaLinux) in a virtual machine. Create a non-root user account, configure sudo access, and verify that you can perform administrative tasks. Explain why using a Red Hat-compatible distribution is essential for RHCSA exam preparation.
2. Practice managing file permissions and ownership by creating a shared directory for a group of users. Set appropriate permissions using `chmod`, `chown`, and `chgrp`, and configure the setgid bit so that new files inherit the group ownership. Verify the configuration by creating files as different users.
3. Configure SELinux on your practice system by switching between enforcing, permissive, and disabled modes. Change the SELinux context of a file or directory, troubleshoot an SELinux denial using `ausearch` and `setsebool`, and explain why SELinux is a critical component of the RHCSA exam.
4. Create and manage LVM storage by setting up physical volumes, a volume group, and logical volumes. Practice extending a logical volume while the filesystem is mounted, and create a snapshot of a logical volume. Explain the advantages of LVM over traditional partitioning for system administrators.
5. Configure a network connection using `nmcli` or `nmtui` by setting a static IP address, gateway, and DNS server. Verify connectivity and test hostname resolution. Troubleshoot a simulated network misconfiguration and document the commands you used to resolve the issue.
6. Manage systemd services by enabling, starting, stopping, and masking services. Create a custom systemd service unit that executes a script at boot, and configure it to restart automatically on failure. Explain the differences between `enable`, `start`, `mask`, and `disable` in the context of systemd.
7. Schedule tasks using both `cron` and `at`. Create a cron job that performs a daily backup of a directory and an `at` job that runs a one-time maintenance script at a specified time. Verify that both tasks execute as expected and explain when each scheduling method is most appropriate.
8. Configure the firewall using `firewalld` by creating a custom zone, adding services and ports, and setting up rich rules to restrict access from specific IP ranges. Make the rules persistent, reload the firewall, and verify the configuration. Discuss how firewalld zones provide flexible network security management.
9. Set up autofs to automatically mount an NFS share or a local filesystem when a user accesses a specific directory. Configure the auto.master and auto.misc files, test the automount behavior, and explain the advantages of autofs over static mounts in `/etc/fstab`.
10. Simulate an RHCSA exam scenario by completing a multi-objective task under a time limit. For example, configure a web server, create user accounts with specific group memberships and password policies, set up LVM storage, configure firewall rules, and ensure SELinux is enforcing. Review your work against the RHCSA exam objectives and identify areas where you need further practice.
