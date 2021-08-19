<h2>Permissions</h2>

| Command | Description | Description |
| --- | --- | --- |
| read | The file's contents can be seen by the user | The files in the directory can be listed by the user |
| write | The file's contents can be changed by the user | The user can add new files to the directory and delete old ones |
| execute | The filename can be used as a UNIX command by the user | The user can go to the directory, but they cannot list the files unless they have read permission. |

Permissions may be specified symbolically, using the symbols u (user), g (group), o (other), a (all), r (read), w (write), x (execute), + (add permission), - (take away permission) and = (assign permission).

For example, the following command will grant the file's owner execution permission:

```bash
chmod u+x file
```

| Permissions | Number |
| --- | --- |
| --- | 0 |
| --x | 1 |
| -w- | 2 |
| -wx | 3 |
| r-- | 4 |
| r-x | 5 |
| rw- | 6 |
| rwx | 7 |

<h2>Default permissions</h2>

* Files: rw-rw-rw- (666)
* Directories: rwxrwxrwx (777)

Use umask to change the default permissions. With no options specified umask, displays which current default permissions are removed (masked).
Three numbers, for user, group and others.

```bash
umask
```

For example, let's say we want to:

1. prevent the file's owner (user) from being granted the execute permission while leaving the rest of the owner permissions untouched;
2. allow the group to read while restricting the group from writing or executing;
3. allow write permission for others while not changing the other permissions.
then, we would use:

```bash
umask u-x,g=r,o+w
```

<h2>ACls</h2>
ACLs (access control lists) in Linux are discretionary access control system permissions that are built on top of regular Linux permissions.

* not all tools support ACLs
* a modern mke2fs now sets acl in default mount options automatically at filesystem creation time, at least in "enterprise" Linux distributions

Set (replaces), modify, or remove the access control list using the <i>setfacl</i> command (ACL). It also updates and deletes ACL entries for each path-specified file and directory. If no path is given, the names of files and directories are taken from standard input (stdin). In this scenario, each line of input should have one path name.

* use <i>-m</i> flag to modify the ACLs:

```bash
setfacl -m g:group_name:rw /opt/test
```

* to have all new files in the directory inherit the ACLs, use the <i>-m</i> flag with the <i>d</i> option:
* 
```bash
setfacl -m d:g:group_name:rw /opt/test
```

* use <i>-X</i> lag to remove a user or group:

```bash
setfacl -X g:group_name /opt/test
```

* use <i>-b</i> flag to remove everything: 

```bash
setfacl -b /opt/test
```

* use <i>-k</i> flag to go back to default ACL's: 

```bash
setfacl -k /opt/test
```

* ACLs from one file/dir can be reused in another one:

```bash
getfacl /opt/test | setfacl --set-file= /opt/test2
```
