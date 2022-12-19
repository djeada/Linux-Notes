## Shells

In Unix, shells are programs that interpret user input and translate it into commands that the operating system can execute. When you open a terminal window, a shell is responsible for providing the interface between you and the operating system.

        user input -> shell -> kernel -> hardware

There are several different shells available, including `bash`, `zsh`, `ksh`, `tcsh`, and `sh`. `Bash` is the default shell on most Linux distributions.

You can view a list of available shells on your system by looking at the `/etc/shells` file. This file will contain a list of paths to all the shells installed on the system. For example, the output of `cat /etc/shells` might look like this:

```
/bin/bash
/bin/csh
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
```

To find out which shell you are currently using, you can use the echo `"$SHELL"` command. Alternatively, you can use `ps -cp "$$" -o command=""` to see the current shell.

To switch to a different shell, such as zsh, you can use the `chsh -s /bin/zsh` command.

## Bash Configuration Files

When a shell is started, it reads certain configuration files to set up the environment and define any necessary variables or aliases. The main configuration files for bash are:

* `~/.bashrc`: This file is read every time a new shell is started. It is intended to be lightweight, with only the most essential commands being executed.
* `~/.bash_profile`: This file is read every time a shell is started.
* `~/.bash_logout`: This file is read when the user logs out.

An example of a `~/.bashrc` script:

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

There are also global configuration files that apply to all users at specific events:

* `/etc/environment`: This file is read by all shells when they start.
* `/etc/bashrc`: This file is read by all bash shells when they start.
* `/etc/profile`: This file is read by all shells when they start.

## Terminals

A terminal window is a graphical interface to a shell. It allows you to enter commands and see the output of those commands in a text-based interface. Many terminals also support customization and provide features such as tabbed windows, split panes, and color schemes.

To open a new terminal window, you can use the keyboard shortcut Ctrl + Alt + T on most systems.

![terminal-shortcut](https://user-images.githubusercontent.com/37275728/190137189-f1abc2d9-fa15-43d8-8c27-ef11dde67db9.png)

## Challenges

1. Check if there is an existing alias for `cat`.
1. List all currently defined aliases.
1. Add some aliases to your `bashrc` file and then remove them from the terminal. Reopen the terminal and check to see if the aliases are still active.
1. Make a list of every profile file on your system.
1. Create a user with a specific program set as his default logon shell. You might, for example, use `/bin/tar`. It's useful when a user should only be able to access one program on the server. 
1. Experiment with various shells. Check which of your custom variables, aliases, and functions are present in the new environment. 
