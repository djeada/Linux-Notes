<h2>Environment variables</h2>

Environment variables are variables that the shell uses and shares.
$PATH, for example, informs the system where to look for commands.

Environment variables are shared by programs launched by the shell.

Use printenv to examine all of the environment variables that are presently defined.

```bash
printenv
```

<h2>$HISTSIZE</h2>

The maximum number of commands that can be remembered.

```bash
echo $HISTSIZE
```

<h2>$HOME</h2>

The current user's home directory.

```bash
echo $HOME
```

<h2>$PWD</h2>

Print working directory. You are now in the following working directory:

```bash
echo $PWD
```

<h2>$RANDOM</h2>

An integer between 0 and 32767 is chosen at random.

```bash
echo $RANDOM
```

<h2>$HOSTNAME</h2>

The hostname given to the system when it boots up.

```bash
echo $HOSTNAME
```

<h2>$PATH</h2>

When a user or script attempts to run a command, it searches the paths in $PATH for a matching file with execute permission.

```bash
echo $PATH
```

Global paths should be set in /etc/profile or /etc/environment:

```bash
PATH=$PATH:/path/to/bin
```
