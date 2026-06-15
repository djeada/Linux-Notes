## NFS: Network File System

NFS stands for Network File System.

It is a protocol that allows one computer to share directories with other computers over a network.

The important idea is:

```text id="hp1p7h"
A remote directory can appear like a local directory.
```

For example, a server may export:

```text id="ux347e"
/opt/shared
```

A client may mount it at:

```text id="uszbjk"
/mnt/nfs_shared
```

Then users on the client can access remote files as if they were local:

```bash id="cbwdek"
ls /mnt/nfs_shared
```

### Big Picture

NFS has two main sides:

- NFS server    shares directories
- NFS client    mounts and uses those directories

Diagram:

```text id="krusg7"
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

```text id="y6y94w"
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

```bash id="nnrdg1"
sudo dnf install nfs-utils
```

On older CentOS 7 systems:

```bash id="e0xui4"
sudo yum install nfs-utils
```

On Debian or Ubuntu systems:

```bash id="qdsmpd"
sudo apt install nfs-kernel-server nfs-common
```

Package names vary slightly by distribution, but the main idea is the same:

- server needs NFS server tools
- client needs NFS client tools

### Creating a Shared Directory

Example server directory:

```bash id="z2fe5p"
sudo mkdir -p /opt/shared
```

Add a test file:

```bash id="r5759y"
echo "hello from NFS server" | sudo tee /opt/shared/hello.txt
```

Set ownership and permissions based on your use case.

For a simple lab:

```bash id="s7hajw"
sudo chmod 755 /opt/shared
```

For a shared writable directory, you may use a group:

```bash id="g8yis5"
sudo groupadd nfsusers
sudo chgrp nfsusers /opt/shared
sudo chmod 2775 /opt/shared
```

The `2` in `2775` sets the setgid bit so new files tend to inherit the directory group.

### `/etc/exports`

The server uses `/etc/exports` to define what directories are shared and who can access them.

Example:

```exports id="bssxu6"
/opt/shared 192.168.1.0/24(rw,sync,root_squash)
```

Meaning:

- /opt/shared       directory being exported
- 192.168.1.0/24    allowed client network
- rw                read-write access
- sync              write changes safely before replying
- root_squash       map client root to unprivileged user

A more restrictive example:

```exports id="s7a70g"
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

```exports id="rg32rx"
/opt/shared 192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
```

Important warning:

- Avoid no_root_squash unless you truly need it.
- It gives root on the client powerful access to the exported directory.

### Applying Export Changes

After editing `/etc/exports`, apply changes with:

```bash id="iy6g5q"
sudo exportfs -r
```

View exports:

```bash id="n57d4e"
sudo exportfs -v
```

Example output:

```text id="b7xx75"
/opt/shared  192.168.1.0/24(sync,wdelay,hide,no_subtree_check,sec=sys,rw,root_squash,no_all_squash)
```

Interpretation:

- The server exports /opt/shared to clients in 192.168.1.0/24.
- The export is read-write.
- root_squash is enabled.

### Starting NFS Services

On systemd systems:

```bash id="l0bb5x"
sudo systemctl enable --now nfs-server
```

Check status:

```bash id="xir812"
systemctl status nfs-server
```

Example output:

```text id="n9hf3d"
● nfs-server.service - NFS server and services
     Loaded: loaded
     Active: active (exited)
```

Interpretation:

- The service is active.
- For NFS, active (exited) can be normal because systemd started the required kernel NFS services.

On older setups, you may also see or manage:

```bash id="z2wdjo"
sudo systemctl enable --now rpcbind
sudo systemctl enable --now nfs-idmapd
```

### Firewall Rules for NFS

For NFSv4, TCP port 2049 is the main port.

For NFSv3, additional RPC services such as mountd and rpcbind may be needed.

With firewalld:

```bash id="u3q2zi"
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --permanent --add-service=mountd
sudo firewall-cmd --permanent --add-service=rpc-bind
sudo firewall-cmd --reload
```

Check:

```bash id="qq9r0c"
sudo firewall-cmd --list-services
```

Example output:

```text id="jmeir4"
ssh dhcpv6-client nfs mountd rpc-bind
```

Interpretation:

- The firewall allows NFS-related services.
- Clients should be able to reach the NFS server if routing and exports are correct.

With UFW, a simple NFSv4 example:

```bash id="w2u3b6"
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

```bash id="l8krq8"
sudo dnf install nfs-utils
```

Debian/Ubuntu:

```bash id="izhh78"
sudo apt install nfs-common
```

Create mount point:

```bash id="ok064r"
sudo mkdir -p /mnt/nfs_shared
```

Mount:

```bash id="nhh0dm"
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

For NFSv4 explicitly:

```bash id="bi6147"
sudo mount -t nfs4 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Check:

```bash id="kmvpeu"
mount | grep nfs
```

Example output:

```text id="mzwh8p"
192.168.1.100:/opt/shared on /mnt/nfs_shared type nfs4 (rw,relatime,vers=4.2,addr=192.168.1.100)
```

Interpretation:

- The NFS share is mounted.
- The client is using NFS version 4.2.
- The mount is read-write.

### Verifying the NFS Mount

List files:

```bash id="uyhe38"
ls -l /mnt/nfs_shared
```

Example output:

```text id="ff7z9p"
-rw-r--r-- 1 root root 22 Jun 1 12:00 hello.txt
```

Read the test file:

```bash id="qhopu8"
cat /mnt/nfs_shared/hello.txt
```

Example output:

```text id="icytql"
hello from NFS server
```

Create a file if write access is allowed:

```bash id="y19cn1"
touch /mnt/nfs_shared/client-test.txt
```

If this works, the mount is writable for your user.

If it fails with permission denied, check Unix permissions, UID/GID mapping, root squashing, and export options.

### Persistent NFS Mounts with `/etc/fstab`

To mount automatically at boot, add an entry on the client.

Example:

```fstab id="cz80y4"
192.168.1.100:/opt/shared /mnt/nfs_shared nfs defaults,_netdev 0 0
```

For NFSv4:

```fstab id="bllsb7"
192.168.1.100:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev 0 0
```

Important option:

```text id="z9uz0f"
_netdev means this mount depends on the network.
```

For systems where the NFS server may not always be available, consider:

```fstab id="vewcb2"
192.168.1.100:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev,nofail,x-systemd.automount 0 0
```

Meaning:

- nofail              do not fail boot if the mount is unavailable
- x-systemd.automount mount on first access instead of immediately at boot

Test fstab:

```bash id="z6ni35"
sudo mount -a
```

Check:

```bash id="ad3xbb"
findmnt /mnt/nfs_shared
```

### UID and GID Mapping

NFS permissions are based heavily on numeric user IDs and group IDs.

This is a major concept.

Linux file ownership is stored as numbers:

- UID = user ID
- GID = group ID

Example:

```bash id="b8w9by"
id alice
```

Output:

```text id="l42xvm"
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

```text id="dhlicb"
/etc/idmapd.conf
```

Example:

```conf id="g5uavc"
[General]
Domain = example.com
```

Restart relevant services after changes.

Example:

```bash id="a3ga48"
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

```text id="tqs9n6"
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

```exports id="g4wx5t"
/opt/shared 192.168.1.0/24(rw,sync,root_squash)
```

Dangerous option:

```exports id="rlw6wf"
/opt/shared 192.168.1.0/24(rw,sync,no_root_squash)
```

Use `no_root_squash` only in carefully controlled environments.

### `all_squash`

The `all_squash` option maps all client users to the anonymous user.

Example:

```exports id="cmtlbx"
/opt/public 192.168.1.0/24(rw,sync,all_squash)
```

This can be useful for simple public drop-box style shares where all access should use one server-side identity.

Common related options:

- anonuid=UID
- anongid=GID

Example:

```exports id="jz49si"
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

```exports id="ebskjz"
/srv/project 192.168.10.0/24(rw,sync,root_squash,no_subtree_check)
```

A risky export is broad:

```exports id="pu09el"
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

```bash id="x53gcw"
sudo mount -t nfs -o rsize=8192,wsize=8192 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Modern systems often negotiate good defaults automatically. Tune only after measuring.

Important safety note:

- async can improve performance but may risk data loss if the server crashes before data is safely written.
- sync is safer but can be slower.

### Managing Exports with `exportfs`

View exports:

```bash id="uwts38"
sudo exportfs -v
```

Reload exports:

```bash id="cc2e3r"
sudo exportfs -r
```

Unexport one directory:

```bash id="p4di7r"
sudo exportfs -u 192.168.1.0/24:/opt/shared
```

Unexport all:

```bash id="ztbh5i"
sudo exportfs -ua
```

Re-export all from `/etc/exports`:

```bash id="ggv0oy"
sudo exportfs -a
```

### Scenario 1: Create a Basic NFS Share

#### Goal

Set up a server export and mount it from a client.

#### Server Steps

Install packages:

```bash id="y84t3b"
sudo dnf install nfs-utils
```

Create directory:

```bash id="o4zjyr"
sudo mkdir -p /opt/shared
echo "hello from server" | sudo tee /opt/shared/hello.txt
sudo chmod 755 /opt/shared
```

Edit `/etc/exports`:

```exports id="kfcw99"
/opt/shared 192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
```

Apply:

```bash id="jux62s"
sudo exportfs -r
sudo systemctl enable --now nfs-server
sudo exportfs -v
```

Example output:

```text id="tzdqxm"
/opt/shared 192.168.1.0/24(sync,wdelay,no_subtree_check,sec=sys,rw,root_squash,no_all_squash)
```

#### Client Steps

Install client tools:

```bash id="cjk5xk"
sudo dnf install nfs-utils
```

Create mount point:

```bash id="g8qbw9"
sudo mkdir -p /mnt/nfs_shared
```

Mount:

```bash id="q95g5v"
sudo mount -t nfs4 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Check:

```bash id="oufo7e"
findmnt /mnt/nfs_shared
cat /mnt/nfs_shared/hello.txt
```

Example output:

```text id="grv0pw"
hello from server
```

#### Interpretation

- The server exported the directory.
- The client mounted it successfully.
- The client can read files stored on the server.

### Scenario 2: Simulate “Access Denied by Server”

#### Goal

Show what happens when the client IP is not allowed by `/etc/exports`.

#### Simulate Problem

On the server, restrict the export to the wrong network:

```exports id="w2dm45"
/opt/shared 10.10.10.0/24(rw,sync,root_squash)
```

Apply:

```bash id="zhgw1l"
sudo exportfs -r
```

On the client:

```bash id="sxka5b"
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Example output:

```text id="xs2map"
mount.nfs: access denied by server while mounting 192.168.1.100:/opt/shared
```

#### Check on Server

```bash id="tl4rsm"
sudo exportfs -v
```

Example output:

```text id="x7c7iv"
/opt/shared 10.10.10.0/24(rw,sync,root_squash)
```

#### Interpretation

- The server is exporting the directory only to 10.10.10.0/24.
- The client is not in that allowed range.
- The server rejects the mount request.

#### Fix

Use the correct client subnet or IP:

```exports id="q7d6wl"
/opt/shared 192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
```

Apply:

```bash id="p0vqvz"
sudo exportfs -r
```

### Scenario 3: Simulate NFS Blocked by Firewall

#### Goal

Diagnose when the export is correct but the client cannot reach NFS services.

#### Simulate Problem

On the server, remove NFS firewall services:

```bash id="spf96q"
sudo firewall-cmd --permanent --remove-service=nfs
sudo firewall-cmd --permanent --remove-service=mountd
sudo firewall-cmd --permanent --remove-service=rpc-bind
sudo firewall-cmd --reload
```

On the client:

```bash id="b3t45n"
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Possible output:

```text id="a9n4r6"
mount.nfs: Connection timed out
```

#### Check Connectivity

```bash id="g3ctzq"
nc -vz 192.168.1.100 2049
```

Example output:

```text id="gbh656"
nc: connect to 192.168.1.100 port 2049 (tcp) timed out
```

#### Check Server Firewall

```bash id="qme7ur"
sudo firewall-cmd --list-services
```

Example output:

```text id="dlu4wr"
ssh dhcpv6-client
```

#### Interpretation

- The NFS export may be correct.
- The server firewall is blocking NFS traffic.
- The client cannot reach port 2049.

#### Fix

```bash id="ggpmz4"
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --permanent --add-service=mountd
sudo firewall-cmd --permanent --add-service=rpc-bind
sudo firewall-cmd --reload
```

Retest:

```bash id="kxdwh8"
nc -vz 192.168.1.100 2049
```

Expected:

```text id="e9uwep"
Connection to 192.168.1.100 2049 port [tcp/nfs] succeeded!
```

### Scenario 4: Simulate Permission Denied from UID/GID Mismatch

#### Goal

Show why matching usernames is not enough if numeric UIDs differ.

#### Situation

On server:

```text id="d80i0q"
alice UID = 1001
```

On client:

```text id="l1tlax"
alice UID = 1002
```

The server directory is owned by UID 1001:

```bash id="qf8b3s"
ls -ln /opt/shared
```

Example output on server:

```text id="mc9vll"
drwxr-x--- 2 1001 1001 4096 Jun 1 12:00 /opt/shared
```

On client, Alice tries:

```bash id="f8qcgn"
touch /mnt/nfs_shared/test.txt
```

Example output:

```text id="rs2iez"
touch: cannot touch '/mnt/nfs_shared/test.txt': Permission denied
```

#### Check IDs

On client:

```bash id="ndspw7"
id alice
```

Example:

```text id="smbxxu"
uid=1002(alice) gid=1002(alice)
```

On server:

```bash id="ouphfo"
id alice
```

Example:

```text id="eep2z3"
uid=1001(alice) gid=1001(alice)
```

#### Interpretation

- NFS uses numeric IDs for permission checks.
- The server receives UID 1002, not the name alice.
- The server does not treat UID 1002 as the owner of files owned by UID 1001.

#### Fix Options

- make UIDs and GIDs consistent
- use centralized identity management
- configure NFSv4 id mapping
- use controlled all_squash mapping for simple shared directories

### Scenario 5: Simulate Root Squash Behavior

#### Goal

Show why root on the client may not have root power on the NFS export.

#### Server Export

```exports id="khv6od"
/opt/shared 192.168.1.0/24(rw,sync,root_squash)
```

Apply:

```bash id="t19ike"
sudo exportfs -r
```

On client as root:

```bash id="zq52bs"
sudo touch /mnt/nfs_shared/root-created.txt
```

Possible output:

```text id="lfvvya"
touch: cannot touch '/mnt/nfs_shared/root-created.txt': Permission denied
```

Or if the directory allows anonymous writes, check ownership:

```bash id="uenf3v"
ls -ln /mnt/nfs_shared/root-created.txt
```

Example output:

```text id="myy9ha"
-rw-r--r-- 1 65534 65534 0 Jun 1 12:30 root-created.txt
```

#### Interpretation

- Client root was mapped to an anonymous unprivileged user.
- This is root_squash protecting the server.
- UID 65534 often represents nobody or nfsnobody.

#### Unsafe Alternative

```exports id="nkdq19"
/opt/shared 192.168.1.0/24(rw,sync,no_root_squash)
```

Warning:

- no_root_squash allows client root to act as root on the export.
- Use only when required and only for trusted clients.

### Scenario 6: Simulate a Stale NFS File Handle

#### Goal

Understand what happens when the server-side exported directory changes while clients still have old references.

#### Simulate

Client mounts:

```bash id="tnr48n"
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
cd /mnt/nfs_shared
```

On the server, rename and recreate the export directory:

```bash id="w034th"
sudo mv /opt/shared /opt/shared.old
sudo mkdir /opt/shared
sudo exportfs -r
```

On the client:

```bash id="zfkifu"
ls
```

Possible output:

```text id="zbl3xr"
ls: cannot access '.': Stale file handle
```

#### Interpretation

- The client holds references to objects that no longer match the server-side export.
- The server-side directory was replaced.
- The client mount needs to be refreshed.

#### Fix

On the client:

```bash id="fdczmf"
cd /
sudo umount /mnt/nfs_shared
sudo mount /mnt/nfs_shared
```

If unmount is busy:

```bash id="tg3edv"
sudo lsof +f -- /mnt/nfs_shared
sudo fuser -vm /mnt/nfs_shared
```

Then stop the using process or move out of the directory.

### Scenario 7: Simulate Boot Hang from NFS in `/etc/fstab`

#### Goal

Show why NFS mounts should be configured carefully for boot.

#### Problem fstab Entry

```fstab id="c5c3lp"
192.168.1.100:/opt/shared /mnt/nfs_shared nfs defaults 0 0
```

If the NFS server is down during boot, the client may wait for a long time.

#### Better Entry

```fstab id="f1uare"
192.168.1.100:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev,nofail,x-systemd.automount 0 0
```

#### Apply

```bash id="va9gob"
sudo systemctl daemon-reload
sudo mount -a
```

Check systemd mount units:

```bash id="iauyw3"
systemctl list-units | grep nfs_shared
```

Example output:

```text id="g0udrs"
mnt-nfs_shared.automount loaded active waiting /mnt/nfs_shared
```

#### Interpretation

- The automount unit waits until the path is accessed.
- nofail prevents boot failure if the server is unavailable.
- This is safer for laptops and clients that may boot away from the NFS network.

### Scenario 8: Simulate Read-Only Export

#### Goal

Show how export options override client expectations.

#### Server Export

```exports id="pgmbx6"
/opt/shared 192.168.1.0/24(ro,sync,root_squash)
```

Apply:

```bash id="h6i8bo"
sudo exportfs -r
```

Client remount:

```bash id="vmmryr"
sudo umount /mnt/nfs_shared
sudo mount -t nfs 192.168.1.100:/opt/shared /mnt/nfs_shared
```

Try write:

```bash id="palzvy"
touch /mnt/nfs_shared/test.txt
```

Example output:

```text id="ptk7qa"
touch: cannot touch '/mnt/nfs_shared/test.txt': Read-only file system
```

#### Check Mount

```bash id="tq7syv"
findmnt /mnt/nfs_shared
```

Example output:

```text id="ian9f0"
TARGET          SOURCE                    FSTYPE OPTIONS
/mnt/nfs_shared 192.168.1.100:/opt/shared nfs4   ro,relatime,vers=4.2
```

#### Interpretation

- The server exported the directory as read-only.
- The client cannot write, even if local commands try to create files.

### Scenario 9: Measure NFS Performance

#### Goal

Check whether NFS is slow and where the bottleneck may be.

#### Write Test

On the client:

```bash id="n9qiry"
dd if=/dev/zero of=/mnt/nfs_shared/testfile bs=1M count=512 conv=fdatasync
```

Example output:

```text id="zr3u77"
536870912 bytes copied, 8.2 s, 65.5 MB/s
```

#### Read Test

```bash id="pkak9p"
dd if=/mnt/nfs_shared/testfile of=/dev/null bs=1M
```

Example output:

```text id="m13evq"
536870912 bytes copied, 4.1 s, 130 MB/s
```

#### Check Mount Stats

```bash id="aw6pze"
nfsiostat 1
```

Example output:

```text id="fsz0uq"
op/s    rpc bklog
120.00  0.00

read:  avg RTT  4.0 ms   avg exe  5.0 ms
write: avg RTT 12.0 ms   avg exe 15.0 ms
```

#### Interpretation

- Writes are slower than reads.
- NFS write latency is higher.
- Possible causes include sync export behavior, server disk speed, network latency, or competing workloads.

#### Other Checks

On client:

```bash id="f4s6kc"
mount | grep nfs
nfsstat -c
```

On server:

```bash id="hgrin7"
nfsstat -s
iostat -xz 1
```

### Scenario 10: Troubleshoot “NFS Server Is Not Responding”

#### Goal

Diagnose a client that hangs or reports server not responding.

#### Symptom

Client log or terminal shows:

```text id="lgbbq1"
nfs: server 192.168.1.100 not responding, still trying
```

#### Check Network

```bash id="lp2ynz"
ping 192.168.1.100
```

Check NFS port:

```bash id="avx2qc"
nc -vz 192.168.1.100 2049
```

Example failure:

```text id="k3hy0m"
nc: connect to 192.168.1.100 port 2049 failed: No route to host
```

#### Check Server Service

On server:

```bash id="rwhwx8"
systemctl status nfs-server
sudo ss -tulnp | grep 2049
```

Example output:

```text id="y04taw"
tcp LISTEN 0 64 0.0.0.0:2049 0.0.0.0:*
```

#### Interpretation

- If port 2049 is not reachable, the issue may be server service, firewall, routing, or network outage.
- If the server is reachable but slow, check server disk and NFS statistics.

### Scenario 11: Use `showmount` to Inspect Exports

#### Goal

Check what the server appears to export.

On client:

```bash id="knldox"
showmount -e 192.168.1.100
```

Example output:

```text id="v7sgao"
Export list for 192.168.1.100:
/opt/shared 192.168.1.0/24
```

Interpretation:

- The server advertises /opt/shared to clients in 192.168.1.0/24.

Important note:

- showmount is most useful with NFSv3-style services.
- NFSv4-only servers may not behave the same way.

### Scenario 12: Unexport a Shared Directory

#### Goal

Stop sharing a directory without editing many files manually.

Check current exports:

```bash id="lgb7xe"
sudo exportfs -v
```

Unexport:

```bash id="wmga8s"
sudo exportfs -u 192.168.1.0/24:/opt/shared
```

Check again:

```bash id="w4rt05"
sudo exportfs -v
```

Interpretation:

- The export was removed from the active export table.
- If the entry remains in /etc/exports, exportfs -r may re-enable it later.

For a permanent stop, remove or comment out the line in `/etc/exports`.

### Common NFS Problems and Fixes

### Problem: Access Denied by Server

Symptoms:

```text id="dyukgw"
mount.nfs: access denied by server
```

Check:

```bash id="ddsceu"
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

```bash id="igsl9u"
sudo exportfs -r
```

and correct `/etc/exports`.

### Problem: Connection Timed Out

Symptoms:

```text id="yu6479"
mount.nfs: Connection timed out
```

Check:

```bash id="dy7w79"
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

```text id="j92faf"
touch: Permission denied
```

Check:

```bash id="ycmho9"
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

```text id="tm9rh1"
-rw-r--r-- 1 nobody nobody file.txt
```

or numeric:

```text id="ddrg78"
4294967294
```

Likely causes:

- NFSv4 id mapping problem
- domain mismatch in idmapd.conf
- unknown user on server
- root_squash or all_squash behavior

Check:

```bash id="kw31r1"
cat /etc/idmapd.conf
id username
nfsidmap -l
```

### Problem: Stale File Handle

Symptoms:

```text id="emafzz"
Stale file handle
```

Likely causes:

- server-side directory replaced
- export changed
- file deleted while client held reference
- server reboot or filesystem remount

Fix:

```bash id="phbi97"
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

```fstab id="d5au5j"
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

```bash id="x6nxz4"
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

```bash id="b7seyz"
sudo dnf install nfs-utils
sudo mkdir -p /opt/shared
sudo vi /etc/exports
sudo exportfs -r
sudo exportfs -v
sudo systemctl enable --now nfs-server
```

Client setup:

```bash id="dazg1m"
sudo dnf install nfs-utils
sudo mkdir -p /mnt/nfs_shared
sudo mount -t nfs4 SERVER:/opt/shared /mnt/nfs_shared
findmnt /mnt/nfs_shared
```

Firewall:

```bash id="miejcz"
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --permanent --add-service=mountd
sudo firewall-cmd --permanent --add-service=rpc-bind
sudo firewall-cmd --reload
```

NFS inspection:

```bash id="vwp5np"
sudo exportfs -v
showmount -e SERVER
nfsstat -s
nfsstat -c
nfsiostat 1
mount | grep nfs
```

Persistent mount:

```fstab id="l29ueu"
SERVER:/opt/shared /mnt/nfs_shared nfs4 defaults,_netdev,nofail,x-systemd.automount 0 0
```

Unmount:

```bash id="po7gb9"
sudo umount /mnt/nfs_shared
```

Force investigation if busy:

```bash id="nh69yn"
sudo lsof +f -- /mnt/nfs_shared
sudo fuser -vm /mnt/nfs_shared
```

### Safe Lab Cleanup

On the client:

```bash id="puavzy"
cd /
sudo umount /mnt/nfs_shared 2>/dev/null
sudo rmdir /mnt/nfs_shared 2>/dev/null
```

Remove fstab test entry if added:

```bash id="m6a6ua"
sudo vi /etc/fstab
sudo systemctl daemon-reload
```

On the server, remove export line from `/etc/exports`, then:

```bash id="u0mrps"
sudo exportfs -r
sudo exportfs -v
```

Optionally remove test directory:

```bash id="rv0n41"
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
