## Introduction to NFS

NFS (Network File System) lets computers share files with other computers. It works on Linux, Mac, and Windows. You can use files on another computer like they are on your own computer.

## Setting up an NFS server

Follow these steps to set up NFS on CentOS 7:

1. Install needed packages:

```
yum install nfs-utils nfs-utils-lib
```

2. Turn on and start rpcbind service:

```
systemctl enable rpcbind
systemctl start rpcbind
```

3. Turn on and start NFS server:

```
systemctl enable nfs-server
systemctl start nfs-server
```

4. Turn on and start NFS lock service:

```
systemctl enable nfs-lock
systemctl start nfs-lock
```

5. Turn on and start NFS idmap service:

```bash
systemctl enable nfs-idmap
systemctl start nfs-idmap
```

6. Add the folder you want to share in `/etc/exports`. For example, to share `/opt/test` with clients in the IP range `192.168.2.0/24`, add this line to `/etc/exports`:

```bash
/opt/test/     192.168.1.0/24(rw,sync,no_root_squash,no_all_squash)
```

Meanings of the options:

* `/opt/test` – folder to share
* `192.168.2.0/24` – clients' IP range
* `rw` – folder permissions
* `sync` – sync shared folder
* `no_root_squash` – allow root access
* `no_all_squash` - keep user access
    
7. Apply changes:

```bash
exportfs -r
```

8. Check if changes were applied:

```bash
exportfs
```

9. Restart NFS server:

```bash
systemctl restart nfs-server
```

## Setting up an NFS client

Follow these steps to set up NFS on CentOS 7:

1. Install needed packages:

```
yum install nfs-utils nfs-utils-lib
```

2. Turn on and start rpcbind service:

```
systemctl enable rpcbind
systemctl start rpcbind
```

3. Turn on and start NFS client:

```
systemctl enable nfs-client
systemctl start nfs-client
```

4. Make a folder on the client to use the shared folder:

```
mkdir /opt/test_client
```

5. Connect the shared folder to the client folder:

```
mount -t nfs 192.168.2.111:/opt/test/ /opt/test_client/ 
```

Replace `192.168.2.111` with the NFS server's IP address and `/opt/test` with the folder you want to share.

6. Use `mount` to check if the shared folder is connected to the client:

```
mount
```

## Additional considerations

* NFS can share folders between Windows, Linux, and Mac.
* Think about security when using NFS. You might want to limit access to certain IP ranges or users.
* Use `exportfs` to manage shared folders on the server. To see current shared folders, use `exportfs -v`. To stop sharing a folder, use `exportfs -u <directory>`.
    
## Challenges

1. Explain the purpose of NFS and how it enables file sharing between different computers.
2. Describe the main components of an NFS server and their roles in the NFS system.
3. Explain the purpose of the rpcbind service and how it is related to NFS.
4. Describe the process of adding a shared directory on an NFS server, including the significance of the `/etc/exports` file.
5. Explain the various options available when defining a shared directory in the `/etc/exports` file and their effects on the sharing configuration.
6. Compare the steps required for setting up an NFS server and an NFS client. What similarities and differences do you observe?
7. Explain the process of mounting a shared directory on an NFS client, and how the client can verify a successful connection.
8. Describe the security considerations and potential risks when using NFS, and how you can mitigate them.
9. Illustrate a use case where NFS can be helpful in sharing directories across different operating systems (Windows, Linux, and Mac).
10. Explain the role of the `exportfs` command in managing shared directories on an NFS server, and demonstrate how to use it to view, update, and unshare directories.
