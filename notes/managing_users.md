<h2>superuser</h2>
The superuser is a privileged user with full access to all commands and files on a system, regardless of their permissions. There is no such thing a superuser without the access rights. Typically, the superuser's login is root. A password is required to access the root account (the root password). Because the root account has the greatest potential for damage, the root password should be carefully crafted and only supplied to those who require it.

!Keep in mind that the following command should not be used:

```bash
rm –rf /*
```

<h2>changing users</h2>
<i>su</i> without any arguments will launch the root user's subshell. If you want to access another user's account, you have to provide their username.

```bash
su adam
```

The -c option enables you to run a command as another user account and redirect the output to your terminal:

```bash
su adam -c whoami
```

<h2>adding user</h2>

<i>useradd</i> is a UNIX system tool for adding new users. It generates a new home directory for the user and adds new user information to the /etc/passwd file.

```bash
useradd adam
```

Flags:
* <i>-m</i> create home dir. The template is located at /etc/skel.
* <i>-u</i> specify UID (it has to be free).
* <i>-G</i> add the user to the following groups.

<h2>passwd</h2>
Use the <i>passwd</i> command to set or modify a user's password:

```bash
passwd adam
```

* <i>passwd -l</i>  blocks user from chaning their password (-u flags unlocks). Why doesn't it keep a user from logging in via other methods?
- It locks only the password, not the account, so users can still authenticate with keys or other methods.
 
Columns of /etc/passwd:

* username
* password
* UID
* GID
* comment (GECOS filed)
* home dir path
* shell (e.g. /bin/bash)

Columns of /etc/shadow

* username
* encrypted password
* number of days since last password change
* number of days before password can be changed again (e.g. 0)
* number of days before password must be changed
* warning period
* inactivity period
* expiration date
* unused
 
<h2>bashrc</h2>

The <i>\~/.bash_profile</i> file would only be utilized once, at login. Every time a shell is started, the  <i>\~/.bashrc</i> script is read. This is similar to  <i>\~/.cshrc</i>  in C Shell.

The script is designed to be lightweight, with just the most important commands being run.

<h2>Groups</h2>

All new users in RHEL/CENTOS are automatically added to the wheel group.

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

Columns of /etc/group

* group name
* password
* group id
* members

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
