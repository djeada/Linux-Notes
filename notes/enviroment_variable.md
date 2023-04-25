## Variable Types

In Unix-like operating systems, variables store data. There are two types of variables in a shell: environment variables and shell variables.

## Environment Variables

Environment variables are set in the shell's environment and are available system-wide. Users typically don't set or change them. They store information like the current user's home directory, the system's hostname, and the directories in the $PATH variable.

To see all currently defined environment variables, use the printenv command.

```bash
printenv
```

### HISTSIZE

The `HISTSIZE` variable sets the maximum number of commands remembered in the command history. To see the current `HISTSIZE` value, use:

```bash
echo $HISTSIZE
```

### HOME

The `HOME` variable holds the current user's home directory, where personal files are stored. To see the current `HOME` value, use:

```bash
echo $HOME
```

### PWD

The `PWD` variable holds the current working directory, where the shell is working. To see the current working directory, use:

```bash
echo $PWD
```

### HOSTNAME

The `HOSTNAME` variable stores the hostname given to the system when it boots up. To display the current hostname, you can use the following command:

```bash
echo $HOSTNAME
```

### PATH

The `PATH` variable holds a colon-separated list of directories. When a user or script tries to run a command, the shell searches the `PATH` directories for a matching executable file. If found, it's executed; if not, an error message is shown. It's a good idea to set PATH to include program directories. To see the current `PATH` value, use:

```bash
echo $PATH
```

To add a directory to `PATH`, use:

```bash
PATH=$PATH:/path/to/bin
```

## Challenges

1. Make a bash script that echoes a message to stdout and ensure it has executable permission. Modify the `PATH` variable to include the script's directory. Test running the script from another location on the machine without using its absolute path.
2. Use the `USERNAME` variable to display a greeting message to the user.
3. List all currently set shell variables and exported shell variables.
4. In your terminal session, create a variable and set it to a number. Print the results of a few arithmetic operations to stdout using this variable.
5. Use the `export` command to set a new environment variable, then use the echo command to print that variable's value.
6. Use the `env` command to show all current environment variables, and use the `-i` flag to start a new shell with a clean environment.
