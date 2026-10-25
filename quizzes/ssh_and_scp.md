# SSH and SCP Quiz

Notes: [Secure Server Access](../notes/ssh_and_scp.md), [Ports](../notes/ports.md), [File Compression and Archiving](../notes/tar_and_gzip.md)

Check your understanding of SSH connections, key-based authentication, tunnels and secure file transfer with SCP, SFTP and rsync.

#### Q. Which command connects to `server.example.com` as user `deploy`?

* [x] `ssh deploy@server.example.com`
* [ ] `ssh server.example.com@deploy`
* [ ] `ssh -u deploy server.example.com`
* [ ] `ssh server.example.com -user deploy`

> **Explanation:** The form is `ssh user@host`. The equivalent option form is `ssh -l deploy server.example.com`; `ssh` has no `-u` or `-user` option.

#### Q. How do you run `df -h` on `server` and see its output locally, without opening an interactive shell?

* [ ] `ssh -N user@server df -h`
* [x] `ssh user@server 'df -h'`
* [ ] `ssh user@server; df -h`
* [ ] `ssh -D df user@server`

> **Explanation:** A command after the host runs on the remote side, and its output comes back to your terminal. In `ssh user@server; df -h` the `df` runs locally after the session ends, and `-N` runs no command at all.

#### Q. Local user `alice` (home `/home/alice`) runs the command below in bash. What does it print?

```bash
ssh bob@server "echo $HOME"
```

* [ ] `/home/bob`
* [ ] `$HOME`
* [x] `/home/alice`
* [ ] An empty line

> **Explanation:** Inside double quotes the local shell expands `$HOME` before `ssh` runs, so the remote side receives `echo /home/alice`. Single quotes, `'echo $HOME'`, pass the variable through unexpanded and print `/home/bob`.

#### Q. `ssh user@server tty` prints `not a tty`, and full-screen programs such as `top` misbehave when run this way. Which option forces a pseudo-terminal?

* [ ] `-T`
* [ ] `-N`
* [ ] `-X`
* [x] `-t`

> **Explanation:** When a remote command is given, `ssh` does not allocate a terminal by default. `-t` requests one, so `ssh -t user@server top` works. `-T` explicitly disables terminal allocation, `-N` runs no command and `-X` forwards X11.

#### Q. The SSH server listens on port 2222. Which command connects to it?

* [ ] `ssh -P 2222 user@host`
* [ ] `ssh user@host:2222`
* [ ] `ssh -l 2222 user@host`
* [x] `ssh -p 2222 user@host`

> **Explanation:** `ssh` takes a lowercase `-p` for the port. `scp` and `sftp` use uppercase `-P` because their `-p` means "preserve times and modes". `user@host:2222` is not port syntax for `ssh`; the URI form `ssh://user@host:2222` is.

#### Q. Which command generates a new Ed25519 key pair?

* [ ] `ssh-add -t ed25519`
* [x] `ssh-keygen -t ed25519`
* [ ] `ssh-copy-id -t ed25519`
* [ ] `ssh-keyscan -t ed25519`

> **Explanation:** `ssh-keygen -t TYPE` creates a key pair, here `~/.ssh/id_ed25519` and `id_ed25519.pub`. Since OpenSSH 9.5 Ed25519 is also the default type. For RSA, `ssh-keygen` defaults to 3072 bits; avoid anything below 2048.

#### Q. After running `ssh-keygen -t ed25519`, which file must stay secret?

* [x] `~/.ssh/id_ed25519`
* [ ] `~/.ssh/id_ed25519.pub`
* [ ] `~/.ssh/known_hosts`
* [ ] `~/.ssh/authorized_keys`

> **Explanation:** The file without `.pub` is the private key; anyone holding it can log in as you wherever the public key is trusted. The `.pub` file is meant to be copied to servers.

#### Q. Which command installs your public key on a server so that later logins can use key authentication?

* [ ] `ssh-add ~/.ssh/id_ed25519.pub`
* [ ] `scp ~/.ssh/id_ed25519 user@server:~/.ssh/`
* [x] `ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server`
* [ ] `ssh-keygen -y user@server`

> **Explanation:** `ssh-copy-id` appends the public key to `~/.ssh/authorized_keys` on the server, creating it if needed. Copying the private key, as in the `scp` option, defeats the point of key pairs.

#### Q. On the server, which file lists the public keys allowed to log in to a user account?

* [ ] `~/.ssh/known_hosts`
* [ ] `~/.ssh/config`
* [ ] `/etc/ssh/ssh_config`
* [x] `~/.ssh/authorized_keys`

> **Explanation:** `sshd` checks the target user's `~/.ssh/authorized_keys` during public-key authentication. `known_hosts` is the client's record of server host keys.

#### Q. During public-key authentication, what does the client send to prove its identity?

* [ ] The private key, encrypted with the server's public key
* [x] A signature made with the private key, which the server checks against the public key
* [ ] The user's password, hashed with the private key
* [ ] The public key alone, with no further proof

> **Explanation:** The private key never leaves the client. The server verifies the signature using the public key in `authorized_keys`, all inside the already-encrypted session.

#### Q. `ssh` refuses to use your key and warns `UNPROTECTED PRIVATE KEY FILE!`. Which command fixes it?

* [ ] `chmod 644 ~/.ssh/id_ed25519`
* [ ] `chmod 640 ~/.ssh/id_ed25519`
* [x] `chmod 600 ~/.ssh/id_ed25519`
* [ ] `chmod 755 ~/.ssh/id_ed25519`

> **Explanation:** OpenSSH ignores a private key that the group or other users can access, so even `640` is rejected as "too open". Mode `600` (or `400`) limits the file to its owner. The `~/.ssh` directory itself is normally `700`.

#### Q. Your public key is in the server's `~/.ssh/authorized_keys`, yet `sshd` keeps rejecting it. On the server, `ls -ld ~` shows `drwxrwxrwx`. What is the likely cause?

* [ ] The key type is not supported by the server
* [ ] `authorized_keys` must be owned by root
* [ ] The client's `known_hosts` entry for the server is stale
* [x] `sshd`'s `StrictModes` check rejects keys when the home directory is writable by others

> **Explanation:** With the default `StrictModes yes`, `sshd` ignores `authorized_keys` if the home directory, `~/.ssh` or the file is writable by group or others, since anyone could have added a key. Run `chmod 755 ~` (or `go-w`) and check the server's auth log.

#### Q. Which option tells `ssh` to use a specific private key file?

* [x] `-i ~/.ssh/work_key`
* [ ] `-k ~/.ssh/work_key`
* [ ] `-f ~/.ssh/work_key`
* [ ] `-p ~/.ssh/work_key`

> **Explanation:** `-i` selects the identity (private key) file. `-f` sends `ssh` to the background, and `-p` sets the port.

#### Q. What does `ssh-agent` do?

* [ ] It generates new key pairs on demand
* [ ] It runs on the server and checks `authorized_keys`
* [ ] It copies public keys to remote servers
* [x] It holds decrypted private keys in memory so you enter each passphrase only once

> **Explanation:** The agent keeps unlocked keys in memory and answers signing requests from `ssh`. You add keys to it with `ssh-add`. The server-side checks are done by `sshd`.

#### Q. Which command loads your private key into the running `ssh-agent`?

* [x] `ssh-add ~/.ssh/id_ed25519`
* [ ] `ssh-keygen -a ~/.ssh/id_ed25519`
* [ ] `ssh-agent ~/.ssh/id_ed25519`
* [ ] `ssh-copy-id ~/.ssh/id_ed25519`

> **Explanation:** `ssh-add` asks for the passphrase once and gives the key to the agent. `ssh-add -l` lists loaded keys. Running `ssh-agent FILE` would try to run `FILE` as a command.

#### Q. Which command prints the fingerprint of the key in `~/.ssh/id_ed25519.pub`?

* [ ] `ssh-keygen -p -f ~/.ssh/id_ed25519.pub`
* [ ] `ssh-keygen -t ~/.ssh/id_ed25519.pub`
* [x] `ssh-keygen -lf ~/.ssh/id_ed25519.pub`
* [ ] `ssh-keygen -R ~/.ssh/id_ed25519.pub`

> **Explanation:** `-l` shows the fingerprint, such as `256 SHA256:... (ED25519)`, and `-f` names the file. `-p` changes a key's passphrase, and `-R` removes a host from `known_hosts`.

#### Q. What is stored in the client's `~/.ssh/known_hosts` file?

* [ ] Public keys of users allowed to log in to this machine
* [x] Host keys of servers you have connected to, used to detect impersonation
* [ ] Hostnames and aliases for your saved connections
* [ ] A log of past SSH sessions

> **Explanation:** On first connection you accept the server's host key, and later connections check it against this file. Aliases belong in `~/.ssh/config`, and user keys in `authorized_keys`.

#### Q. `ssh` warns `REMOTE HOST IDENTIFICATION HAS CHANGED!` for a server. What is the right first step?

* [ ] Delete `~/.ssh/known_hosts` and reconnect
* [ ] Reconnect with `-o StrictHostKeyChecking=no`
* [ ] Generate a new client key with `ssh-keygen`
* [x] Confirm the server's new host-key fingerprint through a trusted channel before trusting it

> **Explanation:** A changed host key may mean a reinstall, or a man-in-the-middle attack. Verify it first; only then remove the old entry with `ssh-keygen -R host`. Deleting entries or disabling checking removes the protection.

#### Q. A server was rebuilt, and you have verified its new host key. Which command removes only its old entry from `~/.ssh/known_hosts`?

* [ ] `ssh-keygen -l -F server.example.com`
* [ ] `ssh-add -d server.example.com`
* [x] `ssh-keygen -R server.example.com`
* [ ] `rm ~/.ssh/known_hosts`

> **Explanation:** `ssh-keygen -R host` deletes that host's keys from `known_hosts` and keeps a backup in `known_hosts.old`. `-F` only finds and prints the entry, `ssh-add -d` removes keys from the agent, and deleting the file discards every saved host key.

#### Q. With this block in `~/.ssh/config`, what does `ssh web` do?

```text
Host web
    HostName 203.0.113.10
    User deploy
    Port 2222
```

* [x] Connects to `203.0.113.10` on port 2222 as user `deploy`
* [ ] Looks up a host named `web` in DNS and connects on port 22
* [ ] Connects to `203.0.113.10` on port 22 as your local username
* [ ] Fails, because `Host` entries are read only by `sshd`

> **Explanation:** A `Host` block defines an alias, and the keywords under it apply when you connect to that alias. `ssh -G web` prints the resulting settings without connecting, and command-line options such as `-p` override the file.

#### Q. `~/.ssh/config` contains the blocks below, in this order. Which port does `ssh web` use?

```text
Host *
    Port 2000

Host web
    HostName 203.0.113.10
    Port 2222
```

* [ ] 2222, because the `web` block is more specific
* [x] 2000, because the first value obtained for each keyword wins
* [ ] 22, because two conflicting `Port` lines cancel out
* [ ] 2222, because later blocks override earlier ones

> **Explanation:** `ssh` reads the file top to bottom and keeps the first value it finds for each keyword, and `Host *` matches every host. Put specific `Host` blocks first and general `Host *` defaults at the end.

#### Q. Which file configures the SSH server daemon, as opposed to the client?

* [ ] `/etc/ssh/ssh_config`
* [ ] `~/.ssh/config`
* [x] `/etc/ssh/sshd_config`
* [ ] `/etc/sshd.conf`

> **Explanation:** The extra `d` stands for daemon: `sshd_config` controls the server, while `ssh_config` and `~/.ssh/config` control the client.

#### Q. Which pair of `sshd_config` settings blocks direct root logins and allows only key-based logins?

* [ ] `PermitRootLogin yes` and `PasswordAuthentication yes`
* [ ] `RootLogin disabled` and `PasswordLogin no`
* [ ] `PermitRootLogin no` and `PubkeyAuthentication no`
* [x] `PermitRootLogin no` and `PasswordAuthentication no`

> **Explanation:** `PermitRootLogin no` blocks root over SSH, and `PasswordAuthentication no` stops password logins (also check `KbdInteractiveAuthentication`). `PubkeyAuthentication no` would turn off keys, the opposite of what you want.

#### Q. `sudo sshd -T` on a stock OpenSSH server shows `permitrootlogin without-password`, the alias of the default `prohibit-password`. What does this allow?

* [x] Root can log in with a key, but not with a password
* [ ] Root cannot log in over SSH by any method
* [ ] Root can log in with a password, but not with a key
* [ ] Root can log in by any method once `PasswordAuthentication yes` is set

> **Explanation:** `prohibit-password` disables password and keyboard-interactive logins for root only, whatever `PasswordAuthentication` says; key logins still work. Use `PermitRootLogin no` to block root entirely.

#### Q. On Ubuntu, you add `PasswordAuthentication no` at the end of `/etc/ssh/sshd_config`, yet `sudo sshd -T | grep -i passwordauth` prints `passwordauthentication yes`. The files are shown below. Why?

```text
# /etc/ssh/sshd_config (first lines)
Include /etc/ssh/sshd_config.d/*.conf

# /etc/ssh/sshd_config.d/50-cloud-init.conf
PasswordAuthentication yes
```

* [ ] `sshd -T` shows compiled-in defaults, not the configuration files
* [ ] Files in `sshd_config.d` always override the main file, wherever the `Include` is
* [x] `sshd` keeps the first value it reads, and the included file is read before your line
* [ ] The setting only takes effect after the server is rebooted

> **Explanation:** Like the client, `sshd` uses the first value obtained for most keywords. The `Include` at the top is read first, so its `yes` wins. Change or remove the drop-in, then check with `sshd -T` before reloading.

#### Q. You edited `/etc/ssh/sshd_config` on a remote server. What is the safest way to apply the change?

* [ ] Reboot the server and reconnect
* [x] Run `sudo sshd -t`, reload the service, and test a new connection before closing the current one
* [ ] Run `sudo systemctl stop ssh`, then start it again from the new session
* [ ] Close your session first, then reconnect to load the new settings

> **Explanation:** `sshd -t` catches syntax errors before they can lock you out. Reloading keeps existing sessions alive, so if the new login fails you can still fix the config from the open session.

#### Q. You changed `sshd` to listen on port 2222 on a server with UFW. Which firewall step is needed so you can still connect?

* [x] `sudo ufw allow 2222/tcp`
* [ ] `sudo ufw deny 2222/tcp`
* [ ] `sudo ufw allow 2222/udp`
* [ ] `sudo ufw delete allow 2222/tcp`

> **Explanation:** SSH uses TCP, so the new port must be allowed before you rely on it; then remove the old port 22 rule. A non-standard port reduces scan noise but does not replace strong authentication.

#### Q. On Ubuntu 24.04, where `sshd` is socket-activated through `ssh.socket`, you change `Port 22` to `Port 2222` in `sshd_config`. What makes it listen on the new port?

* [ ] `sudo systemctl restart ssh.service`
* [x] `sudo systemctl daemon-reload`, then `sudo systemctl restart ssh.socket`
* [ ] `sudo sshd -t`
* [ ] `sudo systemctl reload ssh.socket`

> **Explanation:** systemd, not `sshd`, owns the listening socket. A generator copies `Port` and `ListenAddress` into `ssh.socket`, so you must re-run it with `daemon-reload` and restart the socket. Restarting only `ssh.service` keeps port 22, and socket units cannot be reloaded.

#### Q. Which command makes the SSH service start automatically at boot on Debian 12?

* [x] `sudo systemctl enable ssh`
* [ ] `sudo systemctl start ssh`
* [ ] `sudo systemctl reload ssh`
* [ ] `sudo systemctl status ssh`

> **Explanation:** `enable` creates the links that start the unit at boot, and `start` runs it now; `enable --now` does both. On RPM-based systems the unit is named `sshd`, and on Ubuntu 22.10+ `ssh.socket` starts it on the first connection.

#### Q. Which option increases `ssh` output so you can see where a connection or authentication is failing?

* [ ] `-q`
* [ ] `-V`
* [x] `-v`
* [ ] `-N`

> **Explanation:** `-v` prints debug messages, and `-vv` or `-vvv` add more detail. `-V` prints the version, `-q` suppresses warnings, and `-N` skips the remote command.

#### Q. What does `ssh -L 8080:localhost:5432 user@db.example.com` do?

* [ ] Opens port 8080 on `db.example.com` and forwards it to port 5432 on your machine
* [ ] Starts a SOCKS proxy on local port 8080
* [ ] Copies the database on port 5432 to local port 8080
* [x] Opens port 8080 on your machine and forwards it through SSH to port 5432 on `db.example.com`

> **Explanation:** `-L local_port:dest_host:dest_port` is local forwarding. `localhost` is resolved on the server side, so connecting to `localhost:8080` on your machine reaches the server's local port 5432.

#### Q. After you run `ssh -N -L 8080:localhost:5432 user@db.example.com`, a colleague on your LAN cannot connect to port 8080 on your machine. Why?

* [ ] Local forwarding works only for the user who started `ssh`
* [x] By default `ssh` binds the forwarded port to `127.0.0.1` and `::1` only
* [ ] The colleague must also authenticate to `db.example.com`
* [ ] `-N` makes the tunnel accept only one connection

> **Explanation:** Forwarded ports listen on loopback unless you ask otherwise, which `ss -tln` confirms. To share it, bind explicitly, for example `-L 0.0.0.0:8080:localhost:5432` (or use `-g`), and consider the security impact first.

#### Q. Which option creates a reverse tunnel, so that a port on the remote server forwards back to a service on your machine?

* [x] `-R`
* [ ] `-L`
* [ ] `-D`
* [ ] `-X`

> **Explanation:** `-R remote_port:host:port` opens the listening port on the server and sends connections back through the tunnel; with the server's default `GatewayPorts no` it binds to loopback there. `-L` listens locally, `-D` starts a SOCKS proxy, and `-X` forwards X11.

#### Q. What does `ssh -D 1080 user@host` provide?

* [ ] A debug log written to port 1080
* [x] A local SOCKS proxy on port 1080 that sends traffic out through `host`
* [ ] A forward from local port 1080 to the same port on `host`
* [ ] A disconnect after 1080 seconds of inactivity

> **Explanation:** `-D` sets up dynamic port forwarding. Applications configured to use `localhost:1080` as a SOCKS proxy reach any destination as if they were connecting from `host`.

#### Q. Why add `-N` to a command such as `ssh -N -L 8080:localhost:80 user@host`?

* [ ] It disables host-key checking for the tunnel
* [ ] It uses numeric IP addresses only
* [x] It keeps the tunnel open without running a remote command or shell
* [ ] It compresses traffic through the tunnel

> **Explanation:** `-N` is for forwarding-only sessions. It is often combined with `-f` to send `ssh` to the background after authentication. Compression is `-C`.

#### Q. Which option connects to an internal server through the bastion host `jump.example.com` in a single command?

* [x] `ssh -J user@jump.example.com user@internal`
* [ ] `ssh -L jump.example.com user@internal`
* [ ] `ssh -D jump.example.com user@internal`
* [ ] `ssh -F jump.example.com user@internal`

> **Explanation:** `-J` (ProxyJump) connects to the jump host first and tunnels the SSH connection to the target through it. In `~/.ssh/config` the same thing is written as `ProxyJump`.

#### Q. What does `ssh -X user@host` enable?

* [ ] Extra-verbose debugging output
* [ ] Exclusive access, blocking other sessions
* [ ] Extended key exchange algorithms
* [x] X11 forwarding, so graphical programs on `host` display on your screen

> **Explanation:** `-X` forwards X11 connections through the encrypted tunnel. The server must allow it with `X11Forwarding yes`.

#### Q. Which command copies `report.pdf` from your machine to `/srv/docs/` on `server`?

* [ ] `scp user@server:/srv/docs/ report.pdf`
* [ ] `scp report.pdf server/srv/docs/`
* [x] `scp report.pdf user@server:/srv/docs/`
* [ ] `scp -u report.pdf user@server:/srv/docs/`

> **Explanation:** `scp` works like `cp`: `scp SOURCE DEST`, with remote paths written as `user@host:path`. Without the colon, `server/srv/docs/` is just a local path.

#### Q. Which command downloads `/var/log/app.log` from `server` into the current local directory?

* [ ] `scp . user@server:/var/log/app.log`
* [x] `scp user@server:/var/log/app.log .`
* [ ] `scp -d user@server:/var/log/app.log`
* [ ] `scp user@server /var/log/app.log .`

> **Explanation:** The remote file is the source, so it comes first, and `.` (the current directory) is the destination. Without the colon, `user@server` is treated as a local file name.

#### Q. Which command copies the whole `site/` directory to a server whose SSH daemon listens on port 2222?

* [ ] `scp -p 2222 -r site/ user@server:/var/www/`
* [ ] `scp -P 2222 site/ user@server:/var/www/`
* [ ] `scp --port 2222 -R site/ user@server:/var/www/`
* [x] `scp -P 2222 -r site/ user@server:/var/www/`

> **Explanation:** `scp` uses uppercase `-P` for the port and `-r` to copy directories. Without `-r` it refuses with `"site" is not a regular file`, and lowercase `-p` preserves times and modes.

#### Q. `/tmp/dd` does not exist on `server`. You run the same command twice. Which files exist on the server afterwards?

```bash
scp -r d1 user@server:/tmp/dd   # d1 contains one file, f
scp -r d1 user@server:/tmp/dd
```

* [ ] Only `/tmp/dd/d1/f`
* [ ] Only `/tmp/dd/f`, overwritten by the second copy
* [ ] Only `/tmp/dd/f`, because the second command fails
* [x] Both `/tmp/dd/f` and `/tmp/dd/d1/f`

> **Explanation:** Like `cp -r`, the first copy creates `/tmp/dd` as a copy of `d1`. The second time `/tmp/dd` already exists, so `d1` is copied inside it. Copy into an existing parent, such as `user@server:/tmp/`, for repeatable results.

#### Q. Since OpenSSH 9.0 (Ubuntu 24.04 ships 9.6), what protocol does the `scp` command use by default, and how do you force the legacy one?

* [ ] The SCP/rcp protocol; force SFTP with `-s`
* [x] The SFTP protocol; force the legacy SCP protocol with `-O`
* [ ] FTP over TLS; force SCP with `-T`
* [ ] The rsync protocol; force SCP with `-L`

> **Explanation:** Modern `scp` requests the server's `sftp` subsystem for its transfers. Against a server without that subsystem it fails, and `-O` switches back to the original SCP/rcp protocol, which runs `scp -t` on the remote side.

#### Q. In an interactive `sftp` session, which commands upload a local file and download a remote file?

* [x] `put` and `get`
* [ ] `send` and `receive`
* [ ] `push` and `pull`
* [ ] `upload` and `download`

> **Explanation:** `put local_file` uploads to the remote working directory and `get remote_file` downloads it. `ls`, `cd`, `mkdir` and `rm` act on the remote side, and `exit` ends the session.

#### Q. How is SFTP related to SSH?

* [x] SFTP runs as a subsystem over an SSH connection, using the same port and authentication
* [ ] SFTP is FTP with TLS added on top
* [ ] SFTP needs its own daemon listening on port 21
* [ ] SFTP sends data unencrypted after logging in over SSH

> **Explanation:** SFTP is enabled through a `Subsystem sftp` line in `sshd_config`. It uses SSH's encryption and logins, typically on port 22. FTP with TLS is FTPS, a different protocol.

#### Q. Which command copies the contents of the local `site` directory directly into `/var/www/html/`, without creating `/var/www/html/site/`?

* [ ] `rsync -a site user@server:/var/www/html/`
* [x] `rsync -a site/ user@server:/var/www/html/`
* [ ] `rsync -a site user@server:/var/www/html`
* [ ] `rsync -a site/* user@server:/var/www/html/site/`

> **Explanation:** For `rsync`, a trailing slash on the source means "the contents of this directory". Without it, the directory itself is copied, giving `/var/www/html/site/`. The slash on the destination makes no difference.

#### Q. The server's SSH daemon listens on port 2222. How do you point `rsync` at it?

* [ ] `rsync -avz -P 2222 ./project/ user@host:/srv/project/`
* [ ] `rsync -avz --ssh-port=2222 ./project/ user@host:/srv/project/`
* [x] `rsync -avz -e "ssh -p 2222" ./project/ user@host:/srv/project/`
* [ ] `rsync -avz ./project/ user@host:2222/srv/project/`

> **Explanation:** `-e` sets the remote shell command, so the SSH options go there. In `rsync`, `-P` means `--partial --progress`, not port.

#### Q. What does this command do?

```bash
ssh user@remotehost "tar -czf - /srv/data" > data.tar.gz
```

* [ ] Copies the local `data.tar.gz` to the remote host
* [ ] Extracts `data.tar.gz` into `/srv/data` on the remote host
* [ ] Creates `data.tar.gz` on the remote host and leaves it there
* [x] Creates a compressed archive on the remote host and streams it into a local file

> **Explanation:** `-f -` makes `tar` write the archive to stdout, `ssh` carries that stdout back, and the local `>` saves it. No temporary archive is written on the server.

#### Q. Which plain-text protocol should you avoid on untrusted networks, because it sends logins and data unencrypted?

* [ ] SFTP
* [ ] SCP
* [x] FTP
* [ ] FTPS

> **Explanation:** Plain FTP sends credentials and files in clear text. SFTP and SCP run over SSH, and FTPS adds TLS encryption to FTP.
