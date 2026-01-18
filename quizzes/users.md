#### Q. Which file contains the list of local user accounts and their default shells?

* [ ] `/etc/shadow`
* [ ] `/etc/group`
* [x] `/etc/passwd`
* [ ] `/etc/userlist`
* [ ] `/etc/login.defs`

#### Q. What command creates a new user named `alice` without creating a home directory?

* [ ] `useradd -m alice`
* [x] `useradd -M alice`
* [ ] `adduser --no-home alice`
* [ ] `usermod -N alice`
* [ ] `adduser -d alice`

#### Q. Which file stores the encrypted password hashes on a typical Linux system?

* [ ] `/etc/passwd`
* [ ] `/etc/login.defs`
* [x] `/etc/shadow`
* [ ] `/etc/security/pwhash`
* [ ] `/etc/securetty`

#### Q. How do you add an existing user `bob` to the supplementary group `docker`?

* [ ] `groupadd docker bob`
* [ ] `usermod -a docker bob`
* [x] `usermod -aG docker bob`
* [ ] `addgroup bob docker`
* [ ] `gpasswd -add bob docker`

#### Q. Which command changes the user’s login shell to `/bin/zsh` for user `carol`?

* [ ] `usermod --shell zsh carol`
* [ ] `chsh carol -s zsh`
* [x] `chsh -s /bin/zsh carol`
* [ ] `useradd -s /bin/zsh carol`
* [ ] `passwd -s /bin/zsh carol`

#### Q. What does the `id` command display by default when run as a normal user?

* [ ] Current password expiry information
* [x] UID, GID, and group memberships
* [ ] Last login time and source IP
* [ ] List of all users on the system
* [ ] Home directory and shell path

#### Q. How do you lock the account of user `dave` to prevent logins?

* [ ] `passwd -e dave`
* [ ] `usermod -D dave`
* [x] `passwd -l dave`
* [ ] `userdel -r dave`
* [ ] `chage -E0 dave`

#### Q. Which directory is the default parent for newly created user home directories on many Linux distributions?

* [ ] `/home/users/`
* [ ] `/usr/home/`
* [x] `/home/`
* [ ] `/etc/home/`
* [ ] `/var/home/`
#### Q. Which protocol does LDAP use by default for directory access?

* [ ] HTTP
* [x] TCP/IP on port 389
* [ ] UDP on port 53
* [ ] SMTP on port 25
* [ ] TCP/IP on port 636

#### Q. What is the default port for LDAP over SSL (LDAPS)?

* [ ] 389
* [ ] 465
* [x] 636
* [ ] 3268
* [ ] 8443

#### Q. In an LDAP directory entry, what does “dn” stand for?

* [x] Distinguished Name
* [ ] Directory Number
* [ ] Domain Namespace
* [ ] Data Node
* [ ] Default Name

#### Q. Which file defines sudo privileges for users and groups?

* [ ] `/etc/passwd`
* [ ] `/etc/shadow`
* [x] `/etc/sudoers`
* [ ] `/etc/sudo.conf`
* [ ] `/etc/security/sudoers.d`

#### Q. What is the safest way to edit the sudoers file?

* [ ] `nano /etc/sudoers`
* [x] `visudo`
* [ ] `vim /etc/sudoers`
* [ ] `sudoedit /etc/sudoers.d`
* [ ] `edit /etc/sudoers`

#### Q. Which sudoers directive allows a user to run all commands without being prompted for a password?

* [ ] `ALL =(ALL) ALL`
* [x] `NOPASSWD: ALL`
* [ ] `PASSWD: ALL`
* [ ] `!authenticate`
* [ ] `NOPROMPT: ALL`

#### Q. In sudoers syntax, what does `%admin ALL=(ALL) ALL` do?

* [ ] Grants user “admin” full sudo rights
* [ ] Grants all users full sudo rights on hosts named “admin”
* [x] Grants all members of the “admin” group full sudo rights
* [ ] Denies group “admin” any sudo rights
* [ ] Logs all commands run by group “admin”

#### Q. Which command runs `apt update` as root but preserves your current environment variables?

* [ ] `sudo apt update`
* [ ] `sudo -i apt update`
* [x] `sudo -E apt update`
* [ ] `sudo -s apt update`
* [ ] `sudoenv apt update`

#### Q. By default, where does sudo log its authentication events on many Linux systems?

* [ ] `/var/log/syslog`
* [ ] `/var/log/messages`
* [x] `/var/log/auth.log`
* [ ] `/var/log/sudo.log`
* [ ] `/var/log/secure`

#### Q. Which sudo option runs a login shell as the target user (typically root)?

* [ ] `-E`
* [ ] `-s`
* [x] `-i`
* [ ] `-l`
* [ ] `-u`

#### Q. How do you allow user `alice` to run only `/usr/bin/systemctl` via sudo?

* [ ] `alice ALL=(ALL) ALL: /usr/bin/systemctl`
* [ ] `alice ALL=(ALL) /usr/bin/systemctl`
* [ ] `alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl`
* [x] `alice ALL=(root) /usr/bin/systemctl`
* [ ] `alice ALL=(ALL) !/usr/bin/systemctl`

#### Q. Which command displays both standard permissions and ACLs for the file `example.txt`?

* [ ] `ls -l example.txt`
* [ ] `stat -c "%A %n" example.txt`
* [x] `getfacl example.txt`
* [ ] `lsattr example.txt`
* [ ] `aclshow example.txt`

#### Q. How do you give user `bob` read (`r`) and execute (`x`) permissions on `script.sh` without affecting existing ACL entries?

* [ ] `chmod u+rx script.sh`
* [ ] `setfacl u:bob:rx script.sh`
* [x] `setfacl -m u:bob:rx script.sh`
* [ ] `setfacl --add u:bob:rx script.sh`
* [ ] `chmod +a "bob:rx" script.sh`

#### Q. Which option removes all ACL entries (but leaves standard permissions intact) on `data/`?

* [ ] `setfacl -x a:data`
* [x] `setfacl -b data/`
* [ ] `setfacl --clear-mask data/`
* [ ] `chmod a-rwx data/`
* [ ] `getfacl --remove-all data/`

#### Q. What does the “mask” entry in an ACL represent?

* [ ] The maximum file size allowed
* [x] The maximum permissions granted to named users and groups
* [ ] The default ACL applied to new files
* [ ] The owner’s effective permissions
* [ ] A special ACL for the `root` user

#### Q. How do you set a default ACL so that any new file in `project/` grants group `devs` write access?

* [ ] `setfacl -m d:g:devs:rw project/`
* [x] `setfacl -d -m g:devs:rw project/`
* [ ] `setfacl --default g:devs:rw project/`
* [ ] `setfacl -m g:devs:rw project/`
* [ ] `chmod g+w project/`

#### Q. Which command recursively applies the ACL change to all files and subdirectories under `shared/`?

* [ ] `setfacl -m u:alice:r shared/`
* [ ] `setfacl --recursive u:alice:r shared/`
* [x] `setfacl -R -m u:alice:r shared/`
* [ ] `getfacl -R shared/ | setfacl --apply`
* [ ] `chmod -R +a "alice:rx" shared/`

#### Q. After setting ACLs, which command shows the effective permissions for user `carol` on `report.pdf`?

* [ ] `getfacl --effective carol report.pdf`
* [x] `getfacl -e report.pdf`
* [ ] `setfacl --check u:carol report.pdf`
* [ ] `aclcheck report.pdf carol`
* [ ] `stat -c "%A %n" report.pdf`

#### Q. To remove only the ACL entry for group `sales` on `budget.xls`, which command is correct?

* [ ] `setfacl -m g:sales: budget.xls`
* [ ] `setfacl --delete g:sales budget.xls`
* [x] `setfacl -x g:sales budget.xls`
* [ ] `chmod g-sales- budget.xls`
* [ ] `getfacl -x g:sales budget.xls`

#### Q. What happens if you copy a file with ACLs using `cp --preserve=all`?

* [ ] The ACLs are stripped on the copy.
* [ ] Only the owner and group ACL entries are kept.
* [x] All ACL entries and attributes are preserved on the copy.
* [ ] The copy is placed in a default ACL-enabled directory.
* [ ] The mask is reset but other ACLs are kept.

#### Q. Which umask setting will ensure that new files allow group write permission so ACL default entries can grant rwx to a group?

* [ ] `umask 022`
* [ ] `umask 077`
* [x] `umask 002`
* [ ] `umask 027`
* [ ] `umask 007`

#### Q. What does the `sudo -l` command do for the invoking user?

* [ ] Lists all processes running as root
* [x] Lists which commands the user is allowed (and not allowed) to run via sudo
* [ ] Locks the sudo account for one hour
* [ ] Logs you out of the root shell
* [ ] Lists all sudo logs

#### Q. Which default in `/etc/sudoers` prevents users from keeping their environment variables unless explicitly allowed?

* [ ] `env_keep`
* [ ] `env_passwd`
* [x] `env_reset`
* [ ] `requiretty`
* [ ] `preserve_env`

#### Q. Which permission bit allows a user to read a file?

* [x] `r`
* [ ] `w`
* [ ] `x`
* [ ] `s`
* [ ] `t`

#### Q. What does the octal permission `754` represent for user/group/others?

* [ ] `rwx rwx rwx`
* [ ] `rw- r-x r--`
* [x] `rwx r-x r--`
* [ ] `rwx r-- r-x`
* [ ] `rwx rw- r-x`

#### Q. How do you add execute permission for the owner of `script.sh` without affecting other bits?

* [ ] `chmod 700 script.sh`
* [ ] `chmod u=+x script.sh`
* [x] `chmod u+x script.sh`
* [ ] `chmod +x script.sh`
* [ ] `chmod a+x script.sh`

#### Q. Which special permission on a directory causes new files to inherit the directory’s group?

* [ ] Sticky bit (`chmod +t`)
* [ ] Set-user-ID (`chmod u+s`)
* [x] Set-group-ID (`chmod g+s`)
* [ ] No-execute (`chmod -x`)
* [ ] Immutable bit (`chattr +i`)

#### Q. What does the sticky bit (`t`) do when set on `/tmp`?

* [ ] Makes files in `/tmp` executable
* [ ] Prevents deletion by anyone
* [x] Restricts file deletion so only owner/root can remove their files
* [ ] Inherits owner’s permissions on new files
* [ ] Encrypts files in `/tmp`

#### Q. How do you recursively set permissions `755` on all directories under `project/`?

* [ ] `chmod -R 755 project/`
* [ ] `find project/ -type f -exec chmod 755 {} +`
* [x] `find project/ -type d -exec chmod 755 {} +`
* [ ] `chmod 755 project/*`
* [ ] `chmod 755 project/**`

#### Q. Which command shows the numeric (octal) permission representation for files in the current directory?

* [ ] `ls -l`
* [x] `stat -c "%a %n" *`
* [ ] `getfacl *`
* [ ] `ls -n`
* [ ] `stat --octal *`

#### Q. What is the effect of `chmod o-rwx file.txt`?

* [ ] Grants all permissions to others
* [ ] Removes read/write, grants execute to others
* [x] Revokes all permissions (read, write, execute) for others
* [ ] Sets owner permissions to none
* [ ] Makes the file immutable

#### Q. Which command displays both standard and ACL permissions for `data/`?

* [ ] `ls -la data/`
* [x] `getfacl data/`
* [ ] `stat data/`
* [ ] `aclshow data/`
* [ ] `lsattr data/`

#### Q. How do you set an ACL to give user `bob` read and write access to `report.txt`?

* [ ] `chmod user: bob:rw report.txt`
* [ ] `setfacl -R u:bob:rw report.txt`
* [x] `setfacl -m u:bob:rw report.txt`
* [ ] `setfacl --add bob:rw report.txt`
* [ ] `aclmod u:bob:rw report.txt`

#### Q. Which command-line tool can you use to search an LDAP directory?

* [ ] ldapadd
* [ ] ldapmodify
* [x] ldapsearch
* [ ] ldappasswd
* [ ] slapcat

#### Q. In the LDAP schema, which attribute uniquely identifies an entry within its parent?

* [ ] cn (Common Name)
* [x] rdn (Relative Distinguished Name)
* [ ] uid (User ID)
* [ ] objectClass
* [ ] dn (Distinguished Name)

#### Q. Which suffix is commonly used to specify the base DN for a company “example.com”?

* [ ] dc=company,dc=com
* [ ] dn=example,cn=com
* [x] dc=example,dc=com
* [ ] ou=example,ou=com
* [ ] cn=example,cn=com

#### Q. How do you add a new entry to the directory using LDAP tools?

* [ ] slapcat -i entry.ldif
* [x] ldapadd -f entry.ldif
* [ ] ldapmodify -a entry.ldif
* [ ] ldapsearch -a entry.ldif
* [ ] ldapdelete -f entry.ldif

#### Q. Which operation modifies an existing LDAP entry?

* [ ] ldapadd
* [ ] ldapdelete
* [x] ldapmodify
* [ ] ldapsearch
* [ ] slapindex

#### Q. What file format is used to batch import or export LDAP entries?

* [ ] JSON
* [ ] XML
* [x] LDIF
* [ ] CSV
* [ ] YAML

#### Q. Which objectClass would you include to create a user entry in OpenLDAP?

* [ ] objectClass: organization
* [ ] objectClass: domain
* [x] objectClass: inetOrgPerson
* [ ] objectClass: posixGroup
* [ ] objectClass: ldapSubentry

#### Q. To delete user `eve` and remove her home directory and mail spool, which command is correct?

* [ ] `userdel eve --remove`
* [ ] `deluser eve --home`
* [x] `userdel -r eve`
* [ ] `usermod --delete eve -h`
* [ ] `rmuser eve -a`

#### Q. Which file associates group names with GIDs and lists group membership?

* [ ] `/etc/passwd`
* [x] `/etc/group`
* [ ] `/etc/shadow`
* [ ] `/etc/gshadow`
* [ ] `/etc/sudoers`
