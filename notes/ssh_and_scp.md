## What is SSH?

SSH (Secure Shell) is a network protocol and software suite that enables secure communication between computers over an unsecured network, such as the internet. It is commonly used to securely log into a remote machine and execute commands on it, as well as to transfer files between computers using secure protocols such as SFTP (SSH File Transfer Protocol) or SCP (Secure Copy Protocol).

SSH uses public-key cryptography to authenticate the remote computer and allow the remote computer to authenticate the user. This means that the user's machine generates a pair of keys (a private key and a public key), and the user's public key is stored on the remote machine. When the user attempts to log in to the remote machine, the remote machine uses the stored public key to authenticate the user and allow the connection.

## Connecting to a Remote Host with SSH

To connect to a remote host using SSH, you need to know the host's IP address, as well as the username and password (or have the private key that corresponds to the public key stored on the remote host). You can then use the ssh command with the appropriate flags to connect to the remote host.

Here is the general syntax for connecting to a remote host using SSH:

```
ssh username@serverhost
```

If you are using password authentication, the server will request a password. If you are using key authentication, you will not be prompted for a password.

There are a number of flags that can be used with the ssh command to specify additional options:

* `-l`: Specifies the username to use for the connection.
* `-i`: Specifies the path to the key file. By default, SSH looks for the key file in `~/.ssh/id_rsa`.
* `-F`: Specifies the path to the connection config file. Each user has their own connection config file, located at `~/.ssh/config`, but there is also a global connection config file located at `/etc/ssh/ssh_config`.

To ensure that the `sshd` service is running on your server, you can use the following commands on a Debian-based system:

```
apt install openssh-server
systemctl enable ssh
systemctl start ssh
```

## Key Generation

SSH uses a public-key cryptography system to authenticate the remote computer and allow the remote computer to authenticate the user. This means that each user generates a pair of keys (a private key and a public key) and the user's public key is stored on the remote machine. To generate a new key pair, use the `ssh-keygen` command with the `-t` flag to specify the type of key to generate, such as rsa:

```
ssh-keygen  -t rsa
```

This will generate an RSA public and private key pair in the `~/.ssh` directory. You can use the `ls -a ~/.ssh/` command to list the files in this directory and see the new key pair.

## Uploading the Public Key to the Remote Host

To allow a user to log in to the remote host using their private key, the user's public key must be stored on the remote host. This can be done using the ssh-copy-id command, which copies the user's public key to the remote host.

```
ssh-copy-id -i ~/.ssh/mykey username@serverhost
```

## Using Non-Standard Ports

By default, SSH uses port 22 to establish connections. However, for improved security, you may want to change the port number to a different value. To do this, you must edit the `/etc/ssh/sshd_config` file on the server and specify the new port number. For example port 561. When logging in to the server using SSH, you will then need to specify the port number using the `-p` flag:

```
ssh -p 561 username@serverhost
```

## SCP

SCP (Secure Copy Protocol) is a simple command-line utility for transferring files between computers. It functions similarly to the UNIX cp command, but allows you to specify a user, machine, and files as parameters. To transfer a file from your local machine to the remote server, use the following syntax:

```
scp /local/path/to/file username@server:/remote/path/to/file
```

To transfer a file from the remote server to your local machine, use the following syntax:

scp username@server:/remote/path/to/file /local/path/to/file

You can use the `-r` flag to copy directories recursively, and the -P flag to specify the connection port (the default is 22). For example:

```
scp -P 80 -r root@server:/remote/path/to/directory /local/path/to/directory
```

## SFTP

SFTP (SSH File Transfer Protocol) is a secure file transfer protocol that runs over the SSH protocol. It offers a number of advantages over other file transfer protocols, including high-quality security and the ability to navigate the directory structure, create and delete folders, and perform other file operations. To use SFTP, you will need a client software such as WinSCP, FileZilla, CyberDuck, or others. These clients typically have a GUI interface that allows you to easily connect to the remote server and transfer files.

To connect to a remote server using SFTP, you will need to know the server's IP address and specify the protocol as SFTP or SSH. The default port for SFTP is 22.

To connect to a remote server using SFTP, use the sftp command followed by the username and server hostname or IP address:

```
sftp username@serverhost
```

This will open an SFTP session and prompt you for the password for the specified user. Once you are authenticated, you will see the sftp> prompt, indicating that you are connected to the remote server and can start issuing SFTP commands.

To list the files and directories on the remote server, use the ls command:

```
sftp> ls
```

This will display a list of files and directories in the current directory on the remote server.

To change the current directory on the remote server, use the cd command followed by the path to the desired directory:

```
sftp> cd /path/to/directory
```

To transfer a file from the local machine to the remote server, use the put command followed by the path to the local file:

```
sftp> put /local/path/to/file
```

This will transfer the specified file from the local machine to the current directory on the remote server.

To transfer a file from the remote server to the local machine, use the get command followed by the path to the remote file:

```
sftp> get /remote/path/to/file
```

This will transfer the specified file from the remote server to the current directory on the local machine.


## Other Protocols

In addition to SCP and SFTP, there are several other protocols and tools that can be used for file sharing:

* FTP (File Transfer Protocol) is the standard Internet protocol for transferring files. It is not as secure as SCP or SFTP, but is widely supported and easy to use.
* Rsync is a fast and efficient file-copying tool that can be used to transfer files between computers. It allows you to transfer only the differences between two files, making it more efficient for transferring large files or frequently-updated files.
* SMB (Server Message Block) is a file-sharing protocol used by Windows machines. It is commonly used in local networks of Windows PCs. To share files between Linux and Windows machines, you can install the Samba software on your Linux machine and connect to it from your Windows machine using SMB.

## Challenges

1. If you don't already have a server, you may set one up using one of several free cloud options (for example, EC2 on Amazon Free Tier) or create a virtual machine with Linux on your PC. 
1. Connect to a remote server using the SSH protocol. This can be done by running the ssh command and specifying the username and server hostname or IP address.
1. Use a non-standard port for the SSH connection. To do this, you will need to specify the port number using the -p flag when running the ssh command.
1. Copy a directory from the remote server to your local machine using the scp command. To do this, you will need to specify the path to the directory on the remote server and the destination directory on your local machine.
1. Upload a directory to the remote server using an SFTP client. To do this, you will need to connect to the server using the server's IP address, port 22, and protocol as SFTP or SSH, and use the client's GUI interface to navigate the directories and transfer the directory to the desired location on the server.
1. Describe the difference between SCP and SFTP.
