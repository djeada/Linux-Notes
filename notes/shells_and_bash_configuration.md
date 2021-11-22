<h1>Shells</h1>
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

To switch to <code>zsh</code> in your terminal, you can use the command:

```
chsh -s /bin/zsh
```

<h1>Bashrc</h1>

Every time a shell is started, the  <i>\~/.bashrc</i> script is read. This is similar to  <i>\~/.cshrc</i>  in C Shell.

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

<h2>Bash_profile</h2>

The <i>\~/.bash_profile</i> file is read every time a shell is started.

<h2>bash_logout</h2>

The <i>\~/.bash_logout</i> file is read when the user logs out.

