//TODO:
* /etc/sudoers
* visudo

## Users
### Superuser
The superuser is a privileged user with full access to all commands and files on a system, regardless of their permissions. There is no such thing a superuser without the access rights. Typically, the superuser's login is root. A password is required to access the root account. Because the root account has the greatest potential for damage, the root password should be carefully chosen and kept in secret.

!Keep in mind that the following command should not be used:

```bash
rm –rf /*
```

### Partially granted sudo privileges 

/etc/sudoers is a special file that allows users to be granted sudo privileges solely for specific tools.

If you wish to provide Adam the ability to reboot, run <i>visudo /etc/sudoers</i> and add the following lines at the bottom of the file: 

```bash
# Allow user "adam" to run "sudo reboot"
# ...and don't prompt for a password
#
adam ALL = NOPASSWD:/sbin/reboot
```

The visudo command will automatically verify your syntax and refuse to save if there are any errors. A faulty /etc/sudoers file may prevent you from accessing your server every again!

### Changing users
<i>su</i> without any arguments will launch the root user's subshell. If you want to access another user's account, you have to provide their username.

```bash
su adam
```

The -c option enables you to run a command as another user account and redirect the output to your terminal:

```bash
su adam -c whoami
```

### Adding user

<i>useradd</i> is a UNIX system tool for adding new users (<i>userdel</i> is its counterpart for deleting users). It generates a new home directory for the user and adds new user information to the /etc/passwd file.

```bash
useradd -m adam
```

Flags:
* <i>-m</i> create home dir. The template is located at /etc/skel.
* <i>-u</i> specify UID (it has to be free).
* <i>-G</i> add the user to the following groups.

When adding new users from the command line, you should prefer using <i>adduser</i> (and <i>deluser</i> when deleting users). If you're developing a script, especially if portability is important, you might want to use the lowlevel utilities instead - because adduser/deluser may not be accessible on all distributions, such as SuSE.

```bash
adduser adam
```

### passwd
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
 
## Groups

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

To list all local groups on the system, use:

```bash
cut -d: -f1 /etc/group | sort
```

### User ID and group ID

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

## Challenges

1. Show your user name as well as your unique user identity number (userid).
1. Show the contents of the /etc/shadow. Can you find a reference to your user? Hint: you will need sudo privileges.
1. Check the /var/log/auth.log file to check who is logged in. Use <i>grep</i> to see if someone is using sudo.
1. Display a sorted list of all logged-in users, including the command they are now executing. 
1. Create a group called "friends." Include your user in the newly formed group. Create two additional users and add them to the same group. Check the newly created accounts to see whether everything is in order. Create a directory with read and write permissions for all members of the friends group. Create a few text files in this directory and test if they can be seen and edited by all users. Delete all new users you've made.
1. Allow a user with no sudo privileges to execute the <code>reboot</code> command. Log in to that specific user account. Verify whether the system can be restarted.
1. Create a user with a program set as his default logon shell. You might, for example, use /bin/tar. It's useful when a user should only be able to access one program on the server. 
1. What's the difference between locking and disabling a user account's password? What are the consequences of using the commands <code>usermod -L</code> and <code>passwd -d</code>? 
