<h2>ssh</h2>

* <i>ssh</i> is a safe option for remote login as well as command execution on a remote system. 
* It is a set of standards and a network protocol that allow a secure connection to be established between a local and a distant computer.
* To authenticate the remote computer and allow the remote computer to authenticate the user, it employs public-key cryptography.

Uses:
* connect in to a distant system and run commands using tunneling
* arbitrary TCP port forwarding through SOCKS proxy
* SFTP or SCP protocols are used for secure file transmission

<h2>Connect with remote host</h2>

```bash
ssh username@serverhost
```

Server will request a password if you don't use key authentication.

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

<h2>scp</h2>
<i>scp</i> is a safe method of moving files from one computer to another. It functions similarly to the UNIX cp command, except that the parameters can specify a user, machine, and files.
