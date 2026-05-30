## Shells and Terminals

A Unix shell is a command-line program that lets a user communicate with the operating system. Instead of using buttons and menus, the user types commands, and the shell interprets those commands.

For example, when you type:

```bash
ls
```

the shell understands that you want to list files in the current directory. It then asks the operating system to run the appropriate program and displays the result back to you.

The shell is useful because it gives direct control over the system. You can use it to manage files, run programs, install software, configure your environment, automate repetitive work, and write scripts.

### The Basic Interaction Model

The shell sits between the user and the operating system.

```text
+-------------------+       +----------------+       +--------------------+
|                   |       |                |       |                    |
|    User Input     |<----->|     Shell      |<----->|  Operating System  |
| (Keyboard/Screen) |       | (e.g., Bash)   |       |    (Kernel/HW)     |
|                   |       |                |       |                    |
+-------------------+       +----------------+       +--------------------+
```

The user enters a command through the keyboard. The shell reads the command, interprets it, and passes the request to the operating system. The operating system then interacts with hardware and system resources to complete the task.

A simple example is:

```bash
mkdir projects
```

This command asks the system to create a directory named `projects`.

The shell does not usually do all the work itself. Instead, it starts programs, passes arguments to them, manages input and output, and gives the user a way to control the system.

### Terminal vs Shell

A terminal and a shell are closely related, but they are not the same thing.

```text
+-----------------------------+
| Terminal Emulator           |
|                             |
|  +-----------------------+  |
|  | Shell                 |  |
|  | e.g., bash or zsh     |  |
|  +-----------------------+  |
|                             |
+-----------------------------+
```

The terminal is the window or application where you type commands.

The shell is the program running inside that terminal that understands and executes those commands.

A simple way to remember the difference is:

```text
Terminal = where you type
Shell    = what understands what you type
```

Examples of terminal emulators include GNOME Terminal, Konsole, xterm, Terminator, iTerm2, and Windows Terminal.

Examples of shells include Bash, Zsh, Sh, Ksh, and Tcsh.

### Common Shells

There are several shells available on Unix-like systems. Each one has its own strengths.

#### Bash

Bash stands for Bourne-Again SHell. It is one of the most common shells on Linux systems.

Bash is widely used because it is reliable, well documented, and available on most Linux distributions. Many tutorials and scripts assume Bash or a Bash-compatible shell.

A common Bash path is:

```bash
/bin/bash
```

Bash is a good shell for beginners because it is common, practical, and supported almost everywhere.

#### Zsh

Zsh, or Z Shell, is popular for interactive terminal use. It includes helpful features such as improved tab completion, spelling correction, themes, and plugins.

A common Zsh path is:

```bash
/bin/zsh
```

Many users like Zsh because it can be customized heavily. Tools such as Oh My Zsh make it easier to manage themes and plugins.

#### Sh

Sh, or the Bourne shell, is one of the original Unix shells. It is simple and portable.

On many modern systems, `/bin/sh` may actually point to another shell, such as Dash or Bash in compatibility mode.

Sh is often used when writing portable scripts that should run on many Unix-like systems.

#### Ksh

Ksh, or Korn shell, combines features from the Bourne shell and the C shell. It is powerful for scripting and has been used in many enterprise Unix environments.

It is less common today than Bash or Zsh, but it is still important on some systems.

#### Tcsh

Tcsh is an improved version of the C shell. It provides command-line editing and programmable completion.

It is less common than Bash or Zsh, but it may still appear on older systems or in specific Unix environments.

### Checking Which Shells Are Installed

Linux and Unix-like systems usually store valid login shells in this file:

```bash
/etc/shells
```

To view the available shells, run:

```bash
cat /etc/shells
```

Example output:

```text
/bin/sh
/bin/bash
/bin/dash
/bin/zsh
/usr/bin/zsh
```

This file matters because commands such as `chsh`, which changes your default shell, usually require the new shell to be listed in `/etc/shells`.

If a shell is not listed there, the system may refuse to use it as a login shell.

#### Finding Your Current Shell

There are several ways to check which shell you are using. The methods are similar, but they do not always show exactly the same thing.

#### Method 1: Check `$SHELL`

```bash
echo "$SHELL"
```

This usually shows your default login shell.

Example:

```text
/bin/bash
```

However, this does not always show the shell you are currently using. For example, your default shell may be Bash, but you might have started Zsh manually.

#### Method 2: Check the Current Process

```bash
ps -p "$$" -o comm=
```

This is usually a better way to check the shell currently running.

Here:

```text
$$
```

means “the process ID of the current shell.”

The command asks the system to show the command name for that process.

Example output:

```text
bash
```

or:

```text
zsh
```

#### Method 3: Check `$0`

```bash
echo "$0"
```

This prints the name of the current shell or script.

Example:

```text
-bash
```

A leading dash, such as `-bash`, usually means the shell was started as a login shell.

### Switching Shells

You can switch shells temporarily or permanently.

#### Temporarily Switching Shells

To start another shell, type its name:

```bash
zsh
```

or:

```bash
bash
```

This starts a new shell session inside the current terminal.

To leave the temporary shell and return to the previous one, run:

```bash
exit
```

You can also press:

```text
Ctrl + D
```

Temporary switching is useful when you want to test another shell without changing your account settings.

#### Permanently Changing Your Default Shell

To change your default login shell, use `chsh`.

For example, to make Zsh your default shell:

```bash
chsh -s /bin/zsh
```

You may be asked for your password.

The change usually takes effect the next time you log out and log back in.

Before changing your shell, check that the shell appears in `/etc/shells`:

```bash
cat /etc/shells
```

### Bash Configuration Files

Bash reads startup files when it starts. These files allow you to customize the shell.

You can use them to define aliases, environment variables, shell functions, prompt settings, history behavior, and other preferences.

Which files Bash reads depends on how the shell was started.

There are two important categories:

```text
+-----------------------------+
| Login Shell                 |
| Example: SSH login          |
| Reads login startup files   |
+-----------------------------+

+-----------------------------+
| Interactive Non-Login Shell |
| Example: new terminal tab   |
| Usually reads ~/.bashrc     |
+-----------------------------+
```

### Login Shells

A login shell is started when you log into a system. This can happen through a console login, an SSH session, or sometimes a terminal configured to start as a login shell.

When Bash starts as a login shell, it first reads:

```bash
/etc/profile
```

This is a global configuration file that can affect all users.

Then Bash looks for these user-specific files:

```bash
~/.bash_profile
~/.bash_login
~/.profile
```

Bash reads only the first one it finds.

The order is:

```text
1. ~/.bash_profile
2. ~/.bash_login
3. ~/.profile
```

The startup flow looks like this:

```text
Login Bash starts
       |
       v
Reads /etc/profile
       |
       v
Looks for user startup files
       |
       +--> ~/.bash_profile  if found, read this and stop
       |
       +--> ~/.bash_login    if found, read this and stop
       |
       +--> ~/.profile       if found, read this
```

### Interactive Non-Login Shells

An interactive non-login shell is usually what you get when you open a new terminal window or tab after already logging into a desktop environment.

For this type of shell, Bash usually reads:

```bash
~/.bashrc
```

Some systems also read a system-wide Bash configuration file first, such as:

```bash
/etc/bash.bashrc
```

or:

```bash
/etc/bashrc
```

The flow usually looks like this:

```text
New terminal window opens
       |
       v
Interactive non-login Bash starts
       |
       v
Reads system bashrc file if present
       |
       v
Reads ~/.bashrc
```

The `~/.bashrc` file is especially important because it is commonly used for everyday interactive settings.

### Why `~/.bashrc` Is Often Loaded from `~/.bash_profile`

A common issue is that login shells and non-login shells read different files.

For example, settings in `~/.bashrc` may not load in a login shell. Settings in `~/.bash_profile` may not load when opening a normal terminal window.

To make the shell behave consistently, users often source `~/.bashrc` from `~/.bash_profile`.

A typical `~/.bash_profile` contains:

```bash
# ~/.bash_profile

if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```

This means:

```text
If ~/.bashrc exists, load it.
```

The dot command:

```bash
. ~/.bashrc
```

means the same thing as:

```bash
source ~/.bashrc
```

Both commands run the contents of the file in the current shell.

### Common Things Stored in `~/.bashrc`

The `~/.bashrc` file is commonly used for settings that improve daily terminal use.

Typical contents include:

```text
aliases
environment variables
shell functions
prompt settings
history settings
program shortcuts
```

A small example:

```bash
# ~/.bashrc

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

export EDITOR='nano'
export HISTSIZE=1000
export HISTFILESIZE=2000

PS1='\u@\h:\w\$ '
```

### Aliases

An alias is a shortcut for a command.

For example:

```bash
alias ll='ls -alF'
```

After defining this alias, typing:

```bash
ll
```

runs:

```bash
ls -alF
```

Aliases are useful for commands you type often.

Common examples:

```bash
alias ll='ls -la'
alias cls='clear'
alias grep='grep --color=auto'
alias ..='cd ..'
```

To view all aliases currently defined:

```bash
alias
```

To check whether a specific alias exists:

```bash
alias cat
```

To remove an alias temporarily:

```bash
unalias ll
```

This only removes the alias from the current shell session. To remove it permanently, delete or comment out the alias line in `~/.bashrc`.

### Environment Variables

Environment variables are named values used by the shell and by programs started from the shell.

For example:

```bash
export EDITOR='nano'
```

This tells programs that need a text editor to use `nano` by default.

Another example:

```bash
export PATH="$HOME/bin:$PATH"
```

This adds the user’s `bin` directory to the command search path.

The `PATH` variable is especially important because it tells the shell where to look for programs when you type a command.

To view a variable:

```bash
echo "$PATH"
```

or:

```bash
echo "$EDITOR"
```

The `export` command makes a variable available to programs started from the shell.

Without `export`, the variable may only exist inside the current shell.

### Command History

Bash remembers commands you have typed.

Two common history variables are:

```bash
HISTSIZE=1000
HISTFILESIZE=2000
```

`HISTSIZE` controls how many commands are kept in memory during the current session.

`HISTFILESIZE` controls how many commands are saved in the history file, usually:

```bash
~/.bash_history
```

To view your recent commands:

```bash
history
```

Command history is useful because you can reuse previous commands with the up and down arrow keys.

### Prompt Customization

The shell prompt is the text shown before you type a command.

A prompt might look like this:

```text
adam@linux:~/notes$
```

In Bash, the prompt is controlled by the `PS1` variable.

Example:

```bash
PS1='\u@\h:\w\$ '
```

This means:

```text
\u  current username
\h  hostname
\w  current working directory
\$  $ for normal users, # for root
```

The prompt flow is:

```text
PS1 value
   |
   v
Bash expands symbols like \u, \h, and \w
   |
   v
Prompt appears before each command
```

Prompt customization is useful because it can show helpful information such as the current directory, username, hostname, or Git branch.

### Shell Functions

A shell function is a reusable group of commands.

Functions are more powerful than aliases because they can accept arguments and contain multiple steps.

Example:

```bash
mkcd() {
    mkdir -p "$1"
    cd "$1"
}
```

After adding this to `~/.bashrc` and reloading the file, you can run:

```bash
mkcd projects
```

This creates a directory named `projects` and immediately moves into it.

Here:

```bash
"$1"
```

means the first argument given to the function.

So in this command:

```bash
mkcd projects
```

`projects` becomes `$1`.

### Alias vs Function

Aliases are best for simple shortcuts.

Example:

```bash
alias ll='ls -la'
```

Functions are better when you need arguments, conditions, or multiple commands.

Example:

```bash
backup() {
    cp "$1" "$1.bak"
}
```

If you run:

```bash
backup notes.txt
```

the function creates:

```text
notes.txt.bak
```

A good rule is:

```text
Use an alias for a simple shortcut.
Use a function for reusable logic.
```

### Reloading Bash Configuration

After editing `~/.bashrc`, you do not always need to close and reopen the terminal.

You can reload it with:

```bash
source ~/.bashrc
```

or:

```bash
. ~/.bashrc
```

This applies changes to the current shell session.

For example, if you add:

```bash
alias ll='ls -la'
```

to `~/.bashrc`, then run:

```bash
source ~/.bashrc
```

the alias becomes available immediately.

### Example `~/.bashrc`

Here is a practical example of a `~/.bashrc` file:

```bash
# ~/.bashrc

# Load system-wide Bash settings if they exist
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# Useful aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias cls='clear'

# Environment variables
export EDITOR='nano'
export HISTSIZE=1000
export HISTFILESIZE=2000

# Prompt customization
PS1='\u@\h:\w\$ '

# Create a directory and move into it
mkcd() {
    mkdir -p "$1"
    cd "$1"
}

# Extract different archive types
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)   tar xjf "$1"   ;;
            *.tar.gz)    tar xzf "$1"   ;;
            *.bz2)       bunzip2 "$1"   ;;
            *.rar)       unrar x "$1"   ;;
            *.gz)        gunzip "$1"    ;;
            *.tar)       tar xf "$1"    ;;
            *.tbz2)      tar xjf "$1"   ;;
            *.tgz)       tar xzf "$1"   ;;
            *.zip)       unzip "$1"     ;;
            *.Z)         uncompress "$1";;
            *.7z)        7z x "$1"      ;;
            *)           echo "Do not know how to extract '$1'" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}
```

The `extract` function checks the file extension and chooses the correct extraction command.

For example:

```bash
extract archive.zip
```

runs:

```bash
unzip archive.zip
```

This is useful because the user only needs to remember one command instead of many different archive commands.

### Terminal Emulators

A terminal emulator is a program that gives you access to a shell.

In the past, users interacted with Unix systems through physical terminals. Today, most users use graphical terminal emulator programs.

The relationship looks like this:

```text
+------------------------------------------------+
| Terminal Emulator                              |
|                                                |
|  Displays text output                          |
|  Accepts keyboard input                        |
|  Handles tabs, panes, fonts, colors, shortcuts |
|                                                |
|  Inside it runs a shell such as Bash or Zsh    |
+------------------------------------------------+
```

### Common Terminal Emulator Features

- Modern terminal emulators often include features that make command-line work easier.
- Tabs allow multiple shell sessions in one window.
- Split panes divide the terminal window into sections, with each section running its own shell session.
- Custom colors and themes improve readability and comfort.
- Font settings allow users to change font type and size.
- Scrollback lets users scroll up and review previous output.
- Keyboard shortcuts make it faster to open tabs, close tabs, copy text, paste text, search output, and move between panes.
- Copy and paste support is important because terminal work often involves moving commands, paths, logs, and error messages between programs.

### Common Terminal Emulators

- GNOME Terminal is commonly used on Linux systems running the GNOME desktop environment. It is simple, stable, and easy to use.
- Konsole is the default terminal emulator for KDE Plasma. It is highly configurable and integrates well with KDE.
- xterm is a lightweight and traditional terminal emulator for the X Window System. It is portable but does not include many modern convenience features by default.
- Terminator is useful for arranging many terminal sessions in a grid layout. It is helpful when monitoring logs, running servers, or working on several tasks at once.
- iTerm2 is a popular terminal emulator for macOS. It supports split panes, profiles, search, hotkeys, and advanced customization.
- Windows Terminal is a modern terminal application for Windows. It can run PowerShell, Command Prompt, WSL shells, and other command-line environments.

### Opening a Terminal

On many Linux desktop environments, a terminal can be opened with:

```text
Ctrl + Alt + T
```

This shortcut may vary depending on the desktop environment or system settings.

You can also open a terminal from the application menu by searching for:

```text
Terminal
```

or by selecting the installed terminal emulator.

Visual example:

![Terminal Shortcut](https://user-images.githubusercontent.com/37275728/190137189-f1abc2d9-fa15-43d8-8c27-ef11dde67db9.png)

This screenshot is a helpful reminder that the terminal can usually be launched either with a keyboard shortcut or from the application menu.

### Useful Commands for Exploring Shells

To list installed login shells:

```bash
cat /etc/shells
```

To show your default login shell:

```bash
echo "$SHELL"
```

To show the current shell process:

```bash
ps -p "$$" -o comm=
```

To show all aliases:

```bash
alias
```

To check a specific alias:

```bash
alias cat
```

To reload Bash settings:

```bash
source ~/.bashrc
```

To temporarily start Zsh:

```bash
zsh
```

To exit the current shell:

```bash
exit
```

To change the default shell:

```bash
chsh -s /bin/zsh
```

### Searching for Profile Files

You can use the `find` command to search for files with `profile` in their name.

A basic command is:

```bash
find / -name '*profile*'
```

This searches from the root directory `/`.

However, searching the whole system may produce many permission errors. To hide permission errors, use:

```bash
find / -name '*profile*' 2>/dev/null
```

The part:

```bash
2>/dev/null
```

redirects error messages away from the terminal.

A safer and faster search in your home directory is:

```bash
find "$HOME" -name '*profile*'
```

### Important Safety Note About Changing Shells

Changing your default shell is usually safe if you choose a normal shell such as Bash or Zsh.

However, setting a user’s shell to a non-shell program can cause problems.

For example:

```bash
useradd -s /bin/tar username
```

This creates a user whose login shell is `/bin/tar`.

That is unusual and can prevent the user from having a normal interactive login session. It may be useful only in controlled experiments or restricted environments.

Do not test this on an important system unless you understand the consequences. It is better to use a virtual machine, container, or lab system.

### Challenges

1. Find if there are any existing aliases for a command, like `cat`. Use `alias cat` to see the aliases for `cat`.
2. Display all aliases currently defined in your shell. Simply execute `alias` without any arguments.
3. Open `~/.bashrc` in a text editor, add a new alias like `alias ll='ls -la'`. Save the file, reopen your terminal, and verify the new alias. To remove it, delete or comment out the line in `~/.bashrc`, then save and restart your terminal.
4. Use the `find` command to search your system for files containing 'profile' in their name. Try `find / -name '*profile*'`.
5. Create a new user whose default shell is a non-standard program. For example, `useradd -s /bin/tar username` creates a user with `/bin/tar` as their shell. Be aware of the implications this may have on user interaction with the system.
6. Change your default shell using `chsh -s /path/to/shell`, then open a new terminal session and explore the new environment. Experiment with commands like `alias`, `set`, and `declare -f` to inspect custom variables, aliases, and functions.
7. Write a custom shell function in your `~/.bashrc` file that automates a repetitive task (for example, a function that creates a directory and immediately changes into it). Reload your configuration and test the function. Explain the difference between an alias and a shell function.
8. Compare two different shells (for example, Bash and Zsh) by installing both on your system. Note the differences in tab completion, prompt customization, plugin support, and scripting syntax. Document which features you prefer in each shell.
9. Explore the startup file loading order by adding unique `echo` statements to `~/.profile`, `~/.bash_profile`, `~/.bashrc`, and `/etc/profile`. Open both login and non-login shells and observe which files are sourced in each case. Summarize the loading sequence for each shell type.
10. Customize your shell prompt by modifying the `PS1` variable in your `~/.bashrc` to display useful information such as the current user, hostname, working directory, and git branch (if applicable). Experiment with adding colors using ANSI escape codes and explain how each prompt component is defined.

