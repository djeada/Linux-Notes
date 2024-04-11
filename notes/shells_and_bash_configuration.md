## Shells

A Unix shell is an essential tool that provides a command-line interface for users to interact with the operating system. This interaction occurs in a sequence where the shell reads the user's inputs, translates them into system commands, and then communicates these commands to the operating system kernel for execution, which then interacts with the hardware.

The process can be visualized as follows:

```
+-------------------+       +---------------+       +--------------+
|                   |       |               |       |              |
|  User Input/      |<----->|    Shell      |<----->|   System     |
|  Output Device    |       | (e.g., Bash)  |       | (Kernel/HW)  |
|  (Keyboard/Screen)|       |               |       |              |
|                   |       |               |       |              |
+-------------------+       +---------------+       +--------------+
```

Among a variety of available shells like `bash` (Bourne-Again SHell), `zsh` (Z Shell), `ksh` (Korn SHell), `tcsh` (TENEX C Shell), and `sh` (Bourne SHell), `bash` is the default shell for most Linux distributions because of its extensive feature set and user-friendly nature.

### Examining Available Shells

To discover the shells installed on your system, you can look into the `/etc/shells` file. This file contains the paths to all the shells installed on your system. Use the `cat` command to display the file's content:

```bash
cat /etc/shells
```

The output might look something like this:

```bash
/bin/bash
/bin/csh
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
```

### Identifying Your Current Shell

To find out your current active shell, use the following command:

```bash
echo "$SHELL"
```

Alternatively, you can use the ps command to see the process associated with your terminal:

```bash
ps -cp "$$" -o command=""
```

### Switching Shells

If you wish to switch to a different shell, like the Z shell (zsh), you can use the chsh (change shell) command with the -s option and the path to the desired shell:

```bash
chsh -s /bin/zsh
```

You will need to enter your password, and then you may need to restart your session for the changes to take effect. Make sure the shell you're switching to is listed in your /etc/shells file, or else the chsh command may not succeed.

## Bash Configuration Files

In the bash shell, several configuration files are read when the shell starts, providing a way to control the shell's behavior and set up things like environment variables, functions, and aliases.

Here are the primary configuration files relevant to a bash shell:

* `~/.bashrc`: This is the individual user's bash shell script, which gets executed every time a new interactive shell session starts. It's an ideal place for setting up your environment with commands that are lightweight and essential for your daily usage.

* `~/.bash_profile`: This file, also specific to the individual user, is read and executed when you start a login shell session. It's often used to set environment variables and execute commands that should run once when you log in, such as starting a session manager or launching a personal daemon.

* `~/.bash_logout`: This file is executed when you log out of a login shell session. It's commonly used for cleanup tasks and other end-of-session housekeeping.

Below is a simple example of a `~/.bashrc` script:

```bash
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

Bash also provides system-wide configuration files which affect all users:

- `/etc/environment`: This file is read by all shells upon startup. It's used to set up system-wide environment variables.
- `/etc/bash.bashrc` or `/etc/bashrc` (location varies by system): This is the system-wide version of the individual user's ~/.bashrc file, which gets executed for every user that starts an interactive bash shell.
- `/etc/profile`: This file is a global configuration script that applies to all users. It's executed upon the start of a bash login shell, much like the user-specific `~/.bash_profile`.

## Terminals

Terminals, often referred to as terminal emulators, are computer programs that provide a graphical user interface for interacting with a shell. They serve as a conduit for entering commands and viewing their output, allowing users to communicate with the operating system.

The terminal's features extend beyond just command input and output, offering users a range of customization options to suit their needs and preferences. These options include:

* **Tabbed Windows**: You can have multiple terminal sessions open within one terminal window using tabs, similar to how you might use a web browser. This allows you to work on different tasks in separate sessions without needing to open multiple terminal windows.

* **Split Panes**: Some terminal emulators allow you to divide your terminal window into multiple panes, each of which can host its own independent terminal session. This can be especially useful for monitoring the output of multiple commands at once.

* **Color Schemes**: Terminals typically allow users to customize the colors of the text and background, which can help reduce eye strain and make text easier to read. Additionally, syntax highlighting can use different colors to distinguish different types of text, making code and complex command outputs easier to understand.

* **Font Customization**: You can customize the font size, style, and family to make the terminal more readable and visually appealing.

* **Keyboard Shortcuts**: Terminals often support keyboard shortcuts for actions like creating new tabs, switching between tabs, and copying and pasting text.

On many systems, a new terminal window can be opened quickly using the Ctrl + Alt + T keyboard shortcut. This command brings up a new terminal window where you can begin entering commands.

![Terminal Shortcut](https://user-images.githubusercontent.com/37275728/190137189-f1abc2d9-fa15-43d8-8c27-ef11dde67db9.png)

Various terminal emulators are available, each offering a different set of features and aesthetics. Some of the popular ones include GNOME Terminal, Konsole, xterm, iTerm2, and Hyper. Your choice of terminal can greatly impact your command-line experience, so it's worth trying out a few to see which one you prefer.

## Challenges

1. Find if there are any existing aliases for a command, like `cat`. Use `alias cat` to see the aliases for `cat`.
2. Display all aliases currently defined in your shell. Simply execute `alias` without any arguments.
3. Open `~/.bashrc` in a text editor, add a new alias like `alias ll='ls -la'`. Save the file, reopen your terminal, and verify the new alias. To remove it, delete or comment out the line in `~/.bashrc`, then save and restart your terminal.
4. Use the `find` command to search your system for files containing 'profile' in their name. Try `find / -name '*profile*'`.
5. Create a new user whose default shell is a non-standard program. For example, `useradd -s /bin/tar username` creates a user with `/bin/tar` as their shell. Be aware of the implications this may have on user interaction with the system.
6. Change your default shell using `chsh -s /path/to/shell`, then open a new terminal session and explore the new environment. Experiment with commands like `alias`, `set`, and `declare -f` to inspect custom variables, aliases, and functions.
