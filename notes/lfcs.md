## LFCS (Linux Foundation Certified System Administrator)

The Linux Foundation Certified System Administrator (LFCS) certification validates your ability to perform core system administration tasks on a live Linux system. Like the RHCSA, it's a performance-based exam — you don't answer multiple-choice questions, you complete real tasks on a real system. What sets it apart is that you can choose your exam distribution (Ubuntu or CentOS), making it a solid choice if you work in environments that aren't Red Hat-centric.

This guide covers the exam domains, the commands and skills you need to master, and hands-on exercises that prepare you for what you'll face on exam day.

### Exam Details at a Glance

| Detail | Information |
|--------|-------------|
| **Exam Code** | LFCS |
| **Provider** | Linux Foundation |
| **Format** | Performance-based (hands-on tasks on a live system) |
| **Duration** | 2 hours |
| **Number of Tasks** | Typically 15–20 tasks |
| **Passing Score** | 66% |
| **Cost** | Approximately $395 USD (includes one free retake) |
| **Prerequisites** | None required |
| **Validity** | 3 years |
| **Distribution Choice** | Ubuntu or CentOS/RHEL (you choose at registration) |

### Exam Domains and Weights

The LFCS exam tests five major domains, each weighted differently:

```
LFCS Exam Domains (approximate weights)
├── Essential Commands                           ~25%
│   ├── Log into local and remote consoles
│   ├── Search for files
│   ├── Evaluate and compare file system features
│   ├── Compare and manipulate file content
│   ├── Use input/output redirection
│   ├── Analyze text using basic regular expressions
│   ├── Archive, backup, compress, unpack, and decompress files
│   └── Create, delete, copy, and move files and directories
├── Operation of Running Systems                 ~20%
│   ├── Boot, reboot, and shut down a system safely
│   ├── Boot or change system into different operating modes
│   ├── Install, configure, and troubleshoot bootloaders
│   ├── Diagnose and manage processes
│   ├── Locate and analyze system log files
│   ├── Schedule tasks to run at a set date and time
│   ├── Verify completion of scheduled jobs
│   ├── Update software to provide required functionality
│   └── Verify the integrity of filesystems
├── User and Group Management                    ~15%
│   ├── Create, delete, and modify local user accounts
│   ├── Create, delete, and modify local groups
│   ├── Manage system-wide environment profiles
│   ├── Manage template user environment
│   ├── Configure user resource limits
│   └── Manage user privileges (sudo)
├── Networking                                   ~15%
│   ├── Configure networking and hostname resolution
│   ├── Configure network services to start at boot
│   ├── Implement packet filtering (iptables/nftables)
│   ├── Start, stop, and check the status of network services
│   ├── Statically route IP traffic
│   └── Synchronize time using network peers
├── Service Configuration                        ~10%
│   ├── Configure a caching DNS server
│   ├── Maintain a DNS zone
│   ├── Configure email aliases
│   ├── Configure SSH servers and clients
│   ├── Restrict access to HTTP proxy servers
│   ├── Configure an IMAP and IMAPS service
│   ├── Query and modify the behavior of system services
│   ├── Configure an HTTP server
│   ├── Configure HTTP server log files
│   └── Restrict access to a web page
└── Storage Management                           ~15%
    ├── List, create, delete, and modify storage partitions
    ├── Manage and configure LVM storage
    ├── Create and configure encrypted storage
    ├── Configure systems to mount file systems on demand
    ├── Create and manage RAID devices
    ├── Create, manage, and diagnose advanced file system permissions
    ├── Setup user and group disk quotas
    └── Create and configure file systems
```

### Essential Commands

This domain carries the most weight. You need to be fast and accurate with these skills.

#### Searching for Files

```bash
# Find files by name
find / -name "*.conf" -type f 2>/dev/null

# Find files by ownership
find /home -user student

# Find files by size
find / -size +100M -type f 2>/dev/null

# Find files modified in the last 7 days
find /var -mtime -7 -type f

# Find files by permission
find / -perm 777 -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null    # find SUID files

# Locate files using the locate database
updatedb
locate httpd.conf
```

#### Comparing and Manipulating File Content

```bash
# Compare two files
diff file1.txt file2.txt
diff -u file1.txt file2.txt    # unified format (easier to read)

# Sort file contents
sort /etc/passwd
sort -t: -k3 -n /etc/passwd    # sort by UID numerically

# Remove duplicate lines
sort file.txt | uniq
sort file.txt | uniq -c         # count occurrences

# Extract columns
cut -d: -f1,3 /etc/passwd      # username and UID

# Count lines, words, characters
wc -l /etc/passwd
wc -w /var/log/syslog

# Display specific parts of files
head -20 /var/log/syslog
tail -f /var/log/syslog         # follow in real-time
sed -n '10,20p' largefile.txt   # lines 10 through 20
```

#### Text Analysis with Regular Expressions

```bash
# Basic grep patterns
grep "error" /var/log/syslog
grep -i "warning" /var/log/messages

# Extended regular expressions
grep -E "^root|^admin" /etc/passwd
grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" /var/log/auth.log

# Invert match (show lines that DON'T match)
grep -v "^#" /etc/ssh/sshd_config | grep -v "^$"

# Count matches
grep -c "Failed" /var/log/auth.log
```

#### Archiving and Compression

```bash
# Create a gzipped tar archive
tar czf backup.tar.gz /etc /home

# Create a bzip2 archive
tar cjf backup.tar.bz2 /etc /home

# Create an xz archive
tar cJf backup.tar.xz /etc /home

# Extract archives
tar xzf backup.tar.gz -C /restore/
tar xjf backup.tar.bz2
tar xJf backup.tar.xz

# List archive contents
tar tzf backup.tar.gz

# Use cpio for archiving
find /etc -name "*.conf" | cpio -o > configs.cpio
cpio -id < configs.cpio
```

### Operating Running Systems

#### Boot Targets and System Modes

```bash
# View current target
systemctl get-default

# Change default boot target
systemctl set-default multi-user.target    # no GUI
systemctl set-default graphical.target     # with GUI

# Switch target immediately
systemctl isolate rescue.target
systemctl isolate emergency.target

# View available targets
systemctl list-units --type=target
```

#### Process Management

```bash
# View processes with details
ps aux
ps -ef

# Real-time process monitoring
top
htop    # if installed

# Find a specific process
ps aux | grep nginx
pgrep -a nginx

# Check process resource usage
ps -o pid,ppid,cmd,%mem,%cpu --sort=-%mem | head

# Send signals to processes
kill -15 <PID>      # graceful termination (SIGTERM)
kill -9 <PID>       # forced termination (SIGKILL)

# Background and foreground jobs
command &           # run in background
jobs                # list background jobs
fg %1               # bring job 1 to foreground
bg %1               # resume job 1 in background
```

#### Log File Management

```bash
# View system logs (systemd journal)
journalctl
journalctl -u sshd                # logs for specific service
journalctl --since "1 hour ago"
journalctl -p err                  # only error-level messages
journalctl -f                      # follow new entries

# Traditional log files
tail -f /var/log/syslog            # Debian/Ubuntu
tail -f /var/log/messages          # CentOS/RHEL

# Make journal persistent across reboots
mkdir -p /var/log/journal
systemctl restart systemd-journald
```

#### Software Management

The commands differ based on your chosen distribution:

```bash
# Debian/Ubuntu (apt)
apt update
apt install nginx
apt remove nginx
apt search "web server"
apt list --installed

# CentOS/RHEL (dnf/yum)
dnf update
dnf install httpd
dnf remove httpd
dnf search "web server"
dnf list installed
```

### User and Group Management

```bash
# Create a user with specific properties
useradd -m -s /bin/bash -G developers,sudo jsmith
passwd jsmith

# Modify existing user
usermod -aG docker jsmith         # add to group
usermod -s /bin/zsh jsmith        # change shell
usermod -L jsmith                 # lock account
usermod -U jsmith                 # unlock account

# Delete a user and their home directory
userdel -r jsmith

# Create and manage groups
groupadd developers
groupmod -n devs developers       # rename group
groupdel devs

# Configure password aging
chage -M 90 -W 14 -I 7 jsmith
chage -l jsmith                   # view aging info

# Configure sudo access
visudo
# Add: jsmith ALL=(ALL) ALL
# Or:  %developers ALL=(ALL) NOPASSWD: ALL
```

#### User Resource Limits

```bash
# View current limits
ulimit -a

# Set limits in /etc/security/limits.conf
# <domain>  <type>  <item>  <value>
# student   soft    nproc   100
# student   hard    nproc   150
# @developers soft  nofile  4096
```

#### Skeleton Directory

Files in `/etc/skel/` are copied to every new user's home directory:

```bash
# Add a default .bashrc customization for all new users
echo 'alias ll="ls -la"' >> /etc/skel/.bashrc

# Add default directories
mkdir -p /etc/skel/{Documents,Projects,Scripts}

# New users created after this will get these files automatically
useradd -m newuser
ls -la /home/newuser/    # will contain the skeleton files
```

### Networking

#### Network Configuration

```bash
# View network interfaces and addresses
ip addr show
ip link show

# Configure a static IP (using nmcli on CentOS/RHEL)
nmcli con mod "eth0" ipv4.addresses 192.168.1.100/24
nmcli con mod "eth0" ipv4.gateway 192.168.1.1
nmcli con mod "eth0" ipv4.dns "8.8.8.8"
nmcli con mod "eth0" ipv4.method manual
nmcli con up "eth0"

# Configure using netplan (Ubuntu)
# Edit /etc/netplan/01-netcfg.yaml
# Then apply:
netplan apply

# Configure hostname
hostnamectl set-hostname myserver.example.com

# Hostname resolution
# Edit /etc/hosts
echo "192.168.1.50 dbserver.example.com dbserver" >> /etc/hosts

# View routing table
ip route show

# Add a static route
ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0

# Make static route persistent (CentOS/RHEL)
nmcli con mod "eth0" +ipv4.routes "10.0.0.0/8 192.168.1.1"
```

#### Packet Filtering

```bash
# Using firewalld (CentOS/RHEL)
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-port=8443/tcp
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" service name="ssh" accept'
firewall-cmd --reload
firewall-cmd --list-all

# Using ufw (Ubuntu)
ufw enable
ufw allow ssh
ufw allow 80/tcp
ufw allow from 10.0.0.0/8 to any port 22
ufw status verbose

# Using iptables directly
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -s 10.0.0.0/8 -p tcp --dport 22 -j ACCEPT
iptables -L -n -v
```

#### Time Synchronization

```bash
# Check current time settings
timedatectl

# Enable NTP synchronization
timedatectl set-ntp true

# Configure NTP server (using chronyd)
# Edit /etc/chrony.conf or /etc/chrony/chrony.conf
# Add: server ntp.example.com iburst
systemctl restart chronyd

# Verify synchronization
chronyc sources
chronyc tracking
```

### Storage Management

#### Partition Management

```bash
# List block devices and partitions
lsblk
fdisk -l

# Create a partition (MBR)
fdisk /dev/sdb
# Commands: n (new), p (primary), enter defaults, w (write)

# Create a partition (GPT)
gdisk /dev/sdb
# Or use parted:
parted /dev/sdb mklabel gpt
parted /dev/sdb mkpart primary xfs 1MiB 500MiB

# Create a filesystem
mkfs.xfs /dev/sdb1
mkfs.ext4 /dev/sdb2
```

#### LVM Management

```bash
# Create physical volumes
pvcreate /dev/sdb1 /dev/sdc1

# Create a volume group
vgcreate datavg /dev/sdb1 /dev/sdc1

# Create logical volumes
lvcreate -L 1G -n datalv datavg
lvcreate -l 100%FREE -n loglv datavg    # use all remaining space

# Create filesystem and mount
mkfs.xfs /dev/datavg/datalv
mkdir /mnt/data
mount /dev/datavg/datalv /mnt/data

# Add to /etc/fstab for persistence
echo "/dev/datavg/datalv /mnt/data xfs defaults 0 0" >> /etc/fstab
mount -a    # test the fstab entry

# Extend a logical volume
lvextend -L +500M /dev/datavg/datalv
xfs_growfs /mnt/data               # for xfs
# resize2fs /dev/datavg/datalv     # for ext4

# Display LVM information
pvdisplay
vgdisplay
lvdisplay
```

#### Encrypted Storage with LUKS

```bash
# Create an encrypted partition
cryptsetup luksFormat /dev/sdb1
# You'll be prompted for a passphrase

# Open the encrypted device
cryptsetup open /dev/sdb1 secret_data

# Create a filesystem on the encrypted device
mkfs.ext4 /dev/mapper/secret_data

# Mount it
mkdir /mnt/secure
mount /dev/mapper/secret_data /mnt/secure

# Close when done
umount /mnt/secure
cryptsetup close secret_data
```

#### RAID Management

```bash
# Create a RAID 1 array (mirror)
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

# Check RAID status
cat /proc/mdstat
mdadm --detail /dev/md0

# Create filesystem on RAID device
mkfs.xfs /dev/md0

# Save RAID configuration
mdadm --detail --scan >> /etc/mdadm/mdadm.conf    # Debian/Ubuntu
mdadm --detail --scan >> /etc/mdadm.conf           # CentOS/RHEL
```

#### Disk Quotas

```bash
# Enable quotas on a filesystem
# Add usrquota,grpquota to mount options in /etc/fstab
# Example: /dev/sdb1 /data ext4 defaults,usrquota,grpquota 0 0

# Remount and initialize quotas
mount -o remount /data
quotacheck -cugm /data
quotaon /data

# Set quota for a user (soft/hard limits)
edquota -u jsmith
# Or set directly:
setquota -u jsmith 100M 120M 0 0 /data

# View quota usage
quota -u jsmith
repquota -a
```

### Service Configuration

#### SSH Server Configuration

```bash
# Edit SSH configuration
vi /etc/ssh/sshd_config

# Common security settings:
# PermitRootLogin no
# PasswordAuthentication yes
# PubkeyAuthentication yes
# Port 2222

# Restart to apply changes
systemctl restart sshd

# Set up key-based authentication
ssh-keygen -t ed25519
ssh-copy-id user@remote_server
```

#### HTTP Server Configuration

```bash
# Install and start Apache
# Ubuntu/Debian:
apt install apache2
systemctl enable --now apache2

# CentOS/RHEL:
dnf install httpd
systemctl enable --now httpd

# Create a virtual host (Apache on CentOS)
cat > /etc/httpd/conf.d/mysite.conf << 'EOF'
<VirtualHost *:80>
    ServerName mysite.example.com
    DocumentRoot /var/www/mysite
    <Directory /var/www/mysite>
        AllowOverride None
        Require all granted
    </Directory>
    ErrorLog /var/log/httpd/mysite-error.log
    CustomLog /var/log/httpd/mysite-access.log combined
</VirtualHost>
EOF

mkdir -p /var/www/mysite
echo "<h1>Welcome</h1>" > /var/www/mysite/index.html
systemctl restart httpd

# Open firewall
firewall-cmd --permanent --add-service=http
firewall-cmd --reload
```

### Ubuntu vs CentOS: Key Differences

Since you choose your distribution at registration, know the differences that matter:

| Task | Ubuntu/Debian | CentOS/RHEL |
|------|---------------|-------------|
| Package install | `apt install` | `dnf install` |
| Package search | `apt search` | `dnf search` |
| Service management | `systemctl` (same) | `systemctl` (same) |
| Firewall tool | `ufw` | `firewall-cmd` |
| Web server package | `apache2` | `httpd` |
| Network config | `netplan` / `nmcli` | `nmcli` |
| SELinux/AppArmor | AppArmor (default) | SELinux (default) |
| Default filesystem | ext4 | xfs |
| Config location | `/etc/apache2/` | `/etc/httpd/` |
| Log location | `/var/log/syslog` | `/var/log/messages` |

### Practice Makes Perfect

#### Start Here (Beginner)

I. **Set up your lab:**

- Install your chosen distribution in a virtual machine (for CentOS/RHEL, use Rocky Linux or AlmaLinux since traditional CentOS has reached end-of-life; for Ubuntu, use the latest LTS release)
- Add a second virtual disk for storage practice
- Allocate at least 2GB RAM and 2 CPUs

II. **Master essential commands:**

- Practice `find`, `grep`, `sort`, `cut`, `wc`, and `diff` until they're second nature
- Work through file archiving with `tar` (create, extract, list) using all compression types
- Practice input/output redirection in realistic scenarios

#### Next Level (Intermediate)

III. **System administration tasks:**

- Create users with specific properties (UID, shell, groups, home directory)
- Configure password aging policies
- Set up cron jobs and verify they execute correctly
- Practice log analysis using `journalctl` with various filters

IV. **Networking and services:**

- Configure static IP addresses using the tools for your chosen distribution
- Set up SSH key-based authentication
- Install and configure Apache with custom virtual hosts
- Configure firewall rules to allow and deny specific traffic

#### Advanced Challenges

V. **Storage challenges:**

- Create a complete LVM setup from scratch (PV → VG → LV → filesystem → mount → fstab)
- Set up LUKS-encrypted storage
- Configure disk quotas for users
- Build a RAID 1 array and verify it works correctly

VI. **Timed practice exam:**

- Set a 2-hour timer
- Work through a mix of tasks from all exam domains
- Use only man pages and built-in help (no internet)
- Reboot your VM to verify all changes are persistent

<details>
<summary>Click for hints and tips</summary>

**Choosing Ubuntu vs CentOS for the exam:**

- Pick whichever you use most often in your daily work
- Ubuntu is more common in cloud environments and development
- CentOS/RHEL is more common in enterprise data centers
- If you have no preference, CentOS aligns well with RHCSA prep if you plan to pursue that later

**Exam strategy:**

- The LFCS gives you 2 hours for 15–20 tasks, so pace yourself
- Read each task fully before starting to work on it
- Handle quick tasks first, then tackle complex ones
- Use `man` pages aggressively — they contain answers to most questions
- Verify persistence by checking `/etc/fstab`, enabled services, and reboot behavior

**Common mistakes:**

- Forgetting to make changes persistent (fstab, firewall, service enable)
- Mixing up Ubuntu and CentOS commands under pressure
- Not reading task requirements carefully (e.g., specific mount options or user properties)
- Skipping filesystem verification with `mount -a` or `fstab` syntax checks
- Forgetting to restart services after configuration changes

**Useful exam shortcuts:**

- `man -k keyword` to find relevant commands
- `systemctl list-unit-files | grep enabled` to check enabled services
- `lsblk` for a quick overview of disk layout
- `ss -tlnp` to see listening ports and associated processes

</details>

### What's Next?

After earning the LFCS, consider advancing your career with:

- [LFCE (Linux Foundation Certified Engineer)](https://training.linuxfoundation.org/certification/linux-foundation-certified-engineer-lfce/) — Advanced Linux engineering topics
- [Linux Certification Overview](https://github.com/djeada/Linux-Notes/blob/main/notes/linux_certification_overview.md) — Compare all certification options
- [RHCSA Certification Guide](https://github.com/djeada/Linux-Notes/blob/main/notes/rhcsa.md) — Add a Red Hat certification to your credentials

### Helpful Resources

#### Official Linux Foundation Resources

- [LFCS Certification Page](https://training.linuxfoundation.org/certification/linux-foundation-certified-sysadmin-lfcs/) — Official exam information and registration
- [LFCS Exam Domains](https://training.linuxfoundation.org/certification/linux-foundation-certified-sysadmin-lfcs/#domains) — Current exam objectives
- [Linux Foundation Training](https://training.linuxfoundation.org/) — Official preparation courses

#### Related Notes in This Repository

- [Commands](https://github.com/djeada/Linux-Notes/blob/main/notes/commands.md) — Essential Linux commands reference
- [Permissions](https://github.com/djeada/Linux-Notes/blob/main/notes/permissions.md) — File permissions and ownership
- [Logical Volume Management](https://github.com/djeada/Linux-Notes/blob/main/notes/logical_volume_management.md) — Complete LVM guide
- [Networking](https://github.com/djeada/Linux-Notes/blob/main/notes/networking.md) — Network configuration fundamentals
- [Firewall](https://github.com/djeada/Linux-Notes/blob/main/notes/firewall.md) — Firewall configuration
- [Managing Users](https://github.com/djeada/Linux-Notes/blob/main/notes/managing_users.md) — User and group administration
- [Processes](https://github.com/djeada/Linux-Notes/blob/main/notes/processes.md) — Process management
- [Cron Jobs](https://github.com/djeada/Linux-Notes/blob/main/notes/cron_jobs.md) — Task scheduling
- [Grep](https://github.com/djeada/Linux-Notes/blob/main/notes/grep.md) — Text searching with regular expressions
- [SSH and SCP](https://github.com/djeada/Linux-Notes/blob/main/notes/ssh_and_scp.md) — Secure remote access

**Ready to start studying?** Set up your practice lab with your chosen distribution, then work through each exam domain systematically. The [Linux Certification Overview](https://github.com/djeada/Linux-Notes/blob/main/notes/linux_certification_overview.md) can help you confirm that LFCS is the right choice for your goals.

### Challenges

1. Set up a practice lab environment by installing a Linux distribution (such as Ubuntu or CentOS) in a virtual machine. Configure the system with a non-root user account, set up sudo access, and verify that you can perform administrative tasks. Document the steps you followed and explain why using a dedicated lab is important for exam preparation.
2. Practice essential command-line operations by creating a directory structure, copying and moving files between directories, and using tools like `find`, `grep`, and `tar` to search for and archive files. Time yourself to simulate exam conditions and identify areas where you need more practice.
3. Configure a local filesystem by creating a new partition, formatting it with a filesystem (such as ext4 or xfs), and mounting it at a specific mount point. Make the mount persistent across reboots by editing `/etc/fstab` and verify the configuration after a reboot.
4. Set up and manage Logical Volume Manager (LVM) by creating physical volumes, a volume group, and logical volumes. Practice extending and reducing logical volumes, and explain how LVM provides flexibility compared to traditional partitioning.
5. Configure network settings on your practice system by assigning a static IP address, setting up DNS resolution, and verifying connectivity using `ping`, `ip`, and `ss`. Troubleshoot a simulated network issue (such as an incorrect gateway) and document the resolution steps.
6. Create and manage user accounts and groups. Set up password policies, configure account expiration, and assign users to specific groups with appropriate file permissions. Verify that file access behaves as expected for users in different groups.
7. Schedule automated tasks using cron and systemd timers. Create a cron job that backs up a directory at regular intervals and a systemd timer that runs a cleanup script. Compare the two approaches and explain when each is most appropriate.
8. Configure a basic firewall using either `iptables` or `firewalld`. Set up rules to allow SSH and HTTP traffic while blocking all other incoming connections. Test the configuration by attempting to connect on allowed and blocked ports, and make the rules persistent across reboots.
9. Practice managing system services with `systemctl`. Enable, start, stop, and check the status of services. Create a custom systemd service unit that runs a simple script, and configure it to start automatically at boot.
10. Simulate an exam scenario by completing a multi-step task under a time limit, such as setting up a web server, configuring firewall rules, creating user accounts with specific permissions, and scheduling a backup job. Review your work against the LFCS exam objectives and identify areas for improvement.
