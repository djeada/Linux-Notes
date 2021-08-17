NFS (Network File System) is a server-client protocol used for file sharing between Unix computers. NFS allows you to mount a remote share on your local machine. You may then access any of the files on that remote share directly.

<h2>Server side</h2>

Use the following commands on a Centos7 system:

```bash
yum install nfs-utils nfs-utils-lib

systemctl enable rpcbind
systemctl start rpcbind

systemctl enable nfs-server
systemctl start nfs-server

systemctl enable nfs-lock
systemctl start nfs-lock

systemctl enable nfs-idmap
systemctl start nfs-idmap
```

Assume you want to share the /opt/test directory and your clients' IP range is 192.168.2.0/24.
Then, in /etc/exports, append the following line:

```bash
/opt/test/     192.168.1.0/24(rw,sync,no_root_squash,no_all_squash)
```

* /opt/test – shared dir
* 192.168.2.0/24 – clients' IP range 
* rw – dir's permissions
* sync – synchronize shared directory
* no_root_squash – enable root privilege
* no_all_squash - enable user’s authority

You may now restart the nfs server using the command:

```bash
systemctl restart nfs-server
```

<h2>Client side</h2>

Use the following commands on a Centos7 system:

```bash
yum install nfs-utils nfs-utils-lib

systemctl enable rpcbind
systemctl start rpcbind

systemctl enable nfs-server
systemctl start nfs-server

systemctl enable nfs-lock
systemctl start nfs-lock

systemctl enable nfs-idmap
systemctl start nfs-idmap
```

Make a mount point on the client system to mount the shared directory:

```bash
mkdir /opt/test_client
```

Now you can mount the shared directory on the client machine (assuming server ip is 192.168.2.111):

```bash
mount -t nfs 192.168.2.111:/opt/test/ /opt/test_client/ 
```

Using the <i>mount</i> command, check if the shared directory is mounted or not.

```bash
mount
```
