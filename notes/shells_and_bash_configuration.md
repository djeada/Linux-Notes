## Shells

A Unix shell is a command-line interpreter that provides a user interface for accessing an operating system's services. It allows users to execute commands, run programs, and manage system resources. The shell acts as an intermediary between the user and the operating system kernel, translating user commands into actions performed by the system.

### The Interaction Model

The interaction between the user, shell, and operating system can be visualized as follows:

```
+-------------------+       +----------------+       +--------------------+
|                   |       |                |       |                    |
|    User Input     |<----->|     Shell      |<----->|  Operating System  |
| (Keyboard/Screen) |       | (e.g., Bash)   |       |    (Kernel/HW)     |
|                   |       |                |       |                    |
+-------------------+       +----------------+       +--------------------+
```

- **User input** consists of the commands and data entered by the user through devices like keyboards or other input peripherals, initiating interactions with the system.
- The **shell** acts as an interpreter, translating user commands into instructions and communicating them to the operating system for execution.
- The **operating system** is responsible for executing the commands provided by the shell and managing the system's hardware resources to fulfill user requests.
- By handling user input, the shell serves as a crucial interface between the user and the operating system, ensuring smooth communication and task execution.

### Common Shells

There are several types of shells available, each with unique features:

| Shell                    | Description                                                    | Benefits                                                      | Considerations/Drawbacks                                        |
|---------------------------|----------------------------------------------------------------|---------------------------------------------------------------|----------------------------------------------------------------|
| **`bash` (Bourne-Again SHell)** | The default shell on most Linux distributions; backward-compatible with the original Bourne shell. | Widely used, with extensive scripting support and community resources. | Lacks some advanced features present in newer shells like `zsh`. |
| **`zsh` (Z Shell)**       | Known for its rich feature set, including improved auto-completion, spell correction, and theming capabilities. | Highly customizable, with better autocompletion and plugins.   | Slight learning curve for users unfamiliar with its configuration. |
| **`ksh` (Korn SHell)**    | Combines features of the Bourne shell and the C shell (`csh`). | Useful for scripting, combining the best of both worlds (Bourne and C shell). | Not as widely adopted as `bash` or `zsh`.                       |
| **`tcsh` (TENEX C Shell)**| An enhanced version of the C shell, featuring command-line editing and programmable word completion. | Better user experience with command-line editing features.     | Less common compared to `bash` or `zsh`.                        |
| **`sh` (Bourne SHell)**   | The original Unix shell, simple and portable.                  | Lightweight and portable for basic scripting tasks.            | Lacks many modern features available in newer shells.           |

### Examining Available Shells

To see which shells are installed on your system, inspect the `/etc/shells` file. This file lists all the valid login shells available.

```bash
cat /etc/shells
```

**Example Output:**

```
/bin/sh
/bin/bash
/bin/dash
/bin/zsh
/usr/bin/zsh
```

### Identifying Your Current Shell

To determine your current active shell, you can use several methods:

#### Method 1: Using the `$SHELL` Variable

```bash
echo "$SHELL"
```

**Note:** The `$SHELL` variable shows your default login shell, not necessarily the shell you're currently using.

#### Method 2: Inspecting the Shell Process

```bash
ps -p "$$" -o comm=
```

- `$$` represents the current shell's process ID.
- `ps -p` selects the process with that ID.
- `-o comm=` outputs the command name (the shell).

#### Method 3: Using `echo "$0"`

```bash
echo "$0"
```

- `$0` contains the name of the shell or script being executed.

### Switching Shells

#### Temporarily Switching Shells

You can start a different shell session by typing its name:

```bash
zsh
```

To return to your previous shell, type `exit` or press `Ctrl+D`.

#### Permanently Changing Your Default Shell

To change your default login shell, use the `chsh` (change shell) command:

```bash
chsh -s /bin/zsh
```

- You'll be prompted for your password.
- Changes will take effect the next time you log in.

**Important:** The shell must be listed in `/etc/shells`; otherwise, `chsh` will not accept it.

### Bash Configuration Files

When Bash starts, it reads and executes commands from various startup files. These files allow you to customize your shell environment.

#### Types of Shells

Understanding which configuration files are read depends on how the shell is invoked:

- A **login shell** is a shell session that requires the user to authenticate, such as when logging in from a console or via SSH, before accessing the system.
- An **interactive non-login shell** is opened after the user has already logged in, for instance, when opening a new terminal window, and does not require further authentication.

#### Configuration Files Overview

I. **Global Configuration Files** (affect all users):

- `/etc/profile`: Executed for login shells.
- `/etc/bash.bashrc` or `/etc/bashrc`: Executed for interactive non-login shells.

II. **User-Specific Configuration Files** (affect only the current user):

- `~/.bash_profile` or `~/.bash_login` or `~/.profile`: Read by login shells. Bash reads the first one it finds.
- `~/.bashrc`: Read by interactive non-login shells.
- `~/.bash_logout`: Executed when a login shell exits.

### Bash Startup Sequence

#### For Login Shells:

1. Bash reads `/etc/profile`.
2. Then it looks for `~/.bash_profile`, `~/.bash_login`, and `~/.profile` (in that order) and reads the first one it finds.

#### For Interactive Non-Login Shells:

1. Bash reads `/etc/bash.bashrc` or `/etc/bashrc` (system-wide configuration).
2. Then it reads `~/.bashrc` (user-specific configuration).

### Best Practice: Source `~/.bashrc` from `~/.bash_profile`

To ensure that your settings are consistent across all shell types, it's common to source `~/.bashrc` from `~/.bash_profile`.

**Example `~/.bash_profile`:**

```bash
# ~/.bash_profile

# Source the user's bashrc if it exists
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```

### Sample `~/.bashrc` File

```bash
# ~/.bashrc

# Source global definitions if any
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# Alias definitions
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Environment variables
export EDITOR='nano'
export HISTSIZE=1000
export HISTFILESIZE=2000

# Prompt customization
PS1='\u@\h:\w\$ '

# Functions
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
            *)           echo "Don't know how to extract '$1'..." ;;
        esac
    else
        echo "'$1' is not a valid file!"
    fi
}
```

- **Aliases** provide a way to create shortcuts for frequently used commands, reducing the need for repetitive typing.
- Using `alias ll='ls -alF'` is an example that lists all files in long format, including indicators for file types.
- **Environment variables** are key-value pairs that configure the shell or external programs.
- Setting `export EDITOR='nano'` ensures that nano becomes the default text editor when editing files through the terminal.
- **Prompt customization** helps users personalize their command prompt, displaying important information like username and directory.
- The command `PS1='\u@\h:\w\$ '` modifies the prompt to show the username, hostname, and the current working directory.
- **Functions** are used to create reusable commands that can handle multiple steps or repetitive tasks.
- A function like `extract()` is useful for extracting different archive types such as `.zip`, `.tar.gz`, and `.rar` files, making file management more efficient.

### Terminals

A terminal emulator is a program that emulates a physical terminal within a graphical interface, allowing users to interact with the shell.

#### Terminal Emulator Features

- **Multiple Tabs** allow users to run multiple shell sessions within a single window, improving multitasking efficiency.
- **Split Panes** let users divide the terminal window into multiple panes, each running its own session simultaneously.
- **Customizable Appearance** gives users control over how their terminal looks, enabling adjustments to match personal preferences.
- **Color Schemes** allow changing the text and background colors, enhancing readability or aesthetics.
- **Fonts** can be modified in type and size to suit individual reading comfort.
- **Transparency** is supported by some terminals, allowing the background to appear transparent for a seamless visual experience.
- **Keyboard Shortcuts** make navigation and actions faster within the terminal.
- **Copy/Paste** shortcuts enable quick copying and pasting of text without using the mouse.
- **Navigation** shortcuts allow users to easily switch between tabs or panes using the keyboard.
- **Scrollback Buffer** enables users to view previous output by scrolling up, ensuring that past terminal output is accessible for review.

#### Common Terminal Emulators

| Terminal Emulator    | Description                                             | Benefits                                             | Considerations/Drawbacks                             |
|----------------------|---------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------|
| **GNOME Terminal**    | Default terminal emulator on GNOME desktop environments. | Integrated with GNOME, easy to use.                  | Lacks some advanced customization features.          |
| **Konsole**          | Default terminal emulator on KDE Plasma desktop environments. | Highly customizable and integrates well with KDE.    | Primarily designed for KDE, may not be ideal for other environments. |
| **xterm**            | Basic terminal emulator for the X Window System.         | Lightweight and highly portable.                     | Lacks modern features like tabs or split views.      |
| **Terminator**       | Allows arranging multiple terminals in grids.            | Ideal for multitasking with a grid layout.            | May be overkill for basic terminal usage.            |
| **iTerm2**           | Popular terminal emulator for macOS with advanced features. | Offers split panes, hotkeys, and extensive customization. | Only available on macOS.                             |

#### Opening a Terminal

- `Ctrl + Alt + T` (commonly opens the default terminal).
- Navigate to the system's application menu and select the terminal emulator.

![Terminal Shortcut](https://user-images.githubusercontent.com/37275728/190137189-f1abc2d9-fa15-43d8-8c27-ef11dde67db9.png)

### Challenges

1. Find if there are any existing aliases for a command, like `cat`. Use `alias cat` to see the aliases for `cat`.
2. Display all aliases currently defined in your shell. Simply execute `alias` without any arguments.
3. Open `~/.bashrc` in a text editor, add a new alias like `alias ll='ls -la'`. Save the file, reopen your terminal, and verify the new alias. To remove it, delete or comment out the line in `~/.bashrc`, then save and restart your terminal.
4. Use the `find` command to search your system for files containing 'profile' in their name. Try `find / -name '*profile*'`.
5. Create a new user whose default shell is a non-standard program. For example, `useradd -s /bin/tar username` creates a user with `/bin/tar` as their shell. Be aware of the implications this may have on user interaction with the system.
6. Change your default shell using `chsh -s /path/to/shell`, then open a new terminal session and explore the new environment. Experiment with commands like `alias`, `set`, and `declare -f` to inspect custom variables, aliases, and functions.
