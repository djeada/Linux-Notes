# File Permissions

There are several mechanisms for controlling access to files and directories, including standard permissions, special permissions, and access control lists (ACLs).

## Understanding Permissions

Permissions in Linux control who can access and manipulate files and directories. There are three types of permissions: read (r), write (w), and execute (x).

| Permission | Files | Dirs |
| --- | --- | --- |
| read | The file's contents can be seen by the user. | The files in the directory can be listed by the user. |
| write | The file's contents can be changed by the user. | The user can add new files to the directory and delete old ones. |
| execute | The filename can be used as a UNIX command by the user. | The user can go to the directory, but they cannot list the files unless they have read permission. |

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

## Default Permissions

Default permissions determine the access rights granted to new files and directories. By default, new files have permissions of `rw-rw-rw-` (`666`), which means that any user can read and write to the file, but cannot execute it. New directories have permissions of `rwxrwxrwx` (`777`), which means that any user can read, write, and execute within the directory.

The umask command can be used to change the default permissions for new files and directories. The umask is a number that specifies which permissions should be removed (masked) when a new file or directory is created. For example, a umask of `0022` would remove write permission for others, resulting in default permissions of `rw-r--r--` (`644`) for new files and `rwxr-xr-x (`755`) for new directories.

To view the current umask value, use the umask command without any arguments:

```bash
umask
```

To set the umask value, use the umask command followed by the desired umask value in octal form:

```bash
umask 0022
```

It's important to note that the umask value is only applied to new files and directories, and has no effect on existing files and directories.

Here are some examples of common umask values and the resulting default permissions:

| Umask value	| Default file permissions | Default directory permissions |
| ----------- | ------------------------ | ----------------------------- |
| 022	| rw-r--r--	| rwxr-xr-x |
| 027	| rw-r-----	| rwxr-x--- |
| 077 |	rw-------	| rwx------ |


For example, let's say we want to:

1. prevent the file's owner (user) from being granted the execute permission while leaving the rest of the owner permissions untouched;
2. allow the group to read while restricting the group from writing or executing;
3. allow write permission for others while not changing the other permissions.

Then, we would use:

```bash
umask u-x,g=r,o+w
```

## Special Permissions: setuid, setgid, and the Sticky Bit

Linux has several special permissions that can be set on files and directories to grant additional privileges or restrict certain actions. These special permissions include:

* `setuid`: a bit that causes an executable to execute with the file's owner's privileges. This can be useful for allowing users to execute certain programs as if they were the owner of the file, even if they do not have the necessary permissions to access the file directly.

* `setgid`: a bit that causes an executable to execute with the privileges of the file's group. This can be useful for allowing a group of users to share access to a program or set of files, even if they do not have individual permissions to access the files directly.

* `sticky bit`: a directory bit that permits only the owner or root to remove files and subdirectories. This can be useful for preventing users from deleting or altering files in a shared directory.

To set the setuid bit on a file, use the chmod command with the `u+s` flag:

```
chmod u+s /path/to/file
```

To remove the setuid bit, use the chmod command with the `u-s` flag:

```
chmod u-s /path/to/file
```

To set the setgid bit on a directory, use the chmod command with the `g+s` flag:

```
chmod g+s /path/to/dir
```

To remove the setgid bit, use the chmod command with the `g-s` flag:

```
chmod g-s /path/to/dir
```

To set the sticky bit on a directory, use the chmod command with the `+t` flag:

```
chmod +t /path/to/dir
```

To remove the sticky bit, use the chmod command with the `-t` flag:

```
chmod -t /path/to/dir
```
It's important to note that these special permissions are typically used sparingly, as they can pose security risks if misused.

## ACls
Access control lists (ACLs) are discretionary access control system permissions that are built on top of regular Linux permissions. They allow more fine-grained control over who can access and manipulate files and directories, beyond the standard user, group, and other permissions.

Not all tools support ACLs, but a modern mke2fs now sets ACL in default mount options automatically at filesystem creation time, at least in "enterprise" Linux distributions. To use ACLs, the filesystem must be mounted with the acl option.

The setfacl command can be used to set (replace), modify, or remove the ACL for a file or directory. It can also update and delete ACL entries for each path-specified file and directory. If no path is given, the names of files and directories are taken from standard input (stdin). In this scenario, each line of input should have one path name.

To modify the ACLs, use the `-m` flag followed by the desired ACL specification:

```
setfacl -m g:group_name:rw /opt/test
```

To remove the ACL, use the `-x` flag followed by the ACL specification to be removed:

```
setfacl -x g:group_name /opt/test
```

To display the ACL for a file or directory, use the `-l` flag:

```
getfacl /opt/test
```

Here are some examples of common ACL specifications:

* `u:user_name:rwx`: grant read, write, and execute permissions to the user named user_name
* `g:group_name:r-x`: grant read and execute permissions to the group named group_name
* `o:r--`: grant read permission to others
* `m:rwx`: grant read, write, and execute permissions to the file's owner (u) and the file's group (g)
* `:r-x`: grant read and execute permissions to everyone (equivalent to a:r-x)
* `:---`: remove all permissions for everyone (equivalent to a:---)

It's important to note that ACLs are applied in addition to the standard Linux permissions, and may override or augment them in certain cases. For example, if a file has standard permissions of `rw-rw-r--` and an ACL entry of `g:r-x`, the group would have read and execute permissions, even though the standard permissions do not grant execute permission.

## Challenges

1. Make a temporary text file named temp.txt in your home directory. Using the <code>ls -l</code> command, check the permissions. You'll probably see something like this: 

```bash
-rw-rw-r-- 1 user_name user_group  8 Nov 21 18:02 temp.txt
```

As a result, the file is owned by the user "user name" and the group "user group," who are the only ones who can write to it - but any other user may read it.

Now remove the "user group" group's permission to write to the file and read permission from others.

2. Copy a root-owned file from /etc/ to your home directory; who now owns this file? 
3. Show the umask of any file in both octal and symbolic form.
4. What happens when the owner of a file does not have the necessary permissions to interact with it? Can he, at the very least, remove such a file? 
5. Explain what happens when you try to remove the group's permission to write to the file and read permission from others.
6. Explain the difference between permissions and ACLs.
7. Can a user who is not the owner of a file or directory change the permissions of the file or directory?
8. Should you use ACLs or permissions to restrict file and directory access? 
