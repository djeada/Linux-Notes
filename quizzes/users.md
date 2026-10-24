# Users and Permissions Quiz

Notes: [Managing Users](../notes/managing_users.md), [Permissions](../notes/permissions.md), [LDAP](../notes/ldap.md)

Check your understanding of user and group management, `su` and `sudo`, file permissions, ACLs and LDAP directories.

#### Q. Which file lists local user accounts with their UID, home directory and login shell?

* [ ] `/etc/shadow`
* [ ] `/etc/group`
* [x] `/etc/passwd`
* [ ] `/etc/login.defs`

> **Explanation:** Each line of `/etc/passwd` describes one account: name, password placeholder, UID, primary GID, comment, home directory and shell. Password hashes live in `/etc/shadow`.

#### Q. Which file stores the password hashes and password-aging data for local accounts?

* [ ] `/etc/passwd`
* [ ] `/etc/sudoers`
* [ ] `/etc/securetty`
* [x] `/etc/shadow`

> **Explanation:** `/etc/shadow` holds salted one-way hashes plus expiry fields and is readable only by root. `/etc/passwd` is world-readable, so it only contains an `x` placeholder.

#### Q. What does this `/etc/passwd` line tell you about the account?

```text
deploy:x:1001:2000:Deploy User:/srv/deploy:/usr/sbin/nologin
```

* [x] UID 1001, primary GID 2000, home `/srv/deploy`, and no interactive login shell
* [ ] UID 2000, primary GID 1001, home `/srv/deploy`, and the password is `x`
* [ ] UID 1001, member of 2000 groups, home `/usr/sbin/nologin`
* [ ] UID 1001, primary GID 2000, and the password stored in plain text in field 2

> **Explanation:** The fields are name, password placeholder (`x` means "see `/etc/shadow`"), UID, primary GID, comment, home and shell. A shell of `nologin` is typical for service accounts.

#### Q. In `/etc/shadow`, what does a password field that starts with `!` mean?

* [ ] The account has no password and anyone can log in
* [ ] The password must be changed at next login
* [x] Password authentication is disabled for the account
* [ ] The password is stored unencrypted

> **Explanation:** A hash prefixed with `!` (or a field of `*`) cannot match any password, so password logins fail. `passwd -l` locks accounts this way, but other methods such as SSH keys may still work.

#### Q. Which command creates the user `adam` together with a home directory?

* [ ] `useradd adam`
* [ ] `useradd -M adam`
* [x] `useradd -m adam`
* [ ] `usermod -m adam`

> **Explanation:** `-m` creates the home directory and copies the skeleton files into it. Without it, whether a home is created depends on distribution defaults; `-M` explicitly skips it.

#### Q. Which command creates the user `alice` without a home directory, even if the system default would create one?

* [x] `useradd -M alice`
* [ ] `useradd -m alice`
* [ ] `usermod -M alice`
* [ ] `passwd -d alice`

> **Explanation:** `-M` (`--no-create-home`) overrides `CREATE_HOME` in `/etc/login.defs`. `usermod` changes existing accounts, and `passwd -d` deletes a password.

#### Q. How do `useradd` and `adduser` differ?

* [ ] `adduser` can only create system accounts
* [x] `adduser` is a friendlier, interactive front end that is not available on every distribution
* [ ] `useradd` always prompts for the full name and password
* [ ] `useradd` only works on Red Hat systems

> **Explanation:** `adduser` asks questions and sets up the home directory for you, but it may be missing or behave differently across distributions. `useradd` is the low-level tool and the safer choice in portable scripts.

#### Q. Which command adds the existing user `bob` to the supplementary group `docker` without removing his other groups?

* [ ] `usermod -G docker bob`
* [ ] `groupadd docker bob`
* [x] `usermod -aG docker bob`
* [ ] `useradd -G docker bob`

> **Explanation:** `-a` appends to the supplementary group list. `useradd` would try to create a new user, and `groupadd` creates groups rather than adding members.

#### Q. What happens if you run `usermod -G docker bob` without `-a`?

* [ ] Bob is added to `docker` and keeps his other groups
* [ ] Bob's primary group changes to `docker`
* [ ] The command fails because `-a` is mandatory
* [x] Bob's supplementary groups are replaced, so he is removed from any group other than `docker`

> **Explanation:** Without `-a`, `-G` sets the complete list of supplementary groups. Forgetting `-a` is a classic way to accidentally remove someone from `sudo` or `wheel`.

#### Q. Which command removes user `adam` from the group `admins`?

* [ ] `groupdel admins adam`
* [ ] `usermod -aG admins adam`
* [ ] `userdel adam admins`
* [x] `gpasswd -d adam admins`

> **Explanation:** `gpasswd -d` deletes a single member from a group. `groupdel` removes the whole group and `userdel` deletes the user account.

#### Q. A line in `/etc/group` reads `admins:x:1001:adam,eve`. What does `1001` represent?

* [ ] The number of members
* [x] The group ID (GID)
* [ ] Adam's UID
* [ ] The group's password

> **Explanation:** The fields are group name, password placeholder, GID and a comma-separated member list. `getent group admins` prints the same format.

#### Q. What does `id adam` display?

* [ ] Adam's password expiry information
* [ ] Adam's last login time
* [x] Adam's UID, primary GID and group memberships
* [ ] Adam's home directory and shell

> **Explanation:** `id` prints something like `uid=1000(adam) gid=1000(adam) groups=1000(adam),27(sudo)`. Expiry details come from `chage -l` and logins from `last`.

#### Q. Which command changes the login shell of user `carol` to `/bin/zsh`?

* [ ] `useradd -s /bin/zsh carol`
* [ ] `chmod -s /bin/zsh carol`
* [ ] `export SHELL=/bin/zsh carol`
* [x] `chsh -s /bin/zsh carol`

> **Explanation:** `chsh -s` updates the shell field in `/etc/passwd` (as does `usermod -s`). `useradd` creates new accounts, and exporting `SHELL` only affects the current session.

#### Q. Which command locks the password of user `dave` so password logins fail?

* [x] `passwd -l dave`
* [ ] `passwd -d dave`
* [ ] `passwd -e dave`
* [ ] `passwd -S dave`

> **Explanation:** `-l` prefixes the hash with `!`. It does not disable the account entirely, so SSH key logins may still work. `-d` removes the password, `-e` forces a change at next login and `-S` shows status.

#### Q. Which command deletes the user `eve` together with her home directory and mail spool?

* [ ] `userdel eve`
* [ ] `usermod -L eve`
* [ ] `rm -r /home/eve`
* [x] `userdel -r eve`

> **Explanation:** `-r` removes the home directory and mail spool along with the account. Plain `userdel` leaves the files behind, and deleting the directory alone leaves the account in place.

#### Q. What UID does the root account have?

* [ ] 1
* [x] 0
* [ ] 1000
* [ ] 65534

> **Explanation:** The kernel grants superuser privileges to UID 0, whatever the account is called. Regular users usually start at 1000, and 65534 is commonly `nobody`.

#### Q. What is the difference between `su adam` and `su - adam`?

* [ ] `su - adam` does not ask for a password
* [ ] `su adam` switches to root first
* [x] `su - adam` starts a login shell with adam's own environment and startup files
* [ ] `su - adam` runs only one command and then exits

> **Explanation:** The `-` (or `-l`) option simulates a full login: adam's environment variables are loaded and you start in his home directory. Plain `su adam` keeps much of the caller's environment.

#### Q. Which command runs `whoami` as user `adam` and then returns to your own session?

* [ ] `su adam whoami`
* [x] `su adam -c "whoami"`
* [ ] `su -l whoami adam`
* [ ] `sudo -l adam whoami`

> **Explanation:** `su -c` passes a single command to the target user's shell, and the output appears in your terminal. Here it prints `adam`.

#### Q. To give user `adam` administrative rights through the default sudoers setup, which group do you add him to on Debian/Ubuntu versus RHEL/Fedora?

* [ ] `admin` on both
* [ ] `root` on both
* [x] `sudo` on Debian/Ubuntu and `wheel` on RHEL/Fedora
* [ ] `wheel` on Debian/Ubuntu and `sudo` on RHEL/Fedora

> **Explanation:** Debian-based systems grant `%sudo` full rights, while Red Hat-based systems use `%wheel`. For example, `usermod -aG wheel adam` on RHEL.

#### Q. Why should you edit `/etc/sudoers` with `visudo` rather than a regular editor?

* [ ] `visudo` encrypts the file
* [ ] Regular editors cannot open files in `/etc`
* [x] `visudo` locks the file and checks the syntax before saving, preventing a broken configuration
* [ ] `visudo` automatically grants the current user full rights

> **Explanation:** A syntax error in sudoers can stop `sudo` from working at all, locking you out of administration. `visudo` validates the file and refuses to install a broken version.

#### Q. What does the sudoers line `%wheel ALL=(ALL) ALL` do?

* [ ] Grants the user named `wheel` full sudo rights
* [x] Lets all members of the `wheel` group run any command as any user on any host
* [ ] Lets all users run commands as members of the `wheel` group
* [ ] Denies the `wheel` group any sudo rights

> **Explanation:** `%` marks a group. The fields are hosts (`ALL`), the users you may become (`(ALL)`) and the allowed commands (`ALL`). By default users still have to enter their own password.

#### Q. What does the sudoers line `adam ALL = NOPASSWD:/sbin/reboot` allow?

* [ ] Adam can run any command without a password
* [ ] Adam can reboot only after entering the root password
* [ ] Every user can reboot without a password
* [x] Adam can run `/sbin/reboot` through sudo without being asked for a password

> **Explanation:** The rule names one user and one command, and the `NOPASSWD:` tag skips authentication for it. Other commands still follow the remaining rules.

#### Q. Which sudoers line lets user `alice` run only `/usr/bin/systemctl` as root, still asking for her password?

* [x] `alice ALL=(root) /usr/bin/systemctl`
* [ ] `alice ALL=(ALL) ALL`
* [ ] `alice ALL=(root) NOPASSWD: ALL`
* [ ] `alice ALL=(root) !/usr/bin/systemctl`

> **Explanation:** Listing one command restricts alice to it, and without `NOPASSWD:` she must authenticate. `ALL` would allow every command, and `!` would forbid `systemctl` instead.

#### Q. What does `sudo -l` show?

* [ ] All processes currently running as root
* [ ] The sudo log file
* [x] Which commands the invoking user may run with sudo on this host
* [ ] The list of members in the `sudo` group

> **Explanation:** `sudo -l` (list) prints the user's allowed and forbidden commands according to the sudoers policy. It is the quickest way to check what a new rule grants.

#### Q. Which `sudo` option starts a login shell as the target user, reading that user's profile files?

* [ ] `-E`
* [ ] `-l`
* [x] `-i`
* [ ] `-u`

> **Explanation:** `sudo -i` runs the target user's shell as a login shell, much like `su -`. `-E` preserves your environment, `-l` lists privileges and `-u` only chooses the target user.

#### Q. Which command runs `make install` as root while asking sudo to keep your current environment variables?

* [ ] `sudo -i make install`
* [ ] `sudo -s make install`
* [x] `sudo -E make install`
* [ ] `sudo -k make install`

> **Explanation:** `-E` (`--preserve-env`) requests that your environment be kept, if the security policy allows it. `-i` uses a login environment and `-k` discards cached credentials.

#### Q. Which sudoers `Defaults` setting makes commands run with a minimal, clean environment instead of the caller's variables?

* [ ] `env_keep`
* [x] `env_reset`
* [ ] `requiretty`
* [ ] `secure_path`

> **Explanation:** `env_reset` (on by default) discards most of the caller's environment. `env_keep` lists exceptions that are kept, and `secure_path` sets the `PATH` used for commands.

#### Q. What does the execute (`x`) permission mean on a directory?

* [ ] Programs in the directory can be run
* [ ] Files can be created in the directory
* [ ] The directory's file names can be listed
* [x] The directory can be entered and traversed to reach entries inside it

> **Explanation:** For directories, `r` lists names, `w` lets you create, delete and rename entries (together with `x`), and `x` allows access through the directory. Without `x`, `cd` and opening files inside fail.

#### Q. Bob has write and execute permission on `/shared`, which has no sticky bit. A file there is owned by alice with mode `444`. Can bob delete it?

* [ ] No, because the file is read-only
* [ ] No, because only the owner can delete a file
* [x] Yes, because deleting a file needs write and execute permission on the directory, not on the file
* [ ] Yes, but only if bob is in alice's group

> **Explanation:** Removing a file removes a directory entry, so the directory's permissions decide. `rm` may ask about a write-protected file, but it succeeds. The sticky bit is what prevents this in shared directories.

#### Q. Which symbolic permissions does octal mode `754` represent?

* [ ] `rwxrwxr--`
* [ ] `rw-r-xr--`
* [ ] `rwxr--r-x`
* [x] `rwxr-xr--`

> **Explanation:** Each digit is the sum of read 4, write 2 and execute 1: 7 = `rwx` for the owner, 5 = `r-x` for the group and 4 = `r--` for others.

#### Q. Which octal mode does `chmod u=rw,go=r file.txt` set?

* [ ] `664`
* [x] `644`
* [ ] `640`
* [ ] `755`

> **Explanation:** `u=rw` gives the owner 6 and `go=r` gives group and others 4 each. The `=` operator sets the permissions exactly rather than adding to them.

#### Q. What is the effect of `chmod o-rwx file.txt`?

* [ ] It grants all permissions to others
* [ ] It removes all permissions for the owner
* [x] It removes read, write and execute permission for others, leaving owner and group unchanged
* [ ] It makes the file immutable

> **Explanation:** `o` selects others and `-` removes the listed bits. Owner (`u`) and group (`g`) permissions are not touched.

#### Q. With `umask 027`, what permissions does a new regular file get when the program requests mode `666`?

* [ ] `rw-r--r--`
* [ ] `rw-rw-r--`
* [ ] `rwxr-x---`
* [x] `rw-r-----`

> **Explanation:** The umask clears bits: `666` with group write and all of others' bits masked gives `640`. Directories requested as `777` would become `750`.

#### Q. Why can ordinary users change their own password even though `/etc/shadow` is writable only by root?

* [ ] `/etc/shadow` has the sticky bit set
* [ ] Users are temporarily added to the `root` group
* [x] `/usr/bin/passwd` is setuid root, so it runs with the file owner's privileges
* [ ] Password changes are written to the user's home directory

> **Explanation:** The setuid bit makes an executable run with its owner's user ID. Because setuid programs run as root, they must be audited carefully.

#### Q. `ls -l` shows `-rwSr--r--` for a file. What does the uppercase `S` mean?

* [ ] The file is a socket
* [ ] The file has the sticky bit
* [x] The setuid bit is set, but the owner has no execute permission
* [ ] The file is a symbolic link

> **Explanation:** A lowercase `s` means setuid plus execute, while `S` means the special bit is present without the underlying `x`, which usually signals a mistake.

#### Q. Which permission on a shared project directory makes new files inherit the directory's group?

* [ ] Sticky bit (`chmod +t`)
* [ ] Setuid (`chmod u+s`)
* [x] Setgid (`chmod g+s`)
* [ ] Group write (`chmod g+w`)

> **Explanation:** With setgid on a directory, new files get the directory's group and new subdirectories inherit setgid. It does not grant group write; use a suitable umask or a default ACL for that.

#### Q. What does the sticky bit do on a world-writable directory such as `/tmp`?

* [ ] It makes every file in the directory executable
* [ ] It prevents anyone from deleting files
* [x] It lets only a file's owner, the directory's owner or root delete or rename that file
* [ ] It clears the directory at every reboot

> **Explanation:** Without the sticky bit, anyone with write permission on the directory could remove other users' files. `ls -ld /tmp` shows it as a `t` in the last position (`drwxrwxrwt`).

#### Q. Which command lists every file on the system that has the setuid bit set?

* [ ] `find / -perm /2000 -type f`
* [ ] `find / -perm /1000 -type d`
* [ ] `ls -lR / | grep rwx`
* [x] `find / -perm /4000 -type f 2>/dev/null`

> **Explanation:** In octal, 4000 is setuid, 2000 is setgid and 1000 is the sticky bit. `-perm /4000` matches files with that bit set; `2>/dev/null` hides permission errors.

#### Q. Which command recursively sets mode `755` on every directory under `project/` without changing regular files?

* [ ] `chmod -R 755 project/`
* [ ] `find project/ -type f -exec chmod 755 {} +`
* [x] `find project/ -type d -exec chmod 755 {} +`
* [ ] `chmod 755 project/*`

> **Explanation:** `find -type d` selects only directories and passes them to `chmod`. `chmod -R` would also make every regular file executable, and the glob only reaches the top level.

#### Q. Which command changes the owner of `script.sh` to user `alice` and its group to `devs` in one step?

* [ ] `chmod alice:devs script.sh`
* [ ] `chgrp alice:devs script.sh`
* [x] `chown alice:devs script.sh`
* [ ] `usermod -g devs alice script.sh`

> **Explanation:** `chown user:group` sets both at once; `chgrp` changes only the group. `chmod` changes permission bits, not ownership.

#### Q. Which command grants user `bob` read and write access to `report.txt` through an ACL, keeping existing ACL entries?

* [ ] `chmod u:bob:rw report.txt`
* [ ] `setfacl -x u:bob:rw report.txt`
* [ ] `getfacl -m u:bob:rw report.txt`
* [x] `setfacl -m u:bob:rw report.txt`

> **Explanation:** `setfacl -m` (modify) adds or updates one entry and leaves others intact. `-x` removes entries, and `getfacl` only displays ACLs.

#### Q. Which command removes only the ACL entry for group `sales` from `budget.xls`?

* [ ] `setfacl -b budget.xls`
* [x] `setfacl -x g:sales budget.xls`
* [ ] `setfacl -m g:sales:--- budget.xls`
* [ ] `chgrp -sales budget.xls`

> **Explanation:** `-x` deletes the named entry; no permissions are given in the spec. `-b` would remove every extended entry, and `-m g:sales:---` keeps an entry that denies access.

#### Q. Which command removes all extended ACL entries from `data/`, keeping only the standard owner, group and other permissions?

* [ ] `setfacl -x data/`
* [ ] `chmod a-rwx data/`
* [ ] `getfacl --remove-all data/`
* [x] `setfacl -b data/`

> **Explanation:** `-b` (`--remove-all`) strips named user, named group and mask entries but retains the base permissions. `chmod a-rwx` would remove the base permissions instead.

#### Q. Which command makes every file later created in `project/` grant group `devs` read and write access by default?

* [ ] `setfacl -m g:devs:rw project/`
* [ ] `chmod g+s project/`
* [ ] `setfacl -b project/`
* [x] `setfacl -d -m g:devs:rw project/`

> **Explanation:** `-d` sets a default ACL, which new items in the directory inherit. Without `-d`, the entry applies only to the directory itself, and setgid changes group ownership, not permissions.

#### Q. `getfacl notes.txt` shows the lines below. What access does user `joe` actually have?

```text
user:joe:rwx        #effective:r--
mask::r--
```

* [ ] `rwx`, because named user entries ignore the mask
* [x] Read only, because the mask limits named users and groups
* [ ] No access, because the mask overrides all entries
* [ ] Read and execute, the default for named users

> **Explanation:** The mask is the upper bound for named users, named groups and the owning group. Joe's entry says `rwx`, but only the bits also present in the mask, `r--`, take effect.

#### Q. A file has extended ACL entries. What does running `chmod g=r` on it change?

* [ ] Only the owning group's own ACL entry
* [ ] Nothing, because `chmod` is ignored on files with ACLs
* [ ] It deletes all named ACL entries
* [x] The ACL mask, which can reduce named users' and groups' effective access

> **Explanation:** With an extended ACL, the group bits shown by `ls -l` represent the mask. Changing them with `chmod` therefore changes the mask and limits every named entry.

#### Q. In the DN `uid=jdoe,ou=users,dc=example,dc=com`, what does `ou=users` represent?

* [ ] The user's login name
* [ ] The domain the directory belongs to
* [x] The organizational unit (container) that holds the entry
* [ ] The user's group membership

> **Explanation:** A DN is read from the most specific part to the most general, like a path: `uid=jdoe` is the entry, `ou=users` its container, and `dc=example,dc=com` the domain.

#### Q. What is the conventional base DN for a directory serving the domain `example.com`?

* [ ] `cn=example,cn=com`
* [ ] `ou=example,ou=com`
* [ ] `dn=example.com`
* [x] `dc=example,dc=com`

> **Explanation:** Each part of the DNS name becomes a domain component (`dc`). Searches and new entries are placed under this base, such as `ou=users,dc=example,dc=com`.

#### Q. Which TCP ports do plain LDAP and LDAP over SSL (LDAPS) use by default?

* [ ] 53 and 853
* [ ] 88 and 464
* [x] 389 and 636
* [ ] 443 and 8443

> **Explanation:** LDAP listens on 389, where StartTLS can upgrade the connection, and LDAPS uses TLS from the start on 636. Ports 53/853 are DNS, 88/464 are Kerberos and 443/8443 are HTTPS.

#### Q. Which command searches the subtree `dc=example,dc=com` for the user `jdoe` using simple authentication?

* [ ] `ldapadd -x -b "dc=example,dc=com" "(uid=jdoe)"`
* [ ] `ldapsearch -b "(uid=jdoe)" "dc=example,dc=com"`
* [x] `ldapsearch -x -b "dc=example,dc=com" "(uid=jdoe)"`
* [ ] `ldapwhoami -x "dc=example,dc=com" "(uid=jdoe)"`

> **Explanation:** `-x` selects simple authentication, `-b` sets the search base, and the filter comes after it. `ldapadd` creates entries and `ldapwhoami` only tests a bind.

#### Q. Which LDAP filter matches entries that are of class `person` and have an email address?

* [ ] `(|(objectClass=person)(mail=*))`
* [ ] `(objectClass=person,mail=*)`
* [ ] `(!(objectClass=person)(mail=*))`
* [x] `(&(objectClass=person)(mail=*))`

> **Explanation:** LDAP filters use prefix notation: `&` is AND, `|` is OR and `!` is NOT. `(mail=*)` is a presence test that matches any entry with a `mail` attribute.

#### Q. Which file format is used to add, modify or export LDAP entries in bulk with tools such as `ldapadd` and `ldapmodify`?

* [ ] JSON
* [ ] CSV
* [x] LDIF
* [ ] YAML

> **Explanation:** LDIF (LDAP Data Interchange Format) is plain text listing a `dn:` line followed by attributes. For example, `ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f user.ldif` loads it.

#### Q. A user entry in LDAP has only the `inetOrgPerson` object class, and `getent passwd jdoe` returns nothing. What is missing for Linux login?

* [ ] A `mail` attribute
* [ ] An `ou=groups` entry
* [ ] The `organization` object class
* [x] The `posixAccount` object class with `uidNumber`, `gidNumber`, `homeDirectory` and `loginShell`

> **Explanation:** `inetOrgPerson` describes a person, but NSS needs POSIX attributes to build a Unix account. Adding `posixAccount` (and often `shadowAccount`) with those attributes lets `getent passwd jdoe` resolve.
