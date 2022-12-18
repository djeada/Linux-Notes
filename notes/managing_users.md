## Users

Users are individuals who have access to a system and are able to perform tasks and actions on it. In Linux, user information is stored in two main files: `/etc/passwd` and `/etc/shadow`.

* The `/etc/passwd` file stores basic information about each user, including the username, user ID (UID), group ID (GID), home directory path, and default shell. It is a public file, meaning that the password is stored in a hashed format that is not easily reversible.

* The `/etc/shadow` file stores more sensitive information about users, including the encrypted password, password expiration details, and password history. This file is only accessible to the root user and is not publicly readable.

To view the user information stored in these files, you can use the less command:

```
less /etc/passwd
less /etc/shadow
```

To display a list of all users on the system, you can use the following command:

```
awk -F: '{ print $1}' /etc/passwd | uniq
```

## Superuser

The superuser, also known as the root user, is a special user account with full access to all commands and files on the system, regardless of their permissions. The root user is typically used for system administration tasks and should be used with caution, as it has the greatest potential for causing damage to the system. The root user's login is usually root and a password is required to access the account.

It is important to choose a strong and secure password for the root user and to keep it confidential. It is also important to avoid using dangerous commands, such as `rm -rf /*`, which can delete all files in the root directory.

### Granting sudo privileges

To grant a user, the ability to execute commands with superuser privileges, you can use the `usermod` command. To add the user to the sudo group on Debian-based systems, use the following command (user name is adam in the example below):

```
usermod -aG sudo adam
```

On RedHat-based systems, the equivalent group is called `wheel`:

```
usermod -aG wheel adam
```

After adding the user to the appropriate group, you must also modify the `/etc/sudoers` file to allow members of the group to use sudo. To do this, you can use the `visudo` command to edit the file and uncomment the following line:

```
%wheel ALL=(ALL) ALL
```

### Partially granted sudo privileges

It is also possible to grant a user the ability to use sudo only for specific commands or tools. To do this, you can edit the `/etc/sudoers` file using the visudo command and add a line granting the user the desired privileges. For example, to allow the user adam to execute the reboot command without a password prompt, you can add the following line to the file:

```
adam ALL = NOPASSWD:/sbin/reboot
```

It is important to use the `visudo` command to edit the `/etc/sudoers` file, as it checks the file for syntax errors and prevents you from saving if any are found. A faulty `/etc/sudoers` file can prevent you from accessing your system ever again.

## Switching between users

To switch to another user account, you can use the su command. Without any arguments, `su` will launch the root user's subshell. To access another user's account, you can provide the username as an argument:

```
su adam
```

The `-c` option allows you to run a command as another user and display the output in your terminal:

```
su adam -c whoami
```

## Adding users

To add a new user to the system, you can use the useradd command. This command creates a new home directory for the user and adds the user's information to the `/etc/passwd` file.

```
useradd -m adam
```

The `-m` flag creates the home directory, and the `-u` flag allows you to specify a UID (it must be unique). The `-G` flag allows you to add the user to one or more groups.

Alternatively, you can use the `adduser` command, which is more user-friendly and prompts you for additional information, such as the password. However, `adduser` may not be available on all systems, so it is generally recommended to use `useradd` if you are writing a script that needs to be portable.

```
adduser adam
```

## Changing the password

To change a user's password, you can use the passwd command. When you run the command, you will be prompted to enter the new password.

```
passwd adam
```

You can also use the passwd command to set the password for a new user when you create their account using the useradd or adduser command. To do this, you can use the `-p` flag followed by the encrypted password.

```
useradd -m -p encrypted_password adam
```

It is important to choose strong and secure passwords to protect your system and user accounts.

## Group management

Groups are collections of users who are granted certain permissions or privileges on the system. Groups can be used to manage access to resources and simplify the process of granting or revoking privileges for multiple users at once.

To view the groups on the system, you can use the cat command to display the contents of the `/etc/group` file:

```
cat /etc/group
```

To add a new group, you can use the `groupadd` command:

```
groupadd admins
```

To add a user to a group, you can use the `usermod` command with the `-aG` flag, followed by the group name:

```
usermod -aG admins adam
```

To remove a user from a group, you can use the `gpasswd` command with the `-d` flag, followed by the username:

```
gpasswd -d adam admins
```

### Changing the user and group ownership of a file

To change the owner of a file or directory, you can use the `chown` command, followed by the username and the file or directory name:

```
chown adam file.txt
```

To change the group ownership of a file or directory, you can use the `chgrp` command, followed by the group name and the file or directory name:

```
chgrp admins file.txt
```

You can also use the `chown` command to change both the owner and group ownership of a file or directory at the same time by specifying both the username and group name separated by a colon:

```
chown adam:admins file.txt
```

## User ID and Group ID

In a Unix system, every user and group is assigned a unique identifier known as a user ID (UID) or group ID (GID), respectively. These identifiers are used to identify and differentiate users and groups on the system.

The `/etc/passwd` file stores the UIDs for each user, while the /etc/group file stores the GIDs for each group. When a user creates a file or directory, the system sets the ownership of the file to the user's UID and the user's default group's GID.

The UID and GID can be used to set permissions on files and directories, allowing or restricting access to certain users or groups. For example, you can use the chown command to change the ownership of a file to a specific UID and GID, and the chmod command to set permissions for the owner, group, and other users based on their UIDs and GIDs.

It is important to carefully manage UIDs and GIDs to ensure the security and integrity of your system. The root user, which has the UID 0 and the GID 0, has special privileges and can perform actions that other users may not be able to.

To check a user's UID, you can use the `id` command followed by the username:

```
id adam
```

This will display output similar to the following:

```
uid=1000(adam) gid=1000(adam) groups=1000(adam),4(adm),24(cdrom),27(sudo),46(plugdev),113(lpadmin),128(sambashare)
```

The uid field indicates the user's UID, and the gid field indicates the user's primary group's GID. The groups field lists the GIDs of all groups that the user belongs to.

To check a group's GID, you can use the `getent` command followed by the group name:

```
getent group admins
```

This will display output similar to the following:

```
admins:x:1001:adam
```

The second field, x, indicates that the group's password is stored in the `/etc/shadow` file. The third field indicates the group's GID, and the fourth field lists the names of all users who belong to the group.

To change a user's UID, you can use the usermod command with the `-u` flag followed by the desired UID and the username:

```
usermod -u 1001 adam
```

To change a group's GID, you can use the groupmod command with the `-g` flag followed by the desired GID and the group name:

```
groupmod -g 1001 admins
```

## Challenges 

1. Display your username and unique user identity number (UID).
1. Explain the purpose of the root user.
1. Provide instructions for logging in as root using the terminal.
1. View the contents of the `/etc/shadow` file with the necessary privileges. Can you locate a reference to your user in this file?
1. Consult the `/var/log/auth.log` file to check for currently logged-in users. Use grep to determine if anyone has used sudo.
1. Generate a list of logged-in users, sorted alphabetically, including the command they are currently executing.
1. Create a group called "friends" and include your user in it. Then, create two additional users and add them to the group as well. Verify that the new accounts have been set up correctly. Create a directory with read and write permissions for all members of the friends group. Create a few text files in this directory and test if they can be accessed and modified by all group members. Finally, delete the additional users you created.
1. Allow a user without sudo privileges to execute the reboot command. Log in to that user account and confirm that the system can be restarted.
1. Describe the difference between locking and disabling a user account's password. Explain the consequences of using the commands `usermod -L` and `passwd -d`.
