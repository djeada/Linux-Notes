<h2>superuser</h2>
The superuser is a privileged user with full access to all commands and files on a system, regardless of their permissions. Typically, the superuser's login is root. A password is required to access the root account (the root password). Because the root account has the greatest potential for damage, the root password should be carefully crafted and only supplied to those who require it.

!Don't use:

```bash
rm –rf /*
```

<h2>adding user</h2>

<i>useradd</i> is a UNIX system tool for adding new users. It generates a new home directory for the user and adds new user information to the /etc/passwd file.

```bash
useradd adam
```

<h2>passwd</h2>
Use the <i>passwd</i> command to set or modify a user's password:

```bash
passwd adam
```

* Why is the passwd command able to modify the /etc/passwd file?
- It has the SUID permission mode and is owned by root.

* Why doesn't passwd -l keep a user from logging in via other methods?
- It locks only the password, not the account, so users can still authenticate with keys or other methods.
 
<h2>bashrc</h2>

The <i>\~/.bash_profile</i> file would only be utilized once, at login. Every time a shell is started, the  <i>\~/.bashrc</i> script is read. This is similar to  <i>\~/.cshrc</i>  in C Shell.

The script is designed to be lightweight, with just the most important commands being run.

<h2>Groups</h2>

<i>groupadd</i> creates a new group and saves its details to /etc/group:

```bash
groupadd new_group
```

The command <i>group</i> displays which groups a user is a member of:

```bash
groups username
```

Add the existing user adam to new_group:

```bash
usermod -a -G new_group adam 
```

Change the primary group of adam to new_group:

```bash
usermod -g new_group adam 
```

<h2>User ID</h2>

Each user has a distinct user id (uid). To check a user's id, use:

```bash
id user_name
```

To change UID of user <i>adam</i> to 1100, use:

```bash
usermod -u 1100 adam
```

To change GID of a group called <i>new_group</i> to 2500, use:

```bash
groupmod -g 2500 new_group
```
