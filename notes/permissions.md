## File Permissions

File permissions are crucial in any Unix-like operating systems, including Linux, which employ several mechanisms for controlling access to files and directories. These mechanisms include standard permissions, special permissions, and access control lists (ACLs).

### Standard Permissions
The primary set of file permissions, commonly known as standard permissions, governs the fundamental access levels for files and directories. These permissions fall into three categories:

- Read (`r`)
- Write (`w`)
- Execute (`x`)

Each permission category confers specific capabilities for users, as detailed in the following table:

| Permission | Effect on Files                                 | Effect on Directories                                      |
|------------|-------------------------------------------------|------------------------------------------------------------|
| Read (`r`) | Allows viewing and reading the contents of files.| Enables the listing of directory contents.                 |
| Write (`w`)| Permits modification or deletion of file contents.| Allows adding, deleting, or renaming files in the directory.|
| Execute (`x`)| Enables running the file as a program or script. | Grants the ability to enter the directory and execute commands within it, or access files therein.|

These permissions can be set for different classes of users, each with varying levels of access:

- User (`u`): The owner of the file.
- Group (`g`): Users who are part of the file's group.
- Others (`o`): All other users.

The arrangement of these permissions is typically presented as follows:

```
Owner     Group      Others
r w x     r w x      r w x
| | |     | | |      | | |
| | |     | | |      | | +--- Execute
| | |     | | |      | +----- Write
| | |     | | |      +------- Read
| | |     | | |
| | |     | | +--- Execute
| | |     | +----- Write
| | |     +------- Read
| | |
| | +--------- Execute
| +----------- Write
+------------- Read
```

### Symbolic File Permissions

Symbolic permissions use a set of specific symbols to represent different types of permissions, and who they apply to. The symbols used include:

| Symbol | Meaning                                        |
| ------ | ---------------------------------------------- |
| u      | user (file's owner)                            |
| g      | group (members of the file's owning group)     |
| o      | others (users not in the file's owning group)  |
| a      | all (equivalent to ugo)                        |
| r      | read                                           |
| w      | write                                          |
| x      | execute                                        |
| +      | add the specified permission                   |
| -      | remove the specified permission                |
| =      | assign the specified permission exactly        |

For instance, the command `chmod u+x file` adds execute (`+x`) permissions to the user (`u`) who owns the file named `file`.

### Numeric File Permissions

Numeric or octal permissions, on the other hand, use a three-digit numeric representation for each permission type. Each digit (ranging from 0 to 7) corresponds to a unique combination of read (r), write (w), and execute (x) permissions, as outlined in the table below:

| Permission Combination | Numeric Representation |
| ---------------------- | --------------------- |
| ---                    | 0                     |
| --x                    | 1                     |
| -w-                    | 2                     |
| -wx                    | 3                     |
| r--                    | 4                     |
| r-x                    | 5                     |
| rw-                    | 6                     |
| rwx                    | 7                     |

The first digit represents permissions for the file's owner (user), the second digit represents permissions for the owning group, and the third digit represents permissions for others.

Here's how it works:

1. For the user, group, and others, calculate the numeric value of the permissions you want to assign. For example, read, write, and execute permissions correspond to 7 (rwx = 4+2+1 = 7).
2. Write these values in the order: user, group, others. 

For example, the octal permission mode `771` means:

- The user (file's owner) has read, write, and execute permissions (7 = rwx).
- The owning group members have read, write, and execute permissions (7 = rwx).
- Other users have execute permissions only (1 = --x).

You can assign these permissions using the `chmod` command as follows:

```bash
chmod 771 path/to/file.txt
```

This command sets the permissions of the file path/to/file.txt to 771, as explained above.

### Default Permissions

In Linux, when you create a new file or directory, it is assigned a set of default permissions. These permissions define what types of access are allowed for the owner of the file, members of the group that owns the file, and all other users.

#### Default File and Directory Permissions

By default, new files are created with the permissions `rw-rw-rw-`, equivalent to the numeric value `666`. This allows any user to read and write to the file, but not execute it.

New directories, on the other hand, are created with the permissions `rwxrwxrwx` or `777`. This allows any user to read, write, and execute within the directory.

#### Using Umask to Change Default Permissions

The `umask` command is used to determine the default permissions for newly created files and directories. It's a three-digit number that specifies which permissions should be removed or "masked" when new files and directories are created. 

For example, a `umask` value of `0022` subtracts write permissions for group and others from the default permissions, resulting in default permissions of `rw-r--r--` (`644`) for new files and `rwxr-xr-x` (`755`) for new directories.

To view the current `umask` value, simply use the `umask` command:

```bash
umask
```

To change the umask value, use the umask command followed by the desired octal value:

```bash
umask 0022
```

This will set the umask value to 0022, and new files and directories will be created with the corresponding default permissions. It's important to note that the umask value only affects new files and directories, not existing ones.

#### Examples of Umask Values and Their Effects

Here are some common umask values and the resulting default permissions for files and directories:

| Umask | Value	Default File Permissions | Default Directory Permissions |
| ----- | ------------------------------ | ----------------------------- |
| 022 |	rw-r--r--	| rwxr-xr-x |
| 027	| rw-r-----	| rwxr-x--- |
| 077	| rw-------	| rwx------ |

You can also set the umask value symbolically. For instance, if we want to:

- Remove execute permissions from the owner (user) of a new file while preserving other permissions (u-x).
- Limit the group to only having read permissions (g=r).
- Add write permissions for others without changing their other permissions (o+w).

The umask command would look like this:

```bash
umask u-x,g=r,o+w
```

This command configures the umask such that new files and directories will have the permissions specified.

### Special Permissions: setuid, setgid, and the Sticky Bit

In addition to standard permissions, Linux offers special permissions known as setuid, setgid, and the sticky bit. These permissions provide additional control over access to files and directories and can be used to enhance both functionality and security.

```
Owner   Group   Others
rws     rws     rwt
|||     |||     |||
|||     |||     ||+---- Sticky Bit
|||     |||     |+----- Execute
|||     |||     +------ Write
|||     |||
|||     ||+------ Set Group ID (setgid)
|||     |+------- Execute
|||     +-------- Write
|||
||+-------- Set User ID (setuid)
|+--------- Execute
+---------- Read
```

#### Setuid

The setuid (“set user ID”) bit causes a program to run with the file owner’s user permissions, rather than with the permissions of the user who launched it. In practice, this allows ordinary users to execute specific tasks with elevated privileges—most commonly, root-level privileges—without giving them full root access.

**Why it matters:**

* The `passwd` command needs to modify `/etc/shadow`, which is owned by root. By marking `/usr/bin/passwd` as setuid root, any user can change their own password despite not having write access to the shadow file.
* If a setuid binary is vulnerable (e.g., buffer overflow), an attacker might exploit it to gain root. Always audit and minimize setuid programs.

**How to set the setuid bit:**

```bash
chmod u+s /path/to/program
```

* This adds the “s” in the owner’s execute field.
* Octal equivalent: `chmod 4755 /path/to/program`.

**How to remove the setuid bit:**

```bash
chmod u-s /path/to/program
```

* Removes the “s”, reverting to a normal execute bit.
* Octal equivalent: `chmod 0755 /path/to/program`.

**How to verify if setuid is in place:**

```bash
ls -l /path/to/program
```

* *Set:* `-rwsr-xr-x` → the owner’s `x` is replaced by `s`.
* *Not set (counter-example):* `-rwxr-xr-x`.

**Find all setuid files:**

```bash
find / -perm /4000 -type f 2>/dev/null
```

Lists every file on the system with the setuid bit.

#### Setgid

The setgid (“set group ID”) bit causes an executable to run with the group permissions of the file’s group owner, or on a directory, causes newly created files within to inherit the directory’s group. This facilitates controlled collaboration among group members.

**Why it matters:**

* A backup script owned by group `backup` can be run by any user in that group, with file-creation operations done under the `backup` group, ensuring correct group ownership of backup archives.
* On `/srv/shared`, setgid makes new files inherit the `shared` group, so every team member automatically has group write permission on new files.
* A setgid program with flaws could let a non-group member escalate privileges to that group, potentially accessing sensitive group-owned resources.

**How to set the setgid bit:**

```bash
chmod g+s /path/to/file_or_directory
```

* *Octal equivalent (file):* `chmod 2755 /path/to/file`
* *Octal equivalent (directory):* `chmod 2775 /path/to/directory`

**How to remove the setgid bit:**

```bash
chmod g-s /path/to/file_or_directory
```

Octal equivalent: `chmod 0755 /path/to/file` or `chmod 0775 /path/to/directory`

**How to verify if setgid is in place:**

```bash
ls -ld /path/to/file_or_directory
```

* *Executable with setgid:* `-rwxr-sr-x` (the group’s `x` is replaced by `s`).
* *Directory with setgid:* `drwxrwsr-x`.
* *Not set (counter-example):* `-rwxr-xr-x` or `drwxr-xr-x`.

**Find all setgid files/directories:**

```bash
find / -perm /2000 -type f -or -type d 2>/dev/null
```

Searches for the setgid bit in both files and directories.

#### Sticky Bit

When set on a directory, the sticky bit ensures that within that directory, only the file’s owner (or root) may delete or rename their files. It prevents users from removing or renaming other users’ files in a shared directory.

**Why it matters:**

* On `/tmp`, the sticky bit prevents user A from deleting user B’s temporary files, even though `/tmp` is world-writable.
* Without the sticky bit on a shared directory like `/shared`, any user with write permission could delete or rename another user’s files, leading to accidental or malicious data loss.

**How to set the sticky bit:**

```bash
chmod +t /path/to/directory
```

Octal equivalent: `chmod 1777 /path/to/directory` (common for `/tmp`).

**How to remove the sticky bit:**

```bash
chmod -t /path/to/directory
```

Octal equivalent, restoring typical permissions: `chmod 0777 /path/to/directory`.

**How to verify if the sticky bit is in place:**

```bash
ls -ld /path/to/directory
```

* *Set:* `drwxrwxrwt` – the others’ execute bit is replaced by `t`.
* *Not set (counter-example):* `drwxrwxrwx`.

**Find all sticky directories:**

```bash
find / -type d -perm /1000 2>/dev/null
```

Lists all directories that have the sticky bit set.

#### Quick Reference Table

| Permission | Symbol in `ls -l`            | Octal Mask | Common Use Case                            |
| ---------- | ---------------------------- | ---------- | ------------------------------------------ |
| setuid     | `-rws------`                 | 4xxx       | `passwd` (user password changes)           |
| setgid     | `-rwxr-s---` or `drwxrws---` | 2xxx       | Shared project dirs, group-run executables |
| sticky     | `drwxrwxrwt`                 | 1xxx       | `/tmp`, other world-writable shared dirs   |

Use these checks and examples to ensure each special permission is applied correctly and safely. Keywords for `find` (4000 for setuid, 2000 for setgid, 1000 for sticky) will help audit your system comprehensively.

### Access Control Lists (ACLs)

Access Control Lists (ACLs) are an additional layer of discretionary access control provided by many Linux systems. They allow for more fine-grained control over file and directory access, extending beyond the standard user, group, and other permissions.

ACLs are not supported by all tools, but modern 'mke2fs' typically enables ACLs in the default mount options during filesystem creation in enterprise Linux distributions. To utilize ACLs, the filesystem must be mounted with the 'acl' option.

```
  Type : Entity : Permissions
    |      |         |
    |      |         +---- Read (r), Write (w), Execute (x)
    |      |
    |      +-------------- User name or Group name
    |
    +--------------------- User (u), Group (g), Others (o), Mask (m)
```

#### Setting ACLs with `setfacl`

The `setfacl` command is used to manage ACLs on a file or directory. It can set, modify, or remove ACL entries. If no path is provided, it takes file and directory names from the standard input (stdin). Each line of input should contain one path name.

To modify ACLs, use the `-m` flag followed by the ACL specification. For example, the following command grants read and write permissions to a specific group on a directory:

```bash
setfacl -m g:group_name:rw /opt/test
```

To remove an ACL, use the -x flag followed by the ACL specification to be removed. For example:

```bash
setfacl -x g:group_name /opt/test
```

#### Viewing ACLs with getfacl

The getfacl command is used to display the ACLs of a file or directory. Use the -l flag to list the ACLs:

```bash
getfacl /opt/test
```

#### ACL Specifications

ACL specifications define who has what kind of access to a file or directory. Here are some common examples:

- `u:user_name:rwx` : Grants read, write, and execute permissions to a specific user.
- `g:group_name:r-x` : Grants read and execute permissions to a specific group.
- `o:r--` : Grants read permissions to others.
- `m:rwx` : Grants read, write, and execute permissions to both the owner of the file (u) and the file's group (g).
- `:r-x` : Grants read and execute permissions to everyone (equivalent to a:r-x).
- `:---` : Removes all permissions for everyone (equivalent to a:---).

ACLs are applied in conjunction with standard Linux permissions, and they can either override or supplement them. For example, a file with standard permissions of rw-rw-r-- and an ACL entry of g:r-x would grant read and execute permissions to the group, even though the standard permissions do not grant execute permission. Thus, with the proper use of ACLs, you can achieve a higher level of security and flexibility in managing file and directory access.

### Challenges

1. Create a temporary text file named `temp.txt` in your home directory and use `ls -l` to display its permissions. Note the permissions displayed (e.g., `-rw-rw-r--`), which indicate that both the owner and group have write access, while others have only read access. Use `chmod` to remove write permissions for the group and read permissions for others, and then verify the changes. Discuss how modifying permissions affects file accessibility.
2. Copy a file owned by root, such as `/etc/hosts`, to your home directory, and then check its permissions using `ls -l`. Examine who now owns the file in your home directory, and discuss the implications of file ownership during copy operations, especially when copying files from privileged directories.
3. Use the `umask` command to display the current umask value in octal form. Convert this value to symbolic form and explain how umask affects the default permissions of newly created files and directories. Create a new file and verify its permissions to see how they are influenced by the umask setting.
4. Identify a file owned by a user who lacks read or write permissions on it, and then check if the user can still remove the file. Use appropriate commands to test and explain the results, discussing how file deletion is affected by directory permissions rather than file permissions.
5. If you create bash scripts with `sudo` while configuring a server, how does that affect their ownership and permissions, and will regular users still be able to execute them afterward?
6. Use `chmod` to remove write permissions for the group and read permissions for others on a file. Observe how these changes impact the file’s accessibility, and explain the process of modifying permissions for specific user classes. Discuss the scenarios where adjusting these permissions would be necessary for security or collaboration.
7. Explain the difference between standard file permissions and Access Control Lists (ACLs) in Linux. Research and discuss what additional capabilities ACLs provide, such as setting permissions for individual users or groups beyond the owner, group, and others model.
8. Determine if a user who is not the owner of a file can change its permissions. Then, verify if a user who belongs to the file’s group can modify permissions. Use commands to test these scenarios and explain the results, discussing the limitations on who can alter file permissions.
9. Discuss scenarios where standard permissions are sufficient versus when ACLs are more appropriate for managing access to files and directories. Consider examples such as multi-user systems, shared directories, and files with sensitive information, and explain the benefits of using ACLs in specific cases.
10. Enable ACLs on a file by setting a custom permission for a user who is neither the file’s owner nor part of its group. Use `setfacl` to grant this user read-only access to the file, and then verify the change with `getfacl`. Explain how ACLs provide more granular control over file access and can accommodate complex permission requirements.
11. Explore the concept of the "sticky bit" on a shared directory, such as `/tmp`, by setting it on a new directory and testing its effects. Create a shared directory, set the sticky bit on it, and explain how it restricts users from deleting files they do not own. Discuss scenarios where the sticky bit is useful for multi-user collaboration.
