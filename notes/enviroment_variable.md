<h1>Type of shell variables</h1>

* <i>Environment variables</i> are variables that are set in the environment of the shell.
They are available system wide and usually not set and changed by the user.
* <i>Shell variables</i> are variables that are set by the user.
They are available to the shell and the programs that are run in the shell.

Use printenv to display all of the environment variables that are presently defined.

```bash
printenv
```

<h1>Common environment variables</h1>

There are a number of common environment variables that are used by the shell.

<h2>$HISTSIZE</h2>

The maximum number of commands that can be remembered.

```bash
echo $HISTSIZE
```

<h2>$HOME</h2>

The current user's home directory. This is the directory where the user's personal files are stored. 

```bash
echo $HOME
```

<h2>$PWD</h2>

Print the working directory. This is the directory where the shell is currently working. 

```bash
echo $PWD
```

<h2>$HOSTNAME</h2>

The hostname given to the system when it boots up.

```bash
echo $HOSTNAME
```

<h2>$PATH</h2>

It stores a colon-separated list of directories. When a user or script attempts to run a command, it searches the paths in $PATH 
for a matching file with executable permission. If the file is found, it is executed. If the file is not found, the shell prints an error message.
It is a good idea to set $PATH to include the directories where your programs are installed. 

```bash
echo $PATH
```

To append a directory to <code>$PATH</code>, use the following command:

```bash
PATH=$PATH:/path/to/bin
```

<h1>Challenges</h1>

1. Create a bash script that echoes a message to the standard output. Give the script executable permission. Change the <code>$PATH</code> variable to include the directory where the script is located.
