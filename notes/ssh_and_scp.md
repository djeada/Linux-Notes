## SSH

SSH (Secure Shell) is a protocol and a tool suite that facilitates secure communications and file transfers between computers over a potentially unsafe network such as the internet. It is commonly utilized by system administrators and developers for the following purposes:

- Securely logging into a remote computer.
- Running commands on a remote computer in a safe manner.
- Transferring files between computers without compromising the integrity or confidentiality of the data.
- Tunneling other protocols (like HTTP) through encrypted channels.
- Administering databases and other server resources remotely.

```
  Client                                Server
     |                                      |
     |  1. Request to Connect (via SSH)  -> |
     |                                      |
     |  <- 2. Sends Server's Public Key ----|
     |                                      |
     | 3. Creates Encrypted Session Key --> |
     | (using server's public key)          |
     |                                      |
     |  <- 4. Decrypts Session Key (using   |
     | private key) & establishes session   |
     |                                      |
     | 5. Client Authenticates using ->     |
     | its private key                      |
     |                                      |
     |  <- 6. Verifies using stored public  |
     | key of the client & grants access    |
     |                                      |
     | 7. Secure Communication Channel      |
     | (both ways using session key)        |
     |______________________________________|
```

SSH leverages public-key cryptography to authenticate users and to secure the data being transferred. This ensures that only authorized users can connect, and the data cannot be intercepted in a readable format by malicious actors.

### Connecting with SSH

To initiate a connection using SSH, you require several details and credentials which include:

1. The target computer's IP address or hostname.
2. Your username on the remote system.
3. A secure password or a cryptographic key pair for authentication.

Utilize the following command syntax to connect:

```sh
ssh username@serverhost
```

Depending upon the authentication method chosen, the server will either prompt you for a password (password authentication) or verify the cryptographic key presented (key authentication).

### Advanced SSH Connection Options

The ssh command accommodates various flags that allow you to customize your connection further. Here are some notable options:

- `-l`: Specifies the username for the connection, an alternative way to include the username is ssh -l username serverhost.
- `-i`: Designates the path to the private key file used for key authentication. By default, SSH searches for the key file in the ~/.ssh/id_rsa directory.
- `-F`: Indicates the path to the connection configuration file. While each user maintains a personalized connection configuration file at ~/.ssh/config, a global configuration is stored at /etc/ssh/ssh_config.
- `-p`: Allows you to specify a different port if the server is not using the default SSH port (22).
- `-v, -vv, -vvv`: These options increase the verbosity of the SSH command, which is useful for troubleshooting.

For example SSH usually uses port 22, but you can use another port for better security. To use a different port, like 561, do this:

```
ssh -p 561 username@serverhost
```

### Generating SSH Keys

SSH employs a public-key cryptography system, not only to ascertain the identity of the remote machine but also to facilitate the remote computer in authenticating the user. In this mechanism, each user generates a pair of cryptographic keys: a private key (kept secret and safe) and a public key (shared with the remote systems). This key-based authentication method significantly bolsters security by minimizing the risk associated with password brute-force attacks.

To initiate the process of generating a new key pair, you use the `ssh-keygen` command. The `-t` flag allows you to specify the type of key to generate. Common choices are RSA (a widely used algorithm) and Ed25519 (a modern algorithm with enhanced security features). You can also specify the key's bit size using the `-b` flag for added security, as demonstrated below:

```sh
ssh-keygen -t rsa -b 2048
# or for a more secure option
ssh-keygen -t ed25519
```

Post-creation, your keys will be housed in the ~/.ssh directory. Utilize the ls -a ~/.ssh/ command to enumerate the files in this directory and locate your fresh key pair.

### Sharing Your Public Key with Remote Host

In order to harness your newly created key pair for secure connections, the remote server needs to be aware of your public key. This can be achieved by employing the ssh-copy-id command, which securely copies your public key to the remote host's authorized keys. Here’s how you can execute it:

```sh
ssh-copy-id -i ~/.ssh/id_rsa.pub username@serverhost
# or if you used the ed25519 algorithm
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@serverhost
```

Make sure to replace username, serverhost, and the key file name (if you named your key file something other than the default) with the appropriate values. This step is essential to pave the way for passwordless, secure connections to the remote host.

Remember, protect your private key meticulously as it acts as your cryptographic signature, and losing control over it can compromise the security of your remote connections.

### Connecting to Remote Host with Your SSH Key

Once the public key is shared, you can establish connections seamlessly and securely using your SSH key. The command to connect incorporates the key file and resembles the structure below:

```sh
ssh -i ~/.ssh/id_rsa username@serverhost
# or if you used the ed25519 algorithm
ssh -i ~/.ssh/id_ed25519 username@serverhost
```

This method enhances the security and efficiency of your remote connections, fostering a secure and streamlined workflow.

### Setting Up the SSH Service on Your Server

Before connecting, ensure that the SSH daemon (sshd) is up and running on your server. On Debian-based systems, you can set up and start the SSH service using the following commands:

```sh
sudo apt update
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

These commands will install the SSH server package, enable the SSH service to start at boot, and initiate the SSH service immediately, making your server ready to accept secure connections.

## Transferring Files with SCP

SCP (Secure Copy Protocol), which utilizes SSH for data transfer, offers a secure method for transferring files between computers over a network. Here's how you can leverage SCP for various tasks:

### Uploading Files to a Remote Server

To upload a file from your local machine to a remote server, use the following syntax:

```sh
scp /local/path/to/file username@server:/remote/path/to/file
```

### Downloading Files from a Remote Server

To retrieve a file from a remote server to your local machine, utilize the command below:

```sh
scp username@server:/remote/path/to/file /local/path/to/file
```

### Additional Options

SCP also supports additional flags that can enhance your file transfer operations:

- `-r`: Enables recursive copying of directories.
- `-P`: Allows you to specify a different port if the server is not using the default SSH port (22).

For example, to copy a directory recursively over a specified port, use:

```sh
scp -P 80 -r root@server:/remote/path/to/directory /local/path/to/directory
```

## Transferring Files with SFTP

Secure File Transfer Protocol (SFTP) is a secure method for transferring files between a local and a remote computer. It operates over the SSH protocol, providing encrypted network communication. SFTP is preferred over older protocols like FTP due to its enhanced security features, including secure data transfer and manipulation capabilities within the remote file system.

###  Server Setup

1. SSH as the Underlying Protocol:
   - SFTP works over the SSH protocol. This means that it uses the same port and encryption mechanisms as SSH.
   - If you have SSH access to a server, it typically implies that you can use SFTP as well, as long as the SFTP subsystem is enabled on the server.

2. Configure SSH Server:
   - SFTP depends on the SSH server configuration. It uses the SSH server's settings for port numbers, encryption types, and authentication methods.
   - The SSH configuration file (usually `/etc/ssh/sshd_config`) should have an entry like `Subsystem sftp /usr/lib/openssh/sftp-server` to enable SFTP service.

3. Apply the changes by restarting the SSH service (`sudo systemctl restart ssh`).

### Client Setup

- For command-line usage, no additional installation is required as SFTP comes with most SSH clients.
- For a GUI, install clients like WinSCP, FileZilla, or CyberDuck.

### Connecting to a Remote Server via SFTP

To connect to a remote server using SFTP, follow these steps:

1. Open Terminal or Command Line:
   - On Unix-like systems, open your terminal.
   - On Windows, you can use PowerShell, CMD, or an SSH client like PuTTY.

2. Use the command `sftp username@serverhost` where `username` is your account on the remote server, and `serverhost` is the hostname or IP address of the server.

```sh
sftp username@serverhost
```

3. Authenticate:
   - Enter your password when prompted.
   - If you've set up SSH key authentication, you might not need to enter a password.

### Basic SFTP Commands

Once connected, you can use several commands to manage files:

 - `ls`: Z Lists files and directories in the current directory on the remote server.
 - `cd`: Changes the current directory on the remote server.
 - `put local_file`: Uploads a file from your local machine to the current directory on the remote server.
 - `get remote_file`: Downloads a file from the current directory on the remote server to your local machine.
 - `mkdir directory_name`: Creates a new directory on the remote server.
 - `rmdir directory_name`: Removes a directory on the remote server.
 - `rm file_name`: Deletes a file on the remote server.
 - `exit`: Closes the SFTP session.

Here's how you might use these commands in a session:

```bash
sftp> ls
sftp> cd /path/to/directory
sftp> put /local/path/to/file
sftp> get /remote/path/to/file
sftp> mkdir new_directory
sftp> rmdir old_directory
sftp> rm unwanted_file
sftp> exit
```
   
## Other Protocols for File Transfers

Aside from SCP and SFTP, numerous other protocols and tools can be utilized for transferring files, each with their own characteristics:

- **FTP**: A traditional protocol for file transfers, but lacking modern security features. It's generally recommended to avoid FTP for sensitive data transfers.
- **Rsync**: A fast and efficient tool for synchronizing large sets of files across systems, offering options for incremental transfers.
- **SMB**: A protocol commonly used by Windows systems for sharing files over local networks, it also offers support for various authentication mechanisms to protect data access.

## Challenges

- Server Setup
  - Setup your own server environment using a free cloud provider option such as AWS, Google Cloud, or Azure. Alternatively, you can use a virtualization solution like VirtualBox to set up a virtual machine (VM).
  - Install a Linux distribution (like Ubuntu or CentOS) on your server or VM, ensuring that it is configured with a static IP address.
  - Secure your server by setting up a firewall, disabling root login, and installing necessary security updates.

- Connecting via SSH
  - Connect to your server using the SSH protocol.
  - Try to connect using both password authentication and key-based authentication, understanding the pros and cons of each method.
  - Document any errors or issues you encounter during the connection process and research how to resolve them.

- SSH Port Configuration
  - Modify the SSH configuration to allow connections on a non-standard port (other than 22).
  - Reconnect to the server using the newly specified port, verifying that the connection is successful.
  - Discuss the security implications of using a non-standard port for SSH.

- Utilizing SCP for File Transfer
  - Copy a folder containing several files from the server to your local computer using the SCP protocol.
  - Experiment with different SCP options, such as recursive copy and specifying a different port.
  - Log the transfer times and any other notable observations during the transfer process.

- Leveraging SFTP for File Management
  - Connect to the server using an SFTP client.
  - Upload a folder containing multiple files and subdirectories to the server using SFTP.
  - Use the SFTP client to navigate the remote file system, creating and deleting folders as necessary.
  - Test the file permissions settings by trying to access files with different user accounts.

- Understanding Transfer Protocols
  - Write a detailed explanation of the differences between SCP and SFTP, highlighting their underlying protocols and use cases.
  - Compare the transfer speed, security, and versatility of SCP and SFTP by transferring various types of files of different sizes.
  - Research and discuss other file transfer protocols like FTP and Rsync, comparing them to SCP and SFTP in terms of security and functionality.
