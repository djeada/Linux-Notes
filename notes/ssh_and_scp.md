<h2>ssh</h2>

* <i>ssh</i> is a safe option for remote login as well as command execution on a remote system. 
* It is a set of standards and a network protocol that allow a secure connection to be established between a local and a distant computer.
* To authenticate the remote computer and allow the remote computer to authenticate the user, it employs public-key cryptography.

Uses:
* connect in to a distant system and run commands using tunneling
* arbitrary TCP port forwarding through SOCKS proxy
* SFTP or SCP protocols are used for secure file transmission

<h2>Connect with remote host</h2>

General syntax:

```bash
ssh username@serverhost
```

Server will request a password if you don't use key authentication.

There are number of flags:
* <i>-l</i> to specify the user name.
* <i>-i</i> path to key file (by default it is set to ~/.ssh/id_rsa).
* <i>-F</i> path to connection config file (by default it is set to ~/.ssh/config).

Each user has it's own connection config file, but there is also a global connection config file located at: /etc/ssh/ssh_config.

<h2>Key generation</h2>

* Private key: You keep it on your machine.
* Public key: You send it to the machines you want to get remote access to.

To generate a new key pair, use:

```bash
ssh-keygen  -t rsa
```

In your.ssh directory, you should now have an RSA public and private key pair:

```bash
ls -a ~/.ssh/
```

<h2>Upload the public key to remote host</h2>

The <i>ssh-copy-id</i> command copies the ssh public key to the remote host.

```bash
ssh-copy-id -i ~/.ssh/mykey username@serverhost
```

<h2>Using non-standard ports</h2>
By default, ssh uses port 22. Changing it to a different number improves the security of most servers significantly. You must change the /etc/ssh/sshd file on the server to do this. 

<h2>scp</h2>
<i>scp</i> is a safe method of moving files from one computer to another. It functions similarly to the UNIX cp command, except that the parameters can specify a user, machine, and files.

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

<h1>Challenges</h1>

1. Use ssh to login to a remote server. If you don't already have a server, you may set one up using one of several free cloud options (for example, EC2 on Amazon Free Tier) or a virtual machine installed on your PC. 
2. Use a non-standard port (e.g. 6176) for ssh connection.
