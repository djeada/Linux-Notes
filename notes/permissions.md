<h1>Permissions</h1>

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

<h1>Default permissions</h1>

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

<h1>ACls</h1>
ACLs (access control lists) in Linux are discretionary access control system permissions that are built on top of regular Linux permissions.

* not all tools support ACLs
* a modern mke2fs now sets acl in default mount options automatically at filesystem creation time, at least in "enterprise" Linux distributions

Set (replaces), modify, or remove the access control list using the <code>setfacl</code> command (ACL). It also updates and deletes ACL entries for each path-specified file and directory. If no path is given, the names of files and directories are taken from standard input (stdin). In this scenario, each line of input should have one path name.

* use <code>-m</code> flag to modify the ACLs:

```bash
setfacl -m g:group_name:rw /opt/test
```

* to have all new files in the directory inherit the ACLs, use the <code>-m</code> flag with the <code>d</code> option:

```bash
setfacl -m d:g:group_name:rw /opt/test
```

* use <code>-X</code> lag to remove a user or group:

```bash
setfacl -X g:group_name /opt/test
```

* use <code>-b</code> flag to remove everything: 

```bash
setfacl -b /opt/test
```

* use <code>-k</code> flag to go back to default ACL's: 

```bash
setfacl -k /opt/test
```

* ACLs from one file/dir can be reused in another one:

```bash
getfacl /opt/test | setfacl --set-file= /opt/test2
```

<h1>Challenges</h1>

1. Make a temporary text file named temp.txt in your home directory. Using the <code>ls -l</code> command, check the permissions. You'll probably see something like this: 

```bash
-rw-rw-r-- 1 user_name user_group  8 Nov 21 18:02 temp.txt
```

As a result, the file is owned by the user "user name" and the group "user group," who are the only ones who can write to it - but any other user may read it.

Now remove the "user group" group's permission to write to the file and read permission from others.

2. Explain what happens when you try to remove the group's permission to write to the file and read permission from others.
3. Explain the difference between permissions and ACLs.
4. Can a user who is not the owner of a file or directory change the permissions of the file or directory?
5. Should you use ACLs or permissions to control access to a file or directory?
