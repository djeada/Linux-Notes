## NFS

NFS (Network File System) lets computers share files with other computers. It works on Linux, Mac, and Windows. You can use files on another computer like they are on your own computer.

```
Client                      Server
+--------+                  +--------+
|        |   NFS Protocol   |        |
|  App   |<---------------->| NFS    |
|        |                  | Server |
+--------+                  +--------+
   ||                           /|\
   ||                            |
   ||                  +------------------+
   ||                  |  File System     |
+--------+             | (ext4, XFS, etc) |
|  NFS   |             +------------------+
| Client |                       |
+--------+                       |
   ||                            |
+--------+             +------------------+
| File   |             |   Disk           |
| System |             |   Storage        |
| (local)|             +------------------+
+--------+                    
   ||                        
+--------+
| Disk   |
| Storage|
+--------+
```

### Setting up an NFS Server on CentOS 7

If you want to create NFS shares from a CentOS 7 machine, you'll need to set it up as an NFS server. Here's a step-by-step guide.

I. Install Required Packages

To set up NFS on CentOS 7, first install the necessary packages:

```bash
yum install nfs-utils nfs-utils-lib
```

II. Enable and Start rpcbind Service

```bash
systemctl enable rpcbind
systemctl start rpcbind
```

III. Enable and Start NFS Server Service

```bash
systemctl enable nfs-server
systemctl start nfs-server
```

IV. Enable and Start NFS Lock Service

NFS uses the locking service to lock files and directories:

```bash
systemctl enable nfs-lock
systemctl start nfs-lock
```

V. Enable and Start NFS Idmap Service

This service maps user and group IDs from the server to the client:

```bash
systemctl enable nfs-idmap
systemctl start nfs-idmap
```

VI. Configuring NFS Exports

Edit the /etc/exports file to specify which directories to share and with which options. For instance, to share /opt/test with clients in the IP range 192.168.1.0/24:

```bash
echo "/opt/test/     192.168.1.0/24(rw,sync,no_root_squash,no_all_squash)" >> /etc/exports
```

Here's a breakdown of the options:

- `/opt/test`: The directory you want to share.
- `192.168.1.0/24`: Specifies the range of client IP addresses that should be allowed access.
- `rw`: Read and write permissions.
- `sync`: Ensures changes to the shared directory are committed immediately.
- `no_root_squash`: Allows the root user on the client to have root privileges on the shared directory.
- `no_all_squash`: Preserves the UIDs and GIDs.

VII. Apply Configuration Changes

To let NFS know about your configuration changes:

```bash
exportfs -r
```

VIII. Verify Your Exports

To confirm the shared directories:

```bash
exportfs
```

IX. Restart NFS Server

To ensure all changes are applied and services are in the correct state:

```bash
systemctl restart nfs-server
```

### Setting up an NFS Client on CentOS 7

If you want to access NFS shares from a CentOS 7 machine, you'll need to set it up as an NFS client. Here's a step-by-step guide.

I. Install Required Packages

The necessary tools for accessing NFS shares can be installed with:

```bash
yum install nfs-utils nfs-utils-lib
```

II. Enable and Start rpcbind Service

NFS requires the rpcbind service:

```bash
systemctl enable rpcbind
systemctl start rpcbind
```

III. Enable and Start NFS Client Services

Ensure the NFS client is running:

```bash
systemctl enable nfs-client.target
systemctl start nfs-client.target
```

IV. Create a Mount Point

Prepare a directory on the client where the NFS share will be mounted:

```bash
mkdir /opt/test_client
```

V. Mount the NFS Share

Connect to the NFS share by mounting it:

```bash
mount -t nfs 192.168.2.111:/opt/test/ /opt/test_client/
```

Here:

- Replace `192.168.2.111` with your NFS server's IP address.
- Replace `/opt/test` with the directory shared from the server.

VI. Verify the Mount

Check that the shared directory is successfully mounted:

```bash
mount | grep nfs
```

### Additional Considerations

- NFS can be utilized to share directories between a variety of operating systems, including Windows, Linux, and macOS.
- Be cautious with NFS configurations; always consider security. Restrict access based on IP addresses, users, or other criteria.
- Managing Shared Folders on Server:

I. To view currently shared folders with their respective options, use:
   
```bash
exportfs -v
```

II. To unshare a directory:

```bash
exportfs -u <directory_path>
```

### Challenges

1. Explain the main purpose of NFS. How does it enable file sharing between different computers?
2. Describe the key components of an NFS server. How does each component contribute to the operation of the NFS system?
3. What is the role of the rpcbind service in NFS? Why is it important, and how does it interact with the rest of the system?
4. Detail the steps to share a directory on an NFS server. Why is the `/etc/exports` file crucial in this process?
5. List and explain the various options available in the `/etc/exports` file. How do these options affect the configuration of shared directories?
6. Compare the setup processes for an NFS server and an NFS client. What are the similarities and differences?
7. Explain how to mount an NFS-shared directory on a client. How can the client verify that the connection is successful?
8. Discuss the potential security risks associated with NFS. What measures can be taken to mitigate these risks?
9. Provide an example of how NFS can be useful for sharing directories across different operating systems, such as Windows, Linux, and macOS.
10. Describe the function of the exportfs command in NFS. How is it used to view, modify, and stop sharing directories?
