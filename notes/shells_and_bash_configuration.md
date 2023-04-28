## Shells

Shells in Unix are programs that allow users to interact with the operating system. They receive input from the user and execute commands to perform tasks.

        user input -> shell -> kernel -> hardware

Different shells are available, like `zsh`, `ksh`, `tcsh`, and `sh`. The `Bourne-Again Shell (bash)` is the default shell for most Linux distributions.

To see available shells on your system, check the `/etc/shells` file. It contains paths to all installed shells. Use `cat /etc/shells` to display the list:

```
/bin/bash
/bin/csh
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
```

To find your current shell, use `echo "$SHELL"` or `ps -cp "$$" -o command=""`.

To switch to another shell, like zsh, use `chsh -s /bin/zsh`.

## Bash Configuration Files

When a shell starts, it reads configuration files to set up the environment, variables, and aliases. The main configuration files for bash are:

* `~/.bashrc`: Read every time a new shell starts. It should be lightweight, with essential commands.
* `~/.bash_profile`: Read every time a shell starts.
* `~/.bash_logout`: Read when the user logs out.

An example `~/.bashrc` script:

```
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# User specific aliases and functions
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
```

Global configuration files apply to all users:

* `/etc/environment`: Read by all shells when starting.
* `/etc/bashrc`: Read by all bash shells when starting.
* `/etc/profile`: Read by all shells when starting.

## Terminals

Terminals are graphical interfaces for shells, allowing users to enter commands and see output. They support customization, with features like tabbed windows, split panes, and color schemes.

Open a new terminal window using the Ctrl + Alt + T shortcut on most systems.

![terminal-shortcut](https://user-images.githubusercontent.com/37275728/190137189-f1abc2d9-fa15-43d8-8c27-ef11dde67db9.png)

## Challenges

1. Check for existing `cat` aliases.
2. List all defined aliases.
3. Add and remove aliases in `bashrc`. Reopen the terminal to check if aliases persist.
4. List every profile file on your system.
5. Create a user with a specific program as the default logon shell (e.g., `/bin/tar`). Useful when a user should only access one program on the server.
6. Experiment with different shells. Check which custom variables, aliases, and functions are present in the new environment.
