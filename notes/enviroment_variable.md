## Variable Types

In Unix-like operating systems, variables play a crucial role in the functionality of the shell, acting as containers to store data, configuration settings, and system information. There are primarily two types of variables in a shell environment: environment variables and shell variables.

### Environment Variables

Environment variables are key-value pairs that are recognized globally across the operating system and its applications. These variables are set within the shell's environment, typically initialized at system startup, and maintain their values throughout the session. They provide essential configuration and operational data to both the operating system and the software applications running on it. Although users typically do not modify these variables frequently, understanding and occasionally altering them can be crucial for advanced system management and troubleshooting.

To view all currently defined environment variables, use the `printenv` command:

```bash
printenv
```

Here are some commonly used environment variables:

#### HISTSIZE

The `HISTSIZE` variable determines the maximum number of commands stored in the shell's command history. This is particularly useful for recalling and executing previous commands without retyping them. You can view its value with the following command:

```bash
echo $HISTSIZE
```

For example, if `HISTSIZE` is set to 1000, the shell will keep a history of the last 1000 commands entered.

#### HOME

The `HOME` variable specifies the path to the current user's home directory. This directory serves as a central location for user-specific files and configurations, providing a personal workspace for each user. To check its value, use:

```bash
echo $HOME
```

For instance, if the output is `/home/username`, this directory is where personal files and user-specific configuration files are stored.

#### PWD

`PWD` stands for Present Working Directory. It contains the path of the current directory in which the shell is operating. Display your current directory with:

```bash
echo $PWD
```

This is particularly useful in scripts or command-line operations to dynamically understand and manage the current location in the filesystem.

#### HOSTNAME

The `HOSTNAME` variable stores the system's network name, used for identification over a network. To see the current hostname, you can use:

```bash
echo $HOSTNAME
```

This can be useful for network-related scripts or configurations where the hostname is needed for logging or identification purposes.

#### PATH

The `PATH` variable is a colon-separated list of directories that the shell searches for executable files. When a command is issued, the shell checks these directories in order to find and execute the command. You can view the current `PATH` with:

```bash
echo $PATH
```

To append a new directory to the `PATH`, enabling the shell to locate and execute programs stored in that directory, use the following syntax. This example adds `/path/to/bin` to the existing `PATH`:

```bash
PATH=$PATH:/path/to/bin
```

This modification allows the system to find executables in `/path/to/bin`, enhancing the flexibility and functionality of the Unix-like environment.

### Modifying Environment Variables

While some environment variables are set at startup and rarely changed, others may need modification for specific tasks or configurations. Modifying these variables can be done temporarily for the current session or permanently by adding the changes to shell configuration files like `~/.bashrc` or `~/.profile`.

#### Temporary Modification

To temporarily change an environment variable, you can simply assign a new value in the current shell session. For example:

```bash
export PATH=$PATH:/new/directory
```

This change will persist only for the duration of the session or until the terminal window is closed.

#### Permanent Modification

For a permanent change, add the export statement to a shell configuration file. For instance, to permanently add a directory to the `PATH`, you can add the following line to `~/.bashrc`:

```bash
echo 'export PATH=$PATH:/new/directory' >> ~/.bashrc
```

After editing `~/.bashrc`, reload the file to apply the changes:

```bash
source ~/.bashrc
```

#### Importance and Use

Environment variables play a critical role in the configuration and behavior of the operating system and applications. By managing these variables, users and administrators can customize the environment, control software behavior, and troubleshoot issues more effectively. Understanding how to use and modify these variables is an essential skill for anyone working with Unix-like operating systems.

### Shell Variables

Shell variables are essential components of shell scripting and command-line operations, primarily used to store temporary data and control the behavior of the shell. Unlike environment variables, shell variables are confined to the shell instance in which they are defined and are not passed to child processes. They are particularly useful for managing internal shell settings, holding temporary values, and facilitating script automation.

#### Key Shell Variables

Here are a few examples of commonly used shell variables:

- `PS1` variable defines the appearance of the shell prompt. By customizing `PS1`, users can modify how the prompt looks, including information such as the current directory, username, hostname, or special characters.

  ```bash
  PS1="\u@\h:\w\$ "
  ```
  This example sets the prompt to display the username (`\u`), hostname (`\h`), and the current working directory (`\w`), followed by a dollar sign (`$`).

- The `IFS` variable determines how the shell recognizes word boundaries, primarily affecting how it splits strings into words. By default, `IFS` includes a space, tab, and newline, meaning these characters are used to separate words.

  ```bash
  IFS=','
  ```
  Setting `IFS` to a comma means that word splitting will occur at commas instead of spaces.

#### Creating and Modifying Shell Variables

To create or modify a shell variable, you simply assign a value to a variable name without any spaces around the `=` sign:

```bash
myvar="Hello, World!"
```

In this example, `myvar` is a shell variable assigned the string "Hello, World!". Unlike environment variables, you do not need to use the `export` command unless you intend for the variable to be accessible in subprocesses.

#### Accessing Shell Variables

To retrieve the value stored in a shell variable, you precede the variable name with a dollar sign (`$`). You can use the `echo` command to display its value:

```bash
echo $myvar
```

This command will output:

```
Hello, World!
```

#### Scope and Limitations

- Shell variables are local to the shell session in which they are defined. They are not inherited by child processes, making them useful for controlling the behavior of scripts and commands without affecting other running processes.
- Shell variables are ideal for storing temporary data such as loop counters, command outputs, or intermediate results within scripts.
- By using shell variables, you can customize the shell environment, automate tasks, and manage configuration settings dynamically.

### Challenges

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
