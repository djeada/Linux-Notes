#### Q. What does SSH stand for?

* [ ] Simple Shell
* [x] Secure Shell
* [ ] System Shell
* [ ] Standard Shell
* [ ] Server Shell

#### Q. What is the default port number for SSH?

* [ ] 21
* [x] 22
* [ ] 23
* [ ] 25
* [ ] 80

#### Q. Which command connects to a remote server using SSH?

* [ ] `ssh server username`
* [x] `ssh username@server`
* [ ] `connect username@server`
* [ ] `remote username@server`
* [ ] `login username@server`

#### Q. Which command generates a new SSH key pair?

* [ ] `ssh-add`
* [x] `ssh-keygen`
* [ ] `ssh-create`
* [ ] `ssh-newkey`
* [ ] `ssh-generate`

#### Q. Where are SSH private keys typically stored?

* [ ] `/etc/ssh/`
* [x] `~/.ssh/`
* [ ] `/var/ssh/`
* [ ] `~/keys/`
* [ ] `/home/ssh/`

#### Q. Which file contains the public keys authorized to log into a user's account?

* [ ] `~/.ssh/known_hosts`
* [ ] `~/.ssh/id_rsa`
* [x] `~/.ssh/authorized_keys`
* [ ] `~/.ssh/config`
* [ ] `~/.ssh/identity`

#### Q. Which command copies your public key to a remote server for key-based authentication?

* [ ] `ssh-add`
* [ ] `ssh-keygen -c`
* [x] `ssh-copy-id`
* [ ] `scp ~/.ssh/id_rsa.pub`
* [ ] `ssh-upload`

#### Q. What encryption algorithm is considered more secure and modern for SSH keys?

* [ ] RSA-1024
* [ ] DSA
* [x] Ed25519
* [ ] MD5
* [ ] SHA1

#### Q. Which SSH option specifies a non-default port to connect to?

* [ ] `-l`
* [x] `-p`
* [ ] `-i`
* [ ] `-o`
* [ ] `-P`

#### Q. Which SSH option specifies a private key file for authentication?

* [ ] `-k`
* [ ] `-p`
* [x] `-i`
* [ ] `-f`
* [ ] `-K`

#### Q. What does SCP stand for?

* [ ] Simple Copy Protocol
* [x] Secure Copy Protocol
* [ ] System Copy Protocol
* [ ] Server Copy Protocol
* [ ] Shell Copy Protocol

#### Q. Which command uploads a file to a remote server using SCP?

* [ ] `scp username@server:/remote/file /local/file`
* [x] `scp /local/file username@server:/remote/path/`
* [ ] `scp --upload /local/file server`
* [ ] `cp /local/file ssh://username@server/remote/`
* [ ] `upload /local/file username@server`

#### Q. Which command downloads a file from a remote server using SCP?

* [x] `scp username@server:/remote/file /local/path/`
* [ ] `scp /local/path/ username@server:/remote/file`
* [ ] `scp --download server:/remote/file`
* [ ] `download username@server:/remote/file`
* [ ] `get username@server:/remote/file`

#### Q. Which SCP option enables recursive directory copying?

* [ ] `-d`
* [x] `-r`
* [ ] `-R`
* [ ] `-a`
* [ ] `-c`

#### Q. Which SCP option specifies a non-default port?

* [ ] `-p`
* [x] `-P`
* [ ] `-o`
* [ ] `-port`
* [ ] `-n`

#### Q. What does SFTP stand for?

* [ ] Simple File Transfer Protocol
* [x] Secure File Transfer Protocol
* [ ] System File Transfer Protocol
* [ ] Server File Transfer Protocol
* [ ] Standard FTP

#### Q. Which command starts an interactive SFTP session?

* [ ] `ftp username@server`
* [x] `sftp username@server`
* [ ] `ssh --ftp username@server`
* [ ] `connect-sftp username@server`
* [ ] `ftps username@server`

#### Q. In an SFTP session, which command uploads a local file to the remote server?

* [ ] `upload filename`
* [x] `put filename`
* [ ] `send filename`
* [ ] `copy filename`
* [ ] `push filename`

#### Q. In an SFTP session, which command downloads a file from the remote server?

* [ ] `download filename`
* [x] `get filename`
* [ ] `receive filename`
* [ ] `fetch filename`
* [ ] `pull filename`

#### Q. Which file stores known host keys for SSH connections?

* [ ] `~/.ssh/authorized_keys`
* [ ] `~/.ssh/id_rsa.pub`
* [x] `~/.ssh/known_hosts`
* [ ] `~/.ssh/config`
* [ ] `~/.ssh/identity`

#### Q. Which SSH configuration file is used to define connection settings per host?

* [ ] `~/.ssh/known_hosts`
* [ ] `~/.ssh/authorized_keys`
* [x] `~/.ssh/config`
* [ ] `/etc/ssh/sshd_config`
* [ ] `~/.ssh/options`

#### Q. What is the main SSH server configuration file?

* [ ] `/etc/ssh/ssh_config`
* [x] `/etc/ssh/sshd_config`
* [ ] `/etc/ssh/config`
* [ ] `/etc/sshd.conf`
* [ ] `/var/ssh/sshd_config`

#### Q. Which SSH option increases verbosity for debugging connection issues?

* [ ] `-d`
* [x] `-v`
* [ ] `-V`
* [ ] `-debug`
* [ ] `-D`

#### Q. What type of cryptography does SSH use for secure authentication?

* [ ] Symmetric cryptography only
* [x] Public-key cryptography
* [ ] Hash-based cryptography only
* [ ] Caesar cipher
* [ ] No encryption

#### Q. Which command enables the SSH service to start at boot on a systemd-based system?

* [ ] `systemctl start ssh`
* [x] `systemctl enable ssh`
* [ ] `service ssh enable`
* [ ] `ssh --enable`
* [ ] `chkconfig ssh on`

#### Q. What is the purpose of SSH agent?

* [ ] To generate new SSH keys
* [x] To hold private keys in memory for passwordless authentication
* [ ] To configure SSH server settings
* [ ] To transfer files securely
* [ ] To scan for SSH vulnerabilities

#### Q. Which command adds a private key to the SSH agent?

* [ ] `ssh-keygen`
* [x] `ssh-add`
* [ ] `ssh-agent add`
* [ ] `ssh-key add`
* [ ] `ssh-load`

#### Q. Which protocol does SFTP run over?

* [ ] FTP
* [x] SSH
* [ ] HTTP
* [ ] TLS
* [ ] Telnet

#### Q. What does the `-l` option do in the `ssh` command?

* [x] Specifies the login username
* [ ] Lists available hosts
* [ ] Enables logging
* [ ] Sets the local port
* [ ] Loads a key file

#### Q. Which command can be used to securely tunnel another protocol through SSH?

* [ ] `ssh-tunnel`
* [x] `ssh -L`
* [ ] `ssh-forward`
* [ ] `sshtunnel`
* [ ] `ssh-proxy`

#### Q. What is the minimum recommended key size for RSA SSH keys?

* [ ] 512 bits
* [ ] 1024 bits
* [x] 2048 bits
* [ ] 4096 bits
* [ ] 8192 bits

#### Q. Which SSH option disables strict host key checking?

* [ ] `-o NoHostKey=yes`
* [ ] `-o IgnoreHostKey=yes`
* [x] `-o StrictHostKeyChecking=no`
* [ ] `-o DisableHostCheck=yes`
* [ ] `-o SkipHostKey=yes`

#### Q. What does the `-X` option enable when connecting via SSH?

* [ ] Extra verbose output
* [x] X11 forwarding for graphical applications
* [ ] XML output format
* [ ] Extended authentication
* [ ] Xterm mode

#### Q. What does the `-D` option do in SSH?

* [ ] Disables password authentication
* [x] Creates a dynamic SOCKS proxy
* [ ] Enables debug mode
* [ ] Downloads files
* [ ] Deletes remote files

#### Q. What is the purpose of the `ssh-agent`?

* [ ] To generate SSH keys
* [x] To cache SSH private keys in memory for passwordless authentication
* [ ] To manage SSH connections
* [ ] To configure SSH settings
* [ ] To monitor SSH traffic

#### Q. Which command adds a private key to the ssh-agent?

* [ ] `ssh-keygen -a`
* [x] `ssh-add`
* [ ] `ssh-agent add`
* [ ] `ssh-load`
* [ ] `ssh-import`

#### Q. What does the `-N` option do in an SSH command?

* [ ] Enables null authentication
* [x] Does not execute a remote command (useful for port forwarding)
* [ ] Uses numeric IP addresses
* [ ] Disables host key checking
* [ ] Enables NAT traversal

#### Q. How do you specify a different SSH configuration file?

* [ ] `ssh --config file`
* [x] `ssh -F file`
* [ ] `ssh -c file`
* [ ] `ssh -C file`
* [ ] `ssh --file file`

#### Q. What is the purpose of the `~/.ssh/config` file?

* [ ] To store SSH keys
* [x] To define connection settings for specific hosts
* [ ] To log SSH connections
* [ ] To store known hosts
* [ ] To configure the SSH daemon

#### Q. Which SCP option preserves file modification times and permissions?

* [ ] `-r`
* [x] `-p`
* [ ] `-v`
* [ ] `-C`
* [ ] `-q`

#### Q. What does the `-C` option do in SSH and SCP?

* [ ] Clears the screen
* [x] Enables compression
* [ ] Checks connection
* [ ] Creates directories
* [ ] Copies recursively

#### Q. Which command displays the fingerprint of an SSH key?

* [ ] `ssh-keygen -p`
* [x] `ssh-keygen -lf`
* [ ] `ssh-add -l`
* [ ] `ssh-fingerprint`
* [ ] `ssh-show`

#### Q. What is the default location for the SSH server configuration file?

* [ ] `~/.ssh/sshd_config`
* [x] `/etc/ssh/sshd_config`
* [ ] `/etc/sshd.conf`
* [ ] `/var/ssh/config`
* [ ] `/usr/ssh/sshd_config`

#### Q. Which directive in sshd_config disables password authentication?

* [ ] `NoPassword yes`
* [x] `PasswordAuthentication no`
* [ ] `DisablePassword yes`
* [ ] `AuthPassword no`
* [ ] `PasswordLogin no`

#### Q. What is SOCKS proxy mode in SSH?

* [ ] A secure file transfer mode
* [x] Dynamic port forwarding that creates a local SOCKS proxy
* [ ] A compression algorithm
* [ ] A key exchange method
* [ ] A connection pooling feature
