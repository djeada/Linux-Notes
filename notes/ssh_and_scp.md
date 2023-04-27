## Simple Explanation of SSH

SSH (Secure Shell) is a tool and method for safely connecting, controlling, and transferring files between computers over the internet. It is used for:
- Logging into a remote computer
- Running commands on a remote computer
- Transferring files securely between computers

SSH uses public-key cryptography to make sure only authorized users can connect.

## Connecting with SSH

To connect using SSH, you need:
1. The other computer's IP address
2. Your username and password (or a special key)

Use this command to connect:

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

## Generating SSH Keys

SSH uses a public-key cryptography system to authenticate the remote computer and allow the remote computer to authenticate the user. This means that each user generates a pair of keys (a private key and a public key) and the user's public key is stored on the remote machine. To generate a new key pair, use the `ssh-keygen` command with the `-t` flag to specify the type of key to generate, such as rsa:

```
ssh-keygen  -t rsa
```

Your keys will be in the `~/.ssh` folder. You can use the `ls -a ~/.ssh/` command to list the files in this directory and see the new key pair.

## Sharing Your Public Key with Remote Host

To use your key to connect, the remote computer needs your public key. Send it using:

```
ssh-copy-id -i ~/.ssh/mykey username@serverhost
```

## Using Non-Standard Ports

SSH usually uses port 22, but you can use another port for better security. To use a different port, like 561, do this:

```
ssh -p 561 username@serverhost
```

## Transferring Files with SCP

SCP (Secure Copy Protocol) is a way to move files between computers securely. To send a file to the other computer, use:

```
scp /local/path/to/file username@server:/remote/path/to/file
```

To get a file from the other computer, use:

```
scp username@server:/remote/path/to/file /local/path/to/file
```

You can use the `-r` flag to copy directories recursively, and the `-P` flag to specify the connection port (the default is 22). For example:

```
scp -P 80 -r root@server:/remote/path/to/directory /local/path/to/directory
```

## Transferring Files with SFTP

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

- FTP: An older way to move files. Not very secure.
- Rsync: Fast and efficient for moving lots of files.
- SMB: Used by Windows computers to share files on a local network.

## Challenges

1. Set up your own server using a free cloud option or a virtual machine.
2. Connect to it using SSH.
3. Use a different port for SSH.
4. Copy a folder from the server to your computer with SCP.
5. Upload a folder to the server using SFTP.
6. Explain the difference between SCP and SFTP.

