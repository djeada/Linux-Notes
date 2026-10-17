## NFS: Network File System

NFS stands for Network File System.

It is a protocol that allows one computer to share directories with other computers over a network.

The important idea is:

```text
A remote directory can appear like a local directory.
```

For example, a server may export:

```text
/opt/shared
```

A client may mount it at:

```text
/mnt/nfs_shared
```

Then users on the client can access remote files as if they were local:

```bash
ls /mnt/nfs_shared
```

### Big Picture

NFS has two main sides:

- NFS server    shares directories
- NFS client    mounts and uses those directories

Diagram:

```text
Client                       Network                      Server
+--------+                                            +--------+
| User   |    file open/read/write requests           | NFS    |
| Space  |  <------------------------------->         | Server |
+--------+                                            +--------+
    |                                                     |
+--------+                                            +--------+
| NFS    |                                            | NFS    |
| Client |                                            | Daemon |
+--------+                                            +--------+
    |                                                     |
+--------+                                            +--------+
| Mount  |                                            | Local  |
| Point  |                                            | Export |
+--------+                                            +--------+
    |                                                     |
+--------+                                            +--------+
| Apps   |                                            | Disk   |
+--------+                                            +--------+
```

When a client reads or writes a file under the NFS mount point, the NFS client code sends network requests to the server.

The server receives those requests and performs file operations on its own local filesystem.

### Why Use NFS?

NFS is useful when several systems need shared access to files.

Common reasons include:

- centralized storage
- shared home directories
- shared project directories
- cluster storage
- application data sharing
- backup centralization
- reduced duplicate files
- consistent permissions
- remote access to common files

Example use cases:

- Several Linux servers need the same software directory.
- Multiple users need shared project files.
- A lab needs shared home directories.
- A compute cluster needs central storage.
- A backup server exports restore data.

NFS is common in Linux and Unix environments, but clients also exist for macOS and Windows.

### NFS Server and Client Roles

The NFS server owns and exports the real directory.

- Server:
  - real directory exists on server disk
  - example: /opt/shared

The NFS client mounts that exported directory.

- Client:
  - remote directory appears at local mount point
  - example: /mnt/nfs_shared

Diagram:

```text
Server filesystem:
/
└── opt
    └── shared
        ├── file1.txt
        └── file2.txt

Client filesystem:
/
└── mnt
    └── nfs_shared
        ├── file1.txt
        └── file2.txt
```

The files are physically stored on the server, but visible through the client mount point.

### Important NFS Components

Common NFS-related components include:

- nfs-server       server-side NFS service
- rpcbind          maps RPC services to network ports
- mountd           handles mount requests for older NFS versions
- idmapd           maps user and group names for NFSv4
- exportfs         manages exported directories
- /etc/exports     server export configuration
- /etc/fstab       client persistent mount configuration

NFSv3 often depends on several RPC services and ports.

NFSv4 simplifies firewalling because it mainly uses TCP port 2049.

### NFS Versions

NFS has several versions.

### NFSv2

NFSv2 is old and rarely used today.

Limitations include:

- older design
- limited file size support
- usually UDP-based
- weaker performance and features

### NFSv3

NFSv3 is still widely used.

It introduced improvements such as:

- large file support
- better error reporting
- asynchronous writes
- TCP and UDP support
- better performance than NFSv2

NFSv3 is stable and common, but it often requires more firewall considerations because supporting services may use multiple ports.

### NFSv4

NFSv4 is newer and usually preferred for modern environments.

Advantages include:

- stateful protocol
- single main TCP port, 2049
- better firewall behavior
- Kerberos support
- ACL support
- compound operations
- improved security options
- better cross-platform design

For secure or enterprise environments, NFSv4 with Kerberos is often preferred.

### Basic Server Setup

The NFS server needs:

- NFS utilities installed
- a directory to export
- an /etc/exports entry
- NFS services running
- firewall rules allowing NFS traffic

The basic flow is:

1. Install NFS packages
2. Create shared directory
3. Set ownership and permissions
4. Edit /etc/exports
5. Apply exports with exportfs
6. Start and enable NFS service
7. Open firewall
8. Verify export

### Installing NFS Packages

On RHEL, CentOS, Rocky, AlmaLinux, or Fedora-style systems:

```bash
sudo dnf install nfs-utils
```

On older CentOS 7 systems:

```bash
sudo yum install nfs-utils
```

On Debian or Ubuntu systems:

```bash
sudo apt install nfs-kernel-server nfs-common
```

Package names vary slightly by distribution, but the main idea is the same:

- server needs NFS server tools
- client needs NFS client tools

### Creating a Shared Directory

Example server directory:

```bash
sudo mkdir -p /opt/shared
```

Add a test file:

```bash
echo "hello from NFS server" | sudo tee /opt/shared/hello.txt
```

Set ownership and permissions based on your use case.

For a simple lab:

```bash
sudo chmod 755 /opt/shared
```

For a shared writable directory, you may use a group:

```bash
sudo groupadd nfsusers
sudo chgrp nfsusers /opt/shared
sudo chmod 2775 /opt/shared
```

The `2` in `2775` sets the setgid bit so new files tend to inherit the directory group.

### `/etc/exports`

The server uses `/etc/exports` to define what directories are shared and who can access them.

Example:

```exports
/opt/shared 192.168.1.0/24(rw,sync,root_squash)
```

Meaning:

- /opt/shared       directory being exported
- 192.168.1.0/24    allowed client network
- rw                read-write access
- sync              write changes safely before replying
- root_squash       map client root to unprivileged user

A more restrictive example:

```exports
/opt/shared 192.168.1.50(ro,sync,root_squash)
```

This allows only one client and gives read-only access.

### Common Export Options

- ro              read-only
- rw              read-write
- sync            commit changes before replying
- async           allow delayed writes for performance
- root_squash     map client root to anonymous user
- no_root_squash  allow client root to act as root on server
- all_squash      map all users to anonymous user
- no_all_squash   preserve normal user IDs
- subtree_check   check file location within exported tree
- no_subtree_check skip subtree checks, common for reliability/performance

A common safe default:

```exports
/opt/shared 192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
```

Important warning:

- Avoid no_root_squash unless you truly need it.
- It gives root on the client powerful access to the exported directory.

### Applying Export Changes

After editing `/etc/exports`, apply changes with:

```bash
sudo exportfs -r
```

View exports:

```bash
sudo exportfs -v
```

Example output:

```text
/opt/shared  192.168.1.0/24(sync,wdelay,hide,no_subtree_check,sec=sys,rw,root_squash,no_all_squash)
```

Interpretation:

- The server exports /opt/shared to clients in 192.168.1.0/24.
- The export is read-write.
- root_squash is enabled.

### Starting NFS Services

On systemd systems:

```bash
sudo systemctl enable --now nfs-server
```

Check status:

```bash
systemctl status nfs-server
```

Example output:

```text
● nfs-server.service - NFS server and services
     Loaded: loaded
     Active: active (exited)
```

Interpretation:

- The service is active.
- For NFS, active (exited) can be normal because systemd started the required kernel NFS services.

On older setups, you may also see or manage:

```bash
sudo systemctl enable --now rpcbind
sudo systemctl enable --now nfs-idmapd
```

### Firewall Rules for NFS

For NFSv4, TCP port 2049 is the main port.

For NFSv3, additional RPC services such as mountd and rpcbind may be needed.

With firewalld:

```bash
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --permanent --add-service=mountd
sudo firewall-cmd --permanent --add-service=rpc-bind
sudo firewall-cmd --reload
```

Check:

```bash
sudo firewall-cmd --list-services
```

Example output:

```text
ssh dhcpv6-client nfs mountd rpc-bind
```

Interpretation:

- The firewall allows NFS-related services.
- Clients should be able to reach the NFS server if routing and exports are correct.

With UFW, a simple NFSv4 example:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 2049 proto tcp
```

### Client Setup

The NFS client needs:

- NFS client utilities
- a local mount point
- network access to the server
- permission from the server export
- mount command or /etc/fstab entry

Install packages.

RHEL-style:

```bash
sudo dnf install nfs-utils
```

Debian/Ubuntu:

```bash
sudo apt install nfs-common
```

Create mount point:

```bash
sudo mkdir -p /mnt/nfs_shared
```

Mount:

```bash
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

For NFSv4 explicitly:

```bash
sudo mount -t nfs4 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Check:

```bash
mount | grep nfs
```

Example output:

```text
192.168.1.100:/opt/shared on /mnt/nfs_shared type nfs4 (rw,relatime,vers=4.2,addr=192.168.1.100)
```

Interpretation:

- The NFS share is mounted.
- The client is using NFS version 4.2.
- The mount is read-write.

### Verifying the NFS Mount

List files:

```bash
ls -l /mnt/nfs_shared
```

Example output:

```text
-rw-r--r-- 1 root root 22 Jun 1 12:00 hello.txt
```

Read the test file:

```bash
cat /mnt/nfs_shared/hello.txt
```

Example output:

```text
hello from NFS server
```

Create a file if write access is allowed:

```bash
touch /mnt/nfs_shared/client-test.txt
```

If this works, the mount is writable for your user.

If it fails with permission denied, check Unix permissions, UID/GID mapping, root squashing, and export options.

### Persistent NFS Mounts with `/etc/fstab`

To mount automatically at boot, add an entry on the client.

Example:

```fstab
192.168.1.100:/opt/shared /mnt/nfs_shared nfs defaults,_netdev 0 0
```

For NFSv4:

```fstab
192.168.1.100:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev 0 0
```

Important option:

```text
_netdev means this mount depends on the network.
```

For systems where the NFS server may not always be available, consider:

```fstab
192.168.1.100:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev,nofail,x-systemd.automount 0 0
```

Meaning:

- nofail              do not fail boot if the mount is unavailable
- x-systemd.automount mount on first access instead of immediately at boot

Test fstab:

```bash
sudo mount -a
```

Check:

```bash
findmnt /mnt/nfs_shared
```

### UID and GID Mapping

NFS permissions are based heavily on numeric user IDs and group IDs.

This is a major concept.

Linux file ownership is stored as numbers:

- UID = user ID
- GID = group ID

Example:

```bash
id alice
```

Output:

```text
uid=1000(alice) gid=1000(alice) groups=1000(alice)
```

If Alice has UID 1000 on the client but UID 2000 on the server, permissions may not behave as expected.

- Client thinks alice = UID 1000
- Server thinks alice = UID 2000

- NFS sends numeric UID 1000.
- Server checks permissions for UID 1000.

This can cause:

- unexpected permission denied
- wrong file ownership
- accidental access by the wrong user
- confusing ls -l output

### Strategies for UID and GID Consistency

Common strategies include:

- centralized identity through LDAP, FreeIPA, or Active Directory
- consistent manual UID/GID assignment
- NFSv4 id mapping
- Kerberos-based NFSv4 authentication

In small labs, manually matching UIDs may be enough.

In larger environments, use centralized identity management.

### NFSv4 and `idmapd`

NFSv4 can use name-based identity mapping through `idmapd`.

The client and server should use the same domain in:

```text
/etc/idmapd.conf
```

Example:

```conf
[General]
Domain = example.com
```

Restart relevant services after changes.

Example:

```bash
sudo systemctl restart nfs-idmapd
sudo systemctl restart nfs-server
```

Check identity mapping issues if files appear owned by:

- nobody
- nfsnobody
- 4294967294

These often indicate mapping problems.

### Root Squashing

Root squashing protects the server from root users on clients.

With `root_squash`, a request from UID 0 on the client is mapped to an anonymous user on the server.

```text
Client root UID 0
      |
      v
NFS server maps it to anonymous user
      |
      v
Usually nfsnobody or nobody
```

This prevents client root from automatically having root privileges on the server export.

Example export:

```exports
/opt/shared 192.168.1.0/24(rw,sync,root_squash)
```

Dangerous option:

```exports
/opt/shared 192.168.1.0/24(rw,sync,no_root_squash)
```

Use `no_root_squash` only in carefully controlled environments.

### `all_squash`

The `all_squash` option maps all client users to the anonymous user.

Example:

```exports
/opt/public 192.168.1.0/24(rw,sync,all_squash)
```

This can be useful for simple public drop-box style shares where all access should use one server-side identity.

Common related options:

- anonuid=UID
- anongid=GID

Example:

```exports
/opt/public 192.168.1.0/24(rw,sync,all_squash,anonuid=2000,anongid=2000)
```

This maps all access to UID 2000 and GID 2000.

### Security Considerations

NFS is powerful, but it must be configured carefully.

Good practices:

- export only needed directories
- allow only trusted client IPs or subnets
- use read-only exports where possible
- avoid no_root_squash unless necessary
- use firewall rules to restrict access
- prefer NFSv4 for simpler firewalling
- use Kerberos for stronger authentication where needed
- do not expose NFS directly to the public internet
- use VPN or private networks for remote access

A safe export is usually specific:

```exports
/srv/project 192.168.10.0/24(rw,sync,root_squash,no_subtree_check)
```

A risky export is broad:

```exports
/  *(rw,no_root_squash)
```

Avoid broad exports like that.

### Performance Considerations

NFS performance depends on:

- network latency
- network bandwidth
- server disk speed
- client caching
- NFS version
- mount options
- read/write sizes
- sync vs async exports
- workload pattern

Common mount options include:

- rsize     read buffer size
- wsize     write buffer size
- hard      retry indefinitely on server failure
- soft      fail after timeout
- timeo     timeout value
- retrans   retry count

Example:

```bash
sudo mount -t nfs -o rsize=8192,wsize=8192 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Modern systems often negotiate good defaults automatically. Tune only after measuring.

Important safety note:

- async can improve performance but may risk data loss if the server crashes before data is safely written.
- sync is safer but can be slower.

### Managing Exports with `exportfs`

View exports:

```bash
sudo exportfs -v
```

Reload exports:

```bash
sudo exportfs -r
```

Unexport one directory:

```bash
sudo exportfs -u 192.168.1.0/24:/opt/shared
```

Unexport all:

```bash
sudo exportfs -ua
```

Re-export all from `/etc/exports`:

```bash
sudo exportfs -a
```

### Scenario 1: Create a Basic NFS Share

Set up a server export and mount it from a client.

#### Server Steps

Install packages:

```bash
sudo dnf install nfs-utils
```

Create directory:

```bash
sudo mkdir -p /opt/shared
echo "hello from server" | sudo tee /opt/shared/hello.txt
sudo chmod 755 /opt/shared
```

Edit `/etc/exports`:

```exports
/opt/shared 192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
```

Apply:

```bash
sudo exportfs -r
sudo systemctl enable --now nfs-server
sudo exportfs -v
```

Example output:

```text
/opt/shared 192.168.1.0/24(sync,wdelay,no_subtree_check,sec=sys,rw,root_squash,no_all_squash)
```

#### Client Steps

Install client tools:

```bash
sudo dnf install nfs-utils
```

Create mount point:

```bash
sudo mkdir -p /mnt/nfs_shared
```

Mount:

```bash
sudo mount -t nfs4 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Check:

```bash
findmnt /mnt/nfs_shared
cat /mnt/nfs_shared/hello.txt
```

Example output:

```text
hello from server
```

Interpretation:

- The server exported the directory.
- The client mounted it successfully.
- The client can read files stored on the server.

### Scenario 2: Simulate “Access Denied by Server”

Show what happens when the client IP is not allowed by `/etc/exports`.

#### Simulate Problem

On the server, restrict the export to the wrong network:

```exports
/opt/shared 10.10.10.0/24(rw,sync,root_squash)
```

Apply:

```bash
sudo exportfs -r
```

On the client:

```bash
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Example output:

```text
mount.nfs: access denied by server while mounting 192.168.1.100:/opt/shared
```

#### Check on Server

```bash
sudo exportfs -v
```

Example output:

```text
/opt/shared 10.10.10.0/24(rw,sync,root_squash)
```

Interpretation:

- The server is exporting the directory only to 10.10.10.0/24.
- The client is not in that allowed range.
- The server rejects the mount request.

#### Fix

Use the correct client subnet or IP:

```exports
/opt/shared 192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
```

Apply:

```bash
sudo exportfs -r
```

### Scenario 3: Simulate NFS Blocked by Firewall

Diagnose when the export is correct but the client cannot reach NFS services.

#### Simulate Problem

On the server, remove NFS firewall services:

```bash
sudo firewall-cmd --permanent --remove-service=nfs
sudo firewall-cmd --permanent --remove-service=mountd
sudo firewall-cmd --permanent --remove-service=rpc-bind
sudo firewall-cmd --reload
```

On the client:

```bash
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Possible output:

```text
mount.nfs: Connection timed out
```

#### Check Connectivity

```bash
nc -vz 192.168.1.100 2049
```

Example output:

```text
nc: connect to 192.168.1.100 port 2049 (tcp) timed out
```

#### Check Server Firewall

```bash
sudo firewall-cmd --list-services
```

Example output:

```text
ssh dhcpv6-client
```

Interpretation:

- The NFS export may be correct.
- The server firewall is blocking NFS traffic.
- The client cannot reach port 2049.

#### Fix

```bash
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --permanent --add-service=mountd
sudo firewall-cmd --permanent --add-service=rpc-bind
sudo firewall-cmd --reload
```

Retest:

```bash
nc -vz 192.168.1.100 2049
```

Expected:

```text
Connection to 192.168.1.100 2049 port [tcp/nfs] succeeded!
```

### Scenario 4: Simulate Permission Denied from UID/GID Mismatch

Show why matching usernames is not enough if numeric UIDs differ.

#### Situation

On server:

```text
alice UID = 1001
```

On client:

```text
alice UID = 1002
```

The server directory is owned by UID 1001:

```bash
ls -ln /opt/shared
```

Example output on server:

```text
drwxr-x--- 2 1001 1001 4096 Jun 1 12:00 /opt/shared
```

On client, Alice tries:

```bash
touch /mnt/nfs_shared/test.txt
```

Example output:

```text
touch: cannot touch '/mnt/nfs_shared/test.txt': Permission denied
```

#### Check IDs

On client:

```bash
id alice
```

Example:

```text
uid=1002(alice) gid=1002(alice)
```

On server:

```bash
id alice
```

Example:

```text
uid=1001(alice) gid=1001(alice)
```

Interpretation:

- NFS uses numeric IDs for permission checks.
- The server receives UID 1002, not the name alice.
- The server does not treat UID 1002 as the owner of files owned by UID 1001.

#### Fix Options

- make UIDs and GIDs consistent
- use centralized identity management
- configure NFSv4 id mapping
- use controlled all_squash mapping for simple shared directories

### Scenario 5: Simulate Root Squash Behavior

Show why root on the client may not have root power on the NFS export.

#### Server Export

```exports
/opt/shared 192.168.1.0/24(rw,sync,root_squash)
```

Apply:

```bash
sudo exportfs -r
```

On client as root:

```bash
sudo touch /mnt/nfs_shared/root-created.txt
```

Possible output:

```text
touch: cannot touch '/mnt/nfs_shared/root-created.txt': Permission denied
```

Or if the directory allows anonymous writes, check ownership:

```bash
ls -ln /mnt/nfs_shared/root-created.txt
```

Example output:

```text
-rw-r--r-- 1 65534 65534 0 Jun 1 12:30 root-created.txt
```

Interpretation:

- Client root was mapped to an anonymous unprivileged user.
- This is root_squash protecting the server.
- UID 65534 often represents nobody or nfsnobody.

#### Unsafe Alternative

```exports
/opt/shared 192.168.1.0/24(rw,sync,no_root_squash)
```

Warning:

- no_root_squash allows client root to act as root on the export.
- Use only when required and only for trusted clients.

### Scenario 6: Simulate a Stale NFS File Handle

Understand what happens when the server-side exported directory changes while clients still have old references.

#### Simulate

Client mounts:

```bash
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
cd /mnt/nfs_shared
```

On the server, rename and recreate the export directory:

```bash
sudo mv /opt/shared /opt/shared.old
sudo mkdir /opt/shared
sudo exportfs -r
```

On the client:

```bash
ls
```

Possible output:

```text
ls: cannot access '.': Stale file handle
```

Interpretation:

- The client holds references to objects that no longer match the server-side export.
- The server-side directory was replaced.
- The client mount needs to be refreshed.

#### Fix

On the client:

```bash
cd /
sudo umount /mnt/nfs_shared
sudo mount /mnt/nfs_shared
```

If unmount is busy:

```bash
sudo lsof +f -- /mnt/nfs_shared
sudo fuser -vm /mnt/nfs_shared
```

Then stop the using process or move out of the directory.

### Scenario 7: Simulate Boot Hang from NFS in `/etc/fstab`

Show why NFS mounts should be configured carefully for boot.

#### Problem fstab Entry

```fstab
192.168.1.100:/opt/shared /mnt/nfs_shared nfs defaults 0 0
```

If the NFS server is down during boot, the client may wait for a long time.

#### Better Entry

```fstab
192.168.1.100:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev,nofail,x-systemd.automount 0 0
```

#### Apply

```bash
sudo systemctl daemon-reload
sudo mount -a
```

Check systemd mount units:

```bash
systemctl list-units | grep nfs_shared
```

Example output:

```text
mnt-nfs_shared.automount loaded active waiting /mnt/nfs_shared
```

Interpretation:

- The automount unit waits until the path is accessed.
- nofail prevents boot failure if the server is unavailable.
- This is safer for laptops and clients that may boot away from the NFS network.

### Scenario 8: Simulate Read-Only Export

Show how export options override client expectations.

#### Server Export

```exports
/opt/shared 192.168.1.0/24(ro,sync,root_squash)
```

Apply:

```bash
sudo exportfs -r
```

Client remount:

```bash
sudo umount /mnt/nfs_shared
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Try write:

```bash
touch /mnt/nfs_shared/test.txt
```

Example output:

```text
touch: cannot touch '/mnt/nfs_shared/test.txt': Read-only file system
```

#### Check Mount

```bash
findmnt /mnt/nfs_shared
```

Example output:

```text
TARGET          SOURCE                    FSTYPE OPTIONS
/mnt/nfs_shared 192.168.1.100:/opt/shared nfs4   ro,relatime,vers=4.2
```

Interpretation:

- The server exported the directory as read-only.
- The client cannot write, even if local commands try to create files.

### Scenario 9: Measure NFS Performance

Check whether NFS is slow and where the bottleneck may be.

#### Write Test

On the client:

```bash
dd if=/dev/zero of=/mnt/nfs_shared/testfile bs=1M count=512 conv=fdatasync
```

Example output:

```text
536870912 bytes copied, 8.2 s, 65.5 MB/s
```

#### Read Test

```bash
dd if=/mnt/nfs_shared/testfile of=/dev/null bs=1M
```

Example output:

```text
536870912 bytes copied, 4.1 s, 130 MB/s
```

#### Check Mount Stats

```bash
nfsiostat 1
```

Example output:

```text
op/s    rpc bklog
120.00  0.00

read:  avg RTT  4.0 ms   avg exe  5.0 ms
write: avg RTT 12.0 ms   avg exe 15.0 ms
```

Interpretation:

- Writes are slower than reads.
- NFS write latency is higher.
- Possible causes include sync export behavior, server disk speed, network latency, or competing workloads.

#### Other Checks

On client:

```bash
mount | grep nfs
nfsstat -c
```

On server:

```bash
nfsstat -s
iostat -xz 1
```

### Scenario 10: Troubleshoot “NFS Server Is Not Responding”

Diagnose a client that hangs or reports server not responding.

#### Symptom

Client log or terminal shows:

```text
nfs: server 192.168.1.100 not responding, still trying
```

#### Check Network

```bash
ping 192.168.1.100
```

Check NFS port:

```bash
nc -vz 192.168.1.100 2049
```

Example failure:

```text
nc: connect to 192.168.1.100 port 2049 failed: No route to host
```

#### Check Server Service

On server:

```bash
systemctl status nfs-server
sudo ss -tulnp | grep 2049
```

Example output:

```text
tcp LISTEN 0 64 0.0.0.0:2049 0.0.0.0:*
```

Interpretation:

- If port 2049 is not reachable, the issue may be server service, firewall, routing, or network outage.
- If the server is reachable but slow, check server disk and NFS statistics.

### Scenario 11: Use `showmount` to Inspect Exports

Check what the server appears to export.

On client:

```bash
showmount -e 192.168.1.100
```

Example output:

```text
Export list for 192.168.1.100:
/opt/shared 192.168.1.0/24
```

Interpretation:

- The server advertises /opt/shared to clients in 192.168.1.0/24.

Important note:

- showmount is most useful with NFSv3-style services.
- NFSv4-only servers may not behave the same way.

### Scenario 12: Unexport a Shared Directory

Stop sharing a directory without editing many files manually.

Check current exports:

```bash
sudo exportfs -v
```

Unexport:

```bash
sudo exportfs -u 192.168.1.0/24:/opt/shared
```

Check again:

```bash
sudo exportfs -v
```

Interpretation:

- The export was removed from the active export table.
- If the entry remains in /etc/exports, exportfs -r may re-enable it later.

For a permanent stop, remove or comment out the line in `/etc/exports`.

### Common NFS Problems and Fixes

### Problem: Access Denied by Server

Symptoms:

```text
mount.nfs: access denied by server
```

Check:

```bash
sudo exportfs -v
cat /etc/exports
showmount -e SERVER
```

Likely causes:

- client IP not allowed
- wrong export path
- exports not reloaded
- DNS or hostname mismatch
- NFS version mismatch

Fix:

```bash
sudo exportfs -r
```

and correct `/etc/exports`.

### Problem: Connection Timed Out

Symptoms:

```text
mount.nfs: Connection timed out
```

Check:

```bash
ping SERVER
nc -vz SERVER 2049
systemctl status nfs-server
sudo firewall-cmd --list-services
```

Likely causes:

- firewall blocks NFS
- NFS service stopped
- network route problem
- server down
- wrong IP address

### Problem: Permission Denied While Writing

Symptoms:

```text
touch: Permission denied
```

Check:

```bash
id
ls -ln /mnt/nfs_shared
ls -ln /opt/shared
sudo exportfs -v
```

Likely causes:

- UID/GID mismatch
- directory permissions do not allow write
- read-only export
- root_squash
- all_squash mapping

### Problem: Files Owned by nobody

Symptoms:

```text
-rw-r--r-- 1 nobody nobody file.txt
```

or numeric:

```text
4294967294
```

Likely causes:

- NFSv4 id mapping problem
- domain mismatch in idmapd.conf
- unknown user on server
- root_squash or all_squash behavior

Check:

```bash
cat /etc/idmapd.conf
id username
nfsidmap -l
```

### Problem: Stale File Handle

Symptoms:

```text
Stale file handle
```

Likely causes:

- server-side directory replaced
- export changed
- file deleted while client held reference
- server reboot or filesystem remount

Fix:

```bash
cd /
sudo umount /mnt/nfs_shared
sudo mount /mnt/nfs_shared
```

### Problem: Boot Delays Because NFS Is Unavailable

Symptoms:

- boot waits for remote mount
- emergency mode because mount failed

Fix fstab with:

- _netdev
- nofail
- x-systemd.automount

Example:

```fstab
192.168.1.100:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev,nofail,x-systemd.automount 0 0
```

### NFS Troubleshooting Workflow

When NFS fails, troubleshoot in layers.

1. Is the server reachable?
2. Is NFS service running?
3. Is port 2049 reachable?
4. Is the export listed?
5. Is the client allowed by /etc/exports?
6. Is the firewall open?
7. Is the mount command correct?
8. Are Unix permissions correct?
9. Are UID/GID mappings correct?
10. Are logs showing NFS errors?

Useful commands:

```bash
ping SERVER
nc -vz SERVER 2049
systemctl status nfs-server
sudo exportfs -v
showmount -e SERVER
mount | grep nfs
findmnt /mnt/nfs_shared
id
ls -ln
journalctl -u nfs-server -b
dmesg -T | grep -i nfs
```

### Useful Command Summary

Server setup:

```bash
sudo dnf install nfs-utils
sudo mkdir -p /opt/shared
sudo vi /etc/exports
sudo exportfs -r
sudo exportfs -v
sudo systemctl enable --now nfs-server
```

Client setup:

```bash
sudo dnf install nfs-utils
sudo mkdir -p /mnt/nfs_shared
sudo mount -t nfs4 SERVER:/opt/shared /mnt/nfs_shared
findmnt /mnt/nfs_shared
```

Firewall:

```bash
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --permanent --add-service=mountd
sudo firewall-cmd --permanent --add-service=rpc-bind
sudo firewall-cmd --reload
```

NFS inspection:

```bash
sudo exportfs -v
showmount -e SERVER
nfsstat -s
nfsstat -c
nfsiostat 1
mount | grep nfs
```

Persistent mount:

```fstab
SERVER:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev,nofail,x-systemd.automount 0 0
```

Unmount:

```bash
sudo umount /mnt/nfs_shared
```

Force investigation if busy:

```bash
sudo lsof +f -- /mnt/nfs_shared
sudo fuser -vm /mnt/nfs_shared
```

### Safe Lab Cleanup

On the client:

```bash
cd /
sudo umount /mnt/nfs_shared 2>/dev/null
sudo rmdir /mnt/nfs_shared 2>/dev/null
```

Remove fstab test entry if added:

```bash
sudo vi /etc/fstab
sudo systemctl daemon-reload
```

On the server, remove export line from `/etc/exports`, then:

```bash
sudo exportfs -r
sudo exportfs -v
```

Optionally remove test directory:

```bash
sudo rm -rf /opt/shared
```

### Challenges

1. Set up an NFS server that exports `/opt/shared` to one trusted client IP.
2. Mount the export from a client at `/mnt/nfs_shared` and verify it with `findmnt`.
3. Add a file on the server and confirm it appears on the client.
4. Create a file on the client and confirm it appears on the server.
5. Change the export from `rw` to `ro`, reload exports, remount on the client, and explain the write failure.
6. Simulate an incorrect client subnet in `/etc/exports` and diagnose the resulting `access denied by server` error.
7. Block NFS with the firewall and confirm that the client cannot connect to port 2049.
8. Compare UID and GID values for the same user on client and server. Explain how mismatches affect NFS permissions.
9. Demonstrate root squashing by trying to write as root from the client and inspecting ownership on the server.
10. Add an NFS mount to `/etc/fstab` using `_netdev,nofail,x-systemd.automount`, then test it with `mount -a`.
11. Use `nfsstat` or `nfsiostat` to observe NFS activity during a file copy.
12. Write a troubleshooting report for one NFS failure. Include symptom, command used, output, interpretation, and fix.
