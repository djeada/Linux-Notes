## Introduction to NFS

NFS (Network File System) is a server-client protocol used for file sharing between different computers (there is support for Linux, Mac, and Windows). NFS allows to mount a remote shared directory on your local machine, allowing you to access any of the files on that remote share directly.

## Setting up an NFS server

Here are the steps to install and configure NFS on a CentOS 7 system:

1. Install the necessary packages:

```
yum install nfs-utils nfs-utils-lib
```

2. Enable and start the rpcbind service:

```
systemctl enable rpcbind
systemctl start rpcbind
```

3. Enable and start the NFS server:

```
systemctl enable nfs-server
systemctl start nfs-server
```

4. Enable and start the NFS lock service:

```
systemctl enable nfs-lock
systemctl start nfs-lock
```

6. Enable and start the NFS idmap service:

```bash
systemctl enable nfs-idmap
systemctl start nfs-idmap
```

7. Add the desired shared directory to the `/etc/exports` file. For example, to share the `/opt/test` directory with clients in the IP range `192.168.2.0/24`, you would add the following line to the `/etc/exports` file:

```bash
/opt/test/     192.168.1.0/24(rw,sync,no_root_squash,no_all_squash)
```

Explanation:

* /opt/test – shared dir
* 192.168.2.0/24 – clients' IP range 
* rw – dir's permissions
* sync – synchronize shared directory
* no_root_squash – enable root privilege
* no_all_squash - enable user’s authority

8. Export the changes:

```bash
exportfs -r
```

9. Check if everything was exported:

```bash
exportfs
```

10. You may now restart the NFS server using the command:

```bash
systemctl restart nfs-server
```

## Setting up an NFS client

Here are the steps to install and configure NFS on a CentOS 7 system:

1. Install the necessary packages:

```
yum install nfs-utils nfs-utils-lib
```

2. Enable and start the rpcbind service:

```
systemctl enable rpcbind
systemctl start rpcbind
```

2. Enable and start the NFS client:

```
systemctl enable nfs-client
systemctl start nfs-client
```

4. Create a mount point on the client system to mount the shared directory:

```
mkdir /opt/test_client
```

5. Mount the shared directory on the client machine:

```
mount -t nfs 192.168.2.111:/opt/test/ /opt/test_client/ 
```

Replace `192.168.2.111` with the IP address of the NFS server and `/opt/test` with the desired shared directory.

6. Use the `mount` command to check if the shared directory is successfully mounted on the client:

```
mount
```

## Additional considerations

* NFS can be used to share directories between Windows, Linux, and Mac systems.
* It is important to consider security when using NFS. For example, you may want to limit access to the shared directory to specific IP ranges or users.
* You can also use the exportfs command to manage the shared directories on the server. For example, to view the currently exported directories, use `exportfs -v`. To unmount a shared directory, use `exportfs -u <directory>`.
    
## Challenges

1. What is NFS and how does it work?
1. How do you install and configure NFS on a server?
1. How do you enable and start the NFS services on a server?
1. How do you add a shared directory to the exports file on a server?
1. What are the options available in the exports file and what do they do?
1. How do you install and configure NFS on a client?
1. How do you mount a shared directory on a client?
1. How do you check if a shared directory is successfully mounted on a client?
1. Can NFS be used to share directories between Windows, Linux, and Mac systems?
1. Are there any security considerations to keep in mind when using NFS?
