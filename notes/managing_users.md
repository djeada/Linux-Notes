## Users

Users can use a system and do tasks. In Linux, user info is in two main files: `/etc/passwd` and `/etc/shadow`.

* `/etc/passwd` has basic info about each user, like username, user ID (UID), group ID (GID), home folder, and default shell. It's a public file with the password in a hard-to-reverse format.

* `/etc/shadow` has sensitive info about users, like encrypted password, password expiration, and password history. Only the root user can access this file.

To see the user info in these files, use the less command:

```
less /etc/passwd
less /etc/shadow
```

To show all users on the system, use this command:

```
awk -F: '{ print $1}' /etc/passwd | uniq
```

## Superuser

The superuser, or root user, is a special user with full access to all commands and files on the system, no matter their permissions. The root user is usually for system administration tasks and should be used carefully. The root user's login is usually root, and a password is needed to access the account.

Choose a strong password for the root user, keep it secret, and avoid using dangerous commands like `rm -rf /*`, which can delete all files in the root folder.

### Granting sudo privileges

To let a user do commands with superuser privileges, use the `usermod` command. To add the user to the sudo group on Debian-based systems, use this command (user name is adam in the example):

```
usermod -aG sudo adam
```

On RedHat-based systems, the similar group is called `wheel`:

```
usermod -aG wheel adam
```

After adding the user to the right group, also change the `/etc/sudoers` file to let the group use sudo. Use the `visudo` command to edit the file and uncomment this line:

```
%wheel ALL=(ALL) ALL
```

### Partially granted sudo privileges

You can also let a user use sudo only for certain commands or tools. Edit the `/etc/sudoers` file with the visudo command and add a line giving the user the right privileges. For example, to let the user adam do the reboot command without a password prompt, add this line to the file:

```
adam ALL = NOPASSWD:/sbin/reboot
```

Use the `visudo` command to edit the `/etc/sudoers` file, as it checks for mistakes and stops you from saving if there are any. A bad `/etc/sudoers` file can stop you from ever using your system again.

## Switching between users

To switch to another user account, use the su command. Without any arguments, `su` will start the root user's subshell. To access another user's account, give the username as an argument:

```
su adam
```

The `-c` option lets you run a command as another user and show the output in your terminal:

```
su adam -c whoami
```

## Adding users

To add a new user to the system, use the useradd command. This command makes a new home folder for the user and adds the user's info to the `/etc/passwd` file.

```
useradd -m adam
```


The `-m` flag makes the home folder, and the `-u` flag lets you choose a UID (it must be unique). The `-G` flag lets you add the user to one or more groups.

You can also use the `adduser` command, which is easier to use and asks you for more info, like the password. But `adduser` might not be on all systems, so it's better to use `useradd` if you're that needs to work on different systems.

```
adduser adam
```

## Changing the password

To change a user's password, use the passwd command. When you run the command, you'll be asked to enter the new password.

```
passwd adam
```

You can also use the passwd command to set the password for a new user when you create their account using the useradd or adduser command. To do this, use the `-p` flag followed by the encrypted password.

```
useradd -m -p encrypted_password adam
```

Choose strong and safe passwords to protect your system and user accounts.

## Group management

Groups are sets of users with certain permissions or privileges on the system. Groups help manage access to resources and make it easier to give or take away privileges for multiple users at once.

To see the groups on the system, use the cat command to show the contents of the `/etc/group` file:

```
cat /etc/group
```

To add a new group, use the `groupadd` command:

```
groupadd admins
```

To add a user to a group, use the `usermod` command with the `-aG` flag, followed by the group name:

```
usermod -aG admins adam
```

To remove a user from a group, use the `gpasswd` command with the `-d` flag, followed by the username:

```
gpasswd -d adam admins
```

### Changing the user and group ownership of a file

To change the owner of a file or folder, use the `chown` command, followed by the username and the file or folder name:

```
chown adam file.txt
```

To change the group ownership of a file or folder, use the `chgrp` command, followed by the group name and the file or folder name

```
chgrp admins file.txt
```

You can also use the `chown` command to change both the owner and group ownership of a file or folder at the same time by specifying both the username and group name separated by a colon:

```
chown adam:admins file.txt
```

## User ID and Group ID

In a Unix system, every user and group has a unique ID called a user ID (UID) or group ID (GID). These IDs are used to tell users and groups apart on the system.

The `/etc/passwd` file has the UIDs for each user, while the /etc/group file has the GIDs for each group. When a user makes a file or folder, the system sets the ownership of the file to the user's UID and the user's main group's GID.

The UID and GID can be used to set permissions on files and folders, allowing or blocking access to certain users or groups. For example, you can use the chown command to change the ownership of a file to a specific UID and GID, and the chmod command to set permissions for the owner, group, and other users based on their UIDs and GIDs.

Manage UIDs and GIDs carefully to keep your system safe and working well. The root user, which has the UID 0 and the GID 0, has special privileges and can do things other users can't.

To check a user's UID, use the `id` command followed by the username:

```
id adam
```

This will show output like this:

```
uid=1000(adam) gid=1000(adam) groups=1000(adam),4(adm),24(cdrom),27(sudo),46(plugdev),113(lpadmin),128(sambashare)
```

The uid field shows the user field shows the user's UID, and the gid field shows the user's main group's GID. The groups field lists the GIDs of the user belongs to.

To check a group's GID, use the `getent` command followed by the group name:

```
getent group admins
```

This will show output like this:

```
admins:x:1001:adam
```

The second field, x, means the group's password is stored in the `/etc/shadow` file. The third field shows the group's GID, and the fourth field lists the names of all users in the group.

To change a user's UID, use the usermod command with the `-u` flag followed by the new UID and the username:

```
usermod -u 1001 adam
```

To change a group's GID, use the groupmod command with the `-g` flag followed by the new GID and the group name:

```
groupmod -g 1001 admins
```

## Challenges 

1. Show your username and unique user ID (UID).
2. Explain the purpose of the root user.
3. Give instructions for logging in as root using the terminal.
4. View the `/etc/shadow` file with the right privileges. Can you find a reference to your user in this file?
5. Check the `/var/log/auth.log` file to see which users are currently logged in. Use grep to find if anyone has used sudo.
6. Make a list of logged-in users, sorted alphabetically, including the command they are currently running.
7. Create a group called "friends" and include your user in it. Then, create two more users and add them to the group too. Check that the new accounts are set up right. Create a folder with read and write permissions for all members of the friends group. Create a few text files in this folder and test if they can be accessed and changed by all group members. Finally, delete the extra users you created.
8. Allow a user without sudo privileges to run the reboot command. Log in to that user account and check that the system can be restarted.
9. Describe the difference between locking and disabling a user account's password. Explain what happens when you use the commands `usermod -L` and `passwd -d`.
