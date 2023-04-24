## File Permissions

There are several mechanisms for controlling access to files and directories, including standard permissions, special permissions, and access control lists (ACLs).

## Understanding Permissions

Linux permissions control access to files and directories. There are three types of permissions: read (r), write (w), and execute (x).

| Permission | Files                                | Dirs                                            |
| ---------- | ------------------------------------ | ----------------------------------------------- |
| read       | User can read file's content         | User can list files in the directory            |
| write      | User can modify file's content       | User can add and delete files in the directory  |
| execute    | User can run the file as a command   | User can enter the directory                    |

### Defining Permissions symbolically

Permissions may be specified symbolically, using the symbols.

| Symbol | Meaning   |
| ------ | --------- |
| u      | user      |
| g      | group     |
| o      | other     |
| a      | all       |
| r      | read      |
| w      | write     |
| x      | execute   |
| +      | add       |
| -      | remove    |
| =      | assign    |

For example, the following command will grant the file's owner execution permission:

```bash
chmod u+x file
```

## Numeric Permissions

Permissions are represented by three digits specifying permissions for the owner (user), group, and others.

| Permissions | Digit |
| --- | --- |
| --- | 0 |
| --x | 1 |
| -w- | 2 |
| -wx | 3 |
| r-- | 4 |
| r-x | 5 |
| rw- | 6 |
| rwx | 7 |

Each digit is made up of three bits, with each bit representing a particular permission: read (r), write (w), and execute (x). The permission mode is written as three octal digits, with each digit corresponding to the permissions for the user, group, and others, respectively.

For example, the permission mode 771 specifies that:

* the user has read, write, and execute permissions (7 = rwx)
* the group has read, write, and execute permissions (7 = rwx)
* others have execute permissions (1 = --x)

You can use the `chmod` command to change the permission mode of a file or directory. For example:

```
chmod 771 path/to/file.txt
```

## Default Permissions

Default permissions define the access rights for new files and directories. By default, new files have permissions `rw-rw-rw-` (`666`), allowing any user to read and write but not execute the file. New directories have permissions `rwxrwxrwx` (`777`), permitting any user to read, write, and execute within the directory.

Use the umask command to modify default permissions for new files and directories. The umask is a number indicating which permissions should be removed (masked) when creating a new file or directory. For instance, a umask of `0022` removes write permission for others, resulting in default permissions of `rw-r--r--` (`644`) for new files and `rwxr-xr-x` (`755`) for new directories.

To view the current umask value, use the umask command:

```bash
umask
```

To set the umask value, use the umask command with the desired octal value:

```bash
umask 0022
```

The umask value applies only to new files and directories, not existing ones.

Examples of common umask values and the resulting default permissions:

| Umask value	| Default file permissions | Default directory permissions |
| ----------- | ------------------------ | ----------------------------- |
| 022	| rw-r--r--	| rwxr-xr-x |
| 027	| rw-r-----	| rwxr-x--- |
| 077 |	rw-------	| rwx------ |

For example, if we want to:

1. Prevent the file's owner (user) from being granted the execute permission while keeping other owner permissions;
2. Allow the group to read but restrict writing or executing;
3. Grant write permission for others without changing other permissions.

Then, we would use:

```bash
umask u-x,g=r,o+w
```

## Special Permissions: setuid, setgid, and the Sticky Bit

Linux has special permissions that can be set on files and directories for additional privileges or restrictions:

- `setuid`: a bit that enables an executable to run with the file owner's privileges. Useful for allowing users to execute certain programs as the file owner, even without direct file access permissions.
- `setgid`: a bit that allows an executable to run with the file's group privileges. Useful for sharing access to a program or files with a group of users without individual file access permissions.
- `sticky bi`t: a directory bit that lets only the owner or root remove files and subdirectories. Useful for preventing users from deleting or altering files in a shared directory.

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

Use these special permissions cautiously, as they may pose security risks if misused.

## ACls

ACLs are discretionary access control systems built on top of standard Linux permissions. They provide finer control over file and directory access and manipulation, beyond regular user, group, and other permissions.

Not all tools support ACLs, but modern mke2fs usually sets ACL in default mount options during filesystem creation in "enterprise" Linux distributions. The filesystem must be mounted with the acl option to use ACLs.

Use the `setfacl` command to set (replace), modify, or remove a file or directory's ACL. It can also update and delete ACL entries for specified files and directories. If no path is provided, file and directory names come from standard input (stdin). Each input line should have one path name.

Modify ACLs using the `-m` flag followed by the desired ACL specification:

```
setfacl -m g:group_name:rw /opt/test
```

Remove the ACL using the `-x` flag followed by the ACL specification to be removed:

```
setfacl -x g:group_name /opt/test
```

Display a file or directory's ACL using the `-l` flag:

```
getfacl /opt/test
```

Examples of common ACL specifications:

* `u:user_name:rwx`: grant read, write, and execute permissions to user_name
* `g:group_name:r-x`: grant read and execute permissions to group_name
* `o:r--`: grant read permission to others
* `m:rwx`: grant read, write, and execute permissions to file owner (u) and file's group (g)
* `:r-x`: grant read and execute permissions to everyone (equivalent to a:r-x)
* `:---`: remove all permissions for everyone (equivalent to a:---)

ACLs are applied in addition to standard Linux permissions and may override or augment them. For instance, a file with standard permissions `rw-rw-r--` and an ACL entry `g:r-x` grants the group read and execute permissions, despite the standard permissions not granting execute permission.

## Challenges

1. Create a temporary text file named `temp.txt` in your home directory. Check the permissions using `ls -l`. You might see:

```bash
-rw-rw-r-- 1 user_name user_group  8 Nov 21 18:02 temp.txt
```

The file is owned by "user_name" and the group "user_group", who can write to it. Other users can read it. Remove write permission for "user_group" and read permission from others.

2. Copy a root-owned file from `/etc/` to your home directory. Who owns this file now?
3. Display any file's umask in both octal and symbolic form.
4. What happens if a file owner lacks the necessary permissions to interact with the file? Can they still remove it?
5. Describe what happens when you try to remove a group's write permission to the file and read permission from others.
6. Explain the difference between permissions and ACLs.
7. Can a non-owner user change a file or directory's permissions?
8. Should you use ACLs or permissions to restrict file and directory access?
