## Shells
In Unix, shells are the programs that run on the command line. They are the programs that you use to execute commands.
Most common shells include: <code>bash</code>, <code>zsh</code>, <code>ksh</code>, <code>tcsh</code> and <code>sh</code>.

In /etc/shells you can find a list of all the shells that are available on your system. The file contents should look like this:

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

To switch to <code>zsh</code> in your terminal, you can use the command:

```
chsh -s /bin/zsh
```

## Bashrc

Every time a shell is started, the  <i>\~/.bashrc</i> script is read. This is similar to  <i>\~/.cshrc</i> in C Shell.

The script is designed to be lightweight, with just the most important commands being run.

An example of a <i>\~/.bashrc</i> script is:

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

The <i>\~/.bash_profile</i> file is read every time a shell is started.

### Bash_logout

The <i>\~/.bash_logout</i> file is read when the user logs out.

## Terminals

![terminal-shortcut](https://user-images.githubusercontent.com/37275728/190137189-f1abc2d9-fa15-43d8-8c27-ef11dde67db9.png)


## Challenges

1. Check if there is an existing alias for <code>cat</code>?
1. List all currently defined aliases.
1. Try adding some aliases to your <code>bashrc</code> and then removing them from the terminal. Reopen the terminal and check to see if the aliases are still active.
1. Make a list of every profile file on your system.
1. Experiment with various shells. Check which of your custom variables, aliases, and functions are present in the new environment. 
