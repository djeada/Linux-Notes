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

1. What is NFS and how does it work?
2. How do you set up NFS on a server?
3. How do you turn on and start NFS services on a server?
4. How do you add a folder to share on a server?
5. What do the options in the exports file mean?
6. How do you set up NFS on a client?
7. How do you mount a shared directory on a client?
8. How do you check if a shared directory is successfully mounted on a client?
9. Can NFS be used to share directories between Windows, Linux, and Mac systems?
10. Are there any security considerations to keep in mind when using NFS?
