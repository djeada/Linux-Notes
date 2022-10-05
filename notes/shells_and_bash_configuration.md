## Shells
In Unix, shells are the programs that user input and translate it to the OS commands. Whenever you open the terminal there is a shell repsonsible for the communication.

        user input -> shell -> kernel -> hardware

Most common shells include: `bash`, `zsh`, `ksh`, `tcsh` and `sh`.
`Bash` is the default shell on most distributions.

In `/etc/shells` you can find a list of all the shells that are available on your system. After executing `cat /etc/shells` the output should look like this:

```
/bin/bash
/bin/csh
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
```

To see the default shell for the user, use:

```
echo "$SHELL"
```

Use the following command to determine which shell is currently in use: 

```
ps -cp "$$" -o command=""
```

To switch to `zsh` in your terminal, you can use the command:

```
chsh -s /bin/zsh
```

## Bashrc

Every time a shell is started, the  `~/.bashrc` script is read. This is similar to  `\~/.cshrc` in C Shell.

The script is designed to be lightweight, with just the most important commands being run.

An example of a `~/.bashrc` script is:

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

### Bash_profile

The `~/.bash_profile` file is read every time a shell is started.

### Bash_logout

The `~/.bash_logout` file is read when the user logs out.

### Summary of configuration scripts

There are equivalent global scripts that are applied to all users at a specific event.

| Indvidual | Gloabl |
| --------- | ------ |
| - | /etc/enviroment |
| /home/user/.bashrc | /etc/bashrc |
| /home/user/profile | /etc/profile |

## Terminals

![terminal-shortcut](https://user-images.githubusercontent.com/37275728/190137189-f1abc2d9-fa15-43d8-8c27-ef11dde67db9.png)


## Challenges

1. Check if there is an existing alias for `cat`?
1. List all currently defined aliases.
1. Try adding some aliases to your `bashrc` and then removing them from the terminal. Reopen the terminal and check to see if the aliases are still active.
1. Make a list of every profile file on your system.
1. Create a user with a program set as his default logon shell. You might, for example, use `/bin/tar`. It's useful when a user should only be able to access one program on the server. 
13. Experiment with various shells. Check which of your custom variables, aliases, and functions are present in the new environment. 
