#### Q. What is the default shell on most Linux distributions?

* [ ] zsh
* [x] bash
* [ ] sh
* [ ] ksh
* [ ] tcsh

#### Q. What does "bash" stand for?

* [ ] Basic Shell
* [x] Bourne-Again Shell
* [ ] Batch Shell
* [ ] Binary Shell
* [ ] Best Available Shell

#### Q. Which file lists all valid login shells on a Linux system?

* [ ] `/etc/passwd`
* [x] `/etc/shells`
* [ ] `/etc/shell.conf`
* [ ] `/etc/bash.bashrc`
* [ ] `/etc/login.defs`

#### Q. Which command displays your current shell?

* [ ] `echo $PATH`
* [x] `echo $SHELL`
* [ ] `which shell`
* [ ] `shell --version`
* [ ] `ps shell`

#### Q. Which command permanently changes your default login shell?

* [ ] `shell`
* [x] `chsh`
* [ ] `setshell`
* [ ] `usermod -shell`
* [ ] `newshell`

#### Q. Which configuration file is executed for interactive non-login bash shells?

* [ ] `~/.bash_profile`
* [x] `~/.bashrc`
* [ ] `~/.profile`
* [ ] `~/.bash_login`
* [ ] `/etc/profile`

#### Q. Which configuration file is executed for login shells?

* [ ] `~/.bashrc`
* [x] `~/.bash_profile`
* [ ] `~/.bash_logout`
* [ ] `/etc/bashrc`
* [ ] `~/.inputrc`

#### Q. What is executed when a login shell exits?

* [ ] `~/.bashrc`
* [ ] `~/.bash_profile`
* [x] `~/.bash_logout`
* [ ] `/etc/profile`
* [ ] `~/.profile`

#### Q. Which variable holds the current user's home directory?

* [ ] `$PATH`
* [ ] `$USER`
* [x] `$HOME`
* [ ] `$PWD`
* [ ] `$SHELL`

#### Q. Which command creates an alias in bash?

* [ ] `set ll='ls -la'`
* [x] `alias ll='ls -la'`
* [ ] `define ll='ls -la'`
* [ ] `shortcut ll='ls -la'`
* [ ] `bind ll='ls -la'`

#### Q. Which command displays all currently defined aliases?

* [ ] `list alias`
* [x] `alias`
* [ ] `show aliases`
* [ ] `echo $ALIAS`
* [ ] `aliases --list`

#### Q. What does the `export` command do?

* [ ] Deletes a variable
* [x] Makes a variable available to child processes
* [ ] Imports a variable from another shell
* [ ] Saves a variable to a file
* [ ] Prints a variable value

#### Q. Which variable contains the directories searched for executable programs?

* [x] `$PATH`
* [ ] `$HOME`
* [ ] `$BIN`
* [ ] `$EXEC`
* [ ] `$PROGRAMS`

#### Q. What is the purpose of the `source` command?

* [ ] Downloads a file
* [x] Executes commands from a file in the current shell
* [ ] Creates a backup copy
* [ ] Compiles a script
* [ ] Displays file source code

#### Q. Which symbol is used for single-line comments in bash scripts?

* [ ] `//`
* [x] `#`
* [ ] `--`
* [ ] `/* */`
* [ ] `;`

#### Q. What does the `$?` variable contain?

* [ ] Current process ID
* [x] Exit status of the last command
* [ ] Number of arguments
* [ ] Current shell name
* [ ] Last background job PID

#### Q. What does `$0` represent in a bash script?

* [x] The name of the script
* [ ] The first argument
* [ ] The exit status
* [ ] The process ID
* [ ] The number of arguments

#### Q. Which variable holds the number of positional parameters passed to a script?

* [ ] `$@`
* [ ] `$*`
* [x] `$#`
* [ ] `$0`
* [ ] `$?`

#### Q. What does `$@` represent in a bash script?

* [ ] The script name
* [ ] The number of arguments
* [x] All positional parameters as separate words
* [ ] The exit status
* [ ] The current working directory

#### Q. Which command reads user input into a variable?

* [ ] `input`
* [x] `read`
* [ ] `get`
* [ ] `scan`
* [ ] `prompt`

#### Q. How do you make a bash script executable?

* [ ] `bash script.sh`
* [x] `chmod +x script.sh`
* [ ] `exec script.sh`
* [ ] `run script.sh`
* [ ] `enable script.sh`

#### Q. What is the shebang line for a bash script?

* [ ] `#/bin/bash`
* [x] `#!/bin/bash`
* [ ] `#!bash`
* [ ] `#!/bash`
* [ ] `#/usr/bin/bash`

#### Q. Which operator is used for command substitution in bash?

* [ ] `{command}`
* [x] `$(command)`
* [ ] `[command]`
* [ ] `<command>`
* [ ] `@(command)`

#### Q. What does the `PS1` variable control?

* [ ] Path settings
* [x] The primary command prompt
* [ ] Process status
* [ ] Password settings
* [ ] Print settings

#### Q. Which command displays the value of an environment variable?

* [ ] `show VAR`
* [x] `echo $VAR`
* [ ] `print VAR`
* [ ] `display $VAR`
* [ ] `get VAR`

#### Q. What is the difference between single quotes and double quotes in bash?

* [ ] There is no difference
* [x] Single quotes preserve literal values; double quotes allow variable expansion
* [ ] Single quotes allow variable expansion; double quotes preserve literal values
* [ ] Single quotes are for numbers; double quotes are for strings
* [ ] Single quotes are deprecated

#### Q. Which command runs a script in a subshell?

* [x] `./script.sh`
* [ ] `source script.sh`
* [ ] `. script.sh`
* [ ] `exec script.sh`
* [ ] `eval script.sh`

#### Q. What is the purpose of `~/.inputrc`?

* [ ] Configures shell prompts
* [x] Configures readline key bindings
* [ ] Stores command history
* [ ] Defines aliases
* [ ] Sets environment variables

#### Q. Which command displays the command history?

* [ ] `show history`
* [x] `history`
* [ ] `hist`
* [ ] `commands`
* [ ] `log`

#### Q. How do you run the previous command in bash?

* [ ] `prev`
* [x] `!!`
* [ ] `--`
* [ ] `last`
* [ ] `^`
