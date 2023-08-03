## Variable Types in Unix-like Operating Systems

In Unix-like operating systems, variables are used to store and manipulate data. Within a shell environment, there are two primary types of variables: environment variables and shell variables.

## Environment Variables

Environment variables are global parameters recognized by the system and its applications, set in the shell's environment. These variables are typically initialized at system startup and remain constant throughout a session, providing necessary information to the operating system and software applications. Users generally do not need to set or change them manually.

You can view all currently defined environment variables by using the `printenv` command:

```bash
printenv
```

Here are some commonly used environment variables:

### HISTSIZE

The HISTSIZE variable determines the maximum number of commands that the shell remembers in the command history. This allows you to navigate and execute previously entered commands. To display the current HISTSIZE value, execute:

```bash
echo $HISTSIZE
```

### HOME

The HOME variable holds the file path of the current user's home directory, which typically contains user-specific files and directories. To display the current HOME value, execute:

```bash
echo $HOME
```

### PWD

The PWD (Present Working Directory) variable holds the file path of the directory that the shell is currently operating in. To display your current working directory, execute:

```bash
echo $PWD
```

### HOSTNAME

The HOSTNAME variable contains the name assigned to the system at startup. This name is used by the network and other services to identify the system. To display the current hostname, execute:

```bash
echo $HOSTNAME
```

### PATH

The PATH variable holds a colon-separated list of directories that the shell checks when trying to execute a command. When a user or a script tries to execute a command without specifying a full file path, the shell scans the directories listed in PATH for a matching executable file. If found, it's executed; otherwise, an error message is displayed.

To display the current PATH value, execute:

```bash
echo $PATH
```

You can add a directory to the PATH variable using the following syntax, which appends :/path/to/bin to the existing PATH:

```bash
PATH=$PATH:/path/to/bin
```

This ensures that the shell can find and execute programs stored in /path/to/bin, enhancing the flexibility and functionality of your Unix-like environment.

## Challenges

1. Write a Bash script named `greetings.sh` that prints a welcome message to the standard output. Ensure that it has executable permissions. Modify the `PATH` environment variable to include the directory of your script. Test if you can execute the script from a different directory without specifying its absolute path.
2. Use the `USER` environment variable in a command to print a personalized greeting message, such as "Hello, $USER! Welcome back!".
3. Use a command to list all shell and environment variables that are currently set in your shell.
4. Create a variable in your terminal session, set it to a number, and print the results of a few arithmetic operations on this variable to the standard output.
5. Use the `export` command to create a new environment variable. Print the value of this variable to the standard output using the `echo` command.
6. Use the `env` command to display all current environment variables. Then, start a new shell with a clean environment using the `-i` option with the `env` command.
7. Write a shell script that increments a number stored in a variable each time the script is run. Store this number in an environment variable to make it persistent across separate script executions.
8. Use the `PATH` variable to find an executable file in your system. Try adding a new directory to the `PATH` and confirm that you can execute commands from this directory without specifying the full path.
