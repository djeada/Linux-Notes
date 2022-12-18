## Type variables

In a Unix-like operating system, variables are used to store data. There are two types of variables in a shell: environment variables and shell variables.

## Environment Variables

Environment variables are set in the environment of the shell and are available system-wide. They are usually not set or changed by the user and are used to store information such as the current user's home directory, the hostname of the system, and the directories included in the $PATH variable. 

To view all of the environment variables that are currently defined, you can use the printenv command.

```bash
printenv
```

### HISTSIZE

The `HISTSIZE` variable determines the maximum number of commands that can be remembered in the command history. To display the current value of `HISTSIZE`, you can use the following command:

```bash
echo $HISTSIZE
```

### HOME

The `HOME` variable stores the current user's home directory. This is the directory where the user's personal files are stored. To display the current value of `HOME`, you can use the following command:

```bash
echo $HOME
```

### PWD

The `PWD` variable stores the current working directory. This is the directory where the shell is currently working. To display the current working directory, you can use the following command:

```bash
echo $PWD
```

### HOSTNAME

The `HOSTNAME` variable stores the hostname given to the system when it boots up. To display the current hostname, you can use the following command:

```bash
echo $HOSTNAME
```

### PATH

The `PATH` variable stores a colon-separated list of directories. When a user or script attempts to run a command, the shell searches the directories in `PATH` for a matching file with executable permission. If the file is found, it is executed. If the file is not found, the shell prints an error message. It is a good idea to set $PATH to include the directories where your programs are installed. To display the current value of `PATH`, you can use the following command:

```bash
echo $PATH
```

To append a directory to `PATH`, you can use the following command:

```bash
PATH=$PATH:/path/to/bin
```

## Challenges

1. Create a bash script that echoes a message to the standard output and ensure it has executable permission. Modify the `PATH` variable to include the directory where the script is located. Test running the script from another location on the machine without using its absolute path.
1. Use the `USERNAME` variable to display a greeting message to the user.
1. List all currently set shell variables and exported shell variables.
1. In your terminal session, create a variable and try setting it to a number. Print the results of a few arithmetic operations to stdout using this variable.
1. Use the `export` command to set a new environment variable, then use the echo command to print the value of that variable.
1. Use the `env` command to display all of the current environment variables, and use the `-i` flag to start a new shell with a clean environment.
