# Users and Permissions Quiz

Notes: [Managing Users](../notes/managing_users.md), [Permissions](../notes/permissions.md), [LDAP](../notes/ldap.md)

Check your understanding of user and group management, `su` and `sudo`, file permissions, ACLs and LDAP directories.

#### Q. Which file lists local user accounts with their UID, home directory and login shell?

* [x] `/etc/passwd`
* [ ] `/etc/shadow`
* [ ] `/etc/group`
* [ ] `/etc/login.defs`

> **Explanation:** Each line of `/etc/passwd` describes one account: name, password placeholder, UID, primary GID, comment, home directory and shell. Password hashes live in `/etc/shadow`.

#### Q. Which file stores the password hashes and password-aging data for local accounts?

* [ ] `/etc/passwd`
* [x] `/etc/shadow`
* [ ] `/etc/sudoers`
* [ ] `/etc/securetty`

> **Explanation:** `/etc/shadow` holds salted one-way hashes plus aging fields and is not world-readable: Ubuntu lets only root and the `shadow` group read it, and Fedora gives it mode `000`. World-readable `/etc/passwd` only holds an `x` placeholder.

#### Q. What does this `/etc/passwd` line tell you about the account?

```text
deploy:x:1001:2000:Deploy User:/srv/deploy:/usr/sbin/nologin
```

* [ ] UID 2000, primary GID 1001, home `/srv/deploy`, and the password is `x`
* [ ] UID 1001, member of 2000 groups, home `/usr/sbin/nologin`
* [x] UID 1001, primary GID 2000, home `/srv/deploy`, and no interactive login shell
* [ ] UID 1001, primary GID 2000, and the password stored in plain text in field 2

> **Explanation:** The fields are name, password placeholder (`x` means "see `/etc/shadow`"), UID, primary GID, comment, home and shell. A shell of `nologin` is typical for service accounts.

#### Q. In `/etc/shadow`, what does a password field that starts with `!` mean?

* [ ] The account has no password and anyone can log in
* [ ] The password must be changed at next login
* [ ] The password is stored unencrypted
* [x] Password authentication is disabled for the account

> **Explanation:** A hash prefixed with `!` (or a field of `*`) cannot match any password, so password logins fail. `passwd -l` locks accounts this way, but other methods such as SSH keys may still work.

#### Q. Which command creates the user `adam` with a home directory populated from `/etc/skel`, whatever the distribution's default?

* [ ] `useradd adam`
* [x] `useradd -m adam`
* [ ] `useradd -M adam`
* [ ] `usermod -m adam`

> **Explanation:** `-m` creates the home directory and copies the skeleton files into it. Without it, the result depends on `CREATE_HOME` in `/etc/login.defs`: Fedora creates a home, Ubuntu does not. `-M` explicitly skips it, and `usermod` changes existing accounts.

#### Q. After `useradd -m bob` on Ubuntu, where do the `.bashrc` and `.profile` files in `/home/bob` come from?

* [x] They are copied from the skeleton directory `/etc/skel`
* [ ] They are generated from the settings in `/etc/login.defs`
* [ ] They are copied from root's home directory
* [ ] Bash creates them the first time bob logs in

> **Explanation:** `useradd -m` copies everything in `/etc/skel` (or the directory given with `-k`) into the new home and gives it to the user. Changing `/etc/skel` affects only accounts created later.

#### Q. How do `useradd` and `adduser` differ?

* [ ] `adduser` can only create system accounts, while `useradd` creates regular users
* [ ] `useradd` always prompts for the full name and password, while `adduser` never does
* [x] `adduser` is an interactive front end on Debian/Ubuntu but just a link to `useradd` on Fedora
* [ ] `useradd` only works on Red Hat systems, and `adduser` only on Debian

> **Explanation:** Debian's `adduser` asks for a password and details and creates the home for you; Fedora's `/usr/sbin/adduser` is a symlink to `useradd`. Because `adduser` varies (and minimal images may lack it), `useradd` is the safer choice in portable scripts.

#### Q. Which command adds the existing user `bob` to the supplementary group `docker` without removing his other groups?

* [ ] `usermod -G docker bob`
* [ ] `groupadd docker bob`
* [ ] `useradd -G docker bob`
* [x] `usermod -aG docker bob`

> **Explanation:** `-a` appends to the supplementary group list. `useradd` would try to create a new user, and `groupadd` creates groups rather than adding members.

#### Q. You run `usermod -aG docker bob` while bob is logged in. In his existing shell, `id -Gn` still does not list `docker`. Why?

* [x] Group membership is read at login, so his running shell keeps its old group list
* [ ] `usermod` changes only take effect after the system is rebooted
* [ ] `-aG` writes the change to `/etc/gshadow` only, not to `/etc/group`
* [ ] Bob must run `passwd` before a new group membership becomes active

> **Explanation:** A process's supplementary groups are fixed when the login session starts. `/etc/group` is updated immediately, so a new login (or `newgrp docker` / `su - bob`) picks it up; no reboot is needed.

#### Q. What happens if you run `usermod -G docker bob` without `-a`?

* [ ] Bob is added to `docker` and keeps all of his other supplementary groups
* [ ] Bob's primary group changes to `docker`, and his supplementary groups stay
* [ ] The command fails, because `-a` is mandatory whenever `-G` is used
* [x] Bob's supplementary groups are replaced, so he leaves every group except `docker`

> **Explanation:** Without `-a`, `-G` sets the complete list of supplementary groups. Forgetting `-a` is a classic way to accidentally remove someone from `sudo` or `wheel`.

#### Q. Which command removes user `adam` from the group `admins`?

* [ ] `groupdel admins adam`
* [ ] `usermod -aG admins adam`
* [x] `gpasswd -d adam admins`
* [ ] `userdel adam admins`

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

#### Q. An admin runs `useradd -m -p 'Secret123' carol`. What happens when carol tries to log in with the password `Secret123`?

* [x] Login fails, because `-p` expects an already hashed password and stores the text as-is
* [ ] Login works, because `useradd` hashes the value before storing it
* [ ] Login works only after carol first logs in with an empty password
* [ ] Login fails, because `-p` is accepted only together with `-r`

> **Explanation:** `-p` writes its argument straight into the hash field of `/etc/shadow`, and `Secret123` is not a valid hash, so no password can match it. Set passwords with `passwd carol` or `chpasswd` instead.

#### Q. Which command locks the password of user `dave` so password logins fail?

* [ ] `passwd -d dave`
* [x] `passwd -l dave`
* [ ] `passwd -e dave`
* [ ] `passwd -S dave`

> **Explanation:** `-l` prefixes the hash with `!`. It does not disable the account entirely, so SSH key logins may still work. `-d` removes the password, `-e` forces a change at next login and `-S` shows status.

#### Q. Which command forces user `alice` to choose a new password the next time she logs in?

* [ ] `chage -l alice`
* [x] `chage -d 0 alice`
* [ ] `passwd -l alice`
* [ ] `usermod -L alice`

> **Explanation:** `chage -d 0` sets the last-change date to day 0, so the password counts as expired and must be changed at login; `passwd -e alice` does the same. `chage -l` only displays aging data, while `passwd -l` and `usermod -L` lock the password.

#### Q. Which command deletes the user `eve` together with her home directory and mail spool?

* [ ] `userdel eve`
* [ ] `usermod -L eve`
* [ ] `rm -r /home/eve`
* [x] `userdel -r eve`

> **Explanation:** `-r` removes the home directory and mail spool along with the account. Plain `userdel` leaves the files behind, and deleting the directory alone leaves the account in place.

#### Q. What UID does the root account have?

* [x] 0
* [ ] 1
* [ ] 1000
* [ ] 65534

> **Explanation:** The kernel grants superuser privileges to UID 0, whatever the account is called. Regular users usually start at 1000, and 65534 is commonly `nobody`.

#### Q. You change adam's UID with `usermod -u 2001 adam`; it used to be 1001. What does `ls -l` show as the owner of a file he owned in `/tmp`?

* [ ] `adam`, because `usermod` updates every file on the system
* [ ] `root`, because orphaned files are handed to root
* [x] `1001`, because `usermod` only updates files in his home directory and mail spool
* [ ] `nobody`, because unknown UIDs are shown as 65534

> **Explanation:** Files store a numeric UID. `usermod -u` fixes ownership only inside the home directory and mail spool, so elsewhere the file keeps UID 1001, which no longer has a name. Fix it with `find / -xdev -uid 1001 -exec chown -h adam {} +`.

#### Q. What is the difference between `su adam` and `su - adam`?

* [ ] `su - adam` switches user without asking for adam's password
* [ ] `su adam` switches to root first and only then to adam
* [ ] `su - adam` runs a single command as adam and then exits
* [x] `su - adam` starts a login shell with adam's environment and startup files

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

* [x] `visudo` locks the file and checks its syntax before installing the change
* [ ] `visudo` encrypts the file so that other users cannot read the rules
* [ ] Regular editors cannot open files in `/etc` without special flags
* [ ] `visudo` automatically grants the current user full sudo rights

> **Explanation:** A syntax error in sudoers can stop `sudo` from working at all, locking you out of administration. `visudo` validates the file and refuses to install a broken version.

#### Q. What does the sudoers line `%wheel ALL=(ALL) ALL` do?

* [ ] Grants the user named `wheel` full sudo rights
* [x] Lets all members of the `wheel` group run any command as any user on any host
* [ ] Lets all users run commands as members of the `wheel` group
* [ ] Denies the `wheel` group any sudo rights

> **Explanation:** `%` marks a group. The fields are hosts (`ALL`), the users you may become (`(ALL)`) and the allowed commands (`ALL`). By default users still have to enter their own password.

#### Q. What does the sudoers line `adam ALL = NOPASSWD:/sbin/reboot` allow?

* [x] Adam can run `/sbin/reboot` through sudo without being asked for a password
* [ ] Adam can run any command without a password
* [ ] Adam can reboot only after entering the root password
* [ ] Every user can reboot without a password

> **Explanation:** The rule names one user and one command, and the `NOPASSWD:` tag skips authentication for it. Other commands still follow the remaining rules.

#### Q. Which sudoers line lets user `alice` run only `/usr/bin/systemctl` as root, still asking for her password?

* [ ] `alice ALL=(ALL) ALL`
* [ ] `alice ALL=(root) NOPASSWD: ALL`
* [x] `alice ALL=(root) /usr/bin/systemctl`
* [ ] `alice ALL=(root) !/usr/bin/systemctl`

> **Explanation:** Listing one command restricts alice to it, and without `NOPASSWD:` she must authenticate. `ALL` would allow every command, and `!` would forbid `systemctl` instead.

#### Q. What does `sudo -l` show?

* [ ] All processes currently running as root on this host
* [ ] The sudo log of commands the user has already run
* [ ] The members of the `sudo` group and their privileges
* [x] Which commands the invoking user may run with sudo on this host

> **Explanation:** `sudo -l` (list) prints the user's allowed and forbidden commands according to the sudoers policy. It is the quickest way to check what a new rule grants.

#### Q. Which `sudo` option starts a login shell as the target user, reading that user's profile files?

* [ ] `-E`
* [x] `-i`
* [ ] `-l`
* [ ] `-u`

> **Explanation:** `sudo -i` runs the target user's shell as a login shell, much like `su -`. `-E` preserves your environment, `-l` lists privileges and `-u` only chooses the target user.

#### Q. Which command runs `make install` as root while asking sudo to keep your current environment variables?

* [ ] `sudo -i make install`
* [ ] `sudo -s make install`
* [ ] `sudo -k make install`
* [x] `sudo -E make install`

> **Explanation:** `-E` (`--preserve-env`) requests that your environment be kept, if the security policy allows it. `-i` uses a login environment and `-k` discards cached credentials.

#### Q. Which sudoers `Defaults` setting makes commands run with a minimal, clean environment instead of the caller's variables?

* [ ] `env_keep`
* [ ] `requiretty`
* [x] `env_reset`
* [ ] `secure_path`

> **Explanation:** `env_reset` (on by default) discards most of the caller's environment. `env_keep` lists exceptions that are kept, and `secure_path` sets the `PATH` used for commands.

#### Q. What does the execute (`x`) permission mean on a directory?

* [x] The directory can be entered and traversed to reach entries inside it
* [ ] Programs stored in the directory can be run by any user
* [ ] New files can be created in the directory by group members
* [ ] The names of the entries in the directory can be listed

> **Explanation:** For directories, `r` lists names, `w` lets you create, delete and rename entries (together with `x`), and `x` allows access through the directory. Without `x`, `cd` and opening files inside fail.

#### Q. Bob has write and execute permission on `/shared`, which has no sticky bit. A file there is owned by alice with mode `444`. Can bob delete it?

* [ ] No, because the file's mode `444` makes it read-only for everyone
* [x] Yes, because deletion needs write and execute permission on the directory, not the file
* [ ] No, because only the owner of a file can ever delete it
* [ ] Yes, but only if bob is also a member of alice's primary group

> **Explanation:** Removing a file removes a directory entry, so the directory's permissions decide. `rm` may ask about a write-protected file, but it succeeds. The sticky bit is what prevents this in shared directories.

#### Q. Which symbolic permissions does octal mode `754` represent?

* [ ] `rwxrwxr--`
* [ ] `rw-r-xr--`
* [x] `rwxr-xr--`
* [ ] `rwxr--r-x`

> **Explanation:** Each digit is the sum of read 4, write 2 and execute 1: 7 = `rwx` for the owner, 5 = `r-x` for the group and 4 = `r--` for others.

#### Q. Which octal mode does `chmod u=rw,go=r file.txt` set?

* [ ] `664`
* [ ] `640`
* [ ] `755`
* [x] `644`

> **Explanation:** `u=rw` gives the owner 6 and `go=r` gives group and others 4 each. The `=` operator sets the permissions exactly rather than adding to them.

#### Q. What is the effect of `chmod o-rwx file.txt`?

* [x] It removes read, write and execute for others, leaving owner and group unchanged
* [ ] It grants read, write and execute permission to others
* [ ] It removes all permissions for the owner, leaving group and others
* [ ] It makes the file immutable, so nobody else can change it

> **Explanation:** `o` selects others and `-` removes the listed bits. Owner (`u`) and group (`g`) permissions are not touched.

#### Q. With `umask 027`, what permissions does a new regular file get when the program requests mode `666`?

* [ ] `rw-r--r--`
* [ ] `rw-rw-r--`
* [ ] `rwxr-x---`
* [x] `rw-r-----`

> **Explanation:** The umask clears bits: `666` with group write and all of others' bits masked gives `640`. Directories requested as `777` would become `750`.

#### Q. With `umask 033`, which modes do a new file (requested as `666`) and a new directory (requested as `777`) get?

* [x] File `644`, directory `744`
* [ ] File `633`, directory `744`
* [ ] File `644`, directory `755`
* [ ] File `633`, directory `733`

> **Explanation:** The umask clears bits (`mode & ~umask`); it is not subtraction. `033` removes write and execute for group and others, so `666` becomes `644` and `777` becomes `744`.

#### Q. Why can ordinary users change their own password even though `/etc/shadow` is writable only by root?

* [ ] `/etc/shadow` has the sticky bit set
* [ ] Users are temporarily added to the `root` group
* [x] `/usr/bin/passwd` is setuid root, so it runs with the file owner's privileges
* [ ] Password changes are written to the user's home directory

> **Explanation:** The setuid bit makes an executable run with its owner's user ID. Because setuid programs run as root, they must be audited carefully.

#### Q. On Linux, you run `chmod 4755` on a root-owned shell script `/usr/local/bin/backup.sh` that runs `id -u`. What does it print when alice runs it?

* [ ] `0`, because the setuid bit makes the script run as root
* [x] Alice's own UID, because Linux ignores setuid on interpreted scripts
* [ ] `0`, but only if the script starts with `#!/bin/bash`
* [ ] Nothing, because the kernel refuses to run setuid scripts

> **Explanation:** The kernel honours setuid and setgid only on binary executables; for a `#!` script it starts the interpreter with the caller's IDs. Grant the access with a narrow sudo rule instead.

#### Q. `ls -l` shows `-rwSr--r--` for a file. What does the uppercase `S` mean?

* [x] The setuid bit is set, but the owner has no execute permission
* [ ] The file is a socket, shown by `S` in the owner field
* [ ] The sticky bit is set, and others have no execute permission
* [ ] The file is a symbolic link to a setuid program

> **Explanation:** A lowercase `s` means setuid plus execute, while `S` means the special bit is present without the underlying `x`, which usually signals a mistake.

#### Q. Which permission on a shared project directory makes new files inherit the directory's group?

* [ ] Sticky bit (`chmod +t`)
* [ ] Setuid (`chmod u+s`)
* [x] Setgid (`chmod g+s`)
* [ ] Group write (`chmod g+w`)

> **Explanation:** With setgid on a directory, new files get the directory's group and new subdirectories inherit setgid. It does not grant group write; use a suitable umask or a default ACL for that.

#### Q. `/srv/proj` has mode `drwxrwsr-x`. After `chmod 0775 /srv/proj` with GNU coreutils, what does `ls -ld /srv/proj` show?

* [ ] `drwxrwxr-x`, because the leading `0` clears all special bits
* [x] `drwxrwsr-x`, because GNU `chmod` keeps a directory's setgid bit here
* [ ] `drwxrwSr-x`, because the group execute bit is removed
* [ ] `drwxr-xr-x`, because `0775` resets the group bits

> **Explanation:** For directories, GNU `chmod` preserves the setuid and setgid bits when a numeric mode does not mention them explicitly. Clear the bit with `chmod g-s /srv/proj` or a five-digit mode such as `chmod 00775 /srv/proj`.

#### Q. What does the sticky bit do on a world-writable directory such as `/tmp`?

* [ ] It makes every file created in the directory executable
* [ ] It prevents anyone, including root, from deleting files
* [ ] It makes the system empty the directory at every reboot
* [x] Only a file's owner, the directory's owner or root can delete or rename the file

> **Explanation:** Without the sticky bit, anyone with write permission on the directory could remove other users' files. `ls -ld /tmp` shows it as a `t` in the last position (`drwxrwxrwt`).

#### Q. Which command lists every file on the system that has the setuid bit set?

* [ ] `find / -perm /2000 -type f`
* [ ] `find / -perm /1000 -type d`
* [ ] `ls -lR / | grep rwx`
* [x] `find / -perm /4000 -type f 2>/dev/null`

> **Explanation:** In octal, 4000 is setuid, 2000 is setgid and 1000 is the sticky bit. `-perm /4000` matches files with that bit set; `2>/dev/null` hides permission errors.

#### Q. What does `find / -perm /2000 -type f -o -type d` match?

* [x] Setgid regular files, plus every directory on the system
* [ ] Only setgid regular files and setgid directories
* [ ] Only setgid directories
* [ ] Nothing, because `-o` must be written inside parentheses

> **Explanation:** The implicit AND binds tighter than `-o`, so this reads `(-perm /2000 -type f) -o -type d`. Group the type tests to get setgid files and directories: `find / \( -type f -o -type d \) -perm /2000`.

#### Q. Which command recursively sets mode `755` on every directory under `project/` without changing regular files?

* [ ] `chmod -R 755 project/`
* [ ] `find project/ -type f -exec chmod 755 {} +`
* [x] `find project/ -type d -exec chmod 755 {} +`
* [ ] `chmod 755 project/*`

> **Explanation:** `find -type d` selects only directories and passes them to `chmod`. `chmod -R` would also make every regular file executable, and the glob only reaches the top level.

#### Q. Which command changes the owner of `script.sh` to user `alice` and its group to `devs` in one step?

* [ ] `chmod alice:devs script.sh`
* [x] `chown alice:devs script.sh`
* [ ] `chgrp alice:devs script.sh`
* [ ] `usermod -g devs alice script.sh`

> **Explanation:** `chown user:group` sets both at once; `chgrp` changes only the group. `chmod` changes permission bits, not ownership.

#### Q. Which command grants user `bob` read and write access to `report.txt` through an ACL, keeping existing ACL entries?

* [ ] `chmod u:bob:rw report.txt`
* [ ] `setfacl -x u:bob:rw report.txt`
* [ ] `getfacl -m u:bob:rw report.txt`
* [x] `setfacl -m u:bob:rw report.txt`

> **Explanation:** `setfacl -m` (modify) adds or updates one entry and leaves others intact. `-x` removes entries, and `getfacl` only displays ACLs.

#### Q. Which command removes only the ACL entry for group `sales` from `budget.xls`?

* [x] `setfacl -x g:sales budget.xls`
* [ ] `setfacl -b budget.xls`
* [ ] `setfacl -m g:sales:--- budget.xls`
* [ ] `chgrp -sales budget.xls`

> **Explanation:** `-x` deletes the named entry; no permissions are given in the spec. `-b` would remove every extended entry, and `-m g:sales:---` keeps an entry that denies access.

#### Q. Which command removes all extended ACL entries from `data/`, keeping only the standard owner, group and other permissions?

* [ ] `setfacl -x data/`
* [x] `setfacl -b data/`
* [ ] `chmod a-rwx data/`
* [ ] `getfacl --remove-all data/`

> **Explanation:** `-b` (`--remove-all`) strips named user, named group and mask entries, plus any default ACL, but retains the base permissions. `-x` needs an entry to remove, and `chmod a-rwx` would clear the base permissions instead.

#### Q. Which command makes every file later created in `project/` grant group `devs` read and write access by default?

* [ ] `setfacl -m g:devs:rw project/`
* [ ] `chmod g+s project/`
* [x] `setfacl -d -m g:devs:rw project/`
* [ ] `setfacl -b project/`

> **Explanation:** `-d` sets a default ACL, which new items in the directory inherit. Without `-d`, the entry applies only to the directory itself, and setgid changes group ownership, not permissions.

#### Q. Directory `shared/` has the default ACL entry `default:group:devs:rw-`. A program running with `umask 077` creates `shared/new`, requesting mode `666`. What happens?

* [ ] The umask applies as usual, so `new` is `rw-------` and `devs` has no access
* [ ] Default ACLs apply only to new subdirectories, not to files
* [ ] `new` copies the directory's own access ACL instead
* [x] The umask is not applied; `new` inherits the default ACL, so group `devs` can read and write it

> **Explanation:** When the parent has a default ACL, the new item's ACL comes from it, limited only by the mode the program requested; the umask is ignored. A program asking for `600` would still leave `devs` without effective access.

#### Q. `getfacl notes.txt` shows the lines below. What access does user `joe` actually have?

```text
user:joe:rwx        #effective:r--
mask::r--
```

* [ ] `rwx`, because named user entries ignore the mask
* [ ] No access, because the mask overrides all entries
* [x] Read only, because the mask limits named users and groups
* [ ] Read and execute, the default for named users

> **Explanation:** The mask is the upper bound for named users, named groups and the owning group. Joe's entry says `rwx`, but only the bits also present in the mask, `r--`, take effect.

#### Q. A file has extended ACL entries. What does running `chmod g=r` on it change?

* [ ] Only the owning group's own ACL entry
* [x] The ACL mask, which can reduce named users' and groups' effective access
* [ ] Nothing, because `chmod` is ignored on files with ACLs
* [ ] It deletes all named ACL entries

> **Explanation:** With an extended ACL, the group bits shown by `ls -l` represent the mask. Changing them with `chmod` therefore changes the mask and limits every named entry.

#### Q. In the DN `uid=jdoe,ou=users,dc=example,dc=com`, what does `ou=users` represent?

* [x] The organizational unit (container) that holds the entry
* [ ] The user's login name
* [ ] The domain the directory belongs to
* [ ] The user's group membership

> **Explanation:** A DN is read from the most specific part to the most general, like a path: `uid=jdoe` is the entry, `ou=users` its container, and `dc=example,dc=com` the domain.

#### Q. What is the conventional base DN for a directory serving the domain `example.com`?

* [ ] `cn=example,cn=com`
* [x] `dc=example,dc=com`
* [ ] `ou=example,ou=com`
* [ ] `dn=example.com`

> **Explanation:** Each part of the DNS name becomes a domain component (`dc`). Searches and new entries are placed under this base, such as `ou=users,dc=example,dc=com`.

#### Q. Which TCP ports do plain LDAP and LDAP over SSL (LDAPS) use by default?

* [x] 389 and 636
* [ ] 53 and 853
* [ ] 88 and 464
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
* [ ] YAML
* [x] LDIF

> **Explanation:** LDIF (LDAP Data Interchange Format) is plain text listing a `dn:` line followed by attributes. For example, `ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f user.ldif` loads it.

#### Q. A user entry in LDAP has only the `inetOrgPerson` object class, and `getent passwd jdoe` returns nothing. What is missing for Linux login?

* [x] The `posixAccount` class with `uidNumber`, `gidNumber`, `homeDirectory` and `loginShell`
* [ ] A `mail` attribute holding the user's email address
* [ ] An `ou=groups` entry listing the user's groups
* [ ] The `organization` object class on the user's entry

> **Explanation:** `inetOrgPerson` describes a person, but NSS needs POSIX attributes to build a Unix account. Adding `posixAccount` (and often `shadowAccount`) with those attributes lets `getent passwd jdoe` resolve.

#### Q. On a host whose users come from LDAP through SSSD, `grep jdoe /etc/passwd` finds nothing. Which command shows whether the system can resolve `jdoe` as an account?

* [ ] `grep jdoe /etc/shadow`
* [x] `getent passwd jdoe`
* [ ] `ls -d /home/jdoe`
* [ ] `awk -F: '$1 == "jdoe"' /etc/passwd`

> **Explanation:** `getent` asks every source listed in `/etc/nsswitch.conf` (such as `files` and `sss`), while `/etc/passwd` and `/etc/shadow` hold only local accounts. A directory user's home may not exist until the first login.

#### Q. `ldapsearch -x -b "dc=wrong,dc=com" "(uid=jdoe)"` ends with `result: 32 No such object`. What does that tell you?

* [ ] The client could not contact the LDAP server
* [ ] The bind password was wrong
* [x] The server answered, but the search base DN does not exist
* [ ] The search ran but no entry matched the filter

> **Explanation:** Code 32 means the base or target DN is missing. An unreachable server gives `Can't contact LDAP server (-1)`, a wrong password `Invalid credentials (49)`, and a search with no matches `result: 0 Success` with no entries.
