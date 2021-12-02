<h1>SSH</h1>

SSH is a network protocol for securely communicating with remote machines. It is used to securely log into a remote machine and execute commands on it.

* <code>ssh</code> is a safe option for remote login as well as command execution on a remote system. 
* It is a set of standards and a network protocol that allow a secure connection to be established between a local and a distant computer.
* To authenticate the remote computer and allow the remote computer to authenticate the user, it employs public-key cryptography.

Uses:
* Allows to connect to a remote machines and run commands on it.
* Supports arbitrary TCP port forwarding through SOCKS proxy.
* SFTP or SCP protocols are used for secure file transmission.

<h2>Connect with remote host</h2>

In order to connect to a remote host, you need to know the host's IP address, the username and password or store the public key on the remote host.

General syntax:

```bash
ssh username@serverhost
```

Server will request a password if you don't use key authentication.

There are number of flags:
* <code>-l</code> to specify the user name.
* <code>-i</code> path to key file (by default it is set to ~/.ssh/id_rsa).
* <code>-F</code> path to connection config file (by default it is set to ~/.ssh/config).

Each user has it's own connection config file, but there is also a global connection config file located at: /etc/ssh/ssh_config.

Make sure that sshd service on your server up and running. For Debian based distros, you can use:

```bash
apt install openssh-server
systemctl enable ssh
systemctl start ssh
```

<h2>Key generation</h2>

* Private key: You keep it on your machine.
* Public key: You send it to the machines you want to get remote access to.

To generate a new key pair, use:

```bash
ssh-keygen  -t rsa
```

In your .ssh directory, you should now have an RSA public and private key pair:

```bash
ls -a ~/.ssh/
```

<h2>Upload the public key to remote host</h2>

The <code>ssh-copy-id</code> command copies the ssh public key to the remote host.

```bash
ssh-copy-id -i ~/.ssh/mykey username@serverhost
```

<h2>Using non-standard ports</h2>
By default, ssh uses port 22. Changing it to a different number improves the security of most servers significantly. You must change the /etc/ssh/sshd_config file on the server to do this. 

For example, if you want to use port 561, you would add the following line to the /etc/ssh/sshd_config file:

```
Port 561
```

When logging in to the server, you now need to specify the port number.

<h1>Sharing files between the machines</h1>

After you've mastered remote login with ssh, you could realize that simply connecting to the remote system isn't enough.
You might want to complete the following tasks:

* Copying files from your server to your desktop computer
* Adding pictures, audio files, or videos to your website
* Copying some text or source code from your desktop computer to your server 

<h2>Overview of the protocols</h2>

A Linux server can exchange files in a variety of methods, including:

* Scp: A simple file-copying utility.
* FTP: The standard Internet file sharing protocol.
* SFTP: file access and copying over the SSH protocol 
* Rsync: File copying is a quick and fast process.
* SMB: Microsoft's file-sharing protocol, which is helpful in a local network of Windows PCs. 

<h2>Scp</h2>
<code>Scp</code> is a safe method of moving files from one computer to another. It functions similarly to the UNIX cp command, except that the parameters can specify a user, machine, and files.

To transfer /opt/test from your machine to the /opt dir on the server with IP 192.168.2.105, use the following commands:

```bash
scp /opt/test 192.168.2.105:/opt
```

Using root credentials, copy /etc/passwd from the server:

```bash
scp root@192.168.2.105:/etc/passwd
```

To recursively copy the whole directory, use:

```bash
scp -r root@192.168.2.105:/etc/passwd
```

Use -P flag to specify the connection port (by default it set to 22):

```bash
scp -P 80 -r root@192.168.2.105:/etc/passwd
```

<h2>SFTP</h2>
SFTP offers a lot of significant advantages:

* High-quality security.
* Allows you to navigate the directory structure.
* Folders can be created and deleted.
* On your server, no further configuration is necessary. 

Client software is required to use SFTP. If you're using a Linux desktop, your file manager has a built-in GUI client. Although neither Windows nor macOS offer a built-in GUI client, there are a plethora of third-party alternatives, both free and commercial, available:

* For Windows users, use WinSCP or FileZilla.
* For macOS users, utilize CyberDuck or FileZilla.

Configuring and use your preferred option should be simple. When prompted for server, enter your server's IP address, port 22, and protocol as SFTP or SSH. 

<h1>Challenges</h1>

1. Use SSH protocol to log into a remote server. If you don't already have a server, you may set one up using one of several free cloud options (for example, EC2 on Amazon Free Tier) or create a virtual machine with Linux on your PC. 
2. Use a non-standard port (e.g. 6176) for the SSH connection.
3. Use <code>scp</code> to copy /var/log directory from the server to your desktop.
4. To upload the images directory to your server, use an <code>SFTP</code> GUI of your choice. Using <code>SFTP</code>, try creating various temporary folders, changing their location, and deleting them at the end. 
5. Use <code>scp</code> to copy the contents of the /etc/passwd file from your server to your local machine.
6. Explain the difference between <code>SCP</code> and <code>SFTP</code>.
