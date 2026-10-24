# Shell and Bash Quiz

Notes: [Shells and Terminals](../notes/shells_and_bash_configuration.md), [Variables](../notes/environment_variable.md), [Data Streams](../notes/pipe_and_redirect.md)

Check your understanding of Bash startup files, variables, quoting, redirection and safe scripting.

#### Q. What is the difference between a terminal and a shell?

* [ ] They are two names for the same program
* [x] The terminal is the window you type into; the shell interprets the commands
* [ ] The shell draws the window; the terminal runs the commands
* [ ] A terminal is used only for remote sessions, a shell only for local ones

> **Explanation:** A terminal emulator such as GNOME Terminal or xterm provides the window and keyboard input. The shell (Bash, Zsh, and so on) runs inside it, parses commands and starts programs.

#### Q. Which file lists the shells that may be used as login shells, and is checked by `chsh`?

* [ ] `/etc/passwd`
* [x] `/etc/shells`
* [ ] `/etc/login.defs`
* [ ] `/etc/bash.bashrc`

> **Explanation:** `chsh -s /bin/zsh` normally refuses a shell that is not listed in `/etc/shells`. Each user's chosen login shell is then stored in the last field of their `/etc/passwd` entry.

#### Q. Your login shell is Bash, but you have just typed `zsh` to try it out. Which command reliably shows the shell you are running right now?

* [ ] `echo "$SHELL"`
* [x] `ps -p "$$" -o comm=`
* [ ] `cat /etc/shells`
* [ ] `echo "$PATH"`

> **Explanation:** `$$` is the PID of the current shell, and `ps` prints its command name. `$SHELL` normally holds your default login shell, so it would still say `/bin/bash`.

#### Q. `echo "$0"` prints `-bash`. What does the leading dash tell you?

* [ ] The shell is running in POSIX compatibility mode
* [x] The shell was started as a login shell
* [ ] The shell is a non-interactive subshell
* [ ] The shell is running with restricted permissions

> **Explanation:** By convention, a login shell's `argv[0]` starts with `-`. Login shells read `/etc/profile` and then the first of `~/.bash_profile`, `~/.bash_login` or `~/.profile` that exists.

#### Q. You log in over SSH, and Bash starts as a login shell. A user has both `~/.bash_profile` and `~/.profile`. Which files does Bash read?

* [ ] Only `~/.bashrc`
* [x] `/etc/profile`, then `~/.bash_profile` only
* [ ] `/etc/profile`, then `~/.bash_profile`, then `~/.profile`
* [ ] `~/.profile`, then `/etc/profile`

> **Explanation:** A login shell reads `/etc/profile`, then only the first user file it finds out of `~/.bash_profile`, `~/.bash_login` and `~/.profile`. Here `~/.profile` is skipped because `~/.bash_profile` exists.

#### Q. Which file does Bash read when you open a new terminal tab in a desktop session (an interactive, non-login shell)?

* [ ] `~/.bash_profile`
* [x] `~/.bashrc`
* [ ] `~/.bash_logout`
* [ ] `/etc/profile`

> **Explanation:** Interactive non-login shells read `~/.bashrc`, often after a system-wide file such as `/etc/bash.bashrc`. Aliases, functions and prompt settings usually live there.

#### Q. Aliases defined in `~/.bashrc` are missing when you log in over SSH. What is the usual fix?

* [ ] Move the aliases into `/etc/shells`
* [x] Source `~/.bashrc` from `~/.bash_profile`
* [ ] Rename `~/.bashrc` to `~/.bash_logout`
* [ ] Add `export` in front of each alias

> **Explanation:** SSH starts a login shell, which reads `~/.bash_profile` rather than `~/.bashrc`. Adding `if [ -f ~/.bashrc ]; then . ~/.bashrc; fi` to `~/.bash_profile` gives both kinds of shell the same settings.

#### Q. Which file does Bash run when a login shell exits?

* [ ] `~/.bashrc`
* [ ] `~/.bash_profile`
* [x] `~/.bash_logout`
* [ ] `~/.profile`

> **Explanation:** `~/.bash_logout` runs when a login shell exits, which makes it handy for cleanup such as clearing the screen.

#### Q. You edited `~/.bashrc` to add an alias. How do you apply it to the current shell without opening a new terminal?

* [ ] `bash ~/.bashrc`
* [x] `source ~/.bashrc`
* [ ] `./.bashrc`
* [ ] `export ~/.bashrc`

> **Explanation:** `source` (or `.`) runs the file inside the current shell, so its aliases and variables stay defined. `bash ~/.bashrc` runs it in a child process whose changes vanish when it exits.

#### Q. A script run with `bash` exports a new value. What does the parent shell print afterwards?

```bash
export TOKEN=old
cat > change.sh <<'EOF'
export TOKEN=new
EOF
bash change.sh
echo "$TOKEN"
```

* [x] `old`
* [ ] `new`
* [ ] An empty line
* [ ] `TOKEN`

> **Explanation:** `bash change.sh` runs in a child process. A child gets a copy of the parent's environment and cannot change the parent's copy. Using `source change.sh` would print `new`.

#### Q. Why must a Python virtual environment be activated with `source venv/bin/activate`, not by running `./venv/bin/activate`?

* [ ] The `activate` file is not marked executable
* [x] It must change `PATH` in the current shell, which a child process cannot do
* [ ] Running it directly would install packages globally
* [ ] `source` gives the script root privileges

> **Explanation:** `activate` works by changing variables such as `PATH` and `VIRTUAL_ENV`. Only code that runs in the current shell, by being sourced, can change that shell's environment.

#### Q. What does this print, given the difference between `( )` and `{ }`?

```bash
COLOR=blue
( COLOR=red )
echo "$COLOR"
{ COLOR=green; }
echo "$COLOR"
```

* [ ] `red` then `green`
* [x] `blue` then `green`
* [ ] `blue` then `blue`
* [ ] `red` then `red`

> **Explanation:** Parentheses run commands in a subshell, so its assignment is lost. Braces group commands in the current shell, so `green` sticks. Braces need spaces and a trailing `;` before `}`.

#### Q. What does `printenv` show for a variable that was set but never exported?

```bash
count=5
printenv count
```

* [ ] It prints `5`
* [x] It prints nothing, because `count` is a shell variable that was not exported
* [ ] It prints `count=5`
* [ ] It fails with a syntax error

> **Explanation:** `printenv` is an external program and sees only exported variables. Run `export count` first. `echo "$count"` would still print `5`, because the shell expands the variable itself.

#### Q. What does `DEBUG=1 ./app` do?

* [ ] Sets `DEBUG` permanently in the current shell and runs `./app`
* [x] Puts `DEBUG=1` in the environment of `./app` only
* [ ] Runs `./app` with debug tracing turned on in Bash
* [ ] Fails, because `export` is required

> **Explanation:** A `NAME=value` prefix adds the variable to that one command's environment. Afterwards `echo "$DEBUG"` in the shell prints nothing.

#### Q. Which line adds `~/bin` to the front of the command search path for this shell and its children?

* [ ] `PATH=~/bin`
* [x] `export PATH="$HOME/bin:$PATH"`
* [ ] `export PATH="$PATH;$HOME/bin"`
* [ ] `set PATH=$HOME/bin:$PATH`

> **Explanation:** `PATH` entries are separated by colons and searched left to right, so prepending puts `~/bin` first. `PATH=~/bin` throws away the existing directories, and `;` is not a separator on Linux.

#### Q. What does `env -i bash --norc` give you?

* [ ] A Bash shell that runs as root
* [x] A new Bash process with an empty environment
* [ ] A copy of the current shell, including its unexported variables
* [ ] A Bash shell that ignores `PATH` lookups

> **Explanation:** `env -i` clears the environment before starting the command. This is useful for checking whether a script secretly depends on your personal variables.

#### Q. What does `readonly MAX_RETRIES=5` followed by `MAX_RETRIES=3` do?

* [ ] Silently keeps the value `5`
* [x] Fails with `MAX_RETRIES: readonly variable`
* [ ] Changes the value to `3` and prints a warning
* [ ] Changes the value to `3` only in child processes

> **Explanation:** Read-only variables cannot be reassigned or `unset` in that shell, so Bash reports an error. This is useful for constants in scripts.

#### Q. A script starts with `: "${API_KEY:?API_KEY is required}"`. What happens if `API_KEY` is unset?

* [ ] `API_KEY` is set to the text `API_KEY is required`
* [x] The script prints the message to stderr and exits with a non-zero status
* [ ] The line is ignored, because `:` is a comment
* [ ] The script prompts the user to type a value

> **Explanation:** `${VAR:?msg}` aborts a non-interactive shell with `msg` if `VAR` is unset or empty. `:` is a no-op command that still expands its arguments, so the check runs.

#### Q. What does this print when using the `${x:-7}` default-value expansion?

```bash
x=5; echo "${x:-7}"; unset x; echo "${x:-7}"
```

* [ ] `5` then nothing
* [x] `5` then `7`
* [ ] `7` then `7`
* [ ] `x:-7` then `x:-7`

> **Explanation:** `${x:-7}` uses the default `7` only when `x` is unset or empty, and does not assign it. The `${x:=7}` form would also store `7` in `x`.

#### Q. Which shebang finds `bash` through the user's `PATH`, so the script works where Bash is not at `/bin/bash`?

* [ ] `#!/bin/sh`
* [x] `#!/usr/bin/env bash`
* [ ] `#!bash`
* [ ] `# /usr/bin/bash`

> **Explanation:** `env` searches `PATH` for `bash`, which helps on systems such as FreeBSD or macOS with Homebrew. `#!/bin/sh` may be Dash, which lacks Bash features. A shebang needs `#!` followed by the interpreter's full path.

#### Q. A script `deploy.sh` has a valid shebang. What lets you run it as `./deploy.sh`?

* [ ] `bash deploy.sh`
* [x] `chmod +x deploy.sh`
* [ ] `source deploy.sh`
* [ ] `export deploy.sh`

> **Explanation:** The kernel will only `execve` the file if it has execute permission; it then reads the shebang to pick the interpreter. `bash deploy.sh` runs the script without needing `+x`, but that is not `./deploy.sh`.

#### Q. A script is run as `./greet.sh Ann Bob`. Inside it, what are `$0`, `$1` and `$#`?

* [ ] `Ann`, `Bob`, `2`
* [x] `./greet.sh`, `Ann`, `2`
* [ ] `./greet.sh`, `Ann`, `3`
* [ ] `greet.sh`, `Bob`, `1`

> **Explanation:** `$0` is the name the script was invoked by, `$1` is the first argument, and `$#` counts the arguments, not including `$0`.

#### Q. What does this print, comparing `"$@"` with `"$*"`?

```bash
count() { echo "$#"; }
set -- "a b" c
count "$@"; count "$*"
```

* [ ] `3` then `3`
* [x] `2` then `1`
* [ ] `1` then `2`
* [ ] `2` then `2`

> **Explanation:** `"$@"` expands to each argument as a separate word, keeping `a b` intact, so you get 2. `"$*"` joins every argument into one string, so you get 1. Use `"$@"` to pass arguments through safely.

#### Q. What do `$?`, `$$` and `$!` hold?

* [ ] The PID of the last background job, the exit status, and the shell's PID
* [x] The last command's exit status, the current shell's PID, and the PID of the last background job
* [ ] The argument count, the shell's PID, and the last exit status
* [ ] The current shell's PID, the parent's PID, and the last exit status

> **Explanation:** `$?` is `0` on success and non-zero on failure. `$$` is the shell's own PID, and `$!` is set when you start something with `&`, which makes it useful with `wait "$!"`.

#### Q. What does `echo "Today is $(date +%A)"` do?

* [ ] Prints the text `$(date +%A)` literally
* [x] Runs `date +%A` and puts its output into the string
* [ ] Starts `date` in the background
* [ ] Stores the output of `date` in a variable called `A`

> **Explanation:** `$(...)` is command substitution: the command's stdout, without trailing newlines, replaces the expression. Backticks do the same thing but are harder to nest.

#### Q. With `name=World`, what does `echo 'Hello $name'` print?

* [ ] `Hello World`
* [x] `Hello $name`
* [ ] `Hello`
* [ ] `'Hello World'`

> **Explanation:** Single quotes keep every character literal. Double quotes, as in `"Hello $name"`, still expand variables and command substitutions but prevent word splitting and globbing.

#### Q. Which alias definition makes `ll` run `ls -la`?

* [ ] `alias ll ls -la`
* [x] `alias ll='ls -la'`
* [ ] `alias ll=ls -la`
* [ ] `set ll='ls -la'`

> **Explanation:** There must be no spaces around `=`, and the value needs quotes because it contains a space. `alias` with no arguments lists all aliases, and `unalias ll` removes one.

#### Q. You want a shortcut `backup notes.txt` that copies a file to `notes.txt.bak`. Why use a function instead of an alias?

* [ ] Aliases cannot contain the `cp` command
* [x] A function can use its argument as `$1` anywhere in its body
* [ ] Functions run faster because they are compiled
* [ ] Aliases are deleted when the terminal is resized

> **Explanation:** An alias is only text substitution at the start of a command, so it cannot reuse an argument. `backup() { cp -- "$1" "$1.bak"; }` can. Use aliases for simple shortcuts and functions for logic.

#### Q. Which of these is a valid Bash function definition?

* [ ] `def greet { echo hi; }`
* [x] `greet() { echo "hi $1"; }`
* [ ] `greet() { echo "hi $1" }`
* [ ] `function greet() echo "hi $1"`

> **Explanation:** The body is a brace group, which needs a space after `{` and a `;` or newline before `}`. Without the semicolon, Bash keeps reading and reports a syntax error.

#### Q. In `PS1='\u@\h:\w\$ '`, what do `\u`, `\h` and `\w` expand to?

* [ ] User ID, home directory, and time
* [x] Username, hostname, and current working directory
* [ ] Uptime, history number, and window title
* [ ] Username, home directory, and week day

> **Explanation:** `PS1` is the primary prompt. `\$` shows `$` for normal users and `#` for root.

#### Q. What is the difference between `HISTSIZE` and `HISTFILESIZE`?

* [ ] They are aliases for the same setting
* [x] `HISTSIZE` limits commands kept in memory; `HISTFILESIZE` limits lines saved in `~/.bash_history`
* [ ] `HISTSIZE` is in kilobytes; `HISTFILESIZE` is in lines
* [ ] `HISTSIZE` applies to root; `HISTFILESIZE` applies to normal users

> **Explanation:** During a session, Bash keeps up to `HISTSIZE` commands. When the shell exits, the history file is cut down to `HISTFILESIZE` lines.

#### Q. In an interactive Bash shell, what does `sudo !!` do?

* [ ] Runs `sudo` with no arguments twice
* [x] Re-runs the previous command with `sudo` in front
* [ ] Opens the history list in an editor
* [ ] Repeats the last command that used `sudo`

> **Explanation:** `!!` is history expansion for the previous command line. `!$` expands to the last argument of the previous command.

#### Q. Which redirection sends both stdout and stderr of `make` to `build.log`, overwriting the file?

* [ ] `make 2>&1 > build.log`
* [x] `make > build.log 2>&1`
* [ ] `make >> build.log 2>build.log`
* [ ] `make | build.log`

> **Explanation:** Redirections are processed left to right: stdout goes to the file, then stderr is pointed at the same place. `2>&1 > build.log` points stderr at the old stdout (the terminal) first. Bash's `&> build.log` is a shorter form.

#### Q. Which command adds a line to the end of `notes.txt` instead of replacing its contents?

* [ ] `echo "done" > notes.txt`
* [x] `echo "done" >> notes.txt`
* [ ] `echo "done" < notes.txt`
* [ ] `echo "done" 2> notes.txt`

> **Explanation:** `>>` appends, while `>` truncates the file first. `<` redirects input, and `2>` redirects only stderr.

#### Q. How do you run `find / -name core` and throw away its "Permission denied" messages, while still seeing the results?

* [ ] `find / -name core > /dev/null`
* [x] `find / -name core 2>/dev/null`
* [ ] `find / -name core &> /dev/null`
* [ ] `find / -name core | /dev/null`

> **Explanation:** Error messages go to file descriptor 2, so `2>/dev/null` discards just those. `> /dev/null` would discard the results, and `&>` would discard both streams.

#### Q. Which command shows output on screen and also appends it to `run.log`?

* [ ] `./run.sh > run.log`
* [x] `./run.sh | tee -a run.log`
* [ ] `./run.sh | tee run.log > /dev/null`
* [ ] `./run.sh >> run.log 2>&1`

> **Explanation:** `tee` copies stdin to the screen and to a file, and `-a` appends instead of overwriting. The redirect-only versions show nothing on screen.

#### Q. What does this here-document print when its delimiter is quoted?

```bash
name=World
cat <<'EOF'
Hello $name
EOF
```

* [ ] `Hello World`
* [x] `Hello $name`
* [ ] `Hello`
* [ ] It fails because the delimiter is quoted

> **Explanation:** Quoting the here-document delimiter (`'EOF'`) turns off expansion in the body. With an unquoted `EOF`, the shell would expand `$name` and print `Hello World`.

#### Q. What does `diff <(ls dir1) <(ls dir2)` do?

* [ ] Compares two files literally named `ls dir1` and `ls dir2`
* [x] Compares the outputs of the two `ls` commands as if they were files
* [ ] Copies `dir1` into `dir2`, then compares them
* [ ] Fails, because `diff` cannot read from pipes

> **Explanation:** Process substitution `<(cmd)` runs the command and passes a path such as `/dev/fd/63` that reads its output. That lets programs that expect filenames read command output.

#### Q. What does `set -e` change in a script?

* [ ] It echoes each command before running it
* [x] The script exits when a command fails, outside tests such as `if` or `&&`
* [ ] It exports every variable to child processes
* [ ] It makes unset variables an error

> **Explanation:** `set -e` (errexit) stops the script at the first unchecked failure. Commands used as conditions are exempt. Tracing is `set -x`, and unset-variable errors are `set -u`.

#### Q. What does this script do when it uses an unset variable?

```bash
#!/usr/bin/env bash
set -u
echo "Count is $count"
echo "after"
```

* [ ] `Count is ` then `after`
* [x] An error like `count: unbound variable`, and the script stops
* [ ] `Count is $count` then `after`
* [ ] `Count is 0` then `after`

> **Explanation:** `set -u` (nounset) makes expanding an unset variable an error, which ends a non-interactive shell. Without it, `$count` silently becomes an empty string and hides the bug.

#### Q. What does this print, before and after enabling `pipefail`?

```bash
false | true; echo $?
set -o pipefail
false | true; echo $?
```

* [ ] `1` then `1`
* [x] `0` then `1`
* [ ] `0` then `0`
* [ ] `1` then `0`

> **Explanation:** A pipeline's status is normally that of its last command, so the failing `false` is hidden. With `pipefail`, a pipeline fails if any command in it fails.

#### Q. Which line is the usual "strict mode" at the top of a Bash script: exit on error, error on unset variables, and fail pipelines on any error?

* [ ] `set -ex`
* [ ] `set -eu`
* [x] `set -euo pipefail`
* [ ] `set +euo pipefail`

> **Explanation:** `-e` exits on unchecked errors, `-u` treats unset variables as errors, and `-o pipefail` makes pipeline failures visible. A `+` prefix turns options off instead of on.

#### Q. What does `set -x` do?

* [ ] Exits the script on the first error
* [x] Prints each command, after expansion, before it runs
* [ ] Marks the script as executable
* [ ] Exports every new variable

> **Explanation:** `set -x` (xtrace) prints each command to stderr with a `+` prefix, which is useful for debugging. Turn it off again with `set +x`.

#### Q. What does this `trap` line do in a script?

```bash
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
```

* [ ] Deletes the temporary file immediately
* [x] Removes the temporary file whenever the script exits, including after an error
* [ ] Stops the script from being interrupted with Ctrl+C
* [ ] Prevents other users from reading the temporary file

> **Explanation:** `trap COMMAND EXIT` runs the command when the shell exits for any reason. `trap` can also handle signals such as `INT` or `TERM`, which makes it the standard cleanup tool.
