## Variable Types

In Unix‐style shells, variables let you store and reuse pieces of information—anything from your editor preference (`EDITOR=vim`) to the path where executables live (`PATH=/usr/local/bin:$PATH`) or temporary data in a script (`count=0`).  You’ll encounter two main kinds:

* **Shell variables** exist only in the current session (e.g. `count=5`); use them for loop counters or interim calculations in scripts.
* **Environment variables** are exported (`export VAR=value`) so child processes inherit them—essential for settings like `LANG=en_US.UTF-8`, `HOME=/home/ahmad` or API credentials (`export AWS_ACCESS_KEY_ID=…`).

### Environment Variables

Environment variables are key-value pairs that every process inherits, supplying critical configuration—like executable search paths, language settings, and user preferences—to your shell and applications. Proper management helps you tailor your environment, avoid runtime errors, and simplify scripts.

Run `printenv` to list all current variables:

```bash
printenv
```

Example output: 

```bash
PATH=/usr/local/bin:/usr/bin:/bin:/home/ahmad/bin
HOME=/home/ahmad
LANG=en_US.UTF-8
```

Each line shows `VARIABLE=value`. Scanning this output confirms which settings your tools rely on.

#### HISTSIZE

The number of commands your shell remembers is controlled by `HISTSIZE`. When `HISTSIZE` is large, you can retrieve older commands during a `Ctrl+R` search; if set to `0`, history is disabled entirely.

```bash
echo $HISTSIZE
```

Example output:
 
```bash
1000
```

Here, the last 1,000 commands are stored. You might increase this on a complex debugging session:

```bash
export HISTSIZE=2000
```

but note that overly long histories can slow down interactive searches or consume more memory.

#### HOME

Your home directory path comes from `HOME`. Scripts and applications use this to locate user-specific files (like `~/.config` or `~/.ssh`).

```bash
echo $HOME
```

Example output:

```bash
/home/ahmad
```

Commands like `cp config.json "$HOME/.config/myapp/"` work across any user account. If `$HOME` points to a non-existent path—common in some container setups—you’ll see errors when trying to `cd ~` or write files there.

#### PWD

The `PWD` variable always reflects your current working directory, updating as you `cd`. When a script logs output to `$PWD/log.txt`, it dynamically writes where you invoked it.

```bash
echo $PWD
```

Example output:

```bash
/home/ahmad/projects/env_test
```

If that directory involves symbolic links, `PWD` shows the logical path; use `pwd -P` when you need the physical filesystem location instead.

#### HOSTNAME

Every system has a `HOSTNAME` for network identification. Automated backups that include `$(date +%F)-$HOSTNAME.tar.gz` clearly tag which machine produced each archive.

```bash
echo $HOSTNAME
```

Example output:

```bash
ahmad-laptop
```

In cloud instances, the default hostname may be a random ID; setting `/etc/hostname` ensures consistent naming across reboots.

#### PATH

The `PATH` variable lists directories separated by colons, telling your shell where to find executables. After installing custom tools in `/opt/tools/bin`, exporting `PATH=$PATH:/opt/tools/bin` lets you invoke them without full paths.

```bash
echo $PATH
```

Example output:

```bash
/usr/local/bin:/usr/bin:/bin:/home/ahmad/bin
```

Appending a directory is safe, but when you need your own scripts to override system binaries, place your directory first:

```bash
export PATH=/home/ahmad/custom/bin:$PATH
```

Duplicate or stale entries slow down command lookup; if you spot `/old/path`, remove it by reconstructing `PATH` without it, for example using `awk`.

#### Changing Variables

To adjust environment variables only for your current session, export them directly:

```bash
export DATABASE_URL='postgres://user:pass@localhost/db'
echo $DATABASE_URL
```

Example output:

```
postgres://user:pass@localhost/db
```

This change vanishes when you close the shell. For permanent updates, append export statements to your shell startup files (like `~/.bashrc` or `~/.profile`) and reload them:

```bash
echo 'export EDITOR=vim' >> ~/.bashrc
source ~/.bashrc
echo $EDITOR
```

Example output:

```
vim
```

On macOS or login shells, prefer `~/.bash_profile` or `~/.profile` when `~/.bashrc` isn’t sourced.

#### Tips and Safeguards

Wrap values containing spaces or special characters in quotes (`export GREETING="Hello World!"`), lock variables with `readonly VAR` to avoid accidental changes, and remove obsolete settings using `unset VAR`. In scripts, enable tracing with `set -x` to follow variable expansions, and use parameter expansions that abort when critical variables are empty:

```bash
: "${API_KEY:?API_KEY is required}"  # stops script if API_KEY is unset or blank
```



### Challenges

1. Write a Bash script named `greetings.sh` that prints a welcome message. Make sure the script has executable permissions by using `chmod +x greetings.sh`. Then, modify the `PATH` environment variable to include the directory where the script is stored by using `export PATH=$PATH:/path/to/script`. Test executing the script from any directory without specifying its full path, and explain the importance of the `PATH` variable.
2. Use the `USER` environment variable in a command or script to print a personalized greeting, such as “Hello, $USER! Welcome back!”. Discuss how environment variables can add user-specific context to scripts and commands, and explain why `USER` is automatically set by the system.
3. Display all currently set shell and environment variables by using commands like `set` or `env`. Compare the output of these commands and explain the difference between shell variables and environment variables, as well as how they are inherited by child processes.
4. Create a variable in your terminal session and assign a numeric value to it. Perform a few arithmetic operations with this variable, such as addition or multiplication, and print the results. Explain how shell variables differ from environment variables and discuss the syntax for arithmetic operations in Bash.
5. Use the `export` command to create a new environment variable, then print its value using `echo`. Discuss how the `export` command makes a variable available to child processes and explain when you might need to use it in scripting and system configuration.
6. Use `env` to display all current environment variables, then start a new shell with a completely clean environment by using `env -i`. Explore the differences between the regular shell and the clean shell, and discuss how environment variables are essential for a functioning user environment.
7. Write a shell script that stores a number in an environment variable and increments this number each time the script is run. Ensure the variable persists between script executions by using a file or another method to save the variable's state. Discuss how environment variables can be used to store persistent state information for scripts.
8. Use the `PATH` variable to locate an executable file on your system. Then, add a new directory to `PATH` by using `export PATH=$PATH:/new/directory`. Test running a command from this new directory without its full path, and explain how the `PATH` variable affects command discovery and execution in the shell.
9. Write a script that uses `printenv` to display specific environment variables, such as `HOME`, `SHELL`, and `PWD`. Explain how each of these environment variables is used by the system to manage the user environment, and why they are automatically set when the user logs in.
10. Create a custom environment variable with sensitive information (e.g., an API key or password) and export it. Then, access this variable from within a child process by using `echo` or another command. Discuss best practices for handling sensitive information in environment variables and explain how to prevent accidental exposure of these variables in shared environments.
