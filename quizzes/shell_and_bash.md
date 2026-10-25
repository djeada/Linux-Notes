# Shell and Bash Quiz

Notes: [Shells and Terminals](../notes/shells_and_bash_configuration.md), [Variables](../notes/environment_variable.md), [Data Streams](../notes/pipe_and_redirect.md)

Check your understanding of Bash startup files, variables and the environment, quoting, redirection and safe scripting. Unless a question says otherwise, the shell is Bash 5 on Linux.

#### Q. What is the difference between a terminal and a shell?

* [ ] They are two names for the same program
* [ ] The shell draws the window; the terminal runs the commands
* [x] The terminal is the window you type into; the shell interprets the commands
* [ ] A terminal is used only for remote sessions, a shell only for local ones

> **Explanation:** A terminal emulator such as GNOME Terminal or xterm provides the window and keyboard input. The shell (Bash, Zsh, and so on) runs inside it, parses commands and starts programs.

#### Q. Which file lists the shells that may be used as login shells, and is checked by `chsh`?

* [ ] `/etc/passwd`
* [ ] `/etc/login.defs`
* [ ] `/etc/bash.bashrc`
* [x] `/etc/shells`

> **Explanation:** `chsh -s /bin/zsh` normally refuses a shell that is not listed in `/etc/shells`. Each user's chosen login shell is then stored in the last field of their `/etc/passwd` entry.

#### Q. Your login shell is Bash, but you have just typed `zsh` to try it out. Which command reliably shows the shell you are running right now?

* [ ] `echo "$SHELL"`
* [ ] `cat /etc/shells`
* [ ] `echo "$PATH"`
* [x] `ps -p "$$" -o comm=`

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
* [ ] `~/.bash_logout`
* [x] `~/.bashrc`
* [ ] `/etc/profile`

> **Explanation:** Interactive non-login shells read `~/.bashrc`, often after a system-wide file such as `/etc/bash.bashrc`. Aliases, functions and prompt settings usually live there.

#### Q. Aliases defined in `~/.bashrc` are missing when you log in over SSH. What is the usual fix?

* [x] Source `~/.bashrc` from `~/.bash_profile`
* [ ] Move the aliases into `/etc/shells`
* [ ] Rename `~/.bashrc` to `~/.bash_logout`
* [ ] Add `export` in front of each alias

> **Explanation:** SSH starts a login shell, which reads `~/.bash_profile` rather than `~/.bashrc`. Adding `if [ -f ~/.bashrc ]; then . ~/.bashrc; fi` to `~/.bash_profile` gives both kinds of shell the same settings.

#### Q. Which file does Bash run when an interactive login shell exits?

* [ ] `~/.bashrc`
* [ ] `~/.bash_profile`
* [x] `~/.bash_logout`
* [ ] `~/.profile`

> **Explanation:** `~/.bash_logout` runs when a login shell exits, which makes it handy for cleanup such as clearing the screen. Non-login shells, such as a new terminal tab on most desktops, do not read it.

#### Q. You edited `~/.bashrc` to add an alias. How do you apply it to the current shell without opening a new terminal?

* [ ] `bash ~/.bashrc`
* [x] `source ~/.bashrc`
* [ ] `./.bashrc`
* [ ] `export ~/.bashrc`

> **Explanation:** `source` (or `.`) runs the file inside the current shell, so its aliases and variables stay defined. `bash ~/.bashrc` runs it in a child process whose changes vanish when it exits.

#### Q. What does this print?

```bash
export MODE=dev
bash -c 'MODE=prod; exec sh -c "echo child: \$MODE"'
echo "parent: $MODE"
```

* [ ] `child: dev` then `parent: dev`
* [ ] `child: prod` then `parent: prod`
* [ ] `child: dev` then `parent: prod`
* [x] `child: prod` then `parent: dev`

> **Explanation:** The inner `bash` gets its own copy of the environment, and `exec` keeps that copy because it replaces the program, not the process. Nothing a child does reaches the parent's copy, so the parent still prints `dev`.

#### Q. A cron job must run `/srv/app/app.py` with the packages installed in `/srv/app/.venv`. Which command does that without activating the venv?

* [x] `/srv/app/.venv/bin/python /srv/app/app.py`
* [ ] `VIRTUAL_ENV=/srv/app/.venv python3 /srv/app/app.py`
* [ ] `/srv/app/.venv/bin/activate && python3 /srv/app/app.py`
* [ ] `python3 -m venv /srv/app/.venv /srv/app/app.py`

> **Explanation:** The venv's own interpreter already uses the venv's `site-packages`; activation only puts `.venv/bin` first on `PATH`. Setting `VIRTUAL_ENV` alone does not change `python3`, and `activate` is not executable, so running it fails.

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

* [x] Nothing, because `count` was never exported
* [ ] `5`, because `printenv` reads shell variables
* [ ] `count=5`, in `NAME=value` form
* [ ] A syntax error, because it needs `$count`

> **Explanation:** `printenv` is an external program and sees only exported variables. Run `export count` first. `echo "$count"` would still print `5`, because the shell expands the variable itself.

#### Q. What does `DEBUG=1 ./app` do?

* [x] Puts `DEBUG=1` in the environment of `./app` only
* [ ] Sets `DEBUG` permanently in the current shell and runs `./app`
* [ ] Runs `./app` with debug tracing turned on in Bash
* [ ] Fails, because `export` is required

> **Explanation:** A `NAME=value` prefix adds the variable to that one command's environment. Afterwards `echo "$DEBUG"` in the shell prints nothing.

#### Q. Which line adds `~/bin` to the front of the command search path for this shell and its children?

* [ ] `PATH=~/bin`
* [ ] `export PATH="$PATH;$HOME/bin"`
* [ ] `set PATH=$HOME/bin:$PATH`
* [x] `export PATH="$HOME/bin:$PATH"`

> **Explanation:** `PATH` entries are separated by colons and searched left to right, so prepending puts `~/bin` first. `PATH=~/bin` throws away the existing directories, and `;` is not a separator on Linux.

#### Q. What does `env -i bash --norc` give you?

* [ ] A Bash shell that runs as root
* [x] A new Bash shell that starts with no inherited environment variables
* [ ] A copy of the current shell, including its unexported variables
* [ ] A Bash shell that ignores `PATH` lookups

> **Explanation:** `env -i` clears the environment before starting the command; Bash then sets only a few variables itself, such as `PWD` and `SHLVL`. This shows whether a script secretly depends on your personal variables.

#### Q. What does `readonly MAX_RETRIES=5` followed by `MAX_RETRIES=3` do?

* [x] Fails with `MAX_RETRIES: readonly variable`
* [ ] Silently keeps the value `5`
* [ ] Changes the value to `3` and prints a warning
* [ ] Changes the value to `3` only in child processes

> **Explanation:** Read-only variables cannot be reassigned or `unset` in that shell, so Bash reports an error and the value stays `5`. This is useful for constants in scripts.

#### Q. A script starts with `: "${API_KEY:?API_KEY is required}"`. What happens if `API_KEY` is unset?

* [ ] `API_KEY` is set to the text `API_KEY is required` and the script goes on
* [ ] The line is ignored, because `:` is a comment
* [ ] The script prompts the user to type a value
* [x] The script prints the message to stderr and exits with a non-zero status

> **Explanation:** `${VAR:?msg}` aborts a non-interactive shell with `msg` if `VAR` is unset or empty. `:` is a no-op command that still expands its arguments, so the check runs.

#### Q. What does this print when using the `${x:-7}` default-value expansion?

```bash
x=5; echo "${x:-7}"; unset x; echo "${x:-7}"
```

* [ ] `5` then nothing
* [ ] `7` then `7`
* [x] `5` then `7`
* [ ] `x:-7` then `x:-7`

> **Explanation:** `${x:-7}` uses the default `7` only when `x` is unset or empty, and does not assign it. The `${x:=7}` form would also store `7` in `x`.

#### Q. Which shebang finds `bash` through the user's `PATH`, so the script works where Bash is not at `/bin/bash`?

* [x] `#!/usr/bin/env bash`
* [ ] `#!/bin/sh`
* [ ] `#!bash`
* [ ] `# /usr/bin/bash`

> **Explanation:** `env` searches `PATH` for `bash`, which helps on systems such as FreeBSD or macOS with Homebrew. `#!/bin/sh` may be Dash, which lacks Bash features, and the kernel never searches `PATH` for a shebang interpreter, so `#!bash` fails.

#### Q. A script `deploy.sh` has a valid shebang. What lets you run it as `./deploy.sh`?

* [ ] `bash deploy.sh`
* [x] `chmod +x deploy.sh`
* [ ] `source deploy.sh`
* [ ] `export deploy.sh`

> **Explanation:** Without execute permission, `./deploy.sh` fails with `Permission denied`; with it, the kernel reads the shebang to pick the interpreter. `bash deploy.sh` runs the script without needing `+x`, but that is not `./deploy.sh`.

#### Q. A script is run as `./greet.sh Ann Bob`. Inside it, what are `$0`, `$1` and `$#`?

* [x] `./greet.sh`, `Ann`, `2`
* [ ] `Ann`, `Bob`, `2`
* [ ] `./greet.sh`, `Ann`, `3`
* [ ] `greet.sh`, `Bob`, `1`

> **Explanation:** `$0` is the name the script was invoked by, `$1` is the first argument, and `$#` counts the arguments, not including `$0`.

#### Q. What does this print, comparing `"$@"` with `"$*"`?

```bash
count() { echo "$#"; }
set -- "a b" c
count "$@"; count "$*"
```

* [x] `2` then `1`
* [ ] `3` then `3`
* [ ] `1` then `2`
* [ ] `2` then `2`

> **Explanation:** `"$@"` expands to each argument as a separate word, keeping `a b` intact, so you get 2. `"$*"` joins every argument into one string, so you get 1. Use `"$@"` to pass arguments through safely.

#### Q. What do `$?`, `$$` and `$!` hold?

* [ ] The PID of the last background job, the exit status, and the shell's PID
* [ ] The argument count, the shell's PID, and the last exit status
* [x] The last command's exit status, the current shell's PID, and the PID of the last background job
* [ ] The current shell's PID, the parent's PID, and the last exit status

> **Explanation:** `$?` is `0` on success and non-zero on failure. `$$` is the shell's own PID, and `$!` is set when you start something with `&`, which makes it useful with `wait "$!"`.

#### Q. In Bash, the first line below prints `4100 4100`. What does the second line print?

```bash
echo "$$ $BASHPID"
( echo "$$ $BASHPID" )
```

* [ ] `4100 4100`
* [ ] A new PID twice, such as `4105 4105`
* [x] `4100` followed by a different PID, such as `4100 4105`
* [ ] A new PID followed by `4100`, such as `4105 4100`

> **Explanation:** `$$` always expands to the PID of the main shell, even inside a subshell, while `$BASHPID` is the PID of the process actually running the code. Use `$BASHPID` when a subshell needs its own PID.

#### Q. What does `echo "Today is $(date +%A)"` do?

* [ ] Prints the text `$(date +%A)` literally
* [ ] Starts `date` in the background
* [ ] Stores the output of `date` in a variable called `A`
* [x] Runs `date +%A` and puts its output into the string

> **Explanation:** `$(...)` is command substitution: the command's stdout, without trailing newlines, replaces the expression. Backticks do the same thing but are harder to nest.

#### Q. With `name=World`, what does `echo 'Hello $name'` print?

* [ ] `Hello World`
* [ ] `Hello`
* [ ] `'Hello World'`
* [x] `Hello $name`

> **Explanation:** Single quotes keep every character literal. Double quotes, as in `"Hello $name"`, still expand variables and command substitutions but prevent word splitting and globbing.

#### Q. You run this in an otherwise empty directory. What happens?

```bash
f="my file.txt"
touch "$f"
rm $f
```

* [ ] `rm` deletes `my file.txt`, because `$f` holds the whole name
* [ ] `rm` deletes every file in the directory, because the space acts as a wildcard
* [x] `rm` gets the two arguments `my` and `file.txt`, fails on both, and `my file.txt` remains
* [ ] Bash refuses to run `rm`, because an unquoted `$f` contains a space

> **Explanation:** An unquoted expansion is split into words on `IFS` characters and then globbed, so `$f` becomes two arguments. Write `rm -- "$f"` to pass the name as a single argument.

#### Q. What does this print?

```bash
data="red,green,blue"
IFS=, read -r first second third <<< "$data"
echo "$second"
printf '%q\n' "$IFS"
```

* [ ] `green` then `,`
* [ ] `red,green,blue` then `$' \t\n'`
* [ ] An empty line then `,`
* [x] `green` then `$' \t\n'`

> **Explanation:** A `VAR=value` prefix on `read` sets `IFS` for that one command, so the line is split on commas while the shell's `IFS` keeps its default of space, tab and newline. Changing `IFS` globally can break later commands.

#### Q. Which alias definition makes `ll` run `ls -la`?

* [ ] `alias ll ls -la`
* [ ] `alias ll=ls -la`
* [x] `alias ll='ls -la'`
* [ ] `set ll='ls -la'`

> **Explanation:** There must be no spaces around `=`, and the value needs quotes because it contains a space. `alias` with no arguments lists all aliases, and `unalias ll` removes one.

#### Q. What happens when you run this script with `bash script.sh`?

```bash
#!/usr/bin/env bash
alias ll='ls -la'
ll
```

* [x] It fails with `ll: command not found`, as scripts do not expand aliases
* [ ] It runs `ls -la`, because the alias is defined before it is used
* [ ] It prints the definition `alias ll='ls -la'`
* [ ] It fails with a syntax error on the `alias` line

> **Explanation:** Bash expands aliases only in interactive shells unless `shopt -s expand_aliases` is set. In scripts, use a function such as `ll() { ls -la "$@"; }` instead.

#### Q. You want a shortcut `backup notes.txt` that copies a file to `notes.txt.bak`. Why use a function instead of an alias?

* [ ] Aliases cannot contain the `cp` command
* [x] A function can use its argument as `$1` anywhere in its body
* [ ] Functions run faster because they are compiled
* [ ] Aliases are deleted when the terminal is resized

> **Explanation:** An alias is only text substitution at the start of a command, so it cannot reuse an argument. `backup() { cp -- "$1" "$1.bak"; }` can. Use aliases for simple shortcuts and functions for logic.

#### Q. Which of these is a valid Bash function definition?

* [x] `greet() { echo "hi $1"; }`
* [ ] `def greet { echo hi; }`
* [ ] `greet() { echo "hi $1" }`
* [ ] `function greet() echo "hi $1"`

> **Explanation:** The body is a brace group, which needs a space after `{` and a `;` or newline before `}`. Without the semicolon, Bash keeps reading and reports a syntax error.

#### Q. In `PS1='\u@\h:\w\$ '`, what do `\u`, `\h` and `\w` expand to?

* [x] Username, hostname, and current working directory
* [ ] User ID, home directory, and time
* [ ] Uptime, history number, and window title
* [ ] Username, home directory, and week day

> **Explanation:** `PS1` is the primary prompt. `\h` is the hostname up to the first dot, and `\$` shows `$` for normal users and `#` for root.

#### Q. What is the difference between `HISTSIZE` and `HISTFILESIZE`?

* [ ] They are two names for the same setting, kept for compatibility
* [x] `HISTSIZE` limits commands kept in memory; `HISTFILESIZE` limits lines saved in `~/.bash_history`
* [ ] `HISTSIZE` is measured in kilobytes; `HISTFILESIZE` is in lines
* [ ] `HISTSIZE` applies to root; `HISTFILESIZE` applies to other users

> **Explanation:** During a session, Bash keeps up to `HISTSIZE` commands. When the shell exits, the history file is cut down to `HISTFILESIZE` lines.

#### Q. In an interactive Bash shell, what does `sudo !!` do?

* [ ] Runs `sudo` with no arguments twice
* [x] Re-runs the previous command with `sudo` in front
* [ ] Opens the history list in an editor
* [ ] Repeats the last command that used `sudo`

> **Explanation:** `!!` is history expansion for the previous command line, and Bash echoes the expanded command before running it. `!$` expands to the last argument of the previous command. Scripts have history expansion turned off.

#### Q. Which redirection sends both stdout and stderr of `make` to `build.log`, overwriting the file?

* [ ] `make 2>&1 > build.log`
* [ ] `make >> build.log 2>build.log`
* [ ] `make | build.log`
* [x] `make > build.log 2>&1`

> **Explanation:** Redirections are processed left to right: stdout goes to the file, then stderr is pointed at the same place. `2>&1 > build.log` points stderr at the old stdout (the terminal) first. Bash's `&> build.log` is a shorter form.

#### Q. Which command adds a line to the end of `notes.txt` instead of replacing its contents?

* [ ] `echo "done" > notes.txt`
* [ ] `echo "done" < notes.txt`
* [x] `echo "done" >> notes.txt`
* [ ] `echo "done" 2> notes.txt`

> **Explanation:** `>>` appends, while `>` truncates the file first. `<` redirects input, and `2>` redirects only stderr.

#### Q. How do you run `find / -name core` and throw away its "Permission denied" messages, while still seeing the results?

* [ ] `find / -name core > /dev/null`
* [ ] `find / -name core &> /dev/null`
* [ ] `find / -name core | /dev/null`
* [x] `find / -name core 2>/dev/null`

> **Explanation:** Error messages go to file descriptor 2, so `2>/dev/null` discards just those. `> /dev/null` would discard the results, and `&>` would discard both streams.

#### Q. Which command shows output on screen and also appends it to `run.log`?

* [ ] `./run.sh > run.log`
* [ ] `./run.sh | tee run.log > /dev/null`
* [x] `./run.sh | tee -a run.log`
* [ ] `./run.sh >> run.log 2>&1`

> **Explanation:** `tee` copies stdin to the screen and to a file, and `-a` appends instead of overwriting. The redirect-only versions show nothing on screen.

#### Q. Which Bash command shows both the output and the error messages of `make` on screen and also saves both to `build.log`?

* [ ] `make | tee build.log`
* [x] `make |& tee build.log`
* [ ] `make &> build.log`
* [ ] `make | tee 2> build.log`

> **Explanation:** `|&` is Bash shorthand for `2>&1 |`, so both streams enter the pipe and `tee` copies them to the screen and the file. A plain `|` carries only stdout, so error messages bypass `tee` and are not saved.

#### Q. A `#!/bin/sh` script on Ubuntu, where `/bin/sh` is Dash, contains this line. What happens?

```sh
echo hi &> out.log
```

* [ ] Both stdout and stderr of `echo` go to `out.log`, as in Bash
* [x] `echo hi` runs in the background, and `out.log` is created empty
* [ ] Dash stops with a syntax error at `&>`
* [ ] Only stderr of `echo` goes to `out.log`

> **Explanation:** POSIX sh has no `&>` operator, so Dash reads `echo hi &` followed by `> out.log`, an empty command whose redirection truncates the file. The portable form is `echo hi > out.log 2>&1`.

#### Q. What does this here-document print when its delimiter is quoted?

```bash
name=World
cat <<'EOF'
Hello $name
EOF
```

* [ ] `Hello World`
* [ ] `Hello`
* [x] `Hello $name`
* [ ] It fails because the delimiter is quoted

> **Explanation:** Quoting the here-document delimiter (`'EOF'`) turns off expansion in the body. With an unquoted `EOF`, the shell would expand `$name` and print `Hello World`.

#### Q. What does `diff <(ls dir1) <(ls dir2)` do?

* [ ] Compares two files literally named `ls dir1` and `ls dir2`
* [ ] Copies `dir1` into `dir2`, then compares them
* [x] Compares the outputs of the two `ls` commands as if they were files
* [ ] Fails, because `diff` cannot read from pipes

> **Explanation:** Process substitution `<(cmd)` runs the command and passes a path such as `/dev/fd/63` that reads its output. That lets programs that expect filenames read command output. It is a Bash feature; Dash reports a syntax error.

#### Q. What does `set -e` change in a script?

* [ ] It echoes each command to stderr before running it
* [x] The script exits when a command fails, outside tests such as `if` or `&&`
* [ ] It exports every variable it sets to child processes
* [ ] It turns expanding an unset variable into an error

> **Explanation:** `set -e` (errexit) stops the script at the first unchecked failure. Commands used as conditions are exempt. Tracing is `set -x`, and unset-variable errors are `set -u`.

#### Q. What does this script print?

```bash
#!/usr/bin/env bash
set -e
count=0
((count++))
echo "count is $count"
```

* [x] Nothing: the script exits with status 1 at `((count++))`
* [ ] `count is 1`, because `count++` succeeds
* [ ] `count is 0`, because `count++` is a post-increment
* [ ] An `unbound variable` error for `count`

> **Explanation:** `count++` evaluates to the old value, 0, and an arithmetic command whose value is 0 returns status 1, so `set -e` ends the script silently. `count=$((count + 1))` always succeeds.

#### Q. What does this script print?

```bash
#!/usr/bin/env bash
set -e
f() { false; echo "in f"; }
f || echo "f failed"
echo "end"
```

* [ ] `f failed` then `end`
* [ ] Nothing, because the script exits at `false`
* [x] `in f` then `end`
* [ ] `in f`, `f failed`, then `end`

> **Explanation:** `set -e` is ignored for everything run as the left side of `||` or `&&`, including commands inside a function called there. So `false` does not stop `f`, `f` returns the `echo` status 0, and `f failed` never prints.

#### Q. What does this script do when it uses an unset variable?

```bash
#!/usr/bin/env bash
set -u
echo "Count is $count"
echo "after"
```

* [ ] `Count is ` then `after`, as `$count` expands to nothing
* [ ] `Count is $count` then `after`, printed literally
* [ ] `Count is 0` then `after`, as unset numbers default to 0
* [x] An error like `count: unbound variable`, and the script stops

> **Explanation:** `set -u` (nounset) makes expanding an unset variable an error, which ends a non-interactive shell. Without it, `$count` silently becomes an empty string and hides the bug.

#### Q. What does this print in Bash, before and after enabling `pipefail`?

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

#### Q. On Ubuntu 24.04, `/bin/sh` is Dash 0.5.12. What happens when you run this script with `sh check.sh`?

```sh
false | true
echo "first: $?"
set -o pipefail
echo "after set"
```

* [ ] It prints `first: 0` and `after set`, ignoring the option
* [ ] It prints `first: 1`, then `after set` on the next line
* [x] It prints `first: 0`, then Dash reports `Illegal option -o pipefail` and exits
* [ ] It fails with a syntax error before running any line

> **Explanation:** This Dash version does not implement `pipefail`, and an error in the special builtin `set` ends a non-interactive shell. Use a `bash` shebang and run the script with Bash when you rely on `pipefail`.

#### Q. Which line is the usual "strict mode" at the top of a Bash script: exit on error, error on unset variables, and fail pipelines on any error?

* [x] `set -euo pipefail`
* [ ] `set -ex`
* [ ] `set -eu`
* [ ] `set +euo pipefail`

> **Explanation:** `-e` exits on unchecked errors, `-u` treats unset variables as errors, and `-o pipefail` makes pipeline failures visible. A `+` prefix turns options off instead of on.

#### Q. What does `set -x` do?

* [x] Prints each command, after expansion, before it runs
* [ ] Exits the script as soon as any command fails
* [ ] Marks the script file as executable for its owner
* [ ] Exports every variable that the script creates

> **Explanation:** `set -x` (xtrace) prints each command to stderr with a `+` prefix, which is useful for debugging. Turn it off again with `set +x`.

#### Q. What does this `trap` line do in a script?

```bash
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
```

* [ ] Deletes the temporary file immediately, before the next line
* [ ] Stops the script from being interrupted with Ctrl+C
* [ ] Prevents other users from reading the temporary file
* [x] Removes the temporary file whenever the script exits, including after an error

> **Explanation:** Bash runs an `EXIT` trap on a normal end, on `exit`, after a `set -e` failure, and when a signal such as `SIGINT` or `SIGTERM` kills the script. Nothing can run after `SIGKILL`, so cleanup is skipped then.

#### Q. You build an image from this Dockerfile with `docker build --build-arg APP_VERSION=1.2.3 -t myapp .` and then run `docker run myapp`. What is printed?

```dockerfile
FROM python:3.12-slim
ARG APP_VERSION
CMD ["python", "-c", "import os; print(os.environ.get('APP_VERSION'))"]
```

* [ ] `1.2.3`
* [x] `None`
* [ ] `APP_VERSION`
* [ ] Nothing, because the build fails without a default for the `ARG`

> **Explanation:** `ARG` values exist only while the image is being built. To keep a non-secret value at runtime, add `ENV APP_VERSION=$APP_VERSION`, or pass it with `docker run -e APP_VERSION=1.2.3`.

#### Q. A Docker build needs a private package token only during one `RUN pip install` step. Which approach keeps the token out of the image's layers and history?

* [ ] `docker build --build-arg PIP_TOKEN=...` with `ARG PIP_TOKEN` used in the `RUN` step
* [ ] `ENV PIP_TOKEN=...` before the `RUN` step and `ENV PIP_TOKEN=` after it
* [ ] `COPY .env .` before the `RUN` step and `RUN rm .env` after it
* [x] `docker build --secret id=pip_token,env=PIP_TOKEN` with `RUN --mount=type=secret,id=pip_token`

> **Explanation:** A BuildKit secret is mounted under `/run/secrets/` only for that `RUN` step and is not saved in a layer. A build arg used by `RUN` shows up in `docker history`, and later `ENV` or `rm` steps cannot erase earlier layers.
