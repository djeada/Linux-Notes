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
### Shell Variables

Shell variables control the behavior and state of your current shell session. These temporary name–value pairs can store counters, flags, formatting rules, or other pieces of data that your commands and scripts can reference. Because they live only in the running shell, any variables you define will vanish when you close the terminal.

Shell variables control the behavior of your current shell session, holding temporary values—such as counters, flags, or formatting rules—that disappear when you close the terminal. You create one simply by assigning a name to a value:

```bash
count=10
echo "$count"
```

Example output:

```bash
10
```

Referencing an unset variable returns an empty string, which can silently break scripts or commands.

#### Enforcing Defined Variables

To guard against accidentally using undefined variables in your scripts, you can enable strict mode. This ensures that any reference to a variable that has not been set will cause the script to exit immediately with an error.

```bash
set -u
```

Example script snippet:

```bash
#!/usr/bin/env bash
set -u
echo "Count is $count"   # Aborts here if count is unset.
```

### Customizing Your Prompt (PS1)

Your shell prompt is the primary interface for issuing commands, and customizing it can give you at-a-glance information about your session. The `PS1` variable defines exactly what is displayed at each prompt, letting you include your username, hostname, working directory, and special symbols that reflect your permissions or status.

The `PS1` variable defines what appears at each command prompt. You can include special backslash-escape sequences to display dynamic information:

```bash
PS1="\u@\h:\w\$ "
```

Example output:

```bash
# After setting, your prompt looks like:
ahmad@machine:/home/ahmad$
```

Unsupported or mistyped escapes (e.g., `\x`) will appear literally in your prompt.

**Common escapes:**

| Escape Sequence | Description                           |
| --------------- | ------------------------------------- |
| `\u`            | Current username                      |
| `\h`            | Hostname (up to the first dot)        |
| `\w`            | Current working directory (full path) |
| `\$`            | `#` if running as root, otherwise `$` |

#### Word Splitting and IFS

When you pass a string of words to a shell construct—such as a loop or a command—Bash splits that string into separate words using the **Internal Field Separator** (`IFS`). By default, `IFS` includes whitespace characters: spaces, tabs, and newlines. Changing `IFS` lets you define custom delimiters for splitting, which is essential when working with comma-separated values, semicolon lists, or other structured data in shell scripts.

By default, Bash splits input on whitespace (spaces, tabs, newlines) as defined by the **Internal Field Separator** (`IFS`).

```bash
printf "%s\n" "a b" "x y" "c"
```

Example output:

```bash
# With default IFS, output:
a
b
x
y
c
```

You can change `IFS` to split on a different character. For example, to split on commas:

```bash
IFS=','
printf "%s\n" "a,b" "x,y" "c"
```

Example output:

```bash
# With IFS=',' :
a
b
x
y
c
```

Setting `IFS=` (empty) disables splitting entirely. Loops like

```bash
for item in $list; do …
done
```

will treat the entire string as a single item, potentially causing infinite loops or logic errors.

#### Listing All Definitions

It’s often useful to see everything that’s currently defined in your shell: variables, functions, and aliases. The built-in `set` command without any arguments dumps this entire list, allowing you to spot unwanted overrides or debug unexpected behavior—especially cases where a local variable shadows a critical environment variable like `PATH`.

To inspect every variable, function, and alias in your current shell:

```bash
set
```

Example output:

```bash
BASH=/usr/bin/bash
BASHOPTS=checkwinsize:cmdhist:complete_fullquote:expand_aliases:extglob:extquote:force_fignore:globasciiranges:globskipdots:histappend:interactive_comments:patsub_replacement:progcomp:promptvars:sourcepath
BASH_ALIASES=()
BASH_ARGC=([0]="0")
BASH_ARGV=()
BASH_CMDS=()
BASH_COMPLETION_VERSINFO=([0]="2" [1]="11")
...
```

#### Making Variables Read-Only

Once you’ve set a variable to a value you don’t want to change—such as a maximum number of retries or a critical directory path—it’s best to mark it as read-only. Any subsequent attempts to reassign or unset the variable will fail with an error, helping prevent logic bugs caused by accidental reassignment.

Prevent accidental reassignment by marking variables as immutable:

```bash
readonly max_retries=5
max_retries=3
```

Example output:

```bash
bash: max_retries: readonly variable
```

Attempting to unset:

```bash
unset max_retries
```

yields:

```bash
bash: unset: max_retries: cannot unset: readonly variable
```

### Safe Script Defaults

When writing shell scripts that you expect to run unattended or in production, it’s critical to fail early and loudly on errors, undefined variables, or pipeline failures. The recommended shebang and `set` options at the top of your script enforce these best practices, leading to safer and more maintainable code.

For robust, predictable scripts, combine these options at the top:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

Immediately stops on errors, avoids cascading failures, and catches typos or missing variables before they cause silent malfunctions.

**Options:**

| Option        | Meaning                                                                  |
| ------------- | ------------------------------------------------------------------------ |
| `-e`          | Exit immediately if any command returns a non-zero status.               |
| `-u`          | Treat unset variables as an error when substituting.                     |
| `-o pipefail` | Return the failure status of the first command in a pipeline that fails. |

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
