## Variable Types

In Unix-like operating systems, variables play a crucial role in the functionality of the shell, acting as containers to store data, configuration settings, and system information. There are primarily two types of variables in a shell environment: environment variables and shell variables.

## Environment Variables

Environment variables are key-value pairs recognized globally across the system and its applications, set within the shell's environment. They are usually initialized at system startup, and their values remain consistent throughout the session. These variables provide essential configuration and operational data to the operating system and the software applications running on it. While users typically do not modify these variables frequently, understanding and occasionally altering them can be crucial for advanced system management and troubleshooting.

To view all currently defined environment variables, use the `printenv` command:

```bash
printenv
```

Here are some commonly used environment variables:

### HISTSIZE

Determines the maximum number of commands stored in the shell's command history. This feature is useful for recalling and executing previous commands. View its value with:

```bash
echo $HISTSIZE
```

### HOME

Specifies the path to the current user's home directory, a central location for user-specific files and configurations. Check its value using:

```bash
echo $HOME
```

### PWD

PWD (Present Working Directory): Contains the path of the current directory that the shell is operating in. Display your current directory with:

```bash
echo $PWD
```

### HOSTNAME

Stores the system's network name, used for identification over a network. To see the current hostname:

```bash
echo $HOSTNAME
```

### PATH

A colon-separated list of directories where the shell looks for executable files. When a command is issued, the shell searches these directories in order to find and execute the command. View the current PATH with:

```bash
echo $PATH
```

Append a new directory to PATH using the following syntax, which adds `/path/to/bin` to the existing PATH:

```bash
PATH=$PATH:/path/to/bin
```

This modification enables the shell to locate and execute programs stored in `/path/to/bin`, increasing the versatility of the Unix-like environment.

## Shell Variables

Shell variables are local to the shell instance and are used to store temporary data and control shell functions. Unlike environment variables, shell variables are not inherited by child processes and are typically used to manage internal shell settings or hold temporary values for scripts and commands.

Examples include:

- **PS1**: Defines the shell prompt appearance.
- **IFS (Internal Field Separator)**: Determines how the shell recognizes word boundaries.

To create or modify a shell variable, simply assign a value to a name:

```bash
myvar="Hello, World!"
```

To view the value stored in a shell variable, use the echo command:

```bash
echo $myvar
```

Understanding and effectively managing these variables is key to harnessing the full power of Unix-like operating systems, allowing for customized and optimized user experiences.

## Challenges

I. Create and Execute a Script `greetings.sh`

- Write a Bash script named `greetings.sh` that prints a welcome message.
- Ensure it has executable permissions (`chmod +x greetings.sh`).
- Modify the `PATH` environment variable to include the script's directory (`export PATH=$PATH:/path/to/script`).
- Test executing the script from a different directory without its absolute path.

II. Write a command or script using the `USER` environment variable to print a personalized message like "Hello, $USER! Welcome back!".

III. Use a command to display all currently set shell and environment variables (e.g., `set` or `env`).

IV. Arithmetic Operations with a Shell Variable

- Create a variable in your terminal session and assign a numeric value to it.
- Perform and print a few arithmetic operations on this variable.

V. Create and Display a New Environment Variable

- Use the `export` command to create a new environment variable.
- Print its value using `echo`.

VI. Display Environment Variables and Start a Clean Shell

- Use `env` to display all current environment variables.
- Start a new shell with a clean environment using `env -i`.

VII. Increment a Number in a Script with Environment Variable

- Write a shell script that increments a number stored in a variable each time it is run.
- Store this number in an environment variable for persistence across executions.

VIII. Find and Execute Files Using `PATH`

- Use the `PATH` variable to locate an executable file on your system.
- Add a new directory to the `PATH` (`export PATH=$PATH:/new/directory`).
- Test executing a command from this new directory without its full path.
